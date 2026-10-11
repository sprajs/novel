# Exploratory casebook: later human research contributions

Prepared 11 October 2026 from bounded primary-source searches. **All six cases are `exploratory`, `development`, publicly exposed, and unadmitted.** These are AI-assisted candidate analyses and original draft problems; no independent human domain/provenance review, model execution, or scientific validation occurred. Human-authored publications supply attributed leads. Idea-level human origin and any disclosed AI assistance still require review.

The [corpus protocol](corpus-protocol.md) defines admission gates and independent human review. The older [MeanFlow](../docs/ground_truth/packets/meanflow.md) and [DPO](../docs/ground_truth/packets/dpo.md) equation packets remain calibration material. Here their proposed target is a later method contribution. Getting their old calculus/algebra right cannot establish recovery of that contribution.

## Proposed historical pairings

These exact pins come from the existing [checkpoint audit](../docs/ground_truth/model_audit.md), not newly acquired weights. Public-availability evidence still needs independent historical corroboration. Dates below are recorded repository events and publisher release leads, not independently established first-visibility instants. All competence and local feasibility are unmeasured.

| Pair shorthand | Exact full snapshot | Recorded complete-revision event | Interface condition |
| --- | --- | --- | --- |
| P14 | `EleutherAI/pythia-1.4b` at `8f0af839162ddb466006494a08733ee9cfa2d338` | 2023-04-03 18:33:31 UTC | Base model; original `.bin`, co-located tokenizer; no later instruction tuning or chat template |
| P28 | `EleutherAI/pythia-2.8b` at `f20536c52a97faea73b8997cc789bd913853f14a` | 2023-04-03 18:51:39 UTC | Same historical suite and restrictions; greater capacity is not proven competence |
| Q17 | `Qwen/Qwen3-1.7B` at `d3e258980a49b060055ea9038dad99d75923f7c4` | 2025-04-29 08:55:53 UTC | Original April weights, post-trained model, April tokenizer/template; thinking argument must be fixed |
| Q06 | `Qwen/Qwen3-0.6B` at `6130ef31402718485ca4d80a6234f70d9a4cf362` | 2025-04-29 08:56:31 UTC | April tokenizer/template; smaller fallback only after prerequisite assessment |

