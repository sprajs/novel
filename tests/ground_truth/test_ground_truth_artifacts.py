"""Ground-truth data-flow failures that must stop an experiment."""

import json
from pathlib import Path
import tempfile
import unittest

from artifact_tools import (DATA, ROOT, build_prompt_record, check_donor_pair,
                            check_schema, digest, make_manifest, read_json,
                            validate_collection, validate_split_rows)


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.visible = {
            "task": "Use the observations.",
            "premises_a": "One instrument has one fixed offset.",
            "premises_b": "Differences can be added along a chain.",
            "observations": ["Instrument p reads A=4, B=3."],
            "question": "Find A-B.",
            "response_format": '{"status":"IDENTIFIED","value":"rational"}',
        }

    def test_primary_arms_preserve_all_premises_and_common_prefix(self):
        plain = build_prompt_record(self.visible)
        bridge = build_prompt_record(self.visible, "minimal_bridge", "Compare within an instrument.")
        self.assertEqual(plain["common_prefix_sha256"], bridge["common_prefix_sha256"])
        for record in (plain, bridge):
            self.assertIn(self.visible["premises_a"], record["text"])
            self.assertIn(self.visible["premises_b"], record["text"])
            self.assertEqual(record["sha256"], digest(record["text"].encode()))
            self.assertTrue(record["text"].endswith("Continue with the requested response."))

    def test_evaluator_record_cannot_be_rendered(self):
        for forbidden in ("expected", "certificate", "candidate_id", "ranking", "world_id"):
            bad = dict(self.visible, **{forbidden: "SECRET_GOLD"})
            with self.assertRaises(ValueError):
                build_prompt_record(bad)

    def test_answer_diagnostics_require_explicit_opt_in(self):
        for condition in ("answer_only", "full_explanation"):
            with self.assertRaises(ValueError):
                build_prompt_record(self.visible, condition, "SECRET_GOLD")
            self.assertIn("SECRET_GOLD", build_prompt_record(self.visible, condition, "SECRET_GOLD", diagnostic=True)["text"])
        with self.assertRaises(ValueError):
            build_prompt_record(self.visible, "premises_only", "accidental bridge")

    def test_same_world_and_structural_lineage_cannot_cross_splits(self):
        rows = [{"fixture_id": "a", "world_id": "w", "family_id": "f", "split": "development"},
                {"fixture_id": "b", "world_id": "w", "family_id": "f", "split": "confirmation"}]
        errors = validate_split_rows(rows)
        self.assertTrue(any("world_id" in e for e in errors))
        self.assertTrue(any("family_id" in e for e in errors))
        rows[1]["world_id"] = "new_world"
        self.assertTrue(validate_split_rows(rows))
        rows[1]["family_id"] = "new_family"
        self.assertEqual([], validate_split_rows(rows))

    def test_different_answer_is_more_than_different_fixture_id(self):
        donor = {"world_id": "w1", "family_id": "f1", "split": "development"}
        recipient = {"world_id": "w2", "family_id": "f2", "split": "confirmation"}
        self.assertEqual([], check_donor_pair(donor, recipient, "rational:1", "rational:-2"))
        self.assertTrue(check_donor_pair(donor, recipient, "rational:1", "rational:1"))
        self.assertTrue(check_donor_pair(donor, recipient, "UNKNOWN", "UNKNOWN"))
        same_world = dict(recipient, world_id="w1")
        self.assertTrue(check_donor_pair(donor, same_world, "1", "2"))

    def test_counterfactual_parent_and_template_aliases_remain_clustered(self):
        rows = [{"fixture_id": "a", "world_id": "parent", "family_id": "f1", "split": "development", "template_lineage": "template"},
                {"fixture_id": "b", "world_id": "child", "family_id": "f2", "split": "confirmation", "template_lineage": "template", "counterfactual_parent_id": "parent"}]
        errors = validate_split_rows(rows)
        self.assertTrue(any("template_lineage" in e for e in errors))
        self.assertTrue(any("parent" in e for e in errors))
        self.assertTrue(validate_split_rows(list(reversed(rows))))

    def test_run_metadata_rejects_fake_verdicts_seeds_and_dates(self):
        schema = read_json(DATA / "schema.json")
        props = schema["$defs"]["run_record"]["properties"]
        bad_evaluation = {"parse_valid": "yes", "correct": "banana", "audit_status": True}
        self.assertTrue(check_schema(bad_evaluation, props["evaluation"], schema))
        good_evaluation = {"parse_valid": True, "correct": None, "audit_status": "pending"}
        self.assertFalse(check_schema(good_evaluation, props["evaluation"], schema))
        for bad_seed in ([], {}, True, "2", -1):
            seeds = {key: 1 for key in ("world", "donor", "sampling", "intervention")}
            seeds["sampling"] = bad_seed
            self.assertTrue(check_schema(seeds, props["rng_seeds"], schema))
        time_spec = schema["$defs"]["source"]["properties"]["retrieved_at"]
        for bad_date in ("not-a-timestamp", "2026-10-11", "2026-10-11T12:00:00", "2026-02-30T12:00:00Z"):
            self.assertTrue(check_schema(bad_date, time_spec, schema))
        self.assertFalse(check_schema("2026-10-11T12:00:00Z", time_spec, schema))

    def test_schema_rejects_clean_label_and_mutable_model_revision(self):
        schema = read_json(DATA / "schema.json")
        status_schema = schema["$defs"]["candidate"]["properties"]["status"]
        self.assertTrue(check_schema("clean", status_schema, schema))
        revision_schema = schema["$defs"]["run_record"]["properties"]["model_revision"]
        for revision in ("main", "step143000", "April 2023"):
            self.assertTrue(check_schema(revision, revision_schema, schema))
        self.assertFalse(check_schema("a" * 40, revision_schema, schema))

    def test_json_does_not_silently_overwrite_duplicate_or_nonfinite_data(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "case.json"
            for contents in ('{"expected":1,"expected":2}', '{"value":NaN}'):
                path.write_text(contents)
                with self.assertRaises(ValueError):
                    read_json(path)

    def test_manifest_detects_byte_change_without_self_reference(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "data/ground_truth"
            folder.mkdir(parents=True)
            path = folder / "example.json"
            path.write_text('{"x":1}\n')
            before = make_manifest(root)
            (folder / "manifest.json").write_text(json.dumps(before))
            self.assertEqual(before, make_manifest(root))
            path.write_text('{ "x": 1 }\n')
            self.assertNotEqual(before, make_manifest(root))

    def test_collection_cross_references_and_splits(self):
        self.assertEqual([], validate_collection())


if __name__ == "__main__":
    unittest.main()
