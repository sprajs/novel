"""Strict execution profiles: capacity is a budget, never a GPU marketing name."""

from dataclasses import asdict, dataclass
import importlib.metadata
from pathlib import Path
import platform
import re
import tomllib
import os
import shutil
import subprocess

import torch

GIB = 1024**3
PROFILE_NAMES = ("cloud-cpu", "local-2080ti", "rental")
MODEL_KEYS = ("qwen3_0_6b", "qwen3_1_7b", "qwen3_8b")


class ProfileError(ValueError):
    """A requested execution condition cannot be met; never fall back to CPU."""


@dataclass(frozen=True)
class ProfileRequest:
    profile: str = "cloud-cpu"
    model: str | None = None
    device_index: int = 0
    dtype: str | None = None
    rental_capacity_gib: int = 32
    max_input_tokens: int = 128
    max_new_tokens: int = 8
    batch_size: int = 1
    attention_backend: str = "eager"
    quantization: str | None = None
    gradient: bool = False

    def __post_init__(self):
        if self.profile not in PROFILE_NAMES:
            raise ProfileError(f"Choose a profile from {PROFILE_NAMES}")
        if self.model is not None and self.model not in MODEL_KEYS:
            raise ProfileError("Only immutable, licensed registry models are enabled")
        if self.model == "qwen3_8b" and self.profile != "rental":
            raise ProfileError("The 8B candidate is enabled only for rental; CPU/2080 Ti models are unchanged")
        for name, lo, hi in (("device_index", 0, 63), ("max_input_tokens", 1, 256),
                             ("max_new_tokens", 1, 16), ("batch_size", 1, 1)):
            value = getattr(self, name)
            if type(value) is not int or not lo <= value <= hi:
                raise ProfileError(f"{name} must be an integer in [{lo}, {hi}]")
        if type(self.rental_capacity_gib) is not int or self.rental_capacity_gib not in (24, 32):
            raise ProfileError("Rental capacity must be an explicit 24 or 32 GiB budget")
        if self.profile != "rental" and self.rental_capacity_gib != 32:
            raise ProfileError("The custom capacity override applies only to rental")
        if self.dtype not in (None, "float32", "float16", "bfloat16"):
            raise ProfileError("Unknown precision")
        if self.attention_backend != "eager" or self.quantization is not None:
            raise ProfileError("Canonical instrumentation requires eager, unquantized weights")
        if type(self.gradient) is not bool:
            raise ProfileError("gradient must be boolean")
        if self.profile == "cloud-cpu" and self.device_index != 0:
            raise ProfileError("A CUDA device index is not meaningful for cloud-cpu")

    @property
    def model_key(self):
        if self.model is not None:
            return self.model
        if self.profile == "cloud-cpu":
            return "qwen3_0_6b"
        if self.profile == "rental" and self.rental_capacity_gib == 32:
            return "qwen3_8b"
        return "qwen3_1_7b"


def configure_determinism() -> dict:
    """Call before CUDA discovery/context creation. These are process-local settings."""
    value = os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
    if value not in (":4096:8", ":16:8"):
        raise ProfileError("Set CUBLAS_WORKSPACE_CONFIG=:4096:8 before starting Python")
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    return {"deterministic_algorithms": True, "cublas_workspace_config": value,
            "matmul_tf32": False, "cudnn_tf32": False, "cudnn_benchmark": False}


def inspect_hardware(device_index: int = 0) -> dict:
    """Read actual CUDA visibility; nvidia-smi is supplementary, never a fallback."""
    result = {"torch_version": str(torch.__version__), "cuda_build": torch.version.cuda,
              "cuda_available": bool(torch.cuda.is_available()), "device_count": torch.cuda.device_count(),
              "device_index": device_index, "nvidia_smi": None, "discovery_error": None}
    command = shutil.which("nvidia-smi")
    if command:
        try:
            proc = subprocess.run([command, "--query-gpu=index,name,driver_version,memory.total,memory.free",
                                   "--format=csv,noheader,nounits"], capture_output=True, text=True,
                                  timeout=10, check=False)
            result["nvidia_smi"] = {"returncode": proc.returncode, "rows": proc.stdout.strip().splitlines()}
        except (OSError, subprocess.TimeoutExpired) as exc:
            result["nvidia_smi"] = {"error": type(exc).__name__}
    if result["cuda_available"] and device_index < result["device_count"]:
        try:
            with torch.cuda.device(device_index):
                prop = torch.cuda.get_device_properties(device_index)
                free, total = torch.cuda.mem_get_info(device_index)
                result.update(name=prop.name, capability=list(torch.cuda.get_device_capability(device_index)),
                              total_bytes=total, free_bytes=free, arch_list=torch.cuda.get_arch_list(),
                              native_bf16=torch.cuda.is_bf16_supported(including_emulation=False))
        except (RuntimeError, AssertionError) as exc:
            result["discovery_error"] = str(exc)
    return result