The [April 4 Pythia README revision](https://github.com/EleutherAI/pythia/blob/ceb8e5234db499def6759c54195cd87f465cfb3d/README.md) reports the April 3 replacement-suite release; [Qwen's publisher announcement](https://qwenlm.github.io/blog/qwen3/) is dated April 29, 2025. Full file identities and template hashes reside in the model audit. No guessed training cutoff is used. Later Qwen revisions are ineligible for the April interface condition even when weights match; Pythia-v0 or moving final-step branches cannot substitute for P14/P28.

| Case ID | Domain | Known v1 submission record | Proposed pair | Main unresolved contribution boundary |
| --- | --- | --- | --- | --- |
| `dpo-policy-design-2023` | CS / preference learning | 2023-05-29 17:57:46 UTC | P14 or P28 | Policy-only preference optimization beyond old exponential-tilt and preference algebra |
| `meanflow-training-design-2025` | CS / generative modeling | 2025-05-19 17:59:42 UTC | Q17; Q06 fallback | Average-field training design beyond old calculus and earlier one-step methods |
| `weighted-mincut-clustering-2024` | CS / algorithms | 2024-01-11 02:48:23 UTC | P28; P14 calibration | Weighted clustering/proof ingredients beyond 2021 almost-linear mincut |
| `granular-odd-elasticity-2023` | Physics / driven matter | 2023-11-30 17:20:04 UTC | P28 or P14 | Microscopic granular realization beyond the 2019 odd-elasticity theory |
| `multishape-inverse-design-2023` | Engineering / mechanisms | 2023-04-24 14:29:52 UTC | P28 or P14 | Sequential nonlinear multishape design beyond older multimode materials |
| `amm-dynamic-fees-2025` | Finance / microstructure | 2025-06-03 13:34:28 UTC | Q17; Q06 fallback | Optimal fee-control structure beyond dynamic-fee and inventory-control antecedents |

Every table date is an archive **submission** timestamp, used as a known channel to investigate. It is not certification of first public disclosure. Earlier talks, preprints with other titles, proceedings, code, theses, patents, and equivalent contributions remain open. These examples cannot become sealed confirmation by removing titles or changing surface wording.

## Prompt provenance and feasible outcome scope

None of the drafts below is an admitted `P0 historical_problem`. They were written after inspecting future targets and therefore carry hindsight problem-framing assistance. Removing names does not remove that assistance. Each needs an independent pre-event basis for its problem constraints or must be labeled a supplied-prerequisite/strategy reconstruction condition (`P1`/`P2`) in [the measurement protocol](measurement-protocol.md). In particular, rollout avoidance can direct the DPO design, teacher-free one-step transport narrows MeanFlow's design space, polylogarithmic deterministic weighted mincut identifies a research milestone, cycle-work plus granular surface design narrows a physical mechanism, multiple finite patterns direct the engineering construction, and fee-sensitive arrivals plus a price penalty can reveal the finance model. None is declared leakage-safe merely because it is anonymized or paraphrased.

The proposed output budget is at most 2,048 tokens including reasoning and final answer, with a lower available output budget when the prompt occupies an older model's context window. No draft has been tokenized or tested on these models. The intended short output is a scoped mechanism/design, critical justification and assumptions; empirical success remains a separate evidence claim. A missing necessary proof or experiment yields unvalidated/unknown validity, not an automatic scientific pass.

| Case | Initial feasibility and stop criterion |
| --- | --- |
| DPO | A compact objective/learning design may fit; fresh-context algebra, likelihood, support and gradient probes still must establish prerequisite competence. Stop if the design reduces to the old cancellation fixture |
| MeanFlow | A compact representation/objective/endpoint rationale may fit; JVP, flow and training-target competence are unknown. Stop if the hard training idea is supplied or only the old derivative identity is judged |
| Weighted mincut | **Deferred audit stress case, not a generation-pilot candidate.** An expert must isolate a meaningful new lemma-sized idea and adequate short justification. A generic outline cannot count as theorem recovery; stop if meaningful novelty requires the full long proof |
| Granular mechanism | A mechanism and discriminating experiment plan may fit; continuum/contact reasoning competence is unknown. Treat unperformed simulation/laboratory results as unvalidated, and stop if broad odd-elasticity terminology substitutes for a physical mechanism |
| Multishape design | Needs a complete independently authored geometry/pattern packet and nonlinear-compatibility competence. Stop if diagram/context requirements exceed the pin or if a generic solver slogan replaces a concrete compatible construction |
| AMM fees | Needs a complete model or an explicitly open model-design rubric and stochastic-control competence. No unique-result label without fixed arrival laws/penalties; stop if the result is just an older inventory-control first-order condition |

A development competence floor and human review capacity can make only one or two cases feasible, or none. Keep all exclusions in the selection ledger; do not silently replace difficult contributions with checker-friendly prerequisites or fill domain quotas.

<a id="dpo-policy-design-2023"></a>

## 1. DPO as policy design, not normalizer cancellation

**Case ID:** `dpo-policy-design-2023`. **Target:** construct an offline policy-training method from paired preferences and a reference policy, using the reward/policy relationship to define a preference likelihood in policy parameters and avoid a separately trained reward plus an on-policy RL loop. Account for assumptions, support, identifiability, and optimization limitations. Exclude the claim that this method reproduces particular empirical preference or benchmark gains.

**Dated evidence.** [Rafailov et al., v1 record](https://arxiv.org/abs/2305.18290v1) gives 29 May 2023, 17:57:46 UTC. [V1 Sections 4–5 and Appendix A](https://arxiv.org/html/2305.18290v1) provide the policy reparameterization and training design. P14/P28 precede this recorded channel, conditional on release and earlier-disclosure review. Qwen3 cannot support a 2023 reconstruction claim. V1 is the source boundary; the record also has later versions, whose additions must not be imported into this case.

**Old components and precursor search.** The exponential policy tilt is already in [AWR v1](https://arxiv.org/abs/1910.00177v1), submitted 1 October 2019, and earlier relative-entropy policy search; Bradley–Terry paired comparisons are much older. The existing packet documents these prerequisites. The residual candidate is their use as a direct policy-fitting design, not invention of either equation. Search pre-May-2023 inverse/preference-based RL, direct policy learning, dueling-bandit objectives, reward-weighted regression, and author talks/OpenReview/code. These are incomplete audit leads, not a finding that the residual method had no equivalent predecessor.

**Neutral problem draft, original and unvalidated:**

> You have an offline collection of prompt/completion pairs with a preferred completion in each pair, a strictly positive reference policy, and access to completion log probabilities and gradients. Design a regularized method that learns a policy from these data while limiting expensive fresh rollouts. State the preference assumptions, the objective and update, what is identified, and where your method can fail. Give a validation plan that distinguishes an algebraic reduction from successful learning.

The final packet must state the reward/KL/preference assumptions explicitly and identically across conditions. Hindsight selection of those old ingredients is assistance. Supplying the rearranged log-ratio reward or final policy-only loss would reveal the essential reduction.

**Human judgment and alternatives.** Give separate validity and target-recovery verdicts. A target-equivalent answer needs a coherent policy-only likelihood/objective, rationale, and support/identifiability conditions; cancellation alone is incomplete. A valid direct-ranking, constrained optimization, or other offline preference method can earn alternative-solution credit if its assumptions and regularization meet the problem. An ordinary separate reward/PPO pipeline may solve a broader preference problem but does not recover this target. Do not infer equal training dynamics or preference superiority from an optimum identity. Experts should inspect distribution shift, reference zeros, finite-model misspecification, and shared context offsets; small exact examples support only these local checks.

**Blockers and rights.** Independent novelty/temporal reviews, earlier equivalent-policy objectives, actual historical artifact visibility, complete neutral premise packet, and old-model competence remain unresolved. V1 displays CC BY 4.0. Preference datasets and implementation rights are separate and uninspected; none is uploaded. The current draft is a research-design task, not an executable derivation benchmark or validated rediscovery item.

<a id="meanflow-training-design-2025"></a>

## 2. MeanFlow as a generative training design

**Case ID:** `meanflow-training-design-2025`. **Target:** propose an interval-conditioned average-velocity generative field, a self-contained derivative-based training objective connecting it to an instantaneous flow, and a single learned displacement step; analyze endpoint regularity and approximation limits. This proposed scope must survive comparison with earlier flow-map and one-step training designs. Exclude a claim of newly invented product/material-derivative calculus or reproduced image-quality results.

**Dated evidence.** [Geng et al., v1 record](https://arxiv.org/abs/2505.13447v1) gives 19 May 2025, 17:59:42 UTC. [V1 Sections 4.1–4.3 and Appendix B](https://arxiv.org/html/2505.13447v1) motivate the field, derivative-based target, and network training. Q17/Q06 precede that channel with their original April interfaces. A later July tokenizer cannot inherit April eligibility. The unresolved earlier-public-channel audit still blocks the pairing.

**Old components and precursor search.** Calculus and trajectory averaging are old; the existing packet shows why boundedness at coincident endpoints matters and why a local identity alone does not establish the learned flow. [Shortcut Models v1](https://arxiv.org/abs/2410.12557v1), submitted 16 October 2024, already has step-size-conditioned, single-phase generation. [Inductive Moment Matching v1](https://arxiv.org/abs/2503.07565v1), submitted 10 March 2025, is another earlier single-stage few-step approach. Compare exact objectives and representation choices, consistency models, flow-map learning, and earlier author code/talks. “One-step without distillation” alone is an inadequate novelty boundary.

**Neutral problem draft, original and unvalidated:**

> Samples from an unknown data distribution and samples from a simple source distribution are available. You may use a specified differentiable interpolation and its conditional velocity during training. Propose a model and training method that can transport a source sample to data with one network evaluation, without a pretrained teacher. Explain the representation, supervision, endpoint behavior, and tests needed to establish distributional accuracy.

The complete packet must fix the interpolation and accessible training quantities without supplying the average-field parameterization, target identity, stopped-gradient regression target, or named precursor selection. These could be scaffold conditions but not an unguided problem. The teacher-free design constraint is hindsight framing, recorded explicitly.

**Human judgment and alternatives.** Target recovery requires the interval-average representation, an internally coherent trainable objective and sample step, and correct treatment of derivative paths/boundaries. A correct interval identity with no usable training rule earns prerequisite credit. A different teacher-free one-step method earns valid-alternative credit only under its stated assumptions; if it reproduces an older shortcut/consistency design, label that earlier equivalence separately. Reviewers should assess circular targets, stop-gradient choices, computable Jacobian-vector products, singularities, and why training might approximate the desired transport. Toy ODE and small-distribution checks are supporting tests. Published ImageNet/FID claims require separate experiments and cannot be inferred from symbolic correctness.

**Blockers and rights.** Independent human novelty and temporal review, earlier equivalent flow-map objectives, release-visibility corroboration, a complete pre-disclosure input packet, capability, and empirical validation remain open. V1 displays CC BY 4.0; the existing packet records MIT author code, without clearing ImageNet or model/data dependencies. No code or training data are copied here.

<a id="weighted-mincut-clustering-2024"></a>

## 3. Weighted mincut: an algorithmic proof contribution

**Case ID:** `weighted-mincut-clustering-2024`. **Disposition:** deferred audit stress case, excluded from the initial generation pilot pending expert delimitation. **Target:** develop the weighted-graph clustering/contraction and local-flow proof ingredients needed to upgrade deterministic almost-linear global mincut to a near-linear algorithm with polylogarithmic overhead. Require an explicit approximation/error budget and constructive complexity argument. The exact lemma-sized target and computational model need expert delimitation before admission; a generic algorithm outline cannot count as theorem recovery.

**Dated evidence.** [Henzinger, Li, Rao and Wang, v1 record](https://arxiv.org/abs/2401.05627v1) gives 11 January 2024, 02:48:23 UTC and identifies SODA 2024. [V1 introduction and Sections 3–6](https://arxiv.org/html/2401.05627v1) distinguish weighted clustering, recursion error, and tree-packing/local-flow ingredients. The archive channel follows P14/P28. An earlier accepted-paper listing, conference manuscript or author talk may move the boundary; those channels are unverified here.

**Old components and precursor search.** [Li's almost-linear weighted mincut v1](https://arxiv.org/abs/2106.05513v1) is a 2021 precursor, not a 2024 contribution. The target also compares older simple-graph clustering, Karger tree-packing and randomized methods. A generic claim to deterministically find a weighted mincut is therefore old. Search SODA submission/accepted-paper pages and authors' pages before January 2024; compare 2021 weighted and 2019/2020 simple-graph techniques. The bounded exact-title/date-filter search did not establish the absence of an earlier release.

**Neutral problem draft, original and unvalidated:**

> Consider an undirected graph with positive edge weights. Available baselines are a randomized near-linear global-mincut method, deterministic near-linear methods for simple graphs, and a deterministic weighted method with subpolynomial overhead. Develop a deterministic route to polylogarithmic overhead for weighted graphs. Specify the graph reduction, the guarantee it preserves, accumulated error, and operation count; identify any lemma still requiring proof.

The final packet must specify weight representation, parallel edges, arithmetic/bit complexity, and permitted baseline lemmas. Supplying the target clustering lemma or particular tree-packing construction as a premise would transfer the main contribution into the prompt.

**Human judgment and alternatives.** Target-equivalent proposals need substantive weighted clustering/recursion ideas and justified guarantees, not a pseudocode slogan. Accept another deterministic near-linear route as a valid alternative only with an expert-checked proof and cost model. An older almost-linear method is useful but fails the stated improvement; randomized sampling violates the requested guarantee. Small graph enumeration can find counterexamples to a proposed contraction, but cannot establish universal approximation or asymptotic complexity. A theoretical-algorithms expert must examine heavy-edge cuts, disconnected inputs, contraction safety, recursively compounded error, and all calls hidden inside complexity notation.

**Blockers and rights.** This is the least plausible small-model first case: the paper is 60 pages and the target may not reduce to an independently meaningful short contribution. Human scope review, sufficient premise curriculum, expert proof workload, earliest conference/talk channels, and model competence are unmeasured. V1 links CC BY 4.0; no paper/proof text is redistributed. Do not replace the research contribution with a trivial mincut numeric example merely to obtain a checker.

<a id="granular-odd-elasticity-2023"></a>

## 4. Driven granular matter: a microscopic mechanism for odd response

**Case ID:** `granular-odd-elasticity-2023`. **Target:** propose and justify a microscopic granular design in which chiral contact friction plus oscillatory drive yields a reproducible time-averaged elastic response with an antisymmetric component; specify how to distinguish that response from transient rotation, plasticity, and ordinary dissipative hysteresis. Exclude invention of odd elasticity in general and the paper's detailed defect/force-chain phenomenology.

**Dated evidence.** [Huang, Mandal, Scheibner and Vitelli, v1 record](https://arxiv.org/abs/2311.18720v1) gives 30 November 2023, 17:20:04 UTC. [V1 model and Supplement S1–S2](https://arxiv.org/html/2311.18720v1) describe the contact/drive construction and measurement procedure. P14/P28 predate that channel, while public talks, supplementary media and earlier versions remain unresolved.

**Old components and precursor search.** [Odd elasticity v1](https://arxiv.org/abs/1902.07760v1) was submitted 20 February 2019. Odd-elastic constitutive tensors, active spinners and chiral materials are established antecedents. [A granular-ratchet v1](https://arxiv.org/abs/cond-mat/0306640v1) dates to 25 June 2003; rectifying drive is not itself a new idea. Search contact friction/ratchet models, pre-2023 odd granular response, active-crystal experiments, and author talk/supplement histories. The relevant residual is the granular micro-to-continuum realization and its validity conditions, not permission to write a nonsymmetric tensor.

**Neutral problem draft, original and unvalidated:**

> Design a dense two-dimensional granular material whose coarse-grained stress response can perform signed work over a small closed strain cycle after reaching a driven steady state. The particles may have designed contact surfaces and the experiment may supply periodic mechanical energy. Explain the microscopic ingredients, symmetry and energy accounting, and a measurement protocol that separates a linear effective response from contact rearrangement and transient effects.

This task is a mechanism proposal, not deduction of an unprovided molecular-dynamics result. Do not supply the ratchet friction law, spinning outcome, or measured modulus. Surface design and external drive are available design freedoms; their hindsight selection must be disclosed.

**Human judgment and alternatives.** Target equivalence requires a contact-level chiral rectification mechanism under periodic shear and a defensible coarse-graining/measurement argument. A valid alternative using active torque, feedback or another energy source may satisfy the engineering goal while reproducing an older mechanism; record both labels. A nonsymmetric tensor with no realizable contacts is insufficient. Experts should assess stationary contacts, time-scale separation, probe amplitude, torque balance, dissipative versus quasistatic cycle work, chirality reversal and zero-drive controls. Simulation can test predictions under an agreed model; it cannot by itself establish robust laboratory realization or eliminate every constitutive alternative.

**Blockers and rights.** Human microscopic-mechanism/prior-art review, neutral specification, measurement validity, earlier talks/media, and historical model competence remain open. V1 displays CC BY 4.0. Simulation code/data/supplement rights were not cleared. No experiments or simulations are performed and no movies/figures are uploaded.

<a id="multishape-inverse-design-2023"></a>

## 5. Multishape inverse design: an engineering procedure

**Case ID:** `multishape-inverse-design-2023`. **Target:** design a sequential nonlinear local-constraint procedure that realizes several specified finite-deformation modes in one bar-and-hinge metamaterial while retaining compatibility of prior modes; diagnose unavoidable or likely spurious modes. Exclude invention of multimode metamaterials and any universal success-rate claim.

**Dated evidence.** [Dykstra and Coulais, v1 record](https://arxiv.org/abs/2304.12124v1) gives 24 April 2023, 14:29:52 UTC, about three weeks after P14/P28's recorded uploads. [The versioned HTML](https://arxiv.org/html/2304.12124v1) describes sequential nonlinear local design and additional modes, but renders an internal dateline of **24 August 2026** despite its v1 header. The arXiv submission record dates the archive event; this rendering discrepancy must be resolved against the originally deposited content before technical/version certification.

**Old components and precursor search.** [Oligomodal metamaterials with multifunctional mechanics](https://www.pnas.org/doi/10.1073/pnas.2018610118), published in 2021, is a close primary precursor. The target bibliography also contains earlier multi-shape, topology-optimization, origami and zero-energy-mode design. Compare exact finite-deformation constraints and sequencing to earlier work; look for author theses, repository history, conference slides and institutional announcements before April 24. The short Pythia-to-paper gap makes an earlier public manuscript especially consequential.

**Neutral problem draft, original and unvalidated:**

> A planar bar-and-hinge lattice must accommodate three specified finite-deformation patterns using one fixed geometry. Propose an inverse-design algorithm that makes the patterns compatible across neighboring cells. State what is fixed and adjustable, how constraints are solved, how earlier feasible modes are retained, and how you would detect extra modes, self-intersection, or sensitivity to elastic hinges.

The complete packet needs original target patterns and mechanical constraints. Do not provide the target's sequential construction, figures or numerical success rate. “Three patterns” defines the design task; choosing them or their representation after reading the target remains assistance.

**Human judgment and alternatives.** Target recovery requires a concrete nonlinear local-constraint algorithm and credible preservation/compatibility reasoning. A simultaneous nonlinear optimization or other realizable design can earn valid-alternative credit; assess whether it simply recovers an older design approach. Merely superposing linear zero modes does not establish finite-deformation compatibility. Experts should examine constraint count, over/underconstraint, closed-loop compatibility, boundary conditions, unwanted mechanisms, collisions, stiffness regularization, and manufacturability. Exact kinematic checks and finite-element tests support a stated geometry and range; they do not prove a general success rate or physical robustness.

**Blockers and rights.** Original-version content reconciliation, earlier public channels, older equivalent construction, human mechanism-design review, independent geometry/elastic validation and Pythia competence remain unresolved. V1's record links [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/); its noncommercial/share-alike terms differ from several other leads. This casebook contains original analysis and links, not adapted author diagrams or uploaded paper content. Code/data terms remain uninspected.

<a id="amm-dynamic-fees-2025"></a>

## 6. Dynamic AMM fees: a stochastic-control contribution

**Case ID:** `amm-dynamic-fees-2025`. **Target:** formulate an economically coherent controlled fee policy for a constant-function market maker with price-sensitive order flow, derive or justify tractable state-dependent policies, and explain when deterrence versus attracting flow changes the preferred fee. A generic inventory-sensitive fee or an isolated first-order condition is not the contribution. Require assumptions and approximation/error limitations; exclude real-market optimality or guaranteed LP profit.

**Dated evidence.** [Baggiani, Herdegen and Sánchez-Betancourt, v1 record](https://arxiv.org/abs/2506.02869v1) gives 3 June 2025, 13:34:28 UTC. It also lists v2 on 24 June 2025 and v3 on 30 July 2026. [V1 Sections 2–5](https://arxiv.org/html/2506.02869v1) supply the controlled-arrival model, fee objective and approximate policy analysis. Q17/Q06 precede the v1 archive channel. Current v3 claims cannot inherit that timing without version comparison.

**Old components and precursor search.** Dynamic fees are already considered in [Sabate-Vidales and Šiška's publisher record](https://link.springer.com/chapter/10.1007/978-3-031-32415-4_15), first online 22 July 2023, for FC 2022 workshops. Earlier conference/preprint/code channels may precede that date. The [authors' official code repository](https://github.com/msabvid/cpm_agent_based_sim) is another search lead, whose mutable head does not date release. Inventory-dependent market-making control, Avellaneda–Stoikov, static optimal AMM fees and earlier stochastic games require claim-level comparisons. These antecedents make “adjust fees using inventory/price” too broad.

**Neutral problem draft, original and unvalidated:**

> A constant-product pool competes with an external price venue. Fees affect how often informed and noise traders arrive, and trades change inventory. Design a fee-control model that balances collected fees against a specified penalty for pool-price deviation. State the arrival and price assumptions, derive a defensible policy or approximation, and explain tests that could distinguish protecting against informed flow from encouraging beneficial flow.

Arrival laws and penalties must be fixed before asking for a unique optimal formula. As written this is a model-design problem permitting declared assumptions; it does not have a unique fee answer. Final admission must choose that scope or supply an independently sourced fixed model. Supplying the target's particular exponential intensity and ansatz is potential scaffold leakage, not neutral background.

**Human judgment and alternatives.** Target equivalence requires coherent controlled dynamics, an objective, a justified state-dependent policy/approximation, and credible regime reasoning. A different control or market design can earn valid-alternative credit; familiar inventory-control rules remain earlier-method equivalents. Reviewers should inspect incentives, fee signs/bounds, inventory boundary conditions, exogenous-price assumptions, finite-horizon/terminal conditions, risk penalties, routing/endogenous arrivals, and approximation stability. An HJB residual or simulation under the author's chosen intensities supports mathematical consistency, not empirical economic adequacy. Static fees can be a valid baseline; they do not recover the dynamic contribution.

**Blockers and rights.** Human economic-model/prior-art review, earlier preprint/talk/code channels, model choice and assumption sufficiency, release visibility, and finite-horizon/robustness tests remain open. V1 displays CC BY 4.0; underlying market data/code licenses are uninspected. No financial recommendation, trading decision or real-money experiment is made here.

## Bounded search and adverse evidence

Access date for all new web research above is 11 October 2026. Primary abstract/version histories and relevant public HTML sections were inspected through the browser. No full papers, weights, datasets, code archives or paid sources were downloaded or uploaded. Consequently, no source-content hash is asserted. Existing model artifact hashes are explicitly inherited from the repository audit and are not evidence of new acquisition.

| Search/inspection | Outcome and limitation |
| --- | --- |
| Exact target titles; arXiv v1 records and HTML | Dates and attributed contribution leads located; not an exhaustive first-disclosure audit |
| `Deterministic Mincut in Almost-Linear Time` and exact 2024 title with a pre-January-11 date filter | 2021 antecedent identified; latest-page indexing can show a 2026 revision. Original v1 must define the comparison; no earlier-target absence proven |
| `One Step Diffusion via Shortcut Models`, `Inductive Moment Matching` | Original v1 records give 2024 and March 2025 antecedents; mathematical equivalence remains for human review |
| `granular ratchet odd elasticity` with a pre-April-2023 filter | Earlier ratchet and odd-elasticity mechanisms located; their exact equivalence to the granular realization remains unreviewed |
| `Oligomodal metamaterials with multifunctional mechanics` | Publisher primary precursor located; engineering v1 HTML dateline conflict remains unresolved |
| `Sabate-Vidales fees`, `The case for variable fees in constant product markets` | Publisher and author-code leads located; workshop year, online date, preprint and commit/public-visibility dates must be distinguished |
| `Automated Market Making and Arbitrage Profits in the Presence of Fees` | [May-24-2023 v1 record](https://arxiv.org/abs/2305.14604v1) appears to follow April Pythia, but [v1 title page](https://arxiv.org/html/2305.14604v1) states an initial version of **6 February 2023**. That date is not itself proof of public disclosure, but blocks a simple May-date admission pending visibility/content review. Its bibliography also credits earlier scaling/conjecture results. It is not one of the six proposed pairs |
| `In-memory mechanical computing` | An attempted PMC page produced a browser-check screen. It supplied no affirmative full-text/version evidence and was not retained as a candidate |

Search results from secondary aggregators were used only as leads to primary material, never as admission evidence. Source observations and proposed reviewer criteria are separate: neither an expert rubric draft nor agreement among AI workers means an expert completed the review. The next deliverables are signed human gate assessments and fully specified neutral input packets; the present corpus contains zero admitted cases.
