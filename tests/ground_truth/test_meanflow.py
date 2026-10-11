"""MeanFlow development checks: exact calculus, boundary semantics and leakage."""

import copy
from fractions import Fraction
import json
import unittest

from meanflow_verifier import (load_fixtures, polynomial_endpoint,
                              integrated_velocity, solve_fixture,
                              verify_response, visible_prompt, render_prompt)


class MeanFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = load_fixtures()
        cls.by_id = {fixture["fixture_id"]: fixture for fixture in cls.fixtures}

    def case(self, suffix):
        return copy.deepcopy(self.by_id["meanflow-dev-" + suffix])

    def test_all_hand_checked_development_labels(self):
        self.assertEqual(len(self.fixtures), 9)
        for fixture in self.fixtures:
            self.assertTrue(verify_response(fixture, fixture["expected"]))
            self.assertEqual(fixture["split"], "development")

    def test_endpoint_integral_and_factorized_routes_on_rational_grid(self):
        for a in (-2, 0, 3):
            for b in (-3, 0, 2):
                for c in (-2, 0, 1):
                    for r in (Fraction(-1), Fraction(0), Fraction(1, 2)):
                        for interval in (Fraction(1, 2), Fraction(2)):
                            t = r + interval
                            coefficients = [Fraction(a), Fraction(b), Fraction(c)]
                            endpoints = polynomial_endpoint(coefficients, t) - polynomial_endpoint(coefficients, r)
                            integral = integrated_velocity(coefficients, r, t)
                            factorized_average = b + c * (r + t)
                            self.assertEqual(endpoints, integral)
                            self.assertEqual(endpoints / interval, factorized_average)
                            fixture = self.case("001")
                            fixture["premises"].update(a=str(a), b=str(b), c=str(c), r=str(r), t=str(t))
                            answer = solve_fixture(fixture)
                            self.assertEqual(Fraction(answer["average_velocity"]), factorized_average)
                            self.assertTrue(answer["identity_holds"])

    def test_state_dependent_total_derivative_rejects_partial_only(self):
        fixture = self.case("004")
        answer = solve_fixture(fixture)
        self.assertEqual(answer["partial_time"], "-1")
        self.assertEqual(answer["partial_state"], "1/3")
        self.assertEqual(answer["total_derivative"], "1")
        wrong = dict(answer, total_derivative="-1", identity_rhs="8")
        self.assertFalse(verify_response(fixture, wrong))
        self.assertEqual(Fraction(answer["partial_time"]) + Fraction(answer["instantaneous_velocity"]) * Fraction(answer["partial_state"]), Fraction(1))

    def test_diagonal_is_continuous_extension_and_preserves_derivative(self):
        for suffix in ("003", "005"):
            answer = solve_fixture(self.case(suffix))
            self.assertEqual(answer["average_velocity"], answer["instantaneous_velocity"])
            self.assertEqual(answer["displacement"], "0")
            self.assertNotEqual(answer["total_derivative"], "0")
        # A diagonal observation alone does not distinguish partial from total.
        square = solve_fixture(self.case("005"))
        self.assertNotEqual(square["partial_time"], square["total_derivative"])

    def test_moving_lower_time_invalidates_unmodified_fixed_r_identity(self):
        answer = solve_fixture(self.case("008"))
        self.assertEqual(answer["total_derivative"], "3/2")
        self.assertEqual(answer["average_velocity"], "3")
        self.assertEqual(answer["identity_rhs"], "5/2")
        self.assertFalse(answer["identity_holds"])
        # (1-rho)*u + (t-r)*du/dt = v(t)-rho*v(r).
        self.assertEqual(Fraction(1, 2) * 3 + Fraction(3, 2), 4 - Fraction(1, 2) * 2)

    def test_local_identity_without_diagonal_boundary_is_insufficient(self):
        fixture = self.case("001")
        answer = solve_fixture(fixture)
        # u'=u+K/(t-r) satisfies the local identity but changes displacement.
        interval, constant = Fraction(2), Fraction(2)
        spurious_average = Fraction(answer["average_velocity"]) + constant / interval
        spurious_derivative = Fraction(answer["total_derivative"]) - constant / interval ** 2
        self.assertEqual(spurious_average, Fraction(answer["instantaneous_velocity"]) - interval * spurious_derivative)
        wrong = dict(answer, average_velocity=str(spurious_average), total_derivative=str(spurious_derivative), identity_rhs=str(spurious_average))
        self.assertFalse(verify_response(fixture, wrong))

    def test_incompatible_square_branch_is_not_a_valid_flow(self):
        fixture = self.case("007")
        self.assertEqual(solve_fixture(fixture), {"status": "INAPPLICABLE", "reason": "positive_branch_required"})
        self.assertFalse(verify_response(fixture, {"status": "UNDEFINED", "reason": "positive_branch_required"}))
        fixture["premises"].update(shift="0", r="0", t="1")
        self.assertEqual(solve_fixture(fixture)["status"], "INAPPLICABLE")

    def test_equivalent_exact_rationals_and_alternate_routes_are_accepted(self):
        fixture = self.case("002")
        answer = solve_fixture(fixture)
        answer["average_velocity"] = "9/9"
        answer["total_derivative"] = "6/4"
        answer["displacement"] = "8/6"
        self.assertTrue(verify_response(fixture, json.dumps(answer)))
        affine = solve_fixture(self.case("006"))
        self.assertEqual(affine["total_derivative"], "0")
        self.assertEqual(affine["average_velocity"], "-3")

    def test_response_shape_floats_booleans_and_duplicate_keys_fail(self):
        fixture = self.case("001")
        answer = solve_fixture(fixture)
        for value in (2.0, True, "NaN", "2/0"):
            wrong = dict(answer, average_velocity=value)
            self.assertFalse(verify_response(fixture, wrong))
        self.assertFalse(verify_response(fixture, dict(answer, explanation="extra")))
        self.assertFalse(verify_response(fixture, dict(answer, identity_holds=1)))
        duplicate = json.dumps(answer)[:-1] + ',"status":"VALID"}'
        self.assertFalse(verify_response(fixture, duplicate))

    def test_solver_and_renderer_do_not_consult_gold_or_unapproved_metadata(self):
        fixture = self.case("004")
        answer = solve_fixture(fixture)
        fixture["expected"] = {"secret": "GOLD_SECRET"}
        fixture["source_urls"] = ["https://example.invalid/SOURCE_SECRET"]
        fixture["premises"]["source_title"] = "PREMISE_SECRET"
        fixture["target"]["source_date"] = "TARGET_SECRET"
        self.assertEqual(solve_fixture(fixture), answer)
        visible = visible_prompt(fixture)
        self.assertEqual(set(visible), {"task", "premises_a", "premises_b", "observations", "question", "response_format"})
        serialized = json.dumps(visible)
        for secret in ("GOLD_SECRET", "SOURCE_SECRET", "PREMISE_SECRET", "TARGET_SECRET", "meanflow-dev-004"):
            self.assertNotIn(secret, serialized)
        baseline = render_prompt(fixture)
        bridge = render_prompt(fixture, "minimal_bridge")
        self.assertEqual(baseline["common_prefix_sha256"], bridge["common_prefix_sha256"])
        self.assertTrue(baseline["text"].endswith("Continue with the requested response."))

    def test_bad_world_input_fails_before_scoring(self):
        for key, value in (("c", True), ("t", 2.0), ("r", "3")):
            fixture = self.case("001")
            fixture["premises"][key] = value
            with self.assertRaises(ValueError):
                solve_fixture(fixture)

    def test_collection_obeys_common_fixture_schema(self):
        from artifact_tools import DATA, read_json, check_schema
        schema = read_json(DATA / "schema.json")
        collection = read_json(DATA / "meanflow_fixtures.json")
        self.assertEqual(check_schema(collection, schema["$defs"]["fixture_collection"], schema), [])


if __name__ == "__main__":
    unittest.main()
