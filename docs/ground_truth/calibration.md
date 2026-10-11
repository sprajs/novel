# Public synthetic calibration

`data/ground_truth/calibration_fixtures.json` contains 20 fixed, public development
fixtures: 12 additive-offset worlds and eight badge-navigation worlds. Every
fixture is in `calibration`; this file creates no final or sealed confirmation
items. The cases check competence, composition, uncertainty, and formatting.
They do not measure synthetic novelty, useful-idea diversity, or an intervention
effect. Different wording of a correct proof is not a new strategy label.

The fixture answers were specified analytically before running the verifier.
The verifier never reads `expected` when solving or rendering a fixture.
Loading the file checks that its public gold responses agree with the exact
verifiers. Fixtures are retained as a fixed cohort, including simple controls;
model failures are not a selection criterion. A ceiling result is useful
calibration information.

## Data contract

The JSON object has exactly `schema_version: "ground-truth-v0.1"` and `fixtures`.
Each fixture has these fields:

| Field | Meaning |
| --- | --- |
| `fixture_id` | Unique public item identifier |
| `candidate_id` | `synthetic-offset` or `synthetic-badge` |
| `split` | Always `calibration` |
| `family_id` | Descriptive structural motif, not an empirical transfer claim |
| `world_id` | Unique world/context identifier |
| `mechanism` | `additive_offsets` or `badge_navigation` |
| `premises` | Complete visible world specification |
| `target` | Complete visible query |
| `expected` | Public exact response; kept out of model-facing prompts |
| `verifier_id` | `exact-rational-offset-v1` or `exact-badge-bfs-v1` |
| `prerequisites` | IDs of independent standalone probe fixtures |

Object, instrument, and room names are unique simple identifiers. An object
may be unobserved; a door may be a loop. A world may have zero observations.
Unknown names, missing required fields, extra specification fields, floating
point readings, and boolean badge bits are rejected.

The prerequisite IDs describe which fresh probes to run. Run each prerequisite
and recipient in a separate conversation/context with its own prompt. Do not
prepend a probe, its answer, its bridge, or feedback to a recipient. Prerequisite
fixtures have no prerequisites of their own and use different world IDs from
their recipients. These are independent measurements, not evidence that a model
has passed them. Record both the whole fixed cohort and any prospectively
declared prerequisite-competent subgroup.

## Additive offsets

An offset premise specifies `objects`, `instruments`, `offset_scope`, and
`readings`. Each reading is `{"instrument": "one", "object": "A", "value": "17"}`.
With `offset_scope: "instrument"`, its equation is
`true[A] + offset[one] = 17`. Each instrument has a single unknown fixed additive
offset. With `offset_scope: "reading"`, every reading has an independent offset,
including repeated readings by the same instrument. Within-instrument
cancellation is then invalid.

The optional `known_offsets` map adds explicit instrument-offset equations. It
is used only for ordinary subtraction and absolute-anchoring controls; such
knowledge appears in every prompt arm for those worlds. It cannot supply
reading-specific offsets. All true values and unknown offsets are unbounded
rational numbers. No hidden bounds, equal offsets across instruments, positivity,
integer-only restriction, or default zero offset is assumed.

The target is `{"coefficients": {"A": "1", "C": "-1"}, "constant": "0"}`.
Any rational linear functional of the declared true object values is supported,
including sums, multiple independent components, zero coefficients, and an
affine constant. Restricting a verifier to a pairwise difference or to a globally
zero coefficient sum would miss some of these cases. Coefficient sums must
vanish separately in each unanchored component when using the independent
difference-graph method.

Rationals are strings in integer or numerator/positive-denominator form, such
as `"-2"` or `"7/6000000"`. Decimal strings, whitespace, leading zeros, a zero
denominator, and negative denominators are rejected. Gold answers use the
reduced `Fraction` representation; equivalent valid fractions such as `"18/2"`
are accepted for an answer of `"9"`.

The response has exactly these two fields:

```json
{"status": "IDENTIFIED", "value": "9"}
```

```json
{"status": "UNKNOWN", "value": null}
```

```json
{"status": "INCONSISTENT", "value": null}
```

Exact Gaussian elimination over `fractions.Fraction` first checks consistency.
For a consistent system `A x = b`, the target `c x + k` is identified exactly
when `c` annihilates the null space of `A`, equivalently when appending `c` as a
row does not increase rank. An arbitrary particular solution alone is never
an identification proof. Inconsistency takes precedence even if the target
is the constant zero. Tiny nonzero differences and contradictions are exact;
there is no floating point tolerance.

`offset_audit` supplies certificates that `verify_offset_certificate` checks by
substitution into the original equations, without calling elimination:

* `row_combination`: rational equation weights prove `weights * A = c` and the
  claimed value `weights * b + k`. A satisfying-world witness also proves that
  the observations are consistent.
* `two_worlds`: two rational assignments satisfy all readings and anchors but
  give different target values. Their explicit variable order includes true
  objects and instrument offsets, or separate reading offsets.
