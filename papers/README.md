# Primary papers and local reading cache

Checked against official sources on **11 October 2026**. This is a bounded selection
for the first research increment, with original notes from targeted reading of
methods, controls, and limitations. It is not an exhaustive survey or a claim that
every newer related paper has been found. The source of truth is
[manifest.json](manifest.json): exact titles, all authors as listed on the selected
version, submission/version dates, official URLs, DOI status, license evidence,
reading scope, and observed PDF checksums.

All ten selected PDFs were retrieved from versioned arXiv URLs with HTTP 200 and
their first-page identifiers inspected. They occupy **39,121,949 bytes** (39.1 MB)
in `.cache/papers/`. The manifest records hashes of those observed bytes; these are
not publisher-signed checksums. The current environment successfully accessed both
arXiv and ACL on this date, so the earlier network-blocking assumption is obsolete.

## Lawful access and repository policy

PDFs belong only in the ignored local cache and **must never be committed**.
The repository carries links, bibliographic metadata, and original notes.
[arXiv permits anyone to view and download its papers](https://info.arxiv.org/help/license/index.html),
but public access does not establish a right to redistribute a paper. Each exact
version's `view license` link was checked: seven selected versions point to
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), while the patching tutorial,
Function Vectors, and the September targeted-feature paper point to the
[arXiv nonexclusive distribution license](https://arxiv.org/licenses/nonexclusive-distrib/1.0/).
That latter license grants distribution rights to arXiv. The manifest does not
infer additional redistribution rights for this project. Publisher versions and
third-party figures may carry different conditions; those rights were not audited.

The CAA arXiv version lists Nina Panickssery and Alexander Matt Turner; its
[ACL citation](https://aclanthology.org/2024.acl-long.828/) lists Nina Rimsky and
Alexander Turner. The manifest preserves the authors of the selected arXiv PDF
instead of silently mixing version metadata. The September paper's arXiv DOI was
marked pending registration on the source page when checked.

## Retrieval and integrity checks

The downloader requires an explicit action and never modifies the manifest:

```bash
python scripts/download_papers.py --list
python scripts/download_papers.py --dry-run function-vectors caa
python scripts/download_papers.py --download function-vectors caa
python scripts/download_papers.py --verify function-vectors caa
```

To reproduce the complete selection, pass its explicit IDs:

```bash
python scripts/download_papers.py --download \
  patching-interpretation patching-best-practices function-vectors caa \
  atp-star soft-reasoning noise-steering creativity-neuro nnsight-ndif \
  targeted-feature-learning
```

Only standard-library Python is needed. `--list`, `--dry-run`, and `--verify` work
offline; tests never request the network. Downloads use HTTPS, approved official
hosts, a 20-second socket timeout, and an elapsed-time check with a 60-second
transfer deadline. The deadline is checked around reads; an in-progress read is
bounded by the socket timeout. Redirects are validated before following them.
The downloader caps each file at 25,000,000 bytes and the entire paper cache at
90,000,000 bytes, including temporary files. Both advertised and streamed sizes
are checked. It rejects error pages, truncation, unsafe IDs, and symlinked paths;
temporary files are cleaned after failure. Publication is atomic and refuses an
existing destination, including one created by another process.

A cached hash mismatch fails before any network request and preserves the file.
A newly retrieved checksum mismatch also fails without publishing a PDF. There
is no overwrite/force option. If a future curated entry initially has no hash,
the command emits an unpinned acquisition receipt; inspect PDF identity and record
that observed hash in the manifest before reusing it. An existing unpinned PDF is
never silently trusted. Retrieval failures are errors with a nonzero exit code;
they do not fabricate successful retrieval records.

## Reading sequence and notes

The first five papers support the bridge-transfer study; the following three
inform perturbation/search controls; the last two inform tooling and current
method comparisons. Exact bibliography and fuller machine-readable notes remain
in the manifest. The notes below are interpretations for this experiment, not
independent replications of the papers' results.

| Cache ID and official primary source | Pinned version date | What to read |
| --- | --- | --- |
| [patching-interpretation](https://arxiv.org/abs/2404.15255v1) — How to use and interpret activation patching | 2024-04-23, v1 | Sections 2–4 |
| [patching-best-practices](https://arxiv.org/abs/2309.16042v2) — Towards Best Practices of Activation Patching in Language Models: Metrics and Methods | 2024-01-17, v2 | Sections 3–5 |
| [function-vectors](https://arxiv.org/abs/2310.15213v2) — Function Vectors in Large Language Models | 2024-02-25, v2 | Sections 2–3, 5 |
| [caa](https://arxiv.org/abs/2312.06681v4) — Steering Llama 2 via Contrastive Activation Addition | 2024-07-05, v4 | Sections 3–5, 10 |
| [atp-star](https://arxiv.org/abs/2403.00745v1) — AtP*: An efficient and scalable method for localizing LLM behaviour to components | 2024-03-01, v1 | Sections 3–5 |
| [soft-reasoning](https://arxiv.org/abs/2505.24688v4) — Soft Reasoning: Navigating Solution Spaces in Large Language Models through Controlled Embedding Exploration | 2025-09-13, v4 | Sections 4–5; verifier noise |
| [noise-steering](https://arxiv.org/abs/2604.03380v2) — Noise Steering for Controlled Text Generation: Improving Diversity and Reading-Level Fidelity in Arabic Educational Story Generation | 2026-05-02, v2 | Sections 4–6; Limitations |
| [creativity-neuro](https://arxiv.org/abs/2607.01433v1) — CreativityNeuro: Steering Language Model Weights to Improve Divergent Thinking and Reduce Mode Collapse | 2026-07-01, v1 | Sections 3–8; Appendix F |
| [nnsight-ndif](https://arxiv.org/abs/2407.14561v4) — NNsight and NDIF: Democratizing Access to Open-Weight Foundation Model Internals | 2025-04-01, v4 | Sections 3–5; framework examples |
| [targeted-feature-learning](https://arxiv.org/abs/2609.32355v1) — Gradients for Interventions and Activations for Detection: Targeted Feature Learning in Language Models | 2026-09-26, v1 | Sections 3–4, 6; Appendix B selection |

**Patching interpretation.** Restoration and disruption supply different,
conditional evidence. Use both directions and several controlled corruptions.
Serial dependencies and backup computations can explain asymmetric or null
results. A successful replacement alone does not identify the unique mechanism
the unmodified model normally uses.

**Patching best practices.** Corruption and metric choices can change the map of
important sites. Borrow counterfactual token replacements and corruption-severity
checks; keep logit differences and independently verified generation accuracy.
Gaussian corruption can distort computation, while saturated probabilities can
hide relevant effects. Their methodological findings are task-dependent.

**Function Vectors.** Task-conditioned attention-head means transfer to new prompt
contexts, and some compositions work. Borrow shuffled demonstrations, zero-shot
recipients, altered templates, and output-space controls. Extraction filters for
successful demonstrations and uses task labels and head selection. This makes
generic vector transfer established prior art; the bridge study needs its stricter
different-answer and structural holdouts.

**CAA.** Average paired residual differences and inject them after the instruction.
Borrow held-out free generation, prompting comparisons, and joint layer/amplitude
checks. Its donor contrasts contain answer tokens: copying that extraction protocol
into this study could encode the result. Its free-text evaluations also rely on an
LLM judge, and intervention norms complicate layer comparisons.

**AtP*.** Attention saturation and direct/indirect cancellation cause false
negatives in simple gradient approximations. Use gradients to rank sites, then
check selected and low-ranked sites with exact patches. The study emphasizes
fine-grained nodes and limited prompt distributions; large residual replacements
can be more nonlinear and may be inexpensive enough to check exactly first.

**Soft Reasoning.** The method perturbs an initial generated-token embedding,
greedily continues, and searches embeddings with Bayesian optimization using
same-model verification and coherence rewards. Compare random perturbation,
adaptive search, and token-space branching separately; count all verifier and
generation calls. Its combined gains do not isolate noise, and self-verification
is fallible. Deterministic decoding does not imply every vector yields a distinct
answer.

**Noise Steering.** Decode-only internal perturbations with decay are direct prior
art for temporary noise and recovery. Borrow activation-scale calibration and
separate retained-cache from clean re-prefill experiments. Reported story diversity
does not establish correct reasoning. The authors acknowledge untuned fixed
high-temperature baselines and LLM-judge limitations. Section 4.5 states both
base-scale and recursive decay expressions; declare the implemented schedule
explicitly before replication.

**CreativityNeuro.** Contrastive prompt importance masks rescale weights and
improve reported divergent-thinking originality. Borrow separate originality and
utility outcomes, blinded evaluation, and unrelated factual-competence checks.
The reported Alternative Uses utility reduction and factual-reasoning entanglement
matter for a useful-idea claim. Prompt sets and hyperparameter sweeps still provide
assistance, even without scored behavioral training examples.

**NNsight/NDIF.** The intervention graph separates experiment specification from
local or remote execution. Keep hook sites and timing explicit and compare wrappers
against direct hooks and a no-intervention path. The author's
[26 February 2026 NNsight 0.6 release](https://nnsight.net/blog/2026/02/26/introducing-nnsight-06/)
describes execution changes, vLLM integration, and NNterp standardization. These are
tooling leads; neither the earlier paper nor the release proves compatibility with
this repository's Qwen3 execution and cache semantics. No NNsight installation or
remote execution was performed here.

**September 2026 targeted-feature comparison.** Three signals and two estimators
give different rankings for feature detection and intervention across 15 tasks.
Borrow train/validation/test separation, bidirectional intervention, and an
unrelated-language-loss constraint. Read its signal timing carefully: activation
contrasts fill in targets; gradients condition on target labels. Its intervention
metric measures target-token probability, not free-generation correctness or
bridge transfer. Learned estimators add supervision. Treat this recent preprint as
a control-design lead rather than validation of our proposed mechanism.

Two further 2026 sources were checked at **abstract/metadata level only**, with
complete version and license records under `context_only_sources` in the manifest;
their PDFs were not retrieved. [GTS v2, 18 March 2026](https://arxiv.org/abs/2602.14077v2)
trains a conditional Gaussian sampler using policy optimization despite a frozen
backbone. [LatentTTS v4, 19 April 2026](https://arxiv.org/abs/2510.07745v4)
combines latent trajectory sampling with a trained latent reward model. Their
training and selection costs must accompany any comparison; abstract-level checks
do not establish plug-and-play transfer to the frozen text-model assay.

## Verification

```bash
python -m unittest discover -s tests -p test_papers.py
```

Sixteen offline tests cover manifest completeness, version pinning, safe IDs and
redirects, atomic publication, checksum preservation, size budgets, PDF/error-page
checks, interrupted transfers, deadlines, symlinks, and offline actions. The ten
actual cached files also passed `--verify` against the recorded hashes. Full-paper
replications, exhaustive related-work coverage, and Qwen3 tool compatibility remain
outside this retrieval increment.
