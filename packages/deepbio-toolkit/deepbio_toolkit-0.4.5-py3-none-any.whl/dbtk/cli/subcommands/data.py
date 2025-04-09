import argparse
from collections import Counter
from functools import partial
import hashlib
from itertools import chain
import numpy as np
from pathlib import Path
import pickle
import re
from tqdm import tqdm
from typing import Generator, Iterable, List, Tuple
from typing_extensions import override
import sys
from .._cli import CliSubCommand, subcommand

__doc__ = "Data tools for Deepbio Toolkit"

class SequenceFilter:
    def __init__(self, show_progress: bool):
        self.sequence_index = {}
        self.sequence_count = Counter()
        self.identifier_map = {}
        self.show_progress = show_progress

    def pipe(self, sequence_stream: Iterable[Tuple[str, str]]) -> Generator[str, None, None]:
        if self.show_progress:
            sequence_stream = tqdm(sequence_stream, desc="Analyzing sequences")
        for identifier, sequence in sequence_stream:
            sequence_hash = hashlib.sha256(sequence.encode()).digest()
            seen = sequence_hash in self.sequence_index
            if not seen:
                self.sequence_index[sequence_hash] = len(self.sequence_index)
            self.sequence_count[sequence_hash] += 1
            self.identifier_map[identifier] = self.sequence_index[sequence_hash]
            if not seen:
                yield sequence


