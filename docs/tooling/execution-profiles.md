# Three reproducible execution modes

Verified official sources on 11 October 2026. This increment implements GPU code;
**no GPU was available in the cloud and no CUDA execution or GPU benchmark was
performed here**. CPU/static/mocked results are in [validation](../validation.md).
The original CPU `pyproject.toml`, `uv.lock`, two model entries and dataset handoff
are preserved. The registry adds an immutable Qwen3-8B rental candidate. There is
no rental, driver installer or machine-security change.

| Mode / CLI profile | Default model | Canonical precision/backend | Dependency environment |
| --- | --- | --- | --- |
| Small cloud CPU / `cloud-cpu` | Pinned Qwen3-0.6B | FP32, eager | Root CPU lock, torch 2.8.0+cpu |
| Local 11 GB / `local-2080ti` | Pinned Qwen3-1.7B; first validate 0.6B | FP16, eager | `environments/cu126`, torch 2.8.0+cu126 |
| RTX 5090 32 GB / `rental` | Pinned Qwen3-8B; first validate 0.6B | FP16, eager; explicit native BF16 is a separate condition | `environments/cu128`, torch 2.8.0+cu128 |

[NVIDIA specifies 11 GB for RTX 2080 Ti](https://www.nvidia.com/en-us/geforce/graphics-cards/compare/?section=compare-20),
[24 GB for RTX 3090](https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3090-3090ti/),
[24 GB for RTX 4090](https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4090/),
and **[32 GB GDDR7 for RTX 5090](https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/)**.
The verified product is RTX 5090; this design does not assume a “5090 Ti.”
The rental default targets the **full RTX 5090 32 GB**, requiring its detected
name, SM120 architecture and capacity class. The default 32 GiB binary ceiling
is clamped to CUDA's actual total bytes; the product's GB label is not assumed
to equal 32 GiB. For example, 32,000,000,000 detected bytes means 29.80 GiB,
whereas 32 × 2^30 bytes means 32 GiB. Both retain the normal 20% allocator
headroom against available memory. Reports separate the product target,
requested ceiling, detected total/free bytes and effective allocation limit.
The nominal-class guard allows a small amount of device-reserved memory; it
does not use a provider label as proof of hardware or fit.

`--rental-capacity-gib 24` is an explicit optional custom rental for supported
3090/4090 or other supported architectures. Its default model remains 1.7B and
its ceiling is 24 GiB. It does not set the primary RTX 5090 recommendation.

## Compatible isolated dependencies

All three environments pin Python 3.12.14, uv 0.12.23, Transformers 4.57.6,
Hugging Face Hub 0.36.2, SafeTensors 0.8.0 and NumPy 2.5.4. Each CUDA environment
has a complete separate `uv.lock` with transitive CUDA libraries and hashes.
They are virtual dependency projects; scripts import this checkout's `src/`
without installing the root package's CPU dependency into the CUDA environment.
Always invoke commands from the repository root. Linux x86-64 is the locked
target (including a suitable Linux/WSL2 GPU environment); native Windows/macOS
are not claimed to be validated. CUDA wheels require glibc 2.28 or later.

The [official PyTorch installation archive](https://pytorch.org/get-started/previous-versions/)
lists both 2.8.0 cu126 and cu128; the [cu126](https://download.pytorch.org/whl/cu126/torch/)
and [cu128](https://download.pytorch.org/whl/cu128/torch/) indexes contain Python
3.12 Linux wheels. The immutable [2.8.0 wheel build script](https://github.com/pytorch/pytorch/blob/v2.8.0/.ci/manywheel/build_cuda.sh)
includes SM75 and SM86 in cu126, and SM120 in cu128. See
[NVIDIA's capability table](https://developer.nvidia.com/cuda/gpus): 2080 Ti is
7.5/Turing, 3090 is 8.6/Ampere, 4090 is 8.9/Ada, 5090 is 12.0/Blackwell.
Literal `sm_89` need not appear: [Ada can execute SM86 cubins](https://docs.nvidia.com/cuda/ada-compatibility-guide/index.html).
The guard requires a compatible same-major cubin with equal/lower minor
capability. It does not silently rely on PTX JIT. cu126 is rejected for SM120.

The environments are deliberately distinct even though cu128 also includes
SM75. This avoids extending the local machine's runtime requirements just to
support Blackwell. No latest-default CUDA13 dependency is substituted.
Conservative Linux driver reference points are 560.28.03 for CUDA12.6 and
570.86.16 or a newer driver supporting the RTX5090. These are supported historical
reference points, not a claim about the oldest usable minor-compatible driver.
See [NVIDIA CUDA release tables](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-toolkit-release-notes/index.html)
and [570.86.16's supported products](https://download.nvidia.com/XFree86/Linux-x86_64/570.86.16/README/supportedchips.html).
A local CUDA toolkit is unnecessary for these wheels. Driver upgrades belong to
the machine owner/provider; this repository never installs or modifies drivers.

## Commands to run

Set the writable cache in each shell. Installation is explicit and separate
from the smoke. CUDA environment installation downloads substantial wheel
payloads; allow several GB of disk beyond model snapshots. No CUDA wheel payloads
were installed in this CPU-only cloud merely to claim GPU validation.

```bash
export UV_CACHE_DIR="$PWD/.cache/uv"

# Cloud CPU, preserving PR1's lock and bounded 0.6B download (about 1.52 GB).
uv sync --locked
uv run --locked novel-model download
uv run --locked python scripts/profile_smoke.py --profile cloud-cpu --gradient

# Local RTX 2080 Ti.
uv sync --locked --project environments/cu126
uv run --locked --project environments/cu126 python scripts/profile_smoke.py \
  --profile local-2080ti --preflight-only
PYTHONPATH=src uv run --locked --project environments/cu126 python -m novel.models download
uv run --locked --project environments/cu126 python scripts/profile_smoke.py \
  --profile local-2080ti --model qwen3_0_6b

# RTX 5090: the separate Blackwell environment, full detected 32 GB class.
uv sync --locked --project environments/cu128
uv run --locked --project environments/cu128 python scripts/profile_smoke.py \
  --profile rental --preflight-only
PYTHONPATH=src uv run --locked --project environments/cu128 python -m novel.models download
uv run --locked --project environments/cu128 python scripts/profile_smoke.py \
  --profile rental --model qwen3_0_6b
```

After the first 0.6B forward smoke passes, run its optional gradient check and
then the larger primary candidate. The 2080 Ti remains on 1.7B; RTX 5090 now
defaults to 8B. A download happens only when explicitly requested:

```bash
uv run --locked --project environments/cu126 python scripts/profile_smoke.py \
  --profile local-2080ti --model qwen3_0_6b --gradient
PYTHONPATH=src uv run --locked --project environments/cu126 python -m novel.models \
  download --model qwen3_1_7b --max-bytes 5368709120
uv run --locked --project environments/cu126 python scripts/profile_smoke.py \
  --profile local-2080ti

# RTX 5090: 0.6B gradient mechanics, then the 8B default forward candidate.
uv run --locked --project environments/cu128 python scripts/profile_smoke.py \
  --profile rental --model qwen3_0_6b --gradient
PYTHONPATH=src uv run --locked --project environments/cu128 python -m novel.models \
  download --model qwen3_8b --max-bytes 19327352832
uv run --locked --project environments/cu128 python scripts/profile_smoke.py \
  --profile rental
# Optional selected-activation gradient after the 8B forward report passes.
uv run --locked --project environments/cu128 python scripts/profile_smoke.py \
  --profile rental --gradient

# Optional tiny random-model GPU regression; downloads no weights.
NOVEL_RUN_GPU_TESTS=1 NOVEL_GPU_PROFILE=local-2080ti PYTHONPATH=src \
  uv run --locked --project environments/cu126 python -m pytest -q -m gpu
```

For the last command on an RTX 5090, use `NOVEL_GPU_PROFILE=rental` and
`--project environments/cu128`. That opt-in test uses the primary 32 GB rental;
custom 24 GiB rentals use the smoke CLI's explicit capacity option instead.
`NOVEL_GPU_DEVICE_INDEX` selects a device for that test; `--device-index`
selects a logical CUDA device for the smoke (respecting CUDA_VISIBLE_DEVICES).
The 1.7B snapshot is about 4.08 GB; its explicit 5 GiB cap is a download budget.
The 8B snapshot is 16,397,459,696 bytes (16.40 GB / 15.27 GiB), with an explicit
18 GiB download cap above. These caps are disk/download budgets, not VRAM.
Provision host RAM for approximately 15.26 GiB of 8B FP16 weights plus loading,
conversion and process overhead; at least 32 GiB host RAM is a planning starting
point, not a measured guarantee. Only 0.6B weights were downloaded in this cloud;
8B research fetched bounded metadata/tokenizer files and no weight payloads.
Model loading is always local, hash verified, SafeTensors only, and
`trust_remote_code=False`.

For an explicit custom 24 GB 3090/4090 rental, install `environments/cu126`, use
`--profile rental --rental-capacity-gib 24`, and start with `--model qwen3_0_6b`.
After mechanics checks and the explicit 1.7B download above, omitting `--model`
selects 1.7B for this custom condition. A 5090 explicitly capped at 24 GiB still
requires cu128. Hardware detection selects the required wheel; a mismatch fails.

The CLI defaults to batch one, input cap 128, eight generated tokens, one layer
and one selected position. Its maximum input/generation caps are 256/16; use
`--max-input-tokens 64` for a stricter envelope or a smaller model if capacity
fails. It rejects oversized prompts rather than truncating them. `--config`
accepts the existing strict mechanics config for prompt/seeds/layer/artifact
budget; the selected profile overrides model/device/precision/token caps and
records both source and effective config hashes. `ProfileRequest` is the typed
programmatic config. No ground-truth records or confirmation splits are opened.

## What the report means

The [open CPU repeatability investigation](../validation/cpu-repeatability-investigation.md)
limits stability claims even when an individual smoke passes. Before forwards,
`execution.json` now preserves exact input and runtime context; failed comparisons
retain bounded raw differing values and tensor hashes.

Every valid invocation prints the unique path to
`runs/profile-checks/<id>/diagnostics.json`, including execution failures.
Exit 0 means the requested checks passed; exit 1 means failure. `--preflight-only`
reports model checks as **SKIP**, even if CUDA matrix multiplication passed.
A requested GPU with no usable CUDA is **FAIL**, with downstream checks **SKIP**;
it never runs CPU as a substitute. Argument syntax/bounds errors exit 2 before
execution. The report includes:

- Actual GPU name, logical index, capability, total/free VRAM, CUDA build,
  wheel architectures and supplementary driver rows from `nvidia-smi` when
  available. An actual allocation/matrix multiplication/synchronization checks
  the runtime/driver path before weights load.
- Exact installed-versus-locked distributions, source and selected lock hashes,
  model/tokenizer revisions, license, dtype, eager backend, unquantized state,
  capacity budget and the explicit memory estimate.
- Exact clean-forward repeatability, selected capture, exact no-op/zero-strength invariants, earlier-prefix checks,
  three forced cache steps, seeded raw-token repeatability and hook cleanup.
- Optional finite/nonzero activation gradient with frozen/unmodified weights;
  finite-difference validation is explicitly SKIP for the pretrained GPU run.
  Tiny FP32 finite-difference mechanics are tested separately offline.
- Synchronized load/generation/gradient timings, peak allocated and reserved
  CUDA bytes, host peak RSS, and raw token/output/provenance artifact paths.

Share the diagnostic JSON and, if appropriate, the corresponding bounded run
folder (contains your prompt/raw generations). It records hardware/software,
public experiment inputs and an explicit allowlist of numerical thread/CUBLAS
controls; it does not dump arbitrary environment variables, credentials or home paths.
No automatic upload occurs. Ignored run folders and model weights stay out of Git.

The allocator cap is 80% of `min(free VRAM at preflight, effective capacity)`;
the rental effective capacity is `min(detected total bytes, requested GiB ceiling)`.
The planning envelope must fit below that cap before loading. Other processes
can allocate later; CUDA contexts, external allocations and fragmentation are
not a mathematical fit guarantee. OOM produces FAIL and guidance to shorten the
input, use 0.6B, omit gradients or release competing allocations. No silent dtype,
quantization, CPU offload or automatic lower-memory retry changes the condition.
Host RAM must also accommodate CPU loading before transfer; check the measured
RSS and available host RAM, especially for larger snapshots.

FP16/BF16 cache/prefix tolerances are **prospective guardrails**, recorded with
actual maximum errors. No-op comparisons require exact equality. A failed
numerical check must be investigated/calibrated before causal work; this code
does not widen tolerance automatically or promise matching samples across
hardware/dtypes. CUDA determinism settings and private sampling RNG are recorded;
TF32 is disabled, cuDNN benchmarking is off, and CUBLAS_WORKSPACE_CONFIG is set
before CUDA discovery.

## Scientific scope and optional speed work

See [model suitability](../models/hardware-suitability.md). The original selected
snapshot dates, licenses and undocumented training cutoffs are unchanged.
A local final-token logit contrast gradient is a mechanics check, not a bridge
direction or proof of selective transfer. Parameter gradients/optimizer state
remain absent; backward intermediates still require memory. A tiny token cap
may end before an answer; that is not a reasoning failure.
The default layer remains the explicitly configured layer 14, now within 36
decoder blocks for 8B; this is a mechanics site, not a model-relative causal claim.

Canonical instrumentation is eager, uncompiled, unquantized and uses full-prefix
recomputation. The existing `generate_reference(..., use_cache=True)` is an
optional **clean-only** generation path; it rejects interventions. It is not a
new backend or a throughput benchmark. Quantization/llama.cpp/vLLM comparisons
remain optional separate numerical treatments with their own conversion pins,
locks and tokenizer/logit checks. BF16 (`--dtype bfloat16` on a supported rental)
also changes the numerical condition. On Turing the code requires FP16 and
explicitly rejects BF16 emulation; [PyTorch's native BF16 probe](https://github.com/pytorch/pytorch/blob/v2.8.0/torch/cuda/__init__.py)
is called with `including_emulation=False`.
