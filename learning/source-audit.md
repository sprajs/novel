# Teaching-source audit

Audit date: 12 October 2026. Repository baseline: `3c962e0e26e53f2b33dc6eae4c6f9835223ef89f`. This record accompanies `learning/content.json`. It is a bounded teaching-source audit, not a paper replication, scientific qualification, exhaustive literature survey, or historical corpus admission.

## Coverage

- 13 teaching chapters, 30 source records and 41 glossary entries. All four planned interactive types occur once: timeline, likelihood, sampling and intervention.
- All 18 distinct external primary readings in `Plan/reading-list.md` are covered. The two activation-patching references also occur in the paper manifest.
- All ten selected papers and both context-only papers in `papers/manifest.json` are covered at their pinned versions. The manifest’s NNsight 0.6 release account is also included.
- One additional foundational primary reading, *Attention Is All You Need* v7, supports the architecture explanation. It is explicitly distinguished from the decoder-only Qwen3 implementation.
- The reading-list link to the local model artifact audit is a repository evidence pointer, not another external paper. The teaching path explains why exact weights, tokenizer and template identity matter; it does not re-certify historical public visibility.

## Access and reading depth

Primary browsing was performed on 12 October 2026. The browser successfully opened older arXiv pages, ACL records, the Qwen release page, the OATML author account and the NNsight release article. Several recent exact-version arXiv browser calls returned `DisabledError` or internal errors. Direct public HTTPS requests with Python urllib successfully retrieved their exact metadata and, where available, HTML. This fallback did not use credentials, restricted datasets or proxy circumvention.

The expected `.cache/papers` directory was absent in this checkout. The manifest records a prior ten-PDF retrieval and targeted reading on 11 October; those records are retained as earlier repository evidence, not described as PDFs inspected afresh in this teaching pass. The first pass did not inspect a PDF afresh. In the second pass, the Surface Form Competition PDF was read through the primary ACL web viewer; no PDF was saved to the repository or redistributed. Noise Steering v2 HTML returned HTTP 404; its fresh inspection is limited to exact-version metadata and abstract. Its prior manifest PDF method notes do not change that fresh access label.

“Targeted full-text” below means selected HTML or primary PDF method, interpretation or limitation passages were actually inspected. It does not mean every section, table, appendix, proof, experiment or underlying code was checked. “Read next” instructions in source cards are recommendations, not claims of completed reading. No reported performance figure has been independently reproduced.

