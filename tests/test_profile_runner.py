"""Exercise the complete runner against real tiny Qwen3; no model downloads."""
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
import torch
from transformers import Qwen3Config, Qwen3ForCausalLM

from novel import profile_runner, runner
from novel.models import model_entry
from novel.profiles import ProfileRequest


@pytest.fixture
def prepared(tmp_path, monkeypatch):
    with torch.random.fork_rng():
        torch.manual_seed(23)
        config = Qwen3Config(vocab_size=31, hidden_size=16, intermediate_size=32,
                            num_hidden_layers=3, num_attention_heads=2, num_key_value_heads=1,
                            head_dim=8, max_position_embeddings=64, eos_token_id=None)
        config._attn_implementation = "eager"
        model = Qwen3ForCausalLM(config)
    entry = model_entry(Path("configs/models.json"), "qwen3_0_6b")
    entry["parameters"]["unique_config_implied"] = sum(p.numel() for p in model.parameters())
    entry["model_config"] = config.to_dict()
    monkeypatch.setattr(runner, "model_entry", lambda *_: entry)
    monkeypatch.setattr(profile_runner, "model_entry", lambda *_: entry)
    monkeypatch.setattr(runner, "verify_snapshot", lambda *_: {"fixture": "not a pretrained model"})
    monkeypatch.setattr(runner.AutoModelForCausalLM, "from_pretrained", Mock(return_value=model))

    class Tokenizer:
        chat_template = "offline fixture template"

        def apply_chat_template(self, *_args, **_kwargs):
            return "offline fixture prompt"

        def __call__(self, *_args, **_kwargs):
            return SimpleNamespace(input_ids=torch.tensor([[1, 3, 7, 2]]))

        def encode(self, text, **_kwargs):
            return [5 if text == " A" else 6]

        def decode(self, ids, **_kwargs):
            return repr(ids)

    monkeypatch.setattr(runner.AutoTokenizer, "from_pretrained", Mock(return_value=Tokenizer()))
    monkeypatch.setattr(profile_runner, "inspect_hardware", lambda _: {"torch_version": "2.8.0+cpu"})
    conf = json.loads(Path("configs/cpu-smoke.json").read_text())
    conf["layer"] = 1
    path = tmp_path / "config.json"
    path.write_text(json.dumps(conf))
    return dict(registry=Path("configs/models.json"), cache=tmp_path, runs=tmp_path / "runs", config=path), model


def test_complete_profile_report_tokens_capture_gradient_and_inventory(prepared):
    kwargs, model = prepared
    code, path = profile_runner.validate_profile(ProfileRequest(gradient=True), **kwargs)
    report = json.loads(path.read_text())
    assert code == 0, report
    assert report["checks"]["activation_gradient"]["status"] == "PASS"
    assert report["checks"]["cuda_kernel"]["status"] == "SKIP"
    assert not report["gpu_model_validated"]
    run_path = Path(report["run_path"])
    tokens = json.loads((run_path / "tokens.json").read_text())
    generations = tokens["generations"]
    assert len(generations) == 4 and all(g["generated_ids"] == generations[0]["generated_ids"] for g in generations)
    assert [g["cache_policy"] for g in generations] == ["full_prefix_cache_disabled"] * 4
    assert (run_path / "gradient.safetensors").is_file()
    assert all(report["invariants"][f"clean_cache_logits_{i}"]["status"] == "PASS" for i in range(3))
    assert report["invariants"]["capture_logits"]["atol"] == 0
    record = json.loads((run_path / "run.json").read_text())
    assert record["validation_forward_calls"] == 15 and record["backward_calls"] == 1
    assert record["device"] == "cpu" and record["dtype"] == "float32"
    assert all(p.grad is None and not p.requires_grad for p in model.parameters())
    assert (run_path / "inventory.json").is_file()


def test_preflight_skip_never_claims_model_validation(prepared):
    kwargs, _model = prepared
    code, path = profile_runner.validate_profile(ProfileRequest(), preflight_only=True, **kwargs)
    report = json.loads(path.read_text())
    assert code == 0
    assert report["checks"]["pretrained_smoke"]["status"] == "SKIP"
    runner.AutoModelForCausalLM.from_pretrained.assert_not_called()


def test_failure_preserves_partial_run_and_raw_failure(prepared, monkeypatch):
    kwargs, model = prepared
    monkeypatch.setattr(model, "forward", Mock(side_effect=torch.OutOfMemoryError("fixture OOM")))
    code, path = profile_runner.validate_profile(ProfileRequest(), **kwargs)
    report = json.loads(path.read_text())
    assert code == 1 and report["error"]["out_of_memory"]
    assert report["partial_run"]["status"] == "failed"
    assert (Path(report["run_path"]) / "error.json").is_file()
    assert report["checks"]["pretrained_smoke"]["status"] == "FAIL"


def test_prompt_caps_fail_before_forward(prepared, monkeypatch):
    kwargs, model = prepared
    spy = Mock(side_effect=AssertionError("must not forward"))
    monkeypatch.setattr(model, "forward", spy)
    code, path = profile_runner.validate_profile(ProfileRequest(max_input_tokens=2), **kwargs)
    report = json.loads(path.read_text())
    assert code == 1 and "no silent truncation" in report["error"]["message"]
    spy.assert_not_called()


def test_failed_gradient_is_fail_not_skip(prepared, monkeypatch):
    kwargs, _model = prepared
    monkeypatch.setattr(runner, "activation_gradient", Mock(side_effect=torch.OutOfMemoryError("gradient OOM")))
    code, path = profile_runner.validate_profile(ProfileRequest(gradient=True), **kwargs)
    report = json.loads(path.read_text())
    assert code == 1
    assert report["checks"]["activation_gradient"]["status"] == "FAIL"
    assert report["invariants"]["activation_gradient"]["status"] == "FAIL"
    assert report["invariants"]["clean_cache_logits_2"]["status"] == "PASS"


