"""Bounded failure evidence and read-only numerical-runtime provenance."""

import hashlib
import json
import math
import os

import torch


def tensor_sha256(tensor: torch.Tensor) -> str:
    raw = tensor.detach().cpu().contiguous().reshape(-1).view(torch.uint8).numpy()
    return hashlib.sha256(memoryview(raw)).hexdigest()


def reference_state(model, device: str) -> dict:
    """Small state fingerprints; parameter versions are not weight-content hashes."""
    versions = {name: p._version for name, p in model.named_parameters()}
    return {
        "cpu_rng_sha256": tensor_sha256(torch.random.get_rng_state()),
        "cuda_rng_sha256": tensor_sha256(torch.cuda.get_rng_state(device)) if device.startswith("cuda:") else None,
        "buffer_sha256": {name: tensor_sha256(buffer) for name, buffer in model.named_buffers()},
        "parameter_versions_sha256": hashlib.sha256(json.dumps(versions, sort_keys=True).encode()).hexdigest(),
        "parameter_gradients_absent": all(p.grad is None for p in model.parameters()),
        "hook_counts": [len(layer._forward_hooks) for layer in model.model.layers],
    }


def numerical_runtime() -> dict:
    return {
        "torch_build": torch.__config__.show(), "parallel_info": torch.__config__.parallel_info(),
        "threads": torch.get_num_threads(), "interop_threads": torch.get_num_interop_threads(),
        "deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
        "deterministic_warn_only": torch.is_deterministic_algorithms_warn_only_enabled(),
        "float32_matmul_precision": torch.get_float32_matmul_precision(),
        "mkldnn_enabled": torch.backends.mkldnn.enabled,
        "environment_controls": {name: os.environ.get(name) for name in
                                 ("MKL_NUM_THREADS", "MKL_DYNAMIC", "MKL_CBWR", "OMP_NUM_THREADS",
                                  "OMP_DYNAMIC", "CUBLAS_WORKSPACE_CONFIG")},
    }


def comparison_failure(left: torch.Tensor, right: torch.Tensor, *, atol: float, rtol: float) -> dict:
    """Save both hashes and up to eight actual failing values, not full logit arrays.

    Run only AFTER a failed comparison. Evidence gathering never changes the
    acceptance tolerance, repeats inference, or replaces the original failure.
    """
    if left.shape != right.shape:
        raise ValueError("Comparison failure evidence requires matching tensor shapes")
    left_cpu, right_cpu = left.detach().cpu(), right.detach().cpu()
    mismatch = (~torch.isclose(left, right, atol=atol, rtol=rtol)).detach().cpu()
    count = int(mismatch.sum())
    diff = (left_cpu.double() - right_cpu.double()).abs()
    ranked = torch.nan_to_num(diff, nan=float("inf")).masked_fill(~mismatch, -1).reshape(-1)
    indices = ranked.topk(min(8, count)).indices.tolist()

    def scalar(value):
        number = float(value)
        return number if math.isfinite(number) else str(number)

    samples = []
    for index in indices:
        remaining, coordinates = index, []
        for size in reversed(left.shape):
            coordinates.append(remaining % size)
            remaining //= size
        samples.append({"index": list(reversed(coordinates)),
                        "left": scalar(left_cpu.reshape(-1)[index]),
                        "right": scalar(right_cpu.reshape(-1)[index]),
                        "abs_error": scalar(diff.reshape(-1)[index])})
    return {"shape": list(left.shape), "left_dtype": str(left.dtype), "right_dtype": str(right.dtype),
            "left_device": str(left.device), "right_device": str(right.device),
            "left_sha256": tensor_sha256(left), "right_sha256": tensor_sha256(right),
            "mismatch_count": count, "sample_limit": 8, "largest_failing_values": samples,
            "full_tensors_retained": False}
