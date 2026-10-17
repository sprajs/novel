# Beginner readability review — 12 October 2026

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
