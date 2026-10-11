# Validation performed on 11 October 2026

The first increment passes its CPU engineering boundary. It does not establish
behavioral competence, bridge transfer, novelty, or GPU feasibility. The actual
run's raw tokens, settings, model/source hashes and checks are preserved in
[cpu-smoke-evidence.json](validation/cpu-smoke-evidence.json). Tensor bytes remain
in the ignored local run, with their checksum in the published evidence.

## Environment and tests actually run

Current cloud: five CPU cores, 18,882,699,264 bytes total RAM (17.59 GiB), Linux
x86-64, no `nvidia-smi`, `torch.cuda.is_available() == False`. This inventory is
independent of earlier environment setup receipts and the user's local machine.

Installed into repository `.venv` using `uv sync --locked`: Python 3.12.14,
uv 0.12.23, PyTorch 2.8.0+cpu, Transformers 4.57.6, huggingface-hub 0.36.2,
tokenizers 0.22.2, safetensors 0.8.0, NumPy 2.5.4 and pytest 9.1.1. The complete
transitive dependency/hash record is [uv.lock](../uv.lock). This is an intentionally
tested reference stack; the [tooling report](tooling/current-stack.md) records
newer upstream releases and incompatible dependency combinations.

`uv run --locked pytest -q`: **73 passed, one skipped, 24 subtests passed** in
3.21 seconds. The skip is the CUDA/FP16 test, because this cloud has no CUDA
device or wheel. The CPU tests use random tiny Qwen3 models and no network.
They verify hook-site meaning, capture independence, nonzero patch effects,
identity and zero-strength behavior, RNG separation, exception cleanup, causal
prefixes, clean cache parity, bounded token generation, config/data separation,
model/artifact integrity, and paper retrieval failures. Those are mechanics
checks, not pretrained capability measurements.

Two bounded pretrained smokes were actually run. The second follows the strict
JSON/config validation change and uses committed source
`0023824` (the full commit and each executed Python source hash are in the record).
Documentation was still untracked, so the honest `git_dirty` flag is true;
source hashes matched the committed code and were checked again at export.

| Measurement | First smoke | Final source smoke |
| --- | ---: | ---: |
| Local run ID | `20261011T102648Z-e94a5c040d65` | `20261011T102824Z-ad620cf2f6e4` |
| Total measured wall time, including verification/load/checks | 20.73 s | 19.66 s |
| Model/tokenizer load time | 1.58 s | 1.54 s |
| Peak process RSS | 4.56 GiB | 4.56 GiB |
| Generated tokens across four conditions | 32 | 32 |
| Generation forwards / processed prefix tokens | 32 / 752 | 32 / 752 |
| Validation forwards / backward calls / verifier calls | 9 / 0 / 0 | 9 / 0 / 0 |

These single-run timings are engineering observations, not a throughput
benchmark or a confidence interval. Process RSS includes transient loading and
is not GPU memory. The four conditions are clean, clean repeat, identity, and
zero strength. The prompt has 20 tokens, output cap eight, and every condition
returns the same eight IDs with `stop_reason=max_new_tokens`. The literal output
is `A bridge connects two or more places,`; the incomplete sentence is a capped
mechanics artifact, not an evaluated task answer.

All 12 pretrained checks passed. Capture-only, identity, zero-strength logits
and both causal-prefix comparisons had maximum absolute error **0**. Forced
clean cached versus full-prefix logits had maximum error
**0.000019073486328125**, under the recorded `atol=0.0001`, `rtol=0.00001`.
Global sampling RNG remained unchanged, all generated IDs matched, parameters
remained frozen with unchanged identity/version counters, and owned hooks were
removed. The selected capture is finite FP32 with shape `[1, 1, 1024]`, block 14,
absolute prompt position 19. Its capture-only provenance is separate from the
tested zero-strength patch. Counter/version checks supplement the immutable
download hashes; they are not a cryptographic rehash of every live parameter.

