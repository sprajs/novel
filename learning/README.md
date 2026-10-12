# Novel reading room

The [private reading Site](https://novel-reading-room.sprajs.chatgpt.site) is the
project's living baseline: the concepts and primary sources needed to understand
the experiment being built. Its audience is the repo owner, starting from basic
model and probability concepts. It follows Novel's decisions rather than a
general computer-science syllabus.

- `content.json`: original lessons, paper summaries, source access labels and glossary.
- `source-audit.md`: primary-source verification and reading-inventory coverage.
- `TEACHING-REVIEW.md`: parent review of beginner readability and addressed prerequisites.
- `baseline.json`: reviewed research revision, input hashes and content hash.
- `site/`: dependency-free HTML, CSS and JavaScript, plus the stable hosting identity.
- `MAINTENANCE.md`: when to add, defer, retire and publish reading.
- `CHANGES.md`: substantive curriculum changes and reasons.
- `publication.json`: deployment receipt and the saved maintenance automation.

Build and validate offline using standard-library Python (3.12 or later):

```sh
python scripts/learning/build.py --check
python -m unittest discover -s tests/learning -v
python scripts/learning/build.py
python -m http.server 8765 --directory learning/site/dist --bind 127.0.0.1
```

Open `http://127.0.0.1:8765`. The generated `dist/` is ignored and reproducible;
the source, bibliography and review receipts are committed. Examples are
illustrations, not experimental observations. Readers choose their own order;
there are no quizzes or progress tracking. No papers, weights or private experiment data are served.

Each section has an explicit stable `id`, used in routes such as
`#/learn/likelihood/why-log-probabilities-are-added`. Preserve these IDs when
editing a heading. Chapter `connections` pair a chapter ID with a reason to
follow the link; glossary entries link back to a fuller explanation. The builder
validates those references, primary method URLs and worked figure structures.
Diagrams can be flows, V/M matrices, worked tables or a residual bypass schematic.
