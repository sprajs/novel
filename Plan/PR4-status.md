# Post-freeze idea research: revision and validation record

Prepared 11 October 2026 against verified main
`ea86c6608a0a32c695b6a02122da62767c0fe151`.
[PR #4](https://github.com/sprajs/novel/pull/4) was opened as a draft before the
remaining research was integrated. Merge is held for the requested independent
review and explicit release; this record is not a merge authorization.

## Ownership and changes

This revision owns `Plan/`, introductory research framing/navigation in
`README.md`, and new `data/post_freeze/` and `tests/post_freeze/` specifications.
It changes no runtime, backend, model pin, dependency or environment lock,
existing ground-truth collection, or GPU/CPU validation evidence. Repository
and workspace inspection found no applicable AGENTS.md or local .agents skill
files at the verified base.

The active plan now prioritizes human-idea corpus admission and observational
semantic/likelihood measurement. Bridge transfer and perturb-and-recover remain
later, separately controlled studies. Five original Plan documents, including
the corrected CUSP analysis, are archived byte for byte with source revision
and SHA-256 digests. Existing equations and synthetic fixtures remain useful
calibration; no historical label is promoted.

Four independent AI workers were requested as GPT-6.1 Sol with xhigh reasoning
for methodology, corpus/provenance, skeptical review, and supporting schema
validation. Requested settings are recorded here, not independent attestation
of a serving build. Their agreement is not human expert adjudication. The
[review memo](observational-review.md) records findings and corrections.

Concrete review changes include distinct target/any-valid-solution endpoints,
raw-model versus decoder probability, the supplied-prefix likelihood caveat,
full versus partial evidence for a proposal, state/rubric/schema consistency,
complete-output stopping rules, and the mincut deferral. Six cases are worked
public examples, not a six-item admitted pilot. The one machine admission record
illustrates unresolved MeanFlow method-level admission. Structural checks cannot
establish historical novelty or validate the truth of a review signature.

## Verification

| Check | Result |
| --- | --- |
| New standalone specification suite | 30 passed: 23 admission mutations and 7 exact finite-probability/statistical examples |
| Full repository suite in the unchanged locked environment | 272 passed, 2 skipped, 118 subtests passed |
| Existing ground-truth standalone suite | 87 passed |
| Existing ground-truth schema/manifest checks | Passed; all 44 artifact hashes unchanged |
| Archive integrity | All five Plan copies byte-identical to the verified base; SHA-256 digests match |
| Active Markdown file links and MeanFlow case anchor | Passed |
| `git diff --check` | Passed |

Commands, run from the repository root:

```sh
python tests/post_freeze/validate_admission.py
python -m unittest discover -s tests/post_freeze -p 'test_*.py'
python -m unittest discover -s tests/ground_truth -v
python tests/ground_truth/artifact_tools.py validate
python tests/ground_truth/artifact_tools.py manifest --check
UV_CACHE_DIR=/workspace/research-environment/uv-cache uv sync --locked
UV_CACHE_DIR=/workspace/research-environment/uv-cache uv run --locked python scripts/check_environment.py
UV_CACHE_DIR=/workspace/research-environment/uv-cache uv run --locked pytest -q
git diff --check
```

The first full-suite attempt used the pre-existing research-environment Python:
259 passed, 14 failed, 1 GPU skip, 118 subtests passed. All fourteen failures
stopped in the existing profile environment guard because installed distribution
versions differed from `uv.lock` (including filelock, fsspec, MarkupSafe,
NetworkX, setuptools, and the missing editable project distribution). This was
not treated as a clean run. An offline locked sync identified missing cached
packages; normal `uv sync --locked` then created the ignored repository `.venv`
using cached packages plus the missing Python dependencies. No lock or runtime
source was changed. The final full-suite result above is from that environment.

The final skips are the unenabled GPU test and optional `jsonschema`, which is
not a repository dependency. The separate 30-test run and independent 23-test
admission review both passed the optional Draft 2020-12 validation in the
pre-existing environment where that library is already installed. These are
local test results, not claims of hosted CI or GPU execution.

The suite uses tiny randomly initialized models for engineering tests; no
historical target model or scientific corpus was evaluated. No pretrained
weights or research data were downloaded.

## Remaining scientific work

No historical case is admitted. Independent human domain and temporal review,
earlier-equivalent/channel searches, exact artifact public-visibility evidence,
source rights, complete neutral input packets, competent historical model
selection, human outcome-review calibration, unseen confirmation custody, and
a frozen decoder/rarity/budget choice remain gates. The schema is a structural
consistency aid; signature authentication, long-term custody and append-only
admission history require a later operational process.

The original CPU capture discrepancy remains unexplained despite bounded later
passes, and no GPU validation is added. These limitations matter especially
before interpreting subtle internal differences. No new model probability,
scientific validity, novelty, causal-mechanism or cross-backend parity result is
claimed. No paid workloads, external reviewer messages, full-paper uploads,
private user/work material, or large model acquisitions occurred.
