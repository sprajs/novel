# Historical reconstruction: later scientific-transfer study

This document specifies the historical scientific-transfer track of the
[research programme](research-plan.md). The active entry experiment is
[hidden-context transfer](hidden-context-protocol.md). Historical corpus work
retains its admission and independent-validation requirements. **No historical
idea is admitted yet, and no scientific model-performance result is reported.**

## Long-term ambition

The central question is how a model turns available knowledge into a new,
correct and useful contribution. Novel connects evaluation of that contribution
to the reasoning and internal mechanisms that produce it, then tests methods
for improving discovery under explicit resource budgets.

Historical reconstruction provides a later scientific-transfer assay. The longer
programme extends to causal explanation, reproducible improvements and
prospective work on open research problems across domains. A prospective
contribution requires a contemporary prior-art audit, independent validation
and evidence of scientific value; reconstructing a known result alone cannot
establish it. These are research aims, with later stages contingent on evidence
from the earlier ones.

| Research direction | Intended contribution | Evidence required |
| --- | --- | --- |
| Measure discovery | Auditable tasks and semantic measures of valid scientific contributions | Claim-level admission, independent adjudication and reproducible model evaluation |
| Explain discovery | Testable accounts of reasoning and internal mechanisms | Stable behavioral findings followed by selective causal tests |
| Improve discovery | Methods that increase useful output per compute and review budget | New held-out cases, strong matched baselines and replication |
| Discover prospectively | Independently validated contributions to open research problems | Current prior-art review, domain-specific verification and demonstrated value |

## Historical reconstruction assay

For a fixed, auditable model artifact, how often does a specified generation
procedure recover a human research idea first disclosed after that artifact
existed? How does this vary with historically available background, problem
framing and reasoning instructions? How do exact-string likelihood and selected
internal measurements relate to independently judged semantic success?

Start by building a small, defensible corpus and measuring behavior. Prefer
structured ideas whose value requires a scientific argument, system design,
empirical validation or expert judgment. A first publishable contribution could
be a transparent corpus-admission audit and a bounded reconstruction result,
including a well-measured negative result. A small model at a competence floor
would instead be a feasibility finding. Neither outcome establishes a limit on
all frozen models or identifies a causal discovery mechanism.

The practical hypothesis is that some later human contributions have usable
prerequisites within an old model's reach, yet are infrequently produced under
an explicit search budget. This is testable without assuming that the idea was
absent from all representations. A frozen model can derive a later result from
old knowledge; historical non-exposure and derivability are different questions.
Public-release evidence cannot exclude private precursors, obscure equivalents,
or errors in the historical record. The corpus describes **first documented
public contribution**, not the unknowable moment a person first thought of it.

Synthetic and algebraic fixtures serve as engineering and competence controls,
outside the historical success count. The [evidence collection](../docs/ground_truth/README.md)
provides 51 exact fixtures and candidate audits. Short identities must be
distinguished from later methods and empirical benefits; use the
[earlier-equivalent audit](../docs/ground_truth/lead_temporal_audit.md) to scope
each claim. Mechanics configurations and historically eligible model bundles
have separate roles, documented in the [model audit](../docs/ground_truth/model_audit.md).
Activation transfer and perturb-and-recover require the [causal study gates](causal-review.md).

## Study objects and claim levels

The unit is a **contribution event × eligible model snapshot × input condition**,
not a paper title or a sentence. Several papers can disclose one mechanism;
one paper can contain several dependent contributions. Keep these together in
splits and report the dependence.

Define the claim before model evaluation: problem, assumptions, exact mechanism,
contrast with best earlier work, required evidence and accepted alternatives.
Distinguish concept proposal, correct deductive consequence, reproducible
empirical improvement and practical utility. A published result is evidence to
audit, not infallible ground truth. Human authorship does not by itself prove
unaided human origin; record disclosed computational or AI assistance and
unresolved provenance. AI-discovered artifacts belong in a separate comparison
lane if retained, not in the primary human-origin corpus.

