# Ground-truth collection decision report

Audited 11 October 2026. This collection provides a candidate registry, worked deductive tasks and tested data interfaces for the [machine discovery programme](../../Plan/research-plan.md). It does **not** report a model's failure, successful rediscovery, activation-transfer effect or new scientific discovery. No target-model inference was performed in this collection audit.

## Collection findings

Maintain two model lanes. Keep the infrastructure's July 2025 Qwen3 revisions for mechanics. For a recent historical study, investigate the separately pinned April 29 Qwen3 snapshots against a narrowly scoped MeanFlow application; for DPO, investigate the April 2023 Pythia snapshots. Do not switch infrastructure's model pins silently. None of the twenty surveyed candidates is fully admitted: earliest-equivalent-disclosure, exact public-artifact evidence, prerequisite competence and independent review remain gates.

Prioritize **MeanFlow, DPO, DoRA, SSD and DeltaNet** for further claim-level audits. This is an allocation of audit effort, not a list of certified novel identities. MeanFlow's calculus and DoRA's normalization derivative are classical; only appropriately scoped later combinations/applications could carry a historical reconstruction claim. DPO's finite policy/preference transformation is a concise next derivation target, subject to earlier-equivalent-objective searches. SSD and DeltaNet offer different structural mechanisms but need new worked verifiers and capability probes.

Retain AlphaEvolve's rank-48 complex matrix-multiplication certificate as an ambitious mathematical alternative. Its public [May 14, 2025 announcement](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) predates the June arXiv paper, and therefore matters for checkpoint choice. Checking a supplied certificate is much easier than producing one; it is not yet a small-model A/B bridge task. The registry explicitly distinguishes bilinear tensor rank from unrestricted multiplication-count claims and does not reproduce the certificate here.

## What is concrete now

The [registry](../../data/ground_truth/candidate_registry.json) contains **20 scoped leads: 5 priority pending audit, 10 ambiguous, and 5 rejected for the selected claim/assay**. Each has primary sources, earliest-verified-date semantics, antecedents, A/B, bridge, proposed verification, empirical exclusions, model compatibility, license notes, five ranking scores and next audit actions. This is a purposive survey across sampling, preference optimization, matrix geometry, state-space/fast-weight computation, flow methods, optimization, matrix multiplication, sorting and geometric proof; it is not a representative census or twenty independent discoveries.

Five [worked packets](packets/) cover DPO, exact speculative correction, DoRA, stable attention merging and MeanFlow. They specify assumptions, source versions, alternative valid routes, wrong/irrelevant/answer-only controls and boundaries between deduction and measurement. There are **51 public fixtures**: 20 synthetic calibration worlds, 22 finite examples for the first four research packets, and 9 MeanFlow consequences. The synthetic collection includes exact offset identifiability, two-world UNKNOWN certificates, inconsistency certificates and objective badge-state shortest paths. It is calibration for the method, not evidence of historically novel thought.

The [prompt contract](../../data/ground_truth/prompt_contract.json), [protocol](protocol.md), [split policy](../../data/ground_truth/split_policy.json), [annotation guide](evidence_and_annotation.md), and [schema](../../data/ground_truth/schema.json) separate evaluator information from model-visible inputs. Both primary arms receive A/B. Donors end at a common neutral cue before generated answers. A grounded development pair has DPO donor probability 16/97 and recipient probability 3/4, recomputed from premises; copying the donor answer fails the recipient verifier. That pair is same-family development only. Final structural confirmation remains unmaterialized and cannot be made from these exposed examples.

The [infrastructure adapter](../../tests/ground_truth/infrastructure_adapter.py) exports the sibling branch's exact public JSONL schema and evaluates raw answers separately. Native calibration maps to mechanics; no public item becomes confirmation. The compatibility check reads actual source at infrastructure commit `c5a361363de8bb08aacc5119f1f435a847ad44d3`, without merging or changing that branch. Its reported CPU smoke success is a mechanics result, not behavioral validation of any fixture.

## Findings that change experimental choices

| Finding | Consequence |
| --- | --- |
| Pythia `main` includes post-DPO safetensors; `step143000` branches moved in 2026, and the 2.8B `.bin` identity changed | Use audited literal April 2023 revisions and file identities, not names that sound like immutable training steps |
| April 29 Qwen templates differ from the July 26 mechanics templates despite matching weight identities | A May 2025 historical lane needs the original full snapshot and its own template/runtime checks |
| FlashAttention's scoped online merge has 2018 softmax and 2021 attention antecedents; retained code also has a May 20, 2022 commit before its arXiv date | Reject “rediscovered FlashAttention” for recovering that identity; audit public code visibility and the particular systems contribution separately |
| Low-rank additive/fusible adaptation has 2016 and 2018 antecedents | Reject generic low-rank update plus merge as uniquely LoRA's discovery |
| The scalar speculative residual sampler already appears in 2017 maximal coupling; SOAP points to an essentially equivalent older optimizer | Reject the later-paper attribution of those narrow identities; retain as precise method controls |
| CUSP's detailed auditor explicitly exempts correct predictions/methodologies matching the paper | Output similarity alone must not invalidate a rediscovery |

