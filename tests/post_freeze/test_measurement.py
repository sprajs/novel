"""Exact toy probabilities and fixed-n zero-success calculations; no inference."""

from fractions import Fraction
import math
import unittest

from validate_admission import DATA, ROOT, read_json


class MeasurementExamples(unittest.TestCase):
    def setUp(self):
        self.fixture = read_json(DATA / "finite_measurement.json")
        self.rows = self.fixture["trajectories"]

    def prefix_mass(self, prefixes):
        return sum((Fraction(row["probability"]) for row in self.rows
                    if any(row["tokens"][:len(prefix)] == prefix for prefix in prefixes)),
                   Fraction(0))

    def test_law_is_fully_enumerated_with_distinct_stopped_trajectories(self):
        self.assertFalse(self.fixture["model_evaluated"])
        self.assertTrue(self.fixture["development_only"])
        self.assertTrue((ROOT / self.fixture["protocol_ref"]).is_file())
        self.assertEqual(1, sum(Fraction(row["probability"]) for row in self.rows))
        self.assertEqual(len(self.rows), len({tuple(row["tokens"]) for row in self.rows}))
        self.assertTrue(all(row["tokens"][-1] == "EOS" for row in self.rows))

    def test_exact_path_mass_differs_from_semantic_target_and_validity_mass(self):
        exact = next(Fraction(row["probability"]) for row in self.rows
                     if row["tokens"] == self.fixture["canonical_target_tokens"])
        target = sum(Fraction(row["probability"]) for row in self.rows if row["target_recovery"])
        valid = sum(Fraction(row["probability"]) for row in self.rows if row["scientifically_valid"])
        self.assertEqual(Fraction("1/100"), exact)
        self.assertEqual(Fraction("3/10"), target)
        self.assertEqual(Fraction("11/20"), valid)
        for actual, key in ((exact, "expected_exact_path_mass"),
                            (target, "expected_target_event_mass"),
                            (valid, "expected_valid_event_mass")):
            self.assertEqual(actual, Fraction(self.fixture[key]))

    def test_incomplete_prefixes_overlap_and_cannot_be_summed(self):
        prefixes = self.fixture["overlapping_prefixes"]
        summed = sum(self.prefix_mass([prefix]) for prefix in prefixes)
        union = self.prefix_mass(prefixes)
        self.assertEqual(Fraction("11/100"), summed)
        self.assertEqual(Fraction(self.fixture["expected_prefix_union_mass"]), union)
        self.assertGreater(summed, union)

    def test_candidate_normalization_and_average_scores_are_different_quantities(self):
        probabilities = [Fraction(row["probability"]) for row in self.rows if row["target_recovery"]]
        target_mass = sum(probabilities)
        self.assertEqual(Fraction("1/10"), target_mass / len(probabilities))
        self.assertNotEqual(target_mass, target_mass / len(probabilities))
        self.assertEqual(Fraction("1/30"), probabilities[0] / target_mass)
        self.assertNotEqual(probabilities[0], probabilities[0] / target_mass)
        normalized_path_score = math.exp(math.log(float(probabilities[0])) /
                                         len(self.fixture["canonical_target_tokens"]))
        self.assertNotAlmostEqual(float(target_mass), normalized_path_score)
        self.assertNotAlmostEqual(float(probabilities[0]), normalized_path_score)

    def test_enumerated_complete_paths_give_a_lower_bound_without_an_upper_bound(self):
        target = [row for row in self.rows if row["target_recovery"]]
        subset = sum(Fraction(row["probability"]) for row in target[:2])
        full = sum(Fraction(row["probability"]) for row in target)
        self.assertEqual(Fraction("1/10"), subset)
        self.assertEqual(Fraction("3/10"), full)
        self.assertLess(subset, full)
        # Repeating a selected token path does not create another disjoint event.
        deduplicated = {tuple(row["tokens"]): Fraction(row["probability"])
                        for row in target[:2] + target[:1]}
        self.assertEqual(subset, sum(deduplicated.values()))

    def test_zero_success_bounds_follow_fixed_independent_trial_inversion(self):
        fixture = self.fixture["zero_success_examples"]
        alpha = float(Fraction(fixture["nominal_error"]))
        for n in fixture["sample_counts"]:
            upper = -math.expm1(math.log(alpha) / n)
            self.assertAlmostEqual(fixture[f"expected_upper_{n}"], upper, places=14)
            self.assertAlmostEqual(alpha, (1 - upper) ** n, places=14)
            self.assertGreater(upper, 0)
        needed = math.ceil(math.log(alpha) / math.log1p(-0.01))
        self.assertEqual(299, needed)
        self.assertGreater(fixture["expected_upper_64"], 0.01)
        self.assertLess(fixture["expected_upper_299"], 0.01)

    def test_twelve_event_simultaneous_claim_has_a_wider_bound(self):
        fixture = self.fixture["zero_success_examples"]
        per_event_error = float(Fraction(fixture["nominal_error"])) / fixture["simultaneous_event_count"]
        upper = -math.expm1(math.log(per_event_error) / 64)
        self.assertAlmostEqual(fixture["expected_simultaneous_upper_64"], upper, places=14)
        self.assertGreater(upper, fixture["expected_upper_64"])
        self.assertAlmostEqual(0.05, per_event_error * 12)


if __name__ == "__main__":
    unittest.main()