| Evidence achieved | Permitted description | Not established |
| --- | --- | --- |
| Versioned sources and a proposed claim | Exploratory candidate | Admission, historical novelty or correctness |
| Independent domain/temporal judgments plus permitted input and model audits | Admitted for a stated historical reconstruction assay | Universal absence of precedent or contamination |
| Expert-adjudicated free generation under frozen policy | Target recovery or any-valid-solution success under that policy | Autonomous discovery or reproduction of unpublished empirical evidence |
| Changed expressed reasoning or read-only activations | Behavioral change or internal association | A faithful transcript, causal mechanism, or weight-space distance to the idea |
| Controlled, specific interventions on new held-out cases | Effect of the tested intervention | General causal theory of human or machine discovery |

Difficulty of producing a solution and difficulty of checking it are separate
axes. Some code has cheap unit tests but an incomplete specification, open-world
correctness or expensive systems validation. A formal proof may be cheaply
checked once formalized, while an informal mathematical claim and its assumptions
need substantial expert work. Conversely, a physics idea may have an easy
necessary-condition check. Select by the **actual adjudication burden and
scientific content**, not a blanket ban on code or mathematics. Do not claim an
inherently unsearchable class of ideas.

## Corpus strategy

The [corpus protocol](corpus-protocol.md) defines admission and independent human
review. The [casebook](candidate-casebook.md) works through actual claims and
candidate prompts across domains. They remain exploratory, public development
material. The [machine specification](../data/discovery/README.md) guards
against accidental status promotion; validation cannot establish source truth.

Begin with a bounded audit funnel, proposed at 20 leads, six worked development
events, and up to twelve **newly admitted** confirmation events. These are work
caps, not permission to lower standards to fill a table. Freeze the candidate
search frame, date windows and audit budget before inspecting target outputs.
Keep rejected leads and reason counts. Record domains, laboratories, paper
lineages and model lanes rather than implying a representative sample of human
innovation. Broaden the search if all survivors are ML tricks, but retain an
honest small corpus if other domains cannot be admitted.

Do not use model failure as an admission criterion. The primary cohort includes
all admitted cases selected under the fixed recipe. A later deliberately hard
subset can be useful, but its selection changes the population and must be
reported separately. Public worked examples and paraphrases cannot become a
sealed confirmation set. A custodian must prepare new packets and record access
before their first evaluation; public-source targets still create author/judge
recognition risks, so document those risks and blind generation teams where
possible.

The first-pass ordering is methodological: retain an ML-method continuity case
such as MeanFlow while challenging its classical-calculus surrogate; include a
physics mechanism and engineering design whose boundaries require expert
judgment; consider finance only where the target is a scoped inference/design
with contemporaneously available data. Historical financial fit, current market
performance and a causal economic explanation are different endpoints. No
investment recommendation or trading experiment is part of this programme.

## Model selection is part of the scientific design

The [existing audit](../docs/ground_truth/model_audit.md) identifies April 2023
Pythia and April 2025 Qwen snapshots, including tokenizer/interface distinctions.
Use its literal revisions and unresolved release-evidence notes. The current
July Qwen interfaces are mechanics conditions; an April weight object alone
does not make their later templates historically eligible. Model pins are
explicit experimental conditions and require separate validation when changed.

A model manifest must identify weights, tokenizer, template, adapters,
post-training, generation policy, numerical precision and every information-bearing
external component. Compare the latest plausible public release time of that
bundle with the earliest plausible contribution-bearing public disclosure; an
overlapping date interval is unresolved. Commit timestamps, family launch dates,
training cutoffs and a current vendor card cannot substitute for an artifact
release chain. All prompts and supplied background also need version audits.

Choose the primary model lane after historical and development competence
checks, before confirmation. Proposed first audit lane is the original April
Qwen3-1.7B for suitable later targets because existing mechanics work is nearby;
this is not a tested historical execution path. Pythia supports older candidate
questions but needs a different architecture/base-model interface. Small model
size is a feasibility choice, not evidence that large models could not recover
a target. A capability floor should trigger a recorded model/assay decision,
not a claim about unavailable knowledge.

## Measurement, assistance and controls

The [measurement protocol](measurement-protocol.md) is the detailed specification.
Its primary endpoint is a preregistered **semantic hit event** under a fully
specified prompt, stopping rule and sampling policy. Count both valid recovery
of the target mechanism and **any valid solution** to the challenge. A competing
valid mechanism is not a creative failure. Unresolved validity receives its own
label and sensitivity bounds.