def memory_estimate(entry: dict, request: ProfileRequest, dtype: str) -> dict:
    """Conservative planning envelope, NOT a measured fit or rigorous upper bound."""
    cfg = entry["model_config"]
    width = 4 if dtype == "float32" else 2
    tokens = request.max_input_tokens + max(request.max_new_tokens, 8)
    weights = entry["parameters"]["unique_config_implied"] * width
    kv = 2 * cfg["num_hidden_layers"] * cfg["num_key_value_heads"] * cfg["head_dim"] * tokens * width
    # Runner retains several full-logit comparisons; attention softmax may use FP32.
    logits = 6 * tokens * cfg["vocab_size"] * 4
    attention = 4 * cfg["num_attention_heads"] * tokens**2 * 4
    activations = 12 * tokens * (cfg["hidden_size"] + cfg["intermediate_size"]) * width
    backward = (activations + attention) * cfg["num_hidden_layers"] if request.gradient else 0
    reserve = (4 if request.gradient else 2) * GIB
    return {"weight_bytes": weights, "kv_cache_bytes": kv, "live_logits_allowance_bytes": logits,
            "attention_workspace_estimate_bytes": attention, "activation_estimate_bytes": activations,
            "backward_activation_estimate_bytes": backward, "runtime_reserve_bytes": reserve,
            "planning_bytes": weights + kv + logits + attention + activations + backward + reserve,
            "parameter_gradient_bytes": 0, "optimizer_bytes": 0,
            "note": "Estimate only; includes KV parity although canonical forwards disable cache. Actual peaks and fit require this exact device/run."}


@dataclass(frozen=True)
class ResolvedProfile:
    request: ProfileRequest
    device: str
    dtype: str
    stack: str
    lock_path: str
    capacity_budget_bytes: int | None
    allocator_limit_bytes: int | None
    estimate: dict
    hardware: dict

    def to_dict(self):
        result = asdict(self)
        if self.request.profile == "rental":
            result["capacity_policy"] = {
                "target": "RTX 5090, advertised 32 GB" if self.request.rental_capacity_gib == 32 else "explicit custom 24 GiB ceiling",
                "requested_ceiling_gib": self.request.rental_capacity_gib,
                "detected_total_gib": self.hardware["total_bytes"] / GIB,
                "detected_free_gib": self.hardware["free_bytes"] / GIB,
                "allocator_fraction_of_available_budget": 0.8,
                "note": "GB product label is not converted to usable GiB. Budget is clamped to measured CUDA bytes; runtime headroom remains reserved.",
            }
        return result


def resolve_profile(request: ProfileRequest, hardware: dict, entry: dict) -> ResolvedProfile:
    dtype = request.dtype or ("float32" if request.profile == "cloud-cpu" else "float16")
    capacity = limit = None
    if request.profile == "cloud-cpu":
        if dtype != "float32":
            raise ProfileError("cloud-cpu preserves the FP32 reference condition")
        if hardware["torch_version"] != "2.8.0+cpu":
            raise ProfileError("cloud-cpu requires torch 2.8.0+cpu: use uv run --locked from the repository root")
        device, stack, lock = "cpu", "cpu", "uv.lock"
    else:
        if not hardware["cuda_available"] or not hardware["cuda_build"]:
            raise ProfileError("CUDA requested but unavailable. Use the separate cu126/cu128 environment, check driver and GPU visibility; no CPU fallback")
        if request.device_index >= hardware["device_count"] or hardware.get("discovery_error"):
            raise ProfileError("Cannot inspect the selected CUDA device; check --device-index and driver/runtime visibility")
        capability = tuple(hardware["capability"])
        if capability not in ((7, 5), (8, 0), (8, 6), (8, 9), (9, 0), (12, 0)):
            raise ProfileError(f"Unvalidated architecture {capability}; this profile needs a separately validated wheel")
        if request.profile == "local-2080ti" and (capability != (7, 5) or "2080 ti" not in hardware["name"].lower()):
            raise ProfileError("local-2080ti requires a detected RTX 2080 Ti (SM75)")
        if capability == (7, 5) and dtype != "float16":
            raise ProfileError("Turing canonical execution requires explicit FP16; BF16 emulation is not accepted")
        if dtype == "bfloat16" and not hardware["native_bf16"]:
            raise ProfileError("BF16 requires native support, not emulation; use float16")
        stack = "cu128" if capability == (12, 0) else "cu126"
        runtime = "12.8" if stack == "cu128" else "12.6"
        if hardware["torch_version"] != f"2.8.0+{stack}" or hardware["cuda_build"] != runtime:
            raise ProfileError(f"Detected SM{capability[0]}{capability[1]} requires this reference's torch 2.8.0+{stack}; run uv sync --locked --project environments/{stack}")
        arch = f"sm_{capability[0]}{capability[1]}"
        if not any(candidate.startswith(f"sm_{capability[0]}") and candidate[3:].isdigit()
                   and int(candidate[3:]) <= capability[0] * 10 + capability[1]
                   for candidate in hardware["arch_list"]):
            raise ProfileError(f"Installed wheel lacks a compatible native cubin for {arch}; install environments/{stack}. PTX JIT is not silently substituted")
        ceiling = (11 if request.profile == "local-2080ti" else request.rental_capacity_gib) * GIB
        # Preserve the local guard. For rental, distinguish the advertised GB
        # class from the GiB ceiling and actually detected CUDA-usable bytes.
        minimum = ceiling * 0.95 if request.profile == "local-2080ti" else request.rental_capacity_gib * 10**9 * 0.95
        if hardware["total_bytes"] < minimum:
            raise ProfileError("Detected VRAM is below the requested capacity budget; choose the matching profile/capacity")
        if request.profile == "rental" and request.rental_capacity_gib == 32:
            if capability != (12, 0) or not re.search(r"\brtx\s*5090\b", hardware["name"], re.IGNORECASE):
                raise ProfileError("Default rental requires a detected RTX 5090 (SM120, 32 GB class); use --rental-capacity-gib 24 only for an explicit custom rental")
        capacity = ceiling if request.profile == "local-2080ti" else min(ceiling, hardware["total_bytes"])
        if not 0 < hardware["free_bytes"] <= hardware["total_bytes"]:
            raise ProfileError("Invalid or exhausted free VRAM; close other GPU jobs and retry")
        limit = int(min(capacity, hardware["free_bytes"]) * 0.80)
        device, lock = f"cuda:{request.device_index}", f"environments/{stack}/uv.lock"
    estimate = memory_estimate(entry, request, dtype)
    if limit is not None and estimate["planning_bytes"] > limit:
        raise ProfileError(f"Estimated {estimate['planning_bytes'] / GIB:.2f} GiB exceeds the 80%-of-free/capacity budget {limit / GIB:.2f} GiB. Use --model qwen3_0_6b, shorter --max-input-tokens, omit --gradient, or release other GPU allocations; fit is not guaranteed")
    return ResolvedProfile(request, device, dtype, stack, lock, capacity, limit, estimate, hardware)


