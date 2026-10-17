# Novel's living research baseline

When changing the research question, protocols, paper selection, models,
execution semantics or validated capabilities, review the teaching guide in
`learning/` as part of the same change. Follow `learning/MAINTENANCE.md`.
Explain new prerequisites, add reading only for a concrete project decision,
and retire or defer reading that no longer serves the current direction.

Lead with current research questions and a critical synthesis of primary papers
in AI discovery, reasoning, interpretability and relevant neuroscience. Write in
plain language, defining terms where they enter the argument. Put extended
prerequisites in linked concept notes, rather than making introductory chapters
the entry point. Add a focused, linked explanation page when the reader asks
about a passage. Explain connections with concrete examples, diagrams and maths.
The Site is an open reading reference: no quizzes, comprehension declarations,
completion checkboxes, progress tracking or enforced reading order.

Run `python scripts/learning/build.py --check`. A changed input fingerprint is
a request for substantive review, not permission to refresh hashes blindly.
The guide must distinguish proposed work, engineering checks, numerical
qualification and independently supported scientific results.

The Site remains private and uses the existing project identity in
`learning/site/.openai/hosting.json`. Do not create a replacement Site during
updates. Preserve unrelated work, PDFs, credentials and raw runs outside the
published artifact. Changes go through a pull request; do not infer merge
authorization from a request to update reading.
