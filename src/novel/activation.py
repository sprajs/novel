"""Selected residual hooks for the eager, frozen Hugging Face Qwen3 reference.

The site ``model.model.layers[N]`` is a decoder-block *forward output*: after
the attention residual addition and the MLP residual addition, before the next
block's input normalization (or the model's final normalization at the last
layer). It is neither the attention output nor the residual before the MLP.
The supported Transformers Qwen3 layer returns a tensor; other output layouts
fail explicitly. Captures observe the block output BEFORE this module's patch.

Only unpadded batch-one, full-prefix forwards are instrumented. An additive
patch changes fixed absolute prompt-cue positions, never a moving ``-1`` index.
The anchor records a researcher-supplied semantic role and rationale and checks
its exact token span and original prefix. These checks prevent position drift;
they cannot establish the scientific validity of a claimed semantic alignment.
"""

from contextlib import contextmanager
from dataclasses import dataclass
import math
from typing import Iterator

import torch
from torch import Tensor, nn


def _integer(value: object, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


@dataclass(frozen=True)
class ResidualSite:
    layer: int
    positions: tuple[int, ...]

    def __post_init__(self) -> None:
        _integer(self.layer, "layer")
        if not isinstance(self.positions, tuple) or not self.positions:
            raise ValueError("positions must be a nonempty tuple of absolute indices")
        for position in self.positions:
            _integer(position, "position")
        if len(set(self.positions)) != len(self.positions):
            raise ValueError("positions must be unique")

    @property
    def module_path(self) -> str:
        return f"model.layers.{self.layer}"


@dataclass(frozen=True)
class SemanticAnchor:
    role: str
    start: int
    token_ids: tuple[int, ...]
    prefix_token_ids: tuple[int, ...]
    rationale: str

    def __post_init__(self) -> None:
        _integer(self.start, "anchor start")
        if not isinstance(self.role, str) or not self.role.strip():
            raise ValueError("anchor semantic role must be explicit")
        if not isinstance(self.rationale, str) or not self.rationale.strip():
            raise ValueError("anchor alignment rationale must be explicit")
        for name, ids in (("token_ids", self.token_ids), ("prefix_token_ids", self.prefix_token_ids)):
            if not isinstance(ids, tuple) or not ids:
                raise ValueError(f"anchor {name} must be a nonempty tuple")
            for token in ids:
                _integer(token, f"anchor {name} token")
        end = self.start + len(self.token_ids)
        if end > len(self.prefix_token_ids):
            raise ValueError("anchor span must lie within the original prefix")
        if self.prefix_token_ids[self.start:end] != self.token_ids:
            raise ValueError("anchor token span does not match its original prefix")

    def validate(self, input_ids: Tensor, site: ResidualSite) -> None:
        prefix_length = len(self.prefix_token_ids)
        if input_ids.shape[1] < prefix_length:
            raise ValueError("intervention requires the complete anchored original prefix")
        actual = tuple(input_ids[0, :prefix_length].detach().cpu().tolist())
        if actual != self.prefix_token_ids:
            raise ValueError("input prefix differs from the anchored original prefix")
        end = self.start + len(self.token_ids)
        if any(not self.start <= position < end for position in site.positions):
            raise ValueError("intervention positions must lie in the declared semantic cue span")


@dataclass(frozen=True)
class IdentityIntervention:
    """Install a real output hook that returns the original tensor unchanged."""

    site: ResidualSite


@dataclass(frozen=True)
class AdditiveIntervention:
    """Add ``strength * delta`` at anchored positions after a decoder block.

    ``delta`` must be either [hidden_size] (shared by selected positions) or
    [number_of_selected_positions, hidden_size]. No implicit normalization,
    random perturbation, donor selection, or broadcasting across a batch occurs.
    The tensor is detached and copied when the context is entered, so this is
    an exact inference patch rather than a differentiable intervention optimizer.
    """

    site: ResidualSite
    delta: Tensor
    anchor: SemanticAnchor
    strength: float = 1.0

    def __post_init__(self) -> None:
        if not isinstance(self.site, ResidualSite) or not isinstance(self.anchor, SemanticAnchor):
            raise ValueError("an additive intervention needs a site and semantic anchor")
        if isinstance(self.strength, bool) or not isinstance(self.strength, (int, float)):
            raise ValueError("intervention strength must be a finite number")
        if not math.isfinite(self.strength):
            raise ValueError("intervention strength must be finite")
        if not isinstance(self.delta, Tensor) or not self.delta.is_floating_point():
            raise ValueError("intervention delta must be a floating-point tensor")
        if not bool(torch.isfinite(self.delta).all()):
            raise ValueError("intervention delta must be finite, including at zero strength")


Intervention = AdditiveIntervention | IdentityIntervention


def _validate_model(model: nn.Module, *, frozen: bool = True) -> nn.ModuleList:
    config = getattr(model, "config", None)
    if getattr(config, "model_type", None) != "qwen3":
        raise ValueError("reference instrumentation supports standard Hugging Face Qwen3 only")
    if getattr(config, "_attn_implementation", None) != "eager":
        raise ValueError("reference instrumentation requires eager attention")
    if getattr(model, "is_quantized", False) or getattr(model, "hf_quantizer", None) is not None:
        raise ValueError("reference instrumentation does not support quantized models")
    if hasattr(model, "_orig_mod"):
        raise ValueError("reference instrumentation requires an uncompiled model")
    layers = getattr(getattr(model, "model", None), "layers", None)
    if not isinstance(layers, nn.ModuleList) or not layers:
        raise ValueError("expected decoder blocks at model.model.layers")
    if frozen and (any(module.training for module in model.modules()) or any(p.requires_grad for p in model.parameters())):
        raise ValueError("reference model must be in eval mode with all parameters frozen")
    return layers


def prepare_reference_model(model: nn.Module) -> nn.Module:
    """Explicitly freeze and evaluate an already loaded eager Qwen3 model."""

    _validate_model(model, frozen=False)
    model.eval()
    model.requires_grad_(False)
    return model


def validate_reference_inputs(model: nn.Module, input_ids: Tensor) -> None:
    """Validate the batch-one, unpadded, contiguous-position reference inputs."""

    _validate_model(model)
    if not isinstance(input_ids, Tensor) or input_ids.dtype != torch.long:
        raise ValueError("input_ids must be a torch.long tensor; token IDs are never coerced")
    if input_ids.ndim != 2 or input_ids.shape[0] != 1 or input_ids.shape[1] == 0:
        raise ValueError("reference input_ids must have shape [1, nonempty_sequence]")
    embedding = model.get_input_embeddings().weight
    if input_ids.device != embedding.device:
        raise ValueError("input_ids must be on the input embedding device")
    if bool((input_ids < 0).any()) or bool((input_ids >= embedding.shape[0]).any()):
        raise ValueError("input token ID is outside the model vocabulary")
    if input_ids.shape[1] > model.config.max_position_embeddings:
        raise ValueError("input exceeds the configured context length")


@dataclass
class ResidualHookState:
    captured: Tensor | None = None
    calls: int = 0


@contextmanager
def residual_hooks(
    model: nn.Module,
    input_ids: Tensor,
    *,
    capture_site: ResidualSite | None = None,
    intervention: Intervention | None = None,
) -> Iterator[ResidualHookState]:
    """Install selected output hooks, removing every owned handle on all exits.

    Run exactly the supplied full ``input_ids`` while this context is active;
    ``forward_reference`` enforces that contract. Captures are detached CPU
    clones with shape [1, selected_positions, hidden_size], in requested order.
    Existing external hooks are neither removed nor reordered. Scientific runs
    should avoid mixing externally installed modification hooks with this API.
    No-op, identity, zero strength, and zero delta never draw random numbers.
    """

    validate_reference_inputs(model, input_ids)
    if capture_site is not None and not isinstance(capture_site, ResidualSite):
        raise ValueError("capture_site must be a ResidualSite")
    if intervention is not None and not isinstance(intervention, (AdditiveIntervention, IdentityIntervention)):
        raise ValueError("unsupported intervention type")
    layers = model.model.layers
    sites = [site for site in (capture_site, getattr(intervention, "site", None)) if site is not None]
    for site in sites:
        if site.layer >= len(layers):
            raise ValueError("residual layer is outside model.model.layers")
        if max(site.positions) >= input_ids.shape[1]:
            raise ValueError("residual position is outside the supplied full prefix")
    prepared_delta = None
    if isinstance(intervention, AdditiveIntervention):
        intervention.anchor.validate(input_ids, intervention.site)
        hidden_size = model.config.hidden_size
        expected = (len(intervention.site.positions), hidden_size)
        if tuple(intervention.delta.shape) not in ((hidden_size,), expected):
            raise ValueError(f"delta shape must be [{hidden_size}] or {list(expected)}")
        # Validation also checks user-mutated delta tensors on every entry.
        if not bool(torch.isfinite(intervention.delta).all()):
            raise ValueError("intervention delta must remain finite")
        prepared_delta = intervention.delta.detach().clone()
    state = ResidualHookState()
    handles = []
    expected_shape = (1, input_ids.shape[1], model.config.hidden_size)

    def make_hook(layer: int):
        def hook(_module: nn.Module, _args: tuple, output: Tensor) -> Tensor:
            if not isinstance(output, Tensor) or tuple(output.shape) != expected_shape:
                raise ValueError(f"Qwen3 block output must be a tensor of shape {expected_shape}")
            if not output.is_floating_point() or not bool(torch.isfinite(output).all()):
                raise ValueError("Qwen3 block output must be floating point and finite")
            state.calls += 1
            if capture_site is not None and capture_site.layer == layer:
                if state.captured is not None:
                    raise ValueError("capture context permits only one full-prefix forward")
                state.captured = output[:, list(capture_site.positions), :].detach().to("cpu").clone()
            if not isinstance(intervention, AdditiveIntervention) or intervention.site.layer != layer:
                return output
            if intervention.strength == 0 or not bool(torch.count_nonzero(prepared_delta)):
                return output
            delta = prepared_delta.to(device=output.device, dtype=output.dtype)
            delta = delta * intervention.strength
            if not bool(torch.isfinite(delta).all()):
                raise ValueError("scaled delta is nonfinite in the block output dtype")
            patched = output.clone()
            positions = list(intervention.site.positions)
            patched[:, positions, :] = patched[:, positions, :] + delta
            if not bool(torch.isfinite(patched[:, positions, :]).all()):
                raise ValueError("patched activation is nonfinite")
            return patched
        return hook

    try:
        for layer in sorted({site.layer for site in sites}):
            handles.append(layers[layer].register_forward_hook(make_hook(layer)))
        yield state
    finally:
        for handle in handles:
            handle.remove()


@dataclass(frozen=True)
class ReferenceForward:
    logits: Tensor
    residual: Tensor | None


@torch.no_grad()
def forward_reference(
    model: nn.Module,
    input_ids: Tensor,
    *,
    capture_site: ResidualSite | None = None,
    intervention: Intervention | None = None,
    last_logits_only: bool = False,
) -> ReferenceForward:
    """Recompute a full unpadded prefix with cache disabled and optional hooks.

    Positions are explicitly 0..length-1 and the attention mask is all ones.
    Full-sequence logits are returned unless ``last_logits_only`` is requested.
    Returned logits are native model values, without normalization or sampling.
    This inference helper intentionally does not implement activation gradients.
    """

    with residual_hooks(model, input_ids, capture_site=capture_site, intervention=intervention) as state:
        positions = torch.arange(input_ids.shape[1], device=input_ids.device)
        output = model(
            input_ids=input_ids,
            attention_mask=torch.ones_like(input_ids),
            position_ids=positions.unsqueeze(0),
            cache_position=positions,
            use_cache=False,
            return_dict=True,
            logits_to_keep=1 if last_logits_only else 0,
        )
        logits = output.logits
        expected_length = 1 if last_logits_only else input_ids.shape[1]
        if tuple(logits.shape) != (1, expected_length, model.config.vocab_size):
            raise ValueError("unexpected Qwen3 logits shape")
        if not bool(torch.isfinite(logits).all()):
            raise ValueError("Qwen3 logits must be finite")
        if capture_site is not None and state.captured is None:
            raise ValueError("selected residual hook was never called")
        return ReferenceForward(logits=logits, residual=state.captured)