Teacher forcing computes the probability of an exact token continuation under
a supplied prefix. It is valuable for locating conditional bottlenecks and
comparing preregistered paraphrases, near misses and older-result controls.
It does not sum over all ways to express an idea or all possible reasoning paths.
A reference mechanism supplied early in a continuation can make its remaining
explanation easy. Preserve the first decisive span, prefix assistance, total
log probability, length, token IDs and raw versus transformed logits. Per-token
or per-byte normalizations are diagnostics, not a correction yielding idea
probability. Never compare tokenizer-dependent perplexities as a universal scale.

For each development event, distinguish problem-only, historically eligible
background, explicitly selected prerequisites, a generic reasoning instruction,
and a target-bearing explanation/recognition condition. The latter is a ceiling
or leakage diagnostic. Author-selected precursor combinations and bibliographies
are hindsight assistance even if all source documents are old. Fresh-context
prerequisite probes, length/style controls, plausible wrong mechanisms,
ideas known before model release and insufficient-information cases help interpret failure.
They do not uniquely diagnose hidden knowledge versus reasoning.

Optional visible-reasoning and tensor measurements are read-only in this phase.
Reasoning instructions alter the experimental condition; emitted rationales
are behavior, not guaranteed internal histories. At an identical pre-answer
prefix, deterministic hidden states are identical across future samples, so a
probe cannot explain seed-to-seed outcome variation using those states alone.
Analyze predeclared divergent prefixes or item-level variation, control for
length and position, and keep model/prompt identity fixed. Post-answer decoding
can reveal answer text rather than prior knowledge. No single activation norm,
probe score or weight distance certifies novelty or out-of-distribution thought.

## Initial protocol and decisions

Proposed scale is six development events followed, only if admission succeeds,
by twelve new confirmation events, with 64 independent generations per event
in the primary condition and at most 2,048 output tokens each. That primary
confirmation cap is 1,572,864 generated tokens, excluding prefill, scoring and
additional diagnostics. It is a costing scenario, not an approved inference job
or a claim of sufficient statistical power. Actual runtime and human review cost
must determine the final frozen cap. Use the detailed protocol's arm budget and
report every attempt, invalid output and budget-truncated output.

Zero successes in 64 independent fixed-policy attempts gives a one-sided 95%
upper bound of about 4.57% for that event's success probability, assuming correct
labels and independent identical draws. It cannot show that the probability is
zero. Much rarer probabilities require much larger samples; curator paraphrase
likelihoods cannot fill that gap. Report event-level intervals, finite-cohort
weights, uncertainty from adjudication and the separate assumptions needed to
generalize to other events. Do not treat repeated tokens, paraphrases, samples or
papers about the same idea as independent human discoveries.

Before confirmation, freeze model bundle and numerical environment, eligible
event inventory, prompt/assistance arm, decoder, total stopping budget, semantic
rubric, human judge calibration, unresolved-label handling, primary estimand,
weights, interval method and multiplicity/optional-stopping rules. Changes after
seeing outcomes require a new version and new confirmation; retain old results.

## Staged implementation and stop rules

| Stage | Concrete deliverable | Exit or stop rule | Ownership/dependency |
| --- | --- | --- | --- |
| 0 — specification | Programme, scoped worked cases, admission records and tests | Independent methodological review; zero fabricated admissions | Research owner and methodological reviewers |
| 1 — provenance and adjudication | Versioned claim/input/model packets; prior-art search ledger; two independent human admission reviews | Admit individually, reject/rescope antecedents, or publish an audit-only result | Domain/temporal experts and corpus custodian; not supplied by AI consensus |
| 2 — measurement mechanics | Exact token scoring, semantic response export, fixed-seed generation and read-only capture logs | Hand-computed probability checks, target-span alignment, no-op/capture parity and backend discrepancy characterization | Separate inference implementation; interface in measurement protocol |
| 3 — development | Six exposed events, old-result/near-miss controls, fresh-context competence probes, calibrated human judgments | Stop at competence floor, unjudgeable claims, runtime failure or unacceptable rubric ambiguity; log revisions | Research owner + experts; no target-driven confirmation selection |
| 4 — frozen observation | New admitted cohort, 64-sample scenario or a justified revised budget; target/valid-solution rates and likelihood diagnostics | Report bounds and all outcomes; insufficient precision stays inconclusive | Requires validated model/backend and frozen study manifest |
| 5 — replication | New events, another appropriate checkpoint or domain, stable adjudication | Test whether associations survive changed surfaces and selection frames | Separate budget and protocol |
| 6 — interventions | Specific bridge or perturb-and-recover hypothesis on new cases | Independent free generation, compute-matched strong baselines and selective causal controls | Requires causal-review.md gates and a separate protocol |
| 7 — prospective discovery | Independently selected open problems and new candidate contributions | Contemporary prior-art audit, independent scientific validation and demonstrated value | Requires replicated evaluation and a domain-specific protocol |

