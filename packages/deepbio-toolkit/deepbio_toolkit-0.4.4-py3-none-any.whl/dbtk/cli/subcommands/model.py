import argparse
import importlib
import inspect
import json
import lightning as L
from lightning.pytorch.callbacks import ModelCheckpoint
from pathlib import Path
import sys
import torch
from transformers import PretrainedConfig, PreTrainedModel
from typing import Any, Dict, Optional, Type
from typing_extensions import override
import yaml

from .._cli import CliSubCommand, subcommand
from ..._utils import load_class
from ...config import parse as parse_config
from ...nn.callbacks import ConfigCheckpoint
from ...nn.models import DbtkModel

@subcommand("config", "Generate a default configuration.")
class ConfigCommand(CliSubCommand):
    @override
    def configure(self, parser):
        parser.add_argument("--model", "-m", type=load_class, help="Generate model configuration.")
        parser.add_argument("--datamodule", "-d", type=load_class, help="Generate datamodule configuration.")
        parser.add_argument("--train", "-t", type=load_class, nargs='?', const=True, default=False,
            help="Generate train configuration. Optionally specify a Lightning Trainer class.")
        parser.add_argument("--test", "-e", action="store_true", default=False, help="Generate test configuration.")
        parser.add_argument("--format", "-f", choices=["yaml", "json"], default="yaml", help="Output format.")

    def _clean_config_dict(self, config: PretrainedConfig, config_dict: Dict[str, Any]) -> None:
        """Recursively clean a config dictionary by removing default values.

        Args:
            config: The PretrainedConfig instance
            config_dict: The dictionary to clean, modified in place
        """
        base_config = PretrainedConfig().to_dict()
        to_exclude = [
            "model_type",
            "is_composition",
            "keys_to_ignore_at_inference",
            "attribute_map",
            "base_model_tp_plan",
            "base_model_pp_plan",
        ]

        # Remove default values from current level
        for key in list(config_dict.keys()):
            if key in to_exclude or (key in base_config and config_dict[key] == base_config[key]):
                del config_dict[key]
            # Recursively clean nested configs
            elif hasattr(config, key):
                attr = getattr(config, key)
                if isinstance(attr, PretrainedConfig):
                    self._clean_config_dict(attr, config_dict[key])

    def _generate_model_config(self, model_cls: Type[DbtkModel]) -> Dict[str, Any]:
        """Generate default configuration for a model class.

        Args:
            model_cls: The model class to generate configuration for

        Returns:
            Dictionary containing model configuration with default values

        Raises:
            ValueError: If the model class has no config_class
        """
        if not hasattr(model_cls, 'config_class') or model_cls.config_class is None:
            raise ValueError(f"Model class {model_cls.__module__}.{model_cls.__name__} has no config_class")

        # Generate the default config
        model_config = model_cls.config_class()

        # Fill in any sub-model configs
        for sub_model in model_cls.sub_models:
            sub_model_class = getattr(model_config, f"{sub_model}_class", None)
            if sub_model_class is None:
                setattr(model_config, sub_model, None)
                setattr(model_config, f"{sub_model}_class", None)
                continue
            # Import submodel class if it's a string
            if isinstance(sub_model_class, str):
                module_name, class_name = sub_model_class.rsplit('.', 1)
                sub_model_class = getattr(importlib.import_module(module_name), class_name)
            # Generate submodel config
            sub_model_config = self._generate_model_config(sub_model_class)
            # Add submodel config to main config
            setattr(model_config, sub_model, sub_model_config)
            setattr(model_config, f"{sub_model}_class", f"{sub_model_class.__module__}.{sub_model_class.__name__}")

        config_dict = model_config.to_dict()
        self._clean_config_dict(model_config, config_dict)

        return config_dict

    def _generate_class_config(self, cls: Type[Any], defaults: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate default configuration for any class.

        Args:
            cls: The class to generate configuration for
            defaults: Optional dictionary of default values to use instead of inspecting __init__

        Returns:
            Dictionary containing class_path and config with all parameters
            (None for required parameters without defaults)
        """
        # Handle model classes with config_class
        if issubclass(cls, DbtkModel):
            config = self._generate_model_config(cls)

        # Use provided defaults if available
        elif defaults is not None:
            config = defaults

        # Otherwise inspect __init__ parameters
        else:
            config = {}
            sig = inspect.signature(cls.__init__)
            for name, param in sig.parameters.items():
                if name != 'self':
                    # Use default if available, otherwise None
                    config[name] = param.default if param.default is not inspect.Parameter.empty else None

        return {
            "class_path": f"{cls.__module__}.{cls.__name__}",
            "config": config
        }

    def run(self, args: argparse.Namespace) -> int:
        """Generate a default configuration from the given arguments."""
        config = {}

        # Add model config if requested
        if args.model is not None:
            config['model'] = self._generate_class_config(args.model)

        # Add datamodule config if requested
        if args.datamodule is not None:
            config['datamodule'] = self._generate_class_config(args.datamodule)

        # Add trainer config if requested
        if args.train:
            if isinstance(args.train, bool):
                # If --train was specified without a class, just return the config portion
                config['train'] = self._generate_class_config(L.Trainer)["config"]
            else:
                # If a specific trainer class was provided, return the full class config
                config['train'] = self._generate_class_config(args.train)

        # Output the configuration
        if args.format == 'json':
            json.dump(config, sys.stdout, indent=2)
        else:
            yaml.dump(config, sys.stdout, sort_keys=False)

        return 0

@subcommand("fit", "Fit a model.")
class FitCommand(CliSubCommand):
    @override
    def configure(self, parser):
        parser.add_argument("checkpoint_dir", type=Path,
                          help="Directory to save checkpoints and resume from")
        parser.add_argument("--config", "-c", type=Path, default=[], action="append",
                          help="Configuration files to merge with checkpoint config")

    def run(self, args: argparse.Namespace) -> int:
        """
        Fit a model using configurations from checkpoint and optional config files.

        Args:
            args: Command line arguments containing checkpoint dir and config paths

        Returns:
            0 on success, non-zero on failure
        """
        # Initialize merged config
        merged_config = {}

        # Try to load config from checkpoint first
        last_ckpt = args.checkpoint_dir / 'last.ckpt'
        if last_ckpt.exists():
            try:
                checkpoint = torch.load(last_ckpt)
                if 'config' in checkpoint:
                    merged_config = checkpoint['config']
                    print(f"Loaded config from checkpoint: {last_ckpt}")
            except Exception as e:
                print(f"Warning: Could not load config from checkpoint: {str(e)}", file=sys.stderr)

        # Create checkpoint directory if it doesn't exist
        args.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        # Read and merge additional config files if provided
        if args.config:
            for config_path in args.config:
                if not config_path.exists():
                    print(f"Error: Config file {config_path} does not exist", file=sys.stderr)
                    return 1

                # Load config based on file extension
                try:
                    with open(config_path) as f:
                        if config_path.suffix.lower() == '.json':
                            config = json.load(f)
                        elif config_path.suffix.lower() in ('.yaml', '.yml'):
                            config = yaml.safe_load(f)
                        else:
                            print(f"Error: Unsupported config file format: {config_path}", file=sys.stderr)
                            return 1

                    # Update merged_config with new config
                    merged_config.update(config)
                except Exception as e:
                    print(f"Error loading config file {config_path}: {str(e)}", file=sys.stderr)
                    return 1

        # Parse the merged configuration
        config = parse_config(merged_config)

        # Extract components
        model = config.get('model')
        if not model:
            print("Error: No model configuration found", file=sys.stderr)
            return 1

        datamodule = config.get('datamodule')
        if not datamodule:
            print("Error: No datamodule configuration found", file=sys.stderr)
            return 1

        trainer_config = config.get('train', {})

        # Ensure checkpoint directory exists
        args.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        trainer_config['default_root_dir'] = str(args.checkpoint_dir)

        # Setup checkpointing
        checkpoint_callback = ModelCheckpoint(
            dirpath=args.checkpoint_dir,
            filename='model-{epoch:02d}-{step}',
            save_last=True,  # Save latest model for resuming
            every_n_epochs=1,
            save_on_train_epoch_end=True
        )

        # Setup on exception checkpointing
        exception_callback = L.pytorch.callbacks.OnExceptionCheckpoint(args.checkpoint_dir, "last")

        # Setup config checkpointing
        config_callback = ConfigCheckpoint(merged_config)

        # Add checkpoint callback to existing callbacks
        callbacks = trainer_config.pop('callbacks', []) or []
        callbacks.append(checkpoint_callback)
        callbacks.append(exception_callback)
        callbacks.append(config_callback)
        trainer_config['callbacks'] = callbacks

        # Enable automatic checkpointing
        trainer_config['enable_checkpointing'] = True

        # Create trainer with checkpoint directory
        trainer = L.Trainer(**trainer_config)

        # Check for existing checkpoint
        last_checkpoint = None
        last_ckpt = args.checkpoint_dir / 'last.ckpt'
        if last_ckpt.exists():
            last_checkpoint = str(last_ckpt)
            print(f"Resuming from checkpoint: {last_checkpoint}")

        # Train the model
        trainer.fit(model, datamodule=datamodule, ckpt_path=last_checkpoint)
        return 0


@subcommand("export", "Export a model from a checkpoint to HuggingFace format.")
class ExportCommand(CliSubCommand):
    @override
    def configure(self, parser):
        parser.add_argument("checkpoint", type=Path,
                          help="Path to the checkpoint file")
        parser.add_argument("output_dir", type=Path,
                          help="Directory to save the exported model")

    def run(self, args: argparse.Namespace) -> int:
        """
        Export a model from a checkpoint to HuggingFace format.

        Args:
            args: Command line arguments containing checkpoint path and output directory

        Returns:
            0 on success, non-zero on failure
        """
        # Load the checkpoint
        if not args.checkpoint.exists():
            print(f"Error: Checkpoint file {args.checkpoint} does not exist", file=sys.stderr)
            return 1

        # Load checkpoint and config
        checkpoint = torch.load(args.checkpoint)
        if 'config' not in checkpoint:
            print("Error: No configuration found in checkpoint", file=sys.stderr)
            return 1

        # Parse the configuration
        config = parse_config(checkpoint['config'])
        model: PreTrainedModel = config.get('model')
        if not model:
            print("Error: No model configuration found in checkpoint", file=sys.stderr)
            return 1

        # Create model instance
        if not issubclass(model.__class__, PreTrainedModel):
            print(f"Error: Model class {model.__class__.__name__} is not a PreTrainedModel", file=sys.stderr)
            return 1

        # Load state dict
        if 'state_dict' not in checkpoint:
            print("Error: No state dict found in checkpoint", file=sys.stderr)
            return 1

        # Remove 'model.' prefix from state dict keys if present
        state_dict = {k.replace('model.', ''): v for k, v in checkpoint['state_dict'].items()}
        model.load_state_dict(state_dict)

        # Create output directory
        args.output_dir.mkdir(parents=True, exist_ok=True)

        # Save using HuggingFace format
        model.save_pretrained(args.output_dir)
        print(f"Model exported to {args.output_dir}")
        return 0