def validate_environment(profile: ResolvedProfile) -> dict:
    """Verify the selected lock against installed distributions, not just its hash."""
    if platform.python_version() != "3.12.14" or platform.system() != "Linux" or platform.machine() != "x86_64":
        raise ProfileError("These locks target Linux x86-64 and Python 3.12.14; use the documented isolated environment")
    lock = tomllib.loads(Path(profile.lock_path).read_text())
    observed, mismatches = {}, []
    for package in lock["package"]:
        if "virtual" in package.get("source", {}):
            continue
        name, expected = package["name"], package["version"]
        try:
            actual = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            actual = None
        observed[name] = {"expected": expected, "installed": actual}
        if actual != expected:
            mismatches.append(f"{name}: expected {expected}, found {actual}")
    if mismatches:
        raise ProfileError("Installed distributions differ from the selected lock: " + "; ".join(mismatches)
                           + ". Use uv sync --locked in the selected project; do not mix environments")
    return observed


def initialize_device(profile: ResolvedProfile) -> dict:
    """Execute real kernels before loading weights; an incompatible driver fails here."""
    if profile.device == "cpu":
        return {"status": "SKIP", "reason": "CPU profile; no CUDA kernel executed"}
    device = torch.device(profile.device)
    try:
        torch.cuda.set_per_process_memory_fraction(profile.allocator_limit_bytes / profile.hardware["total_bytes"], device)
        with torch.cuda.device(device), torch.no_grad():
            value = torch.ones((32, 32), device=device, dtype=getattr(torch, profile.dtype))
            product = value @ value
            torch.cuda.synchronize(device)
            if not bool(torch.isfinite(product).all()) or not bool((product == 32).all()):
                raise ProfileError("CUDA matrix kernel produced invalid values")
        del value, product
        torch.cuda.reset_peak_memory_stats(device)
    except RuntimeError as exc:
        if isinstance(exc, torch.OutOfMemoryError) or "out of memory" in str(exc).lower():
            raise
        raise ProfileError(f"CUDA kernel/driver/runtime check failed: {exc}. Verify the NVIDIA host driver supports the pinned {profile.stack} runtime; no system changes were made") from exc
    return {"status": "PASS", "operation": "native device allocation and dtype-specific matrix multiply"}


def synchronize(device: str):
    if device.startswith("cuda:"):
        torch.cuda.synchronize(torch.device(device))


def memory_record(device: str) -> dict:
    if device == "cpu":
        return {"status": "SKIP", "reason": "CPU profile", "peak_allocated_bytes": None, "peak_reserved_bytes": None}
    free, total = torch.cuda.mem_get_info(torch.device(device))
    return {"status": "PASS", "peak_allocated_bytes": torch.cuda.max_memory_allocated(device),
            "peak_reserved_bytes": torch.cuda.max_memory_reserved(device),
            "free_bytes_after": free, "total_bytes": total}


def failure_record(exc: Exception) -> dict:
    oom = isinstance(exc, torch.OutOfMemoryError) or (isinstance(exc, RuntimeError) and "out of memory" in str(exc).lower())
    return {"status": "FAIL", "type": type(exc).__name__, "message": str(exc), "out_of_memory": oom,
            "next_action": ("No automatic retry or CPU fallback. Use qwen3_0_6b, reduce token caps, omit --gradient, release other jobs, then rerun into a new report." if oom
                            else "Correct the reported condition and rerun; skipped checks do not establish GPU support.")}
