import copy
import json
import unittest

from infrastructure_adapter import (TASK_KEYS, evaluate_raw, evaluator_index,
                                    export_task, fixtures_for)
from research_verifiers import solve_fixture


class InfrastructureHandoffTests(unittest.TestCase):
    def test_exact_public_keys_native_split_mapping_and_stable_ids(self):
        ids = set()
        for collection, split in (("calibration", "mechanics"), ("research", "development"), ("meanflow", "development")):
            for fixture in fixtures_for(collection):
                for condition in ("premises_only", "minimal_bridge", "irrelevant", "wrong_bridge"):
                    record = export_task(fixture, condition)
                    self.assertEqual(TASK_KEYS, set(record))
                    self.assertEqual(1, record["schema_version"])
                    self.assertEqual(split, record["split"])
                    self.assertNotIn(record["item_id"], ids)
                    ids.add(record["item_id"])
                    self.assertLessEqual(len(record["prompt"].encode()), 65536)
                    self.assertTrue(record["prompt"].endswith("Continue with the requested response."))
        self.assertEqual(len(ids), 4 * sum(len(fixtures_for(c)) for c in ("calibration", "research", "meanflow")))

    def test_export_does_not_serialize_gold_or_historical_audit(self):
        for collection in ("calibration", "research", "meanflow"):
            fixture = copy.deepcopy(fixtures_for(collection)[0])
            original = export_task(fixture)
            fixture["expected"] = {"status": "SECRET_GOLD"}
            fixture["historical_audit"] = "SECRET_GOLD"
            self.assertEqual(original, export_task(fixture))
            fixture["split"] = "confirmation"
            with self.assertRaises(ValueError):
                export_task(fixture)

    def test_raw_evaluator_preserves_unknown_and_rejects_copied_answer(self):
        index = evaluator_index()
        fixture = next(f for f in index.values() if f["fixture_id"] == "dpo-dev-003")
        correct = evaluate_raw(fixture["world_id"], json.dumps(solve_fixture(fixture)), index)
        self.assertTrue(correct["correct"])
        self.assertEqual("UNKNOWN", correct["status"])
        self.assertEqual("pending", correct["audit_status"])
        self.assertEqual(64, len(correct["verifier_sha256"]))
        wrong = evaluate_raw(fixture["world_id"], '{"status":"VALID","preference_probability":"16/97","odds":"16/81"}', index)
        self.assertFalse(wrong["correct"])

    def test_raw_evaluator_does_not_repair_ambiguous_or_embellished_json(self):
        index = evaluator_index()
        fixture = next(f for f in index.values() if f["fixture_id"] == "offset-plan-chain")
        good = '{"status":"IDENTIFIED","value":"9"}'
        self.assertTrue(evaluate_raw(fixture["world_id"], good, index)["correct"])
        for bad in ('```json\n' + good + '\n```', '{"status":"UNKNOWN","status":"IDENTIFIED","value":"9"}', '{"status":"IDENTIFIED","value":NaN}', good + ' explanation', '[]'):
            result = evaluate_raw(fixture["world_id"], bad, index)
            self.assertFalse(result["parse_valid"])
            self.assertFalse(result["correct"])

    def test_meanflow_dispatch_uses_its_own_oracle(self):
        import meanflow_verifier
        fixture = fixtures_for("meanflow")[0]
        response = json.dumps(meanflow_verifier.solve_fixture(fixture))
        result = evaluate_raw(fixture["world_id"], response)
        self.assertTrue(result["correct"])
        self.assertEqual(meanflow_verifier.VERIFIER_ID, result["verifier_id"])


if __name__ == "__main__":
    unittest.main()
