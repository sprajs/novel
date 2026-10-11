# Candidate survey for historical reconstruction

Prepared 11 October 2026. Machine-readable companion: [candidate_registry.json](../../data/ground_truth/candidate_registry.json). The survey follows [the research plan’s historical admission rule](../../Plan/research-plan.md): the **actual immutable checkpoint, including post-training, must have been publicly released before the earliest disclosure of the exact contribution**. A training cutoff, manuscript year, journal date, mutable model tag or private commit timestamp cannot substitute for that evidence.

**Five candidates deserve priority audits: MeanFlow’s average-velocity identity, DoRA’s normalized low-rank construction, DPO’s pairwise normalization cancellation, SSD’s block decomposition and DeltaNet’s compact-product chunk algorithm. None is admitted or certified historically novel.** MeanFlow is the most convenient recent algebraic option. Scalar speculative correction has a strong finite-probability verifier but is excluded as a 2022 novelty claim because a directly verified 2017 maximal-coupling equivalent exists. SSD and DeltaNet broaden the mechanism beyond cancellation. DPO and DoRA remain useful anchors for packet development while the antecedent and immutable-model audits proceed.

The survey contains 20 actual leads, not 20 independent discoveries. Related sampler and low-rank entries are retained because they have different verification targets or materially different disclosure obstacles. The ambitious AlphaTensor/AlphaEvolve certificates provide a mathematics contrast; AlphaDev offers a non-neural small-program target. The hat monotile records why a famous mathematical result can be unsuitable for this initial assay. The selected scalar speculative residual law, generic LoRA merging, FlashAttention merging and rotated-coordinate SOAP claims are excluded for specified reasons.

These are investigator-selected leads from literature research. No model was downloaded, no inference or hint-response screening was performed, and no source-provided program was executed. Proposed A/B pairs, bridge cues and verifiers are **design sketches**, not tested packets or evidence of prerequisite competence. Hindsight selection of A/B is human assistance and must be reported. A successful future hint response cannot retroactively establish eligibility, novelty or a useful intervention.

## What the dates and scores mean

An arXiv v1 submission-history date is a verified manuscript metadata date and a useful provisional boundary. It is not a complete first-public-disclosure audit; moderation/announcement timing, earlier equivalent results and other channels can change the boundary. Dates below remain provisional unless the stated primary channel is a dated public announcement. `null` in the registry means unresolved. For a disqualified attribution, the relevant earlier equivalent source may supply the date instead of the later named paper.

