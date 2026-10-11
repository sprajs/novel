"""Regression and independent-oracle checks for public development packets."""

import copy
from fractions import Fraction as F
import itertools
import json
from math import lcm
from pathlib import Path
import unittest

from research_verifiers import (dora_derivative, dora_forward, dpo, flashattention,
                                same_answer, solve_fixture, speculative, verify_fixture, visible_prompt)
from artifact_tools import build_prompt_record


ROOT = Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / "data/ground_truth/research_fixtures.json").read_text())
FIXTURES = {row["fixture_id"]: row for row in DATA["fixtures"]}


def count_distributions(total, width):
    for counts in itertools.product(range(total + 1), repeat=width):
        if sum(counts) == total:
            yield [F(value, total) for value in counts]


def uniform_grid_draws(probabilities):
    """A finite equally likely list with the specified exact categorical law."""
    size = lcm(*(p.denominator for p in probabilities))
    return [i for i, p in enumerate(probabilities) for _ in range(int(p * size))]


def enumerate_speculative(p, q):
    """Independent finite probability space; no call to the residual oracle.

    Solve p_i = accepted_i + rho*r_i for r_i, then explicitly enumerate
    proposal, threshold and fallback draws on rational grids.
    """
    a = [min(F(1), pi / qi) if qi else F(0) for pi, qi in zip(p, q)]
    accepted = [qi * ai for qi, ai in zip(q, a)]
    rho = 1 - sum(accepted)
    fallback = [(pi - ai) / rho for pi, ai in zip(p, accepted)] if rho else [F(1)] + [F(0)] * (len(p) - 1)
    proposals = uniform_grid_draws(q)
    fallbacks = uniform_grid_draws(fallback)
    threshold_count = lcm(*(ai.denominator for ai in a))
    counts = [0] * len(p)
    for proposed, u, rejected_draw in itertools.product(proposals, range(threshold_count), fallbacks):
        output = proposed if F(u, threshold_count) < a[proposed] else rejected_draw
        counts[output] += 1
    total = len(proposals) * threshold_count * len(fallbacks)
    return [F(count, total) for count in counts]


def quotient_differential(v, dv, m, dm, norm):
    """First-order coefficient matching from n(t)^2=sum v_i(t)^2.

    For each coordinate solve n*w=m*v at first order, independently of
    constructing a tangent-space projection matrix.
    """
    dn = sum(x * dx for x, dx in zip(v, dv)) / norm
    w = [m * x / norm for x in v]
    return [(dm * x + m * dx - wi * dn) / norm for x, dx, wi in zip(v, dv, w)]


def flat_attention(blocks):
    """Raw exact unblocked weights; does not call the block summarizer."""
    tokens = []
    for block in blocks:
        for k, val, included in zip(block["score_exponents"], block["values"],
                                    block.get("included", [True] * len(block["values"]))):
            if included:
                tokens.append((F(2) ** k, [F(x) for x in val]))
    total = sum(weight for weight, _ in tokens)
    return [sum(weight * val[j] for weight, val in tokens) / total
            for j in range(len(tokens[0][1]))]


