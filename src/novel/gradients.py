"""Local activation derivatives, not training or a claim of causal attribution."""

from dataclasses import dataclass

import torch
from torch import Tensor, nn

from .activation import ResidualSite, validate_reference_inputs


@dataclass(frozen=True)
class ActivationGradient:
    gradient: Tensor
    score: float
    positive_token_id: int
    negative_token_id: int


def activation_gradient(model: nn.Module, input_ids: Tensor, site: ResidualSite,
                        positive_token_id: int, negative_token_id: int) -> ActivationGradient:
    """d(last-position logit contrast)/d(selected block-output activations).

    Only selected positions become differentiable leaves. Frozen upstream work
    is detached; downstream suffix activations still consume backward memory.
    The local score is diagnostic and contains no verifier/ground-truth input.
    This helper is deliberately separate from the inference-only hook API.
    """
    validate_reference_inputs(model, input_ids)
    if torch.is_inference_mode_enabled():
        raise ValueError("Activation gradients cannot run under inference_mode")
    if site.layer >= len(model.model.layers) or max(site.positions) >= input_ids.shape[1]:
        raise ValueError("Gradient site is outside the model/input")
    for token in (positive_token_id, negative_token_id):
        if type(token) is not int or not 0 <= token < model.config.vocab_size:
            raise ValueError("Gradient objective token is outside the vocabulary")
    if positive_token_id == negative_token_id:
        raise ValueError("Gradient objective requires distinct tokens")
    leaf = None

    def hook(_module, _args, output):
        nonlocal leaf
        expected = (1, input_ids.shape[1], model.config.hidden_size)
        if not isinstance(output, Tensor) or tuple(output.shape) != expected or leaf is not None:
            raise ValueError("Gradient hook expects one full-prefix Qwen3 tensor output")
        if not bool(torch.isfinite(output).all()):
            raise ValueError("Nonfinite gradient source activation")
        leaf = output[:, list(site.positions), :].detach().clone().requires_grad_(True)
        patched = output.detach().clone()
        patched[:, list(site.positions), :] = leaf
        return patched

    handle = model.model.layers[site.layer].register_forward_hook(hook)
    try:
        with torch.enable_grad():
            positions = torch.arange(input_ids.shape[1], device=input_ids.device)
            output = model(input_ids=input_ids, attention_mask=torch.ones_like(input_ids),
                           position_ids=positions[None], cache_position=positions,
                           use_cache=False, logits_to_keep=1)
            score = output.logits[0, -1, positive_token_id].float() - output.logits[0, -1, negative_token_id].float()
            if leaf is None or not bool(torch.isfinite(score)):
                raise ValueError("Gradient objective/source is missing or nonfinite")
            gradient, = torch.autograd.grad(score, leaf)
            if not bool(torch.isfinite(gradient).all()) or not bool(torch.count_nonzero(gradient)):
                raise ValueError("Selected activation gradient is nonfinite or identically zero")
            return ActivationGradient(gradient.detach().cpu().clone(), float(score.detach()),
                                      positive_token_id, negative_token_id)
    finally:
        handle.remove()