An independent Astra methods review inspected the core and both actual runs:
artifact hashes/sizes, template re-encoding, generated-ID decoding, source hashes
against the commit, tensor finiteness/shape, cue spans and cost accounting all
agreed. This is AI-assisted engineering/method review, not external peer review.

## Downloads and replay

The only acquired checkpoint is **Qwen/Qwen3-0.6B** at
`c1899de289a04d12100db370d81485cdf75e47ca`, identical tokenizer revision. The
complete local snapshot is **1,519,207,673 bytes**, every allowlisted file checked
against its recorded SHA256. Local path:
`.cache/models/qwen3_0_6b-c1899de289a04d12100db370d81485cdf75e47ca/`.
Loaded unique parameters: **596,049,920**. Source weights are converted explicitly
to CPU FP32; no quantization. Qwen3-1.7B has metadata/hashes only and was not loaded.

Ten paper PDFs are in `.cache/papers/`, **39,121,949 bytes**, all verified against
the [bibliographic manifest](../papers/manifest.json). PDFs and model weights are
ignored and absent from commits. Papers are public lawful downloads; public
redistribution rights are not assumed. Reading notes distinguish full-method
inspection from abstract-only context sources.

```bash
export UV_CACHE_DIR="$PWD/.cache/uv"
uv sync --locked
uv run --locked pytest -q
uv run --locked novel-model verify
uv run --locked novel-smoke --config configs/cpu-smoke.json
# To replay saved settings in the same checkout/environment:
uv run --locked novel-smoke --config runs/20261011T102824Z-ad620cf2f6e4/config.json
```

On a fresh checkout, run `novel-model download` before verify/smoke. Raw local
runs are regenerable, not part of Git. Pin the evidence's source commit and lock
for exact software replay; cross-machine/package-version determinism is not
promised. The final public branch may add documentation after the smoke commit.

## Remaining gates and decisions

- Validate a separate CUDA environment and the RTX 2080 Ti in explicit FP16;
  see [hardware-next.md](tooling/hardware-next.md). No optimized backend was
  installed or benchmarked, and no paid compute was used.
- Integrate the sibling ground-truth branch through the public dataset interface.
  No files under its three owned ground-truth paths were changed. Verifier and
  behavioral calibration remain outside the current smoke.
- Choose the scientific model/mode, task headroom, donor/answer separation,
  budget and effect criterion before confirmation. Qwen3-1.7B is provisional.
- Implement gradients only after the forward baseline; perturbation decay,
  recovery/cache policies, temporal historical audits and scientific claims
  require their own protocols and checks.
- The repository owner still needs to choose a license for original project
  code; upstream software, checkpoint and paper terms are recorded separately.

## Stacked CPU/CUDA profiles increment

The new [profile guide](tooling/execution-profiles.md) supplies actual GPU code,
complete separate cu126/cu128 locks and shareable diagnostic reports. The
[model analysis](models/hardware-suitability.md) preserves original pins and
separates weight arithmetic from runtime/backward memory.

Validation on 11 October 2026: **128 tests passed, 24 subtests passed, 1 explicit
GPU test skipped**. Changed Python files passed Ruff 0.14.14; `compileall` and
`git diff --check` passed. Both CUDA locks pass `uv lock --check` through metadata
resolution; no CUDA wheel payloads were installed and no GPU validation is
inferred from lock resolution. At this stage the root CPU lock, exact registry
and dataset contract were unchanged from PR1 (`066ecdd`). The later 8B addition
below preserves both original model entries and the CPU/dataset contracts.

The real pinned 0.6B CPU model passed the legacy `novel-smoke` command and the
new `cloud-cpu --gradient` profile, including raw seeded generation, selected
capture, exact clean repeat/no-op/zero-strength checks, prefix causality,
three-step forced cache parity, selected gradient, frozen parameters and hook
cleanup. The offline gradient test matches a central finite difference on a
tiny FP32 Qwen3 model. These are mechanics checks, not scientific task scores.
The public [evidence summary](validation/profile-evidence.json) retains actual
measurements and all completed profile attempts; raw tensors/tokens remain in
ignored run directories.

