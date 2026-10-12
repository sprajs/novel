# Local RTX 2080 Ti installation and validation

Executed on 12 October 2026 on the user's Omarchy workstation. PRs #1–#4 were
already merged. PR #5 was reviewed, passed the full locked CPU suite (306 tests,
118 subtests, two skips), merged as `c207e17c9dad9696ea947f82a83a9c7c7240b9bd`,
and pulled with `--ff-only`. No existing open PR remained.

## Installed local paths

- `environments/cu126/.venv`: exact existing Python 3.12.14 / PyTorch
  2.8.0+cu126 / Transformers 4.57.6 lock. Root CPU, fast-build and fast-convert
  locks were also installed separately. The 5090/cu128 reference was not installed.
- `.cache/toolchains/cuda128`: NVCC 12.8.93, CUDA runtime 12.8.90,
  cuBLAS 12.8.4.1, GCC/G++ 13.4.0 and glibc 2.28 compiler sysroot.
  This keeps CUDA compilation independent of the host's unsupported GCC 16.
  Toolchain packages, versions, URLs and hashes are retained in
  `.cache/toolchains/cuda128-explicit.txt`; installation log and the NVIDIA
  12.8.1 redistributable manifest are alongside it.
- `.cache/models`: immutable, complete, SHA-256 verified registry snapshots for
  Qwen3-0.6B (`c1899de289a04d12100db370d81485cdf75e47ca`) and Qwen3-1.7B
  (`70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`). Both have local F16 GGUF
  conversions with source hashes and conversion receipts under `.cache/gguf`.
- `.cache/llama.cpp`: clean stable-tag checkout at
  `d81235049384534c167caea52b85a694f6103d14`.

Installation used `uv tool run --from uv==0.12.23 uv sync --locked` with the
appropriate `--project` argument, preserving the system's existing uv 0.12.5.
The local compiler environment was installed with micromamba 2.9.0 using
conda-forge/NVIDIA channels and these explicit requirements:

```text
cuda-nvcc=12.8.93 cuda-cudart-dev=12.8.90 libcublas-dev=12.8.4.1
gxx_linux-64=13 sysroot_linux-64=2.28
```

