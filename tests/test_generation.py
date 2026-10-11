"""Seeded free-generation, KV parity, and fixed-position causal patch checks."""

import pytest
import torch
from transformers import Qwen3Config, Qwen3ForCausalLM

from novel.activation import (AdditiveIntervention, IdentityIntervention, ResidualSite,
                              SemanticAnchor, forward_reference, prepare_reference_model)
from novel.generation import generate_reference


@pytest.fixture(scope="module")
def model():
    with torch.random.fork_rng():
        torch.manual_seed(183)
        config = Qwen3Config(
            vocab_size=97, hidden_size=32, intermediate_size=64,
            num_hidden_layers=3, num_attention_heads=4, num_key_value_heads=2,
            head_dim=8, max_position_embeddings=64, attention_dropout=0.0,
            bos_token_id=1, eos_token_id=2, pad_token_id=0,
        )
        config._attn_implementation = "eager"
        return prepare_reference_model(Qwen3ForCausalLM(config))


@pytest.fixture
def ids():
    return torch.tensor([[5, 8, 13, 21, 34]], dtype=torch.long)


def anchor_for(ids):
    prefix = tuple(ids[0].tolist())
    return SemanticAnchor("neutral continuation cue", 4, prefix[4:], prefix,
                          "The exact original prompt cue is reused at an absolute position.")


def test_seed_replay_noop_and_zero_do_not_advance_global_rng(model, ids):
    kwargs = dict(seed=947, max_new_tokens=7, temperature=0.9, top_p=0.92, top_k=17)
    global_state = torch.random.get_rng_state().clone()
    clean = generate_reference(model, ids, **kwargs)
    repeated = generate_reference(model, ids, **kwargs)
    site = ResidualSite(1, (4,))
    for intervention in (
        IdentityIntervention(site),
        AdditiveIntervention(site, torch.ones(32), anchor_for(ids), strength=0),
        AdditiveIntervention(site, torch.zeros(32), anchor_for(ids)),
    ):
        result = generate_reference(model, ids, intervention=intervention, **kwargs)
        assert result == clean
    assert clean == repeated
    assert torch.equal(global_state, torch.random.get_rng_state())
    assert len(clean.generated_ids) == 7
    assert clean.forward_calls == 7
    assert clean.processed_tokens == sum(range(5, 12))
    assert clean.stop_reason == "max_new_tokens"
    assert clean.prompt_ids == tuple(ids[0].tolist())
    assert clean.all_ids == clean.prompt_ids + clean.generated_ids
    assert all(not layer._forward_hooks for layer in model.model.layers)


def test_sampling_is_independent_of_global_random_stream(model, ids):
    with torch.random.fork_rng():
        torch.manual_seed(12)
        a = generate_reference(model, ids, seed=21, max_new_tokens=12, top_k=0, top_p=1)
        torch.rand(5000)
        b = generate_reference(model, ids, seed=21, max_new_tokens=12, top_k=0, top_p=1)
        c = generate_reference(model, ids, seed=22, max_new_tokens=12, top_k=0, top_p=1)
    assert a.generated_ids == b.generated_ids
    assert a.generated_ids != c.generated_ids


def test_clean_cached_logits_match_full_prefix_for_distinct_teacher_forced_steps(model, ids):
    # Independent teacher forcing compares numerics even if sampled tokens diverge.
    sequence = ids.clone()
    cache = None
    for forced_token in (7, 19, 29, 41):
        current = sequence if cache is None else sequence[:, -1:]
        start = sequence.shape[1] - current.shape[1]
        positions = torch.arange(start, sequence.shape[1])
        with torch.no_grad():
            cached = model(input_ids=current, attention_mask=torch.ones_like(sequence),
                           position_ids=positions.unsqueeze(0), cache_position=positions,
                           past_key_values=cache, use_cache=True, return_dict=True,
                           logits_to_keep=1)
        full = forward_reference(model, sequence, last_logits_only=True)
        torch.testing.assert_close(cached.logits, full.logits, rtol=1e-5, atol=1e-6)
        cache = cached.past_key_values
        assert cache is not None
        sequence = torch.cat((sequence, torch.tensor([[forced_token]])), dim=1)


