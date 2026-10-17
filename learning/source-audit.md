# Literature and teaching-source audit

## Hidden-context direction — 17 October 2026

This is the current review record. Current inventory: **5 research reviews,
17 optional concept notes, 45 source records and 53 glossary terms**. The earlier
records below retain the counts and decisions of their respective passes.

The owner selected a behaviour-first neuroscience adaptation as Novel's next
research direction, following the linked conversation “Neuroscience Of Novel
Thoughts” and the proposed programme. HC-1 asks whether feedback on one item
changes the first response to a different item under a shared hidden rule.
`Plan/hidden-context-protocol.md` specifies the synthetic information, controls,
models, splits and analysis. It is a proposed experiment, not an implemented
runner, a completed replication or a result. Historical reconstruction and its
admission rules are retained as a later scientific-transfer track.

The remote was fetched; default branch `8aa2393f13f2f787f8d1839704eb2fa1a1e7405a`
was unchanged. These research changes and the reading baseline are reviewed
in the existing PR #10. `baseline.json` identifies the research-plan commit
and the reviewed input hashes. Publication does not merge or approve the PR.

### Focused primary-source follow-up

This task-driven follow-up builds on the bounded frontier search recorded below.
It does not imply a fresh exhaustive search or favour a publication merely for
being recent. The primary texts were checked for the following design decisions:

