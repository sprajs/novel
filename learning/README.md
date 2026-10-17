# Novel reading room

The [private reading Site](https://novel-reading-room.sprajs.chatgpt.site) is a
living literature review for Novel. It opens with current research questions
about discovery, reasoning, internal mechanisms and comparisons with brains.
Reviews connect primary papers, explain methods and results in plain language,
and distinguish reported findings from what Novel has actually established.
Technical terms are defined in the argument; longer explanations are available
through linked concept notes. There is no required reading order.

- `content.json`: research reviews, concept notes, source records and glossary.
- `source-audit.md`: search coverage, exact source versions, access depth and claim checks.
- `TEACHING-REVIEW.md`: editorial review of explanations and evidence boundaries.
- `baseline.json`: reviewed research revision, input hashes and content hash.
- `site/`: HTML, CSS, JavaScript, local KaTeX assets and the stable hosting identity.
- `MAINTENANCE.md`: selection, review, concept expansion and publication contract.
- `CHANGES.md`: substantive editorial changes and reasons.
- `publication.json`: verified deployment receipt and maintenance automation identity.

Build offline using standard-library Python 3.12+ and Node.js 20+:

```sh
python scripts/learning/build.py --check
python -m unittest discover -s tests/learning -v
node scripts/learning/check_math.mjs
python scripts/learning/build.py
python -m http.server 8765 --directory learning/site/dist --bind 127.0.0.1
```

The generated `dist/` is ignored and reproducible. Source PDFs, credentials,
model weights, research packets and raw runs are excluded. Paper results are
attributed reports, not independent replications; invented examples are labeled.

## Linked reviews and explanations

`reviews` holds research-led essays at `#/review/<id>/<section-id>`. Each section
can cite source IDs through `citations` and offer `conceptLinks` with `chapter`,
optional `section`, and a descriptive `label`. Every review source must be cited
in its argument. `relatedReviews` connects questions without imposing a sequence.

The existing `chapters` collection now holds optional concept notes at
`#/concept/<id>/<section-id>`. Old `#/learn/...` links still resolve. Notes can be
reordered without changing navigation. Keep IDs stable when changing titles.
The `prerequisites` metadata describes background links, never a reading gate.

When the reader highlights a term or passage and asks for an explanation, add a
focused concept note (or a focused section if one already fits), link it from
that passage's section, and include a return connection to the research review.
Explain the particular concept in its research context; do not append a generic
introductory course. Text selection itself does not submit a request or store
personal reading state. Future changes go through the same reviewed publication
workflow.

Sources have a stated access scope. Keep targeted full-text reading, publisher
abstracts, author accounts and earlier repository checks distinct. `source-audit.md`
records bounded searches and why sources were selected or deferred. New papers
need a concrete connection to Novel; a date alone is not an inclusion criterion.

Diagrams use flows, matrices, worked tables or a residual schematic. Equations
use `\(...\)` inline and `\[...\]` displayed, with escaped backslashes in JSON.
Define symbols alongside each equation. The pinned local KaTeX renderer emits
selectable visual notation and accessible MathML. Its provenance and MIT license
are retained in `site/vendor/katex/`; no runtime CDN is required. Checks reject
broken review citations, concept anchors, unsafe URLs, invalid math, stale assets
and unreviewed input drift. Quizzes, declarations, checkboxes and progress tracking
remain excluded.
