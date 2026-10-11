"""Mutation tests for claims that must not promote public exploratory material."""

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from validate_admission import (DATA, ROOT, check_schema, check_vocabulary,
                                read_json, time_interval, validate_collection,
                                validate_record)


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.record = read_json(DATA / "meanflow_admission.json")
        self.schema = read_json(DATA / "admission.schema.json")

    def assert_error(self, record, text):
        errors = validate_record(record)
        self.assertTrue(any(text in error for error in errors), errors)

    def event(self, kind, value, precision):
        # Adversarial declarations for tests, never recorded as real evidence.
        return {"kind": kind, "value": value, "precision": precision,
                "evidence_refs": ["meanflow-v1"],
                "caveats": ["TEST ONLY: this is not verified historical evidence."]}

    def declare_eligible(self, release, disclosure):
        record = copy.deepcopy(self.record)
        record["chronology"]["eligibility"] = "eligible"
        record["chronology"]["earlier_channel_search_complete"] = True
        record["model_snapshot"]["verified_full_public_release"] = release
        record["chronology"]["first_public_disclosure"] = disclosure
        return record

    def untrusted_review_payload(self, role):
        # These deliberately fabricated inputs test the guard. They are not
        # scientific reviews, and must never be serialized to the corpus.
        artifacts = copy.deepcopy(self.record["frozen_artifacts"])
        for item in artifacts.values():
            item["sha256"] = hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest()
        return {"reviewer_id": "TEST-ONLY-same-person", "reviewer_kind": "human",
                "expertise": "TEST ONLY: untrusted assertion",
                "independent_of_authors_and_model": True, "conflicts_disclosed": True,
                "reviewed_on": "2026-10-11", "decision": "support",
                "scope": "TEST ONLY: no review was performed",
                "evidence_refs": ["meanflow-v1"], "rationale": "TEST ONLY",
                "review_role": role, "conflict_statement": "TEST ONLY",
                "blinded_to_model_outcomes": True, "reviewed_artifacts": artifacts,
                "signature_ref": "TEST ONLY: not a real signature"}

    def test_shipped_record_is_exploratory_unreviewed_and_unmeasured(self):
        self.assertEqual([], validate_collection())
        self.assertEqual("exploratory", self.record["status"])
        self.assertEqual({"domain": None, "temporal": None}, self.record["independent_human_reviews"])
        self.assertEqual("not_measured", self.record["judgment"]["scientific_competence"])
        self.assertEqual("not_run", self.record["judgment"]["scientific_results"])
        self.assertTrue(all(g["status"] != "passed" for g in self.record["admission_gates"].values()))

    def test_accidental_admission_fails_gates_and_review_requirements(self):
        for status in ("admitted_development", "admitted_confirmation"):
            record = copy.deepcopy(self.record)
            record["status"] = status
            self.assert_error(record, "admission_gates")
            self.assert_error(record, "independent_human_reviews")
        record["status"] = "admitted"
        self.assert_error(record, "status")

    def test_checkbox_passes_cannot_substitute_for_independent_experts(self):
        record = copy.deepcopy(self.record)
        record["status"] = "admitted_development"
        for gate in record["admission_gates"].values():
            gate.update(status="passed", evidence_refs=["meanflow-v1"], blockers=[])
        record["unresolved_blockers"] = []
        self.assert_error(record, "independent_human_reviews.domain")
        self.assert_error(record, "independent_human_reviews.temporal")

    def test_a_pass_cannot_have_a_blocker_or_no_evidence(self):
        record = copy.deepcopy(self.record)
        gate = record["admission_gates"]["human_origin"]
        gate["status"] = "passed"
        self.assert_error(record, "human_origin")
        gate["blockers"] = []
        self.assert_error(record, "evidence_refs")

    def test_same_person_cannot_supply_two_independent_signoffs(self):
        record = copy.deepcopy(self.record)
        for role in ("domain", "temporal"):
            record["independent_human_reviews"][role] = self.untrusted_review_payload(role)
        record["frozen_artifacts"] = record["independent_human_reviews"]["domain"]["reviewed_artifacts"]
        self.assert_error(record, "distinct humans")

    def test_machine_or_nonindependent_or_unblinded_review_is_rejected(self):
        for key, value in (("reviewer_kind", "AI"),
                           ("independent_of_authors_and_model", False),
                           ("blinded_to_model_outcomes", False)):
            record = copy.deepcopy(self.record)
            record["independent_human_reviews"]["domain"] = self.untrusted_review_payload("domain")
            record["independent_human_reviews"]["domain"][key] = value
            self.assert_error(record, "independent_human_reviews.domain")

    def test_review_binds_matching_frozen_artifact_digests(self):
        record = copy.deepcopy(self.record)
        record["independent_human_reviews"]["domain"] = self.untrusted_review_payload("domain")
        self.assert_error(record, "not bound to the frozen artifacts")
        record["frozen_artifacts"] = copy.deepcopy(record["independent_human_reviews"]["domain"]["reviewed_artifacts"])
        record["frozen_artifacts"]["rubric"]["sha256"] = "0" * 64
        record["independent_human_reviews"]["domain"]["reviewed_artifacts"] = copy.deepcopy(record["frozen_artifacts"])
        self.assert_error(record, "bytes differ from declared digest")

    def test_model_revision_and_interface_aliases_or_other_snapshots_fail(self):
        for key in ("full_revision", "tokenizer_revision", "chat_template_revision"):
            for value in ("main", "d3e2589", "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e"):
                record = copy.deepcopy(self.record)
                record["model_snapshot"][key] = value
                self.assertTrue(validate_record(record), (key, value))
        record = copy.deepcopy(self.record)
        record["model_snapshot"]["decoded_chat_template_sha256"] = "0" * 64
        self.assert_error(record, "decoded_chat_template_sha256 disagrees")

    def test_source_versions_must_appear_in_urls_and_be_immutable(self):
        for version, url in (("main", "https://github.com/Gsunshine/meanflow/blob/main/LICENSE"),
                             ("v1", "https://arxiv.org/abs/2505.13447"),
                             ("a" * 40, "https://github.com/Gsunshine/meanflow/blob/main/LICENSE")):
            record = copy.deepcopy(self.record)
            record["provenance"]["sources"][0].update(version=version, url=url)
            self.assertTrue(validate_record(record), (version, url))
        record = copy.deepcopy(self.record)
        record["provenance"]["sources"][2]["url"] = record["provenance"]["sources"][2]["url"].replace(
            "d3e258980a49b060055ea9038dad99d75923f7c4", "a" * 40)
        self.assert_error(record, "URL omits the declared immutable revision")

    def test_unfetched_source_bytes_cannot_have_a_claimed_content_hash(self):
        record = copy.deepcopy(self.record)
        record["provenance"]["sources"][0]["content_sha256"] = "a" * 64
        self.assert_error(record, "content_sha256")

    def test_date_kinds_cannot_convert_submission_or_commit_to_visibility(self):
        record = self.declare_eligible(
            self.record["model_snapshot"]["recorded_git_commit"],
            self.record["chronology"]["submission"])
        self.assert_error(record, "proxies cannot establish eligibility")
        record = copy.deepcopy(self.record)
        record["model_snapshot"]["recorded_git_commit"]["kind"] = "public_visibility"
        self.assert_error(record, "preserve its evidence kind")

    def test_same_day_and_overlapping_uncertainty_do_not_pass(self):
        release = self.event("public_visibility", "2025-04-29", "day")
        for disclosure in (self.event("first_public_disclosure", "2025-04-29", "day"),
                           self.event("first_public_disclosure", "2025-04-29T23:59:59Z", "second"),
                           self.event("first_public_disclosure", "2025-04-28", "day")):
            self.assert_error(self.declare_eligible(release, disclosure), "overlap or are not ordered")

    def test_month_year_or_unknown_precision_cannot_establish_eligibility(self):
        for value, precision in (("2025", "year"), ("2025-04", "month"), (None, "unknown")):
            record = self.declare_eligible(self.event("public_visibility", value, precision),
                                          self.event("first_public_disclosure", "2025-05-19", "day"))
            self.assert_error(record, "coarse or unknown dates")

    def test_precision_preserves_a_day_interval_and_rejects_invalid_dates(self):
        start, end = time_interval(self.event("public_visibility", "2025-04-29", "day"))
        self.assertEqual(86400, (end - start).total_seconds())
        for value, precision in (("2025-04-29", "second"), ("2025-02-30", "day"),
                                 ("2025-04-29T00:00:00", "second"), ("2025", "unknown")):
            with self.assertRaises(ValueError):
                time_interval(self.event("public_visibility", value, precision))

    def test_known_date_order_does_not_clear_earlier_channel_blockers(self):
        record = self.declare_eligible(self.event("public_visibility", "2025-04-29", "day"),
                                      self.event("first_public_disclosure", "2025-05-19", "day"))
        record["chronology"]["earlier_channel_search_complete"] = False
        self.assert_error(record, "unresolved earlier public channels")

    def test_exposed_material_cannot_be_relabelled_confirmation(self):
        record = copy.deepcopy(self.record)
        record["exposure"].update(split="confirmation", public=False, confirmation_eligible=True)
        self.assert_error(record, "public development material cannot become confirmation")
        record["exposure"]["public"] = True
        record["split_custody"]["ever_public"] = False
        self.assert_error(record, "public fixture cannot claim it was never public")

    def test_evaluator_record_is_not_a_visible_prompt_contract(self):
        for parent in (None, "exposure"):
            record = copy.deepcopy(self.record)
            container = record if parent is None else record[parent]
            container["visible_prompt"] = {"expected": "LEAKED TARGET", "candidate_id": "meanflow"}
            self.assert_error(record, "forbidden key visible_prompt")
        record = copy.deepcopy(self.record)
        record["exposure"]["evaluator_metadata_only"] = False
        self.assert_error(record, "evaluator_metadata_only")

    def test_scientific_measurement_never_clears_historical_admission(self):
        record = copy.deepcopy(self.record)
        record["judgment"].update(scientific_competence="measured", scientific_results="measured",
                                   competence_evidence_refs=["meanflow-v1"], result_evidence_refs=["meanflow-v1"])
        # These asserted evidence references do not authenticate a result.
        record["status"] = "admitted_development"
        self.assert_error(record, "chronology")
        self.assert_error(record, "independent_human_reviews")
        record = copy.deepcopy(self.record)
        record["chronology"]["eligibility"] = "ineligible"
        self.assertEqual([], validate_record(record))

    def test_measured_competence_and_results_cannot_use_invented_evidence(self):
        for field, evidence in (("scientific_competence", "competence_evidence_refs"),
                                ("scientific_results", "result_evidence_refs")):
            record = copy.deepcopy(self.record)
            record["judgment"][field] = "measured"
            record["judgment"][evidence] = ["INVENTED-RESULT"]
            self.assert_error(record, "unknown evidence reference INVENTED-RESULT")

    def test_searches_references_and_retained_states_are_explicit(self):
        record = copy.deepcopy(self.record)
        record["provenance"]["prior_art_search_complete"] = True
        self.assert_error(record, "pending query")
        record = copy.deepcopy(self.record)
        record["target"]["human_origin"]["evidence_refs"] = ["missing-source"]
        self.assert_error(record, "unknown evidence reference")
        record = copy.deepcopy(self.record)
        record["status"] = "withdrawn"
        self.assert_error(record, "prior_admission_ref")

    def test_checker_fails_closed_on_unsupported_schema_keywords(self):
        check_vocabulary(self.schema)
        with self.assertRaisesRegex(ValueError, "unsupported schema keywords"):
            check_vocabulary({"type": "string", "not": {"const": "unsafe"}})
        self.assertTrue(check_schema(1, {"const": True}, self.schema))

    def test_json_rejects_duplicate_keys_and_nonfinite_constants(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "case.json"
            for raw in ('{"status":"exploratory","status":"admitted_development"}',
                        '{"score":NaN}', '{"score":Infinity}'):
                path.write_text(raw)
                with self.assertRaises(ValueError):
                    read_json(path)

    def test_optional_full_draft_validator_agrees_on_shipped_shapes(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is optional and is not a project dependency")
        jsonschema.Draft202012Validator.check_schema(self.schema)
        validator = jsonschema.Draft202012Validator(self.schema)
        self.assertFalse(list(validator.iter_errors(self.record)))
        for status in ("admitted_development", "admitted_confirmation"):
            record = copy.deepcopy(self.record)
            record["status"] = status
            self.assertTrue(list(validator.iter_errors(record)))


if __name__ == "__main__":
    unittest.main()
