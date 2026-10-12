# Discovery corpus specifications

This directory supports the proposed [corpus protocol](../../Plan/corpus-protocol.md),
[casebook](../../Plan/candidate-casebook.md), and [measurement protocol](../../Plan/measurement-protocol.md).
It contains one original, public **exploratory development** admission record for
`meanflow-training-design-2025`. It is evaluator metadata, never a visible prompt.
No candidate is admitted, no human expert review has occurred, no model has run,
and no source or model bytes were fetched for this record.

The target is a generative method and its training design. The
[MeanFlow calculus packet](../../docs/ground_truth/packets/meanflow.md) remains
composition/calibration material; its exact checker does not certify the method.
Known submission, recorded Git commit, and publisher release announcement are
different evidence kinds. First public disclosure, complete snapshot visibility,
training end, reviews, custody and frozen artifact digests remain null or unresolved.
Existing audits supply the attributed source facts, literal April model pin, and
original tokenizer/template hashes. `accessed_on` dates refer to those inherited
audits; they do not claim a new web access. Every source `content_sha256` is null
because its bytes were not acquired and hashed for this record. Planned queries
are explicitly distinguished from the inherited bounded search.

`admission.schema.json` is JSON Schema Draft 2020-12. Its states follow the
protocol: `exploratory`, `admitted_development`, `admitted_confirmation`, `rejected`,
and `withdrawn`. Generic admitted shapes require all eleven gates, no blockers,
reviewed human attribution, completed bounded searches, resolved chronological
ordering, distinct independent human domain/temporal sign-offs, and frozen artifact
digests. Reviews declare expertise, conflicts, blindness to model outcomes,
supporting evidence, signature references and the same reviewed artifact identities.
Confirmation additionally requires private, never-public custody. The public
fixture retains null sign-offs, custody and digests; it cannot be relabelled as
sealed confirmation. A withdrawn shape requires a prior admission reference.

Run the offline checks from the repository root:

```sh
python tests/discovery/validate_admission.py
python -m unittest discover -s tests/discovery -p 'test_*.py'
```

The standard-library checker supports only the bundled assertion vocabulary:
local `#/$defs/name` references; object, array, string, boolean and null types;
`const`, `enum`, `required`, `properties`, `additionalProperties: false`, `items`,
`minItems`, `maxItems`, `uniqueItems`, `minLength`, `pattern`, `format` (`date`
and UTC whole-second `date-time`), `allOf`, `anyOf`, `if`, `then`, and `else`.
It recognizes `$schema`, `$id`, `$defs`, `title`, `description`, and `$comment`
as schema metadata and rejects unsupported keywords. It applies Python regular
expressions to the schema's simple ASCII patterns. It is not a general JSON
Schema implementation. If already installed, an optional test also checks the
schema with `jsonschema`; no dependency is added.

Additional checks validate evidence references, local artifact bytes when a
digest is declared, model/interface identity against the existing audit, source
version/URL agreement, role separation and matching reviewed artifacts. They
expand date precision to uncertainty intervals. This v0.1 subset conservatively
rejects year/month/unknown precision for an eligible claim and rejects overlapping
day/second intervals. Submission or Git timestamps cannot supply public-visibility
evidence. The collection check requires every shipped example to remain public,
development and exploratory. Chronology never follows from a scientific result.

A passing checker means **structural consistency only**. It does not authenticate
reviewers/signatures, verify the truth or completeness of a source search, prove
public visibility, audit all model weight-file identities, enforce append-only
state history, independently seal custody, judge semantic leakage, establish
scientific validity/novelty, or settle licenses. Whole-file artifact references
are placeholders for a later frozen input/rubric/provenance bundle; current
casebook prose is not a frozen executable prompt. Full operational admission
still requires the human review and evidence procedure in the corpus protocol.
The closed metadata shape rejects a `visible_prompt` payload; it is not a prompt
renderer or a semantic confidentiality guarantee.

`finite_measurement.json` is a separate hand-enumerated probability example,
outside the admission schema. Six abstract stopped trajectories have exact-path
mass 0.01, total target-recovery mass 0.30, and validity mass 0.55. The tests show
overlapping prefixes, candidate normalization and averaged/length-normalized
scores are different quantities from event mass. Hypothetical fixed-independent-
trial zero-success upper bounds are 0.0457297 for 64 samples and 0.00996915 for
299; allocating 0.05 error across twelve endpoints gives 0.0820708 at 64 samples.
These are arithmetic illustrations of the measurement protocol, never model
observations, scientific judgments, or an implemented inference estimator.
