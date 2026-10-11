"""Offline mechanics checks against real (random, tiny) Qwen3 decoder blocks."""

import pytest
import torch
from transformers import Qwen3Config, Qwen3ForCausalLM

from novel.activation import (
    AdditiveIntervention,
    IdentityIntervention,
    ResidualSite,
    SemanticAnchor,
    forward_reference,
    prepare_reference_model,
    residual_hooks,
)


@pytest.fixture(scope="module")
def model():
    with torch.random.fork_rng():
        torch.manual_seed(117)
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
    return torch.tensor([[5, 8, 13, 21, 34, 55]], dtype=torch.long)


def anchor_for(ids, *, start=4, length=2):
    prefix = tuple(ids[0].tolist())
    return SemanticAnchor(
        role="shared neutral continuation cue", start=start,
        token_ids=prefix[start:start + length], prefix_token_ids=prefix,
        rationale="This exact cue span is fixed before any generated answer tokens.",
    )


def hook_counts(model):
    return tuple(len(layer._forward_hooks) for layer in model.model.layers)


def test_capture_matches_block_output_and_next_block_input(model, ids):
    observed = {}
    block_handle = model.model.layers[0].register_forward_hook(
        lambda _module, _args, output: observed.update(block=output.detach())
    )
    next_handle = model.model.layers[1].register_forward_pre_hook(
        lambda _module, args, kwargs: observed.update(next_input=args[0].detach().clone()),
        with_kwargs=True,
    )
    try:
        result = forward_reference(model, ids, capture_site=ResidualSite(0, (4, 1)))
    finally:
        block_handle.remove()
        next_handle.remove()
    torch.testing.assert_close(observed["block"], observed["next_input"], rtol=0, atol=0)
    torch.testing.assert_close(result.residual, observed["block"][:, [4, 1]], rtol=0, atol=0)
    assert result.residual.shape == (1, 2, 32)
    assert result.residual.device.type == "cpu"
    assert not result.residual.requires_grad
    assert result.residual.grad_fn is None
    observed["block"].fill_(123)
    assert not bool((result.residual == 123).any())


def test_capture_identity_zero_strength_and_zero_delta_preserve_logits_rng(model, ids):
    site = ResidualSite(1, (4, 5))
    baseline = forward_reference(model, ids).logits
    before = torch.random.get_rng_state().clone()
    capture = forward_reference(model, ids, capture_site=site)
    variants = (
        IdentityIntervention(site),
        AdditiveIntervention(site, torch.ones(32), anchor_for(ids), strength=0.0),
        AdditiveIntervention(site, torch.zeros(2, 32), anchor_for(ids), strength=8.0),
    )
    torch.testing.assert_close(capture.logits, baseline, rtol=0, atol=0)
    for intervention in variants:
        result = forward_reference(model, ids, intervention=intervention)
        torch.testing.assert_close(result.logits, baseline, rtol=0, atol=0)
    assert torch.equal(before, torch.random.get_rng_state())
    assert hook_counts(model) == (0, 0, 0)


def test_selected_addition_is_effective_and_unrelated_positions_are_unchanged(model, ids):
    site = ResidualSite(1, (4,))
    delta = torch.linspace(-0.4, 0.4, 32)
    baseline = forward_reference(model, ids, capture_site=ResidualSite(2, (0, 1, 2, 3, 4, 5)))
    observed = {}
    downstream = model.model.layers[1].register_forward_hook(
        lambda _module, _args, output: observed.update(clean_block=output.detach().clone())
    )
    after = None
    try:
        with residual_hooks(model, ids, capture_site=site,
                            intervention=AdditiveIntervention(site, delta, anchor_for(ids)) ) as state:
            final_handle = model.model.layers[1].register_forward_hook(
                lambda _module, _args, output: observed.update(patched_block=output.detach().clone())
            )
            try:
                after = model(input_ids=ids, use_cache=False, return_dict=True)
            finally:
                final_handle.remove()
            captured = state.captured
    finally:
        downstream.remove()
    torch.testing.assert_close(observed["patched_block"][:, [0, 1, 2, 3, 5]],
                               observed["clean_block"][:, [0, 1, 2, 3, 5]], rtol=0, atol=0)
    torch.testing.assert_close(observed["patched_block"][:, 4], observed["clean_block"][:, 4] + delta)
    torch.testing.assert_close(captured, observed["clean_block"][:, [4]], rtol=0, atol=0)
    assert (after.logits[:, 4:] - baseline.logits[:, 4:]).abs().max().item() > 0.01
    torch.testing.assert_close(after.logits[:, :4], baseline.logits[:, :4], rtol=0, atol=0)


def test_shared_prefix_states_ignore_different_future_teacher_forcing(model):
    prefix = [5, 8, 13, 21]
    left = torch.tensor([prefix + [34, 55, 89]], dtype=torch.long)
    right = torch.tensor([prefix + [3, 7]], dtype=torch.long)
    for layer in (0, 1, 2):
        site = ResidualSite(layer, (0, 1, 2, 3))
        a = forward_reference(model, left, capture_site=site)
        b = forward_reference(model, right, capture_site=site)
        torch.testing.assert_close(a.residual, b.residual, rtol=1e-6, atol=1e-7)
        torch.testing.assert_close(a.logits[:, :4], b.logits[:, :4], rtol=1e-6, atol=1e-7)
    # Future text really did change the computation at a future position.
    assert not torch.allclose(a.logits[:, 4], b.logits[:, 4])


