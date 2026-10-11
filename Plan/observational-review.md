# Independent review of the observational study

Prepared 11 October 2026. This is an independent AI-assisted design review,
not human peer review, target admission, or evidence from model inference.
The review inspected the existing plan and ground-truth audits, then the revised
programme, protocols, six-case book, and structural admission specification. The
file-specific findings and checks are recorded below.

## Verdict and scope

A corpus-first study is worthwhile if its claim is bounded: measure how an
immutable model reconstructs later human research contributions under declared
historical inputs, prompts, decoding procedures, and budgets. Admission and
measurement are the first research work. Perturbation and recovery should follow
only after that assay is useful. A collection of attractive papers, an exact
likelihood score, or a colorful activation plot is not yet such an assay.

The existing audits contain valuable negative evidence. Classical normalization,
coupling, low-rank updates, and calculus must not acquire a later discovery date
because a recent paper uses them. None of the twenty existing leads is admitted.
The corrected CUSP discussion must survive the revision: recovering a later
correct method or numerical prediction is an intended outcome, not automatic
evidence of contamination. Its actual auditor exempts those outcomes; named
entities still cannot establish their own training provenance.
[Existing decision report](../docs/ground_truth/decision_report.md),
[benchmark audit](../docs/ground_truth/benchmark_audit.md),
[CUSP v2, Appendix H.1](https://arxiv.org/html/2605.22681v2).

## Fatal inference errors and practical remedies

“Fatal” below means fatal to the stated inference. These errors do not make a
properly bounded observational study impossible.

| Issue | Inference the study cannot make | Required design response |
| --- | --- | --- |
| Chronology | A release date proves all equivalent ideas were absent from training | Pin actual bytes and all input components; audit exact contribution-bearing earlier channels; record unresolved private or overlooked exposure |
| Derivability | A later first disclosure means the old model could not derive it | Distinguish exclusion of a documented later artifact from generative ability; valid earlier reconstruction is a positive result |
| Likelihood | Probability of one supplied text is the probability of an idea or of discovery | Publish token scoring separately from judged free-generation success; retain paraphrase, length, prompt, and near-miss sensitivity |
| Teacher forcing | Activations while reading the target show the model invented it | Label supplied-target traces as recognition/conditioning measurements; inspect unassisted traces separately |
| Reference matching | Failure to match the historical paper proves failure to find a useful idea | Allow valid alternative methods and unexpected insights; adjudicate correctness, utility, and novelty independently |
| Geometry | Weight distance or activation separation proves novelty or discovery | Declare coordinate system and behavioral endpoints; reserve causal claims for a separately controlled intervention study |
| OOD/search | Post-freeze dates prove distributional novelty or an inherently unsearchable task class | Describe documented history and observed finite-budget failures; avoid universal impossibility claims |
| Adjudication | Code or equations make every target trivially verifiable | State the exact specification, assumptions, checker coverage, and empirical remainder; budget expert review |

## What admission must actually establish

The unit should be a scoped contribution, not an entire paper or method name.
An admission packet must say which proposition, mechanism, design, or prediction
is claimed; what the best earlier equivalent contribution established; and what
is genuinely added. Separately record the originating human authors and any
known AI assistance. A human-authored paper is not proof that every included
idea originated with a human. Unclear origin should remain an explicit stratum.

Use a conservative ordering between model-artifact existence and target
disclosure. If either date is an interval, require the latest plausible artifact
date to precede the earliest plausible contribution-bearing disclosure for the
strict historical lane. Submission, announcement, retained commit, first public
push, and journal publication are different events. A hash proves byte identity,
not when the bytes became public. Public release before disclosure is strong
practical evidence that the exact released bytes already existed; it does not
rule out private precursor communication or undocumented data exposure.
[Existing model audit](../docs/ground_truth/model_audit.md),
[temporal audit](../docs/ground_truth/lead_temporal_audit.md).

Audit every model-visible field and source version. A historical URL can now
serve a revised abstract, later citations, or newer code. A later paper's old
bibliography or selected precursor pair carries hindsight selection assistance,
even if every included text predates the checkpoint. Include a challenge written
from independently selected historical material where feasible, and label
bibliography-conditioned and selected-prerequisite conditions separately.

An exact frozen model can derive an insight not explicitly in its training
examples. Chronology neither proves nor disproves that ability. It also does not
prove that a result is outside the model's learned distribution: later work may
reuse familiar algorithms, notation, mechanisms, or proof templates. Historical
exclusion, intellectual novelty, correctness, usefulness, and generative success
need separate fields and separate evidence.

## The likelihood experiment needs a precise estimand

For a fixed prompt `x` and a supplied complete token sequence `y`, a forward-pass
score can compute `log p(y | x) = sum_t log p(y_t | x, y_<t)`. Record the exact
token boundaries, masking, template, stopping convention, precision, and runtime.
Include the completion/EOS rule when claiming a probability of a complete
response. A prefix score concerns a prefix event and is a different measurement.

Teacher forcing gives the model every preceding reference token. Once those
tokens introduce the crucial construction, later probabilities measure
continuation after assistance. High probability of the final derivation cannot
show that the model would propose the construction from the historical prompt.
Score a prespecified idea-introducing span and the full response separately;
publish the conditioning prefix for each. Neither score substitutes for free
generation.

String probability is sensitive to wording. Competing equivalent expressions
can divide mass, and normalization can change rankings without improving
accuracy. Report raw log probability, per-token summaries, and any contextual
calibration as different quantities. Do not call a length-normalized likelihood
or PMI score a probability. Use fixed human-reviewed paraphrase banks, matched
old-result and near-miss controls, and prompt sensitivity rather than selecting
the most favorable wording after scoring.
[Holtzman et al., Surface Form Competition](https://aclanthology.org/2021.emnlp-main.564/),
[Wiegreffe et al., Increasing Probability Mass](https://arxiv.org/abs/2305.14596).

For an adjudicated idea class `C`, the raw model's semantic mass is
`P_p(C | x) = sum_{y in C} p(y | x)`, using temperature-one full-softmax
probabilities with no sampling truncation and a declared complete-response
protocol. A finite set of distinct, disjoint complete token sequences known to
belong to `C` supplies a lower bound when those raw probabilities are summed.
For a deployed decoder `Q`, use its own sequence distribution; raw `p` scores
do not measure `Q`'s success probability. Averaging paraphrase scores, summing
overlapping prefix events, or applying log-sum-exp to normalized scores does not
supply either bound. No feasible reference bank exhausts open scientific
responses. Semantic entropy research addresses equivalence through sampled
answers and estimated clusters; it does not make all unseen scientific
alternatives observable.
[Kuhn et al., Semantic Uncertainty](https://arxiv.org/abs/2302.09664v3).

The feasible primary behavioral quantity is a judged success rate under a fixed
prompt and decoder, with the entire cohort retained. Repeated draws describe that
sampling procedure. For zero successes in `N` independent, identically decoded
trials with a reliable binary judge, a one-sided 95% upper bound is
`1 - 0.05^(1/N)`. It does not bound success under another prompt, longer reasoning,
search, or a different model. Decode constraints may themselves eliminate valid
outputs. Report format and truncation failures rather than silently deleting them.
Repeated sampling can matter substantially in program synthesis, so candidate
count and selection information belong in every comparison.
[Chen et al., Evaluating LMs Trained on Code](https://arxiv.org/abs/2107.03374v2).

## Judgment, alternatives, and weighting

Use a rubric with distinct verdicts for target reconstruction, specification
correctness, relevance, usefulness, historical novelty, and unresolved evidence.
A correct reference match can lack the claimed novelty. A different method can
be correct and useful. A novel-looking proposal can be wrong. Keep reviewer
disagreements and evidence gaps visible; do not hide them in an average score.

Calibrate judges on blinded reference paraphrases, valid alternative solutions,
plausible invalid variants, and old antecedents before exposing model identities
or experimental arms. Human domain review is needed for the central naturalistic
claims; an LLM judge can assist screening. False-negative judgment is especially
dangerous when the output differs from the later reference. Freeze the rubric,
record decisions on an inspectable subset of failures as well as successes, and
send unforeseen candidate ideas through an explicit secondary review track.
LLM-judge research documents position, verbosity, and self-enhancement biases;
agreement on conversational preferences is not validation for scientific novelty.
[Zheng et al., Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685v4).

Choose what the average represents before collecting outcomes. Equal weighting
of admitted contributions estimates this purposive finite cohort. Equal weighting
of domains estimates a deliberately balanced domain mixture. Neither estimates
the probability of discovery across all science. Publish domain-specific results
and the full screening/admission funnel. Do not select targets because the tested
model failed, and do not silently replace hard-to-adjudicate targets with easy
ones. Multiple claims from one paper, laboratory, precursor family, or shared
challenge are dependent; repeated seeds and paraphrases are not new independent
ideas. Resampling and uncertainty must respect those groups.

## Structured domains need different evidence

For CS or mathematics, finite test passing can establish a declared benchmark
property, while a machine-checked proof can establish a formal statement under
its assumptions. Neither automatically establishes the natural-language claim,
general performance, efficiency, implementation safety, or novelty. Verifying a
provided certificate can be much easier than inventing it. The existing
AlphaEvolve and DoRA audits already expose this distinction.

For physics, separate mathematical consequence, modeling assumptions, and
empirical adequacy. Supplying an unmeasured physical law is information assistance,
not evidence that the model filled a computational gap. For engineering, specify
the operating envelope, constraints, tolerances, failure conditions, and which
simulation or hardware evidence remains outstanding. These domains can be useful
precisely because the judgment is harder; difficulty requires an explicit review
budget and uncertainty state.

For finance, reconstructing a statistical method or historically proposed
mechanism is different from establishing a tradable result. Execution against
old data does not settle point-in-time availability, selection over many trials,
transaction costs, regime stability, or future value. Retain these as distinct
validation obligations if they are part of the target claim. Backtest-overfitting
research directly studies selection over strategy configurations.
[Bailey et al., The Probability of Backtest Overfitting](https://scholarworks.wmich.edu/math_pubs/42/).

## Internal measurements and later interventions

Internal-state observations should be secondary and explicitly descriptive.
Contrasting teacher-forced correct and incorrect texts can reflect their tokens,
lengths, likelihoods, or already supplied answers. Probes require held-out
contribution families, surface controls, and predictive evaluation; above-chance
decoding alone does not establish that the model uses the decoded information.
Generated reasoning can omit influences on an answer and is not a transparent
record of computation.
[Turpin et al., Unfaithful Explanations](https://arxiv.org/abs/2305.04388v2).

There is no universal coordinate distance from “ordinary” to “novel” thought.
Parameter geometry can change under function-preserving reparameterization;
therefore a raw weight displacement needs a particular parameterization and a
behavioral question. This is a limitation on interpretation, not a claim that
all metrics in one fixed architecture are useless.
[Dinh et al., Sharp Minima Can Generalize](https://arxiv.org/abs/1703.04933).

A later perturb-and-recover or activation-transfer study needs its own frozen
selection policy, fresh evaluation, no-op/restoration checks, token-space search
controls, matched compute, and answer-leakage controls. Activation-patching
results depend on the metric and corruption/intervention design. Descriptive
separation cannot establish necessity, sufficiency, or a uniquely missing idea.
No finite-budget failure proves a task class inherently unsearchable.
[Zhang and Nanda, Patching Best Practices](https://arxiv.org/abs/2309.16042v2),
[Heimersheim and Nanda, Interpreting Patching](https://arxiv.org/abs/2404.15255).

## Revision review record

The final review read the active [programme](research-plan.md),
[measurement protocol](measurement-protocol.md), [corpus protocol](corpus-protocol.md),
[casebook](candidate-casebook.md), Plan navigation/session/reading/causal files,
root README, and [schema, example, scope notes](../data/post_freeze/README.md)
with their validator and mutation tests. The review checked the methodological
claims against the primary sources linked above; it did not independently
re-audit every candidate paper's full versioned technical content.

| Finding | Resolution in the revised artifacts | Status |
| --- | --- | --- |
| Old plan prioritized synthetic bridge transfer | Programme now starts with claim-level corpus admission and observation; old fixtures remain calibration and the earlier plan is archived | Resolved for planning |
| Reference likelihood could be mistaken for idea probability | Measurement separates decoder `q` from raw `p`, complete-path lower bounds from finite sampling estimates, and first-contribution spans from downstream forced continuation | Resolved |
| Paper matching could suppress valid alternatives | Primary `T = V AND M` and accompanying `V` distinguish target recovery from any valid solution; older equivalent routes and unresolved alternatives retain separate labels | Resolved |
| A plausible scientific proposal could be counted as validated | Each event must freeze an evidence tier: conceptual construction under assumptions, proved property, or empirical realization; missing essential empirical evidence remains unknown/plausible rather than definite `V` | Resolved in specification; actual rubrics pending |
| A short response could be credited with a major theorem | Casebook defers mincut generation until an expert defines an independently meaningful lemma-sized target; scoped response/cap feasibility is a gate, and a generic outline cannot count as proof | Resolved for planning |
| Corpus lifecycle and schema were inconsistent | Schema now uses the protocol's admitted-development/confirmation and withdrawn states, with distinct artifact-bound human review declarations and exposure/custody fields | Resolved structurally |
| Structural checks might be read as authentication or admission | Data README explicitly limits checks to declared consistency and lists signature authentication, source truth, full weight identities, custody, append-only history and semantic leakage as unenforced obligations | Resolved by scope limitation |
| Historical sources could be promoted despite adverse evidence | All six cases and the MeanFlow record remain exploratory; antecedents, manuscript-date evidence, the engineering rendering conflict and public-visibility gaps remain blockers | Correctly unresolved |

Independent execution of the structural CLI passed. The new admission suite
passed **23 tests**, including its optional full Draft 2020-12 shape check with
the already installed `jsonschema` library. The mutation tests exercise status
promotion, independent reviewers, bound digests, mutable model/source aliases,
date kinds/precision, public confirmation exclusion, fabricated references,
duplicate keys and nonfinite JSON. These results establish guard behavior for
declared records, not the truth of the declarations. The review's local links
resolved and `git diff --check` passed at inspection.

No blocking methodological error remains in the reviewed planning specification.
This is readiness for independent review and next-stage admission work, not
readiness for a historical experiment. Human origin and novelty judgments,
earliest-equivalent/channel searches, original source-version reconciliation,
exact public artifact evidence, source rights, complete neutral input packets,
historical-model competence, tier-specific outcome rubrics, expert capacity,
custody and a frozen precision/runtime budget remain scientific gates. Broader
source or serving claims would require additional evidence. The existing CPU
discrepancy and unperformed GPU validation remain engineering limitations.

No model weights or datasets were downloaded, no inference or paid workloads
were run, and this reviewer changed only this document.
