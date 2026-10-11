# Evidence, admission, and annotation

## What is admitted

An item is a precisely scoped proposition plus an input packet, not a paper title. Distinguish (a) an old algebraic identity, (b) its later use in a training or systems method, and (c) a measured benefit of that method. An exact identity verifier certifies (a); it does not establish that the model invented (b) or reproduced (c).

Keep these judgments separate in every review: **correctness**, **deducibility from supplied premises**, **historical eligibility**, **novelty relative to prior art**, **assistance**, and **empirical usefulness**. A historically ineligible derivation can be correct. A previously unknown empirical result can be impossible to infer from the supplied information. A successful historical reconstruction can use later vocabulary without demonstrating contamination.

Historical eligibility requires all of the following before target evaluation:

1. The exact frozen weights, tokenizer, templates, post-training, adapters and transformations are identified. All information-bearing learned components were publicly released before the target's earliest known equivalent public disclosure. An advertised training cutoff or model failure is insufficient.
2. Public-release evidence concerns the actual checkpoint artifacts. A repository creation date, Git commit author timestamp, or later description of an earlier model is supporting evidence, not automatic proof of public availability at that time. Mutable `main`, a moving `step` tag, and a newly converted archive need file-level audit.
3. The target has an earliest **verified** public disclosure with version, date precision, exact claim location and a bounded search log. Inspect v1 rather than importing claims added to a later paper revision.
4. Search preprints and revisions, code commits/releases, abstracts, proceedings, talks/slides, theses, technical reports and equivalent prior art. If a relevant channel cannot be checked, preserve that gap. Absence of a search hit is not proof of absence. The strict date inequality is checkpoint public release < target disclosure; same-day evidence needs times or remains ambiguous.
5. A/B and all other information supplied to the model are audited separately. Post-disclosure pair selection and bridge construction are hindsight assistance even when both component facts are old. A bibliography selected from the target paper is assistance.
6. The consequence is independently checkable and possible under the stated assumptions. A/B competency is probed in fresh contexts. Competence does not make an empirical outcome deducible.
7. Two independently recorded reviews resolve claim scope, chronology and verifier behavior before admission. AI worker agreement in this session is an audit aid, not independent human peer review.

No candidate in this first collection is declared fully admissible. `priority_pending_audit` ranks the next audit effort; it is not a weaker synonym for “clean.” An earlier equivalent mathematical result disqualifies the *claimed later discovery of that identity*, even when the later systems application remains interesting.

## Evidence hierarchy and provenance

| Level | Evidence | Appropriate claim |
| --- | --- | --- |
| E1 | Immutable, dated primary artifact and contemporaneous public-release record; inspected claim/version; file digest | Narrow supported chronology or exact-content claim |
| E2 | Versioned primary preprint/history, publisher record, official code release or model history | Verified disclosure or revision date, with public-availability caveats where applicable |
| E3 | Primary author's retrospective account, current model card, commit metadata without contemporaneous archive | Useful corroboration; public-date and artifact-identity gaps remain |
| E4 | Secondary source, search snippet, generated summary, advertised cutoff | Lead only; do not use as sole admission evidence |
| E0 | Unavailable or uninspected material | Explicit unresolved issue, never affirmative verification |

A stronger level does not settle unrelated claims: an immutable PDF can show a theorem but not establish absence of an earlier talk. Record source URL, upstream version/revision, access date, access outcome, claim supported, date and precision, artifact hash if actually acquired, and limitations. A URL-only citation has `content_sha256: null`; never fabricate a hash of unacquired content. A hash of metadata is not a hash of weights. Preserve author-reported empirical claims as such.

`earliest_verified_public_date` means the earliest supported event found in this bounded audit. `earliest_date_status` must retain pending channels and equivalent-prior-art uncertainty; it does not certify an exhaustive earliest date. A newly found antecedent updates the registry and exclusion reason, without retroactively changing old experimental eligibility records.

## Ranking rubric

Five ordinal axes range from 0 to 2: deducibility from explicit premises; strength of mechanical verification; temporal separation from a plausible immutable public checkpoint; isolation of the claimed novelty from antecedents; prerequisite feasibility for a small older model. Higher totals prioritize review, with ties resolved by the written rationale and scientific diversity. An unresolved chronology or licensing gate cannot be overcome by a high total. These are reviewer judgments, not measured probabilities, and no score depends on whether a target model happened to fail unaided or improve with a hint.

The survey retains rejected cases because they diagnose bad selection rules. Dates, popularity, impressive benchmarks and apparent model failure are not substitutes for claim-level admission.

## Annotation procedure

1. Write the target in one or two falsifiable sentences before reading model outputs. State the best known earlier equivalent and the residual new contribution.
2. Separate premises, relational operation, deductive consequence, and claims requiring new measurements. Mark supplied contemporary facts, chosen vocabulary, and hindsight selection.
3. Have a correctness reviewer derive the answer using a second route where possible. For UNKNOWN, exhibit two consistent worlds with different answers; for INCONSISTENT, provide contradictory constraints. Finite sampling alone never proves an unbounded universal identity.
4. Have a temporal reviewer inspect source versions and model metadata independently of the correctness labels. Store disagreements and their resolution; do not overwrite dissent with a consensus sentence.
5. Label assistance: `observations_only`, `explicit_prerequisites`, `minimal_bridge`, `scaffold`, `worked_answer`, `external_retrieval`, or `bibliography_selected_in_hindsight`. More than one may apply.
6. For outputs, score parse validity and target correctness first. Then classify behavior with uncertainty: prerequisite/knowledge, retrieval, search/composition, arithmetic, instruction/format, information insufficiency, truncation, or unresolved. Do not infer a uniquely absent mental operation from text.
7. Record plausible valid alternative routes even if they do not use the nominated bridge. Accept correct equivalent outputs. A correct answer that cannot establish a requested proof gets answer credit and a separate failed/unknown proof label.

## Independent reviewer checklist

- [ ] I reviewed the scoped claim rather than assuming the title defines novelty.
- [ ] I checked v1 content and searched for earlier equivalent disclosures in the listed channels.
- [ ] I distinguished a verified earliest-found date from an exhaustive earliest date.
- [ ] I inspected public checkpoint release evidence and all learned/post-training components.
- [ ] I did not equate Qwen mechanics eligibility with Pythia historical eligibility.
- [ ] Both primary arms receive identical A/B and observations; the bridge adds a relation, not an absent empirical fact.
- [ ] I verified the target independently, including undefined/underdetermined and inconsistent cases.
- [ ] I tested alternative correct routes and at least one tempting wrong route.
- [ ] I inspected answer-bearing donor text, identifiers, metadata and renderer fields for leakage.
- [ ] The whole latent world and structural lineage are confined to the declared split.
- [ ] Candidate selection and confirmation selection did not use observed unaided/hinted outcomes.
- [ ] Reuse rights are checked per code, data, paper and model artifact; missing terms remain unresolved.
- [ ] The proposed conclusion is behavioral transfer or historical reconstruction under audited inputs, not direct access to thoughts or proof of novelty today.

Record reviewer identity/role, date, reviewed artifact digests, verdict, unresolved objections, and conflict/adjudication notes in an append-only review record. Human review and experimental outcome collection remain unperformed in this collection.
