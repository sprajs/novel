# Infrastructure handoff v0.1

The research branch owns only `data/ground_truth/`, `docs/ground_truth/`, and `tests/ground_truth/`. Root packaging, configuration, model loading and inference belong to the infrastructure work. No root dependency or execution policy is imposed by these artifacts.

The sibling [dataset handoff v1](https://github.com/sprajs/novel/blob/c5a361363de8bb08aacc5119f1f435a847ad44d3/docs/dataset-interface.md) was read at immutable commit `c5a361363de8bb08aacc5119f1f435a847ad44d3`. Its exact nine-key `novel.tasks.TaskInput` schema is supported by `tests/ground_truth/infrastructure_adapter.py`. Native `calibration` maps to public `mechanics`; native `development` remains `development`. Its integer `schema_version: 1` is an export format, distinct from native `ground-truth-v0.1`. We do not map any public fixture to confirmation or silently designate a donor corpus.

```sh
python tests/ground_truth/infrastructure_adapter.py export --collection calibration --condition premises_only > /tmp/calibration-public.jsonl
python tests/ground_truth/infrastructure_adapter.py export --collection research --condition minimal_bridge > /tmp/research-public.jsonl
python tests/ground_truth/infrastructure_adapter.py export --collection meanflow --condition premises_only > /tmp/meanflow-public.jsonl
python tests/ground_truth/check_sibling_interface.py
```

The final command replays acceptance by the **actual** sibling `TaskInput` and JSONL loader using two source files from the fetched immutable Git object, copied into temporary storage. It does not merge sibling code, install packages, or run models. If the commit is absent, fetch the sibling branch first. Evaluation is separate: `evaluate_raw(world_id, raw_text)` returns verifier/version/hash, strict-parse validity, status, correctness and failure reason. It rejects duplicate keys, nonfinite numbers, code fences and trailing explanation rather than repairing outputs. `world_id` must resolve to one evaluator task; the adapter rejects ambiguous multi-target mappings. Counterfactual dependence is retained separately in the native parent/lineage metadata.

## Contracts

`data/ground_truth/schema.json` defines Draft 2020-12 records using `$defs`. `artifact_tools.py` performs the cross-record scientific checks using the standard library; it is intentionally not a general JSON Schema implementation. Fixture premise/target payloads are mechanism-specific and are validated by the corresponding exact verifier. The schema permits their extension while enforcing the shared identity/split contract. No undeclared schema version should be silently accepted.

| File | Consumer contract |
| --- | --- |
| `candidate_registry.json` | `schema_version`, `candidates`; admission is independent from ranking |
| `calibration_fixtures.json` | `fixtures`; exact offset and badge payloads; all public calibration |
| `research_fixtures.json` | `fixtures`; research identity examples; all public development |
| `meanflow_fixtures.json` | `fixtures`; contemporary calculus consequences and invalid-bridge controls; all public development |
| `prompt_contract.json` | Visible/evaluator separation, named arms, capture cue and unresolved freeze gates |
| `model_audit.json` | Research evidence for model choice, **not** an instruction to download/run a model |
| `split_policy.json` | Prospective partition and dependency rules; confirmation unmaterialized |
| `manifest.json` | Inventory of source-controlled ground-truth artifacts, byte hashes and limitations |

Canonical fixture IDs are stable and globally unique across fixture files. `world_id` identifies a latent world, `family_id` its structural family, `candidate_id` the research lead or synthetic mechanism. All variants of a world share its split. Optional `template_lineage` and `counterfactual_parent_id` link aliases and parent worlds; when present, they also cannot cross splits. These identifiers need independent structural review: a validator cannot detect an isomorphic world hidden behind mistaken IDs. Donor-library sharing is recorded for statistical dependence, not prohibited across recipient runs. Primary structural confirmation families must not appear among development or donors. No blind-test ID or answer is embedded in the public collection.

## Rendering and evaluation APIs

For standalone calibration, load `tests/ground_truth/calibration.py` with `importlib.util.spec_from_file_location` or run tests from its directory. Use `load_fixtures`, `render_prompt`, `solve_fixture`, and `verify_response`. Its renderer is behavioral text only; an extraction wrapper must append the common cue, record token alignment and pass causality checks before activation capture. Research packet verifiers reside beside their tests. They use exact arithmetic where possible, do not run generated code and need no network. The test location is a scoped handoff; infrastructure may wrap these APIs after agreeing on a stable runtime package.

The general `build_prompt_record(visible, condition, treatment)` helper in `artifact_tools.py` accepts only the declared visible keys and returns text plus its SHA-256. It deliberately rejects a complete fixture or candidate object. `answer_only` and `full_explanation` require the explicit diagnostic flag. This prevents accidental serialization of `expected`/source metadata into ordinary prompts, but cannot certify that a human-authored bridge has no semantic answer leak. Review its text.

The inference adapter receives only rendered text and its visible record. The evaluator receives `fixture_id`, raw output and the hidden/evaluator fixture. Gold fields never travel through a generic `**fixture` prompt API. Prompt construction and verification may share type definitions, but solve routines must not be called inside a baseline renderer. Do not infer scientific eligibility from a parser success.

## Model handshake

Keep distinct `model_role` values `mechanics` and `historical`. Infrastructure pins July 26, 2025 Qwen3-0.6B `c1899de289a04d12100db370d81485cdf75e47ca` and Qwen3-1.7B `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e` for mechanics. Its reported CPU smoke test establishes mechanics only, with no scientific behavior validated. Training cutoff remains undocumented. The April announcement does not backdate these full snapshots or their changed templates.

The separate historical audit identifies April 29 Qwen3 full snapshots for possible later-May targets: 0.6B `6130ef31402718485ca4d80a6234f70d9a4cf362`, 1.7B `d3e258980a49b060055ea9038dad99d75923f7c4`. Their original template hash differs from the mechanics pins; they require their own runtime/template checks. Historical Pythia snapshots are another separate lane for 2023-and-later targets. The model audit documents why current Pythia `main` or `step143000` is not a substitute for an April 2023 snapshot. Historical admission remains pending; known dates are necessary but insufficient.

Before any historical run, infrastructure must return exact model/tokenizer commits, per-file hashes, public-release evidence, architecture/config hash, all post-training/adapters, precision/conversion recipe, source license, template/hash/arguments, backend/software revision and a no-op/parity report. Newly trained adapters or fine-tuning create a new information-bearing checkpoint. Deterministic format conversions require documented derivation and parity; a later conversion file is not itself proof of a pre-disclosure public release.

`run_record` in the schema defines the minimum research-side metadata. Infrastructure can extend it with timings, tensors and cache events. An immutable configuration hash, fixture hash, exact prompt and generated tokens, conditions, truncation, RNG streams, donor world IDs, intervention digest and verifier version are required to interpret results. RNG null means the named stream is unused, not unknown; unknown required seeds make the run non-reproducible. A null correctness verdict means unevaluated, not incorrect. Store zeros and nulls with declared meaning; missing costs are not zero costs. Source timestamps require an explicit zone. The low-level donor pair guard trusts supplied answer-equivalence keys; those must come from the declared verifier and prospective allocation, never arbitrary caller guesses.

`research_prompting.py` supplies a runnable projection/cue wrapper and a grounded DPO development pair. For example, `python tests/ground_truth/research_prompting.py dpo-dev-001 --condition minimal_bridge` produces prompt text, byte hash and character boundary without consulting gold labels. Token alignment remains the inference adapter's responsibility. `transfer_examples.json` specifies a donor with probability 16/97 and a recipient with probability 3/4; the guard recomputes both from premises. This is a same-family development integration example, not structural confirmation. UNKNOWN and support-invalid fixtures accompany it as guardrails.

The public handoff is reviewable in this branch. Exact model/interface agreement with the execution implementation remains pending until its pinned model manifest and instrumentation test report are returned.