| ID | Exact primary source / revision | Recorded access scope |
| --- | --- | --- |
| semantic-uncertainty | [Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation](https://arxiv.org/abs/2302.09664v3) | Primary targeted method passages directly inspected on 12 October 2026 during the second teaching pass. Sections 3.1–3.3 and Section 4: semantic classes, length effects, sampling, bidirectional entailment and probability aggregation. No independent reproduction or exhaustive full-paper review. |
| semantic-entropy-account | [Detecting hallucinations in large language models using semantic entropy](https://oatml.cs.ox.ac.uk/blog/2024/06/19/detecting_hallucinations_2024.html) | Dated 19 June 2024 author article read on 12 October 2026; Nature full text not checked in this pass. “How it works” and stated limitations; then compare the changes from the earlier paper. |
| surface-form | [Surface Form Competition: Why the Highest Probability Answer Isn’t Always Right](https://aclanthology.org/2021.emnlp-main.564/) | Primary targeted method passages directly inspected on 12 October 2026 during the second teaching pass. PDF Sections 3.1–3.2 (proceedings pages 7040–7042): sequence scoring and domain-conditional likelihood ratio; setup context in Section 4.1. No independent reproduction or exhaustive full-paper review. |
| probability-mass | [Increasing Probability Mass on Answer Choices Does Not Always Improve Accuracy](https://arxiv.org/abs/2305.14596v2) | Primary targeted method passages directly inspected on 12 October 2026 during the second teaching pass. Sections 3.1–3.2 and 5.1–6.3: semantic-class sum, PMI workaround, prompt/choice conditioning and evaluation setup. No independent reproduction or exhaustive full-paper review. |
| ideation-study | [Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers](https://arxiv.org/abs/2409.04109v1) | Exact-version primary abstract and metadata checked on 12 October 2026. Full methods not independently reread for this teaching page. Abstract checked; inspect recruitment, blinding and rating instruments next. |
| execution-study | [The Ideation-Execution Gap: Execution Outcomes of LLM-Generated versus Human Research Ideas](https://arxiv.org/abs/2506.20803v1) | Exact-version primary abstract and metadata checked on 12 October 2026. Full methods not independently reread for this teaching page. Abstract checked; inspect assignment, execution constraints and review design next. |
| code-evaluation | [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374v2) | Primary targeted method passages directly inspected on 12 October 2026 during the second teaching pass. Section 2.1 and Appendix A: subset estimator, bias of the plug-in formula and binomial unbiasedness derivation. No independent reproduction or exhaustive full-paper review. |
| confidence-sequences | [Time-uniform, nonparametric, nonasymptotic confidence sequences](https://arxiv.org/abs/1810.08240v9) | Primary targeted method passages directly inspected on 12 October 2026 during the second teaching pass. Section 1, uniform-coverage definition (1) and properties P1–P4. Advanced boundary constructions are not audited for adoption. No independent reproduction or exhaustive full-paper review. |
| turpin-faithfulness | [Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting](https://arxiv.org/abs/2305.04388v1) | Primary targeted method passages directly inspected on 12 October 2026 during the second teaching pass. Sections 2.1–2.2 and Section 3 setup: biasing prompt features and operational answer/explanation comparison. No independent reproduction or exhaustive full-paper review. |
| lanham-faithfulness | [Measuring Faithfulness in Chain-of-Thought Reasoning](https://arxiv.org/abs/2307.13702v1) | Primary targeted method passages directly inspected on 12 October 2026 during the second teaching pass. Sections 2.1, 2.3 and 2.4: task/sampling setup, early answering through truncation, and inserted reasoning mistakes. No independent reproduction or exhaustive full-paper review. |
| reasoning-faithfulness | [Reasoning Models Don't Always Say What They Think](https://arxiv.org/abs/2505.05410v1) | Primary targeted method passages directly inspected on 12 October 2026 during the second teaching pass. Sections 2–2.1: paired hinted/unhinted prompts, selected answer-switch cases, verbal acknowledgment and random-noise adjustment. No independent reproduction or exhaustive full-paper review. |
| researchbench | [ResearchBench: Benchmarking LLMs in Scientific Discovery via Inspiration-Based Task Decomposition](https://aclanthology.org/2026.findings-acl.644/) | ACL 2026 proceedings metadata/abstract checked on 12 October 2026; repository benchmark audit consulted; no dataset acquired. Proceedings abstract checked; full extraction protocol and data terms require separate review. |
| discoverybench | [DiscoveryBench: Towards Data-Driven Discovery with Large Language Models](https://arxiv.org/abs/2407.01725v1) | Exact-version primary abstract and metadata checked on 12 October 2026. Full methods not independently reread for this teaching page. Abstract checked; inspect task construction and facet-based evaluation next. |
| cusp | [Scientific reasoning does not reliably translate into scientific forecasting in frontier AI](https://arxiv.org/abs/2605.22681v2) | Direct primary metadata and targeted v2 HTML auditor block checked on 12 October 2026 after browser access failed; not a full benchmark re-audit. Abstract and the matching-outcome exemptions in the Evaluation System Prompts inspected. |
| reconstruction | [Reconstruction: A Blind Benchmark for Recovering Research Ideas from Pre-Publication Bibliographies](https://arxiv.org/abs/2608.16645v3) | Exact metadata plus targeted v3 HTML design and limitations passages checked on 12 October 2026. Related Work’s design comparison and Section 5 Limitations inspected. |
| qwen3-release | [Qwen3: Think Deeper, Act Faster](https://qwenlm.github.io/blog/qwen3/) | Official dated release page checked on 12 October 2026; mutable publisher account, not a file-hash or historical-visibility proof. Release account and usage context; exact artifact details come from the repository’s pinned model audit. |
| patching-interpretation | [How to use and interpret activation patching](https://arxiv.org/abs/2404.15255v1) | Primary exact-version metadata and targeted HTML full-text passages checked on 12 October 2026; no independent reproduction or exhaustive appendix review. HTML excerpts from Sections 2–4 inspected. |
| patching-best-practices | [Towards Best Practices of Activation Patching in Language Models: Metrics and Methods](https://arxiv.org/abs/2309.16042v2) | Primary exact-version metadata and targeted HTML full-text passages checked on 12 October 2026; no independent reproduction or exhaustive appendix review. Targeted HTML passages in Sections 3–4 and experimental-settings appendix inspected. |
| function-vectors | [Function Vectors in Large Language Models](https://arxiv.org/abs/2310.15213v2) | Primary exact-version metadata and targeted HTML full-text passages checked on 12 October 2026; no independent reproduction or exhaustive appendix review. Targeted HTML method and experiment passages; discussion of semantic-offset alternatives inspected. |
| caa | [Steering Llama 2 via Contrastive Activation Addition](https://arxiv.org/abs/2312.06681v4) | Primary exact-version metadata and targeted HTML full-text passages checked on 12 October 2026; no independent reproduction or exhaustive appendix review. HTML Section 3 method and Section 10 limitations passages inspected. |
| atp-star | [AtP*: An efficient and scalable method for localizing LLM behaviour to components](https://arxiv.org/abs/2403.00745v1) | Primary exact-version metadata and targeted HTML full-text passages checked on 12 October 2026; no independent reproduction or exhaustive appendix review. HTML Sections 3–4 method and evaluation excerpts inspected. |
| soft-reasoning | [Soft Reasoning: Navigating Solution Spaces in Large Language Models through Controlled Embedding Exploration](https://arxiv.org/abs/2505.24688v4) | Primary exact-version metadata and targeted HTML full-text passages checked on 12 October 2026; no independent reproduction or exhaustive appendix review. HTML Section 4 methodology and beginning of Section 5 evaluation inspected. |
| noise-steering | [Noise Steering for Controlled Text Generation: Improving Diversity and Reading-Level Fidelity in Arabic Educational Story Generation](https://arxiv.org/abs/2604.03380v2) | Exact-version abstract/metadata checked directly on 12 October 2026. HTML returned HTTP 404; no local cached PDF was available. Earlier manifest PDF reading is a separate inherited record. Abstract checked; inspect Sections 4–6 in the pinned PDF before implementation. |
| creativity-neuro | [CreativityNeuro: Steering Language Model Weights to Improve Divergent Thinking and Reduce Mode Collapse](https://arxiv.org/abs/2607.01433v1) | Primary exact-version metadata and targeted HTML full-text passages checked on 12 October 2026; no independent reproduction or exhaustive appendix review. HTML method, human-evaluation, limitations, factual-reasoning and Appendix F excerpts inspected. |
| nnsight-ndif | [NNsight and NDIF: Democratizing Access to Open-Weight Foundation Model Internals](https://arxiv.org/abs/2407.14561v4) | Primary exact-version metadata and targeted HTML full-text passages checked on 12 October 2026; no independent reproduction or exhaustive appendix review. Targeted HTML Section 3 framework passage and section structure inspected. |
| targeted-feature-learning | [Gradients for Interventions and Activations for Detection: Targeted Feature Learning in Language Models](https://arxiv.org/abs/2609.32355v1) | Primary exact-version metadata and targeted HTML full-text passages checked on 12 October 2026; no independent reproduction or exhaustive appendix review. HTML Sections 3–6 and Appendix B excerpts on setup and selection inspected. |
| gts | [GTS: Inference-Time Scaling of Latent Reasoning with a Learnable Gaussian Thought Sampler](https://arxiv.org/abs/2602.14077v2) | Exact-version primary abstract and metadata checked on 12 October 2026. Full methods not independently reread for this teaching page. Abstract only in this pass; a full methodology and compatibility audit is required before adoption. |
| latent-tts | [Parallel Test-Time Scaling for Latent Reasoning Models](https://arxiv.org/abs/2510.07745v4) | Exact-version primary abstract and metadata checked on 12 October 2026. Full methods not independently reread for this teaching page. Abstract only in this pass; a full methodology and compatibility audit is required before adoption. |
| nnsight-release | [Introducing NNsight 0.6](https://nnsight.net/blog/2026/02/26/introducing-nnsight-06/) | Official 26 February 2026 release article checked on 12 October 2026; mutable documentation, not an implementation pin. Release overview and change descriptions; no installation or API execution performed. |
| transformer | [Attention Is All You Need](https://arxiv.org/abs/1706.03762v7) | Primary targeted method passages directly inspected on 12 October 2026 during the second teaching pass. Sections 3.1–3.5: attention scaling, multi-head output projection, residual ordering, feed-forward maps, vocabulary readout and positional encoding. No independent reproduction or exhaustive full-paper review. |

## Version choices

- Versionless reading-list arXiv links are resolved explicitly: Increasing Probability Mass uses v2; DiscoveryBench uses v1; confidence sequences uses v9; Turpin uses v1, matching the measurement protocol’s linked treatment; patching best practices uses manifest v2; patching interpretation uses v1. These choices are bibliographic pins, not claims that they are the universally latest or best versions.
- The 2024 semantic-entropy entry is the dated OATML author account specified by the reading list. This pass did not inspect the Nature full paper. It must never silently acquire a “full paper reviewed” label.
- ResearchBench uses the named ACL 2026 proceedings record. The manuscript’s earlier arXiv history is documented in the repository audit; the ACL date does not establish the disclosure date of any benchmark target.
- CUSP uses v2’s title, *Scientific reasoning does not reliably translate into scientific forecasting in frontier AI*. The v1 title differs. The fresh direct HTML check located the auditor exemption for coincidentally matching methods and numerical predictions. Matching a future target alone is not evidence of contamination.
- Reconstruction uses v3. Its explicit limitations distinguish prompt leakage from parameter exposure and acknowledge missing human agreement, candidate-count/compute differences and selection effects. Its Match endpoint is not imported as Novel’s validity rubric.
- First-publication year is displayed for arXiv sources even when a selected revision appeared later. Exact version URLs identify the actual reading. Dated author/release web pages are mutable sources, not immutable implementation pins.

## Repository evidence and precedence

The following files were consulted. SHA-256 values identify the local source bytes used for this curriculum; they do not attest to truth of the scientific or historical claims. These hashes can be compared during maintenance.

| Repository path | SHA-256 at teaching audit |
| --- | --- |
| `README.md` | `aa1822145663df9fdec5121ca97d4f61e9db9d186eba27b9f409672841163fb0` |
| `Plan/research-plan.md` | `2fd9a9089b15b1229511442fad73d91791a2b59a6318593ad9e28f6dc8148080` |
| `Plan/reading-list.md` | `b7cc1eff67f3b2328264d0267cb917e612c7993c4e83a76cf281bdba628e3541` |
| `Plan/measurement-protocol.md` | `1ff2688a3ef9dfe406daf18d28967e959ff1312a1194fc0a1b74ee7a45f5bb92` |
| `Plan/corpus-protocol.md` | `9a82259591a4eb30672198b6a6239ebe5fef7368237d1c8039e8980dab81814b` |
| `Plan/causal-review.md` | `da89816d6cdb704027ece68abdcc7d4e54451e3175e86505c250af4c2e7e82bd` |
| `papers/README.md` | `9ec309f8f17763dc85f80166e23038336b2a60a4770daefc9df36d218381fd55` |
| `papers/manifest.json` | `37bd1c82f24c4e1fed2714debb5cec36fcc871d286c04d363cb8069270a747f9` |
| `docs/models/selection.md` | `7dab52e96ab79d6a744826f95b5756279ac7fe223c599b859f20169fecc6d463` |
| `docs/tooling/current-stack.md` | `4fe7b06da647cf2c6c42f6b23573576acfd33f6ea95fed435284f66ea9e62400` |
| `docs/validation/local-2080ti.md` | `1d9571ce2323ad15c359ca53e58d7d605ac8d1a9ae3d6cafd7d2238bc1bef5ab` |
| `docs/ground_truth/benchmark_audit.md` | `4f1e1072cd941e412edbd3e9d2f9e39433c84c5f37708dbbd710c09b47367a90` |

The README and research/measurement protocols are authoritative for scientific maturity: no historical idea is admitted and no scientific model-performance result is reported. The 12 October local RTX 2080 Ti report is the newer authority for local operational status. It supersedes older prospective statements that the 1.7B snapshot was not downloaded or GPU work had not yet run, without superseding the scientific qualification gates.

The teaching page records passing bounded uncached mechanics separately from failing strict FP16 cached/full-prefix parity and cross-backend likelihood tests. It does not generalize the passing CPU smoke to all CPU repeatability conditions; the repository’s CPU repeatability investigation remains separate. Short greedy token agreement is explicitly weaker than distributional equivalence. No numerical tolerance was relaxed and no model experiment was run for this teaching task.

## Methodological boundaries

- The explanations and toy examples are original educational synthesis tied to repository protocols. Invented examples and numerical calculations are labelled as such; they are not outputs from pretrained models or historical cases.
- V means a valid solution under the frozen evidence tier; M means the scoped target contribution is present; T = V AND M. Novelty and utility remain separate assessments. Valid alternatives cannot be hidden by reporting only target recovery.
- Raw teacher-forced string likelihood, the executed decoder law, span-conditional scores and free-generation semantic probability remain distinct. An administrative token cap and a sampled stopping token are different events.
- Zero-success bounds are calculated from a fixed independent binomial sampling model. The one-sided 95% values at n = 64, 299 and 2,995 are approximately 4.573%, 0.997% and 0.100%. Simultaneous bounds and label ambiguity are kept separate. These calculations do not certify the sampling assumptions or semantic judges.
- The true-p oracle formula and the combinatorial pass@k estimator are explicitly distinguished; a real selector can perform worse and incurs additional costs.
- Historical admission needs exact contribution-level chronology, input provenance, prior-equivalent review, rights and independent human judgments. Authoritative-looking model or paper dates are not substituted for complete artifact evidence.
- Later interventions require an admitted claim, a capable baseline, reliable semantic measurement, selective predictions, donor/answer/random/no-op controls, matched compute and new held-out event families. Current patching and gradient mechanics do not satisfy those gates by themselves.
- Source cards summarize claims and mechanisms in short original prose. The site contains no paper figures, full text, private research packets, held-out answers or downloaded PDFs. Public availability is not treated as redistribution permission.

## Remaining gaps

Several observational readings remain at abstract/metadata level; their cards identify the method sections that still need inspection. The second pass deepened nine source checks, including semantic grouping, likelihood normalization, pass@k, time-uniform coverage and three different faithfulness methods. Method-level claims for the observational assay mainly follow the repository’s explicit protocols, the independently checked pass@k passage, semantic-equivalence passage, benchmark caveats and elementary calculations. A future protocol change must inspect the relevant full methods instead of treating this teaching page as a substitute.

Noise Steering still needs a fresh pinned-PDF method check before adoption. Its scale schedule and cache behavior should not be implemented from an abstract. The nine other manifest papers received targeted HTML checks, not full replications. GTS and LatentTTS remain abstract-only context; no trained sampler, latent reward model or architecture compatibility is established. NNsight is discussed as tooling, with no installation or API execution performed.

The source inventory is complete for the two requested lists, not exhaustive for the wider field. The teaching path adds only the transformer foundation; it does not attempt a general computer-science curriculum. The first practical research decisions remain historical admission, independent reviewers, model competence, a frozen decoder/rubric/budget, and an affordable precision target.

## Second teaching and editorial pass — 12 October 2026

This pass reviewed all 13 chapters and all 30 source cards with a scoped Astra
teaching audit and a separate parent editorial review. The revision keeps the
same research question, model artifacts, protocols and source inventory. The
research baseline remains `3c962e0e26e53f2b33dc6eae4c6f9835223ef89f`; changes
are teaching content, reference relevance and rendering in PR #9.

The nine source records with a method-text link received direct primary method
checks during this pass. Their table entries above state the inspected sections.
Other entries retain the first pass's access scope; this is not a claim of 30
fresh full-paper reads. Noise Steering remains a pinned-PDF method gap, and the
Nature paper behind the dated OATML account was not newly inspected. No paper
was added simply to teach elementary mathematics. Confidence sequences moved
from core to context because the proposed initial design uses fixed allocations;
no source was retired or removed.

The Qwen-specific explanation was also checked against the installed, locked
Transformers 4.57.6 implementation in `models/qwen3/modeling_qwen3.py`: query/key
normalization and rotary positions, per-layer K/V updates, pre-normalized
attention and feed-forward substeps with two residual additions, final
normalization and vocabulary readout. This is source inspection, not a new
runtime experiment or cache-parity pass. A block-output patch cannot rewrite
that block's already computed cache entries retroactively.

| Chapter | Hidden prerequisite or editorial gap addressed |
| --- | --- |
| Tokens | Probabilities as shares, fractions/percentages, conditional notation, exp/log inverses, ID labels, softmax and filtered sampling. |
| Transformer | Scalar/vector/matrix/tensor axes, coordinate arithmetic, dot products, attention mixture/projection, position information, residual bypass and readout. |
| Inference | Forward/loss/backward/update, frozen parameters, causal cache reuse, backend/precision/tolerance, text versus numerical history and four recovery policies. |
| History | What reconstruction measures, artifact/provenance/hash definitions, invented chronology and explicit P0–P3 assistance. |
| Meaning | Assumptions/mechanism/consequence, unbiasedness and variance, authored V/M cases, semantic grouping and empirical entropy versus the paper estimator. |
| Likelihood | Multiply conditional branches without independence; add disjoint outcomes; logs/underflow; aligned teacher forcing; stop versus cap and surface-form rankings. |
| Sampling | Estimand, Bernoulli/binomial assumptions, seeds versus independence, event chance s, expectation, worked subset estimator and real selection. |
| Uncertainty | Repeated-batch coverage, zero-count surprise, bound derivation, precision planning, label uncertainty, multiple claims and stopping. |
| Judgment | Inspectable rubric, evidence tiers/blinding, explicit zero-division case and the distinct prompt/trace/hint intervention designs. |
| Observational study | One connected invented assay, development/confirmation, plain-language gate dependencies and four evidence levels. |
| Patching | Correlation versus manipulation, donor assistance/controls, two-route redundancy and local logit versus semantic effects. |
| Vectors | Mean differences/confounds, derivative from a scalar slope, numeric gradient/dot-product approximation and detection versus control. |
| Search | Candidate/selector/verifier roles, Gaussian noise scale, adaptive surrogate/acquisition and a complete search endpoint. |

The elementary examples and all diagrams are original. Arithmetic was checked
separately with standard-library Python: the path product, empirical entropy,
pass@5, subset pass@2, zero-count probabilities, one-sided/simultaneous bounds,
299/2,995 sample requirements and gradient displacement agree with the printed
values. These are educational calculations, not model or historical results.

The renderer supports accessible worked tables, a residual bypass schematic,
26 explained crosslinks, glossary-to-chapter links and shareable section routes.
Paper links are explicitly optional. The four interactive examples are
illustrations, including the cache-policy explorer moved into the inference
lesson. No quizzes, declarations, checkboxes, progress state or reading-order
enforcement were introduced. Browser and deployment verification are recorded
in `learning/publication.json` after the actual checks and deployment.

## Parent beginner-readability review — 12 October 2026

After the second task finished, the parent agent read all 13 chapters against
the requirement that a beginner should not need to open the papers first.
`TEACHING-REVIEW.md` records the assessment and the remaining prerequisites
addressed in that review. This adds one introductory section and three glossary
entries, with definitions at their point of use. It does not add a paper or
claim another primary-method inspection. The access labels and scientific
qualification limits above remain applicable.
