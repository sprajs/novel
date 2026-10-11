# Novel: frozen-model intervention research

This repository studies whether bridge-conditioned activations transfer useful
composition to different-answer problems. The first increment provides a small
CPU reference implementation and provenance, **not a scientific result**.
Start with the [research plan](Plan/research-plan.md), then the
[tooling comparison](docs/tooling/current-stack.md),
[model selection](docs/models/selection.md), and [reading notes](papers/README.md).
The Plan remains the original hypothesis scaffold; tested implementation limits
and decisions are recorded separately below.

The locked environment targets Linux x86-64, Python 3.12.14, uv 0.12.23,
PyTorch 2.8.0+cpu and Transformers 4.57.6. Current alternatives were researched
as of 11 October 2026; newer versions are not silently substituted. All direct
dependencies are exact pins; `uv.lock` fixes transitive dependencies and hashes.
CPU FP32 is an engineering condition distinct from the prospective RTX 2080 Ti
FP16 scientific condition. The CPU wheel cannot run CUDA tests.
These commands select CPU Torch even on a GPU host. The new
[three execution profiles](docs/tooling/execution-profiles.md) provide isolated
CUDA locks and actual GPU code; GPU validation is still awaiting hardware.

From the repository root:

```bash
# Requires uv 0.12.23; bootstrap separately if needed: python -m pip install uv==0.12.23
export UV_CACHE_DIR="$PWD/.cache/uv"
uv sync --locked
uv run --locked python scripts/check_environment.py
uv run --locked pytest -q
uv run --locked novel-model inspect
uv run --locked novel-model download
uv run --locked novel-smoke
```

Set `UV_CACHE_DIR` in each new shell before using uv. This project-local cache
is writable in the cloud workspace and is already ignored by `.gitignore`;
the cloud's default `/home/agent/.cache/uv` is read-only.

Only `novel-model download` acquires the pinned Qwen3-0.6B snapshot (1.52 GB,
3 GiB default cap). It checks expected lengths and SHA256 before inference.
`novel-smoke` loads local verified safetensors with remote code disabled and
network-free model loading. A snapshot requires about 1.52 GB on disk; allow
additional space for the roughly 0.9 GB environment and uv caches. CPU runtime
and RAM measurements are in [validation](docs/validation.md).

The smoke performs capture, identity, zero-strength, earlier-prefix causality,
and three clean cached-versus-uncached logit steps, followed by four seeded
eight-token generations. It writes a unique ignored `runs/<run_id>/` directory:
raw prompt/output token IDs and text, rendered template and hash, source/config/
lock/model hashes, software/device information, checks with measured errors,
one selected SafeTensors residual, tensor index, timing/cost and file inventory.
Maximum per-run storage is 10 MiB, at most 12 files; an overflow fails explicitly.
EOS remains in raw IDs. A token-cap stop is recorded without calling it an answer
or a reasoning failure. Textual thinking is generated behavior, not a faithful
transcript of hidden computation.

The adapter supports standard dense Hugging Face **Qwen3 only**, unpadded batch
one, eval mode, frozen parameters, eager attention, no quantization or compile.
Its site is the decoder block output after both residual additions. Additive
patches use an explicit semantic anchor and fixed absolute prompt positions;
the full-prefix reference re-applies them at those positions on every forward.
That is a persistent intervention. Temporary noise, noisy-cache recovery, donor learning, broad sweeps and scientific
evaluation are not implemented. A separate optional selected-activation gradient
checks a local logit contrast; it is mechanics, not learned donor attribution. Clean cached generation is available for parity work and
explicitly rejects interventions. New architectures require new validation.

The offline suite constructs tiny random Qwen3 models: it downloads nothing and
tests the mechanics, including a nonzero effect and hook cleanup. GPU-marked
tests are skipped on this CPU cloud. The [GPU profiles and validation commands](docs/tooling/execution-profiles.md)
implement the next bounded hardware checks; there is no measured GPU or
fastest-backend claim.

Three modes are available through `scripts/profile_smoke.py`: `cloud-cpu`
(Qwen3-0.6B FP32), `local-2080ti` (11 GB, Qwen3-1.7B FP16), and `rental`
(Qwen3-1.7B with a conservative 24 GiB budget). A real RTX5090 has **32 GB**, uses
the separate Blackwell cu128 environment, and permits an explicit 32 GiB budget.
The [model suitability analysis](docs/models/hardware-suitability.md) separates
weights from KV, activations, gradients, logits and working memory. Start GPU
validation with 0.6B before the primary 1.7B candidate.

```bash
# CPU diagnostic with selected activation gradient; uses the snapshot above.
uv run --locked python scripts/profile_smoke.py --profile cloud-cpu --gradient
# RTX2080Ti installation/preflight; no implicit model download or CPU fallback.
uv sync --locked --project environments/cu126
uv run --locked --project environments/cu126 python scripts/profile_smoke.py \
  --profile local-2080ti --preflight-only
```

Every execution report includes PASS/FAIL/SKIP facts and a unique shareable
`runs/profile-checks/<id>/diagnostics.json`. The complete per-device installation,
download, forward and gradient commands are in the
[profile guide](docs/tooling/execution-profiles.md). This cloud validated CPU,
static and mocked paths only; CUDA memory fit, numerics and performance remain
unverified until those commands run on an actual GPU.

Paper retrieval is an explicit bounded command:

```bash
uv run --locked python scripts/download_papers.py --help
```

See [papers/README.md](papers/README.md) for exact retrieval/verification commands,
licenses and reading notes. PDFs, weights, caches, private files and raw runs are
ignored. The public repository contains bibliographic records and original notes,
not downloaded full papers. Public availability alone does not imply permission
to redistribute. No repository-wide software license has been selected on the
owner's behalf; model and paper licenses are recorded independently.

For sibling integration use the [dataset handoff v1](docs/dataset-interface.md).
The separate ground-truth branch owns `data/ground_truth/`, `docs/ground_truth/`,
and `tests/ground_truth/`; this increment does not replace or duplicate those
assets. Hidden answers are excluded from the public generation interface.

Before the first causal study, choose a calibrated task/model combination,
thinking mode, donor/recipient policy, worthwhile effect and compute budget.
Freeze those choices before confirmation. Qwen3-1.7B remains a candidate, not a
downloaded or validated scientific baseline. Historical eligibility must audit
the exact checkpoint/template date and target disclosure; a family launch date
or undocumented training cutoff is insufficient.
