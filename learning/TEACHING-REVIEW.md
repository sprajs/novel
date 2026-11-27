# Teaching review record

## Independent decoder tests — 27 November 2026

The parent reviewed the new concept note, source card and brain-review passage
against targeted primary methods/results, and checked the link in the transfer
review in context. This is an editorial and technical assessment, not a human
novice study or an independent replication.

The note starts from a scientific question: what a fitted decoder can read on
new cases. It defines decoder, label, preprocessing, PCA, autocorrelation,
episode/group, fold, tuning and checkpoint where used. The worked mean
calculation explains the sum and each numerical step; it explicitly avoids
claiming that this arithmetic alone proves an accuracy bias. Fitted values and
selected settings are distinguished. Fitting inside folds and choosing an
appropriate held-out unit address different problems.

The paper's possibility of pessimistic as well as optimistic error is retained.
The note does not imply that any specific brain-alignment study is invalid or
that every preprocessing step requires fitting. An independently specified
transformation can be applied to test inputs; a data-dependent transformation
must respect the intended evaluation boundary. The examples do not silently
change HC-1's split, confirmation procedure or gated scientific status. The
reward-history shortcut, within-checkpoint coordinates and need for a separate
causal hypothesis remain explicit. The page is reachable from the argument and
from the concept index; no linear syllabus or assessment controls are added.

Visual/runtime checks and publication status are reported in the separate
publication receipt after verification.

## Beginner readability review — 12 October 2026

The parent agent read all 13 chapters of the completed second teaching pass at
`636ecc423d65b527add3ecb10c8b0f55470df707`, including their examples, diagrams
and connections. The question was whether the reader could understand Novel's
current experiment without opening the papers first. This was an editorial and
technical read-through, not a study with first-time human readers.

The chapters now provide a usable standalone explanation of the experiment.
They introduce probability before sequence scoring, numerical arrays before
attention, and ordinary sampling before confidence bounds. Worked examples
show the intermediate steps. The papers serve as optional sources for closer
inspection; they do not carry a missing step in the main explanation. Later
intervention chapters remain connected to the experiment's actual evidence
requirements rather than presenting steering as an established discovery tool.

| Chapters read | What makes the explanation followable |
| --- | --- |
| Tokens; transformer; inference | Concrete probabilities and arithmetic lead into token scores, vector operations, attention, residual paths and cached history. Training and running a fixed model are distinguished. |
| History; meaning; likelihood | An invented historical example explains the comparison. Scientific equivalence is separated from matching wording; a branching example explains multiplication along paths and addition across answers. |
| Sampling; uncertainty; judgment | Success counts, repeated batches, zero successes and a worked answer rubric connect statistical statements to what was actually observed and judged. |
| Observational study | One connected invented study joins the earlier concepts and explains why its entry and measurement checks depend on one another. |
| Patching; vectors; search | Manipulation is distinguished from observation. Small numerical examples explain gradients and direction vectors, then connect candidate generation, selection and independent verification. |

The read-through found a small set of assumed prerequisites at the entry points.
The accompanying revision addresses them:

- Open with Novel's question, the earlier fixed model, the later human result,
  and what is compared before introducing the mathematics. Explain “assay” as
  the repeatable measurement procedure.
- Define prefix, forward pass, end-of-sequence, output cap and random seed at
  their first relevant use. Explain fine-tuning and reward models locally.
- Explain entailment with the difference between “exactly two” and “at least
  two,” then connect the example to semantic grouping and automatic judging.
- Define prior and posterior before contrasting credible and confidence
  intervals. Explain labels, supervision and probes before discussing detection.
- Explain latent reasoning before the context-only search readings, and scope
  the wording comparison to the four answers in the example.
- Replace unexplained terminology on the home page and add glossary entries
  for assay, entailment and supervision/probe.

Readers can still encounter unfamiliar details in later chapters, but the
explanations and links supply a route back to the relevant background. There is
no required reading order, quiz, competence declaration or progress tracking.
The review does not claim exhaustive paper reading, reproduced research
results or demonstrated usability with a novice participant. Source-access
limits remain in `source-audit.md`; actual build, browser and publication checks
are recorded separately in `publication.json`.

## Research-led editorial review — 17 October 2026

The reader changed the desired entry point: current research and a connected
literature review, with simple language and optional prerequisites. The parent
read all four Astra-drafted review essays and the three additional concept notes.
It removed introductory progression from navigation, added citations at the
argument level and linked explanations back to the reviews that use them.

Parent edits define NLP, statistical significance, mean ablation, down-projection,
syntactic features and putative single-neuron recordings locally. Optional pages
explain alignment/correlation, sparse features/transcoders and reward learning.
Equations define their symbols and illustrative quantities remain explicitly
invented. The comparison between an unchanged answer model and a newly trained
complete system is preserved. Brain prediction is distinguished from a shared
causal mechanism; publication matching from scientific validity; and candidate
availability from successful selection.

The source audit records targeted primary reads, numerical-result conditions,
the temporal-brain article correction, and the preprint-specific best-of-five
brain-guided result. Parent spot checks covered the learned-search experiment,
EurekaBench endpoints/results, curriculum-RL comparison, circuit replacement-model
evaluation and the visual-alignment word-order control. This is an editorial and
source review, not a human-reader study or independent scientific replication.