The distinction changes actual choices. AlphaEvolve’s rank-48 result was announced on **14 May 2025**, before its **16 June 2025** arXiv v1. AlphaDev’s June 2023 announcement links an LLVM review dating to **24 January 2022**; the initial diff still needs comparison with the exact selected shortcut. SOAP cites a 2020 work, but the equivalent eigenbasis correction was directly verified here in its **5 March 2021 v2**, not assumed to have appeared in its February 2020 v1. A FlashAttention first-release commit dated 20 May 2022 is a separate audit lead supplied by the parallel temporal audit; its public visibility is unproven. [AlphaEvolve announcement](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/), [AlphaEvolve v1](https://arxiv.org/abs/2506.13131v1), [AlphaDev announcement](https://deepmind.google/blog/alphadev-discovers-faster-sorting-algorithms/), [LLVM review](https://reviews.llvm.org/D118029), [earlier optimizer v2](https://arxiv.org/pdf/2002.09018v2).

Five ordinal dimensions range from 0 (weak), through 1 (mixed/unknown), to 2 (favorable): deducibility (D), verifiability (V), temporal separation (T), novelty isolation (N) and prerequisite feasibility (P). Total is their unweighted sum out of 10, used only to make tradeoffs visible. Status and hard admission gates take precedence; a rejected easy identity can score above a difficult but meaningful theorem. T describes a possible release-era family window, not an eligible revision. N=2 means the target contribution is well specified; it does not assert an exhaustive absence of antecedents.

| Candidate | Status | D/V/T/N/P | Total | Provisional relevant date |
| --- | --- | --- | --- | --- |
| [MeanFlow average-velocity identity](#meanflow) | PRIORITY — pending audit | 2/2/2/1/2 | 9/10 | 2025-05-19 |
| [DoRA normalized low-rank direction and radial separation](#dora) | PRIORITY — pending audit | 2/2/1/1/2 | 8/10 | 2024-02-14 |
| [Direct Preference Optimization normalization cancellation](#dpo) | PRIORITY — pending audit | 2/2/1/1/1 | 7/10 | 2023-05-29 |
| [Mamba-2 SSD block decomposition](#ssd) | PRIORITY — pending audit | 2/2/1/1/1 | 7/10 | 2024-05-31 |
| [Parallel DeltaNet through compact rank-one products](#deltanet-wy) | PRIORITY — pending audit | 1/2/1/1/1 | 6/10 | 2024-06-10 |
| [Factored norms for high-rank DoRA](#dora-factored-norms) | AMBIGUOUS | 2/2/2/0/2 | 8/10 | 2026-03-23 |
| [AlphaDev small-sort conditional-copy shortcut](#alphadev-sort3) | AMBIGUOUS | 2/2/0/1/2 | 7/10 | 2023-06-07 |
| [Speculative sampling with shared exponential races](#exponential-race-speculation) | AMBIGUOUS | 2/2/1/0/2 | 7/10 | 2025-04-21 |
| [Frozen-factor low-rank adaptation activation gradient](#lora-fa) | AMBIGUOUS | 2/2/1/0/2 | 7/10 | 2023-08-07 |
| [AlphaEvolve rank-48 complex matrix multiplication certificate](#alphaevolve-rank48) | AMBIGUOUS | 0/2/2/2/0 | 6/10 | 2025-05-14 |
| [Conditional-to-marginal flow-matching gradient equivalence](#flow-matching) | AMBIGUOUS | 2/2/1/0/1 | 6/10 | 2022-10-06 |
| [Causal minibatch TTT-Linear dual form](#ttt-dual) | AMBIGUOUS | 2/2/1/0/1 | 6/10 | 2024-07-05 |
| [AlphaTensor rank-47 GF(2) matrix multiplication certificate](#alphatensor-rank47) | AMBIGUOUS | 0/2/1/2/0 | 5/10 | 2022-10-05 |
| [Stochastic Beam Search without-replacement sequence sampling](#gumbel-topk-sequences) | AMBIGUOUS | 1/2/0/1/1 | 5/10 | 2019-03-14 |
| [Schedule-Free online-to-batch interpolation theorem](#schedule-free) | AMBIGUOUS | 1/1/1/1/1 | 5/10 | 2024-05-24 |
| [FlashAttention online exact-attention merge identity](#flashattention) | REJECTED for selected claim/assay | 2/2/0/0/2 | 6/10 | 2021-12-10 |
| [Generic mergeable low-rank update attributed to LoRA](#lora) | REJECTED for selected claim/assay | 2/2/0/0/2 | 6/10 | Unknown |
| [Adam in the Shampoo eigenbasis attributed to SOAP](#soap) | REJECTED for selected claim/assay | 2/2/0/0/2 | 6/10 | 2021-03-05 |
| [Exact residual correction in speculative decoding](#speculative-decoding) | REJECTED for selected claim/assay | 2/2/0/0/2 | 6/10 | 2017-08-11 |
| [Hat monotile aperiodicity theorem](#aperiodic-monotile) | REJECTED for selected claim/assay | 0/0/1/2/0 | 3/10 | 2023-03-20 |

## Checkpoint compatibility and selecting the next work

The official Qwen3 announcement is dated **29 April 2025** and lists Qwen3-1.7B. The [separate model audit](model_audit.md) now records full original April 29 immutable snapshots: Qwen3-1.7B `d3e258980a49b060055ea9038dad99d75923f7c4` and Qwen3-0.6B `6130ef31402718485ca4d80a6234f70d9a4cf362`, with original tokenizer/template. These can be investigated for MeanFlow (May 2025), AlphaEvolve’s May announcement and the 2026 DoRA factored-norm application. The current July mechanics revision is a separate condition. Exact-claim earlier disclosures remain unresolved; present `main`, later post-training, adapters or revisions do not qualify automatically. The 2025 exponential-race preprint appeared on 21 April, before that Qwen3 announcement, and is consequently not a Qwen3 historical option. All 2024 and older entries need an older publicly released checkpoint for an N2 claim. [Official Qwen3 announcement](https://qwenlm.github.io/blog/qwen3/), [race-sampling v1](https://arxiv.org/abs/2504.15475v1).

For DPO and later 2023/2024 items, inspect literal archived Pythia revisions and their contemporaneous public-release evidence. Current `main` and step labels are insufficient; some labels have later movement histories. Pre-November-2022 sampling needs an earlier eligible family, while the 2019 stochastic-beam option needs a genuinely pre-March-2019 checkpoint and probably faces a serious competence floor. This survey makes no checkpoint eligibility certification; use the separate temporal audit before admitting any item.

Audit MeanFlow’s exact two-time application first if the immediate goal is a recent small-checkpoint packet. Audit DPO first if the immediate goal is a short exact algebraic packet. Use scalar speculative correction as a verifier/method control; any historically new parallel-block systems claim requires separate scope and admission. Preserve DoRA as a matrix-calculus mechanism with a clear detached-norm control. Do not spend initial model budget on the full matrix rank-48/47 searches or geometric aperiodicity proof until their larger competence and verifier burdens are explicitly accepted. A paper’s empirical achievements are unavailable target facts; recovering the algebra must not be scored as reproducing them.

## Candidate dossiers

Each dossier links directly to primary versioned source material. Exact target, A/B, bridge, verification and empirical exclusions are recorded below; the JSON retains all source records, antecedents, licensing notes, per-dimension rationale and audit tasks.

<a id="meanflow"></a>

### MeanFlow average-velocity identity

**PRIORITY — pending audit · 9/10.** Highest recent algebraic audit priority: short derivation and potentially compatible release-era Qwen3; novelty of the elementary identity itself is not established.

**Target:** Let u(z,r,t) be average velocity along the locally unique ODE trajectory ending at arbitrary endpoint(z,t), defined on a neighborhood, with fixed r and dz/dt=v(z,t). Derive u=v-(t-r)[D_z u·v+partial_t u] from the displacement integral and establish the converse with a bounded diagonal limit.

**A/B and bridge:** A: Fundamental theorem of calculus and the product rule with a fixed integration endpoint. B: Total versus partial derivatives along an ODE trajectory; average displacement divided by elapsed time. Bridge: Differentiate the displacement relation along the same trajectory while holding the earlier time fixed. The donor cue must not contain the final identity or JVP direction.

**Prospective verification:** Prospective proof check: differentiate the defining integral, expand the total derivative, and integrate the differential identity back. Include polynomial/nonconstant trajectories, vector fields, r=t limits, and an unbounded C/(t-r) counterexample to an unrestricted converse. Require boundedness or a boundary condition. When requesting separate partial derivatives, define the full endpoint field via the supplied locally unique ODE, including neighboring endpoints and any required branch/domain. An average specified on just one trajectory fixes only its total derivative, not individual partial derivatives.

**Empirical boundary:** One-step ImageNet quality, optimization stability, effectiveness of conditional-velocity substitution or stop-gradient training, and FID comparisons are not established by recovering the identity.

**Date/source evidence:** Verified date in the arXiv v1 submission history, used as a disclosure-date proxy. First public announcement time and earlier talks, code, theses, abstracts and equivalent results are unresolved; this is not a certified earliest disclosure. Primary records: [v1, 2025-05-19](https://arxiv.org/abs/2505.13447v1), [v1, 2025-05-19](https://arxiv.org/html/2505.13447v1).

**Antecedent boundary:** [2022-10-06](https://arxiv.org/abs/2210.02747v1): Flow Matching supplies instantaneous marginal/conditional velocity context. [2024-10-16](https://arxiv.org/abs/2410.12557v1): Shortcut Models already use step-size-conditioned finite-time transport; audit whether its consistency equation or earlier transport literature contains an equivalent two-time identity.

**Next exact-claim audit:** Audit MeanFlow official code and announcement histories for disclosure before 19 May 2025. Separate the classical calculus identity from the paper-specific two-time generative training construction; decide which novelty claim is actually admissible. Test whether the selected average-displacement definition already supplies too much of the result.

**Licensing:** v1 HTML labels the paper CC BY 4.0. Repository and any generated model/data terms need separate version-specific checks.

<a id="dora"></a>

### DoRA normalized low-rank direction and radial separation

**PRIORITY — pending audit · 8/10.** Checkable composition of two explicit older ingredients; strong packet option but the tangent gradient alone is old, and selecting these prerequisites is human assistance.

**Target:** Construct a mergeable adaptation w_j=m_j(w0_j+BA_j)/||w0_j+BA_j|| for each nonzero vector and derive radial scale versus tangent-direction derivatives, with the chosen row/column convention stated explicitly.

**A/B and bridge:** A: Weight normalization separates a vector magnitude from its unit direction. B: A low-rank additive weight update can be merged into a frozen linear map. Bridge: Use the low-rank update as a change in direction, then renormalize that direction independently of its learned magnitude.

**Prospective verification:** Exact expression checks and symbolic derivative of z/||z||; independent finite differences away from zero, explicit initialization equivalence and merged-forward equality. Full normalization gradients and a detached-denominator implementation are separate targets.

**Empirical boundary:** Accuracy, stability, rank robustness and resemblance to full fine-tuning are empirical, not consequences of radial normalization.

**Date/source evidence:** Verified date in the arXiv v1 submission history, used as a disclosure-date proxy. First public announcement time and earlier talks, code, theses, abstracts and equivalent results are unresolved; this is not a certified earliest disclosure. Primary records: [v1, 2024-02-14](https://arxiv.org/abs/2402.09353v1), [v1, 2024-02-14](https://arxiv.org/html/2402.09353v1).

**Antecedent boundary:** [2016-02-25](https://arxiv.org/abs/1602.07868v1): Weight Normalization already provides magnitude/direction reparameterization and tangent projection derivative. [2021-06-17](https://arxiv.org/abs/2106.09685v1): LoRA provides the low-rank additive and mergeable direction update ingredient.

**Next exact-claim audit:** Audit normalized low-rank adapter variants before February 2024. Distinguish a new combination from rediscovering 2016 weight-normalization calculus. Freeze vector convention and norm-detachment semantics before prompt construction.

**Licensing:** v1 HTML labels the paper CC BY-NC-SA 4.0. NVlabs/DoRA code, dependency, model and dataset licenses must be checked independently; paper terms do not license all artifacts.

<a id="dpo"></a>

### Direct Preference Optimization normalization cancellation

**PRIORITY — pending audit · 7/10.** Strong first packet candidate because the composition is short; older inverse-RL/preferences literature and archived pre-disclosure checkpoint competence remain open.

**Target:** Combine the optimal KL-regularized policy relation r(x,y)=beta log(pi(y|x)/pi_ref(y|x))+beta log Z(x) with a Bradley-Terry pairwise likelihood; cancel log Z(x) and derive the pairwise policy log-ratio logistic objective.

**A/B and bridge:** A: KL-regularized reward maximization on a finite action set, including normalization and support conditions. B: Pairwise Bradley-Terry preference likelihood and logistic log-likelihood algebra. Bridge: Compare rewards for alternatives with the same conditioning context so the shared normalizer cancels.

**Prospective verification:** Prospective symbolic substitution and exact/controlled high-precision finite-action checks under varied beta and reference policies. Test zero-support exclusions, separate contexts where cancellation fails, and reward shifts that leave preferences unchanged.

**Empirical boundary:** Human preference alignment, optimization behavior, benchmark wins and real-policy generalization are unavailable from the algebra alone.

**Date/source evidence:** Verified date in the arXiv v1 submission history, used as a disclosure-date proxy. First public announcement time and earlier talks, code, theses, abstracts and equivalent results are unresolved; this is not a certified earliest disclosure. Primary records: [v1, 2023-05-29](https://arxiv.org/abs/2305.18290v1), [v1, 2023-05-29](https://arxiv.org/pdf/2305.18290v1).

**Antecedent boundary:** [2018-05-02](https://arxiv.org/abs/1805.00909v1): Levine variational/control-as-inference review supplies entropy-regularized optimal-policy background; not evidence of the complete DPO pairing. [exact date unresolved](https://doi.org/10.2307/2334029): Bradley and Terry paired-comparison model, 1952 journal work; exact original public date was not independently resolved here.

**Next exact-claim audit:** Audit reward-to-policy preference optimization and earlier inverse reinforcement learning for the same normalization cancellation. Verify an actual pre-disclosure Pythia snapshot, rather than current main or a retrospectively moved step tag.

**Licensing:** Paper and code licenses must be checked separately at the actual version used; this survey links sources and authors original summaries without redistributing their text or code.

<a id="ssd"></a>

### Mamba-2 SSD block decomposition

**PRIORITY — pending audit · 7/10.** Useful structured-linear-algebra bridge; generic recurrence-to-matrix conversion is old, so the block algorithm must be isolated precisely.

**Target:** For scalar-transition selective state recurrences, derive the causal masked matrix representation and a block algorithm with within-block dense products, low-rank off-diagonal factors and propagated boundary states; prove equivalence to the sequential recurrence.

**A/B and bridge:** A: Unroll a time-varying linear state recurrence, including products of intervening transitions. B: Factor cross-block interactions through a low-dimensional boundary state and use associativity of matrix products. Bridge: Cut the recurrence at block boundaries; every cross-block contribution passes through the boundary state.

**Prospective verification:** Independent rational scalar-transition recurrence and dense masked-matrix reference on short sequences with nonzero initial states, unequal blocks and zero/negative transitions; symbolic factorization proves all-size correctness. The mere existence of a recurrent/attention equivalence is not the new target.

**Empirical boundary:** Mamba-2 throughput, scaling, language quality and hardware efficiency are not established by output equality.

**Date/source evidence:** Verified date in the arXiv v1 submission history, used as a disclosure-date proxy. First public announcement time and earlier talks, code, theses, abstracts and equivalent results are unresolved; this is not a certified earliest disclosure. Primary records: [v1, 2024-05-31](https://arxiv.org/abs/2405.21060v1), [v1, 2024-05-31](https://arxiv.org/html/2405.21060v1).

**Antecedent boundary:** [2021-02-22](https://arxiv.org/abs/2102.11174v1): Linear attention/fast-weight recurrence equivalence is already public. [2023-12-01](https://arxiv.org/abs/2312.00752v1): Mamba selective state-space recurrences precede the scalar-transition SSD specialization. [exact date unresolved](https://arxiv.org/html/2405.21060v1): The target itself acknowledges older sequentially semiseparable matrix representations; cited numerical-linear-algebra papers and technical-report histories need direct audit.

**Next exact-claim audit:** Audit older semiseparable matrix multiplication and gated linear attention algorithms for the same scalar-transition block decomposition. Check pre-v1 ICML submissions, talks, Mamba-2 code and public project history.

**Licensing:** Paper and code licenses must be checked separately at the actual version used; this survey links sources and authors original summaries without redistributing their text or code.

<a id="deltanet-wy"></a>

### Parallel DeltaNet through compact rank-one products

**PRIORITY — pending audit · 6/10.** A specific composition with strong exact checks; noncommutativity and rank-one recurrence competence could be difficult for a small checkpoint.

**Target:** Starting from S_t=S_(t-1)(I-beta_t k_t k_t^T)+beta_t v_t k_t^T, derive compact vector-factor recurrences for transition and injection products, then chunk states and outputs without materializing every dense transition.

**A/B and bridge:** A: The delta-rule outer-product memory update and noncommuting ordered matrix products. B: WY-style compact representation of products of identity-minus-rank-one factors. Bridge: Treat the sequence of memory erasures as an ordered product of rank-one factors and apply the same representation to accumulated writes.

**Prospective verification:** Rational small-matrix checks of sequential updates versus compact products and chunk outputs, plus induction. Include nonzero initial state, nonorthogonal keys, varied beta, arbitrary chunk lengths and swapped-order counterexamples. Complexity must be assessed under an explicit cost model.

**Empirical boundary:** GPU training speed, associative recall, perplexity and hybrid-model superiority are empirical and unavailable from algebraic reconstruction.

**Date/source evidence:** Verified date in the arXiv v1 submission history, used as a disclosure-date proxy. First public announcement time and earlier talks, code, theses, abstracts and equivalent results are unresolved; this is not a certified earliest disclosure. Primary records: [v1, 2024-06-10](https://arxiv.org/abs/2406.06484v1), [v1, 2024-06-10](https://arxiv.org/html/2406.06484v1).

**Antecedent boundary:** [2021-02-22](https://arxiv.org/abs/2102.11174v1): Schlag et al. provides the earlier delta-rule fast-weight memory. [exact date unresolved](https://doi.org/10.1137/0908009): Bischof and Van Loan WY representation, journal 1987 with a 1985 technical-report citation in the target; exact earlier public history and generalized non-Householder factors require audit.

**Next exact-claim audit:** Audit compact WY/generalized rank-one product algorithms beyond normalized Householder reflectors. Determine whether older fast-weight parallel training code already realizes the same chunk recurrence.

**Licensing:** Paper and code licenses must be checked separately at the actual version used; this survey links sources and authors original summaries without redistributing their text or code.

<a id="dora-factored-norms"></a>

### Factored norms for high-rank DoRA

**AMBIGUOUS · 8/10.** Recent and highly mechanically checkable, potentially release-era Qwen3 compatible, but easy rediscovery of old algebra cannot by itself establish a new 2026 theorem.

**Target:** Compute each row norm of W+sBA without materializing BA: ||W_j||^2+2s B_j(W_j A^T)^T+s^2 B_j(AA^T)B_j^T, with exact equality and an explicit intermediate-memory cost model.

**A/B and bridge:** A: Quadratic expansion of a squared norm and Gram-matrix identities. B: Associativity of low-rank matrix products and rowwise reductions. Bridge: Expand the squared norm before forming the low-rank product, then contract the small shared dimension first.

**Prospective verification:** Symbolic polynomial identity and exact rational matrices against dense row norms. Include s=0, negative scale, nonorthogonal factors and near-cancellation. Floating-point clamping, detached gradients and measured allocator savings are separate implementation claims.

**Empirical boundary:** Fused-kernel speed-ups, observed GPU memory, bf16 numerical parity and training fidelity require systems measurements.

**Date/source evidence:** Verified date in the arXiv v1 submission history, used as a disclosure-date proxy. First public announcement time and earlier talks, code, theses, abstracts and equivalent results are unresolved; this is not a certified earliest disclosure. Primary records: [v1, 2026-03-23](https://arxiv.org/abs/2603.22276v1), [v1, 2026-03-23](https://arxiv.org/pdf/2603.22276v1).

**Antecedent boundary:** [2024-02-14](https://arxiv.org/abs/2402.09353v1): DoRA makes the normalized low-rank sum a practical target. [2021-06-17](https://arxiv.org/abs/2106.09685v1): Low-rank update contraction is earlier; the displayed norm identity is classical quadratic-form algebra, so its novel application/history must be audited.

**Next exact-claim audit:** Search pre-2026 PEFT/DoRA code, merge implementations and low-rank norm estimation for exactly this contraction. Audit whether paper-specific memory-saving execution rather than the mathematical identity is an admissible target. Pin earliest official code publication and repository license.

**Licensing:** arXiv v1 links a Creative Commons license, but the exact terms and code/data terms were not fully resolved; do not inherit the original DoRA paper license.

<a id="alphadev-sort3"></a>

### AlphaDev small-sort conditional-copy shortcut

**AMBIGUOUS · 7/10.** A non-neural finite-program bridge with plausible small-model prerequisites, but the early LLVM review destroys an uncomplicated 2023 temporal story and instruction-level novelty remains unresolved.

**Target:** Reconstruct an exact three-element comparison/copy sorting program that removes a redundant value movement under the established partial-order invariant, while preserving the multiset and ascending order for signed integers. Specify the exact instruction set and instruction-count benchmark before asserting improvement.

**A/B and bridge:** A: Compare-exchange/min-max operations and known partial orders after an initial comparison. B: Conditional assignment, register liveness and redundant-copy elimination under path invariants. Bridge: Use the order already established by preceding comparisons to identify which conditional copy cannot affect the final sorted output; it must not supply the replacement expression itself.

**Prospective verification:** Prove equivalence over all total preorders of three inputs including ties, then check faithful signed comparison/conditional-move ISA semantics and register/memory behavior. A source-level compare/copy model admits a small complete checker; arbitrary C++ comparators, NaNs, UB and real assembly require additional semantics. Count instructions under a declared cost model; do not infer CPU speed.

**Empirical boundary:** CPU latency, library-level speed-ups, search efficiency and portability are empirical; instruction count alone does not establish the published runtime gains.

**Date/source evidence:** Verified official shortcut announcement on 7 June 2023, but directly inspected related LLVM public review dated 24 January 2022. Exact selected motif in the earliest diff and any still earlier disclosure are unresolved; this candidate cannot be admitted using the 2023 paper date. Primary records: [dated official announcement, live page, 2023-06-07](https://deepmind.google/blog/alphadev-discovers-faster-sorting-algorithms/), [archived public review and dated discussion; initial diff versus selected target unresolved, 2022-01-24](https://reviews.llvm.org/D118029), [main inspected 2026-10-11; immutable historical revision unresolved, date unresolved](https://github.com/google-deepmind/alphadev/blob/main/sort_functions_test.cc), [version of record; full text access incomplete, 2023-06-07](https://www.nature.com/articles/s41586-023-06004-9).

**Antecedent boundary:** [2022-01-24](https://reviews.llvm.org/D118029): An earlier related disclosure from the same work, not independent prior art. Compare every revision to the selected shortcut before using its date as exact-claim boundary. [exact date unresolved](https://github.com/llvm/llvm-project): Existing libc++ sort kernels and older sorting-network/superoptimization literature form the comparison baseline; exact early variant and public release history require audit.

**Next exact-claim audit:** Recover LLVM initial diff402459 and all shortcut-bearing revisions, their public visibility and the linked benchmark artifacts. Compare the selected sort3 program/motif with old sorting networks, compiler peephole optimization and min/max simplification identities. Pin an immutable pre-earliest-code checkpoint; a current Pythia or assumed 2023 release is insufficient.

**Licensing:** Official AlphaDev README states Apache2 for software and CCBY4 for other materials; LLVM artifacts have their own terms. The Nature paper license was not resolved.

<a id="exponential-race-speculation"></a>

### Speculative sampling with shared exponential races

**AMBIGUOUS · 7/10.** Compact verifier-friendly bridge but elementary shared-race coupling is old. Qwen3 arrives after this v1, so the initially attractive 2025 date does not solve temporal eligibility.

**Target:** Couple draft and target categorical draws using the same independent Exp(1) clocks; verify draft tokens by equality with the target race winner and preserve the autoregressive target law when accepting a prefix or replacing its first mismatch.

**A/B and bridge:** A: The minimum of independent exponential clocks scaled by probabilities has the required categorical winner distribution. B: Prefix-conditional autoregressive sampling with matched random numbers for proposed and verified positions. Bridge: Reuse the random clocks under both distributions and compare their winners, keeping the target winner after disagreement.

**Prospective verification:** Analytic integration of winner probabilities and exact conditional-law proof for short blocks. Test probability zeros, support mismatch handling, prefix truncation, ties of probability zero and random-number alignment. Simulation can diagnose but not prove distribution equality.

**Empirical boundary:** Speed-up, acceptance-rate advantage, channel-simulation bounds beyond the selected elementary claim, and empirical parity with other decoders need separate evidence.

**Date/source evidence:** Verified date in the arXiv v1 submission history, used as a disclosure-date proxy. First public announcement time and earlier talks, code, theses, abstracts and equivalent results are unresolved; this is not a certified earliest disclosure. Primary records: [v1, 2025-04-21](https://arxiv.org/abs/2504.15475v1), [v1, 2025-04-21](https://arxiv.org/html/2504.15475v1).

**Antecedent boundary:** [2014-10-31](https://arxiv.org/abs/1411.0030v1): A* Sampling develops Gumbel process sampling; classical Gumbel-max/exponential-race identities are earlier than 2025. [exact date unresolved](https://arxiv.org/html/2504.15475v1): The target cites Maddison 2017 and Li/El Gamal 2018 Poisson functional representation; earlier channel simulation and correlated sampling may already contain the selected coupling.

**Next exact-claim audit:** Audit shared-Gumbel decoding before April 2025 and distinguish an application from a new coupling theorem. Inspect 2025 conference submission/public review histories and exact block verification random-number semantics.

**Licensing:** v1 HTML labels the paper CC BY 4.0. Code terms and release history remain unverified.

<a id="lora-fa"></a>

### Frozen-factor low-rank adaptation activation gradient

**AMBIGUOUS · 7/10.** Simple memory/computation bridge, but the chosen derivative is elementary and the main contribution is engineering and empirical adequacy.

**Target:** For y=x(W0+AB) with W0 and projection-down A frozen, derive dL/dB=(xA)^T delta and identify conditions under which the B-gradient requires retaining xA instead of x solely for this adapter path.

**A/B and bridge:** A: Chain rule for matrix linear maps and outer-product parameter gradients. B: A fixed low-dimensional projection precedes the only trainable matrix. Bridge: Differentiate only the trainable factor after the fixed projection, and retain the projected sufficient activation.

**Prospective verification:** Symbolic matrix differentiation and independent finite-difference B gradients; activation-liveness analysis of the explicitly specified graph. Backbone paths and other trainable parameters may still require x, so do not claim whole-model O(rank) activation storage from this local identity.

**Empirical boundary:** Fine-tuning accuracy parity, end-to-end memory savings and interactions with quantization/sharding require experiments.

**Date/source evidence:** Verified date in the arXiv v1 submission history, used as a disclosure-date proxy. First public announcement time and earlier talks, code, theses, abstracts and equivalent results are unresolved; this is not a certified earliest disclosure. Primary records: [v1, 2023-08-07](https://arxiv.org/abs/2308.03303v1), [v1, 2023-08-07](https://arxiv.org/pdf/2308.03303v1).

**Antecedent boundary:** [2021-06-17](https://arxiv.org/abs/2106.09685v1): LoRA already has the factorized branch. [2020-12-22](https://arxiv.org/abs/2012.13255v1): Frozen subspace fine-tuning antecedent; fixed random features and local sufficient gradient activations may make this exact algebra old.

**Next exact-claim audit:** Audit earlier frozen-factor adapters/random-feature training for the same activation-memory argument. Freeze matrix orientation and graph scope; inspect the paper optimizer/preconditioner extension separately.

**Licensing:** Paper and code licenses must be checked separately at the actual version used; this survey links sources and authors original summaries without redistributing their text or code.

<a id="alphaevolve-rank48"></a>

### AlphaEvolve rank-48 complex matrix multiplication certificate

**AMBIGUOUS · 6/10.** A meaningful recent mathematics target with an exact finite certificate and potential old-Qwen3 chronology, but likely unrealistic for a small-model short-bridge assay.

**Target:** Produce a 48-term rank-one decomposition of the 4x4 matrix-multiplication tensor over the complex numbers (as in the released half-integer complex factor construction), and certify every tensor coefficient. The target is bilinear tensor rank, not unrestricted scalar multiplication count.

**A/B and bridge:** A: Bilinear algorithms correspond to exact sums of rank-one tensors, with a fixed input/output indexing convention. B: Strassen-type decomposition, linear changes of basis and cancellation/search over factor coefficients. Bridge: Explore cancellation among rank-one tensor terms or propose a search procedure whose output is a valid lower-rank certificate. This is an exploratory search bridge, not a known short deduction of the 48-term construction.

**Prospective verification:** An independent exact Gaussian-rational coefficient checker compares all 16^3 entries to the matrix-multiplication tensor; require 48 terms and validate coefficient representation. The official notebook contains the construction and a verifier but was only inspected, not executed or independently validated here.

**Empirical boundary:** Agent discovery rates, search cost, superiority on arbitrary fields, runtime gains and hardware deployment claims are not certified by one valid tensor decomposition.

**Date/source evidence:** Official announcement dated 14 May 2025 is an earlier verified public disclosure than arXiv v1 (16 June 2025). Earlier code, presentations and equivalent certificates are unresolved. Primary records: [dated announcement, live page, 2025-05-14](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/), [v1, 2025-06-16](https://arxiv.org/abs/2506.13131v1), [main inspected 2026-10-11; immutable commit unresolved, date unresolved](https://github.com/google-deepmind/alphaevolve_results/blob/main/mathematical_results.ipynb).

**Antecedent boundary:** [exact date unresolved](https://doi.org/10.1007/BF02165411): Strassen 1969 provides the recursive 49-term benchmark; exact original public date was not resolved. [2022-10-05](https://www.nature.com/articles/s41586-022-05172-4): AlphaTensor 47-term 4x4 result is over GF(2), a different field. [exact date unresolved](https://doi.org/10.1109/T-C.1970.222926): Older Waksman scalar-operation algorithms require scope audit; lower unrestricted counts do not automatically disqualify a bilinear tensor-rank contribution.

**Next exact-claim audit:** Archive the May announcement/linked white paper and notebook first-public visibility; do not use June arXiv as the first disclosure. Independently verify the exact complex certificate and all tensor index conventions. Audit prior bilinear rank-48 constructions and distinguish Waksman/Winograd nonbilinear operation counts. Decide whether a certificate search belongs in a later program-search study instead of the initial composition assay.

**Licensing:** Official results README states Apache 2.0 for software and CC BY 4.0 for other materials. arXiv v1 paper separately labels CC BY-NC-ND 4.0; these licenses must not be conflated.

<a id="flow-matching"></a>

### Conditional-to-marginal flow-matching gradient equivalence

**AMBIGUOUS · 6/10.** Checkable scientific-method derivation, but two close earlier disclosures and classical conditional-regression identities make novelty isolation weak.

**Target:** Define the marginal velocity as the conditional expectation of a conditional velocity given x,t; derive that marginal and conditional squared-regression objectives have the same parameter gradient under integrability and differentiation assumptions.

**A/B and bridge:** A: Mixture/conditional probability, conditional expectation and the tower property. B: Squared regression gradient, with a parameter-free conditional target and justified derivative-expectation interchange. Bridge: Condition the regression gradient on the observed state, replacing the hidden conditional velocity by its conditional expectation.

**Prospective verification:** Symbolic conditional-expectation proof and exact finite-mixture algebra; verify continuity-equation transport as a separate target. Include nonintegrable/parameter-dependent-target counterexamples. Distributional sampling quality does not follow solely from equality of gradients.

**Empirical boundary:** Image quality, likelihood, training stability, practical ODE cost and optimal-transport path gains are empirical.

**Date/source evidence:** Verified date in the arXiv v1 submission history, used as a disclosure-date proxy. First public announcement time and earlier talks, code, theses, abstracts and equivalent results are unresolved; this is not a certified earliest disclosure. Primary records: [v1, 2022-10-06](https://arxiv.org/abs/2210.02747v1), [v1, 2022-10-06](https://arxiv.org/pdf/2210.02747v1).

**Antecedent boundary:** [2022-09-07](https://arxiv.org/abs/2209.03003v1): Rectified Flow earlier models straight-path transport by regression; exact overlap requires audit. [2022-09-30](https://arxiv.org/abs/2209.15571v1): Stochastic Interpolants already derives marginal vector fields from interpolating distributions before the Flow Matching v1.

**Next exact-claim audit:** Compare the exact selected theorem with September 2022 Rectified Flow and Stochastic Interpolants, not their later venues. Audit earlier conditional score-matching and transport-regression formulations for equivalence.

**Licensing:** Paper and code licenses must be checked separately at the actual version used; this survey links sources and authors original summaries without redistributing their text or code.

<a id="ttt-dual"></a>

### Causal minibatch TTT-Linear dual form

**AMBIGUOUS · 6/10.** Useful causal minibatch specialization; generic dual form is explicitly prior art. Needs a narrow differentiation from 2022 rather than a claim to invent the duality.

**Target:** With squared-error gradients all evaluated at the same minibatch start W0, derive both the final weight update and causal token outputs using residual matrices and a masked Gram matrix, avoiding one dense gradient/state matrix per token.

**A/B and bridge:** A: Squared-error linear-model gradients are outer products; minibatch gradients may share a fixed evaluation point. B: Reassociate outer-product sums into matrix products and impose causal prefix masks. Bridge: Substitute each cumulative weight update directly into its output, then collect all inner products into a triangular Gram matrix.

**Prospective verification:** Rational explicit per-token gradients/states versus the dual formula with independent row/column implementations; include unequal learning rates and nonzero W0. Reject equivalence to fully online gradients evaluated at successively updated weights, which is a different algorithm. Audit v1 PDF against HTML equation indexing.

**Empirical boundary:** Long-context quality, hardware throughput and nonlinear-TTT empirical improvements are not available from the simplified equivalence.

**Date/source evidence:** Verified date in the arXiv v1 submission history, used as a disclosure-date proxy. First public announcement time and earlier talks, code, theses, abstracts and equivalent results are unresolved; this is not a certified earliest disclosure. Primary records: [v1, 2024-07-05](https://arxiv.org/abs/2407.04620v1), [v1, 2024-07-05](https://arxiv.org/html/2407.04620v1).

**Antecedent boundary:** [exact date unresolved](https://proceedings.mlr.press/v162/irie22a.html): ICML proceedings in July 2022 (exact day/earlier preprint unresolved). Irie et al. The Dual Form of Neural Networks Revisited already expresses trained linear maps as attention-like key-value memory; this is an actual novelty limitation, not an incidental citation. [2021-02-22](https://arxiv.org/abs/2102.11174v1): Fast-weight memory/linear-attention connection supplies older equivalent components.

**Next exact-claim audit:** Compare the causal shared-W0 minibatch target line by line with Irie 2022 and earlier dual forms. Check whether specifying minibatch and causal Gram premises effectively supplies the result. Audit project talks and public code because the authors describe internal work beginning in 2022.

**Licensing:** v1 HTML labels the paper CC BY 4.0; implementation and pretrained-model terms remain separate.

<a id="alphatensor-rank47"></a>

### AlphaTensor rank-47 GF(2) matrix multiplication certificate

**AMBIGUOUS · 5/10.** Strong mathematical certificate, weak small-model prerequisite and bridge feasibility; retain as an ambitious separate algorithm-search branch.

**Target:** Produce and check a 47-term rank-one decomposition for 4x4 matrix multiplication over GF(2), below the recursive Strassen 49-term construction; do not transfer this field-specific result to characteristic zero.

**A/B and bridge:** A: GF(2) arithmetic and coefficient comparison of bilinear tensor expressions. B: Rank-one tensor decomposition and transformations of existing Strassen-style algorithms. Bridge: Search for cancellations in a structured decomposition and return a complete coefficient certificate. No concise derivational bridge has been established.

**Prospective verification:** Exact parity checks of every tensor coefficient plus output-index checks. Exhaustive enumeration of all matrix pairs is unnecessary once all bilinear coefficients match. A correct decomposition establishes an upper bound, not optimal tensor rank.

**Empirical boundary:** Deep-RL discovery efficiency, search cost, hardware speed-ups and global optimality of rank 47 are unavailable from the certificate alone.

**Date/source evidence:** Verified Nature version-of-record publication date, not a certified first disclosure. Earlier public code/talk/abstract history unresolved; private submission and acceptance dates are not used as disclosure dates. Primary records: [version of record, 2022-10-05](https://www.nature.com/articles/s41586-022-05172-4), [live official repository; immutable historical revision unresolved, date unresolved](https://github.com/google-deepmind/alphatensor).

**Antecedent boundary:** [exact date unresolved](https://doi.org/10.1007/BF02165411): Strassen 1969 multiplication decomposition; investigate subsequent GF(2) tensor-rank algorithms before assigning novelty.

**Next exact-claim audit:** Audit paper-linked algorithm archive and earliest code/talk disclosure; received and accepted dates are not public disclosure. Independently reconstruct/check the 47-term GF(2) certificate and its equivalence class. Search earlier finite-field matrix multiplication decompositions.

**Licensing:** Paper and code licenses must be checked separately at the actual version used; this survey links sources and authors original summaries without redistributing their text or code.

<a id="gumbel-topk-sequences"></a>

### Stochastic Beam Search without-replacement sequence sampling

**AMBIGUOUS · 5/10.** Mechanistically distinct sampling target, but very early release requirement leaves small GPT-2-era checkpoints with uncertain competence; generic Gumbel-top-k is not new.

**Target:** Generate k complete sequences without replacement from a finite autoregressive tree by consistently assigning/truncating Gumbel subtree maxima; prove agreement with the ordered Gumbel-top-k law, rather than rediscovering categorical Gumbel-max alone.

**A/B and bridge:** A: Gumbel-max/top-k equivalence to categorical/Plackett-Luce sampling. B: Factorized sequence probabilities and conditional subtree maxima with globally consistent random perturbations. Bridge: Represent each prefix by the maximum perturbed score of its entire completion subtree and condition children consistently on that maximum.

**Prospective verification:** Exact probability-law derivation for a tiny finite tree and enumeration of ordered samples; independent simulation is secondary. A finite beam that independently perturbs local logits is not automatically exact. Include unequal depths, EOS, ties and k exceeding support.

**Empirical boundary:** Translation quality, diversity usefulness and model-evaluation cost on realistic distributions require experiments.

**Date/source evidence:** Verified date in the arXiv v1 submission history, used as a disclosure-date proxy. First public announcement time and earlier talks, code, theses, abstracts and equivalent results are unresolved; this is not a certified earliest disclosure. Primary records: [v1, 2019-03-14](https://arxiv.org/abs/1903.06059v1), [v1, 2019-03-14](https://arxiv.org/pdf/1903.06059v1).

**Antecedent boundary:** [2014-10-31](https://arxiv.org/abs/1411.0030v1): A* Sampling/Gumbel process antecedent; broad perturb-and-max claims are earlier.

**Next exact-claim audit:** Audit author thesis, code and older stochastic-beam/Gumbel-process results for exact sequence-tree equivalence. Find an actual checkpoint public before March 2019; later GPT-2 size releases or Pythia cannot qualify.

**Licensing:** Paper and code licenses must be checked separately at the actual version used; this survey links sources and authors original summaries without redistributing their text or code.

<a id="schedule-free"></a>

### Schedule-Free online-to-batch interpolation theorem

**AMBIGUOUS · 5/10.** Broader optimizer diversity and a meaningful proof target, but verifier construction and exact proof competence are harder than a matrix identity.

**Target:** For weighted running averages x_t, interpolated evaluation points y_t=beta_t x_t+(1-beta_t)z_t and fresh unbiased stochastic gradients, derive the stated expected suboptimality bound from linearized regret at z_t under the theorem conditions.

**A/B and bridge:** A: Convexity subgradient inequality and martingale/unbiased-gradient expectation with correctly timed randomness. B: Weighted running-average telescoping and an online regret bound. Bridge: Express each new weighted-average displacement in terms of z_t-x_(t-1), then telescope the convexity bounds while accounting for interpolation.

**Prospective verification:** A complete symbolic telescoping proof with measurable/adaptedness assumptions; finite convex examples only sanity-check it. Recovering SGD worst-case rates additionally requires its regret bound. Report theorem horizon-dependent constants separately from practical schedule-free stopping.

**Empirical boundary:** Deep-network performance, robustness, tuning burden and AlgoPerf success are empirical. Numerical examples cannot prove the theorem.

**Date/source evidence:** Verified date in the arXiv v1 submission history, used as a disclosure-date proxy. First public announcement time and earlier talks, code, theses, abstracts and equivalent results are unresolved; this is not a certified earliest disclosure. Primary records: [v1, 2024-05-24](https://arxiv.org/abs/2405.15682v1), [v1, 2024-05-24](https://arxiv.org/pdf/2405.15682v1).

**Antecedent boundary:** [exact date unresolved](https://arxiv.org/pdf/2405.15682v1): The v1 explicitly traces Polyak/Ruppert averaging, primal averaging and earlier online-to-batch conversions; retrieve original articles before assigning novelty to the interpolation theorem.

**Next exact-claim audit:** Trace the exact general theorem through the earlier averaging and online-to-batch works cited by v1. Check whether the constants, weighted case or interpolation, rather than the baseline convergence order, is the contribution.

**Licensing:** Paper and code licenses must be checked separately at the actual version used; this survey links sources and authors original summaries without redistributing their text or code.

<a id="flashattention"></a>

### FlashAttention online exact-attention merge identity

**REJECTED for selected claim/assay · 6/10.** Keep as a verifier/control example, not a FlashAttention novelty item. The specific IO-aware system contribution requires a different target and verifier.

**Target:** Merge exact attention/softmax summaries across blocks using a common running maximum, rescaled normalization masses and weighted-value numerators.

**A/B and bridge:** A: Softmax translation invariance and stable exponential normalization. B: Associative merging of sufficient sums and weighted-value numerators. Bridge: Put the block summaries in a shared exponential scale before adding their masses and numerators.

**Prospective verification:** An exact symbolic rescaling/merge proof and numeric checks can verify the identity. They do not prove GPU IO optimality or reproduce FlashAttention tiling/backward design.

**Empirical boundary:** Hardware IO savings, wall-clock throughput and practical memory efficiency are empirical/system-specific.

**Date/source evidence:** An earlier equivalent exact-memory attention result is verified at Rabe-Staats v1 (10 December 2021); online normalization is earlier still (8 May 2018). First public disclosure of every weighted-merge detail is unresolved. Primary records: [v1, 2022-05-27](https://arxiv.org/abs/2205.14135v1), [v1, 2021-12-10](https://arxiv.org/abs/2112.05682v1), [v1, 2018-05-08](https://arxiv.org/abs/1805.02867v1).

**Antecedent boundary:** [2021-12-10](https://arxiv.org/abs/2112.05682v1): Earlier exact-memory attention disqualifies attributing the generic merge to the 2022 FlashAttention discovery. [2018-05-08](https://arxiv.org/abs/1805.02867v1): Online normalizer recurrence precedes both attention papers.

**Exclusion:** Rejected for the selected 2022 FlashAttention reconstruction claim because the selected merge/exact-memory principle has explicit earlier antecedents. This does not reject the paper-specific IO-aware tiling/backward/complexity contribution.

**Next exact-claim audit:** Locate earliest claim-equivalent weighted merge before 2021 if re-targeting it historically. Temporal worker identified a 20 May 2022 first-release code commit: verify actual public visibility before using it as the earlier FlashAttention disclosure.

**Licensing:** Paper and code licenses must be checked separately at the actual version used; this survey links sources and authors original summaries without redistributing their text or code.

<a id="lora"></a>

### Generic mergeable low-rank update attributed to LoRA

**REJECTED for selected claim/assay · 6/10.** Useful calibration for prerequisites and merge verification; selected equation is elementary old algebra and cannot isolate the LoRA contribution.

**Target:** Derive (W0+BA)x=W0x+B(Ax) and merge a learned low-rank additive adapter into a frozen linear weight.

**A/B and bridge:** A: Matrix associativity and a rank-r factorization. B: Linearity of a frozen layer plus an additive trainable branch. Bridge: Regroup the two factor multiplications and add the update to the frozen weight.

**Prospective verification:** Exact symbolic and rational-matrix equality suffices for the local merge identity; it cannot establish useful low-rank fine-tuning capacity.

**Empirical boundary:** Low intrinsic rank, accuracy parity, adaptation quality and parameter-efficiency benefits need real training evidence.

**Date/source evidence:** Unknown first disclosure of this elementary identity; LoRA v1 is 17 June 2021 but is not treated as its invention date. Primary records: [v1, 2021-06-17](https://arxiv.org/abs/2106.09685v1).

**Antecedent boundary:** [2020-12-22](https://arxiv.org/abs/2012.13255v1): Earlier intrinsic-dimensionality fine-tuning. [exact date unresolved](https://arxiv.org/pdf/2106.09685v1): The v1 references a 2016 low-rank-plus-diagonal recurrent-adaptation antecedent; independently retrieve its exact source and disclosure history before claiming an equivalent neural adapter is new.

**Exclusion:** The selected merge identity is an elementary algebraic consequence and older low-rank adaptation exists; a 2021 LoRA novelty claim cannot rest on this identity.

**Next exact-claim audit:** If re-targeted, identify the empirical or adapter-design contribution beyond matrix distributivity and find a suitable verifier. Retrieve and compare the 2016 factorized-adaptation reference in the original LoRA bibliography.

**Licensing:** Paper and code licenses must be checked separately at the actual version used; this survey links sources and authors original summaries without redistributing their text or code.

<a id="soap"></a>

### Adam in the Shampoo eigenbasis attributed to SOAP

**REJECTED for selected claim/assay · 6/10.** Direct prior-art disqualification for the generic rotated optimizer; a narrower 2024 equivalence theorem could be considered under a new candidate ID after audit.

**Target:** Rotate a matrix gradient into the eigenspaces of Kronecker factors, maintain diagonal squared-gradient statistics there, apply an adaptive update, and rotate back.

**A/B and bridge:** A: Orthogonal change of coordinates and Kronecker-factored gradient statistics. B: Elementwise adaptive preconditioning in a chosen coordinate basis. Bridge: Apply the diagonal optimizer where the matrix preconditioner is diagonal, then undo the basis transform.

**Prospective verification:** Symbolic fixed-basis change-of-coordinate equality and explicit tiny-matrix updates; changing-basis moment transport must be specified. The newer idealized Shampoo-to-Adafactor theorem is a distinct possible target, not admitted here.

**Empirical boundary:** Training speed, robustness to infrequent eigendecompositions and the practical superiority reported by SOAP are empirical.

**Date/source evidence:** Verified equivalent antecedent in the March 2021 v2. Target paper is September 2024; exact first disclosure of the antecedent is unresolved, and the 2020 v1 date is not substituted for v2. Primary records: [v1, 2024-09-17](https://arxiv.org/pdf/2409.11321v1), [v2, 2021-03-05](https://arxiv.org/pdf/2002.09018v2).

**Antecedent boundary:** [2021-03-05](https://arxiv.org/pdf/2002.09018v2): Directly inspected earlier eigenbasis/diagonal-gradient correction; SOAP v1 Section 3 explicitly calls this essentially equivalent for 2D layers. [2020-02-20](https://arxiv.org/abs/2002.09018v1): The earlier paper began in 2020, but inspected v1 did not show the same appendix; do not assert that the equivalent algorithm was definitely public in 2020.

**Exclusion:** Rejected as a 2024 novelty item: the target acknowledges an essentially equivalent earlier algorithm and a pre-2024 version was directly inspected.

**Next exact-claim audit:** Verify whether equivalent code/presentation preceded March 2021 and where v1/v2 differ. If re-targeting, formally specify every assumption of the 2024 idealized Shampoo-to-Adafactor theorem and audit its novelty separately.

**Licensing:** Paper and code licenses must be checked separately at the actual version used; this survey links sources and authors original summaries without redistributing their text or code.

<a id="speculative-decoding"></a>

### Exact residual correction in speculative decoding

**REJECTED for selected claim/assay · 6/10.** Excellent scalar verifier/control, but a directly verified 2017 maximal-coupling equivalent disqualifies attributing this scalar law to the 2022 discovery. Specific parallel/block systems contributions are a separate unaudited scope.

**Target:** For draft q and target p on a finite alphabet, derive acceptance min(1,p(x)/q(x)) and rejection replacement proportional to(p-q)_+, proving the final one-token marginal is p. This scalar correction is the selected packet claim; parallel target scoring and an autoregressive block systems contribution require a separate historical scope.

**A/B and bridge:** A: Finite probability mixtures, conditional probability, and pointwise minimum/positive-part identities. B: Parallel target scoring of a proposed prefix and left-to-right autoregressive factorization. Bridge: Account for the probability mass already emitted through accepted proposals, then complete the target distribution with the missing mass.

**Prospective verification:** Exact rational small-alphabet probabilities and symbolic mass conservation, including q=0, p=0 and p=q. The earlier maximal-coupling algorithm yields this residual law after swapping source p/q labels. A block/EOS/cache extension can be checked separately but is not a newly admitted claim here.

**Empirical boundary:** Wall-clock acceleration, hardware-numeric distribution fidelity, draft-model usefulness and output quality on real LLMs require measurement.

**Date/source evidence:** The selected scalar accept/positive-residual law is verified in an earlier maximal-coupling v1 submitted 11 August 2017. The speculative-decoding target paper v1 is 30 November 2022; generic scalar-law novelty at that later boundary is disqualified. Thorisson 2000 is an earlier lead, not independently inspected. Primary records: [v1, 2022-11-30](https://arxiv.org/abs/2211.17192v1), [v1, 2022-11-30](https://arxiv.org/pdf/2211.17192v1), [v1, 2023-02-02](https://arxiv.org/abs/2302.01318v1), [v1, 2017-08-11](https://arxiv.org/html/1708.03625v1).

**Antecedent boundary:** [2017-08-11](https://arxiv.org/html/1708.03625v1): Direct claim-equivalent maximal-coupling antecedent, independently opened after reviewer supplied the lead; selected scalar residual novelty is rejected, not merely uncertain. Thorisson 2000 Chapter1§4.5 is cited here but not directly inspected. [2025-04-21](https://arxiv.org/html/2504.15475v1): Later primary analysis identifies equivalence to older greedy rejection/channel-simulation procedures; follow its Harsha and Flamich references to their original versions before admitting algorithmic novelty. [exact date unresolved](https://doi.org/10.1137/080712720): Harsha et al., The Communication Complexity of Correlation: earlier rejection/channel simulation antecedent cited by the later analysis; conference/preprint/journal disclosure dates and exact equivalence require verification.

**Exclusion:** Rejected for the selected scalar residual identity because an exact maximal-coupling antecedent is directly verified in 2017. This does not reject the distinct application to parallel autoregressive model scoring; that systems target requires its own claim, earliest-disclosure audit and verifier.

**Next exact-claim audit:** If re-targeting, define the specific parallel block-scoring/application contribution and independently audit it; do not reuse the scalar packet as a 2022 novelty claim. Audit authors code, patents, workshop abstracts and talks; document the independent 2023 paper without using its later date as eligibility.

**Licensing:** Paper and code licenses must be checked separately at the actual version used; this survey links sources and authors original summaries without redistributing their text or code.

<a id="aperiodic-monotile"></a>

### Hat monotile aperiodicity theorem

**REJECTED for selected claim/assay · 3/10.** Historically meaningful mathematics, but outside the initial short-bridge/mechanically verified assay; retained to document domain-selection limits.

**Target:** Construct the hat tile and prove it tiles the plane while admitting no periodic tiling, including permitted reflections and the full substitution/hierarchy argument.

**A/B and bridge:** A: Substitution tilings, matching constraints and local-to-global hierarchy proofs. B: Geometric exact coordinates and complete classification of admissible local clusters. Bridge: Force every legal tiling to organize into larger metatiles recursively. No brief prerequisite pair or independent checker was established in this survey.

**Prospective verification:** A finite patch or animated tiling is insufficient. Need independently checked exact geometric construction and a universal hierarchy/aperiodicity proof, not only bounded searches. The published v1 is 89 pages and includes computer-assisted components.

**Empirical boundary:** Visual plausibility, finite patch generation and finite searches do not establish global aperiodicity.

**Date/source evidence:** Verified date in the arXiv v1 submission history, used as a disclosure-date proxy. First public announcement time and earlier talks, code, theses, abstracts and equivalent results are unresolved; this is not a certified earliest disclosure. Primary records: [v1, 2023-03-20](https://arxiv.org/abs/2303.10798v1), [v1, 2023-03-20](https://arxiv.org/pdf/2303.10798v1).

**Antecedent boundary:** [exact date unresolved](https://arxiv.org/pdf/2303.10798v1): The target reviews earlier aperiodic tiles and substitution methods; original sources and prepublication talks must be traced if revisited.

**Exclusion:** Rejected for this initial assay because no tractable independent universal proof checker or plausible short A/B bridge was identified; finite geometry demonstrations would certify a weaker claim.

**Next exact-claim audit:** Only revisit after specifying a sound independent geometric proof/certificate checker and prerequisite curriculum. Audit early author announcements, talks and code rather than relying on the preprint date.

**Licensing:** Paper and code licenses must be checked separately at the actual version used; this survey links sources and authors original summaries without redistributing their text or code.

## Bounded search record and remaining admission work

The actual research pass used primary web searches plus direct arXiv abstract/history, HTML and PDF version pages. Query themes included MeanFlow; SSD/Mamba-2; delta-rule parallelization; speculative residual/Gumbel/exponential-race sampling; TTT dual forms; SOAP/Shampoo/Adam; schedule-free optimization; Flow Matching/Rectified Flow; and LoRA/DoRA/frozen factors. Version dates and selected method sections were inspected for the registered targets; targeted antecedents included the online softmax normalizer, Rabe–Staats attention, weight normalization, fast-weight memory, the 2022 dual-form paper, 2020/2021 Shampoo versions and September 2022 transport methods. Unreliable guessed arXiv IDs were discarded after checking their titles; the registry uses the verified records.

For constructive mathematics and program synthesis, the pass checked official DeepMind announcements, Nature metadata/method text where accessible, official repositories and selected notebook/source cells. Read-only GitHub HTTP checks confirmed that the AlphaEvolve notebook contains the complex rank-48 construction and a coefficient verifier, and the AlphaDev source contains assembly routines/tests. It followed the official AlphaDev link to LLVM D118029. These checks establish the presence of artifacts, not independently verified correctness or first-public repository visibility. No repository code was executed. Some arXiv HTML endpoints were unavailable or rendered indexing errors; PDF was used when possible, and affected equations require a PDF comparison before implementation.

The dated official Qwen3 announcement was checked, and the completed separate immutable model audit was read for cross-file consistency. The separate model audit supplies the original April Qwen pins and archived Pythia evidence; these are not promoted here into candidate admission conclusions. Live pages and repository `main` were used only as audit leads; they need immutable archival references before experimental admission.

This pass **did not comprehensively search talks, slides, theses, patents, archived deleted pages, private-to-public repository transitions or every bibliography citation**. These are remaining work, not negative search results. Each candidate needs an exact-claim earliest-disclosure report, original antecedent comparison, immutable model/tokenizer/post-training release record, licensed eligible input manifest, independent verifier review and fresh prerequisite probes. Supplied A/B sources, prompts, retrieved corpus and bridge cues must all be audited for leakage. Search/admission criteria must be frozen before inspecting model hint effects; any later observed responsiveness belongs in a separate empirical screening record.

The survey is complete as a ranked source-backed selection artifact. No candidate is currently marked historically admissible, and no claim of autonomous discovery, absence of obscure precedent or empirical reproduction follows from this survey.
