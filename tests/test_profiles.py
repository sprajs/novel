"""Hardware decisions tested without renting a GPU or installing CUDA wheels."""
from dataclasses import replace
import json
from pathlib import Path
from unittest.mock import Mock

import pytest
import torch

from novel.models import model_entry
from novel import profiles
from novel.profiles import GIB, ProfileError, ProfileRequest, memory_estimate, resolve_profile
from novel.profile_runner import validate_profile


def entry(key="qwen3_1_7b"):
    return model_entry(Path("configs/models.json"), key)


def hardware(capability=(7, 5), total=11, free=10, **overrides):
    blackwell = capability == (12, 0)
    result = dict(torch_version="2.8.0+cu128" if blackwell else "2.8.0+cu126",
                  cuda_build="12.8" if blackwell else "12.6", cuda_available=True,
                  device_count=1, device_index=0, name="NVIDIA GeForce RTX 2080 Ti",
                  capability=list(capability), total_bytes=int(total * GIB), free_bytes=int(free * GIB),
                  arch_list=["sm_75", "sm_80", "sm_86", "sm_90"] + (["sm_120"] if blackwell else []),
                  native_bf16=capability[0] >= 8, discovery_error=None)
    result.update(overrides)
    return result


def test_profile_defaults_preserve_models_and_precisions():
    assert ProfileRequest().model_key == "qwen3_0_6b"
    for profile in ("local-2080ti", "rental"):
        assert ProfileRequest(profile).model_key == "qwen3_1_7b"
    result = resolve_profile(ProfileRequest("local-2080ti"), hardware(), entry())
    assert result.dtype == "float16" and result.device == "cuda:0"
    assert result.allocator_limit_bytes == int(10 * GIB * 0.8)


@pytest.mark.parametrize("kwargs", [dict(profile="auto"), dict(dtype="auto"), dict(model="qwen3_8b"),
    dict(device_index=-1), dict(device_index=True), dict(batch_size=2), dict(max_input_tokens=257),
    dict(max_new_tokens=17), dict(max_new_tokens=0), dict(attention_backend="flash_attention_2"),
    dict(attention_backend="sdpa"), dict(quantization="int4"), dict(gradient=1),
    dict(rental_capacity_gib=32), dict(profile="rental", rental_capacity_gib=48)])
def test_invalid_or_unbounded_request(kwargs):
    with pytest.raises(ProfileError):
        ProfileRequest(**kwargs)


@pytest.mark.parametrize("changes,match", [
    (dict(cuda_available=False), "unavailable"), (dict(cuda_build=None), "unavailable"),
    (dict(torch_version="2.8.0+cpu"), "cu126"), (dict(cuda_build="13.0"), "cu126"),
    (dict(arch_list=["sm_80"]), "cubin"), (dict(discovery_error="driver failed"), "inspect"),
    (dict(total_bytes=8*GIB), "capacity"), (dict(free_bytes=GIB), "Estimated"),
    (dict(free_bytes=0), "free VRAM"), (dict(name="Tesla T4"), "2080 Ti"),
])
def test_incompatible_devices_builds_and_resources(changes, match):
    with pytest.raises(ProfileError, match=match):
        resolve_profile(ProfileRequest("local-2080ti"), hardware(**changes), entry())


def test_cuda_index_and_dtype_guards():
    with pytest.raises(ProfileError, match="device"):
        resolve_profile(ProfileRequest("local-2080ti", device_index=1), hardware(), entry())
    with pytest.raises(ProfileError, match="FP16"):
        resolve_profile(ProfileRequest("local-2080ti", dtype="bfloat16"), hardware(native_bf16=True), entry())
    with pytest.raises(ProfileError, match="native"):
        resolve_profile(ProfileRequest("rental", dtype="bfloat16"), hardware((8, 6), 24, 23, native_bf16=False), entry())


@pytest.mark.parametrize("capability", [(8, 6), (8, 9), (12, 0)])
def test_rental_uses_actual_architecture_not_card_label(capability):
    resolved = resolve_profile(ProfileRequest("rental"), hardware(capability, 32, 30, name="arbitrary provider label"), entry())
    assert resolved.capacity_budget_bytes == 24 * GIB
    assert resolved.stack == ("cu128" if capability == (12, 0) else "cu126")
    assert resolved.allocator_limit_bytes == int(24 * GIB * .8)


def test_blackwell_cannot_use_turing_wheel_and_32_requires_capacity():
    with pytest.raises(ProfileError, match="cu128"):
        resolve_profile(ProfileRequest("rental"), hardware((12, 0), 32, 30, torch_version="2.8.0+cu126", cuda_build="12.6"), entry())
    with pytest.raises(ProfileError, match="capacity"):
        resolve_profile(ProfileRequest("rental", rental_capacity_gib=32), hardware((8, 9), 24, 23), entry())
    result = resolve_profile(ProfileRequest("rental", rental_capacity_gib=32), hardware((12, 0), 32, 30), entry())
    assert result.capacity_budget_bytes == 32 * GIB
    assert result.allocator_limit_bytes == int(30 * GIB * .8)


def test_unknown_architecture_and_wrong_direction_cubins_rejected():
    with pytest.raises(ProfileError, match="architecture"):
        resolve_profile(ProfileRequest("rental"), hardware((10, 3), 32, 30), entry())
    with pytest.raises(ProfileError, match="cubin"):
        resolve_profile(ProfileRequest("rental"), hardware((8, 6), 24, 23, arch_list=["sm_89"]), entry())