Local browser checks covered all four research routes, three new concept routes
and a legacy `#/learn/tokens` link at 391px, with typeset math, no raw delimiters,
no math errors and no horizontal page overflow. Desktop checks at 1440px covered
the homepage and circuit review; screenshots confirmed readable text and the
paired-intervention diagram. Review → concept → review navigation, mobile menu,
source filtering, empty search and concept search were exercised. No browser
warnings or errors were captured. This verifies the local build, not a signed-in
production browser session.

## Hidden-context teaching and design review — 17 October 2026

The parent read the complete new transfer review and hidden-context concept note
without relying on the papers to supply a missing explanatory step. The review
begins with a concrete shared-rule problem, then shows what the human experiment
motivates, what HC-1 supplies to a network and what competing explanations survive.
The linked note defines context, XOR, prior/posterior, Brier score, carried state
and a fitted decoder. Worked examples distinguish a prediction justified by the
evidence from a lucky answer. Hippocampus, recurrent state and causal attention
are defined where used. Diagrams and equations describe the proposed experiment;
they are not plotted results.

An independent Astra methodological reviewer inspected the source/task mapping
and identified design errors before implementation. The revised protocol uses
600 confirmation split groups from 819 available, distinguishes groups from
sampled instances, probes each trained network in its own coordinate system,
trains both ambiguity predictions and reports balanced change/stay accuracy.
The parent additionally specified a separate ordinary-recall query and the
odd-pass robustness exposure. A final review moved the competence gate to the
trained stay-query position and required both change and stay accuracy for the
reliable-transfer label; immediate recall remains a position-shift control. Known change timing, reward decoding shortcuts,
limited abstract rule diversity and a perfect one-bit baseline remain visible
limitations. The ambiguity example uses identical observations and opposite
labels; its one-half prediction follows from that explicit paired generator.

The older historical-assay pages remain useful optional reference. Their status
and current programme connections now say later scientific-transfer work. This
review is an editorial and design assessment, not testing with a novice reader,
implementation verification or independent replication. Actual content, renderer,
browser and deployment checks are recorded in the publication receipt.

## 5 November 2026 — parent review of the literature additions

Read the two new review sections, the complete relational-inference concept
note, both paper cards and their surrounding transfer/discovery arguments.
This is a targeted editorial and technical review, not a fresh audit of every
older source or a comprehension study with human readers.

The reader can enter at the research comparison and follow a concept link
without opening a paper. “Transitive,” “premise,” rank, symbolic distance and
ansatz are defined locally. The parcel example shows both candidate procedures
and explicitly charges the preparation of stored ranks. Conflicting premises
make their possible disagreement concrete without claiming to identify a neural
algorithm from a correct answer. The related/control example defines every
subscript and sign before computing a five-percentage-point illustrative
difference. It is labelled as an example, not the paper's analysis or Novel's
registered endpoint.

The new human-study count is tied to Experiment 1. The custom transformers'
reasoning-chain supervision is explicit. Unsatz's overall transfer counts are
presented before the selected successful-first-world subset, with the small
denominators and absence of independent replication retained. The article
comparisons distinguish external programs from transient model state. HC-1's
one-bit solution and behaviour-first gates remain visible; there is no new
experiment authorization. Free navigation, existing links and the absence of
quizzes, completion declarations and progress tracking are preserved.

Validation: all 12 learning-contract tests passed; all 157 mathematical
expressions rendered with the pinned KaTeX renderer. The baseline check matched
128 reviewed project inputs and the static build completed. Local Chrome
inspection confirmed the new concept note, displayed rank/transfer equations,
worked tables and the discovery-review link to its exact concept section.
The in-app browser was unavailable, so Chrome supplied this bounded desktop
preview check. No new mobile or authenticated-production visual pass is claimed.

## 20 November 2026 — parent review of the causal comparison

Read the new transfer/brain passages in context, the entire shared-relationships
note and the source card against the targeted primary methods/results. This was
a parent editorial and technical review, not an independent agent review, a new
audit of all older papers or a study with novice readers.

The note starts with four characters and two possible pairings. It defines
transition, relational structure, likelihood, prior/posterior, LSTM, RSA, ablation,
counterbalancing, standardized effect size and preregistration where needed.
The Bayesian example states its two hypotheses, equal priors, unchanged structure
and independent-probe assumptions before multiplying likelihoods. It distinguishes
noisy evidence from HC-1's initially indistinguishable causes. All displayed
symbols are explained in the surrounding prose; the reader need not open a paper
to follow the argument.

The human task and network task are separated, including the network's supplied
retrieval of same-state history. The comparison does not count repeated lesion
episodes as independently trained networks or equate the stochastic task's
80% ceiling with HC-1's deterministic accuracy gate. The human intervention
result includes both inference and direct-learning impairment; the confidence
interval and effect size are not presented as percentages. The note distinguishes
a direct comparison of effects from significance in only one group. Original
visuals and calculations explain claims; none is a plotted Novel result.

The earlier behaviour-first protocol remains active. Existing links and free
navigation are preserved; no quiz, declaration, checkbox or progress state is
introduced. Exact content, math, browser and publication checks are recorded in
the publication receipt only after verification.

The mobile preview identified long Bayesian equations. Their final form separates
likelihood-times-prior weights from normalization, with every weight defined in
the prose and the calculation broken into short aligned lines.

Verification: the initial local Chrome preview showed the new concept, equations
and table at desktop width and 391 pixels. It found sideways scrolling inside
the two long equations, which prompted the aligned rewrite. After the interrupted
run resumed, no browser was available. The final equations passed the pinned
renderer check; the final mobile fit and review-to-concept navigation were not
visually rechecked. No authenticated-production visual check is claimed.
