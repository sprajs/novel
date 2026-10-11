# Speculative decoding: residual correction preserves a marginal

Candidate ID: `speculative-decoding`. Status: **public development composition packet; reject novelty of the scalar identity in 2022**. The target is a one-step exact sampling construction, not a wall-clock speedup or the invention of speculative execution.

## Proposition, prior information, and dates

Let p and q be probability distributions on one finite alphabet. Prerequisite A: drawing X from q and accepting it with probability `min(1, p(X)/q(X))` assigns accepted mass `min(p_i,q_i)` to symbol i. The acceptance ratio is needed only for q_i > 0. Prerequisite B: for disjoint accepted/rejected branches, output probability is accepted mass plus rejection probability times the conditional fallback probability. Nonnegative masses can be normalized by their positive total.

Supply A and B, the full vectors, and the definition of exactness in both primary arms. Ask the model to construct the fallback distribution and prove that every output marginal equals p, including q-zero symbols and the p=q case. A gives the standard accept/reject operation; B gives probability accounting. Giving the residual formula as a premise would make the construction a substitution exercise and must be a separately labeled easier arm.

[Leviathan, Kalman, and Matias v1](https://arxiv.org/abs/2211.17192v1) was submitted 2022-11-30 at 17:33:28 UTC; [Appendix A.1](https://arxiv.org/html/2211.17192v1) proves the corrected sampling marginal. [Chen et al. v1](https://arxiv.org/abs/2302.01318v1) was submitted 2023-02-02 at 18:44:11 UTC. Its 2023 date cannot serve as the earliest disclosure for the overlapping scalar construction.

The stronger historical obstacle is [Jacob, O'Leary, and Atchadé v1](https://arxiv.org/abs/1708.03625v1), submitted 2017-08-11, whose [Section 4.1, Algorithm 4 and Appendix B](https://arxiv.org/html/1708.03625v1) already give maximal coupling by acceptance plus residual rejection sampling. Swap their p/q roles to match this packet's draft/target convention. They cite Thorisson's 2000 book, Chapter 1 Section 4.5, as an earlier description. That book attribution is a lead, not a claim that its full text was independently inspected here. A scalar residual-identity success cannot establish reconstruction of a new 2022 discovery.

## Bridges and controls

Minimal bridge: **“Account for the target probability mass already supplied by the accepted branch.”** Alternate: **“Partition each symbol's target mass into shared and unfilled portions.”** Fresh-context probes test threshold acceptance mass, mixture probabilities, normalization of a nonnegative vector, and treatment of a zero-probability event.

Wrong bridge: “After rejection, draw again from the unchanged target distribution.” Irrelevant true text: “Permuting the labels of a categorical distribution preserves its total probability.” Answer-only for `spec-dev-001` is the expected JSON in the fixture file, including fallback `(0,0,1)`; its donor state must not enter the primary minimal-bridge contrast. A full-explanation donor contains the following derivation and is only a leakage/ceiling control. Include p=q as a bridge-unnecessary case and a deliberately stale proposal-probability case as a bridge-inapplicable control.

## Worked derivation and exact finite example

Write `c_i=min(p_i,q_i)`, `alpha=sum c_i`, and `rho=1-alpha`. Because p and q both sum to one,

```text
d_i = p_i - c_i = max(p_i-q_i, 0)
sum d_i = rho.
```

For rho>0 the residual distribution is `r_i=d_i/rho`. The output mass is `c_i + rho r_i = p_i`, individually for every i. For rho=0, p=q, rejection never occurs, and the fallback distribution is unused; returning 0/0 is an error. If q_i=0<p_i, that symbol cannot be accepted but receives the needed mass through the fallback. Disjoint supports give alpha=0 and fallback=p. This is exact real/rational probability accounting; it does not imply floating-point implementations generate bit-identical streams with a conventional decoder.

`spec-dev-001` uses target p=(1/3,1/6,1/2) and draft q=(1/2,1/3,1/6). The acceptance probabilities are (2/3,1/2,1); accepted masses are (1/3,1/6,1/6), totaling 2/3. The missing masses are (0,0,1/3), so rejection probability is 1/3 and fallback is (0,0,1). Adding the branches recovers p. The wrong “resample p” fallback instead returns `(4/9,2/9,1/3)`, visibly biased.

An alternative valid route formulates a coupling: the common mass is the diagonal component and the unmatched p mass is the second marginal of the residual component. Another samples repeatedly from p, accepting a proposed fallback i with probability `(p_i-q_i)_+/p_i`; its eventual conditional law is the same r. These routes earn full consequence credit.

The executable oracle computes acceptance and branch probabilities with `Fraction`. An independent regression check enumerates equally likely points on finite rational grids for proposal, acceptance, and residual draws rather than sampling randomly. A sweep over all three-symbol integer-count distributions of total four checks zeros, equality, and disjoint support. These checks validate the one-step finite construction; extending to autoregressive strings requires the same argument at each actual retained prefix. Cache handling and batched proposal verification are additional implementation obligations.

## Inapplicability, performance, and audit boundary

In `spec-dev-004`, actual draft q=(3/4,1/4), target p=(1/4,3/4), but the acceptance ratio and fallback are computed from stale draft scores (1/2,1/2). The output becomes `(3/8,5/8)`, not p. A selective bridge intervention should identify this failure instead of asserting that every accept/reject sampler is exact. The output schema reports the actual marginal and `target_equal:false`; it does not conceal the counterexample by returning the claimed p. Scores after top-k/top-p/temperature transforms must refer to the distribution actually sampled, and both primary arms must contain any such transforms.

No hardware latency, draft cost, acceptance behavior on real corpora, or speedup is supplied by these premises. Those are empirical questions. The dated search inspected both decoding v1 records, their exactness argument, and the 2017 maximal-coupling construction; queries included “Unbiased Markov chain Monte Carlo with couplings” and “SpecTr maximal coupling.” Earlier deterministic blockwise decoding and speculative-execution work, patents, talks, and project history remain to audit if a different systems contribution is proposed. This packet has already found enough prior art to reject the scalar novelty claim; incomplete search is not a reason to rescue it.

Apply the [common immutable checkpoint requirements](README.md) with a cutoff appropriate to the *actual claim*. A pre-November-2022 checkpoint alone cannot make the already-known coupling theorem a later discovery. Qwen3 provides no relevant historical evidence. Target and antecedent v1 PDF hashes are in [source snapshots](source_snapshots.json). Leviathan v1 displays CC-BY-4.0; the 2017 arXiv source has the nonexclusive distribution license. The repository contains original finite examples and no copied upstream sampling code or evaluation data.
