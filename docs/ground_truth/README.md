# Ground-truth research collection

This is a research specification and an executable development collection, not a completed historical benchmark or a model-performance report. Read [the decision report](decision_report.md) for the current recommendation and unresolved gates. Every fixture committed here is public calibration/development material. **There is no sealed confirmation set in this repository.**

The collection contains 20 ranked leads, five worked research packets, six model snapshot audits and 51 exact fixtures. No historical candidate is fully admitted and no target-model behavior is measured here.

| Artifact | Purpose |
| --- | --- |
| [Candidate survey](candidate_survey.md) / [registry](../../data/ground_truth/candidate_registry.json) | Ranked claims, dated primary evidence, antecedents, and exclusions |
| [Model audit](model_audit.md) / [record](../../data/ground_truth/model_audit.json) | Historical snapshot identities, release evidence, post-training limitations |
| [Lead temporal audit](lead_temporal_audit.md) | DPO, FlashAttention, and LoRA chronology and prior-art conflicts |
| [Evidence packets](packets/) | Derivations, prerequisites, bridges, counterexamples, and empirical limits |
| [Benchmark audit](benchmark_audit.md) | ResearchBench, DiscoveryBench, CUSP, Reconstruction and licensing |
| [Evidence and annotation guide](evidence_and_annotation.md) | Admission hierarchy, dates, independence and reviewer checklist |
| [Experiment protocol](protocol.md) | Primary estimand, prompt ladder, donor boundary, splits and interpretation |
| [Calibration specification](calibration.md) | Tiny exact offset and badge worlds, standalone prerequisite probes |
| [Infrastructure interface](interface.md) | Versioned paths, visible/hidden boundary, run and model requirements |
| [Adversarial review](adversarial_review.md) | Independent AI review findings, fixes, scope and remaining limits |
| [Schema](../../data/ground_truth/schema.json) | Machine-readable candidate, fixture, prompt, and run contracts |
| [Manifest](../../data/ground_truth/manifest.json) | Content hashes and provenance; reproducible with the command below |

Run from the repository root, using Python 3.10 or newer and the standard library:

```sh
python -m unittest discover -s tests/ground_truth -v
python tests/ground_truth/artifact_tools.py validate
python tests/ground_truth/artifact_tools.py manifest --check
```

`manifest` without `--check` rebuilds the inventory after an intentional change. It hashes raw bytes, not a reserialized approximation. Do not regenerate it to hide unexpected drift. Source URLs and revision identifiers refer to upstream evidence; local file hashes attest to this collection, not to the truth of the historical claims. No paper PDFs, restricted datasets, checkpoint weights, or model responses are included.

The collection includes a narrow CUSP evidence correction in [Plan/research-plan.md](../../Plan/research-plan.md); unrelated plan sections remain unchanged. Current-main verification and the base revision are recorded in the manifest. Code and data licensing for these new original artifacts remains an explicit repository-owner decision; no upstream paper or model license is inherited automatically.
