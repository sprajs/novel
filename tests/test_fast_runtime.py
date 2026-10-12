"""Scientific-contract and runtime guards; no downloads or GPU required."""
import hashlib
import json
import math
from pathlib import Path

import pytest

from novel.fast_runtime import (PIN, backend_config, checked_completion, completion_request,
                                full_logprobs, gpu_preflight, host_record, logprob_metrics, reject_implicit_overrides, server_command, verify_artifact,
                                verify_build, verify_full_offload, write_new)


def distribution(values):
    return {"completion_probabilities": [{"top_logprobs": [{"id": i, "logprob": v} for i, v in enumerate(values)]}]}


def test_full_vocabulary_likelihood_and_fail_closed_on_missing_tail():
    values = [math.log(0.75), math.log(0.25)]
    assert full_logprobs(distribution(values), 2) == values
    with pytest.raises(ValueError, match="complete"):
        full_logprobs(distribution(values[:1]), 2)
    with pytest.raises(ValueError, match="Unnormalized"):
        full_logprobs(distribution([-1, -1]), 2)


@pytest.mark.parametrize("value", [None, float("nan"), float("inf"), -3.402823466e38])
def test_invalid_or_float_underflow_floor_is_not_a_log_likelihood(value):
    with pytest.raises(ValueError, match="Nonfinite/floored"):
        full_logprobs(distribution([0.0, value]), 2)


def test_duplicate_token_ids_and_post_sampling_probs_rejected():
    response = distribution([math.log(0.5)] * 2)
    response["completion_probabilities"][0]["top_logprobs"][1]["id"] = 0
    with pytest.raises(ValueError, match="complete"):
        full_logprobs(response, 2)
    with pytest.raises(ValueError, match="complete"):
        full_logprobs({"completion_probabilities": [{"top_probs": [{"id": 0, "prob": 1}]}]}, 1)


def test_kl_normalization_does_not_erase_raw_likelihood_error():
    reference = [math.log(0.75), math.log(0.25)]
    fast = [value + math.log(1.00003) for value in reference]
    metrics = logprob_metrics(reference, fast, fast, 1)
    # Same normalized distribution, despite the backend's raw mass/score error.
    assert abs(metrics["kl_reference_to_fast"]) < 1e-15
    assert metrics["raw_probability_mass_error"] == pytest.approx(0.00003)
    assert metrics["fast_target_logprob"] != metrics["reference_target_logprob"]
    assert metrics["normalized_fast_target_logprob"] == pytest.approx(reference[1])
    different = [math.log(0.5)] * 2
    assert logprob_metrics(reference, different, different, 1)["kl_reference_to_fast"] == pytest.approx(0.13081203594113697)


def test_exact_prompt_ids_no_sampling_filter_prompt_reuse_or_stop_strings():
    request = completion_request([17, 151645])
    assert request["prompt"] == [17, 151645]
    assert request["temperature"] == -1 and request["samplers"] == ["temperature"]
    assert request["min_p"] == 0 and request["repeat_penalty"] == 1
    assert request["post_sampling_probs"] is False
    assert request["cache_prompt"] is False and request["return_tokens"] is True
    assert request["stop"] == [] and request["ignore_eos"] is False
    with pytest.raises(ValueError):
        completion_request([1], tokens=True)
    with pytest.raises(ValueError):
        completion_request([1], seed=2**32 - 1)


def test_sampling_is_explicit_and_not_an_equivalence_claim():
    request = completion_request([1], seed=42, temperature=0.7, top_k=20, top_p=0.8)
    assert request["samplers"] == ["top_k", "top_p", "min_p", "temperature"]
    assert request["post_sampling_probs"] is False and request["seed"] == 42
    with pytest.raises(ValueError, match="temperature"):
        completion_request([1], temperature=float("nan"))


class StubClient:
    def __init__(self, result):
        self.result, self.calls = result, 0

    def call(self, endpoint, request):
        assert endpoint == "/completion"
        self.calls += 1
        return self.result


def test_context_overflow_fails_before_inference():
    client = StubClient({})
    with pytest.raises(ValueError, match="context"):
        checked_completion(client, completion_request([1] * 10), 12)
    assert client.calls == 0


def test_equality_context_boundary_requires_one_token_slack():
    client = StubClient({})
    with pytest.raises(ValueError, match="one token"):
        checked_completion(client, completion_request([1] * 10, tokens=2), 12)
    assert client.calls == 0


@pytest.mark.parametrize("changed", [{"truncated": True}, {"tokens_evaluated": 3}, {"tokens": None}, {"stop_type": "none"}])
def test_truncation_implicit_bos_and_missing_token_trace_fail(changed):
    client = StubClient({"truncated": False, "tokens_evaluated": 2, "tokens": [3], "stop_type": "limit", **changed})
    with pytest.raises(ValueError):
        checked_completion(client, completion_request([1, 2]), 512)


