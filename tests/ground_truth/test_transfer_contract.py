import copy
import unittest
from unittest.mock import patch

from artifact_tools import DATA, read_json
from research_prompting import (dpo_answer_key, load_research_fixtures,
                                render_research_prompt, validate_transfer_examples)
from research_verifiers import solve_fixture, verify_fixture


class GroundedTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = load_research_fixtures()

    def test_actual_donor_and_recipient_have_different_verified_answers(self):
        self.assertEqual([], validate_transfer_examples(self.fixtures))
        donor = self.fixtures["dpo-dev-001"]
        recipient = self.fixtures["dpo-dev-002"]
        self.assertNotEqual(dpo_answer_key(donor), dpo_answer_key(recipient))
        self.assertFalse(verify_fixture(recipient, solve_fixture(donor)))

    def test_fabricated_equivalence_keys_and_fake_holdout_are_rejected(self):
        record = read_json(DATA / "transfer_examples.json")
        record["pairs"][0]["donor_answer_key"] = "pretend-different"
        record["pairs"][0]["structural_holdout"] = True
        errors = validate_transfer_examples(self.fixtures, record)
        self.assertTrue(any("fabricated" in e for e in errors))
        self.assertTrue(any("holdout" in e for e in errors))

    def test_primary_renderer_ignores_oracles_and_evaluator_metadata(self):
        fixture = copy.deepcopy(self.fixtures["dpo-dev-001"])
        original = render_research_prompt(fixture)
        fixture["expected"] = {"value": "SECRET_GOLD"}
        fixture["candidate_id"] = "SECRET_GOLD"
        fixture["premises"]["expected"] = "SECRET_GOLD"
        fixture["target"]["expected"] = "SECRET_GOLD"
        with patch("research_prompting.solve_fixture", side_effect=AssertionError("baseline called oracle")):
            mutated = render_research_prompt(fixture)
            bridge = render_research_prompt(fixture, "minimal_bridge")
        self.assertEqual(original, mutated)
        self.assertNotIn("SECRET_GOLD", bridge["text"])
        self.assertEqual(mutated["common_prefix_sha256"], bridge["common_prefix_sha256"])

    def test_all_research_conditions_render_and_answer_only_is_explicit(self):
        for fixture in self.fixtures.values():
            baseline = render_research_prompt(fixture)
            for condition in ("minimal_bridge", "alternate_bridge", "wrong_bridge", "irrelevant", "generic_reasoning"):
                record = render_research_prompt(fixture, condition)
                self.assertEqual(baseline["common_prefix_sha256"], record["common_prefix_sha256"])
            with self.assertRaises(ValueError):
                render_research_prompt(fixture, "answer_only")
            self.assertTrue(render_research_prompt(fixture, "answer_only", diagnostic=True)["diagnostic"])

    def test_information_gap_and_domain_error_remain_guardrails(self):
        unknown = self.fixtures["dpo-dev-003"]
        inapplicable = self.fixtures["dpo-dev-004"]
        self.assertEqual("UNKNOWN", solve_fixture(unknown)["status"])
        self.assertEqual("INAPPLICABLE", solve_fixture(inapplicable)["status"])
        for fixture in (unknown, inapplicable):
            with self.assertRaises(ValueError):
                dpo_answer_key(fixture)
            self.assertFalse(verify_fixture(fixture, solve_fixture(self.fixtures["dpo-dev-001"])))

    def test_numeric_observation_fields_cannot_smuggle_records_or_prose(self):
        for fixture_id, field in (("dora-dev-001", "v"), ("dora-dev-006", "W0"), ("dpo-dev-001", "reference")):
            for poison in ({"expected": "SECRET_GOLD"}, "SECRET_GOLD"):
                fixture = copy.deepcopy(self.fixtures[fixture_id])
                fixture["premises"][field] = [poison]
                with self.assertRaises((ValueError, TypeError)):
                    render_research_prompt(fixture)
        fixture = copy.deepcopy(self.fixtures["flash-dev-001"])
        fixture["premises"]["blocks"][0]["values"] = [[{"expected": "SECRET_GOLD"}]]
        with self.assertRaises(ValueError):
            render_research_prompt(fixture)


if __name__ == "__main__":
    unittest.main()
