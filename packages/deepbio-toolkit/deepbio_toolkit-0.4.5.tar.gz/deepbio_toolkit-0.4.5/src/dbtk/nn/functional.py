import math
import torch
import torch.nn.functional as F
from typing import Iterable, Optional, Union

def weighted_softmax(
    input: torch.Tensor,
    weights: Optional[torch.Tensor] = None,
    dim: Optional[Union[int, Iterable[int]]] = None,
    dtype: Optional[Union[str, torch.dtype]] = None
) -> torch.Tensor:
    """
    Compute the softmax of the input tensor with weights.

    Args:
        input: The input tensor.
            Shape: [batch_size, sample_size]
        weights: Optional weights.
            Shape: [batch_size, sample_size]
        dim: Optional dimension to compute softmax.
        dtype: Optional dtype for the output.

    Returns:
        The softmax of the input tensor with non-redundant weights.
            Shape: [batch_size, sample_size]
    """
    input_max, _ = input.max(dim=dim, keepdim=True)
    exp_input = torch.exp(input - input_max)
    if weights is not None:
        exp_input *= weights
    result = exp_input / torch.sum(exp_input, dim=dim, keepdims=True)
    if dtype is not None:
        result = result.to(dtype=dtype)
    return result

def scaled_dot_product_attention_with_weights(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attn_mask: Optional[torch.Tensor] = None,
    dropout_p: Optional[Union[float, torch.Tensor]] = 0.0,
    is_causal: bool = False,
    scale: Optional[Union[float, torch.Tensor]] = None,
    enable_gqa: bool = False,
    need_weights: bool = False
) -> torch.Tensor:
    if not need_weights:
        return F.scaled_dot_product_attention(
            query=query,
            key=key,
            value=value,
            attn_mask=attn_mask,
            dropout_p=dropout_p,
            is_causal=is_causal,
            scale=scale,
            enable_gqa=enable_gqa
        )
    L, S = query.size(-2), key.size(-2)
    scale_factor = 1 / math.sqrt(query.size(-1)) if scale is None else scale
    attn_bias = torch.zeros(L, S, dtype=query.dtype, device=query.device)
    if is_causal:
        assert attn_mask is None
        temp_mask = torch.ones(L, S, dtype=torch.bool).tril(diagonal=0)
        attn_bias.masked_fill_(temp_mask.logical_not(), float("-inf"))
        attn_bias.to(query.dtype)

    if attn_mask is not None:
        if attn_mask.dtype == torch.bool:
            attn_bias.masked_fill_(attn_mask.logical_not(), float("-inf"))
        else:
            attn_bias = attn_mask + attn_bias

    if enable_gqa:
        key = key.repeat_interleave(query.size(-3)//key.size(-3), -3)
        value = value.repeat_interleave(query.size(-3)//value.size(-3), -3)

    attn_weight = query @ key.transpose(-2, -1) * scale_factor
    attn_weight += attn_bias
    attn_weight = torch.softmax(attn_weight, dim=-1)
    output = torch.dropout(attn_weight, dropout_p, train=True) @ value
    return output, attn_weight

def non_redundant_scaled_dot_product_set_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    key_abundance: Optional[torch.Tensor] = None,
    attn_mask: Optional[torch.Tensor] = None,
    dropout_p: Union[float, torch.Tensor] = 0.0,
    scale: Optional[Union[float, torch.Tensor]] = None,
    enable_gqa: bool = False,
    need_weights=False
) -> torch.Tensor:
    if key_abundance is None:
        return scaled_dot_product_attention_with_weights(
            query=query,
            key=key,
            value=value,
            attn_mask=attn_mask,
            dropout_p=dropout_p,
            scale=scale,
            enable_gqa=enable_gqa,
            need_weights=need_weights
        )
    scale_factor = 1 / math.sqrt(query.size(-1)) if scale is None else scale

    if enable_gqa:
        key = key.repeat_interleave(query.size(-3)//key.size(-3), -3)
        value = value.repeat_interleave(query.size(-3)//value.size(-3), -3)

    if attn_mask is not None:
        if attn_mask.dtype == torch.bool:
            key_abundance = key_abundance.clone()
            key_abundance.masked_fill_(attn_mask.logical_not(), 0)
        else:
            key_abundance = torch.clamp_max(key_abundance, attn_mask)

    attn_weight = query @ key.transpose(-2, -1) * scale_factor
    attn_weight = weighted_softmax(attn_weight, key_abundance, dim=-1)
    output = torch.dropout(attn_weight, dropout_p, train=True) @ value
    if need_weights:
        return output, attn_weight
    return output