* `contradiction`: rational equation weights satisfy `weights * A = 0` and
  `weights * b != 0`.

Equation weights follow reading order, then `known_offsets` map insertion order.
Certificates are audit artifacts; they are not part of the model response and
are not inserted into prompts. Rational witnesses prove unbounded uncertainty
directly. Small-world enumeration is not used to declare a target identified.

## Badge navigation

A badge premise specifies `rooms`, `doors`, and `start: [room, bit]`. Each door
is directed and has exactly `from`, `to`, `requires`, and `toggle`. `requires`
is integer `0`, integer `1`, or `"any"`; `toggle` is a boolean. Check the
requirement against the badge before moving, then toggle after arrival if
requested. All moves cost one. Unlisted transitions do not exist.

The target is `{"room": "D", "badge": "any"}`; a goal may instead require
integer `0` or `1`. Reaching the right room with the wrong bit does not reach
that goal. BFS tracks the full `(room, badge)` state. A room can be revisited
with a different badge; revisiting the identical full state is unnecessary
for a shortest path. These fixtures use at most four rooms/eight states. The
solver also works for larger explicitly specified finite room sets.

The response has exactly `status`, `distance`, and `path`. Paths include both
the initial and final states, so distance is the number of edges:

```json
{"status": "REACHABLE", "distance": 2, "path": [["A", 0], ["C", 0], ["D", 0]]}
```

```json
{"status": "UNREACHABLE", "distance": null, "path": null}
```

A start already satisfying the goal has distance zero and a one-state path.
The verifier checks the supplied start, every door transition, the final goal,
and the exact shortest distance. It accepts every valid shortest path, including
the alternative via C in the public diamond fixture; the gold path is only one
example. A legal longer path is rejected. Badge bits and distances must be
integers; Python/JSON booleans are rejected in those positions.

## Fixed cases and hand checks

| Fixture | Purpose and hand-checked result |
| --- | --- |
| `offset-subtraction-probe` | Known zero offset: 11 − 4 = **7** |
| `offset-shared-probe` | Unknown common offset: 17 − 12 = **5** |
| `offset-signed-chain-probe` | Signed composition: (2 − 7) + (4 − 1) = **−2** |
| `offset-absolute-probe` | An unanchored absolute true value is **UNKNOWN** |
| `offset-anchored-absolute` | Explicit offset 2: true R = 11 − 2 = **9** |
| `offset-plan-chain` | (17 − 11) + (25 − 22) = **9** |
| `offset-negative-chain` | (9 − 14) + (6 − 2) = **−1** |
| `offset-disconnected` | A and C lie in independently shiftable components: **UNKNOWN** |
| `offset-inconsistent-cycle` | A − B = 4 and B − C = 3 contradict A − C = 6: **INCONSISTENT** |
| `offset-per-reading` | Fresh offsets prevent cancellation of 17 and 11: **UNKNOWN** |
| `offset-tiny-rational` | 1/1500000 + 1/2000000 = **7/6000000** |
| `offset-weighted-functional` | 2(A − B) − (C − D) + 1 = 6 − 5 + 1 = **2** |
| `badge-transition-probe` | Requires 0, then toggles: A0 → B1, distance **1** |
| `badge-goal-probe` | P1 → Q1 cannot reach Q0: **UNREACHABLE** |
| `badge-plan-revisit` | A0 → B1 → C0 → A1 → D1, distance **4** |
| `badge-plain-alternatives` | Badge is irrelevant; either diamond branch has distance **2** |
| `badge-gated-unreachable` | The only start door requires the wrong bit: **UNREACHABLE** |
| `badge-state-detour` | S0 → C1 → B1 → G1; first reaching B0 cannot end the search, distance **3** |
| `badge-start-is-goal` | Initial W1 already satisfies the goal, distance **0** |
| `badge-cycle-goal-bit` | A0 → B0 → A1 reaches the same room with its required new bit, distance **2** |

The fixture motifs provide distinct checks, not a balanced confirmatory
allocation or held-out topology experiment. New confirmation worlds and frozen
split rules require a later artifact; none are implied by these family labels.

## Prompt arms and original tiny prompts

`render_prompt(fixture, condition)` returns one behavioral prompt string built
only from validated visible premises, the target, mechanism output instructions,
and a declared cue. It does not render fixture IDs, prerequisites, expected
answers, certificates, or trial metadata. The premises-only and bridge arms have
identical world information and explicit prerequisite facts A and B; the bridge
is appended after the common prompt. Both offset arms state same-offset
cancellation `(x + b) - (y + b) = x - y` and signed composition
`(x - y) + (y - z) = x - z`. The same-offset requirement is explicit, so the
per-reading case remains underdetermined. Both badge arms state the lawful
single-step badge update and that every consecutive move of a route must be
lawful, with shortest routes minimizing unit-cost moves. The reusable instruction
to use `(room, badge)` as the search state appears in the bridge cue only.