class ResearchPacketTests(unittest.TestCase):
    def test_public_development_schema(self):
        self.assertEqual(DATA["schema_version"], "ground-truth-v0.1")
        self.assertEqual(DATA["historical_admission"], "none")
        self.assertEqual(len(FIXTURES), len(DATA["fixtures"]))
        self.assertEqual({f["candidate_id"] for f in FIXTURES.values()},
                         {"dpo", "speculative-decoding", "dora", "flashattention"})
        for fixture in FIXTURES.values():
            self.assertEqual(fixture["split"], "development")
            for field in ("family_id", "world_id", "target", "expected", "verifier_id"):
                self.assertTrue(fixture[field])
            self.assertTrue(fixture["premises"]["prerequisite_A"])
            self.assertTrue(fixture["premises"]["prerequisite_B"])
            self.assertIsInstance(fixture["target"], dict)
            self.assertTrue(fixture["target"]["question"])
            self.assertTrue(fixture["target"]["response_format"])
            self.assertEqual(set(fixture["condition_text"]),
                             {"minimal_bridge", "alternate_bridge", "wrong_bridge", "irrelevant"})

    def test_renderer_preserves_primary_premises_and_excludes_metadata(self):
        for fixture in FIXTURES.values():
            visible = visible_prompt(fixture)
            plain = build_prompt_record(visible)
            guided = build_prompt_record(visible, "minimal_bridge", fixture["condition_text"]["minimal_bridge"])
            self.assertEqual(plain["common_prefix_sha256"], guided["common_prefix_sha256"])
            for prerequisite in ("prerequisite_A", "prerequisite_B"):
                self.assertIn(fixture["premises"][prerequisite], plain["text"])
                self.assertIn(fixture["premises"][prerequisite], guided["text"])
            altered = copy.deepcopy(fixture)
            for key in ("expected", "candidate_id", "family_id", "world_id", "case_kind", "sources"):
                altered[key] = "SECRET_EVALUATOR_VALUE"
            altered["premises"]["secret"] = "SECRET_EVALUATOR_VALUE"
            altered["target"]["secret"] = "SECRET_EVALUATOR_VALUE"
            if "blocks" in altered["premises"]:
                for block in altered["premises"]["blocks"]:
                    block["expected"] = "SECRET_EVALUATOR_VALUE"
                    block["nested_metadata"] = {"gold": "SECRET_EVALUATOR_VALUE"}
            self.assertEqual(visible_prompt(altered), visible)
            self.assertNotIn("SECRET_EVALUATOR_VALUE", plain["text"])

    def test_reason_codes_are_visible_and_counterfactuals_recorded(self):
        for fixture in FIXTURES.values():
            if "reason" in fixture["expected"]:
                self.assertIn(fixture["expected"]["reason"], visible_prompt(fixture)["response_format"])
        self.assertEqual(FIXTURES["dpo-dev-006"]["counterfactual_parent_id"], FIXTURES["dpo-dev-001"]["world_id"])
        self.assertEqual(FIXTURES["dora-dev-003"]["counterfactual_parent_id"], FIXTURES["dora-dev-002"]["world_id"])

    def test_all_handcrafted_labels(self):
        for fixture in FIXTURES.values():
            with self.subTest(fixture=fixture["fixture_id"]):
                self.assertEqual(solve_fixture(fixture), fixture["expected"])
                self.assertTrue(verify_fixture(fixture, fixture["expected"]))

    def test_oracles_do_not_read_expected(self):
        for fixture in FIXTURES.values():
            altered = copy.deepcopy(fixture)
            altered["expected"] = {"status": "BOGUS"}
            self.assertEqual(solve_fixture(altered), fixture["expected"])
            self.assertFalse(verify_fixture(fixture, altered["expected"]))

    def test_equivalent_fractions_and_bad_answers(self):
        original = FIXTURES["dpo-dev-001"]
        equivalent = {"status": "VALID", "preference_probability": "32/194", "odds": "32/162"}
        self.assertTrue(verify_fixture(original, equivalent))
        for wrong in ("81/97", "1/2", "0", "0/0", True, 16 / 97):
            candidate = dict(equivalent, preference_probability=wrong)
            self.assertFalse(verify_fixture(original, candidate))
        self.assertFalse(same_answer({"status": "UNKNOWN"}, {"status": "unknown"}))
        self.assertFalse(same_answer({"target_equal": True}, {"target_equal": 1}))
        self.assertFalse(same_answer({"status": "VALID"}, {"status": "VALID", "extra": 1}))

    def test_dpo_strengths_against_cross_product_odds(self):
        positive = [p for p in count_distributions(5, 3) if all(p)]
        for pi, q, beta in itertools.product(positive, positive, (1, 2, 3)):
            p = dict(policy=pi, reference=q, beta=beta, same_context=True, pair=[0, 2])
            answer = dpo(p)
            left = (pi[0] * q[2]) ** beta
            right = (pi[2] * q[0]) ** beta
            self.assertEqual(answer["preference_probability"], left / (left + right))
            reverse = dpo(dict(p, pair=[2, 0]))
            self.assertEqual(answer["preference_probability"] + reverse["preference_probability"], 1)

    def test_dpo_wrong_reference_or_temperature_fails(self):
        fixture = FIXTURES["dpo-dev-001"]
        for change in (dict(reference=["1/3"] * 3), dict(beta=1)):
            changed = dict(fixture["premises"], **change)
            self.assertNotEqual(dpo(changed)["preference_probability"], F(16, 97))
        for change in (dict(same_context="false"), dict(pair=[True, 2]), dict(pair=[0, 99])):
            with self.assertRaises(ValueError):
                dpo(dict(fixture["premises"], **change))

    def test_dpo_cross_context_is_not_identified(self):
        # Two legal reward normalizers preserve pi and q independently.
        # Multiplying only context A's exp(reward) by 2 changes cross-context odds.
        base_odds = F(16, 81)
        self.assertNotEqual(base_odds / (1 + base_odds), 2 * base_odds / (1 + 2 * base_odds))
        self.assertEqual(solve_fixture(FIXTURES["dpo-dev-003"])["status"], "UNKNOWN")

    def test_speculative_against_explicit_finite_enumeration(self):
        distributions = list(count_distributions(4, 3))
        for p, q in itertools.product(distributions, repeat=2):
            answer = speculative(dict(target_distribution=p, actual_proposal=q))
            self.assertEqual(answer["output"], enumerate_speculative(p, q))
            self.assertEqual(answer["output"], p)
            self.assertEqual(sum(answer["output"]), 1)

    def test_speculative_wrong_fallback_and_stale_scores_fail(self):
        p, q = [F(1, 3), F(1, 6), F(1, 2)], [F(1, 2), F(1, 3), F(1, 6)]
        accepted = [min(x, y) for x, y in zip(p, q)]
        rho = 1 - sum(accepted)
        wrong = [x + rho * pi for x, pi in zip(accepted, p)]
        self.assertEqual(wrong, [F(4, 9), F(2, 9), F(1, 3)])
        self.assertNotEqual(wrong, p)
        answer = solve_fixture(FIXTURES["spec-dev-004"])
        self.assertFalse(answer["target_equal"])
        self.assertEqual(answer["output"], ["3/8", "5/8"])

    def test_speculative_zero_rejection_and_missing_support(self):
        self.assertIsNone(solve_fixture(FIXTURES["spec-dev-003"])["residual"])
        self.assertIsNone(solve_fixture(FIXTURES["spec-dev-002"])["acceptance"][1])
        with self.assertRaises(ValueError):
            speculative(dict(target_distribution=["1/4", "1/4"], actual_proposal=["1/2", "1/2"]))

    def test_dora_derivative_against_quotient_expansion(self):
        for scale, m, dm, dx, dy in itertools.product((F(1, 2), F(1), F(3)), (F(2), F(10)),
                                                    (F(-2), F(0), F(3)), range(-2, 3), range(-2, 3)):
            v, dv = [3 * scale, 4 * scale], [F(dx), F(dy)]
            answer = dora_derivative(dict(v=v, dv=dv, m=m, dm=dm, derivative_mode="ordinary"))
            self.assertEqual(answer["dw"], quotient_differential(v, dv, m, dm, 5 * scale))
            self.assertEqual(answer["radial_rate"], dm)

    def test_dora_detachment_is_not_the_function_derivative(self):
        ordinary = solve_fixture(FIXTURES["dora-dev-002"])
        detached = solve_fixture(FIXTURES["dora-dev-003"])
        self.assertEqual(ordinary["dw"], ["0", "0"])
        self.assertEqual(detached["dw"], ["12", "16"])
        self.assertFalse(verify_fixture(FIXTURES["dora-dev-003"], ordinary))

    def test_dora_forward_and_effective_rank_counterexample(self):
        p = copy.deepcopy(FIXTURES["dora-dev-006"]["premises"])
        p["magnitudes"] = ["10", "10"]
        answer = dora_forward(p)
        w = answer["weight"]
        delta = [[w[i][j] - F(p["W0"][i][j]) for j in range(2)] for i in range(2)]
        # BA is rank one; the effective update has nonzero determinant.
        self.assertEqual(delta[0][0] * delta[1][1] - delta[0][1] * delta[1][0], 30)
        self.assertEqual(answer["column_norm_squares"], [F(100), F(100)])
        with self.assertRaises(ValueError):
            dora_derivative(dict(v=[1, 1], dv=[1, 0], m=1, dm=0, derivative_mode="ordinary"))

    def test_flash_merge_against_flat_attention(self):
        scores = [-3, 0, 2, -1]
        values = [["1", "2"], ["-1", "3"], ["4", "0"], ["0", "-2"]]
        for order in itertools.permutations(range(4)):
            for boundary in range(1, 4):
                blocks = []
                for ids in (order[:boundary], order[boundary:]):
                    blocks.append(dict(score_exponents=[scores[i] for i in ids],
                                       values=[values[i] for i in ids]))
                answer = flashattention(dict(blocks=blocks))
                self.assertEqual(answer["output"], flat_attention(blocks))
                shifted = [dict(block, score_exponents=[k + 20 for k in block["score_exponents"]]) for block in blocks]
                self.assertEqual(flashattention(dict(blocks=shifted))["output"], answer["output"])
        blocks = FIXTURES["flash-dev-002"]["premises"]["blocks"]
        self.assertEqual(flashattention(dict(blocks=blocks))["output"], flat_attention(blocks))

    def test_flash_missing_mass_countermodels_and_wrong_merge(self):
        # Same observed local outputs (0,1), incompatible global results.
        self.assertNotEqual(F(1, 2), F(3, 4))
        self.assertEqual(solve_fixture(FIXTURES["flash-dev-003"])["status"], "UNKNOWN")
        valid = flashattention(FIXTURES["flash-dev-001"]["premises"])
        wrong = [(F(1, 3) + 2) / 2, (F(2, 3) + 3) / 2]
        self.assertEqual(wrong, [F(7, 6), F(11, 6)])
        self.assertNotEqual(valid["output"], wrong)
        self.assertEqual(solve_fixture(FIXTURES["flash-dev-004"])["status"], "UNDEFINED")
        self.assertEqual(solve_fixture(FIXTURES["flash-dev-005"])["output"], ["2", "-1"])

    def test_versioned_source_hash_records(self):
        record = json.loads((ROOT / "docs/ground_truth/packets/source_snapshots.json").read_text())
        self.assertEqual(len(record["sources"]), 10)
        for source in record["sources"]:
            self.assertTrue(source["id"].endswith("v1"))
            self.assertTrue(source["url"].endswith(source["id"]))
            self.assertEqual(len(source["sha256"]), 64)
            int(source["sha256"], 16)
            self.assertGreater(source["bytes"], 0)


if __name__ == "__main__":
    unittest.main()