**Unresolved repeatability observation:** one CPU full-profile attempt failed
an exact capture-logit check with maximum error `0.003936767578125`. An earlier
attempt and two later full attempts passed; a separate bounded same-resident
probe found exact agreement in six alternating clean/capture forwards. The root
cause was not established. There is no automatic retry, warmup exclusion or
widened tolerance. A new exact clean-forward-repeat gate runs before capture so
future reports can distinguish baseline drift from an observer effect. Preserve
and investigate any recurrence before interpreting causal results; this draft
does not claim unconditional CPU bitwise stability.

Hardware discovery found torch `2.8.0+cpu`, CUDA build null, availability false,
zero CUDA devices, no `nvidia-smi` and no visible NVIDIA device files. Actual
`local-2080ti` and `rental` preflight requests therefore correctly produced FAIL
reports with downstream GPU/model checks SKIP, without model loading or CPU
fallback. RTX2080Ti/3090/4090/5090 memory fit, native precision numerics, driver
compatibility and performance remain **unverified** until run on actual hardware.
No model larger than 0.6B was downloaded in this cloud, and no compute was rented.

The requested independent GPT-6.1 Sol review found and helped fix partial-failure
status propagation and installed-versus-locked dependency checking. Its final
review found no remaining blocking code issue; this does not replace GPU testing.


### Bounded repeatability follow-up

The [CPU repeatability investigation](validation/cpu-repeatability-investigation.md)
reconstructs the original failure, retains its exact config/error, and reports
six fresh-process probes (four original five-thread, two one-thread controls).
All 36 nontrivial within-process comparisons were exact, with recorded state
unchanged. The discrepancy was **not reproduced; stability is not established**.
The failure-evidence gap is repaired and covered by injected-mismatch tests;
no numerical defaults or tolerances changed. The original root cause remains an
explicit scientific repeatability blocker. Follow-up results: **143 tests passed,
24 subtests passed, 1 GPU skip**, plus the full pinned CPU gradient smoke and
static checks. See the investigation evidence for exact data and wheel-source
verification; no GPU-runtime claim is made.

### Full-capacity RTX 5090 correction

The rental default now targets **RTX 5090 32 GB and pinned Qwen3-8B**, with a
32 GiB ceiling clamped to detected CUDA bytes and 20% allocation headroom.
24 GiB is only an explicit custom rental; CPU and 2080 Ti model/precision/token
defaults are unchanged. The [updated commands](tooling/execution-profiles.md)
start with 0.6B mechanics, then explicitly download and validate the 8B candidate.

Validation: **156 tests passed, 24 subtests passed, 1 GPU skip**. Ruff 0.14.14,
compilation, diff checks and both CUDA lock checks passed. Tests cover the new
default, GPU identity/architecture, decimal GB versus GiB, actual available
memory, gradient/context bounds and the legacy CPU bypass guard. Constructing
all three full architectures on the PyTorch metadata-only device confirmed
parameter counts and embedding ties without allocating weights. The pinned
8B config/index hashes and the five allowlisted index shards were independently
checked against official metadata. Original small-model entries, CPU lock and
scientific data contract are unchanged.

Current cloud preflight passed for CPU with model checks SKIP; rental correctly
failed for unavailable CUDA with GPU/model checks SKIP. The [new evidence](models/rtx5090-evidence.json)
records these results and the metadata-only acquisition. No new pretrained
execution was performed for this correction, no 8B weights were downloaded,
and no GPU compute was used or rented. 8B memory envelopes are estimates only;
actual GPU numerics/fit and the original CPU repeatability anomaly remain open.
