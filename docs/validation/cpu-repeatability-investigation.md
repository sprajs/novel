# CPU repeatability investigation — still open

**Status: the original discrepancy was not reproduced within a fixed bound;
its cause is unresolved. This is not a stability certificate or a numerical fix.**
The same draft PR repairs the failure-evidence gap so a recurrence can be
investigated. It changes no precision, seeds, thread defaults, backend, cache
policy, sampling settings or acceptance tolerances, and adds no retry/warmup.

## Exact original failure

Run `20261011T121557Z-92d81a5e278a`, diagnostic
`20261011T121557Z-ca59276b6ce9`, failed `capture_logits`:

```text
AssertionError: Engineering invariant failed: capture_logits,
max_abs_error=0.003936767578125
atol=0.0, rtol=0.0, status=FAIL
```

This was clean forward number 1 compared with capture-only forward number 2.
Both used the same complete input, `use_cache=False`, no past KV state, frozen
eval weights and eager attention. The residual site was layer 14, final prompt
position 19. Sampling, cache parity and optional gradients had **not yet run**;
they cannot explain this observed comparison. The zero-strength intervention
also had not been created. No raw generation resulted from this failed attempt.

The [byte-identical original config](cpu-repeatability-original-config.json)
records Qwen3-0.6B at the unchanged registry pin, CPU FP32, five threads,
fixture seed 42, sampling seed 17, non-thinking template, 128 input/eight new
token caps, and prompt `Briefly describe what a bridge connects.` The original
config's generic `atol=1e-4`/`rtol=1e-5` was overridden to **zero** for the
capture comparison; the saved check confirms that. The reconstructed pinned
tokenizer input has 20 tokens; its exact IDs and rendered text are in
[the investigation evidence](cpu-repeatability-evidence.json).

The original error record retained the maximum absolute difference but **not**
the tensor values, differing positions/count, exact rendered input, first-pass
RNG/buffer state or CPU runtime settings. Thus there is no justified claim about
which logit/token differed, whether it could change a sampled answer, or whether
the cause was first-forward baseline drift, the observer, a backend issue or
another transient. The current reconstruction cannot recover lost raw evidence.

## Bounded reproduction

Fixed before execution: six sequential fresh Python processes, seven forwards
each, using the existing downloaded/hash-verified snapshot and pinned CPU
software. Four processes used the original five threads; two used one thread
as a distinct diagnostic condition. Every process ran:

```text
clean0 → capture0 → clean1 → capture1 → identity → zero-strength → clean2
```

There was no warmup and no sampling, cache, backward, model download or GPU
execution. Each result was compared exactly with `clean0`; the first clean /
capture pair preserves the original failing order. Every case was retained.

| Condition | Processes | Nontrivial within-process comparisons | Result |
| --- | ---: | ---: | --- |
| Original five threads | 4 | 24 | All exact; maximum error 0 |
| One-thread control | 2 | 12 | All exact; maximum error 0 |

CPU RNG, rotary-buffer hashes, parameter version counters, absence of parameter
gradients and hook counts were unchanged around all forwards. The four
five-thread processes also shared one output hash. The two one-thread processes
shared a different output hash: **thread counts are distinct numerical
conditions**, not interchangeable baselines. This is not evidence that one thread
fixes the original issue; no default was changed. Parameter version checks are
not cryptographic proof against arbitrary out-of-band weight mutation.

[The bounded probe](cpu-repeatability-probe.py) is a validation reproducer, not
a new execution profile. Its only change from the executed source is the path
to the committed byte-identical original config; both script hashes and all
case summaries are retained. To run one additional explicitly named diagnostic
from the repository root after the existing 0.6B download:

```bash
export UV_CACHE_DIR="$PWD/.cache/uv"
mkdir -p runs/repeatability
PYTHONPATH=src uv run --locked python docs/validation/cpu-repeatability-probe.py \
  --threads 5 --output runs/repeatability/fresh-five-thread.json
```

It refuses to overwrite that output. Do not rerun until a passing result appears
or reinterpret a later pass as erasing a failure. Diagnostic continuation within
a case is fixed in advance and reports overall FAIL if any comparison fails.
The canonical smoke still fails immediately on the first failed invariant.

## Threading and backend review

