import json

import pytest
import torch

from novel.diagnostics import comparison_failure, numerical_runtime, tensor_sha256


def test_failure_evidence_retains_actual_values_and_limits_rows():
    left = torch.arange(60, dtype=torch.float32).reshape(1, 3, 20)
    right = left + 0.5
    right[0, 2, 19] += 1
    evidence = comparison_failure(left, right, atol=0, rtol=0)
    assert evidence["mismatch_count"] == 60
    assert len(evidence["largest_failing_values"]) == 8
    assert evidence["largest_failing_values"][0] == {"index": [0, 2, 19], "left": 59.0, "right": 60.5, "abs_error": 1.5}
    assert evidence["left_sha256"] == tensor_sha256(left)
    assert evidence["right_sha256"] != evidence["left_sha256"]
    assert not evidence["full_tensors_retained"]
    assert len(json.dumps(evidence)) < 4096


def test_sampling_reports_only_failed_entries_under_the_original_tolerance():
    left, right = torch.tensor([1.0, 1000.0]), torch.tensor([1.01, 1001.0])
    evidence = comparison_failure(left, right, atol=0, rtol=0.001)
    assert evidence["mismatch_count"] == 1
    assert evidence["largest_failing_values"][0]["index"] == [0]


def test_failure_sampling_does_not_lose_float64_or_bfloat16_values():
    left = torch.tensor([1.0], dtype=torch.float64)
    right = left + 1e-10
    result = comparison_failure(left, right, atol=0, rtol=0)
    assert result["largest_failing_values"][0]["right"] == right.item()
    assert result["largest_failing_values"][0]["abs_error"] > 0
    assert len(tensor_sha256(torch.tensor(1.0, dtype=torch.bfloat16))) == 64


def test_nonfinite_failure_evidence_is_strict_json_serializable():
    evidence = comparison_failure(torch.tensor([float("nan")]), torch.tensor([float("inf")]), atol=0, rtol=0)
    json.dumps(evidence, allow_nan=False)


def test_diagnostic_does_not_consume_rng_or_change_inputs():
    left, right = torch.ones(4), torch.zeros(4)
    rng = torch.get_rng_state().clone()
    versions = left._version, right._version
    comparison_failure(left, right, atol=0, rtol=0)
    assert torch.equal(rng, torch.get_rng_state())
    assert (left._version, right._version) == versions


def test_runtime_records_threading_backend_and_determinism():
    runtime = numerical_runtime()
    assert runtime["threads"] == torch.get_num_threads()
    assert "MKL_DYNAMIC" in runtime["environment_controls"]
    assert runtime["float32_matmul_precision"] == torch.get_float32_matmul_precision()
    assert runtime["torch_build"] and runtime["parallel_info"]


def test_broadcast_failure_does_not_mislabel_coordinates():
    with pytest.raises(ValueError, match="matching tensor shapes"):
        comparison_failure(torch.ones(1), torch.zeros(2), atol=0, rtol=0)
