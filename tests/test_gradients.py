import pytest
import torch
from transformers import Qwen3Config, Qwen3ForCausalLM

from novel.activation import AdditiveIntervention, ResidualSite, SemanticAnchor, forward_reference, prepare_reference_model
from novel.gradients import activation_gradient


def fixture():
    with torch.random.fork_rng():
        torch.manual_seed(25)
        config = Qwen3Config(vocab_size=31, hidden_size=16, intermediate_size=32,
                            num_hidden_layers=3, num_attention_heads=2, num_key_value_heads=1,
                            head_dim=8, max_position_embeddings=64)
        config._attn_implementation = "eager"
        return prepare_reference_model(Qwen3ForCausalLM(config)), torch.tensor([[1, 3, 7, 2]])


def test_selected_activation_derivative_matches_central_finite_difference():
    model, ids = fixture()
    site = ResidualSite(1, (3,))
    state = [(id(p), p._version) for p in model.parameters()]
    result = activation_gradient(model, ids, site, 5, 9)
    direction = torch.linspace(-1, 1, model.config.hidden_size)
    anchor = SemanticAnchor("diagnostic", 3, (2,), tuple(ids[0].tolist()), "Fixed mechanics cue")
    epsilon = 1e-3
    scores = []
    for strength in (epsilon, -epsilon):
        logits = forward_reference(model, ids, intervention=AdditiveIntervention(site, direction, anchor, strength)).logits
        scores.append(float(logits[0, -1, 5] - logits[0, -1, 9]))
    numeric = (scores[0] - scores[1]) / (2 * epsilon)
    analytic = float((result.gradient[0, 0] * direction).sum())
    assert analytic == pytest.approx(numeric, abs=1e-4, rel=2e-3)
    assert result.gradient.shape == (1, 1, 16) and not result.gradient.requires_grad
    assert state == [(id(p), p._version) for p in model.parameters()]
    assert all(p.grad is None and not p.requires_grad for p in model.parameters())
    assert all(not layer._forward_hooks for layer in model.model.layers)


def test_gradient_runs_inside_no_grad_but_rejects_inference_mode():
    model, ids = fixture()
    with torch.no_grad():
        assert activation_gradient(model, ids, ResidualSite(1, (3,)), 5, 9).gradient.abs().sum() > 0
    with torch.inference_mode(), pytest.raises(ValueError, match="inference_mode"):
        activation_gradient(model, ids, ResidualSite(1, (3,)), 5, 9)


def test_gradient_cleans_owned_hook_on_forward_failure(monkeypatch):
    model, ids = fixture()
    monkeypatch.setattr(model, "forward", lambda **_: (_ for _ in ()).throw(RuntimeError("mock failure")))
    with pytest.raises(RuntimeError, match="mock failure"):
        activation_gradient(model, ids, ResidualSite(1, (3,)), 5, 9)
    assert all(not layer._forward_hooks for layer in model.model.layers)


@pytest.mark.parametrize("site,tokens", [(ResidualSite(3, (0,)), (5, 9)), (ResidualSite(1, (4,)), (5, 9)),
                                        (ResidualSite(1, (0,)), (5, 5)), (ResidualSite(1, (0,)), (5, 31))])
def test_gradient_rejects_invalid_sites_and_objectives(site, tokens):
    model, ids = fixture()
    with pytest.raises(ValueError):
        activation_gradient(model, ids, site, *tokens)