Human adjudication may dominate cost. At the proposed confirmation scale, two
independent first-pass judgments on each of 768 outputs require 1,536 reviews
before disagreements and substantive empirical validation. Measure minutes per
review on development; reduce or narrow the study if this is infeasible. An LLM
can triage, but its score is not the primary scientific validity certificate.
Recruitment, paid services, GPU rental and large model acquisition need a
separate execution budget and operational plan.

The existing [GPU validation gaps](../docs/validation.md) and
[CPU repeatability investigation](../docs/validation/cpu-repeatability-investigation.md)
remain binding engineering caveats. A fixed seed is not a promise of identical
trajectories across batch shapes, kernels, precision, hardware or backends.
Backend parity must cover probability scoring as well as generation. Faster
inference changes feasibility, not corpus validity.

## Literature position

ResearchBench, DiscoveryBench, CUSP and Reconstruction supply candidate sources
and protocol comparisons, not a ready-made eligible corpus. The
[benchmark audit](../docs/ground_truth/benchmark_audit.md) preserves source-version
and licensing distinctions. CUSP's detailed auditor **exempts correct methods
and predictions matching the paper**; matching the intended result is not itself
contamination. Its named-entity test still cannot certify training history.
Reconstruction's bibliography is selected in hindsight, and its v3 limitations
include human validation of the match judge and candidate-matched controls.
[Primary CUSP rubric](https://arxiv.org/html/2605.22681v2#A8.SS1),
[Reconstruction v3](https://arxiv.org/html/2608.16645v3).

Human research-idea evaluations motivate separate novelty, feasibility and
realized-value judgments. They do not certify our historical candidates. The
reported ideation/execution distinction is a reason to preserve unresolved
empirical claims in the outcome rubric. [Si et al. 2024](https://arxiv.org/abs/2409.04109v1),
[Si et al. 2025](https://arxiv.org/abs/2506.20803v1).

Semantic-uncertainty work motivates grouping paraphrases, but discovering
clusters in a finite sample does not enumerate all valid realizations of an
unseen research mechanism. Treat automated equivalence as a fallible measurement
instrument. [Farquhar et al., author account](https://oatml.cs.ox.ac.uk/blog/2024/06/19/detecting_hallucinations_2024.html).
Experiments on expressed reasoning motivate faithfulness cautions and later
intervention tests, not blanket dismissal of all rationales.
[Turpin et al.](https://arxiv.org/abs/2305.04388),
[Lanham et al.](https://arxiv.org/abs/2307.13702).

No unique literature gap is established by this specification. The prospective
contribution is the conjunction of artifact-level temporal eligibility,
claim-level human adjudication, distinction between target and alternative
solutions, and reproducible semantic/likelihood measurement.

## Concrete unresolved scientific decisions

1. Which exact human contributions survive earlier-equivalent and origin audits,
   and which level of empirical support counts as a valid solution?
2. Which exact historical model bundle is sufficiently capable and reproducible?
   The April Qwen lane is a proposal, not a validated scientific baseline.
3. Can independent experts agree on target equivalence and competing solutions
   without turning the problem into recognition of the paper's wording?
4. What independently selected historical problem/background packet avoids
   solving the task through hindsight while leaving it sufficiently specified?
5. What sampling policy and budget are meaningful for the target rarity, with
   affordable human judgments and honest unresolved-label bounds?
6. Who curates unseen confirmation packets and preserves an auditable separation
   from method development? Public fixtures cannot supply that separation.
7. Which internal association would justify a *new* causal intervention study,
   rather than merely rediscovering surface, length or answer-token differences?

These gates determine when each study can proceed and what its results can
support. Historical novelty certification, semantic probability estimation and
prospective scientific discovery each require their own evidence.