def test_raw_terminal_eog_can_differ_from_rendered_content():
    response = {"truncated": False, "tokens_evaluated": 1, "tokens": [151645], "stop_type": "eos", "content": ""}
    assert checked_completion(StubClient(response), completion_request([1]), 512) == response


def test_explicit_server_numerical_conditions_and_slots():
    cpu = backend_config()["profiles"]["cloud-cpu"]
    cmd = server_command(Path("server"), Path("model.gguf"), cpu, port=1234, slots=2)
    assert cmd[cmd.index("--ctx-size") + 1] == "1024"
    assert cmd[cmd.index("--parallel") + 1] == "2"
    assert cmd[cmd.index("--flash-attn") + 1] == "off"
    assert cmd[cmd.index("--host") + 1] == "127.0.0.1"
    assert "--no-context-shift" in cmd and "--no-cache-prompt" in cmd and "--no-warmup" in cmd
    assert cmd[cmd.index("--reasoning") + 1] == "off"
    assert cmd[cmd.index("--verbosity") + 1] == "4"


def test_artifact_and_native_libraries_integrity_checked(tmp_path):
    model = tmp_path / "F16.gguf"
    model.write_bytes(b"model")
    write_new(model.with_suffix(".gguf.json"), {"llama_commit": PIN, "artifact_sha256": hashlib.sha256(b"model").hexdigest(), "quantization": "F16"})
    assert verify_artifact(model)["quantization"] == "F16"
    model.write_bytes(b"changed")
    with pytest.raises(ValueError, match="integrity"):
        verify_artifact(model)
    build = tmp_path / "build"
    (build / "bin").mkdir(parents=True)
    hashes = {}
    for name in ("llama-server", "llama-bench", "llama-quantize", "libllama.so"):
        (build / "bin" / name).write_bytes(b"binary")
        hashes[name] = hashlib.sha256(b"binary").hexdigest()
    write_new(build / "receipt.json", {"commit": PIN, "profile": "cloud-cpu", "runtime_hashes": hashes})
    verify_build(build, "cloud-cpu")
    (build / "bin/libllama.so").write_bytes(b"different")
    with pytest.raises(ValueError, match="integrity"):
        verify_build(build, "cloud-cpu")


def test_gpu_planning_rejects_wrong_device_or_exhausted_memory(monkeypatch):
    monkeypatch.delenv("CUDA_VISIBLE_DEVICES", raising=False)
    profile = backend_config()["profiles"]["rental"]
    artifact = {"artifact_bytes": 16 * 1024**3, "model_key": "qwen3_8b"}
    monkeypatch.setattr("subprocess.check_output", lambda *a, **k: "NVIDIA GeForce RTX 5090, 12.0, 32768, 32000, 570.124.06")
    assert gpu_preflight("rental", profile, artifact, 1)["status"] == "PASS"
    monkeypatch.setattr("subprocess.check_output", lambda *a, **k: "NVIDIA GeForce RTX 5090, 12.0, 32768, 12000, 570.124.06")
    with pytest.raises(ValueError, match="free VRAM"):
        gpu_preflight("rental", profile, artifact, 1)
    monkeypatch.setattr("subprocess.check_output", lambda *a, **k: "NVIDIA GeForce RTX 4090, 8.9, 24576, 24000, 570.124.06")
    with pytest.raises(ValueError, match="name/compute"):
        gpu_preflight("rental", profile, artifact, 1)


def test_requested_gpu_layers_do_not_establish_actual_gpu_execution():
    assert verify_full_offload("load_tensors: offloaded 37/37 layers to GPU")["total_layers"] == 37
    for text in ("warning: no usable GPU found", "offloaded 10/37 layers to GPU", "offloaded 0/0 layers to GPU"):
        with pytest.raises(ValueError, match="Full GPU offload"):
            verify_full_offload(text)


def test_receipts_and_outputs_are_not_overwritten(tmp_path):
    path = tmp_path / "result.json"
    write_new(path, {"status": "FAIL"})
    with pytest.raises(FileExistsError):
        write_new(path, {"status": "PASS"})
    assert json.loads(path.read_text())["status"] == "FAIL"


def test_implicit_server_keys_are_rejected_without_recording_secrets(monkeypatch):
    monkeypatch.setenv("LLAMA_ARG_API_KEY", "do-not-save-this-secret")
    assert "LLAMA_ARG_API_KEY" not in host_record()["environment"]
    with pytest.raises(ValueError, match="implicit LLAMA_ARG"):
        reject_implicit_overrides()