def test_anchor_checks_exact_prefix_and_declared_cue_positions(model, ids):
    site = ResidualSite(0, (4,))
    intervention = AdditiveIntervention(site, torch.ones(32), anchor_for(ids))
    extended = torch.cat((ids, torch.tensor([[7, 9]])), dim=1)
    forward_reference(model, extended, intervention=intervention)
    changed = extended.clone()
    changed[0, 0] = 6
    with pytest.raises(ValueError, match="prefix differs"):
        forward_reference(model, changed, intervention=intervention)
    with pytest.raises(ValueError, match="complete anchored"):
        forward_reference(model, ids[:, :5], intervention=intervention)
    with pytest.raises(ValueError, match="semantic cue span"):
        forward_reference(model, ids, intervention=AdditiveIntervention(ResidualSite(0, (2,)),
                          torch.ones(32), anchor_for(ids)))
    assert hook_counts(model) == (0, 0, 0)


def test_hook_cleanup_preserves_external_hooks_on_body_and_forward_errors(model, ids):
    handle = model.model.layers[0].register_forward_hook(lambda _m, _a, _o: None)
    counts = hook_counts(model)
    try:
        with pytest.raises(RuntimeError, match="deliberate"):
            with residual_hooks(model, ids, capture_site=ResidualSite(0, (4,))):
                raise RuntimeError("deliberate context body failure")
        assert hook_counts(model) == counts
        intervention = AdditiveIntervention(ResidualSite(0, (4,)),
                                            torch.full((32,), torch.finfo(torch.float32).max),
                                            anchor_for(ids), strength=2.0)
        with pytest.raises(ValueError, match="scaled delta is nonfinite"):
            forward_reference(model, ids, intervention=intervention)
        assert hook_counts(model) == counts
    finally:
        handle.remove()


def test_partial_hook_registration_is_cleaned_up(model, ids, monkeypatch):
    counts = hook_counts(model)
    def failed_register(*args, **kwargs):
        raise RuntimeError("deliberate registration failure")
    monkeypatch.setattr(model.model.layers[1], "register_forward_hook", failed_register)
    intervention = IdentityIntervention(ResidualSite(1, (4,)))
    with pytest.raises(RuntimeError, match="registration failure"):
        with residual_hooks(model, ids, capture_site=ResidualSite(0, (4,)), intervention=intervention):
            pass
    assert hook_counts(model) == counts


@pytest.mark.parametrize("bad_layout", [False, True])
def test_nonfinite_or_changed_block_output_layout_fails_and_removes_owned_hook(model, ids, bad_layout):
    def corrupt_output(_module, _args, output):
        return (output,) if bad_layout else torch.full_like(output, float("nan"))
    handle = model.model.layers[0].register_forward_hook(corrupt_output)
    counts = hook_counts(model)
    try:
        with pytest.raises(ValueError, match="shape|finite"):
            forward_reference(model, ids, capture_site=ResidualSite(0, (4,)))
        assert hook_counts(model) == counts
    finally:
        handle.remove()


@pytest.mark.parametrize("delta", [torch.ones(31), torch.ones(1, 1, 32), torch.ones(2, 32)])
def test_wrong_delta_shapes_fail_before_hook_installation(model, ids, delta):
    with pytest.raises(ValueError, match="delta shape"):
        forward_reference(model, ids, intervention=AdditiveIntervention(
            ResidualSite(0, (4,)), delta, anchor_for(ids)))
    assert hook_counts(model) == (0, 0, 0)


@pytest.mark.parametrize("delta,strength", [(torch.full((32,), float("nan")), 0),
                                          (torch.ones(32), float("inf")),
                                          (torch.ones(32, dtype=torch.long), 1)])
def test_nonfinite_or_nonfloating_interventions_fail(ids, delta, strength):
    with pytest.raises(ValueError):
        AdditiveIntervention(ResidualSite(0, (4,)), delta, anchor_for(ids), strength=strength)


@pytest.mark.parametrize("site", [ResidualSite(3, (4,)), ResidualSite(0, (6,))])
def test_bad_sites_fail_before_hooks(model, ids, site):
    with pytest.raises(ValueError):
        forward_reference(model, ids, capture_site=site)
    assert hook_counts(model) == (0, 0, 0)


@pytest.mark.parametrize("bad_ids", [torch.tensor([[5.0, 8.0]]), torch.tensor([[5], [8]]),
                                     torch.tensor([[]], dtype=torch.long), torch.tensor([[97]])])
def test_invalid_reference_inputs_are_rejected(model, bad_ids):
    with pytest.raises(ValueError):
        forward_reference(model, bad_ids)


def test_training_and_trainable_parameters_are_rejected(model, ids):
    model.train()
    try:
        with pytest.raises(ValueError, match="eval mode"):
            forward_reference(model, ids)
    finally:
        model.eval()
    parameter = next(model.parameters())
    parameter.requires_grad_(True)
    try:
        with pytest.raises(ValueError, match="frozen"):
            forward_reference(model, ids)
    finally:
        parameter.requires_grad_(False)
