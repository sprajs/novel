# Keep the reading baseline aligned with Novel

The Site is a research-led literature review for Novel. Select recent work on
AI discovery, reasoning, interpretability and neuroscience for a concrete
connection to measuring, explaining or improving discovery. The canonical
source lives in this repository. The active next experiment is hidden-context
transfer (HC-1, `Plan/hidden-context-protocol.md`); review its task information,
reference policies and behavioural evidence before promoting representation or
causal claims. Historical reconstruction is a later scientific-transfer track. Its stable,
private Site identity is in `site/.openai/hosting.json`. Preserve that identity
and audience on every publication.

Start with a current research question, finding or disagreement. Use simple
language and define terms where they first matter, without requiring prior
paper reading. Explain methods, results, assumptions and limitations; compare
papers rather than listing summaries. Keep extended prerequisites in linked
concept notes and retain stable links when adding a requested explanation of
a highlighted passage. Do not add quizzes, comprehension declarations, completion checkboxes,
progress tracking or enforced reading order. The reader chooses what to read.

## Review triggers and decisions

Review when the question, admitted corpus, measurement contract, model artifact,
execution behavior or validation evidence changes. The input fingerprint covers
the README, Plan, docs, model environments, source implementation, discovery
specification, calibration tools and selected paper manifests. New/deleted input
files are detected as well as edits. CI flags drift on pull requests; branch
protection is configured separately and is not claimed here.

Also perform a bounded primary-literature search when seven days have passed
since the last documented frontier search, or when the reader requests a
research update. Search all four review areas, record queries and coverage
dates, and follow useful new papers to methods/results rather than treating
search snippets as full-text access. Include counterevidence and competing
methods. A newer publication is not automatically better or relevant. Do not
call the selection exhaustive, a live ranking, or the latest available result
without a suitably scoped check. Preserve the previous publication when nothing
material changes; record quiet search receipts in automation-local state.

For every material change, inspect the actual current repo state and answer:

1. Which decision must the reader now understand?
2. Which prerequisites are missing from the current explanation?
3. Which existing sources still help make that decision?
4. Which reading should move to `later`, `context` or `retired`?

Update `content.json`, its source access labels, and `source-audit.md`. Use
primary sources. Separate abstract/metadata checks from targeted methods
reading; preserve the distinction between authors' results and independent
replication. Never upgrade scientific status from a smoke or numerical test.
Update `CHANGES.md` with additions, removals and reasons. Remove retired sources
from chapter dependencies and active recommendations. `retired` records are
visible only through the explicit retired-library filter; they are not homework.
Changing the original inventories can remove a source entirely, if its reason
and original identity remain in the audit/change record.

Only after substantive review, record the full research revision and the actual
review date. This command intentionally does not infer that hashes prove
understanding:

```sh
python scripts/learning/build.py --refresh-baseline \
  --revision FULL_RESEARCH_COMMIT_SHA --reviewed-at YYYY-MM-DD
python -m unittest discover -s tests/learning -v
node scripts/learning/check_math.mjs
python scripts/learning/build.py --check
python scripts/learning/build.py
```

Use LaTeX delimiters for mathematics, with displayed equations for the main
relationships. Keep definitions and worked steps alongside the notation. The
pinned KaTeX assets are local; preserve their provenance and license when
updating them. Check all expressions with the same renderer used by the browser.

The baseline revision identifies the research commit reviewed. The per-file
hashes also record reviewed modifications in the curriculum PR, including the
README link; the revision is not a claim that every hashed byte already existed
in that research commit. The content hash detects changes made after review.
The Site's source commit and deployment version are separate publication
identities. Do not update the review date on unchanged daily checks.

## Publish the same private Site

Use the current Sites skill and its supported source helper. Read `get_site`,
confirm owner/private access and obtain a fresh short-lived source credential.
Never put credentials into files, command arguments, Git remotes or output.

Open the existing Site source in an empty ignored directory under
`.local/`, using the source helper and its hidden-stdin credential input. Use
the returned checkout path. Then mirror the checked canonical build:

```sh
python scripts/learning/prepare_publish.py --checkout .local/learning-site
```

If the helper returns a different checkout, pass that path instead. The mirror
preserves Git metadata and unrelated files. It replaces only the declared Site
source and generated output. The hosted source contains the exact static output
and review receipts; the full research repo, PDFs and raw runs are excluded.

Run the Sites source helper with the opening result, credential, `commands: []`
and an absolute archive path under `.local/`. Pass its verified project ID,
source commit and archive to the private save/deploy operation. Retain version
and deployment IDs and poll only nonterminal states. Read back the GitHub PR
head/checks and the deployment result. A build, push or saved version is not a
successful deployment. A failure preserves the last working publication.

## Daily maintenance

A daily local heartbeat in the originating Codex chat reviews this repository
and the existing Site. It uses authenticated GitHub and Sites access available
to that chat, requires the desktop/host to be available, and is not a cloud
service or real-time guarantee. There is no public write endpoint or stored
publishing token. Its native automation state is separate from this document.

Fetch the remote before comparing inputs. If a curriculum PR remains open,
update that PR rather than creating duplicates, and account for newer changes
on the default branch. Use an isolated checkout for unattended work and preserve
dirty user work. Do not merge PRs automatically. Once this feature is merged,
review the default branch and create/update a focused reading PR when needed.
Publish the reviewed reading branch to the same Site, retaining an accurate
research revision and recording its review/PR provenance. Publication of a
reading update is not approval or merge of a research change.

Stay quiet when unchanged or non-actionable. Notify meaningful updates,
publication failure, inaccessible sources/access or a required research
decision. Do not acquire paid compute, contact reviewers or conduct unrelated
research as maintenance. If authentication or the runtime is unavailable, report
the exact limitation; do not claim unattended updates worked.