Evidence and exact revisions are in the [model audit](model_audit.md), [lead temporal audit](lead_temporal_audit.md), [survey](candidate_survey.md), and [benchmark audit](benchmark_audit.md). Dates reflect inspected primary records and bounded searches; commit timestamps alone do not prove historical public visibility.

## What changes make the deductions valid

These are verified mathematical distinctions, not measured effects of hints on a model:

- **DPO:** same-context reward offsets cancel, yielding 16/97 in the first finite example. Different contexts with an unspecified relative reward offset remain UNKNOWN. Additional algebra cannot replace that missing information.
- **Speculative correction:** acceptance and residual mass must use the actual proposal distribution. The stale-score control gives output (3/8, 5/8), not its desired (1/4, 3/4). Restoring the matched proposal assumptions restores the exact marginal identity; speed still needs measurement.
- **DoRA:** the true normalized function derivative removes a radial direction change. A detached denominator gives a different autodiff rule: the paired example changes from (0,0) to (12,16). Neither derivation establishes fine-tuning quality or a new 2024 theorem. The supplied-construction forward fixture tests execution, not invention of that construction.
- **MeanFlow:** differentiation along the supplied velocity field, with the earlier time fixed, gives the intended relation. Replacing the total derivative with a partial derivative is wrong in the state-dependent example. Moving the lower time requires the corresponding boundary term. The field is defined for neighboring endpoint states; a single observed trajectory alone would not identify its partial derivatives.
- **Synthetic offsets and navigation:** shared offsets, connected constraints and sufficient state information permit exact deductions. Per-reading offsets, disconnected constraints, contradictory observations and unreachable goals retain their appropriate non-answer outcomes. A shortest path may revisit a room with another badge state.

The renderer and verifier accept alternative valid routes. For example, attention can be computed directly from all supplied scores; correct output is not evidence that a particular merge algorithm was used. Future experiments can measure behavioral sensitivity to a bridge and causal transfer, but cannot read a uniquely missing thought from generated reasoning.

## Review and validation

Independent AI workers performed temporal, benchmark and adversarial reviews; these are not human peer reviews. Requested worker configurations included GPT-6.1 Sol xhigh and Astra xhigh; exact serving builds were not independently attested. The [adversarial review](adversarial_review.md) records both findings and residual limits.

Review produced concrete fixes: structured target/response contracts; visible reason-code vocabularies; nested attention-block projection preventing hidden metadata leakage; strict duplicate-key parsing; explicit counterfactual/template lineage checks; typed evaluation/seed/timestamp fields; genuine irrelevant controls; shared A/B in synthetic primary arms; and a neighborhood definition for MeanFlow partial derivatives. All final tests and exact counts are recorded in [validation_report.json](../../data/ground_truth/validation_report.json). Reproduction commands:

```sh
python -m unittest discover -s tests/ground_truth -v
python tests/ground_truth/artifact_tools.py validate
python tests/ground_truth/calibration.py check-fixtures
python tests/ground_truth/check_sibling_interface.py
python tests/ground_truth/artifact_tools.py manifest --check
git diff --check
```

Ten version-specific paper PDFs were lawfully retrieved temporarily and hashed for version inspection; only citations, hashes and original summaries are committed. Public model metadata and tokenizer files were inspected; no checkpoint weights, restricted corpus, copied paper PDF or inference outputs are committed. The [manifest](../../data/ground_truth/manifest.json) records raw-byte hashes of this collection. It is not a guarantee of source truth or historical exclusion.

## Use within the programme

The [corpus protocol](../../Plan/corpus-protocol.md) governs admission of actual
scientific contributions. For MeanFlow, audit the training design and its
antecedents rather than admitting the classical calculus identity as a new
discovery. Historical model lanes require complete artifact and interface
evidence, competence checks and independent domain/temporal adjudication.

Use these public fixtures to check scoring, prerequisite competence, prompt
boundaries and exact verifiers. The [measurement protocol](../../Plan/measurement-protocol.md)
defines the observational study's semantic endpoints and confirmation process.
No supplied prompt has a measured hint benefit, and these exposed fixtures
cannot become a sealed confirmation set.

Transfer and specificity studies require the [causal study gates](../../Plan/causal-review.md)
and their own held-out population, donor policy and power analysis. The local
[transfer calibration protocol](protocol.md) supplies controls for that stage.
Scientific admission, human review, licensing and behavioral evidence remain
unresolved; passing fixture checks cannot settle them.
