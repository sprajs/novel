# Measuring recovery of ideas disclosed after a model freeze

Scope: later scientific-transfer track; the next experiment is [HC-1](hidden-context-protocol.md).

Prepared 11 October 2026. Status: proposed observational protocol, ready to turn into a preregistration after the explicit freeze decisions below. No target model has been run, no historical discovery has been certified, and no confirmation corpus exists. Numerical allocations are feasibility proposals, not measured runtime or a claim of adequate rare-event power.

This later historical reconstruction study asks how a particular immutable model distributes probability over valid reconstructions of human ideas whose first contribution-bearing public disclosure came after that model already existed. It measures behaviour and conditional likelihood, then characterizes observable failures. Changing activations, weights, caches, or decoding to increase recovery is a later experiment with its own protocol. The [causal study guide](causal-review.md) defines requirements for that work; this protocol defines the observational endpoint.

The [ground-truth collection](../docs/ground_truth/README.md) supplies development fixtures, audits, and verifier precedents. Its DPO, speculative-decoding, DoRA, FlashAttention, and MeanFlow packets are not admitted historical discoveries. In particular, recovering a classical identity appearing inside a later method cannot establish recovery of that method's novel contribution. Read the [antecedent audit](../docs/ground_truth/lead_temporal_audit.md), [model audit](../docs/ground_truth/model_audit.md), and [corrected benchmark audit](../docs/ground_truth/benchmark_audit.md) before selecting events.

## 1. Claim, unit, and primary estimands

An **event** is one precisely stated contribution, with its assumptions, useful consequence, and novelty boundary. It is not automatically an entire paper, a named system, or each question derived from one paper. Two papers sharing the same contribution belong to one event cluster. Several dependent contributions from a paper must retain a shared paper/family identifier.

For event `i`, freeze a model-visible problem `x_i`, an immutable model/interface `m`, a decoder `d`, and a total output-token budget `B`. Let `H` be the complete generated token trajectory, including any expressed reasoning, delimiters, answer, and sampled stopping token. At the cap, the trajectory ends by the declared administrative stopping rule. The decoder induces the distribution `q_m,d,B(H | x_i)`. All probabilities below are conditional on this exact setup.

Two separate predicates are essential:

- `V_i(H)`: the nominated final proposal is a valid solution to the problem as posed, meeting the preregistered assumptions, constraints, evidence tier, and utility threshold within that tier. Valid alternatives to the human contribution count here.
- `M_i(H)`: the proposal contains the event's specified contribution rather than merely a familiar antecedent, vague suggestion, correct numerical consequence, or shared terminology.

The primary target-recovery event is `T_i(H) = V_i(H) AND M_i(H)`. Estimate `pi_T,i = Pr_q[T_i(H)=1]` and report `pi_V,i = Pr_q[V_i(H)=1]` alongside it. Report partial mechanism matches separately; they do not silently enter `T`. Since `T` is a subset of `V`, a scoring result with more target recoveries than valid solutions is an evaluation failure.

Valid alternatives also receive separate novelty tags: `known_pre_freeze`, `historically_novel_candidate`, `current_community_novel_candidate`, or `unresolved`. These tags require an independent antecedent/current-literature assessment against the stated reference archive; validity alone does not establish novelty. A preregistered novel-alternative endpoint may be added in a later study with its own definition and multiplicity allocation. In this initial study unexpected alternative ideas are preserved for review, without post hoc expansion of the primary target criterion.

For example, an older exact attention implementation could solve an attention problem validly while missing a later contribution's particular IO schedule and bound. It is a `V` success and an `M` failure. Calling it a creative failure would confuse recovery of one historical mechanism with solving the scientific problem. Conversely, a sentence resembling the later algorithm without a sound derivation or implementable construction can match `M` and fail `V`.

Grade the final endorsed proposal, using a rule established before sampling. The proposed task asks for one coherent proposal; if the model lists several unranked candidates, grade the first nominated proposal and record the additional candidates separately. An idea mentioned tentatively and then rejected in the reasoning is an exploratory trace annotation, not primary recovery. Verifier-assisted best-of-many selection is a different system and must not be introduced into this baseline.

The primary corpus summary is the equal-event average `mean_i pi_T,i` over the fixed `admitted_confirmation` corpus, accompanied by every event's interval and the analogous valid-solution average. Development and exploratory cases are reported separately. Domain summaries are secondary. This is inference about the selected corpus and decoder. A convenience corpus of interesting published successes does not represent all human discoveries, all possible ideas, or a distribution of scientific opportunities.

The historical label means reconstruction of a contribution unavailable through the declared pre-freeze public history. It does not establish a contribution new today, unsupervised scientific autonomy, or impossibility of exposure through a contaminated prompt. A temporally eligible model producing the target is the intended positive observation. Matching the later method or result must not be used to disqualify that observation merely because it matches. CUSP's published auditor explicitly exempts matching methods and numerical predictions; its named-entity audit also does not certify training provenance. [CUSP v2, Appendix H.1](https://arxiv.org/html/2605.22681v2#A8.SS1); [local evidence correction](../docs/ground_truth/benchmark_audit.md).