| Condition | Appended cue |
| --- | --- |
| `premises_only` | None |
| `minimal_bridge`, offset | “Compare readings made with the same fixed offset before combining comparisons.” |
| `minimal_bridge`, badge | “Search over (room, badge) states; revisiting a room with another badge can matter.” |
| `irrelevant`, both mechanisms | “A paragraph can contain several sentences, and a sentence can contain several words.” |
| `wrong_bridge`, offset | “Treat readings made by different instruments as though their unknown offsets were equal.” |
| `wrong_bridge`, badge | “Mark each room visited the first time it is reached and never revisit it with another badge.” |

Aliases `unguided` and `bridge` map to the primary arms; `control` maps to
`irrelevant`. The offset minimal bridge refers to shared fixed offsets and
does not invent that property for the explicitly per-reading world. That world
remains UNKNOWN. The wrong-bridge controls intentionally propose invalid
reasoning; they change no equations or door rules. These cues have not been
length-matched or empirically calibrated. The irrelevant cue states a true fact
unrelated to either mechanism. When a tokenizer is selected, measure and record
each arm's token length and any differences; no perfect length match is claimed.

The original tiny offset case is: each instrument adds an unknown fixed offset;
one reads A = 17 and B = 11, two reads B = 25 and C = 22; determine A − C or
report uncertainty/inconsistency. Its bridge is the offset cue above. The tiny
badge case lists the four doors A0 → B1, B1 → C0, C0 → A1, and A1 → D1, starts
at A0, and asks for a shortest path to D. The fully rendered prompts additionally
state directed-door semantics, unbounded-offset semantics, and the exact output
contract so all assumptions are visible.

Explicitly making A and B available in both primary arms removes an asymmetric
knowledge explanation for a bridge effect. These small tasks may consequently
be at ceiling; that outcome is useful calibration and does not justify selecting
only difficult or failed instances.

The renderer is **not extraction-ready**: it does not append the agreed common
neutral extraction cue or tokenize the prompt. Before any activation capture,
the extraction wrapper must append that same neutral cue in both arms, select
the comparable completed-cue residual site, and record the exact rendered text,
token IDs, cue boundaries, tokenizer/model revisions, and extraction site. The
wrapper also owns seeded generation and separate fresh probe contexts. Changing
wording or cues during an experiment must produce a separately recorded prompt
artifact. No model execution or activation capture is performed by this module.

## APIs and commands

Everything uses the Python standard library. From the repository root:

```bash
python tests/ground_truth/calibration.py check-fixtures
python tests/ground_truth/calibration.py solve offset-plan-chain
python tests/ground_truth/calibration.py render badge-plan-revisit --condition minimal_bridge
python -m unittest discover -s tests/ground_truth
```

`load_fixtures` rejects duplicate JSON keys at every nesting level, nonstandard
numeric constants, and trailing text before schema validation. `check-fixtures`
checks all public gold responses and all offset certificates.
`solve` emits an answer plus certificate for offsets, or an example shortest
answer for badge worlds. `render` emits behavioral prompt text only. Use
`--fixtures PATH` to select a compatible calibration JSON file. These commands
do not infer new splits or generate worlds.

Until infrastructure integrates the module as a package, import by file path:

```python
import importlib.util
from pathlib import Path

path = Path("tests/ground_truth/calibration.py").resolve()
spec = importlib.util.spec_from_file_location("calibration", path)
calibration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calibration)

fixtures = calibration.load_fixtures()
fixture = next(f for f in fixtures if f["fixture_id"] == "offset-plan-chain")
prompt = calibration.render_prompt(fixture, "premises_only")
answer = calibration.solve_fixture(fixture)
assert calibration.verify_response(fixture, answer)
audit = calibration.offset_audit(fixture["premises"], fixture["target"])
assert calibration.verify_offset_certificate(fixture["premises"], fixture["target"], **audit)
```

Public entry points are `load_fixtures(path=None)`, `solve_fixture(fixture)`,
`solve_offset(premises, target)`, `offset_audit(premises, target)`,
`verify_offset_certificate(premises, target, answer, certificate)`,
`solve_badge(premises, target)`, `verify_response(fixture, response)`, and
`render_prompt(fixture, condition="premises_only")`.

`verify_response` accepts a decoded Python dictionary, not a response string.
It returns False for missing/extra response fields, invalid status/type/value,
illegal paths, and non-shortest paths. A malformed world specification raises
ValueError. The caller owns JSON parsing: reject duplicate keys, nonstandard
numeric constants, trailing text, fenced/prose responses, and parse errors
before scoring. A dictionary alone cannot reveal a duplicate key discarded by
an earlier parser. Preserve raw model text separately from the decoded response.

The independent tests include analytic numeric/UNKNOWN/INCONSISTENT cases,
graph-difference versus Gaussian-elimination checks on every fixed-instrument
fixture, direct enumeration of simple state paths versus BFS on every badge
fixture, malformed response checks, alternate shortest paths, invalid
certificates, extreme tiny rational differences, and prompt leakage checks.
Enumeration establishes badge shortest paths only in a specified finite graph;
it is never used to infer offset identifiability from a bounded numeric sample.
