# First day plan for the frozen language model study

Prepared 11 October 2026

Start with a brief review of the bridge-transfer question, then move into local setup and a small inference/capture smoke test if you choose to proceed. The recommended session combines practical progress with enough specification to make the first run interpretable. Keep the fully offline alternative below if the machine remains unavailable.

## Recommended balanced morning

| Time budget | Action | Concrete output |
| --- | --- | --- |
| 20 minutes | Review the claim and hand-check one offset case, one different-answer case, and one UNKNOWN case | A provisional assay and primary outcome |
| 20 minutes | After choosing to proceed, inventory actual hardware, driver, available memory, disk, and toolchain | A compatibility record and setup gate |
| 30 minutes | Create a new isolated local project/repository and reference environment; select a compatible stack | A clean project and provisional dependency record |
| 20 minutes plus transfer time | Select an immutable model/tokenizer snapshot and acquire it only after the proceed decision | Exact revisions, template, license, and file hashes |
| 40 minutes | Run tiny seeded inference, selected residual capture, and no-op checks | Tokens, finite tensor shapes, timing/memory, and check results |
| 20 minutes | Read patching interpretation and skim Function Vectors extraction | Notes linking the smoke test to the research question |
| 15 minutes | Record what passed, what failed, and the next bounded task | A reproducible setup record and next action |

Allow roughly three hours of active work; downloads and compatibility troubleshooting can take longer. Stop at a documented checkpoint if they consume the session. A successful day can end with working inference and capture; full benchmark construction and gradients can wait.

## Future user approved setup path

**FUTURE USER-APPROVED ACTIONS ONLY.** The setup rows are a plan for execution after the researcher chooses to proceed. No setup, installation, repository creation, model download, or inference was performed while preparing this document. Commands and package versions remain provisional until the actual driver and immutable revisions are known. GPU rental is a separate later decision.

**Gate 1 — inventory before installation.** Confirm the RTX 2080 Ti and usable VRAM, NVIDIA driver, host RAM, free disk, and Python/build compatibility. Choose a driver-compatible PyTorch/Transformers reference environment. Create a new local repository outside unrelated repositories; use a separate environment for any later optimized backend. Record a tested dependency lock after the smoke test passes.

**Gate 2 — select before download.** Provisionally choose Qwen3-1.7B, or 0.6B if mechanics or memory requires it. Record an immutable checkpoint and tokenizer revision, model configuration, license, chat-template text/hash, and thinking-mode settings. Acquire that snapshot only after the proceed decision. Use explicit FP16 on Turing; do not substitute BF16 or quantized weights silently.

**Gate 3 — inference before intervention.** Use batch one, a short prompt, and a small generated-token cap. In thinking mode, retain appropriate seeded sampling rather than greedy decoding; an unfinished answer at this cap is not a reasoning failure. Save rendered prompt/token IDs, generation settings, raw output, wall time, and peak memory. First repeat clean inference; then capture one selected residual site without changing it. Check shape, finiteness, and unchanged output/logits within a calibrated tolerance. Add an identity/zero-strength hook and confirm that it consumes no sampling randomness. Cache/full-prefix parity and prefix invariance are required before causal experiments, not prerequisites for the first token to run.

Keep gradients, sweeps, and large trace capture out of this smoke test. If memory fails, shorten the sequence or use 0.6B and record the change. A separate llama.cpp CUDA or conditional vLLM benchmark comes after the reference path works; it is optional first-day work, not a setup dependency.

Core reading: [How to use and interpret activation patching](https://arxiv.org/abs/2404.15255), sections 2–4, then [Function Vectors](https://arxiv.org/abs/2310.15213), extraction and transfer. Use the short block to frame the mechanics; finish the readings later.

## Hand checked starting cases

Assume each instrument adds an unknown fixed offset to every reading it makes. Instrument 1 reads A = 17 and B = 11; instrument 2 reads B = 25 and C = 22. The true difference A − C is 9. The bridge is: “Compare readings made with the same instrument before combining comparisons.”

A different-answer target is instrument 3 reading D = 9 and E = 14, and instrument 4 reading E = 6 and F = 2. The answer D − F is −1. A second target, G = 12 and H = 8 on one instrument, H = 13 and I = 20 on another, gives G − I = −3. These are examples for specification, not experimental results.

Include a disconnected observation graph requiring UNKNOWN, inconsistent equations requiring INCONSISTENT, per-reading offsets for which the proposed cancellation is invalid, and a simple case needing no bridge. Specify exact linear equations and ask whether the target difference is constant across all consistent worlds. For UNKNOWN, construct two worlds satisfying the observations but giving different target values. Do not accept one arbitrary solver output as proof of identifiability.

For a second mechanism, use four rooms and a one-bit badge with explicit door requirements and toggles. A solution may revisit the same room with a new badge value. The bridge is to search over (room, badge), not room alone. A graph over at most eight states admits an exact shortest-path check. Hold out graph topology, with ordinary maps and unreachable goals as controls.

## Decisions before the causal pilot

- Choose the first assay and whether both mechanisms are needed for the pilot. Arithmetic at ceiling is a calibration result, not a reason to manufacture errors.
- Choose a worthwhile improvement, provisionally 5 percentage points, and whether the first small study instead targets a larger 10-point effect. The initial 160-world mixture is not powered automatically for either decision.
- Choose the time budget. The report proposes bounded calibration and a separately frozen confirmation cap; these are limits rather than runtime forecasts.
- Select thinking mode as the primary condition or explicitly choose non-thinking mode. Qwen3 thinking-mode baselines should use seeded sampling, not greedy decoding.
- Decide whether a carefully bounded negative causal result would be a worthwhile first research artifact. Historical reconstruction is a later branch, not the sole success condition.
- Name one eventual scientific problem worth investigating. Do not choose an optimization toy merely because it is easy to score.

## Checks before calling the pilot ready

Can the unguided model in principle deduce the answer from supplied information? Does the bridge avoid the target answer and name an operation rather than add a missing law? Are prerequisite probes administered in fresh contexts? Are donor and recipient answer pools separated prospectively? Are structural siblings confined to one split? Does an independent verifier handle valid alternatives, UNKNOWN, and INCONSISTENT? Will every world be reported rather than filtering targets by observed hint benefit?

The primary outcome is independently verified free-generation success against the unmodified baseline. Irrelevant, random, answer-only, wrong-bridge, and generic task-vector controls address specificity. A single-answer arithmetic assay measures composition, not novel scientific ideas. Keep the distinction in the pilot title.

## Fully offline alternative

If the machine is unavailable or setup is deferred, use the original three-hour specification route: 20 minutes on the claim and falsifier; 40 minutes on the two core readings; 45 minutes authoring six offset worlds and six control worlds; 30 minutes specifying badge-state navigation and structural holdouts; 25 minutes choosing the metric, useful-effect threshold, and budget; and 20 minutes auditing identifiability, donors, and splits. End with a one-page specification and hand-checked item sheet. This is an alternative to the balanced morning, not an additional prerequisite before setup.