The [NVIDIA redistributable manifest](https://developer.download.nvidia.com/compute/cuda/redist/redistrib_12.8.1.json)
identifies NVCC 12.8.93; its release-notes table lists 12.8.90. The build script
now allows an explicit `--nvcc-version 12.8.93`, retains the original default,
and checks both new and reused builds against the requested compiler version.
Receipts record the actual selected C++ compiler rather than the ambient `c++`.

## Driver and voice service

The loaded NVIDIA module is **615.71.09**, while installed nvidia-utils and the
on-disk DKMS module are **615.78.08**. System `nvidia-smi` initially failed with
`Driver/library version mismatch`. DKMS reports the new module installed for
both the running Omarchy kernel and the installed Arch kernel.

Matching compute libraries and `nvidia-smi` were extracted from the existing
cached `nvidia-utils-615.71.09-1-x86_64.pkg.tar.zst` into
`.cache/host/nvidia-615.71.09/usr`. Its package hash is retained in
`.cache/host/package-sha256.txt`. No system driver, desktop service or boot
configuration was replaced. An eventual reboot is needed to use the updated
on-disk driver consistently; the machine was not rebooted during this work.

`scripts/local_gpu.py` first tests normal system access. When that fails, it
selects only an already provisioned library directory matching the **loaded**
module, verifies it with `nvidia-smi`, and applies it to the requested process.
It prefers working system libraries after a reboot and does not force the old
version. `--toolchain` additionally selects the local CUDA/GCC compiler tools.
There is no global `LD_LIBRARY_PATH`, shell configuration or driver downgrade.

Voxtype's `parakeet-tdt-0.6b-v3` daemon and its OSD child were stopped with
`systemctl --user disable --now voxtype.service`. The service is inactive and
its graphical-session startup link was removed. No socket/timer activation was
found. Keep it manual:

```bash
systemctl --user start voxtype.service  # when dictation is wanted
systemctl --user stop voxtype.service   # release it again
```

The voice model is no longer resident. The initial driver mismatch prevented
measuring its prior VRAM usage, so no reclaimed-VRAM amount is claimed. The
window manager and browsers continue to use GPU memory for the desktop.

## PyTorch results

CUDA discovery, native FP16 matrix multiplication and the explicitly enabled
GPU unit test pass. Hardware is an RTX 2080 Ti, SM75, with about 10.58 GiB
CUDA-reported usable total memory; the cu126 wheel includes `sm_75`.

The full pretrained profile **fails**, with unchanged prospective tolerances:

| Condition | Result |
| --- | --- |
| 0.6B FP16, gradient requested | Preflight/kernel pass; first cached/full-prefix comparison fails, max logit error 0.0390625; downstream gradient/generation skipped |
| 1.7B FP16, gradient requested | Rejected by planning guard: 8.53 GiB estimate versus 7.31 GiB allowed at that moment; no weights loaded |
| 1.7B FP16, no gradient | Preflight/kernel pass; first cache comparison fails, max error 0.0625 |

A separately declared 20-input-token / one-output-token 1.7B gradient preflight
also failed its planning guard (7.46 GiB versus 7.40 GiB available budget),
without loading weights. No guard was bypassed.

All original diagnostics and replay records are retained under
`runs/local-gpu-20261012/profile-checks/` and its sibling run folders. There was
no threshold widening or retry into a claimed full-profile pass.

A separate diagnostic, [local-gpu-cache-probe.py](local-gpu-cache-probe.py),
compared reduced-precision FP16 GEMM reductions enabled/disabled. Both conditions
retained exact clean repeats but had the same three cache maximum errors:
0.0390625, 0.033203125 and 0.1875. Turning that flag off did not resolve the
failure; canonical defaults were left intact. Both produced finite nonzero
0.6B activation gradients. This does not identify a root cause or qualify the
cache path. [PyTorch's numerical-accuracy documentation](https://docs.pytorch.org/docs/2.8/notes/numerical_accuracy.html)
describes shape-dependent floating-point differences and the reduction flag;
it does not establish that the observed errors are acceptable.

The separate [uncached operational probe](local-gpu-operational-probe.py)
passes on both pretrained models: exact clean repeats, exact capture/no-op
logits, finite residuals, a nonzero patch changing logits, repeated eight-token
greedy generation, frozen weights, absent parameter gradients, and hook cleanup.
The 0.6B selected-activation gradient is finite/nonzero (L2 1.76089).
The 1.7B gradient remains skipped following its planning rejection.

Peak PyTorch allocations were 1,292,124,160 bytes for 0.6B and 3,542,241,280 bytes
for 1.7B in this short operational workload. These exclude context/external
allocations and do not override the full-profile planning guard. Raw IDs,
selected residuals, gradient tensors, source hashes and measurements are in
`runs/local-gpu-20261012/operational/`. The probes cover engineering mechanics,
not scientific effect calibration or historical reconstruction.

Run from the repository root (output folders are exclusive; use a fresh name):

```bash
PYTHONPATH=src NOVEL_RUN_GPU_TESTS=1 python scripts/local_gpu.py -- \
  environments/cu126/.venv/bin/python -m pytest -q tests/test_generation.py -m gpu

PYTHONPATH=src python scripts/local_gpu.py -- \
  environments/cu126/.venv/bin/python docs/validation/local-gpu-operational-probe.py \
  --output runs/local-gpu-operational-new

python scripts/local_gpu.py -- environments/cu126/.venv/bin/python \
  scripts/profile_smoke.py --profile local-2080ti --model qwen3_0_6b --gradient
```

The last command still fails its cache guard. The operational probe is deliberately
reported separately and does not turn the full profile green.

## Native GPU results

The stable native server, benchmark and quantizer were built for SM75 using the
pinned build environment. The first attempt compiled successfully but failed
at executable linking: the isolated sysroot linker could not locate indirect
CUDA/OpenMP dependencies. Its full log is preserved as
`.cache/fast/local-2080ti/recipe-build.initial-link-failure.log`.
An explicit `--link-library-dir .cache/toolchains/cuda128/lib` supplies the
linker's `-rpath-link` search path. Reconfiguration reused the compiled objects
and completed all three targets. The successful recipe, CMake cache, binary
hashes, selected compiler and `ldd` output are in the build receipt. Reuse with
12.8.93 passes verification; requesting 12.8.90 against that receipt is rejected.

```bash
python scripts/local_gpu.py --toolchain -- environments/fast-build/.venv/bin/python \
  scripts/fast_build.py --profile local-2080ti --nvcc-version 12.8.93 \
  --link-library-dir .cache/toolchains/cuda128/lib --jobs 4

python scripts/local_gpu.py -- environments/fast-build/.venv/bin/python \
  scripts/fast_predict.py --profile local-2080ti \
  --gguf .cache/gguf/qwen3_1_7b-70d244cc86ccca08cf5af4e1e306ecf908b1ad5e/F16.gguf \
  --termination hf-eos --tokens 32 --repeats 2 --output runs/native-1.7b-new
```

All generation conditions below pass; runtime logs confirm **29/29 layers
offloaded to the GPU** for both model sizes:

- 0.6B F16, 1.7B F16 and 0.6B Q8_0: two prompts, two repeats, 32-token cap,
  greedy decoding with the explicit HF EOS adapter.
- 0.6B F16: two concurrent slots, two prompts/two repeats, 16-token cap.
- 0.6B F16: native-stop sampling, temperature 0.7/top-k 20/top-p 0.8/min-p 0,
  seed 17 plus repeat index, 16-token cap.
- 0.6B F16: native JSON grammar, two repeats, 32-token cap. Both outputs parse
  as the requested `{"answer":"yes"}` object. This is a bounded fixture, not
  general JSON Schema or semantic certification.

The sequential native synthetic-token microbenchmarks also pass with full
offload (32-token prefill / eight-token decode, three repetitions, native warmup):

| Artifact | Prefill tokens/s | Decode tokens/s |
| --- | ---: | ---: |
| 0.6B F16 | 2866.52 | 179.54 |
| 1.7B F16 | 2656.33 | 128.19 |
| 0.6B Q8_0 | 3138.50 | 251.55 |

These short native microbenchmarks exclude normal server/task overhead and do
not rank scientific accuracy or constitute a long-workload throughput claim.
Each complete native job and benchmark report, raw response, command, server log,
probability trace and timing is retained under `runs/local-gpu-20261012/`.
The Q8 conversion descends from the verified 0.6B F16 parent and uses the hashed
local quantizer without an importance matrix.

## Cross-backend likelihood failures and release-check fix

Initial F16/Q8 equivalence attempts stopped before native startup because
`release_reference` compared against an allocation baseline taken before the
first cuBLAS operation. A controlled device probe measured zero initial bytes,
**33,554,432 bytes** after the preflight GEMM, and the same 33,554,432 bytes
after model deletion, garbage collection, synchronization and cache release.
The persistent library workspace was being mistaken for a retained model.

The checker now calls the existing device/kernel preflight before measuring
its baseline. The allocation-above-baseline rejection is unchanged. Tests cover
initialization ordering, accepting only the measured workspace baseline, and
continuing to reject retained allocations. All three corrected GPU runs returned
exactly to their 32 MiB baseline before native startup; reference vectors were
persisted before loading the native model. Original failures remain alongside
the corrected runs and have not been overwritten.

The corrected comparisons complete but **fail the unchanged likelihood gates**:

| Reference FP16 → native artifact | Max absolute logprob error | Max KL | Max absolute continuation-score delta (nats) | Result |
| --- | ---: | ---: | ---: | --- |
| 0.6B → F16 | 0.250797 | 0.000366300 | 0.0563673 | FAIL |
| 0.6B → Q8_0 | 0.973127 | 0.00239419 | 0.253544 | FAIL |
| 1.7B → F16 | 0.279343 | 0.0000154958 | 0.000390424 | FAIL |
| Predeclared maximum | 0.1 | 0.0001 | 0.05 | Unchanged |

Native repeated full-vocabulary probabilities are exact in all measured steps,
and all six short greedy cases match HF IDs, decoded text and effective stop
reasons. These matches do not cancel the likelihood failures. The HF EOS adapter
preserves the separately recorded native EOG differences. No threshold, token
law, logits, weights or tokenizer metadata was changed to make a run pass.
General scientific interchangeability remains false for all conditions.

Example comparison command, using a new exclusive output directory:

```bash
python scripts/local_gpu.py -- environments/cu126/.venv/bin/python \
  scripts/fast_equivalence.py --profile local-2080ti --model qwen3_0_6b \
  --gguf .cache/gguf/qwen3_0_6b-c1899de289a04d12100db370d81485cdf75e47ca/F16.gguf \
  --device cuda:0 --dtype float16 --termination hf-eos \
  --output runs/local-equivalence-f16-new
```

Final local regression suite: **308 tests and 118 subtests pass**, two skips
(optional jsonschema and the GPU-marked test in the CPU environment). The GPU
unit test was separately enabled in cu126 and passed. Syntax and diff checks
pass. No hosted CI result is claimed.

The compact [evidence summary](local-2080ti-evidence.json) records actual statuses,
measurements and hashes of local source/raw artifacts. Some runs occurred while
setup/report files were being edited and record a dirty checkout; the canonical
runtime source hashes and executed probe hashes are retained. The published
probe copies add an explicit output-directory option; the exact executed originals
remain in the ignored run folder. The original CPU repeatability investigation
is separate and remains open.
