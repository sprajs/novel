# Novel: a research programme for machine discovery

Novel studies how a neural network turns previous experience into a useful new
solution, how that ability persists and transfers, and which mechanisms can
improve it. The next experiment is **hidden-context transfer**: after evidence
changes a shared rule, does the network update its answer for an item that has
received no new feedback? The [HC-1 protocol](hidden-context-protocol.md) defines
the task, controls, proposed models, data, analysis and implementation gates.

**Status: research direction and protocol selected; no HC-1 implementation,
training run, behavioural result or scientific discovery is reported.** Existing
inference software provides bounded engineering capabilities, not qualification
of the new task or its proposed architectures.

## What we want to understand

Transforming an old idea can produce something new. The useful question is which
transformation occurred: retrieving an answer, combining familiar parts,
transferring a relation, changing the problem representation, or selecting an
experiment that revises a belief. These operations need distinct tasks and
measurements. Novel will study them from behaviour to internal representations,
then selective intervention and transfer to scientific problems.

Neuroscience supplies experimental designs and competing explanations. Matching
a behaviour is a computational task adaptation; it does not establish matching
brain circuitry. A causal effect in a model is a model result. Novel will not
assume that an LLM lacks an ability, or that an engineered memory/agent loop is
part of its base model. Exposure, execution and available information define
each comparison.

## Research tracks and their order of evidence

| Track | Question and first deliverable | Gate for the next claim |
| --- | --- | --- |
| Hidden context — active | HC-1: transfer after one informative observation, compared with item-local and one-bit strategies | Correct generator/references, competent fixed models, held-out task groups and independent training seeds |
| Reorganisation — next | Adapt rule-guided sequence construction using new combinations of familiar items | Separate reconstructing an order from measuring spontaneous internal replay; specify every extra update and its cost |
| Persistence and experiment choice — later | Does learning survive context reset, transfer to new tasks and guide useful evidence collection? | Distinguish recurrent/context state, external memory and weight changes; compare equal information and computation |
| Mechanistic explanation — gated | Identify representations associated with successful transfer, then disrupt and restore selectively | Frozen probe/intervention recipes, new data, alternatives, no-op/capture parity and information-matched controls |
| Scientific transfer — later | Test whether an established operation improves independently validated scientific contributions | Historical admission or prospective prior-art review, semantic validity, expert judgment and domain-specific evidence |

This is an order for research claims, not a required reading sequence. The
[reading room](https://novel-reading-room.sprajs.chatgpt.site/#/review/transfer)
links the concepts at the point they become useful.

## First experiment and interpretation

HC-1 uses four items and two opposite response rules. After demonstrations of
both rules, feedback on one item indicates a global switch or continued use of
the current rule. The first response for another item measures immediate
transfer. A simple reversal policy can pass, so the primary result can establish
cross-item updating without uniquely identifying a hidden-state algorithm.

The follow-up ambiguity task makes global changes and local exceptions initially
indistinguishable, then supplies a second observation that separates them. It
tests calibrated prediction and evidence-sensitive updating. Success cannot be
defined as guessing a hidden cause before the evidence makes it knowable.

Start with small task-trained recurrent and transformer networks under controlled
exposure. An existing language model is a separate transfer lane: unknown
pretraining exposure, text interfaces and different computation prevent direct
architectural conclusions from raw score differences. The detailed protocol
sets development recipes; confirmation requires a frozen, implemented and
numerically checked runner. No paid job or large-model acquisition is included.

## Deliverables and decision points

1. **Measurement packet:** task generator, visible/evaluator separation, reference
   policies, counterfactual twins and analytical checks. Impossible distinctions
   and leaked targets stop the study before model evaluation.
2. **Development report:** exact training data, seeds, recipes, ordinary competence,
   transfer, timing and uncertainty simulation. Failures and recipe changes remain
   visible; confidence-based cherry-picking of episodes is prohibited.
3. **Frozen behavioural report:** new initialization seeds and held-out groups,
   paired conditions and separate uncertainty across models and episodes. Report
   what a trivial strategy already explains before escalating the claim.
4. **Mechanistic protocol:** only after behaviour is reliable, nominate a specific
   representation and a discriminating intervention. Probe accuracy alone does
   not show that the network uses that information.
5. **Transfer report:** evaluate new rule structures, retention, replay or active
   evidence selection under their own protocols, then decide which operation
   merits testing on scientific tasks.

## Scientific novelty remains a separate endpoint

HC-1's held-out arrangements are new to the documented task training, not new
scientific contributions. The [historical reconstruction plan](historical-reconstruction.md),
[corpus protocol](corpus-protocol.md), [semantic measurement protocol](measurement-protocol.md)
and [scientific causal gates](causal-review.md) remain later-track specifications.
No historical idea has been admitted. Public worked examples remain development
material; source chronology, human adjudication and numerical qualification cannot
be replaced by synthetic task accuracy.

The existing [validation limits](../docs/validation.md) and
[RTX 2080 Ti measurements](../docs/validation/local-2080ti.md) retain their scope.
GRU/training support and the HC-1 evaluator must be implemented and validated
separately from the Qwen inference adapter. A passing toy-task test, a passing
engineering check and a scientific result remain different facts.

## Literature and open scientific choices

The [reading selection](reading-list.md) prioritises human context inference,
computational abstraction and rule-guided reorganisation. Older experiments are
useful when their designs discriminate explanations; recent research supplies
extensions and counterevidence. No unique literature gap is established by this
plan. Before a paper claim, search directly for prior computational adaptations
of the same task and reconcile available task code/materials.

Open choices after development include which richer rule family defeats a
one-bit strategy, what evidence budget is sufficient for ambiguous cases, and
whether a proposed representation remains useful across training histories.
The next [working session](first-day-plan.md) turns the specification into a
reviewable measurement packet before any neural result is claimed.
