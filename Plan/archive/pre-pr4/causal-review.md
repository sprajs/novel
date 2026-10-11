# Independent causal and statistical review

Prepared 11 October 2026. Research and planning only. This is an AI-assisted methodological review, not external peer review. No experiments, software installation, model acquisition, repository changes, or external contact were performed.

## Verdict

The strongest feasible entry question is whether a bridge-conditioned intervention transfers to fresh unguided deductions with different answers. A positive result establishes a useful transferable intervention within the tested distribution. It does not by itself establish scientific discovery or identify a native missing concept. The main plan has incorporated the central safeguards from this review: independent prerequisites, pre-answer extraction, different-answer transfer, semantic alignment, bidirectional patches, cache distinctions, free-generation evaluation, and world-level uncertainty.

## Highest-priority findings from review of the draft research plan

The review examined the draft research plan and its appendices. Strengthening information-identifiability, adding a second badge-state assay, predetermining disjoint donor-answer pools, and clarifying that the illustrative power calculation tests against zero rather than against a five-point worthwhile-effect threshold are appropriate safeguards. Three additional revisions are important:

1. **Separate single-answer accuracy from useful-idea diversity.** The nuisance-offset assay is a useful composition experiment, but one exact answer per problem does not establish the yield of distinct useful ideas or strategies. A final-answer checker cannot certify that differently worded explanations represent genuinely different valid methods. In the entry assay, report verified accuracy and compute-adjusted success. Before making the perturbation experiment a novelty test, specify either multiple acceptable independently verified answers or a checked proof language with a defensible strategy-equivalence scheme. A null on the single-answer assay is a bounded reasoning result, not a null about creativity. This need not commit the later project to bin packing or any particular optimization toy.

2. **Prevent a harmful-sham success.** The draft names bridge-minus-irrelevant-delta as the primary contrast, while its strong-go rule refers to the primary confidence interval. An irrelevant direction could damage the model and make an ineffective bridge vector appear beneficial. Require verified improvement over the unmodified unguided baseline as well as specificity against the sham. One clean design is to make improvement over baseline primary, then use sham/random/answer-direction controls to qualify the explanation. Another is a preregistered conjunctive success rule. Define an acceptable harm margin for UNKNOWN/bridge-inapplicable cases; a pooled accuracy gain can otherwise hide increased confidently invalid answers. Guardrails need uncertainty and cannot be certified by observing zero failures in a tiny sample.

3. **Apply sample-size arithmetic to the actual primary population.** The draft's 160 confirmation worlds include only 80 from held-out structural families, approximately 40 per held-out family. The illustrative 157-world calculation for a ten-point effect therefore does not describe the held-out-family subset. Declare either the fixed weighted mixture as primary, with held-out-family results a limited replication analysis, or enlarge the primary held-out stratum according to pilot variance and budget. Neither the total number of completions nor pooling heterogeneous strata silently resolves this issue.

The draft already appropriately says that small pilots are not definitive, that few families do not justify broad family-cluster inference, and that nonsignificance is not evidence of no effect. The corrections above make those cautions operative in the success rules.

## Recommended minimal causal protocol

### Claims and gates

Keep three claims separate:

- **Search:** internal perturbation increases verified candidate yield at fixed operational cost.
- **Transfer:** a development-derived intervention improves unguided recipients with different answers.
- **Mechanism:** nominated components implement a specified operation during ordinary successful reasoning.

