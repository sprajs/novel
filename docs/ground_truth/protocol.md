# Prompt and transfer protocol v0.1

## Estimands and prospective selection

The primary endpoint is independently verified **free-generation success on unguided held-out consequences**, after a frozen intervention learned from other worlds whose concrete answers differ. Here “unguided” means no bridge or solution text in the recipient; both primary arms receive the same complete observations and explicit prerequisites A/B. Compare the bridge-derived intervention with the unmodified recipient baseline. Also compare matched irrelevant, random, answer-only and generic-task interventions. Improvement relative only to a harmful sham is insufficient.

This specification promotes the held-out structural population to primary. The plan's illustrative 160-world mixture and 80-world held-out subset are not a powered design for this endpoint. Sample size, family weighting, practical effect threshold, harm margins, seed count and budget remain unresolved, to be fixed from development variance and actual runtime before generating confirmation data. Do not silently claim power from total completion count.

Choose candidates by temporal evidence and verifiability, and choose development difficulty using a logged recipe. Retain every calibration outcome. Do not admit a confirmation item because that model failed without help and succeeded with hints. All numeric examples in this repository have been seen by authors and are development material. Final families and worlds must be newly instantiated by a designated custodian after protocol freeze, with the authoring/evaluation boundary recorded.

## Common prompt and hint ladder

The visible task is built from an allowlist: ordinary observations, A, B, assumptions, target question and response schema. Names, source titles/dates, publication venue, candidate status, gold answers and verifier traces are omitted unless explicitly part of the treatment. Citation-free paraphrasing does not remove conceptual or hindsight assistance; retain source links in evaluator metadata.

| Arm | Extra content after identical observations and A/B | Role |
| --- | --- | --- |
| P0 `premises_only` | None | Primary textual baseline |
| P1 `minimal_bridge` | One reusable relation, no substituted instance values or target result | Primary guided donor |
| P2 `scaffold` | Named intermediate quantities and steps, still no numeric target | Diagnostic assistance ladder |
| P3 `worked_example` | Solved independent development example | Demonstration and extra information control |
| P4 `full_explanation` | Same-item worked result | Ceiling/leakage diagnostic only |
| C1 `wrong_bridge` | A plausible invalid relation | Specificity and suggestibility |
| C2 `irrelevant` | True, unhelpful prose, naturally matched style/length | Context and compliance control |
| C3 `answer_only` | Gold structured result | Explicit answer leakage diagnostic, evaluator-built only |
| C4 `generic_reasoning` | Generic checking instruction | Generic elicitation control |
| O `observations_only` | Separate baseline omitting explicit A/B | Knowledge/retrieval assistance diagnostic; not the primary causal contrast |

P0 and P1 must be identical before the treatment span. Record rendered text, token IDs and semantic spans, because equal character length is not token matching. Natural-length and matched-token controls are separate conditions; do not claim padding has no effect. Every packet specifies alternative valid routes; the verifier must accept their correct consequences without demanding the nominated explanation.

Concrete calibration bridges are “Compare readings from one instrument before joining comparisons” and “Keep the room and badge together as the search state.” Wrong counterparts compare different instruments directly or discard every later visit to an already seen room. The former fails if offsets vary per reading, and the latter fails on a necessary revisit with a changed badge. Numeric and route examples belong to the calibration specification, not a sealed test.

Historical packets add their own explicit counterconditions: context-dependent DPO normalizers cannot be cancelled across different contexts; residual sampling must use the positive part and renormalize; a zero-norm direction is undefined in normalized weight parameterizations. These are information/validity controls, not harder versions of an always-valid bridge.

## Prerequisites and failures

Probe A and B in separate fresh contexts, using distinct worlds and no carry-over conversation. Score basic arithmetic/probability/graph transition checks separately from recognizing when an operation applies. Supply A/B in both primary arms even if independent probes pass; that makes the primary contrast less dependent on retrieval. Report all targets and a preregistered competence stratum, not only prerequisite successes selected after inspecting target outcomes.

