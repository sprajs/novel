# Reading tied to Novel’s research decisions

The active task is [hidden-context transfer](hidden-context-protocol.md). Primary
reading supplies a task, a computational comparison or a measurement decision.
The reading room explains these in connected prose; there is no required order.
Source access is recorded in [the audit](../learning/source-audit.md).

## Current behavioural track

| Decision | Primary reading | Use and limit |
| --- | --- | --- |
| What counts as transfer after feedback? | [Courellis et al. 2024](https://www.nature.com/articles/s41586-024-07799-x) | Adapt the first other-item inference contrast; omit clinical recordings/reward magnitude explicitly; no claim of human-equivalent mechanism. |
| How could abstraction arise in a neural network? | [Johnston and Fusi 2023](https://www.nature.com/articles/s41467-023-36583-0) | Computational counterpoint and held-out decoder generalisation; not proof that HC-1 needs the same representation. |
| What would sequence reorganisation add? | [Liu et al. 2019](https://discovery.ucl.ac.uk/10078375/1/1-s2.0-S0092867419306403-main.pdf) | Next-track task design; reconstructing a sequence is distinct from spontaneous replay. |

## Later historical scientific-transfer track

These sources remain useful for historical contribution admission, semantic
measurement and eventual discovery claims. They are deferred from the next
working session, not prerequisites for running HC-1. The following selection
was prepared 11 October 2026 and retains its bounded source-access notes.

| Decision | Primary reading | Use and limit |
| --- | --- | --- |
| What counts as the same idea? | [Kuhn et al., Semantic Uncertainty, v3](https://arxiv.org/abs/2302.09664v3); [Farquhar et al., authors' account](https://oatml.cs.ox.ac.uk/blog/2024/06/19/detecting_hallucinations_2024.html) | Separate wording from meaning. Sample clustering does not enumerate all unseen scientific alternatives or certify validity. |
| What does reference likelihood measure? | [Holtzman et al., Surface Form Competition](https://aclanthology.org/2021.emnlp-main.564/); [Wiegreffe et al., Increasing Probability Mass](https://arxiv.org/abs/2305.14596) | Inspect surface-form and normalization effects. A calibrated or normalized score is not an idea probability. |
| How should research ideas be judged? | [Si et al., expert idea study, v1](https://arxiv.org/abs/2409.04109v1); [Si et al., ideation/execution study, v1](https://arxiv.org/abs/2506.20803v1) | Distinguish expert ratings of novelty/feasibility from realized research outcomes. Neither admits a historical target for this study. |
| What does repeated generation estimate? | [Chen et al., code evaluation, v2](https://arxiv.org/abs/2107.03374v2) | Understand candidate-count and pass@k estimands. An oracle's ability to find a correct candidate is different from deployable self-selection. |
| Can we stop after a promising batch? | [Howard et al., confidence sequences](https://arxiv.org/abs/1810.08240) | A future adaptive study needs valid sequential inference. This initial proposal uses fixed counts and cannot reuse fixed-N bounds after outcome-dependent stopping. |
| Can expressed reasoning explain a success? | [Turpin et al.](https://arxiv.org/abs/2305.04388); [Lanham et al., v1](https://arxiv.org/abs/2307.13702v1); [Chen et al., reasoning-model study, v1](https://arxiv.org/abs/2505.05410v1) | Motivates separate behavioral annotation and later causal tests. Faithfulness is task/condition dependent, not guaranteed by plausible prose; the newer study tests whether reasoning traces reveal hint use. |
| Which existing corpus is usable? | [ResearchBench](https://aclanthology.org/2026.findings-acl.644/); [DiscoveryBench](https://arxiv.org/abs/2407.01725); [CUSP v2](https://arxiv.org/html/2605.22681v2); [Reconstruction v3](https://arxiv.org/html/2608.16645v3) | Use as candidate/protocol sources. Read the [version/license audit](../docs/ground_truth/benchmark_audit.md); no item is automatically eligible. |
| Which exact model predates the claim? | [Existing artifact audit](../docs/ground_truth/model_audit.md), linked immutable cards/trees; [Qwen3 release](https://qwenlm.github.io/blog/qwen3/) | A family release/cutoff does not replace byte and interface identity. Do not use a current card to silently replace the historical template. |
| When can internal association become a causal experiment? | [Patching best practices](https://arxiv.org/abs/2309.16042); [patching interpretation](https://arxiv.org/abs/2404.15255) | State the intervention, metric, controls and conditional interpretation before patching. See [later causal gate](causal-review.md). |

Use the historical protocols when that track is activated; HC-1 has its own
behavioural measurements and checks. No source certifies our corpus or reproduces
its authors' experiments merely by being listed here.

## Source access and boundaries

The source audit checked public primary pages and version histories on
11 October 2026. The documents link claims to their sources; the corpus
casebook records candidate-specific uncertainties. No full
paper or restricted benchmark is redistributed. No upstream license is adopted
as the repository's license.

The Nature landing page for semantic entropy failed to render in the main
research pass; the authors' public OATML account was read successfully. This is
sufficient for the limited wording/meaning distinction used here, not a claim
of rechecking every experiment. The CUSP HTML browser omitted its full auditor
block, so the existing source-version audit and a direct public HTML inspection
are used for that narrow correction. Some arXiv renderings contain version/date
ambiguities; those remain explicit in the casebook rather than becoming clean
historical evidence. Author claims about performance are not independent
replications.

The [causal study guide](causal-review.md) identifies methodological reading for
interventions. A future experiment must audit the versions relevant to its own
claims.