Transfer is a useful result even without a complete mechanism. Generic vector transfer is already established prior art, so the prospective contribution is the controlled bridge contrast, its failure modes, its answer-independent transfer, and its comparison with strong elicitation/search baselines. Function Vectors already demonstrates transfer from in-context demonstrations and some vector composition. [Function Vectors](https://arxiv.org/abs/2310.15213)

Begin with a behavioral calibration of tens of independent worlds, not an extensive activation sweep. Run prerequisite probes in fresh contexts. Do not test A and B immediately before the target in a shared conversation, since that itself supplies assistance. Require strong prerequisite performance and meaningful minimal-bridge headroom on a prospectively specified development distribution. Numerical thresholds are design heuristics to avoid floor/ceiling effects, not universal tests of a latent bridge.

Retain all calibration results. Selecting a difficulty recipe for a guidance gap is legitimate development but restricts generalization. A model that needs a full worked explanation when a minimal bridge is ineffective has not passed a minimal-bridge gate.

### Prompt interventions

Preserve separate unguided, premises-only, minimal-bridge, full-explanation, answer-only, wrong-bridge, irrelevant-text, and instrumentation-no-op conditions. Specify precisely whether premises-only supplies new information or merely highlights relevant information already available in the world. The unguided task must contain enough information to determine the target answer, including a specified UNKNOWN outcome when it does not.

For teacher forcing, identical earlier-prefix states must remain unchanged when later forced text is varied, up to calibrated numerical tolerance. Capture donors only after the bridge has been consumed and before answer-bearing continuation. This cannot prevent a post-bridge state from already representing a computable answer; different-answer donors and transfer controls remain essential.

Use a shared neutral continuation cue as an initial alignment anchor. Record the cue's semantic role, token IDs, absolute position, position IDs, and mask. Equal integer indices alone are not semantic alignment. Compare natural alignment to matched-length controls rather than assuming padding is harmless.

### Donor and recipient design

The principal additive candidate is the mean of paired bridge-minus-control states from development donors. Preserve that mean separately from centered PCA. Freeze donor policy, contrast, layer, position, amplitude, and duration before opening confirmation targets.

Different-answer eligibility should be established by a prospectively constructed split or answer-pool policy, not a donor chosen adaptively using a hidden test answer. Balance donor labels and record which symbols, signs, magnitudes, and vocabulary overlap. Disjoint exact answers are stronger against simple copying, but they can introduce numeric-range or tokenization shifts; use comparable difficulty and report the shift. UNKNOWN and other shared output classes require explicit exception/stratum treatment rather than an impossible universal disjointness assertion.

Compare the candidate against equal-norm random directions, unrelated/shuffled donor contrasts, matched irrelevant contrasts, and answer-only directions. A generic reasoning/confidence/compliance contrast is a useful additional challenge. If the vector improves ordinary lookup and formatting as much as composition, the intervention may be useful while the bridge-specific explanation is weakened.

Same-instance guided-to-unguided restoration is localization, not the principal transfer result. Whole-state replacement can overwrite recipient-specific information. Additive deltas preserve more of it but may create unnatural states. Treat these as distinct estimands.

### What patching establishes

Test restoration and disruption at the same sites. Restoration supports conditional sufficiency; disruption supplies conditional necessity evidence. A lack of symmetry can arise from serial dependencies, redundant paths, or backup behavior. Before asserting absence, consider a bounded set of joint interventions and rescue tests. Patching evidence is specific to its prompt distributions and changed features. [How to use and interpret activation patching, sections 2–3](https://arxiv.org/html/2404.15255v1)

Real donor states are not automatically on-distribution when combined with another recipient's computation. Use a short amplitude/interpolation sweep, activation-norm checks, downstream disruption measures, and unrelated competence controls. These are diagnostics, not proof of a neural manifold. A large delta is not evidence of a missing concept; patch sufficiency can bypass the model's native route.

Localize with inexpensive continuous scores, then validate with independent free generation and the objective verifier. Exact patches precede activation gradients. Attribution methods can rank candidates, but their approximations can miss effects; validate selected high-ranked and a sample of low-ranked sites exactly. [AtP*](https://arxiv.org/abs/2403.00745)

Changing patching metrics and corruption methods can change conclusions. Preserve both continuous diagnostic scores and verified generation accuracy. [Towards Best Practices of Activation Patching](https://arxiv.org/abs/2309.16042)

## Perturbation and recovery requirements

Start with a short embedding/residual intervention and a bounded development grid. Scale Gaussian noise relative to a declared activation statistic with dimension accounted for. Keep token-sampling, perturbation, donor-selection, and world-generation RNGs separate. Zero-amplitude intervention must leave the sampler trajectory unchanged in the same validated execution path.

Recovery policies are separate treatments:

- **Retained cache:** noise stops, but earlier perturbed computations can survive in KV entries and emitted tokens.
- **Clean re-prefill:** recompute the realized text prefix without noise, removing perturbed cache states while retaining noise-selected tokens.
- **Separate clean refinement:** a fresh clean generation revises the candidate, adding a second search procedure.

Each needs a corresponding clean/no-noise control and full cost accounting. Re-prefill is not equivalent to undoing the intervention. Parameter perturbation can wait until these simpler experiments work.

Tune temperature/top-p and prompt-diversity baselines on the same development allowance as noise. Include extra ordinary samples and clean refinement using the additional compute available to the experimental method. Give equal verifier/selection information to compared methods. Report generated/prefilled tokens, candidate counts, model passes, verifier calls, measured GPU time, and development cost separately. Equal output counts are insufficient; equal wall time alone also conflates algorithmic and implementation effects.

Noise Steering provides direct prior art for training-free internal noise with decay in educational generation. Soft Reasoning combines embedding perturbation with verifier-guided search, requiring an ablation of search/selection from noise. Neither establishes the proposed scientific-discovery claim. [Noise Steering](https://arxiv.org/abs/2604.03380), [Soft Reasoning](https://arxiv.org/abs/2505.24688)

## Statistics and decision rules

The independent unit is the underlying world/problem. Average repeated-seed outcomes within a world and analyze paired world differences. Keep related paraphrases and counterfactual variants in the same split and resampling cluster. With only a few structural families, report family-specific effects and limit cross-domain claims.

For one paired binary outcome per independent world, the rough planning approximation

`n ≈ (1.96 + 0.84)^2 × disagreement_probability / target_effect^2`

gives about 627 worlds for detecting a five-point difference from zero when the discordance probability is 0.2, or about 157 for ten points. Discordance 0.4 doubles those counts. This is not the sample size for proving the improvement exceeds a five-point worthwhile threshold. Repeated seeds, differing task difficulty, multiplicity, stratification, and clustering require pilot-based recalculation.

Specify one primary comparison, population weighting, practical effect threshold, harm guardrails, analysis time, and fixed budget before confirmation. Distinguish:

- **Strong go:** the prespecified useful-effect criterion and control/guardrail conditions are satisfied.
- **Promising:** the estimate is positive but precision still includes negligible and worthwhile effects.
- **No-go for the tested intervention:** an adequately precise interval rules out the worthwhile gain, or controls explain the result as answer transfer or generic response bias.
- **Inconclusive:** insufficient precision, invalid guidance gate, ceiling/floor, instrumentation failure, or compromised evaluation.

Failed no-op, causality, verifier, or numerical checks are engineering failures. Stop interpretation and repair them before scientific testing. A failed confirmation can motivate another study but does not permit retuning on the same sealed outcomes. Report a null as a bound on a specified method, model, distribution, and budget, never as proof that frozen models cannot create useful ideas.

## Scope and remaining uncertainty

Textual reasoning is a behavioral artifact, not direct evidence of internal computation. It can guide error taxonomy without certifying the mechanism. Controlled studies have found explanations that omit causal influences on model answers. [Language Models Don't Always Say What They Think](https://arxiv.org/abs/2305.04388)

The unresolved questions are whether the small model has a useful competence/composition gap; whether guidance supports an answer-independent transferable contrast; whether the effect beats generic task elicitation; whether it extends to independently chosen structures; and whether local throughput permits meaningful precision. The draft appropriately treats these as empirical questions rather than promises.
