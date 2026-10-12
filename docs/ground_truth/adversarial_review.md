# Independent adversarial review

Reviewed 11 October 2026. Verdict: **the reviewed collection is usable as exposed development material after the corrections recorded below. No historical novelty claim, model capability result, or causal-transfer result is admitted.** No remaining arithmetic defect was found in the checked finite subfamilies. This is a scoped verdict, not certification of every surveyed candidate or every possible input.

## Reviewer identity and scope

This review was performed by a separate AI reviewer task. The parent confirmed the requested launch configuration as `model=gpt-6.1-sol`, `reasoning_effort=xhigh`, `fork_turns=none`. The exact serving build was not independently attested. This is AI review, not human peer review. Independence here means separate reasoning and alternative calculations; the reviewer could see public gold labels and author explanations and was not blinded.

Reviewed the five worked packets, their three fixture collections, `calibration.py`, `research_verifiers.py`, `meanflow_verifier.py`, prompt projections, grounded DPO transfer checks, and the public infrastructure adapter. Also checked the model audit for date/identity overclaims and the decision report for consistency with these artifacts. The broader candidate registry was checked for counts and the speculative-sampling disposition. SSD, DeltaNet, SOAP, and the AlphaEvolve certificate were not independently rederived or executed by this reviewer.

Only this review file was authored by the reviewer. Corrections to worker-owned files were requested from their owners and then inspected. All execution described below was offline mathematical or interface checking; no target-model inference, generated response code, training, or activation intervention was run.

## Findings and adjudication

| ID | Severity | Evidence and consequence | Final status |
| --- | --- | --- | --- |
| R1 | Medium: information boundary | In the initial research projection, adding `premises.blocks[0].expected="SECRET_GOLD=9/7,2"` left the attention oracle unchanged but inserted the secret into the model prompt. An outer premise allowlist did not protect nested block records. | **Resolved.** The renderer now projects each block to scores, values, and masks. Independent reinjection of `expected` and `source_title` leaves the visible record identical. The committed regression also poisons nested metadata. No actual contaminated model run was observed. |
| R2 | Medium: grading fairness | Initial DPO and attention questions requested UNKNOWN/UNDEFINED “with a reason,” while the verifier required undisclosed exact reason strings. A correct UNKNOWN with “The relative block masses are not provided” was rejected. | **Resolved by an explicit contract.** Every required reason code appears in the visible response format. Free explanatory prose is still not graded as a proof; that limitation is now stated. |
| R3 | Medium: integration | All 22 initial research targets were strings, while the shared fixture schema required an object. The collection checker returned 22 target-shape errors despite passing packet tests. | **Resolved.** Targets contain `question` and `response_format`; all three fixture collections pass the common validator. |
| R4 | Low: artifact integrity | The initial standalone calibration loader used ordinary `json.loads` and silently accepted duplicate keys. The common strict reader rejected the identical bytes. | **Resolved.** The calibration loader now rejects duplicates and nonstandard JSON constants itself. The original duplicate-key reproduction fails as required. |
| R5 | Medium: premise adequacy | Values of an average on one trajectory do not identify its separate spatial/time partial derivatives. For the time-field example, adding `lambda*(z-a-b*t-c*t^2)` preserves all observed path values while changing `partial_z` and `partial_t`; the total derivative is unchanged. | **Resolved.** MeanFlow premise A now defines the average along the unique backward ODE solution ending at every nearby endpoint. The square-root domain is explicit. The previously arbitrary extension is excluded without supplying the answer formula. |
| R6 | Medium: claim scope | DoRA derivative fixtures supply the normalized local map. Its forward fixture also says that BA changes the direction argument, supplying most of the placement insight. Raw-token attention fixtures permit ordinary unblocked evaluation. Correct numeric answers cannot distinguish invention or use of the nominated algorithm. | **Retained limitation, explicitly disclosed.** The DoRA packet distinguishes local calculus from forward consequences; the decision report calls the supplied construction execution rather than invention. Attention accepts flattening and disclaims inference of a streaming strategy. A construction-discovery endpoint would require a new question and equivalence rubric. |
| R7 | Medium: historical attribution | The initial registry left the scalar speculative identity as a 2022 priority while the packet had verified the equivalent 2017 maximal-coupling construction. Combining that identity with an unaudited block-systems scope obscured the rejection. | **Resolved.** The registry now rejects the selected scalar claim, records the 2017 antecedent, and separates the possible autoregressive systems contribution as an unaudited alternate scope. |
| R8 | Low: new-packet handoff | The first public adapter handled calibration and the original four-paper collection but could not dispatch a MeanFlow development fixture to its own renderer/oracle. | **Resolved.** MeanFlow is a separate supported collection. All 204 rows across 51 fixtures and four conditions round-trip through the actual pinned sibling interface. |

Other reviewers prompted improvements to seed/evaluation typing, lineage checks, irrelevant controls, and synthetic A/B. The final suite covering those changes passed here; their initial discovery is not attributed to this reviewer.