| Source | Material actually inspected | Why selected and limits |
| --- | --- | --- |
| [Courellis et al., Nature 2024](https://www.nature.com/articles/s41586-024-07799-x), [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11338822/) | Parent targeted publisher/indexed passages; independent Astra reviewer inspected PMC task, inference trial definition, performance grouping and neural abstraction passages. Parent direct HTML/PDF retrieval redirected or failed and is not counted as a full-text read. | Human anchor for first-other-item transfer after feedback. HC-1 omits reward magnitude and clinical recording conditions. Performance-defined grouping cannot independently establish the same performance contrast. Supplements, participant data and code have not been reconciled; a close-replication claim would require that work. |
| [Johnston and Fusi, Nature Communications 2023](https://www.nature.com/articles/s41467-023-36583-0), [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9950464/) | Targeted primary full-text abstraction/results passages and data/code availability. Figshare 21761348 v1 and Zenodo 7465963 were identified, not downloaded or executed. | Computational counterpoint: learned representations can generalise across task conditions. Guides held-out decoding; does not predict an HC-1 score or prove a shared human mechanism. |
| [Liu et al., Cell 2019, author-hosted PDF](https://discovery.ucl.ac.uk/10078375/1/1-s2.0-S0092867419306403-main.pdf) | Targeted task and decoding passages on PDF pages 2–4 during the direction review. No supplement reconciliation or human-data analysis. | Later sequence-reorganisation question. A produced sequence and spontaneously decoded replay are different outcomes; merely pausing a model supplies no computation. |

No source result has been independently reproduced. The new figures are original
schematics, and the numerical examples are analytic consequences of the proposed
generator. Access scopes are visible on each paper card. The three sources are
added to both the repository reading list and the Site inventory.

### Review decisions

The new leading review starts with transfer, connects the human task to a
controlled network assay, shows paired change/stay and ambiguous-cause examples,
and links to a focused concept note on hidden variables, Bayes' rule, calibration,
state and decoding. The examples expose the simple one-bit reversal strategy
that can solve task A. They also explain why two indistinguishable worlds cannot
be classified before new evidence arrives. Neither explanation needs the reader
to open the paper first.

Historical measurement, evaluation and model-selection sources move to `later`:
semantic uncertainty, the semantic entropy account, surface-form competition,
probability mass, ideation/execution studies, code evaluation, ResearchBench,
DiscoveryBench, CUSP, Reconstruction, Qwen3 release and EurekaBench. The existing
faithfulness evidence readings move to `context`. History, meaning, likelihood
and historical observational notes are marked later. No source is deleted or
retired; older URLs remain valid for reference. Current broad reviews remain
available, with their project implications scoped to the relevant later stage.

An independent methodological review corrected the confirmation allocation to
fit the available held-out groups, separated split groups from repeated episode
instances, specified within-checkpoint probes, trained both ambiguity query
positions, and made balanced change/stay accuracy the primary endpoint. It also
identified the known change position and reward shortcut as limits. A final review replaced the shifted-position recall competence gate with
in-distribution stay accuracy and required a minimum change accuracy as well as
stay accuracy before using the label reliable transfer. Immediate recall remains
a separately labelled robustness control. The parent incorporated these
corrections and reviewed the new teaching prose. These are design/editorial checks, not numerical
qualification, human-reader testing or scientific evidence.

## Research-led review — 17 October 2026

This earlier research-led pass preceded the hidden-context direction above. The 12 October teaching audits below are also historical records. Inventory at this pass: **4 research reviews, 16 optional concept notes, 42 source records and 49 glossary terms**. Twelve sources were added and four existing sources received deeper methods/results reading. The original 30-source reading inventory remains available; foundational chapters moved out of the main navigation rather than being retired as irrelevant.

The reviewed default-branch baseline is `8aa2393f13f2f787f8d1839704eb2fa1a1e7405a`. The remote was fetched and the current research plan, source inventory and validation boundaries reviewed. PR #9 merged during this review; its merge tree exactly matches the previous curriculum head, with no further research changes since `3c962e0e26e53f2b33dc6eae4c6f9835223ef89f`. This revision follows the merged default branch in a new focused PR. It changes the reading experience and literature synthesis, not the research protocol or scientific qualification.

### Scope and selection

The review connects machine discovery, reasoning and search, mechanistic interpretability, and AI/neuroscience. Searches explicitly included 2026 and October leads. Selection is bounded by relevance to Novel; this is neither an exhaustive survey nor a live leaderboard. Older work remains when it supplies a competing interpretation or an essential method. No paper results were independently reproduced. The original diagrams and illustrative calculations are explanatory synthesis.

### Search record

Queries:

- `site.arxiv.org "Reconstruction: A Blind Benchmark" "2608.16645"`
- `site.arxiv.org "Scientific reasoning does not reliably" "2605.22681"`
- `site.arxiv.org "Can LLMs Generate Novel Research Ideas" "execution"`
- `site.arxiv.org reinforcement learning reasoning capability pass k base models 2025 2026`
- `site.arxiv.org/abs/ "scientific discovery" "October" "2026" benchmark`
- `site.arxiv.org/abs/ "reasoning" "October" "2026" "search" "pass"`

Web search used for current discovery and initial primary pages. Several arXiv HTML fetches returned DisabledError through web; direct HTTPS retrieval with urllib succeeded. HTML text parsed with the Python standard library. No downloaded papers or benchmark data retained, no model experiments run.

Screened leads not selected:

- [Autonomous Science Bench](https://arxiv.org/abs/2610.18449): Recent search lead; no primary methods reading; not needed for this bounded comparison.
- [MechHypoBench](https://arxiv.org/abs/2610.05197): Search lead only; deeper method review deferred.
- [Station open-ended discovery study](https://arxiv.org/abs/2610.08927): Search lead only; no result imported.
- [Does RL Expand the Capability Boundary of LLM Agents?](https://arxiv.org/abs/2604.14877): Abstract/search lead; tool-use setting useful later but outside this eight-source selection.

Queries:

- `site.transformer-circuits.pub 2025 circuit tracing attribution graphs limitations biology language model`
- `site.arxiv.org mechanistic interpretability 2026 circuit tracing evaluation`
- `site.nature.com language models brain alignment 2025 2026 representations`
- `Transformer Circuit Faithfulness Metrics Miller ablation`
- `Beyond representational alignment brain-guided 2026 arxiv`
- `Language Model Circuits Are Sparse in the Neuron Basis ICML 2026`

Searched primary-source domains for 2025 circuit tracing, 2026 mechanistic interpretability/circuit evaluation, and 2025–2026 language-model brain alignment.
Included 2026 searches explicitly; selected July 2026 ICML neuron-basis circuits, June 2026 cellular study and June 2026 brain-guided reasoning preprint (later journal publication verified). No claim that these are the latest papers in every subfield.
Retained 2024 faithfulness critique because it directly changes interpretation of current circuit metrics.
Attention QK extension (July 2025) surfaced but was not promoted after web access failures; no claims from it used.
Nature pages intermittently failed in web.open; direct HTTP retrieval recovered targeted full text for visual alignment, neuronal mapping and arXiv brain-guided reasoning.
2026 sources remain author-reported findings, not independent replications.
July 2026 CircuitKIT was inspected at methods/results depth but excluded from the final eight-paper selection in favor of the directly competing neuron-basis experiment; this is a focus decision, not a negative validity judgment.

### Source checks and result provenance

Exact versions are linked below. A targeted full-text check covers the stated passages, not every appendix, experiment or implementation. Journal publication status is kept separate from the actual version read.

#### The Ideation-Execution Gap: Execution Outcomes of LLM-Generated versus Human Research Ideas

- Source inspected: [execution-study](https://arxiv.org/html/2506.20803v1)
- Passages: Sections 2–4, Tables 4–5, Section 5.1 and stated attrition in Section 3.1
- Access: Targeted primary full-text method/results passages; not exhaustive paper or appendix review; no independent replication.
- Checked claim: 43 completed projects: Sections 2–3.
- Checked claim: Effectiveness gaps −1.879 AI and −0.052 human: Table 5.
- Checked claim: Project-level post-execution comparisons nonsignificant: Table 4 and Section 4.1; 19 human / 24 AI.

#### Scientific reasoning does not reliably translate into scientific forecasting in frontier AI

- Source inspected: [cusp](https://arxiv.org/html/2605.22681v2)
- Passages: Methods, Model Evaluation, Supplementary Table S8, Appendix H.1 leakage rubric and main-text limitations
- Access: Targeted primary full-text method/results passages; not exhaustive paper or appendix review; no independent replication.
- Checked claim: Near-chance merged binary accuracy across six models: Supplementary Table S8; per-model domain means 0.476–0.506.
- Checked claim: Appendix H.1 explicitly passes matching correct methods and coincidentally matching numerical predictions.

#### Reconstruction: A Blind Benchmark for Recovering Research Ideas from Pre-Publication Bibliographies

- Source inspected: [reconstruction](https://arxiv.org/html/2608.16645v3)
- Passages: Sections 3.1–3.4, 4.3, Table 2 and Section 5 Limitations
- Access: Targeted primary full-text method/results passages; not exhaustive paper or appendix review; no independent replication.
- Checked claim: 643 papers/six domains and 36.0% unweighted domain mean: Table 2.
- Checked claim: 5-of-20 versus 5-of-5 candidates and no reported human agreement: Section 5.

#### Reasoning Models Don't Always Say What They Think

- Source inspected: [reasoning-faithfulness](https://arxiv.org/html/2505.05410v1)
- Passages: Sections 2–3, Figure 1 discussion and Sections 4 and 7.2
- Access: Targeted primary full-text method/results passages; not exhaustive paper or appendix review; no independent replication.
- Checked claim: 25% Claude3.7 Sonnet and39% DeepSeekR1 acknowledgment averages:Section3/Figure1 discussion.
- Checked claim: Answer-switch conditioning and random-noise correction:2.1.

#### EurekaBench: Measuring Agentic Ability to Discover New Scientific Insights

- Source inspected: [eurekabench](https://arxiv.org/html/2610.00492v1)
- Passages: Sections 2.1–2.2, 3.1–3.2, 4–6; Table 2; Appendix C.2
- Access: Targeted primary full-text method/results passages; not exhaustive paper or appendix review; no independent replication.
- Checked claim: 26 tasks/306 insight questions: Section 3.2.
- Checked claim: GPT 6 Astra PA 47.4/SI29.4 vs human48.8/69.7: Table 2.
- Checked claim: PA/SI are unconditional normalized rubric scores; human reference is current scientific progress, not matched-budget trial: Sections 2.2 and 4.
- Checked claim: Judge can derive additional insights through experiments: Section 2.2; Section 6 distinguishes experimentation-only insights.

#### Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?

- Source inspected: [rlvr-boundary](https://arxiv.org/html/2504.13837v5)
- Passages: Sections 2.2–3.3, 5 and 7; selected validity checks in Section 3.1
- Access: Targeted primary full-text method/results passages; not exhaustive paper or appendix review; no independent replication.
- Checked claim: v5 selected after checking live version history; first publication 18 April 2025, selected revision24 November2025.
- Checked claim: Main temperature0.6/top-p0.95/cap16384: Section3; coding exception32k:3.2.

#### Curriculum Reinforcement Learning Can Incentivize Reasoning Capacity in LLMs Beyond the Base Model

- Source inspected: [curriculum-rl](https://arxiv.org/html/2606.22317v1)
- Passages: Sections 3.1–3.3, 4.1–4.2, Table 1 and discussion of scope
- Access: Targeted primary full-text method/results passages; not exhaustive paper or appendix review; no independent replication.
- Checked claim: Mean pass@256 gain9.8 percentage points over base: Figure3 discussion/Table1.
- Checked claim: Five model settings/three benchmarks:4.1.
- Checked claim: Teacher-guidance SFT precedes RL:3.2–3.3.

#### Beyond Repeated Sampling: Learning Search Policies for LLM Reasoning

- Source inspected: [learned-search](https://arxiv.org/html/2609.26704v1)
- Passages: Sections 6.1–6.2 and 7.3; Table 3; Appendices D.3 and D.6
- Access: Targeted primary full-text method/results passages; not exhaustive paper or appendix review; no independent replication.
- Checked claim: 1k held-out DeepMath hard problems, filtered using128 failures:6.1.
- Checked claim: Pass@12839.20 vs19.00:Table3, max-of-mean variant.
- Checked claim: Same32B answer/judge model, different scoring prompt:6.1.
- Checked claim: Training1024 answer generations plus1024 judge calls per problem before update:7.3.
- Checked claim: Fresh baseline19.46% estimated with1280 samples per problem:D.6; retained as audit context, not displayed as independent replication.

#### Circuit Tracing: Revealing Computational Graphs in Language Models

- Source inspected: [circuit-tracing](https://www.transformer-circuits.pub/2025/attribution-graphs/methods.html)
- Passages: Sections 2, 3, 5 and 7.
- Access: Primary HTML: targeted architecture, evaluation and limitation passages directly inspected. Inspected 17 October 2026; no independent replication or exhaustive full-paper review.

#### On the Biology of a Large Language Model

- Source inspected: [circuit-biology](https://www.transformer-circuits.pub/2025/attribution-graphs/biology.html)
- Passages: Introductory multistep case, methodology, limitations.
- Access: Primary HTML: targeted case-study and limitation passages inspected. Inspected 17 October 2026; no independent replication or exhaustive full-paper review.

#### Transformer Circuit Faithfulness Metrics Are Not Robust

- Source inspected: [circuit-faithfulness](https://arxiv.org/html/2407.08734v1)
- Passages: Sections 3 and 4.
- Access: Primary arXiv HTML: targeted ablation definitions and results inspected; COLM 2024 publication verified. Inspected 17 October 2026; no independent replication or exhaustive full-paper review.

#### Language Model Circuits Are Sparse in the Neuron Basis

- Source inspected: [neuron-basis-circuits](https://raw.githubusercontent.com/mlresearch/v306/main/assets/arora26c/arora26c.pdf)
- Passages: Sections 3–6 and limitations.
- Access: ICML 2026 proceedings verified; primary PDF retrieved in memory and text-extracted after web content-type failure. Targeted methods, results and limitations inspected 17 October 2026. No independent replication.

#### High-level visual representations in the human brain are aligned with large language models

- Source inspected: [visual-brain-alignment](https://www.nature.com/articles/s42256-025-01072-0)
- Passages: Results: mapping and contextual-information controls; Fig. 3.
- Access: Publisher full text: targeted results and control passages directly inspected via web and HTTP retrieval. Inspected 17 October 2026; no independent replication or exhaustive full-paper review.

#### Temporal structure of natural language processing in the human brain corresponds to layered hierarchy of large language models

- Source inspected: [temporal-brain-hierarchy](https://www.nature.com/articles/s41467-025-65518-0)
- Passages: Temporal-receptive-window results and interpolation significance methods.
- Access: Targeted publisher-indexed full-text results and interpolation methods inspected. Direct HTTP inspection of the 17 April 2026 correction (https://www.nature.com/articles/s41467-026-72170-9) confirms incorrectly rendered colored plots in Figure 3; the correction states results and conclusions are unaffected and the HTML/PDF figure is amended. Inspected 17 October 2026; no independent replication or exhaustive full-paper review.

#### Mapping the neuronal building blocks of human language with language models

- Source inspected: [neuronal-language](https://www.nature.com/articles/s41586-026-10691-5)
- Passages: Results and Fig. 3; language-model and predictivity methods.
- Access: Publisher full text fetched directly after intermittent browser errors; targeted counts, comparison and method passages inspected. Inspected 17 October 2026; no independent replication or exhaustive full-paper review.

#### Beyond representational alignment with brain-guided language models for robust reasoning

- Source inspected: [brain-guided-reasoning](https://arxiv.org/html/2606.11893v1)
- Passages: NARI controls, NARF transfer results and neural-predictivity methods.
- Access: Primary source for the exact numerical result is arXiv v1, dated 10 June 2026: targeted NARI controls, NARF transfer and predictivity methods inspected via direct HTTP. Later journal publication, Nature Machine Intelligence, 3 August 2026, https://www.nature.com/articles/s42256-026-01278-w, was checked bibliographically and at abstract level only. Its full methods were not reconciled. Inspected 17 October 2026; no independent replication.

### Parent consolidation and boundaries

The parent read all four essays and the three added concept notes. It independently checked the primary learned-search design/results, EurekaBench scores and endpoint definitions, the visual-alignment word-order control, and the circuit-tracing evaluation account. The source review also resolved the temporal-brain paper’s 17 April 2026 correction: it concerned colored plots in Figure 3 and states that results/conclusions are unaffected. The 13.2-point brain-guided reasoning claim is pinned to the June preprint, qualified as best-of-five, and is not silently attributed to reconciled journal methods.

The parent made technical definitions more local (NLP, statistical significance, neuron recordings, syntactic features, mean ablation and down-projection), added optional notes on alignment, sparse features and reward learning, and retained the distinction between a frozen answer model and a newly trained complete system. It added original diagrams for the alignment comparison and paired intervention. The review includes negative and conditional findings, with no claim of a universally best method.

Neuroscience readings are comparative context for future mechanisms, not proof of biological identity or prerequisites for the first Novel assay. New frontier sources are in the review because they change a measurement or experimental comparison. Earlier background stays behind concept links. No source was retired, and no historical contribution was admitted.

No paid services, participant data, model runs or experiments were acquired. Full papers are linked, not redistributed. Source access failures were addressed only by ordinary public HTTPS retrieval or explicitly narrower labels; no access controls were bypassed.

---

## Historical audit — 12 October 2026

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
