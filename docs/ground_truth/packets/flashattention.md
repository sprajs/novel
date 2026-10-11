# FlashAttention: a deliberately rejected novelty target

Candidate ID: `flashattention`. Status: **public development algebra packet and historical-adjudication negative control**. Its scoped target—merging stable softmax attention summaries—is useful and verifiable, but already described before FlashAttention. This packet must not be admitted as rediscovering a new 2022 result.

## Proposition and chronology

For a fixed query and disjoint key blocks B, let scores be s_i, vector values v_i, and define a block summary

```text
m_B = max_i s_i
l_B = sum_i exp(s_i-m_B)
z_B = sum_i exp(s_i-m_B) v_i.
```

Prerequisite A is the shift invariance of softmax: multiplying all exponentiated scores by one positive factor does not change normalized weights. Prerequisite B is the weighted-average definition of attention and additivity of sums over disjoint sets. Both definitions and the block data are given in both primary arms. Ask for a merge operation returning the same global attention as the unblocked computation, without retaining all individual scores and values. Supply the summary fields to make the target a merge-composition task, not invention of a data structure. Hindsight selection of those fields is substantial assistance.

[FlashAttention v1](https://arxiv.org/abs/2205.14135v1) was submitted 2022-05-27 at 17:53:09 UTC. The relevant [Section 3.1 / Algorithm 1](https://arxiv.org/html/2205.14135v1) combines exact attention with tiling and memory-aware execution. This packet does not attempt to reconstruct its IO-complexity result, recomputation scheme, GPU kernel, or empirical performance.

[Milakov and Gimelshein v1](https://arxiv.org/abs/1805.02867v1), submitted 2018-05-08 at 07:34:17 UTC, gives an online normalizer update. More decisively, [Rabe and Staats v1](https://arxiv.org/abs/2112.05682v1), submitted 2021-12-10 at 17:25:07 UTC, already gives the [stable running attention numerator and denominator, and chunked implementation in Sections 3–4](https://arxiv.org/html/2112.05682v1). Its formulas use rescaling by maximum differences for both statistics. This antecedent covers the chosen target, not merely a vague neighboring idea. A post-2021/pre-May-2022 model can already have encountered the result; an earlier model would need a cutoff against the earlier claim.

## Bridges and controls

Minimal bridge: **“Convert the block summaries to the same reference scale before combining them.”** Alternate: **“Undo each block's local normalization only up to a shared global factor.”** Neither gives a numeric answer. Fresh-context probes test softmax shift invariance, combining unnormalized weighted sums, scalar multiplication of vectors, and handling masked elements.

Wrong bridge: “Average the separately normalized block outputs with equal weight.” Irrelevant true text: “A permutation matrix preserves a vector's Euclidean norm.” Answer-only for `flash-dev-001` is the expected JSON containing output `(9/7,2)`, merged maximum exponent 2, denominator 7/4 and numerator `(9/4,7/2)`. Full explanation contains the following derivation and is a leakage/ceiling condition. Single-block inputs are bridge-unnecessary controls. Only-normalized-output summaries are underdetermined; fully masked rows are undefined under the specified operation.

## Worked derivation and exact fixture

For blocks A and B choose `m=max(m_A,m_B)`, `a=exp(m_A-m)`, `b=exp(m_B-m)`. Then

```text
l = a l_A + b l_B
z = a z_A + b z_B
output = z/l.
```

Every rescaled term satisfies `exp(m_A-m) exp(s_i-m_A)=exp(s_i-m)`. Thus l and z are exactly the denominator and numerator of global stable attention. The argument proves associativity of merging nonempty summaries in exact arithmetic because every merge represents the same unnormalized sum at its recorded reference scale. In floating point, different merge trees can differ by rounding; no claim of bitwise equality is made.

To avoid transcendental approximations, the fixtures choose `s_i=k_i log 2` with integer k_i, so every exponential difference is the exact rational `2^(k_i-k_j)`. The field `score_exponents` records k, not s, and `maximum_exponent` uses the same convention. This is a declared test subfamily of ordinary exponential softmax, not a different “base-two attention” model.

`flash-dev-001` has block A with k=(0,1), values ((1,0),(0,1)); and block B with k=(2), value ((2,3)). A's summary is `m_A/log2=1, l_A=3/2, z_A=(1/2,1)`. B's is `2, 1, (2,3)`. The merged maximum is 2; scale A by 1/2 and B by 1, yielding `l=7/4`, `z=(9/4,7/2)`, and output `(9/7,2)`. Independently, raw weights (1,2,4) give numerator `(9,14)` and denominator 7. Equal averaging of the local outputs instead gives `(7/6,11/6)`, which fails.

A valid alternative merges unnormalized raw exponentials without subtracting maxima, then divides. It has worse numerical stability for general inputs but is mathematically correct and must receive consequence credit. Another merges block normalized outputs using their correctly rescaled probability masses. The independent test oracle flattens all unmasked tokens and computes their raw exact weighted average; it does not call the block-merge implementation. Tests vary block partitions, order, common score offsets, vector values, negative exponents, and masks.

Because the public numeric fixtures expose raw tokens, flattening is available to the model too. Success validates the output consequence and does not prove the model used a streaming merge operation or discovered sufficient statistics. A future merge-only task would have to supply only summaries and use an independently checked intermediate certificate, under a separately declared experimental endpoint.

## Unknown and inapplicable worlds

If only each block's normalized output is supplied, the merge generally cannot be determined. For two one-token blocks with scalar outputs 0 and 1, equal unnormalized masses give global output 1/2, whereas masses 1 and 3 give 3/4; both observations have the same local outputs. `flash-dev-003` expects UNKNOWN because the relative mass/reference information is absent. The bridge cannot create it. Equal local outputs would be an identifiable special case and must not be labeled UNKNOWN blindly.

For a fully masked row, the denominator is zero. `flash-dev-004` expects UNDEFINED, as this packet specifies no library-specific convention such as an all-zero output. In `flash-dev-002`, a masked high-score distractor must not affect the result, which is exactly 1. Dropping masks or double-counting overlapping blocks changes the specified weighted sum. Blocks are explicitly disjoint here; overlap would require a different inclusion rule.

## Admission, systems claims, and rights

On 2026-10-11 the audit examined the three version-specific papers, their recorded submission histories, and the actual online/chunked equations; searches included “Online normalizer calculation for softmax” and “Self-attention Does Not Need O(n^2) Memory.” This is enough to reject this narrow 2022 novelty claim, even while earlier attention/coupling variants and non-paper disclosures remain unsearched. A later project could choose a genuinely distinctive IO theorem as its target, but would need explicit machine-model premises and an independent proof checker; replacing the target is a new candidate, not a repaired label for these fixtures.

Correct block algebra alone does not establish lower wall time, kernel availability, memory traffic, backward-pass correctness, or a reproduced scientific discovery. Apply the [common immutable model audit](README.md); no checkpoint is certified, and Qwen3 supplies no pre-2022 historical witness. The temporary v1 PDF checks are identified in [source snapshots](source_snapshots.json). The three arXiv first versions display the nonexclusive distribution license rather than a blanket redistribution license. These packets contain no copied kernels, source PDFs, figures, or upstream benchmark examples.
