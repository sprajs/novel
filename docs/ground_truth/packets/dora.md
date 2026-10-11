# DoRA: low-rank directions, normalization, and gradient semantics

Candidate ID: `dora`. Status: **public development composition packet; historical eligibility unresolved for the composition, rejected for novelty of normalization's projection derivative**. This packet does not claim that an algebraic derivation predicts fine-tuning accuracy.

## Exact scoped claim and prerequisites

For one nonzero weight column v and positive scalar m, define `w=m v/||v||`. For a matrix, apply this definition separately to each column. Prerequisite A: weight normalization separates a column's magnitude from its direction. Prerequisite B: a low-rank adaptation changes a frozen matrix W0 by BA, where B has r columns and A has r rows, so rank(BA) <= r. Supply these definitions in both primary arms. The task asks for a construction that uses BA to change the direction argument while preserving a separately specified magnitude, then asks for a local directional derivative of the resulting *ordinary mathematical function*.

The construction is `W'=normalize_columns(W0+BA) diag(m)` (column convention). Matrix orientation is explicit: many libraries store transposed linear-layer weights. Do not infer that every library implementation uses this column axis. Fixing m does not hold the direction fixed, and rank(BA)<=r does not imply rank(W'-W0)<=r after column normalization and independent scaling.

Fixture `dora-dev-006` exercises the forward low-rank composition. Fixtures `dora-dev-001` through `005` supply the normalized local map and test its calculus consequences; they cannot show that a model constructed the low-rank combination. Their construction-oriented bridge can be redundant. Analyze any bridge lift on these easier diagnostics separately from the forward task.

[DoRA v1](https://arxiv.org/abs/2402.09353v1) was submitted 2024-02-14 at 17:59:34 UTC. Its [Sections 4.1–4.3](https://arxiv.org/html/2402.09353v1) contain the normalized low-rank direction construction, an ordinary derivative, and a detached-normalizer variant. A is already present in [Salimans and Kingma's Weight Normalization v1](https://arxiv.org/abs/1602.07868v1), submitted 2016-02-25 at 10:13:45 UTC. B is the central parameterization in [LoRA v1](https://arxiv.org/abs/2106.09685v1), submitted 2021-06-17 at 17:37:18 UTC. Those older prerequisites are necessary disclosure evidence, not proof that their exact combination was previously unreported.

## Bridges and separate probes

Minimal bridge: **“Put the low-rank change inside the direction argument while keeping the magnitude parameter separate.”** Alternate bridge: **“Normalize the adapted column before applying its desired length.”** The derivative question is a downstream consequence of this construction. If the construction itself is supplied in an easier task, label that task as normalization calculus rather than reconstruction of the combination.

Fresh-context A probes normalize (3,4), distinguish magnitude from direction, and differentiate a scalar square-root norm. B probes multiply small BA matrices, count factor parameters, and check a rank-one determinant. The primary prompt must identify whether it asks for a function derivative or an automatic-differentiation rule with a detached denominator. Otherwise the target is ambiguous.

Wrong bridge: “Normalize W0 first and add BA afterward; the column length stays fixed.” Irrelevant true text: “A square matrix and its transpose have the same determinant.” Answer-only for the first derivative fixture is `{"status":"VALID","dw":["29/25","72/25"],"radial_rate":"3"}`. Full explanation is the derivation below and is not a minimal donor. A pure magnitude update is a bridge-unnecessary case. A zero direction and a detached-normalizer derivative are mandatory controls.

## Construction, derivative, and fully worked examples

A tiny forward construction uses

```text
W0 = [[0,0], [4,5]], B = [[3],[0]], A = [[1,0]], m=(10,5).
W0+BA = [[3,0], [4,5]], with column norms (5,5).
W' = [[6,0], [8,5]], with squared column norms (100,25).
```

BA has rank one. This tiny matrix illustrates the operation; with six factor-plus-magnitude parameters versus four dense entries, it does **not** demonstrate parameter savings. Parameter savings require dimensions and rank satisfying the appropriate count, and training success is an empirical result.

For the local consequence put n=||v|| and u=v/n, perturb v by `t h` and m by `t mu`, and differentiate at t=0. Differentiating `n(t)^2=v(t)^T v(t)` gives `n'=v^T h/n=u^T h`. Applying the product/quotient rules yields

```text
dw/dt = mu u + (m/n) [h-u(u^T h)]
u^T (dw/dt) = mu.
```

Thus a direction perturbation parallel to v produces zero ordinary first-order change when m is fixed. For v=(3,4), m=10, h=(1,2), mu=3: n=5, u=(3/5,4/5), u^T h=11/5, and `h-u(u^T h)=(-8/25,6/25)`. Multiply by 2 and add `(9/5,12/5)` to obtain `(29/25,72/25)`; its dot product with u is exactly 3. This is `dora-dev-001`.

An alternative valid proof decomposes h into radial and orthogonal components before expanding the normalized vector. Another differentiates the invariants `||w||=m` and positive direction alignment, solving the resulting linear constraints. The tests use a first-order quotient expansion from the squared-norm constraint as a check independent of the projected-vector implementation. They cover varying scales, radial/tangent directions, and nonzero magnitude changes. Rational fixtures use vectors with rational Euclidean norms; the exact Python verifier explicitly rejects unsupported irrational norms rather than approximate them. The mathematical identity itself has no such restriction.

The gradient for a loss with column gradient g is `grad_v L=(m/n)(I-uu^T)g` and `grad_m L=u^T g`; these follow by taking the adjoint of the differential. This projection formula is weight-normalization algebra from before DoRA, not a 2024 discovery.

## The important failing variant

DoRA v1 Section 4.3 explicitly treats the normalization denominator as constant in backpropagation in its memory-saving variant. That surrogate gradient is `(m/n)g`; it lacks the projection term. The forward function still renormalizes at every evaluation. Distinguish **the actual function derivative**, **the automatic-differentiation rule**, and **the optimizer's finite update**.

`dora-dev-002` uses v=(3,4), m=10, h=(6,8), mu=0. The true derivative is `(0,0)`. `dora-dev-003` uses the identical inputs but explicitly asks for the detached-denominator autodiff rule: `(12,16)`, with radial rate 20. Treating them as equivalent is a substantive error. The detached case is bridge-inapplicable to a claim that its autodiff gradient is tangent. `dora-dev-004` uses v=(0,0), where normalization is undefined; an epsilon regularization would define a different function and must be supplied as an additional premise. The verifier does not silently add one.

## Historical and empirical limits

The 2026-10-11 audit checked first-version PDFs and dates for DoRA, LoRA and Weight Normalization, including DoRA's detachment passage and the older derivative. Queries included “Weight Normalization 2016”, “DoRA 2402.09353”, and the target's related-work references. Earlier normalized low-rank adaptations, author announcements/code, OpenReview versions, and equivalent geometric parameterizations still need a complete prior-art audit. Identifying these A/B sources with hindsight is assistance; deriving a familiar Jacobian is not evidence that the model invented DoRA.

Fine-tuning quality, correlation patterns between magnitude/direction updates, memory reduction, and negligible inference overhead require models, data, kernels, and measurement. The algebra proves none of those empirical claims. Apply the [common immutable checkpoint protocol](README.md), including all post-training, with the earliest equivalent disclosure of the claimed combination. No eligible checkpoint is fixed; Qwen3 cannot be the historical witness for a February 2024 result. [Source snapshots](source_snapshots.json) record retrieved v1 PDF hashes. DoRA v1 is marked CC-BY-NC-SA-4.0; LoRA and Weight Normalization's arXiv nonexclusive licenses do not grant general paper redistribution. No training examples, weights, figures, or upstream implementation are redistributed here.