@pytest.mark.parametrize("do_sample", [False, True])
def test_clean_cached_and_uncached_generation_match_and_costs_are_distinct(model, ids, do_sample):
    kwargs = dict(seed=31, max_new_tokens=8, do_sample=do_sample, top_k=13, top_p=0.91)
    full = generate_reference(model, ids, **kwargs)
    cached = generate_reference(model, ids, use_cache=True, **kwargs)
    assert cached.generated_ids == full.generated_ids
    assert cached.forward_calls == full.forward_calls == 8
    assert cached.processed_tokens == 5 + 7
    assert full.processed_tokens == sum(range(5, 13))
    assert cached.cache_policy == "clean_cached"
    assert full.cache_policy == "full_prefix_cache_disabled"


def test_eos_is_preserved_without_parsing_or_extra_forward(model, ids):
    raw = generate_reference(model, ids, seed=1, max_new_tokens=4, do_sample=False)
    eos = raw.generated_ids[0]
    stopped = generate_reference(model, ids, seed=1, max_new_tokens=4, do_sample=False,
                                 eos_token_ids=(eos,))
    assert stopped.generated_ids == (eos,)
    assert stopped.all_ids[-1] == eos
    assert stopped.stop_reason == "eos"
    assert stopped.forward_calls == 1
    assert stopped.processed_tokens == ids.shape[1]


def test_intervention_is_reapplied_at_fixed_cue_every_full_prefix_step(model, ids):
    site = ResidualSite(0, (4,))
    delta = torch.linspace(-0.8, 0.8, 32)
    patch = AdditiveIntervention(site, delta, anchor_for(ids))
    before = []
    after = []
    baseline_handle = model.model.layers[0].register_forward_hook(
        lambda _m, _a, output: before.append(output.detach().clone()))
    # The following block's input independently observes the patched residual.
    downstream_handle = model.model.layers[1].register_forward_pre_hook(
        lambda _m, args: after.append(args[0].detach().clone()))
    try:
        result = generate_reference(model, ids, seed=13, max_new_tokens=4,
                                    do_sample=False, intervention=patch)
    finally:
        baseline_handle.remove()
        downstream_handle.remove()
    assert [tensor.shape[1] for tensor in before] == [5, 6, 7, 8]
    assert [tensor.shape[1] for tensor in after] == [5, 6, 7, 8]
    for clean, patched in zip(before, after, strict=True):
        torch.testing.assert_close(patched[:, 4], clean[:, 4] + delta)
        other_positions = [p for p in range(clean.shape[1]) if p != 4]
        torch.testing.assert_close(patched[:, other_positions], clean[:, other_positions], rtol=0, atol=0)
    # Independently construct the persistent-patch greedy trajectory.
    sequence = ids.clone()
    expected = []
    for _ in range(4):
        token = int(forward_reference(model, sequence, intervention=patch,
                                     last_logits_only=True).logits[0, -1].argmax())
        expected.append(token)
        sequence = torch.cat((sequence, torch.tensor([[token]])), dim=1)
    assert result.generated_ids == tuple(expected)
    assert all(not layer._forward_hooks for layer in model.model.layers)


def test_real_intervention_changes_generated_raw_token(model, ids):
    clean = generate_reference(model, ids, seed=7, max_new_tokens=1, do_sample=False)
    # A strong final-block cue patch toward another output token must change
    # the sampled result; this is plumbing evidence, not semantic transfer.
    target = (clean.generated_ids[0] + 1) % model.config.vocab_size
    delta = model.lm_head.weight[target].detach().clone() * 10000
    patch = AdditiveIntervention(ResidualSite(2, (4,)), delta, anchor_for(ids))
    patched = generate_reference(model, ids, seed=7, max_new_tokens=1, do_sample=False,
                                 intervention=patch)
    assert patched.generated_ids == (target,)
    assert patched.generated_ids != clean.generated_ids