An unaided error can reflect knowledge, retrieval, search, arithmetic, formatting, information insufficiency or truncation. Bridge benefit measures behavioral sensitivity. It does not uniquely identify a missing thought. Correct exposed reasoning may not describe the actual computation; incorrect exposed reasoning may accompany a correct guess. Score answer, proof/certificate if requested, and explanatory text separately.

## Answer-free donor boundary

For paired development donors, append minimal bridge or matched control, then the same neutral cue: `Continue with the requested response.` Capture after the cue has been consumed, before the first generated answer token. Neither prefix contains a gold answer, worked explanation, verifier verdict, hidden target label, candidate ranking or source identifying the desired later method. Store the prefix SHA-256 and token-span boundary.

No-op/capture-only parity and prefix causality are prerequisite instrumentation checks. Varying later teacher-forced answers must leave earlier identical-prefix states unchanged within the stack's calibrated tolerance. The internal state can already encode an answer derivable from the visible world; a textual boundary alone is not an information firewall. Different-answer transfer and balanced donor labels address that remaining alternative.

Preassign donor and recipient answer pools before evaluating targets. Same-instance restoration and whole-state replacement are localization diagnostics; the primary transfer uses disjoint donor worlds and unguided recipients. Keep means and any centered decomposition separate. Freeze extraction worlds, contrast, layer, cue, amplitude, normalization, duration and aggregation on development.

Use a two-axis donor challenge: vary bridge presence at fixed donor answer, and vary donor answer at fixed bridge. Add answer-only deltas, unrelated contrasts, sign-reversed and norm-matched random deltas, shuffled donor pairings, generic “check carefully” deltas, and demonstration task vectors. Report donor-answer copying, format changes and harm on bridge-inapplicable cases. Broad competence improvement can be useful but weakens a bridge-specific interpretation.

Disjoint numeric answer pools are possible for offset/DPO tasks, with token/sign/magnitude shifts recorded. For badge tasks, mere different room letters are weak separation. Require distinct route-state signatures/topologies or lengths under a predeclared answer equivalence; do not claim independence from renamed isomorphic paths. UNKNOWN/INCONSISTENT/UNREACHABLE labels form shared-class guardrail strata, excluded from a universal different-answer assertion.

## Splits and dependence

Use two levels: `world_id` groups latent world, paraphrases, counterfactuals and seeds; `family_id` groups graph/proof topology or structural rule. A split assignment table fixes the entire family for the primary structural-transfer claim. Development donors and development recipients can have separate roles inside the development partition, but never overlap worlds. A same-family unseen-world evaluation is secondary and explicitly named.

The initial public fixture files use only `calibration` or `development`. The manifest reserves `confirmation` with `materialized: false`. Do not rename public fixtures to confirmation later. New family definitions chosen after inspecting confirmation performance require a new study. Seeding alone does not seal a generator whose outputs and labels have already been inspected.

No prompt builder should receive the whole evaluator record. Render from `visible` plus the named treatment only. Keep gold labels and verifiers in a separate evaluator input. Public development labels can be committed; final content lives outside this repository until the study is complete. Commit a custodian-issued inventory digest and access log before evaluation, recognizing that hashes alone do not prove non-access.

## Evaluation and interpretation

Preserve raw generations, strict parsing failures, truncation and all attempted seeds. Use the exact verifier to assess free output; teacher-scored gold likelihood is a localization diagnostic. Numeric rational equivalence and alternate shortest paths should pass; malformed structured responses remain invalid. A verifier failure stops interpretation. Statistical units are worlds; repeated seeds and shared donors induce dependence. A fixed donor library supports inference conditional on that library; multiple libraries need crossed/hierarchical uncertainty.

Require improvement over the unmodified baseline and justified uncertainty for prespecified harms on UNKNOWN and bridge-inapplicable cases. Record family-specific performance and uncertainty; a few families do not establish broad transfer. Any broad inference sweep, compute purchase or new model acquisition lies outside this research collection. No model was evaluated here.