The observed follow-up environment uses Python3.12.14, torch2.8.0+cpu,
Transformers4.57.6, Intel MKL2024.2, oneDNN3.7.1, OpenMP and AVX512, with
`float32_matmul_precision=highest`, deterministic algorithms on and MKLDNN
available. The report captures actual intra-/inter-op thread counts and an
allowlist of thread-related environment variables. These are present-run
observations, not retroactively measured state from the original failure.

[Intel's MKL reproducibility conditions](https://www.intel.com/content/www/us/en/docs/onemkl/developer-guide-linux/2024-2/reproducibility-conditions.html)
make CPU dispatch, thread configuration and related arithmetic controls relevant
to investigation. However, [PyTorch2.8's OpenMP thread setter](https://raw.githubusercontent.com/pytorch/pytorch/v2.8.0/aten/src/ATen/ParallelOpenMP.cpp)
calls both the MKL local thread setter and `mkl_set_dynamic(false)`. The runner
already called `torch.set_num_threads(5)` before loading; unset `MKL_DYNAMIC`
is therefore **not evidence** that dynamic MKL threads caused this failure.
No forced MKL compatibility mode, thread change or backend disablement was
adopted as an unproven fix. [PyTorch's reproducibility guidance](https://docs.pytorch.org/docs/2.8/notes/randomness.html)
also does not make a passing deterministic-mode run proof of universal
repeatability. The pinned Qwen3 source has dropout disabled in eval and default
RoPE without its dynamic-update branch.

## Repair and remaining scientific blocker

The repaired runner writes `execution.json` before any forward invariant:
actual rendered input/token IDs, pinned snapshot hashes, CPU/backend runtime,
RNG/buffer fingerprints, parameter-version fingerprint and hook counts. On a
failed numerical comparison, `error.json` now retains both tensor hashes,
shape/dtype/device, exact failing-element count and up to eight largest failing
coordinates with **both actual values**. This stays bounded; it does not persist
huge full-logit arrays. Post-failure state is recorded where the device remains
usable. Diagnostic errors cannot replace the original numerical FAIL.

Regression tests inject both clean-repeat and capture mismatches. They assert
that the first failure stops inference, generation never starts, gradients stay
SKIP, zero tolerances remain unchanged, and replay context plus raw difference
samples survive in the failed report. Tests cover sample bounds, relative
thresholds, FP64/BF16 serialization, nonfinite JSON handling and unchanged RNG/
inputs. Independent review identified an additional reporting bug: NaN/infinite
maximum errors could prevent strict JSON from saving `error.json`. These values
now serialize explicitly as strings; injected NaN/Inf and diagnostic-exception
regressions preserve the original assertion and failed report. The complete
suite passes 143 tests and 24 subtests, with one GPU test skipped. The evidence
collection and serialization repair are not numerical fixes.

**Remaining blocker:** without a recurrence retaining the missing evidence,
there is no demonstrated cause or targeted arithmetic repair. Exact forward
repeatability remains an open requirement before interpreting subtle activation
or intervention effects. A passing individual smoke supports only its executed
mechanics; it does not certify that causal findings or cross-process stability
are valid. Existing failed evidence remains committed and unaltered.

## CUDA source verification and PR status

The official [PyTorch2.8 installation archive](https://pytorch.org/get-started/previous-versions/)
continues to publish cu126/cu128. The exact Python3.12 Linux wheel URLs and SHA256
values in both locks were matched against the [cu126](https://download.pytorch.org/whl/cu126/torch/)
and [cu128](https://download.pytorch.org/whl/cu128/torch/) indexes without downloading
wheel payloads. The [immutable build script](https://github.com/pytorch/pytorch/blob/v2.8.0/.ci/manywheel/build_cuda.sh)
includes SM75/86 in cu126 and SM120 in cu128. [NVIDIA's Ada guide](https://docs.nvidia.com/cuda/ada-compatibility-guide/index.html)
confirms the SM86-to-SM89 cubin compatibility used by the guard. These establish
published build/support paths, **not actual GPU execution** in this cloud.

The follow-up remains in draft PR#3 against PR1, not main. The verified PR1 base
is `066ecdd204c9b9150f851e085ef31ea12f790457`. GitHub reported no attached status
checks at investigation start; local results are not presented as hosted CI.
No merge, paid compute, driver change or model/CPU lock replacement occurred.