## 2. Admission and freeze before any confirmation sampling

Keep an event ledger that retains accepted, rejected, and unresolved candidates. Admission depends on chronology, contribution-level novelty, prompt integrity, and adjudicability. It must not depend on whether the selected model fails unaided, assigns a low canonical likelihood, or succeeds with a hint.

Each candidate needs the following completed event card:

| Field | Required decision or evidence |
| --- | --- |
| Contribution | The smallest useful new mechanism/proposition to recover; an explicit contrast with the nearest antecedent |
| Human disclosure | Versioned contribution-bearing text/code and the earliest verified public channel; earlier preprints, code, talks, abstracts, theses, and equivalent results searched |
| Freeze identity | Literal model revision and file hashes, all post-training/adapters, tokenizer and template identities, numerical conversion, and evidence that the relevant frozen artifact existed before disclosure |
| Historical problem | A question a pre-disclosure researcher could have asked, with a dated basis for constraints/observations and permitted assumptions |
| Prompt provenance | Exact historical source versions and excerpts; separately identify curator-authored instructions, target-selected prerequisites, and every form of hindsight assistance |
| Validity/evidence tier | Freeze conceptual construction under stated assumptions, proved property, or empirical realization as the endpoint; give its mathematical check, executable test, or domain rubric and concrete failure cases. Empirical claims need relevant evidence, not only plausible prose |
| Mechanism identity | Required contribution components, accepted equivalents, exclusion of earlier methods, and counterexamples that distinguish surface similarity from recovery |
| Reviews | Independent domain and chronology judgments, disagreements, access/license decision, and exact lifecycle status `exploratory`, `rejected`, `admitted_development`, `admitted_confirmation`, or `withdrawn` |

A paper's date after an advertised training cutoff is insufficient. An old repository name, a moving branch, or a current chat template is insufficient. The local audit documents why April 2023 Pythia snapshots and April 2025 Qwen snapshots have different historical roles, and why later `main`, final-step branches, and tokenizer revisions cannot be substituted casually. Preserve the audited complete artifact identity. Runtime conversions performed now are declared numerical conditions; they are not new historically trained models.

Do not manufacture an admitted set by selecting a small classical lemma from a larger novel construction. If a target requires empirical validation unavailable in the historical prompt, distinguish proposing the mechanism from correctly predicting an unknowable future measurement. Design problems can admit many valid solutions; measurement questions may be underdetermined. The curator must state which problem is being asked.

The proposed development set contains six events and the proposed confirmation set twelve distinct eligible events, preferably spanning more than one scientific mechanism/domain. These are targets for collection, not existing items. If twelve cannot pass admission, report the actual smaller cohort and its limitations; do not replace rejected events with synthetic fixtures under a historical-discovery label. Splitting by paraphrase or consequence of the same event does not provide independent confirmation. If only unresolved candidates remain, stop the historical claim and continue separately labeled mechanics or exploratory case studies.

Freeze before confirmation: event inventory and cluster IDs; canonical problem and permitted inputs; rubric and equivalence rules; reviewer plan; model/interface; decoder; output/stop policy; reference realizations and span annotations; diagnostic sites; sample counts/seeds; exclusion policy; interval construction; planned comparisons; operational caps; and the scientist-approved meaning of a worthwhile recovery probability. Hashes support auditability but do not prove a custodian did not inspect content. Record custody/access separately.

## 3. Prompt conditions and the actual sampling law

Use one short, model-appropriate canonical problem prompt per confirmation event. Base models may require a completion format rather than an invented chat interface; few-shot formatting examples must be generic, historically eligible, and declared. An instruction-tuned model's exact template and thinking argument are part of the condition. No target-paper title, distinctive later system name, citation, gold answer, verifier trace, or hidden evaluator metadata enters the primary prompt.

| Condition | Model-visible information | Interpretation |
| --- | --- | --- |
| `P0 historical_problem` | Historically available problem, observations, constraints, and generic response request | Primary historical problem-conditioned reconstruction |
| `P1 supplied_prerequisites` | P0 plus explicitly supplied pre-freeze prerequisites selected by the curator | Knowledge/retrieval assistance; target-based selection is declared hindsight |
| `P2 structural_hint` | P1 plus a minimal relation or strategy | Guided reconstruction; supplying a novel relation is direct method assistance |
| `P3 supplied_construction` | Target construction/conclusion supplied for criticism or verification | Recognition/execution diagnostic; never free invention |

Do not describe P1 as unassisted if its curated precursor pair reveals the desired combination. If no independently justified P0 can be constructed, make selected-prerequisite reconstruction the named study and explain that scope. Paraphrases prepared before evaluation form prompt sensitivities, not extra independent events. Do not select the best prompt on confirmation outputs. Pooling heterogeneous prompts estimates a defined prompt mixture only if its weights and allocation were frozen in advance.

