# Research plan for useful idea generation in frozen language models

Prepared 11 October 2026 • Planning and literature research

## Recommendation

Start with a small, objectively verified study of **transferable bridge interventions**. Establish that a frozen model can perform prerequisite operations, struggles to compose them unaided, improves when given a minimal bridge, and can benefit on different-answer targets from an intervention extracted from other guided examples. Run the original perturb-and-recover idea as a second, compute-controlled experiment after this assay works. Neither experiment initially warrants the claim that a model has made a scientific discovery.

The generic perturb-and-recover proposal has direct prior art. The plausible contribution is a careful account of *when* latent interventions improve valid composition beyond strong token-space search, whether their effects transfer beyond answer leakage, and what causal evidence supports an explanation. An informative negative result is possible: an intervention may change diversity without increasing valid solutions, or improve the same task without transferring to a new deduction family.

Qwen3-1.7B is a reasonable first reference model because it is small, dense, openly available, and supports explicit thinking and non-thinking modes. Use Qwen3-0.6B to debug mechanics if necessary. Neither is guaranteed to support a useful scientific reasoning assay. On the RTX 2080 Ti, plan unquantized FP16 PyTorch/Transformers instrumentation and separately benchmark supported generation backends. Full activation-gradient studies may exceed 11 GB; that question requires measurement.

The research direction should be chosen through a meaningful problem, a defensible benchmark, and an explanation that survives attempts to falsify it. Reserve a later decision for a scientifically useful problem. Bin packing and generic agent infrastructure are not default destinations.

No experiments, software installations, model downloads, repository edits, compute purchases, or external contacts are part of this deliverable. All numerical budgets and thresholds below are proposed design choices, not measurements.

## 1 What the claims would mean

Separate five notions. **Diversity** is variation among outputs. **Originality** is distance from a specified reference set, preferably in solution structure rather than wording. **Correctness** is satisfaction of an independently checked specification. **Utility** is improvement on a task someone cares about, with costs and failure modes included. **Discovery** requires a correct, consequential result that was not previously available within a declared historical or prospective reference frame. A surprising wrong answer can be original; originality is not a substitute for correctness.

Use four levels of novelty. N0 means a new string; N1 means a distinct valid solution strategy within this experiment; N2 means a reconstruction unavailable in the frozen checkpoint's documented public history; N3 means a result new to the relevant research community. The entry experiment tests composition on new instances; a later multi-solution assay targets N1. Historical reconstruction may support N2 after an audit. N3 requires a current literature search and independent scientific validation; an old-checkpoint success alone cannot establish it.

**Retrieval** reproduces an available fact or solution. **Composition** applies known components to a new combination or instance. **Discovery** establishes new knowledge under the chosen reference frame. These are operational distinctions, not claims that internal computation divides neatly into three modules. Random synthetic worlds reduce exact-item memorization but do not erase learned algorithms or familiar templates.

| Claim | Positive evidence | What a negative result means |
| --- | --- | --- |
| Prerequisites are usable | Strong performance on A, B, and their immediate applications without bridge help | The assay cannot isolate a composition failure if prerequisite competence is absent |
| A bridge changes performance | Minimal bridge beats premises-only and matched irrelevant text on new instances | The chosen bridge, model, or task may be ineffective or already at ceiling |
| A bridge-derived intervention transfers | Frozen intervention improves unguided targets with different answers and held-out structure | A powered result can bound transfer for this intervention class; it does not show all latent interventions fail |
| Perturbation improves search | More distinct valid solutions per fixed compute than tuned sampling and refinement | A diversity-only effect supports exploration but not useful idea generation |
| A proposed computation matters | Specific bidirectional and path interventions predict selective behavioral changes | A failed ablation can reflect redundancy, compensation, misalignment, or a wrong hypothesis |
| Historical reconstruction occurred | A valid result from an eligible old checkpoint with audited inputs | Failure says little about modern models or the feasibility of human discovery |

The most defensible first paper question is: **Can a bridge-conditioned activation intervention improve composition in a frozen small language model across answer-balanced instances, and which transfer and compute controls eliminate apparent gains?** The checkpoint remains frozen, but donor selection and intervention tuning are supervised method development. Report that assistance explicitly; “no weight training” does not mean “no learned intervention.”

“Ordinary sampling misses” means lower success within a stated finite budget. It does not generally mean that the successful string has zero probability under the unmodified model.

## 2 Prior art and the possible contribution

