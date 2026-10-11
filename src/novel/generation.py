"""Bounded seeded raw-token generation for the Qwen3 reference engine.

Uncached generation recomputes the entire realized prefix at each step. A patch
is consistently reapplied to its fixed absolute original-prompt cue positions
on EVERY such recomputation, including later steps. This is persistent causal
intervention, not temporary noise followed by clean re-prefill. There is no
moving last-token intervention and no intervention-bearing KV-cache reuse.

Clean cached decoding is a separate parity/efficiency condition. It supports
no hooks or interventions, and returns the same raw IDs interface. No chat
template, parsing, answer extraction, hidden verifier input, or output repair
is performed here. EOS, if sampled, is retained in the generated IDs.
"""

from dataclasses import dataclass
import math

import torch
from torch import Tensor, nn

from .activation import Intervention, _integer, forward_reference, validate_reference_inputs


MAX_NEW_TOKENS = 256


@dataclass(frozen=True)
class GenerationResult:
    prompt_ids: tuple[int, ...]
    generated_ids: tuple[int, ...]
    stop_reason: str
    forward_calls: int
    processed_tokens: int
    seed: int
    cache_policy: str

    @property
    def all_ids(self) -> tuple[int, ...]:
        return self.prompt_ids + self.generated_ids


def _sampling_parameters(temperature: float, top_p: float, top_k: int) -> None:
    for name, value in (("temperature", temperature), ("top_p", top_p)):
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    if not 0 < top_p <= 1:
        raise ValueError("top_p must lie in (0, 1]")
    _integer(top_k, "top_k")


def _sample_token(logits: Tensor, *, generator: torch.Generator, temperature: float, top_p: float, top_k: int) -> Tensor:
    scores = logits.float() / temperature
    if top_k:
        threshold = torch.topk(scores, min(top_k, scores.shape[-1])).values[-1]
        scores = scores.masked_fill(scores < threshold, -torch.inf)
    if top_p < 1:
        sorted_scores, sorted_indices = torch.sort(scores, descending=True)
        cumulative = torch.softmax(sorted_scores, dim=-1).cumsum(dim=-1)
        remove = torch.zeros_like(cumulative, dtype=torch.bool)
        remove[1:] = cumulative[:-1] >= top_p
        sorted_scores = sorted_scores.masked_fill(remove, -torch.inf)
        scores = torch.empty_like(scores).scatter(0, sorted_indices, sorted_scores)
    probabilities = torch.softmax(scores, dim=-1)
    if not bool(torch.isfinite(probabilities).all()) or not bool(probabilities.sum() > 0):
        raise ValueError("sampling probabilities must be finite and nonempty")
    return torch.multinomial(probabilities, num_samples=1, generator=generator)


@torch.no_grad()
def generate_reference(
    model: nn.Module,
    prompt_ids: Tensor,
    *,
    seed: int,
    max_new_tokens: int,
    temperature: float = 0.7,
    top_p: float = 0.8,
    top_k: int = 20,
    do_sample: bool = True,
    eos_token_ids: tuple[int, ...] = (),
    intervention: Intervention | None = None,
    use_cache: bool = False,
) -> GenerationResult:
    """Generate at most 256 new tokens, using a private device-local RNG.

    ``prompt_ids`` must already be an unpadded [1, length] long tensor on the
    embedding device. Caller chooses exact stop tokens; an empty tuple disables
    EOS stopping. A token cap is reported as ``max_new_tokens`` and does not
    imply task failure. Context overflow is rejected before any model execution.
    """

    validate_reference_inputs(model, prompt_ids)
    _integer(seed, "seed")
    if seed > 2**63 - 1:
        raise ValueError("seed must fit a nonnegative signed 64-bit integer")
    _integer(max_new_tokens, "max_new_tokens", minimum=1)
    if max_new_tokens > MAX_NEW_TOKENS:
        raise ValueError(f"max_new_tokens exceeds the reference cap of {MAX_NEW_TOKENS}")
    if prompt_ids.shape[1] + max_new_tokens > model.config.max_position_embeddings:
        raise ValueError("prompt and generation cap exceed the configured context length")
    _sampling_parameters(temperature, top_p, top_k)
    if not isinstance(do_sample, bool) or not isinstance(use_cache, bool):
        raise ValueError("do_sample and use_cache must be boolean")
    if not isinstance(eos_token_ids, tuple):
        raise ValueError("eos_token_ids must be an explicit tuple")
    for token in eos_token_ids:
        _integer(token, "EOS token ID")
        if token >= model.config.vocab_size:
            raise ValueError("EOS token ID is outside the model vocabulary")
    if use_cache and intervention is not None:
        raise ValueError("cached generation supports clean execution only; interventions require full-prefix recomputation")

    sequence = prompt_ids.detach().clone()
    generator = torch.Generator(device=sequence.device)
    generator.manual_seed(seed)
    generated = []
    past_key_values = None
    forward_calls = 0
    processed_tokens = 0
    stop_reason = "max_new_tokens"
    for _step in range(max_new_tokens):
        if use_cache:
            current = sequence if past_key_values is None else sequence[:, -1:]
            start = sequence.shape[1] - current.shape[1]
            positions = torch.arange(start, sequence.shape[1], device=sequence.device)
            output = model(
                input_ids=current,
                attention_mask=torch.ones_like(sequence),
                position_ids=positions.unsqueeze(0),
                cache_position=positions,
                past_key_values=past_key_values,
                use_cache=True,
                return_dict=True,
                logits_to_keep=1,
            )
            past_key_values = output.past_key_values
            if past_key_values is None:
                raise ValueError("clean cached execution returned no KV cache")
            if tuple(output.logits.shape) != (1, 1, model.config.vocab_size) or not bool(torch.isfinite(output.logits).all()):
                raise ValueError("clean cached logits have invalid shape or nonfinite values")
            logits = output.logits[0, -1]
            processed_tokens += current.shape[1]
        else:
            output = forward_reference(model, sequence, intervention=intervention, last_logits_only=True)
            logits = output.logits[0, -1]
            processed_tokens += sequence.shape[1]
        forward_calls += 1
        if do_sample:
            token = _sample_token(logits, generator=generator, temperature=temperature, top_p=top_p, top_k=top_k)
        else:
            token = torch.argmax(logits).reshape(1)
        token_id = int(token.item())
        generated.append(token_id)
        sequence = torch.cat((sequence, token.reshape(1, 1)), dim=1)
        if token_id in eos_token_ids:
            stop_reason = "eos"
            break
    return GenerationResult(
        prompt_ids=tuple(prompt_ids[0].detach().cpu().tolist()),
        generated_ids=tuple(generated),
        stop_reason=stop_reason,
        forward_calls=forward_calls,
        processed_tokens=processed_tokens,
        seed=seed,
        cache_policy="clean_cached" if use_cache else "full_prefix_cache_disabled",
    )
