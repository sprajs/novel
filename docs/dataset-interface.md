# Dataset handoff v1

Infrastructure branch: `infra/first-research-increment-20261011`, base
`36b7f6bff70f79642b1ab6d65e591c1b96a44738` (remote main observed 2026-10-11).
The independent ground-truth session owns `data/ground_truth/`,
`docs/ground_truth/`, and `tests/ground_truth/`. This branch does not write those
paths or duplicate their generators/verifiers.

`novel.tasks.TaskInput` accepts a **public-only**, one-condition-per-line JSONL
view. The exact required keys are:

```json
{"schema_version":1,"item_id":"world-1-unguided","world_id":"world-1","family_id":"offset","lineage_id":"structure-1","split":"mechanics","condition":"unguided","prompt":"Complete public observations and question only"}
```

Split is `mechanics`, `donor`, `development`, or `confirmation`. Default loading
rejects confirmation. Sibling exporters can emit this view without changing
their native storage. Keep ground truth, proofs, donor eligibility, and historical
audit fields in separate files keyed by `world_id`; extra fields are rejected.
This protects against accidental whole-record prompt construction, not against
an answer deliberately embedded in the public prompt. Audit the rendered text.

Generation returns raw token IDs and raw decoded text. A separate evaluator
should accept `(world_id, raw_text)` and return a JSON-compatible record including
verifier name/version, validity/status, exact-match result where meaningful,
and failure reason. It must not repair outputs silently or feed hidden answers
back into baseline generation. No grader is implemented here: the independent
ground-truth branch owns that scientific specification.

This interface does not certify split/lineage independence, donor-answer
separation, identifiability, or historical eligibility. Those remain upstream
audits and scientific gates. The initial runner uses one mechanics prompt and
does not open any ground-truth corpus.
