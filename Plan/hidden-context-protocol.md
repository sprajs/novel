# Hidden-context transfer: HC-1

Version 0.1, 17 October 2026. **Selected next experiment; specification only.**
The task generator, training runner and analysis are not implemented or run.
The first deliverable is a checked synthetic behavioural assay, not a discovery
claim or a replication of human neural activity. This protocol is the entry
point for the [research programme](research-plan.md).

## Question and the narrow claim

After feedback reveals a change in a shared rule, can a network immediately
change its answer for a different item that has received no new feedback?
This tests transfer beyond independent item-by-item updating. A one-bit reversal
strategy can solve the primary task, so success does not uniquely identify a
latent-context algorithm, human-like understanding, creativity or a hippocampal
mechanism. Null results are scoped to a trained model, interface and budget.

The human anchor is [Courellis et al., Nature 2024](https://www.nature.com/articles/s41586-024-07799-x),
which studies inference following unannounced context changes. HC-1 preserves
the informative distinction between feedback on one item and transfer to other
items. It uses synthetic symbols and binary correctness feedback, omits the
human experiment's high/low reward factor and clinical recording conditions,
and uses scripted demonstrations so all models see identical evidence. Human
accuracy percentages and neural time scales are not quantitative targets.
The source's inference-present grouping is itself defined by inference accuracy;
we will not reuse such grouping as independent evidence of an accuracy difference.

## A. Primary task: a shared rule can reverse

An episode contains four distinct item identities chosen from a vocabulary of
16 familiar symbols. Let x identify an item, b(x) be its binary reference action,
and c be the hidden context (0 or 1). The correct action is

\[
y(x,c)=b(x)\mathbin{\oplus}c.
\]

XOR, written \(\oplus\), leaves b unchanged when c=0 and reverses it when c=1.
Exactly two of the four reference actions are 0. Neither b nor c is supplied to
the network. Context 0 is anchored to the episode's first demonstrated map;
context labels are never assigned afresh by an arbitrary probe convention.

### Visible episode, fixed before model responses

1. **Familiarisation:** three blocks with contexts 0, 1, 0. Each block contains
   two independently shuffled passes over all four items: 24 demonstration
   events in total. Each event displays `(item, demonstrated_action, reward)`.
   Demonstrated actions are balanced across the two passes for each item (one
   of each action, order random); reward is 1 exactly when the action is correct.
   This supplies every item's mapping in both contexts. Block/context names,
   latent values, generator seeds and boundary markers are hidden. Event count
   and order are observed, as in any sequential task, and are controlled below.
2. **Diagnostic event:** choose a cue item q uniformly. In the change condition
   c becomes 1; in its paired stay condition c remains 0. Display the same
   scripted action b(q). Reward is therefore 0 for change and 1 for stay.
   This is information supplied to every model, not an error selected because
   a particular model happened to make it. The scripted action is not scored
   as that model's own choice.
3. **Transfer query:** choose r uniformly among the three items other than q.
   Display r with a query marker and ask for its action distribution. No target
   answer, reward, rationale, second switch or other feedback precedes this
   response. One transfer query is the primary observation per episode variant.
4. End the episode and reset all transient state. Additional queries, retention
   tests and explanations belong to separate diagnostic runs; they cannot
   influence this primary observation.

An invented example: the last familiar map sends triangle left and circle right.
A demonstrated left response to triangle receives negative feedback. Under the
shared-switch-only task, circle now requires left. Repeating circle-right is
consistent with an item-local update, but so are other failures; inspect controls
before attributing a mechanism.

Each matched episode group has the same familiarisation, cue, query and symbols
in its change/stay variants. Only the diagnostic reward and evaluator's target
differ. Keep those variants in one split and pair them in analysis. Change/stay
are balanced. Random guessing has expected accuracy 0.5; an always-reverse rule
without reading feedback succeeds only on the change half.

### Controls and identifiable conclusions

| Condition or reference | Purpose and interpretation |
| --- | --- |
| Per-item last-correct-action learner | Updates the cue only. Tests the value of cross-item transfer. |
| Feedback-gated one-bit reversal policy | Reverses all mappings after a diagnostic contradiction. Can solve A perfectly; its success limits the mechanistic claim. |
| Exact latent-context observer | Uses the stated generative task and visible history. Reference for available information, not a learned or compute-matched competitor. |
| No diagnostic feedback | Identical prefix with missing reward; balanced change/stay is unknowable, expected accuracy 0.5. Tests target leakage and position shortcuts. |
| Cue-only query, on separate copies | Checks local use of feedback; not evidence of cross-item inference. |
| No-change trials; separate immediate mapping recall | Stay accuracy checks the trained interface and detects indiscriminate reversal. Immediate recall also changes query position and is a robustness control. |
| Label/action counterbalancing | Permutes item identities and action coding, including which output coordinate means left. |
| Variable familiarisation length | Separately reported robustness set with 1 or 3 passes per block, rather than the primary 2; tests event-position shortcuts. |

Ordinary mapping recall uses a separate copy of the same familiarisation history,
followed immediately by one uniformly chosen item query, without a diagnostic
event or context change. Its target is the last demonstrated map. Use one such
copy per evaluation split group, identical across models; never feed its response
back into the transfer episode. In the odd-pass robustness sets, each item's
demonstrated actions are independently uniform rather than exactly balanced;
binary correctness still determines the correct action. Report this exposure
difference alongside the length manipulation. Immediate recall moves the query
one event earlier than in training; especially with learned positions, its failure
can reflect this interface shift rather than absent mapping memory. Do not use
it alone as the competence gate.

Do not filter evaluation episodes by the model's preceding correctness,
confidence, expressed surprise or success. Familiarisation competence is reported
separately. The fixed primary endpoint includes every valid generated episode;
invalid model responses count as failures. Infrastructure failures are reported
as missing runs, never silently converted to incorrect answers or omitted seeds.

## B. Ambiguity task: global change or local exception?

This is a separately trained/evaluated extension after A works. It fixes a flaw
in the tempting control “reverse for a global change but not for an exception”:
the two causes can produce the same first observation.

Construct matched pairs explicitly. Choose q first, then choose G (global
reversal) or L (a persistent exception affecting q alone) with probability 1/2.
In both, the diagnostic scripted old action on q receives reward 0. Everything
visible up to the first other-item query is byte-identical. On r≠q the correct
action reverses under G and stays under L. Therefore the conditional probability
of either action is 1/2 at this point. It is not possible to distinguish the
causes from the supplied evidence. This balance follows from this particular
generator; choosing an exception item independently would change the posterior.

Record the first predictive distribution, then supply a diagnostic demonstration
on a second distinct item s, using its old action. Its reward distinguishes G
from L. Query the remaining fourth item t, without its new feedback. Compare
calibration before the distinguishing evidence and transfer accuracy after it.
No event-type flag, output filename, ordering convention or condition-specific
prompt may reveal G/L. Pair twins across all data partitions. A phase-B ideal
observer updates from the actual generator probabilities, not an assumed 50/50
prior applied to a different dataset.

Primary A models tested on B without retraining are distribution-shift tests.
Models trained on B form a separate study condition. B uses equal-weight cross-entropy losses at BOTH query positions, with paired G/L examples supplying opposite labels at the first identical prefix. The second query uses the distinguishing evidence; loss and reporting remain separate by query position. Neither comparison may be
presented as an unexplained change in the same model's innate ability.

## Models, exposure and state

### Controlled neural-network lane

Proposed development recipes, not existing supported adapters:

- One-layer gated recurrent unit (GRU) with hidden size 64; a recurrent network carries a state between
  events. A linear input projection and two-action output head surround it.
- Two-layer causal transformer, width 64, four attention heads and feed-forward
  width 128, with learned positions for up to 64 events and a two-action head.
- Both receive the same one-hot event fields: 16 item coordinates, two action
  coordinates, two reward coordinates, and demonstration/query markers. Missing
  action/reward coordinates are zero, not a coded target. Event projection has
  width 64. No explicit context, base map or switch indicator enters either model.

Use CPU FP32 first, the repository's pinned environment, no dropout, cross-entropy
on the training episode's final query, AdamW with learning rate 0.0003, betas
(0.9, 0.999), epsilon 1e-8, weight decay 0.01, gradient norm cap 1, batch 32.
Train on one fixed pre-generated 20,000-variant A dataset, shuffled once per seed,
one pass (625 updates). A predeclared 100,000-variant recipe (3,125 updates) is the
only initial development expansion; it is a nested extension of the first set.
Fix parameter initialisation and data-order RNGs separately. Match experience
across architectures, record parameters/FLOPs/time, and do not claim equal compute.
Actual architecture/optimizer implementation must be pinned and tested before use.

Evaluate with weights frozen, gradients off and identical full histories.
Reset GRU state and transformer context between episodes; retain state within
one episode. There is no online weight learning, external memory, tool call,
chain-of-thought budget, retry or best-of-many selection in A's primary condition.
Learning across training episodes and adapting state during evaluation are
different processes and receive separate fields in the run manifest.

### Language-model transfer lane

Add only after the synthetic lane's generator and measurement checks pass. Use
a separately pinned, numerically qualified local model and text renderer, with
all demonstrations preserved and answer fields clearly separated. Compare
experience-only framing with an explicitly explained inverse-rule condition;
do not pool them. A fixed pretrained model may already know the general strategy.
Fresh labels do not prove a novel task or training non-exposure.

Specify label tokenisation, full-vocabulary versus two-label probability
normalisation, and invalid output handling before execution. A forced two-label
choice is a declared restricted policy, not unconstrained generation. Existing
Qwen mechanics and failed FP16 cache/cross-backend gates do not qualify this
experiment. No new model download or paid run is authorised by this specification.

## Data splits and records

A split group is the unordered four-symbol set plus its reference-map assignment,
with action-complement variants grouped together. There are C(16,4) × 3 = 5,460 such groups; only three abstract inverse-map pairs exist for four balanced binary items. A paired episode instance is a sampled history/cue/query within a split group; its two serialized variants are change and stay. The 20,000 training variants comprise 10,000 paired instances sampled with replacement from training split groups; the larger recipe extends these. Repeated histories do not create new split groups. Assign whole groups to fixed
training/development/confirmation partitions (70/15/15), using a committed
generator version and seed before training. All 16 symbols must occur during
training. Confirmation tests new combinations and mappings of familiar symbols,
not wholly untrained embeddings. Report task-rule exposure explicitly: the
inverse-rule family is shared across splits. New rule families are a later test.

Development uses seeds 0–4 and 200 held-out episode groups. Select the smallest
recipe achieving at least 95% stay-condition accuracy on development
for all five seeds; if neither does, record a competence floor and revise only
with a new protocol version. This gate is about operating the task, not primary
transfer success. Report transfer even when the competence gate fails, labeled
development; it cannot diagnose a missing general reasoning ability.

Before confirmation, freeze the selected recipe, source/lock/data hashes, group
inventory and analysis. Use ten new initialisation seeds 10–19 and 600 new
confirmation split groups, with one paired instance per group and approximately
balanced map, cue and response conditions (report achieved counts). The 70/15/15
partition has 3,822/819/819 groups, so this allocation fits without reusing a group. Generate
both change/stay variants for each group. Do not expand samples after inspecting
confirmation outcomes. These are proposed fixed allocations, not an achieved
power calculation. A timing and simulation study on development must establish
feasibility and interval precision; any revision precedes confirmation access.

Keep three distinct records:

| Record | Required contents |
| --- | --- |
| Visible episode | ordered observed fields and query markers only; schema/generator versions and opaque episode IDs stay in the record envelope, never in model input |
| Evaluator sidecar | group/split, reference map, contexts, G/L cause where relevant, targets, admissible information, counterfactual partner IDs; never supplied to the model |
| Run/result | model/checkpoint/lock/code/data hashes, seed roles, exact input and state-reset policy, raw outputs and probabilities, validity flags, stop reason, costs, prediction timestamps and optional capture identity |

Split metadata can accompany files for auditing but cannot enter model features.
Confirmation packet generation/access has a receipt. Published examples stay
development examples. Do not commit private human recordings or distribute
source-paper figures. Synthetic release licensing is an owner decision; this
plan does not choose a repository-wide license.

## Outcomes and analysis

For model seed s and split group g, score the first other-item query separately
for change and stay. The primary endpoint is balanced accuracy, the equally
weighted average of change and stay accuracy, compared with chance (0.5). Report
both components, ordinary recall and the one-bit policy alongside it. The
change-minus-per-item contrast is descriptive: that baseline has zero change
accuracy, so even guessing improves it. For an operational claim of reliable
transfer, require the lower 95% interval for balanced accuracy to exceed 0.5
and mean change and stay accuracy each to be at least 0.95; publish all
outcomes when these design guardrails fail. These thresholds are not evidence
for a unique algorithm or human equivalence.
Prediction ties use the frozen action-0 tie rule; raw probabilities are retained.

Average within each seed, then equally across seeds. Produce seed-level plots,
paired per-group contrasts and 95% intervals using a crossed bootstrap: resample
training seeds and whole episode groups independently, preserving both condition
twins and paired model comparisons (10,000 resamples, fixed analysis seed).
For a fixed checkpoint, report an additional group-only interval explicitly
conditional on that checkpoint. Thousands of trials are not thousands of trained
networks or human participants. All intervals remain conditional on the chosen
training dataset and task family. Two architectures are separate primary reports;
architecture superiority is exploratory, not a multiplicity-free confirmatory claim.

For B, score the probability of action 1 with mean squared error
\(N^{-1}\sum_i(p_i-y_i)^2\) (Brier score). Identical ambiguous prefixes should
receive identical distributions, and the correct conditional prediction is 0.5.
Report pre-evidence calibration and post-evidence accuracy separately. A confident
guess that happens to match one hidden branch is not successful identification.
No p-value or threshold certifies a particular internal algorithm. A places
the possible change at a known event position after a fixed context sequence:
it tests evidence-conditioned transfer, not detection of arbitrary change times.
The variable-length control does not by itself establish change-point detection.

## Representation analysis, then causal tests

Only after robust behaviour: fix a capture boundary immediately after diagnostic
feedback and before the transfer query. Decoding the answer after it is emitted
does not explain inference. Train a linear context decoder on development runs,
hold out item/map groups WITHIN each trained checkpoint, and compare with an
input-history decoder, shuffled labels and untrained-network features. Fit a
separate probe for each checkpoint and aggregate scores across training seeds;
independent networks have unaligned hidden coordinates. Cross-network decoding
would require a separately justified representation alignment. Context is anchored to
the first map; label permutations must follow this anchor across episodes.

In A, context is recoverable from the diagnostic reward itself. Successful
decoding could therefore reflect remembered feedback rather than an abstract
context. Balance action/reward histories, vary earlier context and cue identity,
and compare multiple histories leading to the same inferred rule in a separately
specified diagnostic set. Predeclare probe layer/site and regularisation on
development. Report cross-condition generalisation, not just a random-trial split.

Later intervention protocols must specify selective disruption, unrelated-task
controls, activation-matched random directions/sites, no-op parity and restoration
on new data. A reset tests dependence on state but is not a selective context
lesion. A rescue can inject answer information; use donors from other items/maps
and preserve the information available at the intervention time. These tasks do
not require historical scientific corpus admission, but transferring a claim to
scientific discovery still requires the separate [causal gates](causal-review.md).

## Implementation order and decision gates

1. Implement generator, evaluator sidecars and reference policies. Hand-audit
   counterfactual twins; test label balance, split overlap, no-feedback chance,
   ambiguity-prefix equality and post-evidence identifiability. Reference policies
   must achieve analytically expected scores before neural runs.
2. Implement both model adapters and event rendering. Verify future-target
   invariance, reset isolation, deterministic evaluation on the chosen backend,
   unchanged outputs under read-only capture and exact accounting of all queries.
3. Run development within the frozen cap, inspect competence, timing and precision.
   Publish unsuccessful recipes too. Stop and version changes for interface
   failures, split leakage, impossible targets or numerical instability.
4. Freeze confirmation and run it once. Report all seeds and uncertainty. Then
   decide whether B or a more expressive rule family would distinguish surviving
   behavioural explanations; a perfect one-bit baseline is an informative limit.
5. Open representation/intervention work only with a separate frozen hypothesis.
   Replay, retention and active experiment selection follow their own protocols.

## Reading and source boundary

- [Courellis et al. 2024](https://www.nature.com/articles/s41586-024-07799-x): task adaptation; full-text access and inspected sections in the reading-room audit.
- [Johnston and Fusi 2023](https://www.nature.com/articles/s41467-023-36583-0): computational counterpoint and held-out abstraction measurement; not an HC-1 result.
- [Liu et al. 2019](https://discovery.ucl.ac.uk/10078375/1/1-s2.0-S0092867419306403-main.pdf): subsequent rule-guided sequence study; behavioural reconstruction and spontaneous replay are distinct endpoints.

The [reading room](https://novel-reading-room.sprajs.chatgpt.site/#/review/transfer)
explains the scientific argument and links to optional concept notes. All numeric
allocations here are design choices. No behavioural, neural or scientific result
is established by writing or validating this document.
