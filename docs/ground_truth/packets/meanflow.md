# MeanFlow: finite-interval velocity and the moving endpoint

Candidate ID: `meanflow`. **Public development composition packet; historical admission pending.** The tested consequence is an exact relation among interval-average velocity, instantaneous velocity and a derivative along a specified flow. This relation is classical calculus. Correctly deriving it is not discovery of a new mathematical identity, recovery of the full MeanFlow training method, or evidence of useful one-step image generation.

## Source, chronology and narrower claim

[Mean Flows for One-step Generative Modeling, v1](https://arxiv.org/abs/2505.13447v1) was submitted on **19 May 2025 at 17:59:42 UTC**. The current arXiv page lists only v1 on 11 October 2026. In [v1 Section 4.1](https://arxiv.org/html/2505.13447v1), Eq. 3 defines an average field; Eq. 6 relates it to instantaneous velocity; Eq. 8 expands the trajectory derivative with tangent `(v,0,1)`. Appendix B.3 discusses recovery of the integral definition. The application uses a parameterized network and a regression target whose gradient is stopped. The authors report one-evaluation image-generation results; those measurements cannot be inferred from this packet's exact arithmetic.

The substantive 2025 research question is the application of an average-velocity field and derivative-based training to generative modeling. The prerequisite calculus predates that application. MIT's [Fall 2006 calculus calendar](https://ocw.mit.edu/courses/18-01-single-variable-calculus-fall-2006/pages/calendar/) lists product/quotient rules, the chain rule, the fundamental theorem and average values; its [Fall 2007 multivariable calendar](https://ocw.mit.edu/courses/18-02-multivariable-calculus-fall-2007/pages/calendar/) lists multivariable differentials and the chain rule. These are dated teaching antecedents, not proposed invention dates for calculus. The operator below is the usual material derivative, also expressible as directional differentiation along a flow; no claim of a novel Lie-derivative identity is made.

The bounded audit inspected v1 abstract/history and relevant HTML sections, these older course records, and the author's code README/license. It did not exhaust earlier talks, slides, workshops, preprint announcements, theses, code, or equivalent generative-model objectives. April 29 immutable Qwen snapshots in the [checkpoint audit](../model_audit.md) precede the known May 19 submission, conditional on exact artifact/public-visibility evidence and unresolved earlier target disclosures. Modern templates must not be substituted. Even a chronologically eligible checkpoint reconstructing this calculus would not establish novelty relative to the older mathematical antecedents.

## Precisely specified information

Let a continuously differentiable scalar velocity field `v(z,s)` define unique local ODE solutions. For **each arbitrary nearby endpoint** z at t, solve backward to r and define

```text
dz(s)/ds = v(z(s),s),  z(t)=z,
u(z,r,t) = [integral from r to t of v(z(s),s) ds] / (t-r),  r<t.
```

This defines an endpoint-dependent field in a neighborhood, rather than an arbitrary extension of values on one observed curve. At `r=t`, require its continuous extension. This distinction is essential: a single trajectory determines the derivative along itself, but does not separately identify its spatial and time partial derivatives without a specified field.

Prerequisite A is the ODE flow definition, the integral displacement relation and average definition above. Prerequisite B is the ordinary product/chain rule, including

```text
df/dt = partial_t f + v * partial_z f + rho * partial_r f,
rho = dr/dt.
```

Supply A/B and all parameters identically in both primary arms. Source names, dates, candidate IDs, expected values and worked derivations are evaluator metadata. The [fixture renderer](../../../tests/ground_truth/meanflow_verifier.py) projects only approved premise/target fields to the six-field prompt contract and uses the common neutral capture cue. No off-trajectory formula for u is supplied: it follows from the explicitly supplied global field and endpoint solution.

## Minimal bridge and alternative route

Minimal bridge: **“Differentiate the interval-scaled average along the trajectory; keep the lower time fixed when deriving the fixed-lower relation.”** It names an operation without an instance answer or final relation. An alternative valid bridge is: **“Replace the velocity integral by endpoint displacement, then apply the quotient rule along the trajectory.”** The verifier accepts their equivalent consequences; it does not require a nominated verbal explanation.

Fresh-context prerequisites should separately probe a polynomial derivative/integral, the derivative of a product, differentiation of a composite field at a moving endpoint, and the limit of an average over a shrinking interval. The deliberate wrong bridge holds z fixed and drops the spatial chain-rule term. This is harmless for a spatially independent field, so the state-dependent control is required. Irrelevant text states a fact about paragraphs, sentences and words; exact token-length matching remains a separate calibration. Answer-only and full-explanation donors, if constructed by the evaluator later, are explicit leakage diagnostics; none is a minimal-bridge donor.

## Original derivation and the boundary

Fix r and follow a trajectory as t changes. The integral equals `z(t)-z(r)`, so

```text
(t-r) u(z(t),r,t) = z(t)-z(r).
u + (t-r) D_t u = v(z(t),t).
D_t u = partial_t u + v * partial_z u.
u = v - (t-r) D_t u.
```

The first equality followed by product differentiation proves the local identity. An independent route uses the quotient rule directly on the displacement:

```text
D_t u = [(t-r) v(z(t),t) - (z(t)-z(r))] / (t-r)^2.
```

Multiplication and substitution yield the same relation without assuming a learned network. This is also a direct fundamental-theorem route: integrate the known derivative of z, evaluate the two endpoints, and then differentiate their quotient.

At the diagonal the integral quotient is `0/0`, so never evaluate that raw quotient. Continuity of v gives `u(z,t,t)=v(z,t)`. The derivative in the fixed-r identity remains a derivative with r held fixed; differentiating the diagonal function with r=t moving is a different operation. For a quadratic trajectory, fixed-r `D_t u=c`, while a diagonal path has derivative `2c`.

The local differential identity alone admits spurious fields if diagonal regularity is discarded: add `K/(t-r)` to a correct u. That term cancels between u and `(t-r)D_t u`, while the displacement gains K. Boundedness/continuous extension excludes it. Thus small residuals away from the diagonal do not independently certify the integral average or a valid neural approximation. The verifier checks actual endpoints as well as the identity.

## Worked exact worlds

For `z(s)=a+b*s+c*s^2`, the global field is `v(z,s)=b+2*c*s`. Any endpoint has backward solution `z(s)=z+b*(s-t)+c*(s^2-t^2)`. Consequently

```text
u(z,r,t)=b+c*(r+t),
partial_t u=c, partial_z u=0, D_t u=c  (fixed r).
```

With `a=b=0`, `c=1`, `r=0`, `t=2`, endpoints are 0 and 4. The average is 2; instantaneous velocity is 4; the derivative is 1; the recovered right-hand side is `4-2*1=2`. The fractional case `a=3`, `b=-2`, `c=3/2`, `r=1/3`, `t=5/3` has lower endpoint `5/2`, displacement `4/3`, average 1, endpoint velocity 3 and derivative `3/2`. These distinct answers are public development material.

To distinguish partial from total differentiation, use `v(z,s)=2*sqrt(z)` with the unique positive local solution. The arbitrary-endpoint backward solution is

```text
z(s)=[sqrt(z)+(s-t)]^2,
sqrt(z)+(r-t)>0,
u(z,r,t)=2*sqrt(z)-(t-r).
```

The supplied member is `z(s)=(k+s)^2` with `k+s>0` throughout the interval. At `k=1`, `r=0`, `t=2`, the endpoint is 9. The average is 4, `partial_t u=-1`, `partial_z u=1/3`, and `v=6`. Therefore `D_t u=-1+6/3=1`. Correct recovery gives `6-2*1=4`; partial-only recovery gives 8. A trajectory with `k=-2`, `r=0`, `t=1` violates the stated positive branch and receives INAPPLICABLE, rather than silently using an unrelated extension or sign convention.

For a moving lower limit, the correct relation is instead

```text
(1-rho)u + (t-r)du/dt = v(z(t),t) - rho*v(z(r),r).
```

Take `z(s)=s^2`, local `r=t/2`, and `t=2`. Here r=1, rho=1/2, average=3 and total derivative=3/2. The unmodified fixed-r right-hand side is `4-1*(3/2)=5/2`, unequal to 3. The generalized relation has both sides equal to 3. This case controls whether the model respects a required assumption rather than mechanically emitting the named identity.

## Executable contract and limits

[Nine development fixtures](../../../data/ground_truth/meanflow_fixtures.json) cover ordinary and rational quadratics, diagonal extensions, state-dependent square flows, constant velocity, an invalid branch, and moving r. Family/world IDs and the two canonical template lineages are evaluator metadata. Every fixture is public development, never confirmation. Distinct labels alone do not create independent structural families; new confirmation must follow the common split/custodian protocol.

The exact response contains status plus rational values for average, endpoint velocity, time/state partials, actual total derivative, fixed-r right-hand side, displacement and lower endpoint, plus boolean `identity_holds`. INAPPLICABLE contains exactly status and reason. Equivalent exact fractions and integers are accepted; floats, boolean numeric substitutes, duplicate JSON keys, omitted or extra fields, and inconsistent values fail. The right-hand-side field evaluates the **recovered fixed-r relation using the actual total derivative**, even in the moving-r countercondition; it is not permission to assume rho=0. This grading verifies consequences, not arbitrary proofs or the provenance of a generated explanation.

`solve_fixture(f)`, `verify_response(f,obj)`, `visible_prompt(f)` and `render_prompt(f,condition)` are standalone APIs. The solver ignores stored expected labels. Horner endpoint evaluation is checked against separately integrated polynomial-velocity coefficients; chain-rule derivatives are checked against the factored trajectory route and the generalized Leibniz relation. The tests exercise these routes across 162 rational worlds, plus wrong derivatives, boundaries, malformed responses and nested metadata leakage. No generated code is executed and no model was run.

## Rights and unresolved evidence

The arXiv paper displays CC BY 4.0. The author's [JAX repository](https://github.com/Gsunshine/meanflow) has an [MIT license at observed commit d70cb55d298ee03c53bf6da67bec281082e4e2d9](https://github.com/Gsunshine/meanflow/blob/d70cb55d298ee03c53bf6da67bec281082e4e2d9/LICENSE). That code license does not clear ImageNet, model weights, pretrained components, or another training corpus. None is required or acquired here. This packet and its polynomial fixtures are original; repository-owner licensing remains a separate decision.

Public HTML and license/README text were inspected on 11 October 2026. No paper PDF or training dataset was downloaded for this packet; no source-content hash is asserted. Two initially attempted MIT calendar URLs without `/pages/` failed, then the canonical calendar pages succeeded. An attempted material-derivative PDF endpoint was unavailable and supplies no affirmative evidence. The older calendar records establish that the calculus prerequisites were already taught; a complete equivalent-objective and earliest-disclosure audit remains open. Historical eligibility, prerequisite competence, training convergence, approximation error, distributional validity, image quality and runtime all remain unmeasured.