@subcommand("import_sequences", "Generate a random run ID.")
class ImportSequences(CliSubCommand):
    @override
    def configure(self, parser):
        parser.add_argument("input_paths", nargs="+", type=Path, help="Input FASTA(s) or FASTQ file(s) containing DNA sequences.")
        parser.add_argument("--output_id_map", "-i", action="store_true", help="Do not output an ID map.")
        parser.add_argument("--output_abundance_map", "-a", action="store_true", help="Do not output an abundance map.")
        parser.add_argument("--output", "-O", type=Path, required=False, help="Path to the output .seq file.")
        parser.add_argument("--silent", "-s", action="store_true", help="Do not show progress bar.")

    def read_fasta(self, path: Path, prefix_sequence_ids: bool) -> Generator[Tuple[str, str], None, None]:
        import gzip
        prefix = ""
        if prefix_sequence_ids:
            prefix = path.name.rstrip(".gz").rstrip(".fasta") + "."
        open_fn = partial(gzip.open, mode="rt") if path.suffix == ".gz" else open
        with open_fn(path) as f:
            identifier = ""
            sequence = ""
            for line in f:
                if line.startswith(">"):
                    if sequence != "":
                        yield prefix+identifier, sequence
                    identifier = re.match(r">(\S+)", line).group(1) # type: ignore
                    sequence = ""
                else:
                    sequence += line.strip()
            if sequence != "":
                yield prefix+identifier, sequence

    def read_fastq(self, path: Path, prefix_sequence_ids: bool) -> Generator[Tuple[str, str], None, None]:
        import gzip
        prefix = ""
        if prefix_sequence_ids:
            # try to extract name from standard fastq format
            match = re.match(r"(.+)_S\d+_L\d+_R\d+_\d+.fastq(?:\.gz)?", path.name)
            if match is not None:
                prefix = match.group(1) + "."
            else:
                prefix = path.name.rstrip(".gz").rstrip(".fastq") + "."
        open_fn = partial(gzip.open, mode="rt") if path.suffix == ".gz" else open
        with open_fn(path) as f:
            prev = ""
            index = 0
            for line in f:
                if line.startswith("+"):
                    yield f"{prefix}{index}", prev.rstrip()
                prev = line

    def read(self, path: Path, prefix_sequence_ids: bool) -> Generator[Tuple[str, str], None, None]:
        if path.name.rstrip(".gz").endswith(".fasta"):
            return self.read_fasta(path, prefix_sequence_ids)
        if path.name.rstrip(".gz").endswith(".fastq"):
            return self.read_fastq(path, prefix_sequence_ids)
        raise ValueError(f"Unsupported file type: {path.suffix}")

    def write(self, config):
        from dbtk.data.formats import SequenceStore
        sequence_filter = SequenceFilter(not config.silent)
        sequence_stream = chain.from_iterable(
            self.read(path, prefix_sequence_ids=(len(config.input_paths) > 1))
            for path in config.input_paths
        )
        SequenceStore.create(
            sequence_filter.pipe(sequence_stream),
            config.output.with_suffix(".seq"),
            show_progress=(not config.silent)
        )
        if not config.silent:
            print("Finishing up...")
        if config.output_id_map:
            with open(config.output.with_suffix(".idmap"), "wb") as f:
                print("Writing", len(sequence_filter.identifier_map), "identifiers to ID map.")
                pickle.dump(sequence_filter.identifier_map, f)
        if config.output_abundance_map:
            with open(config.output.with_suffix(".abundance"), "wb") as f:
                unit = max(int(2**np.ceil(np.log2(np.ceil(np.log2(max(sequence_filter.sequence_count.values()))) + 1e-8))), 8)
                index_dtype = getattr(np, f"uint{unit}")
                counts = np.array(list(sequence_filter.sequence_count.values()), dtype=index_dtype)
                f.write(np.uint8(unit).tobytes() + counts.tobytes())
        if not config.silent:
            print("Analyzed", sum(sequence_filter.sequence_count.values()), "sequences.")
            print("# Unique sequences:", len(sequence_filter.sequence_index))
            print("# Duplicate sequences:", sum(count for count in sequence_filter.sequence_count.values() if count > 1))
            print(f"{1-len(sequence_filter.sequence_index)/sum(sequence_filter.sequence_count.values()):.2%}% sequence reduction")
            print("")

            # print total file size reduction (including abundance and id map if present)
            total_input_size = sum(path.stat().st_size for path in config.input_paths)
            total_output_size = config.output.with_suffix(".seq").stat().st_size
            percent_difference = 1 - total_output_size/total_input_size
            if config.output_id_map:
                total_output_size += config.output.with_suffix(".idmap").stat().st_size
            if config.output_abundance_map:
                total_output_size += config.output.with_suffix(".abundance").stat().st_size
            # determine appropriate units
            units = ["B", "KB", "MB", "GB", "TB"]
            i = 0
            while total_input_size > 1024 and i < len(units):
                total_input_size /= 1024
                i += 1
            print(f"Total input size: {total_input_size:.2f} {units[i]}")
            i = 0
            while total_output_size > 1024 and i < len(units):
                total_output_size /= 1024
                i += 1
            print(f"Total output size: {total_output_size:.2f} {units[i]}")
            print(f"{percent_difference:.2%}% file size reduction")

            print("Done.")

    def run_multiple(self, config: argparse.Namespace) -> int:
        if config.output is None:
            print("Output path is required when importing multiple files.", file=sys.stderr)
            return 1
        if config.output.is_dir():
            print("Output path must be a file when importing multiple files.", file=sys.stderr)
            return 1
        self.write(config)
        return 0

    def run_single(self, config: argparse.Namespace) -> int:
        input_path = config.input_paths[0]
        input_file_name = re.sub(r"\.(fastq|fasta)(\.gz)?$", "", input_path.name)
        if config.output is None:
            # strip fasta/fastq + .gz extension
            config.output = input_path.with_name(input_file_name)
        elif config.output.is_dir():
            config.output = config.output / input_file_name
        self.write(config)
        return 0

    def run(self, config: argparse.Namespace) -> int:
        """
        Import the provided FASTA/FASTQ files into a sequence store.

        Args:
            config (argparse.Namespace): _description_

        Returns:
            int: _description_
        """
        if len(config.input_paths) > 1:
            return self.run_multiple(config)
        return self.run_single(config)