def test_missing_lock_is_preflight_failure(prepared, monkeypatch):
    kwargs, _model = prepared
    monkeypatch.setattr(profile_runner, "sha256_file", Mock(side_effect=FileNotFoundError("lock missing")))
    code, path = profile_runner.validate_profile(ProfileRequest(), **kwargs)
    report = json.loads(path.read_text())
    assert code == 1
    assert report["checks"]["preflight"]["status"] == "FAIL"
    assert report["checks"]["pretrained_smoke"]["status"] == "SKIP"


def test_later_generation_failure_preserves_successful_gradient(prepared, monkeypatch):
    kwargs, _model = prepared
    monkeypatch.setattr(runner, "generate_reference", Mock(side_effect=RuntimeError("generation failed")))
    code, path = profile_runner.validate_profile(ProfileRequest(gradient=True), **kwargs)
    report = json.loads(path.read_text())
    assert code == 1
    assert report["checks"]["activation_gradient"]["status"] == "PASS"
    assert report["checks"]["pretrained_smoke"]["status"] == "FAIL"


@pytest.mark.parametrize("condition,call_number", [("clean_repeat_logits", 2), ("capture_logits", 3)])
def test_numerical_failure_preserves_replay_context_and_raw_errors(prepared, monkeypatch, condition, call_number):
    kwargs, _model = prepared
    forward = runner.forward_reference
    calls = 0

    def altered(*args, **kw):
        nonlocal calls
        calls += 1
        result = forward(*args, **kw)
        if calls == call_number:
            from dataclasses import replace
            logits = result.logits.clone()
            logits[0, -1, 0] += 0.125
            return replace(result, logits=logits)
        return result

    monkeypatch.setattr(runner, "forward_reference", altered)
    generation = Mock(side_effect=AssertionError("sampling must not start"))
    monkeypatch.setattr(runner, "generate_reference", generation)
    code, path = profile_runner.validate_profile(ProfileRequest(gradient=True), **kwargs)
    report = json.loads(path.read_text())
    assert code == 1 and calls == call_number  # No retry or warmup bypass.
    assert report["checks"]["activation_gradient"]["status"] == "SKIP"
    check = report["invariants"][condition]
    assert check["status"] == "FAIL" and check["atol"] == check["rtol"] == 0
    evidence = check["failure_evidence"]
    assert evidence["mismatch_count"] == 1
    assert evidence["largest_failing_values"][0]["index"] == [0, 3, 0]
    assert evidence["largest_failing_values"][0]["abs_error"] == pytest.approx(.125)
    run_path = Path(report["run_path"])
    context = json.loads((run_path / "execution.json").read_text())
    assert context["input_ids"] == [1, 3, 7, 2]
    assert context["model_revision"] == context["tokenizer_revision"]
    assert context["snapshot_files_sha256"]
    assert context["runtime"]["threads"] == 5
    assert report["partial_run"]["state_at_failure"] == context["initial_state"]
    assert report["partial_run"]["execution_context"] == "execution.json"
    generation.assert_not_called()


@pytest.mark.parametrize("bad", [float("nan"), float("inf")])
@pytest.mark.parametrize("condition,call_number", [("clean_repeat_logits", 2), ("capture_logits", 3)])
def test_nonfinite_comparison_still_saves_the_failed_report(prepared, monkeypatch, bad, condition, call_number):
    kwargs, _model = prepared
    forward, calls = runner.forward_reference, 0

    def altered(*args, **kw):
        nonlocal calls
        calls += 1
        result = forward(*args, **kw)
        if calls == call_number:
            from dataclasses import replace
            logits = result.logits.clone()
            logits[0, -1, 0] = bad
            return replace(result, logits=logits)
        return result

    monkeypatch.setattr(runner, "forward_reference", altered)
    code, path = profile_runner.validate_profile(ProfileRequest(), **kwargs)
    report = json.loads(path.read_text())
    assert code == 1 and report["error"]["type"] == "AssertionError"
    check = report["invariants"][condition]
    assert check["status"] == "FAIL"
    assert check["max_abs_error"] in ("nan", "inf")
    assert check["failure_evidence"]["largest_failing_values"][0]["right"] in ("nan", "inf")
    assert report["partial_run"]["execution_context"] == "execution.json"
    assert calls == call_number


@pytest.mark.parametrize("exception", [MemoryError, TypeError])
def test_diagnostic_errors_cannot_mask_the_original_assertion(prepared, monkeypatch, exception):
    kwargs, _model = prepared
    forward, calls = runner.forward_reference, 0

    def altered(*args, **kw):
        nonlocal calls
        calls += 1
        result = forward(*args, **kw)
        if calls == 2:
            from dataclasses import replace
            return replace(result, logits=result.logits + .125)
        return result

    state, state_calls = runner.reference_state, 0

    def failing_state(*args):
        nonlocal state_calls
        state_calls += 1
        if state_calls > 1:
            raise exception("diagnostic unavailable")
        return state(*args)

    monkeypatch.setattr(runner, "forward_reference", altered)
    monkeypatch.setattr(runner, "reference_state", failing_state)
    monkeypatch.setattr(runner, "comparison_failure", Mock(side_effect=exception("diagnostic unavailable")))
    code, path = profile_runner.validate_profile(ProfileRequest(), **kwargs)
    report = json.loads(path.read_text())
    assert code == 1 and report["error"]["type"] == "AssertionError"
    assert report["invariants"]["clean_repeat_logits"]["failure_evidence_error"] == exception.__name__
    assert report["partial_run"]["state_at_failure_error"] == exception.__name__
    assert calls == 2
