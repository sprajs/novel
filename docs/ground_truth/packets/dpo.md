# DPO: removing the shared reward normalizer

Candidate ID: `dpo`. Status: **public development composition packet; historical eligibility unresolved**. The target is the policy-only Bradley–Terry probability and its negative log-likelihood, not evidence that DPO beats another alignment method.

## Proposition and pre-disclosure information

For a fixed context x and a finite action set, let q be a strictly positive reference distribution, beta > 0, and r a finite reward. Prerequisite A is the unique optimum of `sum_y pi(y) r(y) - beta KL(pi || q)`:

```text
pi(y) = q(y) exp(r(y)/beta) / Z(x).
```

Prerequisite B is a pairwise likelihood on the same context and reward scale:

```text
P(a preferred to b | x) = exp(r(a)) / (exp(r(a)) + exp(r(b))).
```

Supply both equations and assumptions in **both** primary arms. Do not give A as `r = beta log(pi/q) + constant` in the primary task: that is an optional easier prerequisite probe. Ask for a formula using pi, q, beta and a finite example; do not supply a reward vector or Z. The terms “DPO” and the target paper's name are evaluator-only metadata.

The [DPO first version](https://arxiv.org/abs/2305.18290v1) was submitted 2023-05-29 at 17:57:46 UTC. Its [Section 4 and Appendix A.2](https://arxiv.org/html/2305.18290v1) contain the mapping and likelihood substitution. The narrow new combination being tested is applying the policy–reward relation inside preference fitting; the checkpoint should not be credited with the paper's datasets, optimization behavior, or experimental results.

A predates the target: [Advantage-Weighted Regression v1](https://arxiv.org/abs/1910.00177v1), submitted 2019-10-01 at 02:23:38 UTC, has the normalized reference-policy exponential tilt in Equation 8 and Appendix A. Its advantage baseline is constant across actions at fixed state and is absorbed into the normalizer. [Relative Entropy Policy Search](https://ojs.aaai.org/index.php/AAAI/article/view/7727/7588) provides an older 2010 constrained-policy antecedent. B dates to Bradley and Terry's [1952 paired-comparison model](https://www.jstor.org/stable/2334029), documented in the publisher's [December 1952 issue](https://www.jstor.org/stable/i315445); write positive strengths as exp(r). The publisher article body was not accessible through one attempted OUP endpoint, so the mathematical formula is additionally corroborated by the explicit BT equation in DPO v1. This is not a newly discovered preference model.

## Bridge, probes, and matched conditions

Minimal bridge: **“Express each compared reward through its policy ratio, then compare within the same context.”** Alternate valid bridge: **“Work with preference odds and cancel factors shared by both choices.”** Neither contains a target number or the final likelihood.

Fresh-context probes: normalize q times supplied positive weights; rearrange a one-variable exponential relation; convert supplied positive strengths to a pairwise probability; show that adding one constant to both rewards leaves preferences unchanged. A successful target after a failed prerequisite probe does not support the proposed composition diagnosis.

Wrong bridge: “Treat each context normalizer as the reference probability of the preferred choice.” Irrelevant true text: “A categorical distribution can be sampled by dividing the unit interval into intervals of the specified probabilities.” Answer-only for the first numeric fixture: `{"status":"VALID","preference_probability":"16/97","odds":"16/81"}`. Full explanation is the derivation below; neither answer-bearing arm is a minimal bridge donor. Match style and measure exact tokenizer lengths when a checkpoint is chosen rather than claim character counts are token matching.

## Worked consequence and independent checks

Taking logs of A gives `r(y) = beta log(pi(y)/q(y)) + beta log Z`. Subtract at a single x. The shared term disappears, so with `R = pi(a) q(b) / (q(a) pi(b))`:

```text
r(a)-r(b) = beta log R
P(a > b) = R^beta / (1 + R^beta)
loss(a,b) = log(1 + R^(-beta)).
```

An independent route avoids subtracting logs: substitute `exp(r(y)) = Z^beta (pi(y)/q(y))^beta` into B and cancel the common positive factor. This route is the executable oracle. For finite positive distributions, the optimum follows by rewriting the objective as `beta log Z - beta KL(pi || pi*)`. Equality holds only at pi*. This verifies the assumption behind A; it does not assert equivalence of finite-data nonlinear optimization trajectories, PPO updates, and DPO updates.

Fixture `dpo-dev-001` uses q = (1/2, 1/3, 1/6), pi = (1/3, 1/2, 1/6), beta = 2, and compares index 0 to index 1. The ratios are 2/3 and 3/2. Their squared strengths are 4/9 and 9/4; the common denominator gives probability `16/(16+81) = 16/97`, odds 16/81, and loss `log(97/16)`. The third action checks that the problem is not silently reduced to a normalized binary policy. The verifier returns only rational probability and odds; it does not approximate the logarithmic loss.

The executable rational subfamily restricts beta to positive integers; this is a verifier limitation, not a restriction of the theorem. Tests compare direct strength normalization to the cross-multiplied odds route across multiple policies and beta values, check label swapping, and reject omission of q or beta. Equivalent fractions are accepted; equivalent proof routes are not penalized.

## Failure worlds and historical admission

Cross-context comparisons are underdetermined if relative reward offsets are absent: changing only the additive reward constant in context x1 leaves its pi fixed but changes a preference between x1 and x2. `dpo-dev-003` therefore expects UNKNOWN, not cancellation across contexts. A q-zero action with positive pi is incompatible with finite-reward tilting: `dpo-dev-004` expects INAPPLICABLE for this specified identity. These are different from a valid probability of 1/2. A bridge-unnecessary case uses pi=q, and its pairwise probability must be 1/2. Reversing the compared labels supplies a different-answer counterfactual check, not an independent recipient world; `dpo-dev-006` records `dpo-dev-001-world` as its counterfactual parent.

On 2026-10-11 the audit checked the target v1, its references to AWR/reward-weighted regression, AWR v1, the REPS primary paper, and the Bradley–Terry publication record; queries included “Relative Entropy Policy Search Peters 2010 paper” and “Bradley Terry 1952 paired comparisons.” This is a bounded precursor search, not an exhaustive proof that the precise DPO transformation first became public on May 29. Inverse reinforcement learning, earlier preference-policy objectives, author talks, OpenReview timestamps, and code/blog histories still need equivalent-claim review.

Apply the immutable model and external-input requirements in the [common protocol](README.md). No checkpoint has an admitted release record here. Pythia is a candidate family for a later audit, not a certified artifact. Qwen3 is ineligible for a 2023 historical claim. The target PDF hash is recorded in [source snapshots](source_snapshots.json). DPO v1 displays CC-BY-4.0; AWR's arXiv nonexclusive license and the historical publisher material must not be treated as permission to redistribute full papers. The supplied equations and finite examples are sufficient; no paper text or preference corpus is required by the runner.