Final root hardening validates nominal numeric leaves before rendering and restricts the derivative-mode vocabulary. A record or arbitrary explanatory text placed inside weights, vectors, probabilities, or attention values is rejected without consulting the oracle. The final transfer regression covers this boundary.

## Independent mathematical checks

**DPO.** Direct strength substitution gives `(pi_a/q_a)^beta` and `(pi_b/q_b)^beta`; their common reward-scale factor cancels only within one context. In the first fixture these strengths are `4/9` and `9/4`, giving odds `16/81`, probability `16/97`, and loss `log(97/16)`. The separate context offsets remain free, so the cross-context answer is UNKNOWN. These equations agree with [DPO v1 Section 4 and Appendix A.2](https://arxiv.org/html/2305.18290v1). The rational executable subfamily uses positive integer beta; it does not check arbitrary real beta or optimization trajectories.

**Residual sampling.** The accepted symbol mass is `min(p_i,q_i)`. Its missing target mass is `p_i-min(p_i,q_i)` and sums to the rejection probability. Completing that branch restores every marginal, including missing proposal support; for p=q the fallback is unused. An independent branch-mass check covered all 225 pairs of three-symbol distributions with integer counts summing to four. The stale-score fixture independently gives `(3/8,5/8)`, rather than `(1/4,3/4)`. The equivalent acceptance/residual construction is directly present in [Jacob, O'Leary, and Atchadé v1 Section 4.1, Algorithm 4](https://arxiv.org/html/1708.03625v1), after swapping the draft/target notation. This supports rejecting scalar novelty in 2022; the cited Thorisson book was not independently inspected.

**DoRA.** Differentiating the squared norm and then the quotient gives `dw=mu*u+(m/n)*(h-u*(u dot h))`. Its ordinary radial component is mu. The first fixture gives `(29/25,72/25)` with radial component 3. The radial perturbation `(6,8)` gives zero under the ordinary derivative, but `(12,16)` and radial component 20 under denominator-detached autodiff. These are different derivative semantics. [DoRA v1 Section 4.3](https://arxiv.org/html/2402.09353v1) explicitly makes that detachment; the projected gradient already occurs in [Weight Normalization v1](https://arxiv.org/abs/1602.07868v1). The tiny forward example gives columns `(6,8)` and `(0,5)`; it establishes neither parameter savings nor fine-tuning quality.

**Stable attention.** Rescaling both block numerator and denominator to the larger maximum gives denominator `7/4`, numerator `(9/4,7/2)`, and output `(9/7,2)`. Independently, raw weights `(1,2,4)` give numerator `(9,14)` divided by 7. Equal block averaging is wrong. Equal local outputs remain identifiable despite missing relative masses; unequal outputs generally do not. The stable numerator/denominator construction is already explicit in [Rabe and Staats v1 Sections 3–4](https://arxiv.org/html/2112.05682v1). Exact algebra does not imply floating-point merge-tree equality or a recovered IO theorem.

**MeanFlow.** Solving the endpoint ODE independently yields `u=b+c*(r+t)` for the time field and `u=2*sqrt(z)-(t-r)` on the positive square-root branch. All nine fixture consequences agree. In the state-dependent example, the time partial is -1 and the spatial contribution is 2, giving total derivative 1; partial-only recovery would give 8 instead of 4. With moving r, `(1-rho)*u+(t-r)*du/dt=v(t)-rho*v(r)` holds. The local fixed-r identity alone admits the exact counterexample `v=0, u=1/(t-r)`; the continuous/vanishing-displacement boundary is essential for its converse. The packet includes that restriction rather than treating finite residual checks as a universal proof. The corresponding source equations occur in [MeanFlow v1 Section 4.1 and Appendix B.3](https://arxiv.org/html/2505.13447v1).

**Synthetic calibration.** A separately implemented bipartite potential graph was compared with Gaussian elimination on 2,000 seeded rational offset systems, including contradictory equations and anchors; all answers matched and their raw-equation certificates checked. All public calibration labels were also inspected. An alternative equally short badge path is accepted; room revisits with a changed bit remain legal. The public shortest-path and offset tests use independent routes rather than bounded-world sampling as a proof of identification.

## Replayed checks and provenance limits

- `python -m unittest discover -s tests/ground_truth -v`: **87 tests passed** in the final full replay, including the numeric-leaf renderer guard and final MeanFlow cue wording.
- `python tests/ground_truth/artifact_tools.py validate`: all collection/schema/reference checks passed; counts are 20 calibration, 22 four-paper development, and 9 MeanFlow development fixtures.
- `python tests/ground_truth/check_sibling_interface.py`: **204 public condition rows passed** the real TaskInput and JSONL loader at `c5a361363de8bb08aacc5119f1f435a847ad44d3`. This is interface compatibility, not target-model behavior.
- All 10 available temporary PDF snapshots were independently rehashed; SHA-256 and byte counts match the recorded source inventory. MeanFlow used inspected HTML and has no asserted acquired-PDF hash.
- All 42 model-manifest entries marked locally byte-verified were independently rehashed from available temporary metadata/tokenizer/card files and matched. Weights were not acquired or tensor-compared; their LFS identities remain publisher-reported.
- Poisoning evaluator labels and private metadata leaves the checked primary prompts unchanged. The grounded DPO donor is `16/97`, its recipient is `3/4`, and a donor answer fails the recipient oracle. This is same-family development, not structural confirmation.

Pythia's literal April snapshots, later mutable branches, and Qwen's differing April/July templates are distinguished in the audit. A repository timestamp or matching weight identifier is not an independently archived public-release event, complete post-training audit, or contamination certificate. Current documents preserve those gates and admit no clean historical item. The decision report's 20-candidate disposition counts (5 priority, 10 ambiguous, 5 rejected) match the registry.

## Remaining objections

The public artifacts and corrected finite contracts do not close the historical admission gates. Earlier equivalent claims and non-paper disclosures remain incompletely searched; exact checkpoint public availability and complete learned-input lineage require adjudication. Classical calculus, normalization, coupling, and attention identities must remain distinct from later systems/training contributions. The proof oracles check requested finite consequences, not arbitrary universal arguments.

No prerequisite competence, hint benefit, donor-answer copying rate, transfer effect, numerical replay, runtime, or empirical scientific benefit was measured. Confirmation families, answer pools, effect thresholds, variance-based sample size, and custodian sealing remain unmaterialized. Public examples cannot become confirmation by renaming their split. Human/domain review and repository-owner licensing decisions remain open. These are remaining scientific gates, not failures that passing unit tests can resolve.

## Reviewed artifact snapshot

These SHA-256 values identify the reviewed bytes. Later edits require reconciliation with this record; the final collection manifest may additionally include this review and subsequent handoff documents.

The decision-report hash below identifies the [audited snapshot](https://github.com/sprajs/novel/blob/b491c365446644f16147afc7cac62fa316c8b2d9/docs/ground_truth/decision_report.md).
It is a review receipt for that version. The collection report's programme
navigation and framing can evolve; the manifest records the current bytes.

| Artifact | SHA-256 |
| --- | --- |
| `docs/ground_truth/packets/dpo.md` | `f436e0cddd3cdfc6625d4b68643885febfede892f25088ee950ca56b8ed1131f` |
| `docs/ground_truth/packets/speculative-decoding.md` | `90a2a73249eacd7af2f6c3e80bdb744d30f350686b7230e3fb54f8301c58f971` |
| `docs/ground_truth/packets/dora.md` | `5269ad9dbf5386d258d3ea69339a4e104e08af97a54eb4bb110cd9a1bdcf78c6` |
| `docs/ground_truth/packets/flashattention.md` | `61038d0c3e04aba5cd31ba5c8bd8e8e8187bd3473e1e1382a9ba4ffada9aa774` |
| `docs/ground_truth/packets/meanflow.md` | `31d412d28f0249dfee837414c3bbfa31fba0bc8c6f7edc10dfd7ffc9ada0d9e3` |
| `tests/ground_truth/calibration.py` | `c05a8e54d529f2e2377035ffe5a0a4b2b9bf2fa45fa3965eadac050a4deae0da` |
| `tests/ground_truth/research_verifiers.py` | `9404c97fbb175e9c0e2851aa7ff764d4f26bfeb2ad3b389dfc2f13b05ec4b2ed` |
| `tests/ground_truth/test_transfer_contract.py` | `3dec8354709b4c15acc5e719c522309b02c8b973a9057ed3e92ea0f6f7f10153` |
| `tests/ground_truth/meanflow_verifier.py` | `9d225331621745fd90098b133e1cabcf0ee67299a06f04fb2fd17d4a7b7b1047` |
| `tests/ground_truth/infrastructure_adapter.py` | `c08e97dc29040de85522d8c244fa0ddc3a6d664a5c1da0ec9ad5b4add0eeb1bf` |
| `data/ground_truth/calibration_fixtures.json` | `be388aff7755730170cc6929be0cdc763f74c51b489cc0e3e75f3b7e47822fbc` |
| `data/ground_truth/research_fixtures.json` | `5ccfc4142a55286ed9a93c8d99c66813f67fe4e56d1199a9543c054e21b95f56` |
| `data/ground_truth/meanflow_fixtures.json` | `2b35de0726a777245258656ecec5eb738a09135dc70de6cae2538ec06da5ca7e` |
| `data/ground_truth/schema.json` | `b097b14910627bc38d4b3926a0f6003716bad0c784834810669f562e8036e4e1` |
| `data/ground_truth/candidate_registry.json` | `317bcda69d1b121bf4dcea917b8361610f7cc7d5cd6f5a02e3cb5c1b639d758d` |
| `data/ground_truth/model_audit.json` | `74f97eb01210675774c87163a2b1ac6a1c386ee3445da5a4284d7c808e8627f3` |
| `docs/ground_truth/decision_report.md` | `022a769e622f4b9d84a6bcb5a71dc9c11c00d987fe7f5a3ca94e50702a7cc19c` |