The proposed primary decoder is ancestral sampling with temperature `1`, no top-p/top-k/min-p filtering, no repetition or presence penalties, and no constrained grammar. Under verified absence of additional runtime masks/processors, its next-token law equals the frozen model's raw softmax law `p_m`. This choice measures the model's raw sampling law, not the best practical decoding strategy. An automatic suppression of special tokens, EOS constraint, forced thinking transition, or other processor makes the actual law `q` different; record and name it honestly.

Manufacturer-recommended practical decoding may be a separately frozen sensitivity condition. Temperature rescales logits and truncation filters renormalize retained tokens, so samples under such a decoder estimate `pi` under `q`, not semantic mass under raw `p_m`. A target path can have positive raw probability and zero probability under top-p. Nucleus sampling is a deliberate change to the token distribution, with a distinct quality/diversity tradeoff. [Holtzman et al., *The Curious Case of Neural Text Degeneration*, v2](https://arxiv.org/html/1904.09751v2).

On development, inspect coherent completion rate, format compliance, output length, and cap truncation. If the proposed raw-law decoder produces no valid/comprehensible completions, or pervasive incomplete reasoning makes the assay unsuitable, stop that configuration. Select and preregister a suitable `q` or budget on development, then describe the eventual result as conditional on that `q`. Do not preserve a raw-probability claim while secretly replacing its sampling law. A proposed warning trigger is more than 20% development outputs without a complete endorsed final proposal at the cap; the response is feasibility review, not selective removal of long confirmation failures.

`B <= 2,048` is a proposed output ceiling, counting reasoning and final tokens together. It is not a promise that 2,048 tokens suffice. Freeze a common feasible budget for primary events after accounting for the selected model's context window and rendered prompt lengths. In particular, a model with a 2,048-token total context cannot accept a long prompt plus 2,048 output tokens. If a valid problem requires more context than the chosen historical model can provide, that is a model/assay feasibility failure. Shortening the problem so far that the target strategy is supplied is not a neutral fix.

Stop on the model/interface's declared terminal token or at `B`; preserve the exact stop reason. An administratively stopped output can satisfy the bounded endpoint if it already contains a complete endorsed final proposal; sampled EOS is not required for semantic success. Do not append an answer cue after the cap or discard unfinished reasoning from cost accounting. Maintain independent seeded draws in fresh contexts, with no conversation carry-over or verifier feedback. Distinct seeds are a reproducibility mechanism, not proof of IID sampling: validate actual RNG handling, caching, batching, and absence of adaptive feedback. Randomize run order within the frozen schedule to expose operational drift.

Retain duplicate sampled outputs in the numerator and denominator: they carry probability mass. Deduplication is appropriate for a distinct-mechanism inventory, not for estimating a draw's recovery probability. Repeated greedy decoding of the identical deterministic condition supplies one outcome, not independent binomial trials.

## 4. Semantic adjudication and valid alternatives

Write the rubric before measuring probabilities. It should name the necessary mechanism, assumptions, supported consequence, and minimum justification, with original examples of valid paraphrases, genuine alternative solutions, near misses, and plausible wrong ideas. Accept algebraic/programmatic equivalence where justified; do not require exact wording, variable names, equation layout, or the later paper's chosen narrative.

Meaning-level grouping is motivated by semantic-uncertainty research, which explicitly distinguishes probability of a token sequence from probability of an equivalence class of meanings. Its QA clustering method is not a scientific correctness or novelty verifier. A mechanism with multiple interacting conditions may be neither equivalent to nor entailed by a superficially similar paragraph. [Kuhn, Gal, and Farquhar, Section 3.1](https://arxiv.org/html/2302.09664v3); [Farquhar et al., *Nature* 2024](https://www.nature.com/articles/s41586-024-07421-0).

Prefer a typed output contract suited to the domain: assumptions, proposed object/mechanism, derivation or implementable construction, and claimed consequence. Keep semantic validity separate from successful schema parsing. A valid mechanism expressed in prose can satisfy the semantic endpoint even when its JSON is malformed; report operational schema success separately. This avoids manufacturing a conceptual failure from punctuation. The proposed contract still requires an endorsed final proposal; an unfinished scratchpad without one fails the bounded final-proposal endpoint and is recorded as truncation.

Freeze the event's completion rule: all scientifically required fields are expressed, the proposal is endorsed as the final answer, and unresolved contradictory claims do not invalidate it. A proposal complete by token `B` can pass even if additional commentary runs into the cap; a partial mechanism inside unfinished reasoning cannot. Report administrative cap stops and incomplete-final-proposal stops separately. This endpoint concerns the content produced within the budget, rather than a hypothetical continuation after it.

For structured CS/engineering ideas, a checker can establish consequences or constraints but may not establish target mechanism identity. For physics, a correct numerical prediction does not imply a new explanatory theory. For finance, a coherent strategy or theorem requires its declared market/observation/transaction assumptions; a historical profitable realization alone does not establish an ex ante valid general mechanism. These are rubric design distinctions, not financial recommendations. When correctness needs experiments or domain judgment, retain that requirement rather than reducing validity to an LLM match score.

Keep mechanism match, validity under stated assumptions, plausibility/testability, and empirical support as separate labels. Set each event's primary hit threshold before generation. A mathematically valid construction in an idealized model need not be experimentally realizable; an executable implementation need not achieve its proposed distributional benefit. If empirical adequacy is essential to the requested solution and remains unresolved, label it `unknown` or `plausible_proposal`, not a definite `V` or novel-valid success. If the stated endpoint is conceptual recovery, name that scope and do not upgrade it to scientifically validated performance.

Proposed confirmation adjudication uses two independent domain reviewers on all primary outputs, blinded to sampling condition, likelihoods, tensor statistics, and other reviewers' judgments. They may inspect the evaluator-only target packet to assess contribution identity. Each records `V`, `M`, assumptions satisfied, unsupported claims, alternative mechanism class, and uncertainty, with the decisive output span and justification. Resolve disagreements using a third reviewer or retain `unknown`; do not force consensus. AI-assisted draft annotations can reduce clerical work but do not substitute for independent human review without explicitly downgrading the evidence.

Human-review research supplies a precedent for blinded assessment of research proposals while also emphasizing that expert novelty/feasibility judgments require later execution to establish scientific outcomes. That study does not certify this corpus, rubric, or frozen model. [Si, Yang, and Hashimoto, *Can LLMs Generate Novel Research Ideas?*, v1](https://arxiv.org/abs/2409.04109v1).

Before confirmation, calibrate on at least ten authored examples per rubric containing both valid alternative wordings and critical near-miss/antecedent controls. Any critical false-positive admission stops rubric use until revised and recalibrated on fresh examples. A tiny calibration set does not certify judge sensitivity/specificity. Reviewer capacity is a substantive budget decision: 768 primary outputs imply 1,536 independent reviews, potentially far more human time than GPU time. If that capacity is unavailable, reduce the cohort before freeze or label the study exploratory; do not silently assume that an uncalibrated automated judge makes the same measurement.

Preserve all sampled outputs. Sample frequency estimates event probability; lexical novelty and semantic-cluster counts are descriptive extras. Low semantic entropy can accompany confidently wrong ideas, and high entropy can accompany multiple valid mechanisms. Neither establishes discovery or rarity of the target. In particular, do not average likelihoods of sampled strings and call that semantic mass: such an average is generally a different quantity from the sum over all accepted outputs.

## 5. Forward-pass likelihood: exact targets and decisive spans

Forward passes are an essential observation, but they answer a different question from sampling. For a fixed token realization `y = (y_1, ..., y_L)` and exact prompt `x`, compute

```text
ell_p(y | x) = sum_t log p_m(y_t | x, y_<t).
```

Include a sampled terminal token if the claim concerns that exact completed trajectory. A score omitting terminal probability is a prefix-cylinder probability, not the probability of that complete stopped answer. A trajectory stopped administratively at `B` has a different endpoint: its length-B prefix probability under the declared cap policy. Record which object is being scored. Store per-token log probabilities, not only a rounded scalar; use stable log-softmax accumulation, explicit token offsets, and the actual generation prefix.

Teacher forcing presents earlier target tokens to the model. It exactly scores the declared token path, subject to numerical fidelity, but it does not measure how often the model independently reaches that path. A gold derivation can already supply the essential idea before the purportedly decisive line. A high probability for the last line then measures conditional continuation after assistance. Report at least these separately:

1. **Full-path score:** the complete declared realization, including actual interface wrappers and any represented reasoning/answer boundary.
2. **First contribution-bearing span:** a domain-annotated mechanism step with its exact preceding context. Name what target information the forced prefix already supplies.
3. **Downstream consequence span:** continuation after the mechanism has been supplied. This measures execution or continuation conditional on that mechanism.

Choose spans from the contribution analysis while blinded to scores. State semantic dependencies, not only token positions. If the proposed “first” span follows an equivalent formulation of the idea, relabel it as downstream; it is not evidence of where the idea originated. For a free-generation trace, its emitted first contribution-bearing span can be replayed and scored, but conditioning on a successful trace is outcome selection and the result remains descriptive.

For each event, prepare up to eight original reference realizations before confirmation: one concise valid construction; two materially different valid representations/paraphrases; one longer justification; two plausible matched errors; the nearest pre-freeze method where it is a meaningful control; and an optional domain-specific alternative. A reviewer certifies their labels. Record which realizations include the target mechanism and which solve the problem through another route. No target-paper paragraph is required or copied. Interfaces with thinking markers require complete declared serialization; do not score a target as if it were a final answer when the template actually puts it inside a reasoning block.

For matched controls, vary one substantive step while maintaining similar format and token length where feasible. Report actual lengths rather than pretending semantic counterparts have identical tokenization. A correct-versus-error log-likelihood difference is evidence of preference between these strings conditional on that prompt. Normalizing over a finite candidate set yields probability conditional on membership in that artificial set; it is not an unconditional probability of the idea and is not a creativity score. A first-token margin cannot stand for a multi-token mechanism.

Report raw full-sequence log likelihood, token count, byte count, mean log likelihood per token, and descriptive bits per UTF-8 byte where relevant. Raw likelihood measures a path; per-token normalization measures average predictability. Neither substitutes for semantic event probability. Longer strings contain additional probabilistic decisions, so a detailed correct proof can have much lower joint likelihood than a short vague assertion. Length-sensitive search is a recognized issue in sequence models, but applying a length reward changes the score and does not recover a missing semantic probability. [Murray and Chiang, *Correcting Length Bias in Neural Machine Translation*](https://aclanthology.org/W18-6322/).

A deterministic tokenizer maps a chosen text to one token sequence, whereas a model may emit other token segmentations decoding to the same bytes. Therefore the canonical encoding's score need not equal total probability of that text, much less of its meaning. Within this study retain the identical tokenizer and exact token paths. Across models, compare semantic sampling rates on the same scientific specification and expose tokenizer/interface differences; do not interpret different per-token likelihoods as a common probability scale.

If a finite set `S_i` consists of distinct, complete stopped token trajectories all certified as target recovery under the same prompt/law/budget, then

```text
sum_(y in S_i) q(y | x_i) <= pi_T,i.
```

This is a mass lower bound over enumerated valid paths. Use log-sum-exp and deduplicate token trajectories. Incomplete prefixes can overlap, and summing them double-counts continuations; only mutually exclusive events can be summed directly. The bound may be extremely small because unenumerated paraphrases and reasoning paths carry most mass. A small lower bound provides no upper bound. Curator-created paraphrases are a diagnostic library, not an unbiased sample of valid realizations. If `q != p`, a raw-`p` sum bounds raw-`p` mass only; score the decoder's processed conditional probabilities separately when a `q` bound is desired.

When expressed reasoning `R` precedes the final answer `A`, the target probability marginalizes over all possible reasoning paths and answer realizations:

```text
pi_T,i = sum_(r,a) q(r,a | x_i) * T_i(r,a).
```

Forcing one chosen reasoning trace and scoring `q(a | x_i,r)` does not perform that marginalization. Sampling complete trajectories is the proposed estimator. The initial study does not claim exact semantic probability from a finite paraphrase bank, beam search, or importance sampling. In particular, samples from truncated `q` cannot reconstruct raw `p` mass in excluded regions by reweighting: support is missing. A later rare-event estimator would need its own support, weight-variance, and validation study.

## 6. Sampling uncertainty, rarity, dependence, and selection

For one frozen event/prompt/decoder, draw `n=64` independent trajectories and count definite target recoveries `k`. Estimate `pi_T,i` by `k/n` and use binomial inversion for the interval. The proposed default is a two-sided 95% Clopper–Pearson interval for descriptive per-event tables, with the one-sided 95% upper bound stated separately when making a low-probability claim. Exact binomial inversion is implemented and documented by [R's `binom.test`](https://stat.ethz.ch/R-manual/R-patched/library/stats/html/binom.test.html) and [SciPy's `proportion_ci(method='exact')`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html). “Exact” concerns binomial coverage, not truth of the model, historical audit, or semantic labels.

With `k=0`, the one-sided upper bound at error level `alpha` is `U = 1 - alpha^(1/n)`, from `Pr(0 successes | pi) = (1-pi)^n`. The following values are calculations, not observed results:

| Independent samples for one event | Zero-success upper bound, one-sided 95% |
| --- | --- |
| 64 | 4.573% |
| 128 | 2.313% |
| 256 | 1.163% |
| 299 | 0.997% |
| 2,995 | 0.100% |
| 29,956 | 0.010% |

To make `U <= epsilon` after zero successes requires `n >= ceil(log(alpha)/log(1-epsilon))`. Consequently, this proposed budget cannot substantiate claims at probabilities such as `10^-3` or `10^-4`. Nor does a low exact-string probability substantiate them. “No recovery in 64 trials” is an observation, not “the model cannot have this idea” or “the idea has zero mass.” If rarity is the central scientific claim, choose `epsilon` and an affordable precision target before finalizing sample size; otherwise publish bounds at the precision the budget supports.

For simultaneous event-level rarity claims over twelve target endpoints, use a union-bound allocation such as `alpha_i = 0.05/12`. With zero successes at `n=64`, the corresponding one-sided upper bound is about 8.21% per event. Joint claims for both `T` and `V`, additional prompt conditions, models, or chosen thresholds must count those endpoints too. Per-event descriptive 95% intervals should be labeled nonsimultaneous. There is no default confirmatory significance hunt over layers, prompts, and novelty metrics.

For the fixed-corpus mean, a conservative interval is the weighted average of event-specific simultaneous lower and upper bounds, with an error allocation frozen for that family. Do not apply one pooled binomial interval to all completions as if all events shared the same `pi`. Do not bootstrap seeds as if they were independent scientific discoveries. Repeated prompts, sources, consequences, and common model/donor context belong to their event/paper clusters. Any claim about a wider event population requires a sampling frame and enough independent event/family units; twelve curated events cannot supply that by accumulating more seeds.

If `u` outputs have unresolved semantic judgments, report a sensitivity range: definite recoveries `k` through possible recoveries `k+u`. Lower uncertainty bounds based on `k` and upper bounds based on `k+u` make ambiguity visible, conditional on the adjudication procedure being reliable. Do not drop uncertain outputs from the denominator. Unknown chronology is different: an event with unresolved admission stays exploratory and its outputs do not enter the admitted historical summary.

An incomplete final proposal at the administrative cap is an observed failure within `B`, not missing data for that bounded endpoint. A cap stop after a complete valid final proposal can succeed under the frozen completion rule. Preserve both in the denominator and report cap/incompleteness rates, because extending `B` would define a different probability. Also report invalid/unsupported proposals, abstention, ordinary antecedent solutions, valid alternative mechanisms, and parse-only failures. An infrastructure failure is not a semantic failure: log the attempted run, repair without inspecting outcomes, and apply the frozen rerun policy. A proposed policy permits one exact-seed rerun after a documented crash, retains both records, and marks persistent failures missing; if missingness could depend on output content, bound or invalidate the affected estimate rather than assuming it is ignorable.

Stop each event at its fixed allocation. Do not sample failures until a success appears and report the same fixed-n interval, or stop early after an appealing interval. Time-uniform confidence sequences exist for valid optional stopping, but choosing one is a different registered design. [Howard et al., *Time-uniform, nonparametric, nonasymptotic confidence sequences*, 2021 journal article; arXiv v9](https://arxiv.org/abs/1810.08240v9). Operational termination for a broken stack or exceeded cap remains allowed; label incomplete allocation honestly and do not turn it into a success-based stopping rule.

A useful secondary search summary is oracle recovery at fixed `k <= n`: `1 - C(n-c,k)/C(n,k)`, where `c` is the number of successes among the independent samples. This is the pass-at-k estimator introduced in the code-model evaluation literature. It measures availability of an acceptable candidate if an oracle can recognize it; an actual selector can perform worse. Never equate it with unselected one-draw probability, and do not replace it by the biased plug-in formula without explanation. [Chen et al., Section 2.1 and Appendix A](https://arxiv.org/html/2107.03374v2).

Report model self-selection or expert selection only if a selection policy and its costs were prospectively specified; neither is identical to oracle pass-at-k. Duplicate candidates remain sampling trials here too.

Keep a selection ledger for every model, prompt, candidate, reference realization, annotation rule, and diagnostic tried. Confirmation failures do not authorize retuning that confirmation set. A revised decoder or rubric requiring outcome-based changes makes the affected data development material for a new study. The later intervention experiment must use a new confirmation population, not simply the observational events selected because their baseline failed and their guided condition succeeded.

## 7. Failure diagnostics with limited conclusions

The observational study should locate informative behavioural gaps before proposing a neural explanation. Run prerequisite questions in separate fresh contexts so administering them cannot teach the target continuation. Include recognition of the operation's applicability, assumptions/counterconditions, and simple execution, rather than only vocabulary recall. Retain every primary target in the main report regardless of prerequisite performance; a competence-defined stratum is secondary and must be specified before confirmation.

The proposed diagnostic allocation per confirmation event is sixteen short completions in total: four prerequisite probes with two independent seeds each, four P1 completions, and four P2 completions. These small samples supply case-level evidence, not precise assistance-effect estimates. P3 recognition, extra prompt paraphrases, practical-decoder comparisons, and longer-budget reruns require an explicitly reserved allocation or a separate exploratory phase. Do not silently exceed the cap by adding controls after seeing failures.

| Observed pattern | Supported diagnostic description | Remaining alternatives |
| --- | --- | --- |
| Prerequisites fail in fresh contexts | Knowledge/retrieval/execution weakness under those probes | Probe framing, unfamiliar format, numerical difficulty, and domain mismatch |
| P1 improves recovery | Recovery is sensitive to supplied historical knowledge | Additional context, curator's selection guidance, or extra task specification |
| P2 improves on P1 | Recovery is sensitive to a structural hint | The hint may supply the novel contribution, simplify search, or change compliance |
| Recognition/execution succeeds but P0 generation fails | Elicited execution is stronger than unaided production under this protocol | Recognition is easier, answer conditioning, search/format/budget effects |
| Target path scores well conditionally but target is not sampled | Some particular continuation is locally preferred after the given prefix | Prefix rarity, many other branches, earlier forced leakage, decoder support |
| Valid alternatives occur without target recovery | The model can solve the problem using other mechanisms | The target may be unnecessary, weakly prompted, or overly narrow as a recovery criterion |

These patterns do not identify mutually exclusive failure causes. A supplied prerequisite can both add knowledge and guide search. A model can answer a component probe but fail to retrieve/apply it in the target context. The event's finite sampling estimate bounds performance under a chosen elicitation policy; it does not locate a unique missing thought.

A prospectively controlled prompt intervention, with fixed model/decoder/budget and randomized or otherwise justified matched comparisons, can identify the behavioural effect of supplying that information on output recovery, with appropriate uncertainty. The small diagnostic allocation here usually provides only imprecise effect estimates. Such a behavioural causal effect still does not show which hidden computation mediated it. The restriction concerns inference from tensor/text correlations to an internal mechanism, not the possibility of causal inference about controlled prompt changes.

## 8. Expressed reasoning and read-only internal observations

Preserve raw reasoning and final output separately where the interface exposes them. Annotate explicit assumptions, first expressed target mechanism, errors, alternative routes, self-corrections, and contradictions. Score final validity and reasoning quality separately. No expressed reasoning is an honest observation if none is available; do not substitute a retrospective explanation generated after the answer as the original trace.

Expressed reasoning is a behavioural artifact, not a guaranteed account of internal computation. Work on biased explanations shows unacknowledged influences; work on truncating/editing CoT shows task-dependent dependence on the visible trace; and newer reasoning-model evaluations find incomplete verbalization of supplied hints. These results warrant caution, not a universal claim that every reasoning trace is unfaithful. [Turpin et al., 2023](https://arxiv.org/html/2305.04388v1); [Lanham et al., 2023](https://arxiv.org/html/2307.13702); [Chen et al., 2025](https://arxiv.org/html/2505.05410).

For the initial observational phase, capture only selected residual states and output statistics through non-mutating hooks. Proposed sites are residual outputs nearest one-quarter, one-half, three-quarters, and the final layer, with an exact integer mapping frozen for the chosen architecture. Capture the final problem-prefix position once per event/condition, then generated positions 1, 32, 128, and 512 for a preselected eight primary seeds per event where those positions exist. Missing positions due to early stopping are structural missingness, not fabricated zero states. Save raw vectors only at those sites, plus norms and token metadata; no all-token/all-layer attention or vocabulary-logit dumps by default.

A deterministic frozen model has the same state for the same exact prefix before sampling. Sixty-four independent seeds do not create sixty-four independent pre-answer states at that boundary. Later states differ because different earlier tokens have been sampled. State differences between P0, P1, and P2 can reflect changed inputs, positions, wording, or answer information; they cannot by themselves establish a latent bridge computation. Similar vectors on forced successful traces can encode the supplied target rather than its spontaneous construction.

Before interpretation, require capture-only/no-hook parity, finite states, exact prefix/token alignment, calibrated numerical tolerance, and full-prefix/cache replay agreement. Varying later teacher-forced text must leave earlier identical-prefix states unchanged within that tolerance. Each saved state records whether it precedes generated answer information, follows an emitted mechanism, or lies in an externally forced target trace. The latter is a supplied-text response, not evidence of unassisted idea formation.

An optional untrained logit-lens view applies the model's final normalization/readout to selected intermediate residuals and reports only nominated next-token diagnostics. It is a readout convention, not calibrated intermediate semantic probability. The tuned lens addresses some brittleness with separately learned affine translators, which are additional fitted objects. [Belrose et al., *Eliciting Latent Predictions from Transformers with the Tuned Lens*](https://arxiv.org/html/2303.08112). No lens training is part of this initial protocol. If a pre-existing compatible lens is later used, pin its provenance and treat it as a separate analysis.

Do not train a high-capacity probe on twelve confirmation labels and call successful classification a discovered representation. Future fitted probes need event-level holdouts, shuffled-label/control tasks, complexity accounting, and generalization checks. Probe research demonstrates why decoder capacity and memorization can mimic representation evidence. [Hewitt and Liang, *Designing and Interpreting Probes with Control Tasks*](https://aclanthology.org/D19-1275/). An observational association or readable feature still does not establish that the feature is causally used to produce the idea.

Activation patching, ablation, gradients for intervention selection, vector extraction, and perturbation sweeps are reserved for the later phase. That phase should specify transfer, no-op, different-answer, generic/answer/random controls, and new confirmation data. Patching research documents sensitivity to corruption methods and output metrics, so an attractive layer map alone is insufficient causal evidence. [Zhang and Nanda, 2023](https://arxiv.org/html/2309.16042v1); [Heimersheim and Nanda, 2024](https://arxiv.org/html/2404.15255v1).

## 9. Proposed feasibility budget and decision gates

Use the following upper allocations only if the events are admitted and the scientist approves the measured local feasibility. All output limits include reasoning, failures, and unsuccessful candidates.

| Allocation | Proposed size | Maximum output tokens at 2,048 each |
| --- | --- | --- |
| Development behaviour/decoder checks | 6 events × 16 samples | 196,608 |
| Primary confirmation | 12 events × 64 samples | 1,572,864 |
| Confirmation diagnostic allowance | 12 events × 16 completions total | 393,216 |
| Total generation ceiling | 1,056 completions | 2,162,688 |

This ceiling excludes neither unsuccessful outputs nor inconvenient events. It also does not price prefill, reference scoring, selected-state replay, CPU verification, adjudication, or storage. Account for those separately. Proposed initial scoring limits are at most eight reference realizations per event and one replay per selected captured trajectory. A separate runtime ceiling must be set from existing mechanics timing or a bounded development calibration; token count cannot guarantee GPU-hours. Exceeding a runtime cap creates an incomplete study, not permission to replace the declared denominator or increase the allocation silently. No paid jobs, model acquisition, or infrastructure changes are authorized by this document.

| Gate | Required evidence and action |
| --- | --- |
| G0 historical admissibility | Exact contribution/model chronology, precursor distinction, permitted inputs, and independent review. Unresolved cases remain exploratory; no admitted items means no historical confirmation claim |
| G1 measurement integrity | Exact rendered tokens/decoder, stop semantics, correct shifted log-prob scoring, verifier/rubric checks, capture parity, and reproducible reference path. Failure halts interpretation |
| G2 development feasibility | Coherent output, adequate context/length, attainable adjudication, usable checks, and measured cost. Change decoder/budget only here, then freeze |
| G3 confirmation completeness | Fixed event inventory, counts, seed schedule, custody, and all raw attempts retained. Unexpected outcome-dependent selection invalidates the affected confirmation claim |
| G4 observational report | T and V rates with explicit intervals/ambiguity; exact-string and span diagnostics labeled conditional; failure/alternative rates and costs included. Wide bounds support an inconclusive rarity result |
| G5 subsequent causal study | A specific mechanism hypothesis with selective predictions and justified practical value, plus a separately frozen intervention/split/budget protocol. Observational associations do not automatically open a sweep |

A valid target recovered from a temporally admitted model under P0 supports historical problem-conditioned recoverability. A target recovered only under P2 supports guided recoverability under declared assistance. Zero P0 successes supports the calculated finite-budget upper bound; it cannot establish that the model lacks the idea. Consistently valid alternative mechanisms may make a target-specific intervention scientifically less compelling even if `pi_T` is small.

## 10. Report record and unresolved scientist decisions

For each event retain: contribution and cluster IDs; admission/version history; source permissions; exact model/tokenizer/template/file identities; numerical/runtime condition; prompt and assistance label; token IDs and spans; decoder processors; stop and cap rules; sample IDs/seeds/order; full raw trajectories; per-token likelihoods for the declared reference paths; rubric/version/reviewer judgments and unresolved cases; selective tensor index and checksums; verifier results; all errors/reruns/exclusions; prefill/generated/scored tokens; forward-pass counts, GPU/CPU time, and peak memory/storage; development-selection ledger; and the preregistration/confirmation inventory digest.

Publish a per-event table before an aggregate: `n`, definite/possible `T`, definite/possible `V`, truncation, alternative solution classes, intervals, full-path scores with lengths, first-mechanism/downstream span conditions, and assistance sensitivity. Provide original summaries and links to primary sources rather than redistributing restricted benchmark or paper text. Archive the exact publicly retrievable source versions/metadata permitted by their licenses. Source and artifact hashes attest to byte identity, not scientific truth.

The scientist still needs to choose the actual novel contribution cohort and admission confidence; the historical model and full interface; P0 versus explicitly assisted reconstruction where historical problem framing is uncertain; primary decoder and attainable output budget; practical rarity threshold and precision target; independent domain reviewers and their time budget; event weights and wider-population ambition; runtime/storage caps; and the scientific consequence that would justify a later intervention. The proposed six/twelve events and 64 samples are a small observational starting point, not an automatic resolution of those choices.

Source verification for this protocol used the linked primary papers, publisher/proceedings pages, and official statistics documentation on 11 October 2026. CUSP's auditor exemption was also located in the directly fetched v2 HTML after the browser's extracted text omitted that block. The original Clopper–Pearson DOI page and Holm JSTOR page did not provide readable full text, so no argument here relies on their inaccessible contents; binomial coverage is supported by inspected official implementations and the zero-success/union-bound calculations are stated explicitly. No dataset or weight corpus was acquired and no probability, human-review performance, or internal-mechanism result was measured.
