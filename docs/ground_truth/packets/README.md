# Research evidence packets: public development material

Prepared 2026-10-11. These are newly authored, fully exposed teaching and verifier fixtures. They are **not sealed tests, historical reconstructions, or experimental results**. No model was run. The five packets deliberately distinguish a paper-associated identity from the paper's research contribution.

| Packet | Exact executable target | Historical disposition |
| --- | --- | --- |
| [DPO](dpo.md) | Eliminate the context normalizer from a pairwise preference likelihood | Promising selected-prerequisite composition; earliest equivalent disclosure and checkpoint audit incomplete |
| [Speculative decoding](speculative-decoding.md) | Recover the exact target marginal with residual sampling | Valid composition task; reject a claim that the scalar identity originated in 2022 because maximal coupling predates it |
| [DoRA](dora.md) | Compose low-rank updates and normalization; distinguish true and detached derivatives | Forward composition is usable; projection derivative is older weight-normalization algebra, not a new 2024 theorem |
| [FlashAttention](flashattention.md) | Merge stable attention sufficient statistics | Intentionally rejected 2022 novelty target: the scoped identity already appears in pre-2022 attention work |
| [MeanFlow](meanflow.md) | Differentiate interval-average velocity along a specified flow | Recent application worth auditing with April 2025 checkpoints; the calculus identity itself is classical |

Each packet supplies prerequisite A and B in both primary arms. The primary contrast is `A+B+question` versus the identical text plus a short relational bridge. Historical source titles, bibliographies, target paper, dates, worked derivations, verifier metadata, and expected outputs are evaluator material. A prompt renderer must allowlist the designated premise, question, response-schema, and condition text rather than serialize a whole fixture. Source selection itself is hindsight assistance and must be reported as such.

The [JSON fixtures](../../../data/ground_truth/research_fixtures.json) contain exact rational examples, edge cases, and counterexamples. They share `schema_version = ground-truth-v0.1`; all use `split = development`. The public expected labels cannot subsequently be made sealed by renaming their split. The [verifiers](../../../tests/ground_truth/research_verifiers.py) and [regression checks](../../../tests/ground_truth/test_research_packets.py) use Python's standard library and `Fraction`. Run from the repository root:

```sh
python -m unittest discover -s tests/ground_truth -p 'test_research_packets.py' -v
```

The additional [MeanFlow fixtures](../../../data/ground_truth/meanflow_fixtures.json) and [verifier](../../../tests/ground_truth/meanflow_verifier.py) exercise exact calculus, partial versus total derivatives, and invalid moving-boundary assumptions. All 31 research examples are public development. The scoped test command above covers the first four packets; the full discovery command in the collection README also runs MeanFlow and interface checks.

These check finite instances and specified rational subfamilies. They do not automatically grade arbitrary natural-language proofs, establish general theorem discovery, or establish empirical speed/accuracy improvements. Alternative derivations receive equal credit if their final structured consequence satisfies the independent specification. Proof-strategy diversity would need a separate equivalence rubric; different prose is not a new method.

Every fixture's `target` object contains a `question` and explicit `response_format`, including the allowed machine reason codes. The code is part of the answer contract; arbitrary explanation prose is not checked or silently treated as a proof. `research_verifiers.visible_prompt(fixture)` creates the six allowed model-visible fields for `artifact_tools.build_prompt_record`; it does not render evaluator-only metadata. A label reversal or derivative-mode counterfactual has a recorded `counterfactual_parent_id` and is not an independent new world for statistical inference.

## Common protocol and unresolved dependencies

Prerequisite probes must run in fresh contexts. Keep the prospectively selected cohort, including failures. Assess A, B, and their immediate applications before interpreting a composition gap. Extract any donor activation after the bridge and neutral continuation cue but before the answer or derivation. Different donor and recipient worlds must have different answers, with answer-token overlap tracked. Reserve future structural families, model choices, extraction sites, and vector tuning for a genuinely new, unmaterialized confirmation set.

Every packet needs premises-only, minimal bridge, alternate valid bridge, wrong bridge, irrelevant true text, answer-only, and full-explanation arms. Add an ordinary “reason carefully” prompt and ordinary demonstrations under the same budget. A strong effect must improve over the unmodified baseline as well as a sham, preserve undefined/unknown judgments, and survive different-answer transfer. False bridge benefit, donor-answer copying, or indiscriminate numeric answers are failures of the proposed selective-computation explanation. No-op and negative-direction intervention checks are instrumentation requirements, not represented as new factual worlds here.

**No immutable historical checkpoint is certified.** For each candidate the experiment ledger must eventually record model repository, exact commit, weight and tokenizer hashes, chat template and special-token hashes, complete post-training lineage, exact public availability evidence, frozen inference code revision, numerical format, and every external tool/corpus/prompt dependency. A commit timestamp alone does not prove public availability. A base model's release does not date a later fine-tune. Mutable `main`, an advertised training cutoff, and a paper title are insufficient. A signed or independently archived release record and artifact identity are needed before a historical admission decision. The target cutoff must be the earliest found public equivalent claim, including earlier talks, abstracts, code, slides, patents, and precursor papers—not automatically the preprint's submission date. Qwen3 can be a modern composition pilot; it cannot establish pre-disclosure reconstruction for these 2022–2024 claims.

The audit performed here covers the explicit sources and searches documented in each packet. Absence of a search hit is not proof of novelty. Search engines and current GitHub pages cannot establish completeness of historical coverage. Remaining searches must examine author/project histories, conference submissions, announcements, and equivalent formulations across fields. Do not infer clean contamination status from model failure or from asking the model whether it recognizes a paper.

The 2022–2024 packets require older historical models; MeanFlow has a separate provisional April 2025 Qwen lane in the model audit. Neither lane is admitted automatically. Read the Qwen-ineligibility statement above as applying to the four 2022–2024 targets, not to all later applications.

## Source handling and rights

[Source snapshots](source_snapshots.json) record SHA-256 hashes of ten version-specific PDFs retrieved on 2026-10-11 into a temporary audit directory. The PDFs were text-extracted to check that the relevant equations or algorithms occur in the cited versions; they are not vendored into this repository. The hash identifies retrieved content, not its release date or license grant. ArXiv submission histories independently support the listed version dates, but earlier non-arXiv disclosures remain open.

These packets use original exposition, new finite examples, mathematical facts, and links. They do not copy a benchmark, paper figure, paper source, or upstream implementation. ArXiv's nonexclusive distribution license is not a blanket right to redistribute papers or derivative corpora. DPO and Leviathan's v1 pages display CC-BY-4.0; DoRA's v1 displays CC-BY-NC-SA-4.0; FlashAttention v1 displays the arXiv nonexclusive license. Check exact licenses before including source text, code, model weights, or external data. No repository-wide data/code license is assigned by this work, and paper licenses do not automatically apply to these fixtures.