**Perturbing and recovering is already studied.** [Noise Steering](https://arxiv.org/abs/2604.03380), published in [BEA 2026](https://aclanthology.org/2026.bea-1.41/), applies Gaussian noise to embeddings, attention, or residual states and decays it to zero. Its educational Arabic story evaluation does not establish scientific discovery. Its fixed-temperature comparison motivates stronger tuned sampling controls here. Do not claim to invent temporary disruption followed by clean continuation.

[Soft Reasoning](https://arxiv.org/abs/2505.24688) perturbs the first reasoning-token embedding and searches perturbations using Bayesian optimization. Any reported end-to-end gain combines the perturbation with search and verification; the new study must charge for those components separately. [FIRE](https://arxiv.org/abs/2410.21236) explores high-temperature first-token sampling followed by ordinary decoding and is a particularly relevant cheap control. [Soft Thinking](https://arxiv.org/abs/2505.15778) is a different approach using soft token mixtures, useful for locating the wider latent-reasoning literature rather than as the initial local implementation.

[LatentTTS](https://arxiv.org/abs/2510.07745), also in the [ACL 2026 proceedings](https://aclanthology.org/2026.acl-long.2069/), searches continuous latent reasoning trajectories in specially prepared latent models. [GTS](https://arxiv.org/abs/2602.14077) learns latent-noise mechanisms. These motivate search-space questions but do not demonstrate a plug-and-play intervention on an arbitrary frozen text-reasoning model. Preserve the distinction between a frozen inference checkpoint and a method whose latent interface required training.

[CreativityNeuro](https://arxiv.org/abs/2607.01433) studies inference-time weight rescaling and a measured originality–utility tradeoff. Its claims must be assessed at the level of the evaluated tasks and judges. A result on creativity scoring is not evidence of correct scientific invention. Parameter interventions remain a later branch here because they affect many computations and complicate restoration and cache semantics.

**Transferable activation vectors also have substantial prior art.** [ActAdd](https://arxiv.org/abs/2308.10248) extracts activation differences from contrasting prompts. [Contrastive Activation Addition](https://arxiv.org/abs/2312.06681) averages paired residual differences to steer behavior. [Function Vectors](https://arxiv.org/abs/2310.15213) provides causal evidence that task representations extracted from demonstrations transfer to new contexts, including some composition. [In-Context Learning Creates Task Vectors](https://arxiv.org/abs/2310.15916) similarly compresses demonstrations into internal task representations. Calling a vector a “bridge” does not itself add a contribution.

The proposed addition is a conjunction of controls: prerequisites independently demonstrated; minimal relational help separated from answer help; donors with different answers; transfer to held-out rules or mechanisms; bridge-inapplicable controls; independent free generation; and comparison with tuned, compute-matched search. An intervention that only makes the model more confident, verbose, compliant, or likely to emit a familiar answer format should fail this conjunction.

The causal methodology follows the distinctions emphasized in [patching best practices](https://arxiv.org/abs/2309.16042) and [interpreting activation patching](https://arxiv.org/abs/2404.15255). [AtP*](https://arxiv.org/abs/2403.00745) supplies a later efficient candidate-ranking method, while [IOI circuit analysis](https://arxiv.org/abs/2211.00593) illustrates stronger circuit-level tests. These are methodological foundations, not evidence that the proposed bridge exists as a single direction.

For an eventual executable discovery assay, [FunSearch](https://www.nature.com/articles/s41586-023-06924-6) shows the value of pairing a pretrained generator with an objective evaluator and iterative program search; the [authors' account](https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/) describes the generation–evaluation loop. [MAP-Elites](https://arxiv.org/abs/1504.04909) motivates measuring diverse high-quality solutions. These support an evaluation architecture, not a commitment to bin packing or a claim that perturbations caused a discovery.

## 3 The dataset strategy

### Controlled worlds first

The first assay should have a finite specification, an exact answer or proof checker, explicit prerequisite probes, and a bridge that names a reusable operation without supplying the target result. Use newly generated instances whose answers and surface vocabulary are balanced. Keep the generator separate from the verifier so one implementation bug cannot certify itself.

For the primary composition claim, the bridge must be derivable from information already available in the unguided world. A hint to eliminate an intermediate variable changes strategy; supplying a previously absent physical law changes information. Both are legitimate studies, but an information-theoretically underdetermined unguided question cannot diagnose missing computation. Treat UNKNOWN and INCONSISTENT as separate outputs.

**First competence calibration: cancellation of nuisance offsets.** Two instruments have unknown constant additive offsets. Instrument 1 reads A = 17 and B = 11. Instrument 2 reads B = 25 and C = 22. Ask for the true difference A − C. Within-instrument differences give A − B = 6 and B − C = 3, hence A − C = 9. A minimal bridge says: “Compare readings made with the same instrument before combining comparisons.” It contains no target number.

Probe subtraction, recognition of a shared offset, chaining signed differences, and the distinction between relative and absolute identifiability separately. Hold out values, names, graph topology, edge orientation, number of instruments, and distractor placement. Include disconnected graphs requiring UNKNOWN, inconsistent measurements requiring an inconsistency report, and per-reading offsets for which cancellation is invalid. Check identifiability with exact rational linear algebra: a queried linear functional must be invariant over every solution of the observation equations. A second verifier can enumerate small integer worlds or check a proof certificate on an appropriately restricted subfamily. Specify those subfamilies so bounded enumeration does not falsely prove unbounded identifiability.

This arithmetic example may be too easy. That is useful calibration information. Increase structural complexity before increasing arithmetic burden, because the desired bottleneck is composition. Do not select only instances on which the model failed; keep a prospectively defined cohort and report all results, with a separately declared prerequisite-competent subgroup.

The offset assay has one identifiable numeric answer, so it measures correctness and composition, not diversity of useful ideas. Do not score differently worded proofs as novel strategies without a validated proof-equivalence scheme. A later idea-generation assay must admit multiple independently checkable solutions, rules, or hypotheses and a declared equivalence relation. A perturbation null on single-answer arithmetic cannot establish absence of a creativity benefit elsewhere.

**Second concrete assay: state augmentation in a small navigation world.** Use four rooms and a one-bit badge; doors can require or toggle the badge. A path can need to revisit room A with a different badge state, as in A0 → B1 → C0 → A1 → D. The bridge is to treat the pair (room, badge) as the state. Specify all transitions in the prompt; exact breadth-first search over at most eight states verifies reachability and any shortest path. Hold out graph topologies, not merely room names. Include plain maps with an irrelevant badge, unreachable goals, and instances where room-only search is already sufficient. This is conceptually more distinct from offset cancellation than another additive or XOR invariant.

Two alternatives prevent this convenient toy from defining the project. **Typed relational worlds** provide facts and a small rule set, with a bridge such as “the output type of relation A matches the input type of relation B”; forward chaining gives exact entailment and countermodels. **Finite transformation worlds** use small permutations or affine maps with a reusable conjugation, inversion, or composition rule; exhaustive evaluation checks the result. Unseen numbers or renamed objects are instance holdouts. Unseen proof graphs, composition rules, or nuisance mechanisms are structural holdouts. Transfer between these worlds is a harder, separately labeled test, not something assumed from a successful arithmetic patch.

A later scientifically motivated synthetic family could use dimensional analysis, observability, invariants, or nuisance cancellation in simplified physical models. The laws and observations would be fully specified. It would test rediscovery within a designed world, while remaining distinct from an open astrophysical discovery.

### Smallest viable benchmark

Proposed starting allocation: 24 mechanics cases, 48 donor cases, 96 development cases, and 160 sealed confirmation worlds. Donor and development instances come from two predefined structural families. Confirmation contains 80 new instances from those families and 80 from two held-out structural families. Include negative and UNKNOWN cases within each eligible stratum. Use four generation seeds per confirmation world if the pilot budget allows. More seeds reduce Monte Carlo noise; they do not create more independent worlds or families.

The first 24 cases test formatting, competence, and identifiability, not the hypothesis. The 48 donors supply bridge versus control activations, with answer distributions balanced. Development chooses exactly one primary intervention and its locations. Confirmation data and verifier outputs remain sealed until configurations are frozen. Four structural families are a minimum demonstration, not evidence of universal transfer. If initial effects survive, expand to at least six substantially different families and report family-specific effects rather than hiding heterogeneity in a single average.

For feasibility, those four structural families may initially be two graph motifs within each of the offset and badge mechanisms. Use separate donor libraries for different mechanisms. This tests held-out structural transfer within a mechanism; transferring one offset-derived direction into badge reasoning is a stronger, exploratory cross-mechanism claim. Preassign disjoint donor and recipient answer pools where the task permits, so enforcing different-answer donors does not adapt vectors to hidden test labels. Record how many genuinely different mechanisms, structures, and instances each result covers.

### Existing datasets and their roles

| Resource | Appropriate use | Limitation for this project |
| --- | --- | --- |
| [ResearchBench](https://aclanthology.org/2026.findings-acl.644/) and [repository](https://github.com/ankitala/ResearchBench) | Inspiration retrieval and combining precursor ideas; later naturalistic evaluation | Published-paper dates do not establish checkpoint eligibility; curated inspirations are assistance |
| [DiscoveryBench](https://arxiv.org/abs/2407.01725) and [repository](https://github.com/allenai/discoverybench) | Data-grounded hypotheses, analysis, and verifier design | Often requires data analysis/tools; not a direct test of pretrained conceptual invention |
| [CUSP](https://arxiv.org/html/2605.22681v1) | Candidate events and temporal metadata to audit | The [detailed auditor](https://arxiv.org/html/2605.22681v1#A7.SS1) explicitly exempts matching methods and numerical predictions; its named-entity judgment does not establish training provenance |
| [Reconstruction](https://arxiv.org/abs/2608.16645) | Bibliography-conditioned reconstruction protocol and critique | Acknowledges parametric contamination; reconstruction scores are not proof of historical novelty |

ResearchBench's code is MIT, while its gated dataset states CC-BY-NC-4.0 plus access terms including redistribution restrictions. Preserve the exact terms in the manifest; do not redistribute the corpus under the code license. DiscoveryBench's database is ODC-By, with underlying source datasets requiring item-level review. CUSP's official dataset card labels the data MIT, while upstream source-content terms still matter. Reconstruction's public benchmark/code terms remain unresolved. A paper's open-access license never automatically licenses its benchmark, source papers, or external data. Newly authored synthetic data can receive an explicit license once ownership and dependencies are clear; CC0 or CC-BY for data and MIT for original code are possible later choices, not decisions made here.

### Historical audit after the causal pilot

No historical item in this plan is securely audited. The admission rule is stronger than an advertised knowledge cutoff: the **actual frozen checkpoint, including post-training, must have been publicly released before the earliest public disclosure of the claimed target contribution**. A later revision of an older base checkpoint does not qualify automatically. Record immutable model and tokenizer revisions, release evidence, preprint versions, talks, slides, code, abstracts, patents where relevant, and precursor results. A journal date alone is insufficient.

For each candidate, write the exact proposition being reconstructed, the best earlier result, the new contribution, prerequisite A, prerequisite B, and every input the model receives. Audit whether the bridge or A/B selection already expresses the discovery. Hindsight selection of a promising pair is meaningful human assistance even if neither source contains the answer. Report unassisted, corpus-constrained, selected-prerequisites, and bridge-assisted conditions separately. Search access, if later added, must use a frozen eligible corpus with logged retrieval; an unrestricted modern tool can destroy the temporal claim.

Possible domains are short mathematical identities, small algorithmic improvements with executable checks, and specific physical-model deductions with available pre-discovery observations. Select by auditability and prerequisite competence, not celebrity. Attention algorithms illustrate the difficulty: [Rabe and Staats](https://arxiv.org/abs/2112.05682) predates [FlashAttention](https://arxiv.org/abs/2205.14135). Recovering memory-efficient exact attention is not necessarily reconstructing FlashAttention's particular contribution. A historical item passes only when its target distinction has been written and independently checked.

An old checkpoint succeeding on a later result supports historical reconstruction under the audited inputs. It does not prove absence of obscure precursor knowledge, autonomy, novelty today, or the same internal mechanism as the human discovery. Ambiguous cases belong in a separately labeled exploratory set.

A concrete candidate for a later audit is the algebraic core of [Direct Preference Optimization](https://arxiv.org/abs/2305.18290v1), first submitted 29 May 2023: combine the KL-regularized policy–reward relation with a pairwise preference likelihood and cancel the context-dependent normalization term. An archived pre-disclosure [Pythia release](https://github.com/EleutherAI/pythia) is a plausible checkpoint family to investigate, not an eligible checkpoint certified here. Verify the derivation symbolically and on finite-action examples with varied policies and temperatures. Reconstructing the identity would not reproduce the paper's empirical alignment results. Exact archived release evidence, earlier equivalent disclosures, and prerequisite competence remain open; the local Qwen3 model cannot supply the historical timing claim for this 2023 result.

## 4 The causal bridge experiment

### Prompt conditions and prerequisite gate

Use a common question, output schema, and preregistered token budget. Preserve raw rendered prompts and token IDs. The conditions below have different purposes and must not be pooled as “guided.”

| Condition | Information supplied | Role |
| --- | --- | --- |
| Unguided | Task and ordinary observations only | Practical baseline |
| Premises only | Explicit A and B, without their useful relationship | Separates missing knowledge from composition |
| Minimal bridge | A reusable relation or operation linking A and B, no answer | Primary guided donor |
| Full explanation | Worked reasoning, including answer-bearing content if needed | Ceiling and leakage diagnostic |
| Answer only | Correct target output without derivation | Measures answer/format information |
| Wrong bridge | Plausible but invalid relation, matched in presentation | Specificity and suggestibility |
| Irrelevant control | Length/style-matched true but unhelpful material | Extra context and compliance control |
| No-op intervention | Same execution path with identity patch or zero amplitude | Instrumentation control |

Length matching is a diagnostic, not a guarantee of matched information. Match token counts where possible and also test natural paraphrases rather than relying on awkward padding. Include alternate valid bridges where available. The suggested assay gate is at least 85% prerequisite accuracy on development and a bridge lift of at least 15 percentage points on the selected task family. These are design heuristics to avoid a floor or ceiling, not tests of a universal principle. Failure triggers task simplification or a model-capacity decision before causal interpretation.

### Teacher forcing and alignment

A decoder-only model cannot revise an earlier prefix state in response to later tokens. Teacher forcing a bridge changes the states at and after that bridge and their subsequent descendants; it changes neither earlier prefix activations nor frozen weights. Before any causal study, require a test showing identical earlier-prefix states for runs that share a prefix but differ in a later forced continuation, within calibrated numerical tolerance.

For the primary extraction, force only the minimal bridge or its matched control, followed by a neutral common cue. Capture states **after bridge consumption and before any answer-bearing continuation**. If a bridge logically makes the answer easy, that is expected assistance; the extra protection is cross-instance transfer to a different target answer. Full explanations and answer-only donors remain leakage diagnostics. Teacher-forced answer likelihood is a localization instrument, not the primary success metric.

Align by semantic role: final observation, end of premise B, end of bridge/control, common continuation cue, and designated generation steps. Save exact token spans, absolute positions, position IDs, attention masks, and an alignment rationale. Equal token index is insufficient when sequences have different meanings. Compare natural semantic alignment with a length-matched condition to detect position or rotary-embedding artifacts. Exclude ambiguous alignments prospectively, with their frequency reported.

### Transfer and exact interventions

On donor data, compute paired differences between minimal-bridge and matched-control residual states at selected semantic sites. Start with the mean difference, inspect individual donors, and retain the mean separately if later decomposing variation. Each target receives either a donor from another world or an aggregate built from disjoint donor worlds. The donor must have a different answer; balance shared and disjoint answer-token forms, signs, magnitudes, and UNKNOWN status where meaningful.

First test whole-state replacement within the same instance as a localization diagnostic. Then test cross-instance replacement, which may overwrite target-specific content, and additive mean-delta interventions, which may preserve more target information but produce unnatural states. Do not confuse these estimands. Freeze a small set of layer, position, and amplitude choices using development data only. Apply the selected intervention to a target with no bridge text and let it generate freely.

Run both directions: guided-to-unguided patches test whether the selected state can supply useful information; unguided-to-guided patches test whether replacing it disrupts the guided computation. The latter is not a proof of absolute necessity, especially when circuits are redundant. Add negative directions, shuffled donor labels, matched random vectors, answer-only vectors, and irrelevant-text vectors. Test tasks on which the bridge is inappropriate: a general confidence or compliance boost should not cause confident numeric answers to unidentifiable problems.

Include a generic “reason carefully” contrast and an ordinary demonstration-derived task-vector baseline under the same extraction budget. If these match the bridge intervention, report generic task elicitation as a viable explanation. Add bridge-unnecessary targets, where a genuine selective benefit should be small, and keep prerequisite probes in fresh contexts so administering a probe does not itself teach the subsequent target.

A concrete mechanistic prediction for the offset assay is that a useful intervention improves cancellation and composition while preserving UNKNOWN judgments and ordinary subtraction. If it mainly increases the probability of a number, mirrors the donor's answer, or degrades bridge-inapplicable cases, the “bridge computation” explanation is weakened. Report target correctness, donor-answer copying, invalid confident answers, output length, and a small unrelated competence panel together.

### Strength of the causal conclusion

A large activation delta is a description of changed context, not proof of a missing concept. A successful patch establishes sufficiency under the tested intervention and recipient state; it may bypass the model's native solution route. Conversely, a failed single-site ablation can miss distributed or redundant computation. Check joint patches, resampled replacements, and rescue experiments before asserting absence.

Monitor activation norms, downstream distribution shifts, fluency, and performance on controls. Interpolate between real donor and recipient states, compare several naturally occurring donors, and test low amplitudes. These are useful off-manifold diagnostics; none proves that an intervention lies on a meaningful neural manifold. A mechanistic account needs selective predictions on new counterfactuals and, later, evidence about component interactions. Textual reasoning is another behavioral output: [work on unfaithful chain-of-thought explanations](https://arxiv.org/abs/2305.04388) shows why plausible prose cannot certify the internal explanation.

## 5 Perturb and recover with fair search controls

Run this experiment only after the verifier and baseline task distribution are credible. Its primary question is whether perturbing internal state buys useful exploration beyond ordinary sampling at the same cost. Keep an independent test set if development has already used the first benchmark's confirmation labels.

Begin with embedding or residual interventions; defer attention-weight and parameter perturbations until hook and cache semantics are understood. Random noise should be isotropic Gaussian scaled relative to a development-estimated residual RMS, with vector dimension accounted for. Structured alternatives include the bridge mean direction, its negative, a random direction matched in norm, and a low-rank donor subspace. Keep random versus structured noise separate from whether any verifier selects among candidates.

Use a small development-only grid: for example, three layer bands, two windows, and three nonzero relative amplitudes plus zero. A window can be the first generation step or an early 8-token interval; set a specified linear or exponential decay to exactly zero. This is at most 18 nonzero combinations per perturbation type before any additional choices. Record all attempted configurations and their development costs. Avoid combining layer, window, amplitude, covariance, schedule, and task into an unbounded search.

Run strong baselines: a development-tuned temperature/top-p policy, prompt paraphrases, more independent ordinary samples, a high-temperature first-token condition, and clean draft–critique–refine at equal total cost. When a method receives a verifier or reward-guided search, give the same information and selection opportunities to its comparison. Include raw candidate yield and selected-result yield. Choosing the best answer after observing hidden test correctness is an oracle metric, not a deployable method.

Keep token-sampling RNG, perturbation RNG, donor RNG, and data-generation RNG separate. Reusing a common sampling seed can reduce paired variance, but different trajectories consume randomness differently; use a documented per-step coupling where possible and do not claim identical seeds imply identical sampled paths across engines.

### Recovery has three distinct meanings

**Retained-cache continuation.** Turn noise off and continue using the existing KV cache. Earlier noisy states can remain encoded in keys and values, depending on where the hook acted, while generated tokens also carry their effects. This is operational recovery with persistent history.

**Clean re-prefill.** Turn noise off, discard the full cache, and recompute the exact original prompt plus the generated prefix under the clean model before continuing. This removes perturbed internal cache states but preserves the changed text. Charge for the repeated prefill. Never reuse a cache after altering the prefix or intervention history.

**Separate clean refinement.** Start a new clean context containing the problem and noisy draft, then request a revision. This measures a generator–refiner system. Its control is a clean draft plus the same clean refinement, with equal budgets and instructions.

Compare all three after selecting a small number of perturbations. Also replay saved prefixes with clean re-prefill to separate text-mediated effects from retained-state effects. If parameter perturbations are eventually attempted, restore from a pristine state, verify tensor hashes, clear or explicitly retain caches as assigned, and confirm clean outputs recover. Parameter changes are unnecessary for the first project.

## 6 The measurement ladder

1. **Behavior and invariants.** Establish correctness, competence, bridge lift, exact tokenization, and no-op equivalence. These gates precede interpretation.
2. **Targeted activation capture.** Save selected residual sites on short sequences in inference mode. Summaries include norm, paired delta, cosine similarity, and variation across instances. Do not dump every activation for every generated token.
3. **Exact patching.** Sweep a modest number of layers and aligned sites; evaluate restoration, disruption, negative controls, and independent free generation. This establishes the basic intervention effects.
4. **Activation gradients and attribution patching.** With weights frozen, allow gradients only through the needed activation computation and a local, declared score. A gradient–delta inner product ranks candidates under a first-order approximation. Saturation, nonlinear interactions, and cancellation can make it wrong; validate top-ranked and randomly sampled low-ranked sites with exact patches. AtP* explicitly studies approximation failure modes. No optimizer or parameter updates are needed.
5. **Mean and spectral structure.** Form a matrix of donor deltas using only extraction/development data. Keep the mean delta as its own candidate. Compare uncentered SVD with centered PCA; centering can remove the very shared effect being sought. Choose rank on development, use shuffled contrasts and bootstrap stability as controls, and judge components by held-out intervention effects rather than variance explained.
6. **Component and path tests.** Only after a reproducible effect, distinguish MLP, attention-output, and residual contributions, then test nominated paths. Include joint interventions to reveal redundancy. Reproduce counterfactual predictions on a new family before describing a circuit as an explanation.

Avoid large Hessian studies or unsupervised spectral fishing at the outset. The relevant measurement is whether a precise intervention changes a verified behavior selectively. A gradient of answer likelihood can identify an answer direction rather than an abstract bridge; use answer-balanced donors, alternative score definitions, and generation validation. Correct-answer versus plausible-wrong-answer logit differences are useful where tokenization permits, but multi-token and UNKNOWN answers require explicitly defined sequence scores. Report raw probabilities and verified accuracy alongside normalized restoration scores, whose denominators can be unstable.

Maintain an exploration ledger. Every layer, metric, rank, prompt, donor policy, and noise configuration chosen after seeing results belongs in development. Confirmation evaluates frozen choices; a failed confirmation followed by a revised hypothesis requires new confirmation data.

## 7 Models and local execution

### Choice of reference checkpoint

Choose Qwen3-1.7B provisionally for the scientific pilot and 0.6B for a short mechanics fallback. This balances a simple dense architecture, accessible instrumentation, and local capacity; it is not a claim that the newest or smallest model is scientifically best. Keep one model and one thinking mode fixed for the first confirmatory comparison. Select difficulty by prerequisite competence and guided headroom. If neither size supports the assay, change the task or justify a larger-model replication before interpreting intervention failures.

The official [1.7B](https://huggingface.co/Qwen/Qwen3-1.7B) and [0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) cards identify Apache-2.0 models with pretraining and post-training. The cards require Qwen3-capable Transformers, at least 4.51.0. For thinking mode, the stated starting sampling settings are temperature 0.6, top-p 0.95, top-k 20, and min-p 0; the card warns against greedy decoding. Preserve seeded sampling for substantive thinking-mode baselines. Greedy or teacher-scored runs can still serve clearly labeled engineering diagnostics. Count reasoning tokens within the output budget and report incomplete reasoning/truncation rather than silently extracting a guessed final answer.

The [1.7B configuration](https://huggingface.co/Qwen/Qwen3-1.7B/blob/main/config.json) has residual width 2,048, and the [0.6B configuration](https://huggingface.co/Qwen/Qwen3-0.6B/blob/main/config.json) width 1,024. Both specify 28 layers, 16 query heads, 8 KV heads, and head dimension 128. Both configurations advertise BF16 weights. The card's 32,768-token context and config's 40,960 maximum positions are distinct fields; neither is the proposed local sequence length. Begin far below either.

### Hardware and current documentation

The RTX 2080 Ti is Turing, compute capability 7.5. NVIDIA documents FP16 tensor-core operations; native BF16 support is absent on this generation. Request FP16 explicitly rather than copying a BF16 or dtype-auto example, and check numerical behavior after conversion from released BF16 weights. A software BF16 tensor or emulated operation does not establish native acceleration. Sources: [NVIDIA GPU table](https://developer.nvidia.com/cuda/gpus), [Turing tuning guide](https://docs.nvidia.com/cuda/turing-tuning-guide/index.html), and [PyTorch BF16 capability API](https://docs.pytorch.org/docs/main/generated/torch.cuda.is_bf16_supported.html).

Current primary-source checks on 11 October 2026 found [PyTorch 2.14](https://pytorch.org/blog/pytorch-2-14-release-blog/), [Transformers 5.19.0](https://github.com/huggingface/transformers/releases/tag/v5.19.0), and [vLLM 0.31.0](https://github.com/vllm-project/vllm/releases/tag/v0.31.0). These are research-time references, **not a tested dependency lock**. A current web page, model-card minimum, and installed binary can disagree. Inspect the chosen wheel's architectures and driver compatibility during authorized setup, then pin the tested stack. Preserve an independent vLLM environment because its compiled kernels depend on its own PyTorch/CUDA combination.

| Execution path | Planned purpose | Support and limitation |
| --- | --- | --- |
| PyTorch plus Transformers | Canonical FP16 hooks, exact patches, later activation gradients | Eager, uncompiled reference first; inspect pinned Qwen3 modules |
| llama.cpp CUDA | First efficient generation candidate | Qwen3 and CUDA Turing supported; F16 conversion parity and throughput still require checks |
| vLLM FP16 | Conditional benchmark competitor | Current docs explicitly include compute capability 7.5 and RTX20xx; 11 GB usability remains unmeasured |
| SGLang | Deferred option | Current installation and SM75-specific issues need a bounded compatibility review; no verified local recommendation here |

Relevant official sources are the [PyTorch module-hook API](https://docs.pytorch.org/docs/2.14/generated/torch.nn.Module.html), [autograd notes](https://docs.pytorch.org/docs/main/notes/autograd.html), [Transformers Qwen3 documentation](https://huggingface.co/docs/transformers/en/model_doc/qwen3), [cache explanation](https://huggingface.co/docs/transformers/en/cache_explanation), [llama.cpp build documentation](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md), [native server documentation](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md), and [vLLM GPU requirements](https://docs.vllm.ai/en/latest/getting_started/installation/gpu/). The [vLLM attention-backend](https://docs.vllm.ai/en/latest/design/attention_backends/) and [quantization](https://docs.vllm.ai/en/latest/features/quantization/) matrices should be checked for the pinned release rather than relying on old universal claims about Turing.

The mainstream [FlashAttention-2 package](https://github.com/Dao-AILab/flash-attention) targets newer NVIDIA architectures and points to a separate Turing subset implementation. This does not imply that llama.cpp's own similarly named attention kernel has the same restriction. Start the PyTorch reference with eager attention and benchmark supported alternatives separately. [SGLang's installation documentation](https://docs.sglang.io/docs/get-started/install) and its [SM75 lifecycle discussion](https://github.com/sgl-project/sglang/issues/6006) do not together certify the desired complete setup; a closed issue is not proof of a final support policy.

### Two paths with explicit parity checks

Reference instrumentation should use eval mode, frozen parameters, batch one, no compile, no quantization, and cache off for initial full-prefix comparisons. Map each hook to a precise operation: block input, attention output, MLP output, residual addition, or normalization boundary. These are not interchangeable. For later activation gradients, inference mode must be off and a selected activation or input embedding must require gradients. Freezing every parameter while feeding integer token IDs otherwise creates no useful autograd graph. Use a local scalar objective and selective gradient computation, with short FP32 and finite-difference checks where feasible.

Fast backends produce token IDs, textual reasoning, and optional tool-call records. These **textual traces are not internal tensor traces**. Public serving APIs should not be assumed to support arbitrary residual replacement, activation gradients, or path patching. Keep causal experiments in the reference engine unless an optimized backend has separately validated hooks.

Use a canonical immutable Hugging Face snapshot. A llama.cpp F16 GGUF should derive from that snapshot with a pinned conversion recipe; Q8 and Q4 are separate numerical treatments. Match tokenizer files, chat template, template arguments, input token IDs, BOS/EOS/stop tokens, thinking mode, sampling filters, output budget, and cache precision. Save unparsed raw outputs. The current llama-server documents thinking template arguments even where an older Qwen guide warns otherwise; rendered token-ID checks settle the actual local behavior.

Compare fixed-prefix logits or teacher-scored log probabilities, then task-level output distributions. Equal seeds do not guarantee identical sampled sequences across kernels or backends; [vLLM's reproducibility guidance](https://docs.vllm.ai/en/latest/usage/reproducibility/) is explicit about execution conditions. Replaying text generated by a quantized engine through FP16 PyTorch is useful analysis of that text but does not turn it into an FP16-generated baseline.

Benchmark Transformers FP16, llama.cpp F16, and Q8 separately; add vLLM if its bounded smoke test passes. Proposed workload grid: prompts of 128, 512, and 2,048 tokens and outputs of 128, 512, and 1,024 tokens, initially one sequence, then modest concurrency. Record cold start separately from warm prefill, time to first token, decode rate, total item latency, completed and verified-successful traces per hour, peak VRAM, truncations, and sustained thermal effects. Use [llama-bench's documented metrics](https://github.com/ggml-org/llama.cpp/blob/master/tools/llama-bench/README.md). Choose the best measured feasible backend for the actual workload, not an unmeasured “fastest” engine.

### Memory estimates and calibration

The following arithmetic assumes batch one and FP16 storage. GB means decimal bytes; GiB and MiB are binary units. It excludes allocator reserve, CUDA context, workspaces, live intermediates, display use, and fragmentation.

| Allocation | Qwen3 1.7B | Qwen3 0.6B |
| --- | --- | --- |
| Approximate raw weights | 3.4 GB or 3.17 GiB | 1.2 GB or 1.12 GiB |
| KV cache per token per sequence | 112 KiB | 112 KiB |
| KV cache at 4,096 tokens | 448 MiB | 448 MiB |
| One residual site in all 28 layers at 4,096 positions | 448 MiB | 224 MiB |
| Same residual site at 32 selected positions per layer | 3.5 MiB | 1.75 MiB |

The KV calculation multiplies two tensors by 28 layers, 8 KV heads, 128 dimensions, sequence length, batch size, and two bytes. The smaller model therefore does not halve KV memory. Full 4,096-position vocabulary logits would occupy about 1.16 GiB in FP16 or 2.32 GiB in FP32. All-layer, 16-head, 4,096-by-4,096 attention matrices in FP16 would require about 14 GiB by themselves. Avoid indiscriminate attention or full-logit capture.

Calibrate measured peak allocated/reserved memory at 256, 512, and 1,024 total tokens, then increase only as justified. Compare no capture, one selected site, bounded patching, and selected positions across layers. Use sequential donor and recipient passes on one resident model. A provisional policy is to stay below 80–85% of *measured available* VRAM. Record host RAM and disk as well; they have not been established for this machine.

Freezing parameters removes optimizer and parameter-gradient storage, not backward activation memory. Start gradient mechanics with a short suffix and a local objective, cache disabled. Shorten, capture fewer sites, or use 0.6B before renting. If a scientifically necessary competent model or suffix cannot fit, prepare a separate rental decision with measured requirements, provider options, capacity, time cap, and price approval. A modern 24 GB GPU may be a sufficient next step; no need for an H100 has been demonstrated and no spending is authorized.

## 8 Statistical design and decision rules

Define one primary transfer comparison: the frozen cross-instance bridge-delta intervention against the unmodified unguided baseline, both with complete task information. Matched irrelevant-delta, random-direction, generic-elicitation, and task-vector controls test specificity. A harmful sham cannot create a positive result by making the comparison artificially easy. Report premises-only performance separately. For the minimum study, the primary population is the fixed weighted mixture of 160 confirmation worlds; the 80 held-out-structure worlds form a separately reported secondary stratum. Choose a minimum worthwhile gain before confirmation; a proposed threshold is 5 percentage points in verified success, with 10 points as a more detectable early target.

For the subsequent perturbation study, use a new primary comparison against the strongest development-selected ordinary-search policy at a fixed operational budget. If both studies are jointly presented as confirmatory, preregister the two primary hypotheses and control their familywise error, for example with Holm correction. Secondary layer maps, ranks, novelty metrics, and family interactions are exploratory unless separately powered and registered.

The independent unit is the underlying world or problem. Average seeds within each world, retain paired method differences, and use a world-level paired bootstrap or an appropriate paired model. Keep paraphrases, counterfactual variants, and related donor worlds in the same split and resampling cluster. With only a few families, report results for each and avoid pretending that a family-level bootstrap estimates broad domain generalization reliably. Later human judgments need both stimulus and rater uncertainty.

A rough planning approximation for one paired binary outcome gives a required number of independent worlds equal to about 7.84 times the methods' disagreement probability, divided by the squared target improvement. At disagreement probability 0.2, detecting 5 points with roughly 80% power at a two-sided 5% level takes about 627 worlds; 10 points takes about 157. At disagreement probability 0.4, both counts double. This ignores several complications and is not a sample-size guarantee. Use the pilot's world-level variance and clustering to recompute precision before opening confirmation data. Four seeds on 160 worlds do not imply 640 independent problems.

Those examples test against zero improvement. Demonstrating that the lower confidence bound exceeds a 5-point worthwhile threshold is harder: a true 10-point effect has only a 5-point margin above that threshold. Recalculate power for the actual decision rule, multiplicity, donor variability, and within-world seed averaging. If estimating generalization over donor libraries, use repeated independently constructed libraries and a crossed or hierarchical analysis; one fixed library supports a conclusion conditional on that library.

The 160-world minimum therefore supports pipeline validation and detection of some large effects. If budget cannot support the needed precision, explicitly label the result exploratory or inconclusive. It is better to state a wide interval than to rename a pilot a definitive creativity test.

The held-out-structure stratum has only 80 worlds, and each of its two families only 40. Do not apply the 157-world example to those smaller strata. If held-out structural transfer is promoted to the confirmatory primary claim, enlarge and power that stratum before unblinding. Predefine error guardrails, for example at most a 5-point rise in false definite answers on UNKNOWN cases and at most a 5-point drop on unrelated competence tasks. These margins are proposed choices; establishing them with confidence may require additional controls and sample size. An imprecise guardrail result prevents a strong utility claim.

### Fixed budgets and selection accounting

Proposed initial cap: at most one million generated tokens and six measured local GPU-hours for behavioral calibration and intervention development, stopping at whichever cap is reached first. Reduce the development grid rather than silently increasing the budget. Before confirmation, use measured runtime to choose and freeze a feasible cap; an illustrative ceiling is four million generated tokens and 72 local GPU-hours for the initial transfer study, including its controls. These are limits, not expected runtime, and the researcher should decide whether they fit the available time. Prefill tokens, backward passes, and verifier work receive separate accounting.

For fair search, set the primary budget in measured GPU time on one fixed execution stack, with synchronized timing and randomized method order. Also report generated/prefill tokens, model passes, candidate counts, CPU verifier time, and development cost. A same-token analysis helps separate algorithmic gains from implementation overhead; a wall-time analysis captures practical usefulness. Across engines, performance comparisons and causal comparisons are distinct experiments. Charge for failed candidates, verifier selection, re-prefill, refinement, and direction extraction. Report both first-use and amortized costs of an intervention library.

Metrics should include unselected verified success; distinct valid strategies after canonicalization; oracle pass-at-k or coverage; actual selector success; invalid output and contradiction rates; and useful solutions per budget. Oracle coverage is an upper bound when the correct candidate cannot be recognized at deployment. Keep diversity and originality measurements separate, state the reference archive, and inspect the Pareto tradeoff with correctness. Semantic-embedding distance and an LLM creativity judge are secondary measurements rather than proof of scientific novelty.

### Go and stop criteria

**Strong go:** the primary confidence interval lies above the worthwhile-effect threshold relative to the unmodified baseline, leakage and no-op tests pass, the declared error guardrails are supported, and the effect appears in independent free generation. A specifically bridge-related claim also needs evidence beyond the generic-vector controls. **Promising:** the estimate is positive but precision does not distinguish negligible from worthwhile gains or settle guardrails; expand only under a declared new study. **No-go for this tested method:** a sufficiently precise interval excludes the worthwhile gain, or controls explain the effect as answer copying or generic response bias. **Inconclusive:** the assay fails prerequisite or guided-headroom gates, instrumentation is unstable, the interval is too wide, or the evaluation is compromised.

Stop immediately for failed verifier consistency, no-op mismatch beyond tolerance, test contamination, or nonfinite activations. These are engineering failures, not negative scientific evidence. Stop adaptive development at its cap and inspect the sealed test once. A failed test is not permission to retune on it. For a meaningful null, state the intervention class, task distribution, model, compute budget, confidence interval, and upper bound on useful benefit.

## 9 Architecture and implementation milestones

The planned system has six small components: a manifest-driven task source; a prompt renderer; a generation adapter; an instrumented model adapter; an independent verifier; and an analysis pipeline. Keep data provenance and run identity shared across them. Backend adapters return tokens and timing; the instrumented adapter additionally returns named tensors and intervention events. The verifier receives candidate outputs and the hidden specification but supplies no hidden answers back to generation unless a separately declared search condition allows it.

The entry benchmark needs a restricted answer/proof format rather than arbitrary generated Python. Validate syntax, exact answers, identifiability, and proof steps against a trusted checker. For later executable rules, use a network-disabled, unprivileged sandbox with read-only fixtures, limited CPU/time/memory, no credentials or host mounts, allowlisted interfaces, and logged timeouts. Containerization is an implementation option, not a complete security argument. Treat all generated code as untrusted and validate checker failures independently.

| Milestone | Required artifact | Acceptance check |
| --- | --- | --- |
| M0 Specification | Task, split, metric, and provenance manifests | Independent hand audit of small worlds and explicit UNKNOWN cases |
| M1 Reference execution | Token and configuration records, no-op report | Stable tokenization, cache/full-prefix parity, prefix causality, zero intervention |
| M2 Behavioral assay | All prompt-control results | Prerequisite competence, bridge headroom, no ceiling/floor |
| M3 Causal pilot | Donor manifest, patches, leakage controls | Different-answer transfer evaluated by free generation |
| M4 Sealed confirmation | Frozen configuration and statistical report | World-level uncertainty and registered stopping rules |
| M5 Perturbation comparison | Search budgets and recovery ablations | Tuned baselines and equal verifier/refinement access |
| M6 Mechanism study | Exact validation of gradients/subspaces/paths | New selective counterfactual predictions and replication |
| M7 Scientific extension | Audited historical dossiers or prospective task | Independent correctness, provenance, and declared novelty scope |

Tests are necessary here because small numerical or data-flow errors can reverse scientific conclusions. Planned tests include answer and UNKNOWN gold cases; generator–verifier disagreement checks; split disjointness by structure; donor/recipient answer exclusion; prompt/token round trips; hook shape/site assertions; no-op and zero-amplitude identity; independent RNG streams; clean cache versus full-prefix equivalence; teacher-forcing prefix invariance; correct cache invalidation; finite-difference checks for selected gradients; bounded artifact storage; and a tiny end-to-end replay from saved metadata. Numerical tolerance is calibrated on the chosen stack, not imposed as unrealistic cross-backend bitwise identity.

Detailed directories, schemas, and retention policies appear in the appendices. They are a specification, not implemented software.

## 10 First morning and the later roadmap

### First morning

The recommended morning combines a short research review with practical setup once the researcher chooses to proceed. Spend 20 minutes on the claim and three hand-checked cases; 20 minutes inventorying actual hardware, driver, usable VRAM, RAM, disk, and toolchain; 30 minutes creating a new isolated local project/repository and reference environment; 20 minutes selecting and acquiring a pinned model snapshot, plus transfer time; 40 minutes on tiny seeded inference, selected residual capture, and no-op checks; 20 minutes on patching interpretation and Function Vectors; and 15 minutes recording results and the next task. Allow roughly three active hours, with downloads and compatibility troubleshooting additional. Working inference and capture are a useful first-day result; the full assay need not be finished first.

**FUTURE USER-APPROVED SETUP ONLY.** After the proceed decision, inventory compatibility before installing; create the project outside unrelated repositories; choose an immutable checkpoint/tokenizer revision and record its license, configuration, and template before downloading. Use a compatible PyTorch/Transformers reference stack, explicit FP16, batch one, a short prompt, and a small token cap. Repeat clean seeded inference, then add non-mutating selected residual capture and an identity/zero-strength hook. Record tokens, finite tensor shapes, memory, timing, and calibrated numerical/no-op agreement. An unfinished thinking trace at a tiny token cap is not a reasoning failure. Resolve cache/full-prefix parity and prefix invariance before causal experiments. Shorten sequences or use 0.6B if needed; leave gradients and sweeps for later. Commands and package versions remain provisional until the actual driver and immutable revisions are known. A separate optimized-backend environment and benchmark follow the working reference path. No setup has been executed here, and rental remains a separate decision.

The fully offline alternative remains available: 20 minutes on the claim, 40 on the two core readings, 45 authoring six offset worlds and six controls, 30 specifying badge-state navigation and structural holdouts, 25 choosing the outcome and budget, and 20 auditing identifiability and donor/split rules. End with a one-page specification and a hand-checked item sheet. This is an alternative session, not a prerequisite that delays approved setup. The first-day companion provides the detailed gates and examples.

Decisions before implementation are: preferred first assay; acceptable local time budget; whether 5 or 10 percentage points is the useful early target; whether thinking mode is the primary condition; whether a causal-methods result would be worthwhile even if historical discovery proves infeasible; and which eventual scientific problem merits sustained attention. Provider and rental budget can wait until a measured need exists. These decisions can be recorded without designing a product or committing to an optimization toy.

### Weeks long roadmap with branches

**Week 1:** finalize the assay, independent verifier specification, model/config manifest, and behavioral calibration. Read the core patching and task-vector papers. If prerequisite competence is poor, simplify the assay or compare capacity; if it is at ceiling, increase structural difficulty. Do not search activations yet.

**Week 2:** establish exact instrumentation and selected-site captures, then same-instance localization and cross-instance transfer. Freeze donor selection, semantic positions, and the small development search. Investigate answer-only, wrong-bridge, irrelevant, generic-elicitation, and random-direction controls.

**Week 3:** run the preregistered transfer confirmation with frozen choices and world-level uncertainty. Produce a positive, negative, or inconclusive report with preserved artifacts. If leakage explains the effect, redesign the contrast and use new data. If no worthwhile effect is supported with adequate precision, write that result rather than moving to larger models by default.

**Weeks 4 and 5:** if justified, test perturb-and-recover against tuned sampling, initial-token exploration, extra samples, and clean refinement. Separate all cache policies. Alternatively, pursue a promising bridge mechanism with short activation gradients and exact validation. Avoid doing both broadly if the local budget makes interpretation or completion difficult.

**Weeks 6 and 7:** test the surviving effect on additional structural families and, if necessary and approved, a larger model. Add mean-versus-subspace tests, joint component interventions, and limited path patching. Write a reproducible methods report. Publishability depends on the evidence and positioning, not on obtaining a positive result.

**Weeks 8 onward:** screen 10–20 historical candidates for a possible 3–5 fully audited case studies, or choose a prospective scientific-rule task with an objective validation path. Those yields are planning assumptions. For historical work, audit chronology before running target attempts. For prospective work, maintain a dated candidate archive, compare to current literature, and validate usefulness on unseen problems. Expert review or collaboration may become appropriate only if the researcher elects to arrange it; no contacts are part of this plan.

The endpoint is a research artifact: benchmark, intervention protocol, causal account with limits, or a validated scientific result. Infrastructure remains subordinate to that endpoint.

## 11 Prioritized reading syllabus

The core route is about five to seven hours across several days. Read methods and limitations with a concrete question in mind; full-paper reading is unnecessary at the start. Times below are planning estimates for a reader familiar with scientific research and ML engineering.

| No | Source and sections | Expected learning | Time |
| --- | --- | --- | --- |
| 1 | [A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html): transformer overview, residual stream, attention composition | Map familiar transformer operations to the objects being patched; the simplified models do not cover every Qwen detail | 45–60 min |
| 2 | [How to use and interpret activation patching](https://arxiv.org/abs/2404.15255): sections 2–4 | Distinguish restoration, disruption, redundancy, and metric pitfalls | 35–45 min |
| 3 | [Towards Best Practices of Activation Patching](https://arxiv.org/abs/2309.16042): metrics, corruption experiments, recommendations | Choose meaningful diagnostics and identify conclusions sensitive to setup | 35–45 min |
| 4 | [Function Vectors](https://arxiv.org/abs/2310.15213): extraction, causal tests, transfer, composition | Understand the closest antecedent to the bridge-transfer claim | 60–90 min |
| 5 | [ActAdd](https://arxiv.org/abs/2308.10248) and [CAA](https://arxiv.org/abs/2312.06681): methods, one experiment each | Specify simple contrastive-vector baselines before elaborate spectral methods | 35–50 min |
| 6 | [Noise Steering](https://aclanthology.org/2026.bea-1.41/): methods, evaluation, limitations | Recognize direct overlap and improve the sampling comparison | 30–40 min |
| 7 | [Soft Reasoning](https://proceedings.mlr.press/v267/zhu25ae.html): method, ablations, evaluation appendix; [FIRE](https://arxiv.org/abs/2410.21236): method skim | Separate noise, search, verification, and token-space branching | 45–60 min |
| 8 | [Qwen3 card](https://huggingface.co/Qwen/Qwen3-1.7B) and [Transformers cache explanation](https://huggingface.co/docs/transformers/en/cache_explanation) | Fix decoding, templates, and cache semantics before implementation | 25–35 min |

Read these when the corresponding stage becomes necessary:

- [In-Context Learning Creates Task Vectors](https://arxiv.org/abs/2310.15916), method and intervention experiments, 25–35 minutes: a second view of task compression and a useful generic task-vector control.
- [AtP*](https://arxiv.org/abs/2403.00745), approximation failures and exact-validation experiments, 45–60 minutes, then [IOI](https://arxiv.org/abs/2211.00593), path patching and faithfulness/completeness/minimality, 60–90 minutes: move from localization to a tested circuit hypothesis.
- [PPLM](https://arxiv.org/abs/1912.02164), hidden-state optimization method, 20 minutes: establish older inference-time gradient-steering precedent before claiming a new gradient approach.
- [ResearchBench](https://aclanthology.org/2026.findings-acl.644/) task construction, [DiscoveryBench](https://arxiv.org/abs/2407.01725) task/verifier design, and [Reconstruction](https://arxiv.org/abs/2608.16645) limitations, 60–90 minutes combined: decide which naturalistic task each benchmark actually measures. Read [CUSP](https://arxiv.org/html/2605.22681v1) Track II and its contamination algorithm for 15 minutes before adopting any temporal scoring rule.
- [CreativityNeuro](https://arxiv.org/abs/2607.01433), methods, human evaluation, Appendix F, 35–45 minutes: examine the difference between originality effects and an established utility improvement.
- [LatentTTS](https://aclanthology.org/2026.acl-long.2069/) and [GTS](https://arxiv.org/abs/2602.14077), methods and training details, 45–60 minutes combined: understand why trained latent-model results do not transfer automatically to this frozen text model.
- [FunSearch](https://www.nature.com/articles/s41586-023-06924-6), evaluator and search loop, and [MAP-Elites](https://arxiv.org/abs/1504.04909), archive/descriptor definitions, 45–60 minutes combined: design a useful-rule assay after choosing a real problem.

Optional later reading notes should answer five questions per paper: exact intervention; supervision and compute; strongest baseline; what the result actually establishes; and one control to borrow. Do not turn reading into a prerequisite for starting the small behavioral specification.

## 12 Independent review and the revised plan

AI-assisted methodological reviews examined prior art, datasets, local feasibility, and causal/statistical interpretation. These are methodological reviews, not external peer review.

The prior-art review rejected a broad novelty claim for perturb-and-recover and added initial-token exploration as a strong baseline. It also found that Soft Reasoning's verifier can generate/refine answers, so that paper's system gain cannot be attributed to perturbation alone. The revised plan separates transfer, search, and mechanism, and charges all selection and refinement costs.

The dataset review rejected advertised cutoffs as sufficient evidence and highlighted hindsight pairing. A subsequent [CUSP rubric audit](../docs/ground_truth/benchmark_audit.md) corrected the earlier broad critique: the detailed auditor exempts matching methods and numerical predictions, while its named-entity judgment cannot establish training provenance. The review also noted Reconstruction's acknowledged parametric contamination and its unmatched candidate-selection comparison. The revised plan starts with new controlled worlds and uses historical benchmarks only as candidate sources until each item passes an audit.

The hardware review corrected two likely mistakes: both proposed Qwen sizes have the same KV-cache dimensions, and current vLLM documentation includes Turing. It also emphasized explicit FP16 and the need to mark activations as requiring gradients when parameters are frozen. The revised plan uses separate instrumentation and generation paths with measured calibration and no claim that gradients fit locally.

The causal review rejected same-instance restoration as the central endpoint, required extraction before answer-bearing text, and emphasized the weak power of small pilots. The revised plan makes different-answer free-generation transfer primary, preserves no-op and prefix-causality invariants, includes bridge-inapplicable tasks, and distinguishes “no useful effect under this protocol” from an underpowered result.

A further independent review of the assembled draft found three issues that were corrected: single-answer assays cannot measure a range of useful ideas; a harmful sham can inflate an apparent gain; and only half of the proposed confirmation set tests held-out structures. The final protocol therefore separates composition from multi-solution novelty, makes the unmodified baseline the primary comparison, and limits the initial confirmatory claim to the declared mixture unless the structural-transfer stratum is enlarged.

Concrete open questions remain. Does a 1.7B model have a useful gap between prerequisite competence and composition? Does a bridge-derived effect survive stronger generic task-vector and elicitation controls? Can semantic positions be aligned without introducing a new confound? Is the effect stable across answer spaces and structural families? Can the verifier recognize valid alternative ideas? Is any historical candidate both chronologically eligible and deducible from the information available then? What local runtime makes a powered study worthwhile? None of these is settled by the literature or hardware specification.

## Appendix A Planned directories and artifact schemas

Create a new project outside unrelated repositories only when implementation begins. A proposed layout is:

```text
frozen-bridge-study/
  protocol/             claims, preregistration, review, decisions
  manifests/            models, datasets, splits, donors, licenses
  configs/              reference, generation, interventions, budgets
  tasks/                world specifications and future generators
  verifiers/            independent checkers and gold cases
  adapters/             reference hooks and generation interfaces
  runs/<run_id>/        metadata, tokens, events, scores, tensor index
  tensors/<shard>/      selected tensors with checksums
  analysis/             planned aggregation and statistical notebooks
  reports/              frozen results, figures, exclusions
  tests/                invariants, verifier checks, replay fixtures
```

The following are field specifications, not implemented schemas.

**Model manifest:** model ID; immutable source revision; per-file hashes; exact checkpoint public release evidence; tokenizer revision and hashes; chat-template text/hash and arguments; model configuration; precision conversion; quantization recipe if any; license; software versions; CUDA/driver; GPU identity and available memory; attention implementation; deterministic settings; backend build commit.

**Task manifest:** item/world/family/template IDs; split; generator version and seed; premises; prerequisite probes; bridge and all control texts; hidden answer or accepted-equivalence predicate; proof/identifiability specification; verifier version; semantic anchors; donor eligibility; structural lineage; source URLs and versions; license and upstream terms; historical target contribution; earliest-disclosure evidence and uncertainty; hindsight assistance; audit status and exclusion reason. Hidden answers and full explanations are not fields passed wholesale to generation.

**Run record:** run ID; parent experiment ID; config and manifest hashes; method/condition; world and donor IDs; all RNG seeds; exact rendered prompt and token IDs; token spans, positions and masks; sampling settings; thinking mode; sequence limits; timestamp and hardware; backend/precision; cache policy; all prefill/generated/verifier tokens; forward/backward counts; GPU/CPU time; peak allocated/reserved memory; output tokens/text; stop reason; truncation; verifier outcomes; errors; source-artifact hashes.

**Intervention record:** hook module path and precise pre/post operation; layer; semantic position mapping; token window; donor contrast; vector/tensor hash; dtype; shape; amplitude units and normalization; noise distribution/covariance; schedule; RNG state reference; hook order; cache reset/retention events; restoration hash for any future parameter intervention. A human should be able to distinguish “residual before MLP” from “block output” without opening implementation code.

**Tensor index:** run, world, site, layer, semantic span, shape, dtype, storage path, checksum, compression, capture selection probability, and whether the tensor is detached or part of an autograd run. Retain only selected donor and diagnostic recipient states. Use safe array/tensor formats rather than executable object serialization for shared artifacts.

**Evaluation record:** raw and canonical output; valid/invalid/UNKNOWN; equivalence class or strategy ID; proof-check results; hidden-test generalization; donor copying; selection rank and selector information; novelty reference archive version; cost; failure category; blinded human ratings if later applicable. Preserve raw candidates so the chosen result cannot hide the failed search.

## Appendix B Storage and replay policy

Use JSONL or Parquet for records and an explicit tensor index. Keep all small prompt/config/seed/score metadata and all raw generated text/token IDs, subject to source licenses. A planning cap of 2 GB for text/logs and 20 GB for selected tensors is ample for a bounded pilot but must be checked against actual disk space. Do not assume compression ratios. Estimate token-ID storage at four bytes per token plus metadata and text overhead, then measure a sample.

At 4,096 positions, saving one FP16 residual site in every 1.7B layer costs roughly 448 MiB per example; 1,000 such traces approach 438 GiB. A policy that “saves everything for later” is therefore unsuitable. Capture selected semantic positions, aggregate statistics online where appropriate, and retain a stratified diagnostic subset chosen without knowledge of success. Keep complete traces only for a small declared audit set. No full-vocabulary logits or all attention matrices by default.

Set file-count and byte limits, write failures explicitly, and never silently truncate tensors while labeling them complete. Prefer CPU transfer and sequential donor/recipient execution; account for transfer time in practical performance. Content-address selected vectors and immutable manifests so results can be replayed even when large regenerable tensors are discarded. Preserve an artifact inventory, retention reasons, and any licensing-related omissions.

## Appendix C Proposed initial configuration choices

Reference starting choices are batch one; explicit FP16; eval; frozen weights; eager uncompiled attention; no quantization; initial full-prefix cache disabled; total sequence ladder 256, 512, 1,024; selected residual capture only. For free generation, introduce cache only after clean cached versus uncached equivalence checks and document its treatment. Begin with one semantic cue and a few layer bands. Gradient mechanics use a short local suffix, autograd enabled, and a selected activation requiring gradients.

For llama.cpp, a future bounded starting configuration is a pinned CUDA build targeting architecture 75, one slot, context at most 4,096, FP16 KV, context shifting disabled, and prompt reuse disabled during parity checks. F16 from the canonical snapshot is the first numerical comparison; Q8 is a separate speed/memory condition. Batch and microbatch choices must be measured. Do not copy flags from an unpinned tutorial.

For vLLM, a conditional initial smoke configuration is FP16, tensor parallel one, max sequences one, context at most 4,096, conservative memory utilization, eager execution, and a recorded compatible attention backend. Tune graphs and concurrency only after correctness and capacity are demonstrated. Keep the backend's dependency environment separate. SGLang remains deferred.

Configuration changes, quantization, thinking-mode changes, context truncation, cache reuse, and backend switches all create a new named condition. A reproducibility record must not silently mix them. Exact tested revision hashes remain intentionally unresolved until authorized acquisition and setup; this report does not invent them.

## Appendix D Source verification notes and unresolved evidence

Primary-source verification was completed for the cited paper records, relevant full-text methods where accessible, official model cards/configurations, and current framework/backend documentation. The Transformer Circuits source was checked in its original HTML; the authors' FunSearch account supplies limited background where the Nature full text could not be accessed. Paper links remain the preferred reading destinations. This is a focused literature review, not a proof that no other work makes the same controlled-transfer contribution.

Specific statistical cautions from the prior-art review: CreativityNeuro's primary record describes an ICML 2026 Creativity and Generative AI workshop paper. Its human evaluation reports originality and surprise gains with reduced utility; Appendix F's reported 15.2% hypervolume increase has p = 0.18, which does not establish an improved Pareto frontier. The reviewer also found a mean MMLU reduction of 3.13 percentage points under the default masks. These are source-reported quantities, not independently reproduced results. The study's multiple comparisons and stimulus/rater structure matter for interpretation. [Primary full text](https://arxiv.org/html/2607.01433v1).

Soft Reasoning is in [ICML 2025 proceedings](https://proceedings.mlr.press/v267/zhu25ae.html); its search includes same-model verification and answer refinement. LatentTTS is in [ACL 2026 main proceedings](https://aclanthology.org/2026.acl-long.2069/) and includes trained latent-model/reward machinery. GTS's checked arXiv record did not establish a venue. Noise Steering's [BEA proceedings](https://aclanthology.org/2026.bea-1.41/) support the venue attribution. Venue labels alone do not change the limits of the evaluated tasks.

The [ResearchBench dataset card](https://huggingface.co/datasets/ankilok/ResearchBench) and [data-license file](https://raw.githubusercontent.com/ankitala/ResearchBench/main/DATA_LICENSE.md) distinguish restricted dataset access from MIT code. [DiscoveryBench's license](https://raw.githubusercontent.com/allenai/discoverybench/main/LICENSE) is ODC-By for its database; source content still requires review. [CUSP's official data card](https://huggingface.co/datasets/SeanWu25/CUSP) labels the data MIT and its code also carries MIT, with upstream provenance still relevant. Reconstruction's paper license does not settle benchmark/code reuse. No restricted corpus was acquired in this work.

CUSP's detailed data-contamination auditor in [v1 Appendix G.1](https://arxiv.org/html/2605.22681v1#A7.SS1) and [v2 Appendix H.1](https://arxiv.org/html/2605.22681v2#A8.SS1) explicitly exempts correct methods and numerical predictions that match the later paper. Failure requires a name quoted verbatim from the response, verified post-cutoff public release, and a judgment that the name could not have been independently invented; uncertainty should yield `unclear`. The earlier critique inferred too much from broad Track II wording: matching a later method or result alone does not fail this detailed rubric. The narrower limitation remains that the judge's independent-invention assessment does not establish training provenance, and a pass does not exclude unnamed memorization. The [audit](../docs/ground_truth/benchmark_audit.md) inspected the published prompts; implementation parity and false-positive rates were not measured. Reconstruction's [v3 limitations](https://arxiv.org/html/2608.16645v3) acknowledge parametric contamination and absent human agreement for its Match rubric; inferred cutoffs and unequal candidate pools do not support a clean causal comparison of discovery or collaboration.

Useful controlled-data precedents, to inspect when specifying the generator, are [RuleTaker](https://arxiv.org/abs/2002.05867), [CLUTRR](https://arxiv.org/abs/1908.06177), and [PrOntoQA](https://arxiv.org/abs/2210.01240). Their existence is another reason to distinguish a new instance from a new reasoning method. Reuse requires checking each actual release's terms.

Remaining blockers apply to implementation, not this plan: no measured local memory/runtime; no selected immutable checkpoint revision or tested dependency lock; no empirically calibrated task family; no powered sample-size determination; no securely audited historical item; no chosen rental provider/budget; and no justified claim of a literature gap or scientific discovery.
