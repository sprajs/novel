# Novel: toward a science of machine discovery

Novel is a research programme for understanding how AI systems generate,
develop and validate new scientific ideas. Its long-term aim is to turn that
understanding into methods that reliably expand what these systems can discover:
from recovering known human insights to producing useful contributions that
survive independent scrutiny.

The programme connects three questions: what makes a generated idea correct,
novel and useful; which reasoning processes and internal mechanisms make it
possible; and how to improve discovery under a measurable compute and review
budget. It progresses through reproducible evaluation, mechanistic explanation,
controlled interventions and prospective research across domains.

The first study uses historical reconstruction as a controlled starting point:
can a fixed model recover human contributions first publicly disclosed after
its exact artifact existed? Corpus admission and semantic measurement come
first, followed by causal studies once the assay is reliable. **No historical
idea is admitted yet, and no scientific model-performance result is reported.**
The implementation and provenance records establish engineering capabilities.

Start with the [Novel reading room](https://novel-reading-room.sprajs.chatgpt.site),
the private, living literature review for this project. It connects recent
research on machine discovery, reasoning, interpretability and neuroscience,
explains results with diagrams and mathematics, and links to concept notes
where more background is useful. Its
[versioned source and maintenance contract](learning/README.md) keep reading
aligned with the programme, including retiring reading that stops being useful.

Continue with the [programme and roadmap](Plan/research-plan.md), then the
[tooling comparison](docs/tooling/current-stack.md),
[model selection](docs/models/selection.md), and [reading notes](papers/README.md).
The [research guide](Plan/README.md) connects the protocols and next working
session. The [evidence collection](docs/ground_truth/README.md) supplies candidate
audits and exact calibration tasks; the [measurement protocol](Plan/measurement-protocol.md)
separates semantic success from reference-string likelihood. Tested
implementation limits remain below.

The locked environment targets Linux x86-64, Python 3.12.14, uv 0.12.23,
PyTorch 2.8.0+cpu and Transformers 4.57.6. Current alternatives were researched
as of 11 October 2026; newer versions are not silently substituted. All direct
dependencies are exact pins; `uv.lock` fixes transitive dependencies and hashes.
CPU FP32 and RTX 2080 Ti FP16 are distinct engineering conditions; scientific
qualification remains separate. The CPU wheel cannot run CUDA tests.
These commands select CPU Torch even on a GPU host. The
[three execution profiles](docs/tooling/execution-profiles.md) provide isolated
CUDA locks and GPU code. [Local RTX 2080 Ti results](docs/validation/local-2080ti.md)
record successful operational checks and the remaining numerical failures.

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
tests the mechanics, including a nonzero effect and hook cleanup. The GPU unit
gate has also passed on a local RTX 2080 Ti. [Local installation and results](docs/validation/local-2080ti.md)
record working uncached inference/capture on 0.6B and 1.7B, plus outstanding
FP16 cache-parity failures. The [GPU profiles and validation commands](docs/tooling/execution-profiles.md)
retain their strict numerical gates; an operational pass is separate from full
profile or scientific qualification.

Three modes are available through `scripts/profile_smoke.py`: `cloud-cpu`
(Qwen3-0.6B FP32), `local-2080ti` (11 GB, Qwen3-1.7B FP16), and `rental`
(RTX 5090 **32 GB**, Qwen3-8B FP16). The rental uses the separate Blackwell cu128
environment and the full detected capacity up to a 32 GiB ceiling, with normal
runtime headroom. Marketing GB and CUDA-reported bytes/GiB are recorded separately.
The [model suitability analysis](docs/models/hardware-suitability.md) separates
weights from KV, activations, gradients, logits and working memory. Start GPU
validation with 0.6B before the primary 1.7B candidate on the 2080 Ti or 8B on
the RTX 5090.

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

For existing runtime integration use the [dataset handoff v1](docs/dataset-interface.md).
The calibration and candidate-audit collection lives under `data/ground_truth/`,
`docs/ground_truth/`, and `tests/ground_truth/`. The
[discovery corpus admission specification](data/discovery/README.md) is separate;
it does not promote those exploratory fixtures to historical ground truth.
Hidden answers are excluded from the public generation interface.

Before the first observational study, admit scoped claims through independent
domain/temporal review, validate an eligible model bundle and freeze the prompt,
decoder, semantic rubric, sample budget and analysis. Qwen3-1.7B remains a
candidate, not a downloaded or validated scientific baseline. Historical
eligibility must audit the exact checkpoint/template date and earlier equivalent
disclosures; a family launch date or undocumented training cutoff is insufficient.
See the [research programme](Plan/research-plan.md) for remaining decisions and
the conditions for a later causal study.
