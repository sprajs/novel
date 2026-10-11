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

`uv run --locked pytest -q`: **73 passed, one skipped, 23 subtests passed** in
3.05 seconds. The skip is the CUDA/FP16 test, because this cloud has no CUDA
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
