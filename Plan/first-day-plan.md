# First working session: qualify one claim

Prepared 11 October 2026. The goal is a reviewable corpus packet and an executable
measurement specification, not a quick historical-discovery result. Setup already
exists; consult the current README rather than repeating the archived setup plan.

| Time cap | Work | Concrete output |
| --- | --- | --- |
| 20 minutes | Read the active programme and choose one casebook claim | Exact mechanism, assumptions and the earlier claim it must differ from |
| 45 minutes | Inspect its earliest located contribution-bearing version and two strongest antecedents | Source/version/access ledger; a precise remaining novelty claim or a documented rejection |
| 30 minutes | Compare the historical model bundle against disclosure intervals | Literal revisions and a list of unverified public-release channels; no inferred training cutoff |
| 30 minutes | Draft a pre-disclosure challenge and an original target summary | Visible prompt separated from evaluator metadata; explicit hindsight-assistance label |
| 30 minutes | Write target-equivalence, competing-valid-solution and near-miss examples | Proposed human rubric, including unresolved and empirical-evidence labels |
| 25 minutes | Run structural corpus checks and review the proposed scoring interface | Validation output and one small hand-computed probability fixture specification |

A three-hour session may end with rejection or unresolved provenance. That is
progress if the evidence and next search are recorded. Do not fill a candidate
quota by relaxing admission. The public worked cases remain development material.

Use the commands in [data/discovery/README.md](../data/discovery/README.md)
for the new specification and the existing ground-truth checks:

```sh
python -m unittest discover -s tests/ground_truth -v
python tests/ground_truth/artifact_tools.py validate
python tests/ground_truth/artifact_tools.py manifest --check
```

Next, allocate domain and temporal reviewers who can independently assess the
packet; AI agreement is not that review. No reviewer has been contacted by this
plan. Before model evaluation, agree on the semantic rubric, empirical-validity
threshold, assistance conditions and approximate minutes per output judgment.

For a later small development run, use the [measurement protocol](measurement-protocol.md)
and the exact historical model manifest. Do not substitute the July mechanics
template into an April historical condition. Start with token-scoring correctness,
clean generation, capture-only parity and stop-reason logging. Do not acquire a
large model or launch a paid workload as part of this session specification.

At session end, record the scientific blocker separately from an engineering
failure. Missing historical evidence, lack of empirical identifiability, poor
judge agreement, model competence floor and insufficient runtime have different
remedies. Keep the [CPU repeatability caveat](../docs/validation/cpu-repeatability-investigation.md)
and [unperformed GPU validation](../docs/validation.md) visible in any execution
handoff.