def test_cpu_pin_and_fp32_are_preserved():
    h = dict(torch_version="2.8.0+cpu", cuda_available=False, cuda_build=None)
    assert resolve_profile(ProfileRequest(), h, entry("qwen3_0_6b")).lock_path == "uv.lock"
    with pytest.raises(ProfileError, match="FP32"):
        resolve_profile(ProfileRequest(dtype="float16"), h, entry())
    with pytest.raises(ProfileError, match="2.8.0\\+cpu"):
        resolve_profile(ProfileRequest(), {**h, "torch_version": "2.8.0+cu126"}, entry())


def test_memory_math_counts_tied_weights_kv_and_backward_separately():
    request = ProfileRequest("local-2080ti")
    small = memory_estimate(entry("qwen3_0_6b"), request, "float16")
    primary = memory_estimate(entry(), request, "float16")
    assert primary["weight_bytes"] == 1_720_574_976 * 2
    assert primary["kv_cache_bytes"] == small["kv_cache_bytes"] == 114_688 * 136
    assert primary["planning_bytes"] > primary["weight_bytes"] + primary["kv_cache_bytes"]
    backward = memory_estimate(entry(), replace(request, gradient=True), "float16")
    assert backward["backward_activation_estimate_bytes"] > 0
    assert backward["planning_bytes"] > primary["planning_bytes"]
    assert backward["parameter_gradient_bytes"] == backward["optimizer_bytes"] == 0


def test_cuda_kernel_failure_is_actionable(monkeypatch):
    resolved = resolve_profile(ProfileRequest("local-2080ti"), hardware(), entry())
    monkeypatch.setattr(torch.cuda, "set_per_process_memory_fraction", Mock(side_effect=RuntimeError("driver too old")))
    with pytest.raises(ProfileError, match="driver/runtime"):
        profiles.initialize_device(resolved)


def test_cpu_kernel_is_explicit_skip():
    resolved = resolve_profile(ProfileRequest(), {"torch_version": "2.8.0+cpu"}, entry())
    assert profiles.initialize_device(resolved)["status"] == "SKIP"


def test_oom_is_not_retried_or_disguised():
    result = profiles.failure_record(torch.OutOfMemoryError("test allocation"))
    assert result["status"] == "FAIL" and result["out_of_memory"]
    assert "No automatic retry or CPU fallback" in result["next_action"]


def test_missing_cuda_produces_shareable_failed_report_before_loading(tmp_path, monkeypatch):
    from novel import profile_runner
    monkeypatch.setattr(profile_runner, "inspect_hardware", lambda _: {"torch_version": "2.8.0+cpu", "cuda_available": False, "cuda_build": None})
    loader = Mock(side_effect=AssertionError("must not load weights"))
    monkeypatch.setattr(profile_runner, "run", loader)
    code, path = validate_profile(ProfileRequest("local-2080ti"), registry=Path("configs/models.json"),
                                 cache=tmp_path, runs=tmp_path, config=Path("configs/cpu-smoke.json"))
    report = json.loads(path.read_text())
    assert code == 1 and report["status"] == "FAIL"
    assert report["checks"]["preflight"]["status"] == "FAIL"
    assert report["checks"]["pretrained_smoke"]["status"] == "SKIP"
    assert not report["gpu_model_validated"]
    loader.assert_not_called()


def test_model_oom_report_keeps_passed_preflight_and_no_false_gpu_pass(tmp_path, monkeypatch):
    from novel import profile_runner
    monkeypatch.setattr(profile_runner, "inspect_hardware", lambda _: hardware())
    monkeypatch.setattr(profile_runner, "initialize_device", lambda _: {"status": "PASS"})
    monkeypatch.setattr(profile_runner, "validate_environment", lambda _: {"mocked": True})
    monkeypatch.setattr(profile_runner, "memory_record", lambda _: {})
    loader = Mock(side_effect=torch.OutOfMemoryError("mocked OOM"))
    monkeypatch.setattr(profile_runner, "run", loader)
    code, path = validate_profile(ProfileRequest("local-2080ti"), registry=Path("configs/models.json"),
                                 cache=tmp_path, runs=tmp_path, config=Path("configs/cpu-smoke.json"))
    report = json.loads(path.read_text())
    assert code == 1 and report["error"]["out_of_memory"]
    assert report["checks"]["preflight"]["status"] == "PASS"
    assert report["checks"]["pretrained_smoke"]["status"] == "FAIL"
    assert not report["gpu_model_validated"]
    assert loader.call_count == 1


def test_installed_dependencies_must_match_selected_lock(monkeypatch):
    resolved = resolve_profile(ProfileRequest(), {"torch_version": "2.8.0+cpu"}, entry())
    version = profiles.importlib.metadata.version
    monkeypatch.setattr(profiles.importlib.metadata, "version",
                        lambda name: "4.99.0" if name == "transformers" else version(name))
    with pytest.raises(ProfileError, match="transformers: expected 4.57.6, found 4.99.0"):
        profiles.validate_environment(resolved)


def test_cuda_kernel_oom_remains_an_oom(monkeypatch):
    resolved = resolve_profile(ProfileRequest("local-2080ti"), hardware(), entry())
    monkeypatch.setattr(torch.cuda, "set_per_process_memory_fraction", Mock(side_effect=torch.OutOfMemoryError("kernel OOM")))
    with pytest.raises(torch.OutOfMemoryError):
        profiles.initialize_device(resolved)
