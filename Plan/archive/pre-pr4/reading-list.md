# Reading syllabus for frozen model intervention research

Prepared 11 October 2026

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

## Later reading

- [In-Context Learning Creates Task Vectors](https://arxiv.org/abs/2310.15916), method and intervention experiments, 25–35 minutes: a second view of task compression and a useful generic task-vector control.
- [AtP*](https://arxiv.org/abs/2403.00745), approximation failures and exact-validation experiments, 45–60 minutes, then [IOI](https://arxiv.org/abs/2211.00593), path patching and faithfulness/completeness/minimality, 60–90 minutes: move from localization to a tested circuit hypothesis.
- [PPLM](https://arxiv.org/abs/1912.02164), hidden-state optimization method, 20 minutes: establish older inference-time gradient-steering precedent before claiming a new gradient approach.
- [ResearchBench](https://aclanthology.org/2026.findings-acl.644/) task construction, [DiscoveryBench](https://arxiv.org/abs/2407.01725) task/verifier design, and [Reconstruction](https://arxiv.org/abs/2608.16645) limitations, 60–90 minutes combined: decide which naturalistic task each benchmark actually measures. Read [CUSP](https://arxiv.org/html/2605.22681v1) Track II and its contamination algorithm for 15 minutes before adopting any temporal scoring rule.
- [CreativityNeuro](https://arxiv.org/abs/2607.01433), methods, human evaluation, Appendix F, 35–45 minutes: examine the difference between originality effects and an established utility improvement.
- [LatentTTS](https://aclanthology.org/2026.acl-long.2069/) and [GTS](https://arxiv.org/abs/2602.14077), methods and training details, 45–60 minutes combined: understand why trained latent-model results do not transfer automatically to this frozen text model.
- [FunSearch](https://www.nature.com/articles/s41586-023-06924-6), evaluator and search loop, and [MAP-Elites](https://arxiv.org/abs/1504.04909), archive/descriptor definitions, 45–60 minutes combined: design a useful-rule assay after choosing a real problem.

Optional later reading notes should answer five questions per paper: exact intervention; supervision and compute; strongest baseline; what the result actually establishes; and one control to borrow. Do not turn reading into a prerequisite for starting the small behavioral specification.