@pytest.mark.parametrize("kwargs", [dict(max_new_tokens=0), dict(max_new_tokens=257),
                                    dict(max_new_tokens=60), dict(temperature=0),
                                    dict(top_p=0), dict(top_p=1.1), dict(top_k=-1),
                                    dict(seed=-1), dict(eos_token_ids=(97,))])
def test_invalid_generation_config_fails_before_forward(model, ids, monkeypatch, kwargs):
    def should_not_run(*args, **kw):
        raise AssertionError("invalid configuration executed the model")
    monkeypatch.setattr(model, "forward", should_not_run)
    config = dict(seed=1, max_new_tokens=3)
    config.update(kwargs)
    with pytest.raises(ValueError):
        generate_reference(model, ids, **config)


@pytest.mark.parametrize("identity", [False, True])
def test_cached_interventions_are_explicitly_rejected(model, ids, identity):
    site = ResidualSite(0, (4,))
    intervention = IdentityIntervention(site) if identity else AdditiveIntervention(site, torch.ones(32), anchor_for(ids))
    with pytest.raises(ValueError, match="clean execution only"):
        generate_reference(model, ids, seed=1, max_new_tokens=3, use_cache=True,
                           intervention=intervention)


@pytest.mark.gpu
@pytest.mark.skipif(not torch.cuda.is_available(), reason="requires a separate CUDA/FP16 reference environment")
def test_cuda_fp16_eager_noop_and_clean_cache_gate(model, ids):
    # Prospective hardware gate only: it is skipped in this CPU-only environment.
    # These initial numerical tolerances must be recorded/reviewed on real hardware.
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(183)
        gpu_model = prepare_reference_model(Qwen3ForCausalLM(model.config)).to(device="cuda", dtype=torch.float16)
    gpu_ids = ids.to("cuda")
    baseline = forward_reference(gpu_model, gpu_ids)
    identity = forward_reference(gpu_model, gpu_ids, intervention=IdentityIntervention(ResidualSite(1, (4,))))
    zero = forward_reference(gpu_model, gpu_ids, intervention=AdditiveIntervention(
        ResidualSite(1, (4,)), torch.ones(32, device="cuda", dtype=torch.float16), anchor_for(ids), strength=0))
    torch.testing.assert_close(identity.logits, baseline.logits, rtol=0, atol=0)
    torch.testing.assert_close(zero.logits, baseline.logits, rtol=0, atol=0)
    assert baseline.logits.dtype == torch.float16
    prefix = gpu_ids[:, :-1]
    with torch.no_grad():
        prefill = gpu_model(input_ids=prefix, attention_mask=torch.ones_like(prefix),
                            position_ids=torch.arange(prefix.shape[1], device="cuda").unsqueeze(0),
                            cache_position=torch.arange(prefix.shape[1], device="cuda"),
                            use_cache=True, return_dict=True, logits_to_keep=1)
        cached = gpu_model(input_ids=gpu_ids[:, -1:], attention_mask=torch.ones_like(gpu_ids),
                           position_ids=torch.tensor([[gpu_ids.shape[1] - 1]], device="cuda"),
                           cache_position=torch.tensor([gpu_ids.shape[1] - 1], device="cuda"),
                           past_key_values=prefill.past_key_values, use_cache=True,
                           return_dict=True, logits_to_keep=1)
    torch.testing.assert_close(cached.logits, baseline.logits[:, -1:], rtol=1e-2, atol=2e-3)
    clean = generate_reference(gpu_model, gpu_ids, seed=44, max_new_tokens=4)
    noop = generate_reference(gpu_model, gpu_ids, seed=44, max_new_tokens=4,
                              intervention=IdentityIntervention(ResidualSite(1, (4,))))
    assert noop.generated_ids == clean.generated_ids
