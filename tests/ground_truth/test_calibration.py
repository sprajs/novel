"""Analytical and independent checks for public calibration, never confirmation."""

import copy
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


_SPEC = importlib.util.spec_from_file_location("ground_truth_calibration", Path(__file__).with_name("calibration.py"))
calibration = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(calibration)


def offset_case(readings, coefficients, *, objects=None, scope="instrument", anchors=None, constant="0"):
    objects = objects if objects is not None else list(dict.fromkeys(o for _, o, _ in readings))
    premises = {"objects": objects, "instruments": list(dict.fromkeys(i for i, _, _ in readings)),
                "offset_scope": scope,
                "readings": [{"instrument": i, "object": o, "value": v} for i, o, v in readings]}
    if anchors is not None:
        premises["known_offsets"] = anchors
    return {"mechanism": "additive_offsets", "premises": premises,
            "target": {"coefficients": coefficients, "constant": constant}}


def graph_offset_answer(fixture):
    """Independent difference/potential method for fixed-instrument fixtures.

    Cancelling each instrument against its first observation creates object
    difference edges. Anchors connect to an independently fixed zero node.
    This method does not build the verifier's matrix or call its elimination.
    """
    premises, target = fixture["premises"], fixture["target"]
    if premises["offset_scope"] != "instrument":
        raise ValueError("This independent method requires fixed instrument offsets")
    zero = "__fixed_zero__"
    graph = {name: [] for name in premises["objects"] + [zero]}
    first = {}
    def edge(a, b, difference):
        graph[a].append((b, difference))
        graph[b].append((a, -difference))
    for reading in premises["readings"]:
        instrument, name, value = reading["instrument"], reading["object"], Fraction(reading["value"])
        if instrument in first:
            reference, reference_value = first[instrument]
            edge(reference, name, value - reference_value)
        else:
            first[instrument] = (name, value)
        if instrument in premises.get("known_offsets", {}):
            edge(zero, name, value - Fraction(premises["known_offsets"][instrument]))
    component, potential = {}, {}
    for root in graph:
        if root in component:
            continue
        component[root], potential[root] = root, Fraction(0)
        stack = [root]
        while stack:
            node = stack.pop()
            for neighbor, delta in graph[node]:
                proposed = potential[node] + delta
                if neighbor in potential:
                    if potential[neighbor] != proposed:
                        return {"status": "INCONSISTENT", "value": None}
                else:
                    component[neighbor], potential[neighbor] = root, proposed
                    stack.append(neighbor)
    totals = {}
    value = Fraction(target["constant"])
    for name, coefficient in target["coefficients"].items():
        coefficient = Fraction(coefficient)
        root = component[name]
        totals[root] = totals.get(root, Fraction(0)) + coefficient
        value += coefficient * (potential[name] - (potential[zero] if root == component[zero] else 0))
    if any(weight for root, weight in totals.items() if root != component[zero]):
        return {"status": "UNKNOWN", "value": None}
    return {"status": "IDENTIFIED", "value": str(value)}


def exhaustive_badge_distance(fixture):
    """Independent enumeration of simple state paths (at most eight states).

    A shortest path has no repeated full state. Revisiting a room with a new
    bit is allowed. This check reads door rules directly, without the BFS graph.
    """
    premises, target = fixture["premises"], fixture["target"]
    lengths = []
    def visit(state, seen):
        room, bit = state
        if room == target["room"] and (target["badge"] == "any" or bit == target["badge"]):
            lengths.append(len(seen) - 1)
            return
        for door in premises["doors"]:
            if door["from"] == room and door["requires"] in (bit, "any"):
                neighbor = (door["to"], 1 - bit if door["toggle"] else bit)
                if neighbor not in seen:
                    visit(neighbor, seen | {neighbor})
    start = tuple(premises["start"])
    visit(start, {start})
    return min(lengths) if lengths else None


class OffsetAnalyticalTests(unittest.TestCase):
    def assert_answer(self, fixture, status, value=None):
        expected = {"status": status, "value": value}
        audit = calibration.offset_audit(fixture["premises"], fixture["target"])
        self.assertEqual(audit["answer"], expected)
        self.assertTrue(calibration.verify_offset_certificate(fixture["premises"], fixture["target"], **audit))
        self.assertTrue(calibration.verify_response(fixture, expected))

    def test_plan_case_is_nine_not_raw_cross_instrument_difference(self):
        fixture = offset_case([("one", "A", "17"), ("one", "B", "11"),
                               ("two", "B", "25"), ("two", "C", "22")], {"A": "1", "C": "-1"})
        self.assert_answer(fixture, "IDENTIFIED", "9")
        self.assertFalse(calibration.verify_response(fixture, {"status": "IDENTIFIED", "value": "-5"}))

    def test_signed_chain_is_negative(self):
        fixture = offset_case([("i", "A", "2"), ("i", "B", "7"), ("j", "B", "4"), ("j", "C", "1")], {"A": "1", "C": "-1"})
        self.assert_answer(fixture, "IDENTIFIED", "-2")

    def test_absolute_value_and_unbalanced_sum_are_unknown(self):
        readings = [("i", "A", "8"), ("i", "B", "3")]
        self.assert_answer(offset_case(readings, {"A": "1"}), "UNKNOWN")
        self.assert_answer(offset_case(readings, {"A": "1", "B": "1"}), "UNKNOWN")

    def test_any_linear_functional_and_constant_are_supported(self):
        fixture = offset_case([("i", "A", "4"), ("i", "B", "1"), ("j", "C", "7"), ("j", "D", "2")],
                              {"A": "2", "B": "-2", "C": "-1", "D": "1"}, constant="1/2")
        self.assert_answer(fixture, "IDENTIFIED", "3/2")
        self.assertEqual(graph_offset_answer(fixture), calibration.solve_fixture(fixture))

    def test_global_zero_sum_is_insufficient_on_disconnected_components(self):
        fixture = offset_case([("i", "A", "4"), ("i", "B", "1"), ("j", "C", "7"), ("j", "D", "2")], {"A": "1", "C": "-1"})
        self.assert_answer(fixture, "UNKNOWN")

    def test_unobserved_objects_and_zero_functional(self):
        self.assert_answer(offset_case([], {"A": "1"}, objects=["A"]), "UNKNOWN")
        self.assert_answer(offset_case([], {}, objects=["A"], constant="-7/3"), "IDENTIFIED", "-7/3")
        self.assert_answer(offset_case([("i", "A", "3")], {"B": "0"}, objects=["A", "B"]), "IDENTIFIED", "0")

    def test_anchor_identifies_absolute_values(self):
        fixture = offset_case([("i", "A", "11"), ("i", "B", "6")], {"A": "1"}, anchors={"i": "2"})
        self.assert_answer(fixture, "IDENTIFIED", "9")
        self.assertEqual(graph_offset_answer(fixture), calibration.solve_fixture(fixture))

    def test_contradictory_cycle_overrides_even_constant_target(self):
        readings = [("i", "A", "6"), ("i", "B", "2"), ("j", "B", "8"), ("j", "C", "5"),
                    ("k", "A", "11"), ("k", "C", "5")]
        self.assert_answer(offset_case(readings, {}), "INCONSISTENT")
        self.assert_answer(offset_case(readings, {"A": "1", "C": "-1"}), "INCONSISTENT")

    def test_duplicate_reading_disagreement_is_inconsistent(self):
        self.assert_answer(offset_case([("i", "A", "1"), ("i", "A", "2")], {"A": "1"}), "INCONSISTENT")

    def test_per_reading_offsets_cannot_cancel(self):
        fixture = offset_case([("i", "A", "17"), ("i", "B", "11")], {"A": "1", "B": "-1"}, scope="reading")
        self.assert_answer(fixture, "UNKNOWN")
        # Even disagreeing repeats can be consistent when every offset is fresh.
        self.assert_answer(offset_case([("i", "A", "1"), ("i", "A", "2")], {"A": "1"}, scope="reading"), "UNKNOWN")

    def test_no_float_tolerance_swallows_tiny_difference(self):
        denominator = 10 ** 80
        fixture = offset_case([("i", "A", f"1/{denominator}"), ("i", "B", "0")], {"A": "1", "B": "-1"})
        self.assert_answer(fixture, "IDENTIFIED", f"1/{denominator}")
        self.assertFalse(calibration.verify_response(fixture, {"status": "IDENTIFIED", "value": "0"}))

    def test_tiny_inconsistency_is_still_inconsistent(self):
        fixture = offset_case([("i", "A", "0"), ("i", "A", "1/1000000000000000000000000000000")], {})
        self.assert_answer(fixture, "INCONSISTENT")

    def test_certificate_checker_rejects_forgery_without_using_solver(self):
        fixture = offset_case([("i", "A", "4"), ("i", "B", "1")], {"A": "1", "B": "-1"})
        audit = calibration.offset_audit(fixture["premises"], fixture["target"])
        forged = copy.deepcopy(audit)
        forged["certificate"]["weights"][0] = "0"
        self.assertFalse(calibration.verify_offset_certificate(fixture["premises"], fixture["target"], **forged))
        forged = copy.deepcopy(audit)
        forged["certificate"]["world"][0] = "999"
        self.assertFalse(calibration.verify_offset_certificate(fixture["premises"], fixture["target"], **forged))
        # A row combination alone cannot establish consistency on contradictory facts.
        impossible = offset_case([("i", "A", "1"), ("i", "A", "2")], {})
        cert = {"kind": "row_combination", "weights": ["0", "0"],
                "variables": ["object:A", "offset:i"], "world": ["1", "0"]}
        self.assertFalse(calibration.verify_offset_certificate(impossible["premises"], impossible["target"], {"status": "IDENTIFIED", "value": "0"}, cert))

    def test_unknown_witnesses_really_disagree(self):
        fixture = offset_case([("i", "A", "4")], {"A": "1"})
        audit = calibration.offset_audit(fixture["premises"], fixture["target"])
        bad = copy.deepcopy(audit)
        bad["certificate"]["worlds"][1] = bad["certificate"]["worlds"][0][:]
        self.assertFalse(calibration.verify_offset_certificate(fixture["premises"], fixture["target"], **bad))
        bad = copy.deepcopy(audit)
        bad["certificate"]["worlds"][0][0] = "999"
        self.assertFalse(calibration.verify_offset_certificate(fixture["premises"], fixture["target"], **bad))

    def test_contradiction_certificate_needs_nonzero_rhs(self):
        fixture = offset_case([("i", "A", "1"), ("i", "A", "2")], {})
        self.assertFalse(calibration.verify_offset_certificate(fixture["premises"], fixture["target"],
            {"status": "INCONSISTENT", "value": None}, {"kind": "contradiction", "weights": ["0", "0"]}))


class BadgeAnalyticalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = {f["fixture_id"]: f for f in calibration.load_fixtures()}

    def test_revisit_room_with_new_bit_is_required(self):
        fixture = self.fixtures["badge-plan-revisit"]
        answer = calibration.solve_fixture(fixture)
        self.assertEqual(answer["distance"], 4)
        self.assertEqual(answer["path"], [["A", 0], ["B", 1], ["C", 0], ["A", 1], ["D", 1]])
        self.assertTrue(calibration.verify_response(fixture, answer))

    def test_an_alternative_shortest_path_is_accepted(self):
        fixture = self.fixtures["badge-plain-alternatives"]
        alternative = {"status": "REACHABLE", "distance": 2, "path": [["A", 0], ["C", 0], ["D", 0]]}
        self.assertNotEqual(alternative, fixture["expected"])
        self.assertTrue(calibration.verify_response(fixture, alternative))

    def test_legal_longer_path_is_rejected(self):
        fixture = copy.deepcopy(self.fixtures["badge-plain-alternatives"])
        fixture["premises"]["doors"].append({"from": "B", "to": "C", "requires": "any", "toggle": False})
        longer = {"status": "REACHABLE", "distance": 3, "path": [["A", 0], ["B", 0], ["C", 0], ["D", 0]]}
        self.assertFalse(calibration.verify_response(fixture, longer))

    def test_room_only_visited_set_would_lose_detour(self):
        answer = calibration.solve_fixture(self.fixtures["badge-state-detour"])
        self.assertEqual(answer["distance"], 3)
        self.assertEqual(answer["path"], [["S", 0], ["C", 1], ["B", 1], ["G", 1]])

    def test_requirement_is_checked_before_toggle(self):
        fixture = self.fixtures["badge-transition-probe"]
        self.assertEqual(calibration.solve_fixture(fixture)["distance"], 1)
        bad = {"status": "REACHABLE", "distance": 1, "path": [["A", 0], ["B", 0]]}
        self.assertFalse(calibration.verify_response(fixture, bad))

    def test_goal_badge_and_initial_goal_are_distinct(self):
        self.assertEqual(calibration.solve_fixture(self.fixtures["badge-goal-probe"])["status"], "UNREACHABLE")
        self.assertEqual(calibration.solve_fixture(self.fixtures["badge-start-is-goal"])["distance"], 0)
        cycle = calibration.solve_fixture(self.fixtures["badge-cycle-goal-bit"])
        self.assertEqual(cycle["distance"], 2)
        self.assertEqual(cycle["path"], [["A", 0], ["B", 0], ["A", 1]])

    def test_unreachable_cannot_be_claimed_reachable(self):
        fixture = self.fixtures["badge-gated-unreachable"]
        self.assertTrue(calibration.verify_response(fixture, {"status": "UNREACHABLE", "distance": None, "path": None}))
        self.assertFalse(calibration.verify_response(fixture, {"status": "REACHABLE", "distance": 1, "path": [["A", 0], ["D", 0]]}))


class FixtureAndFormatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = calibration.load_fixtures()

    def test_public_fixed_cohort_and_fresh_prerequisites(self):
        self.assertEqual(len(self.fixtures), 20)
        self.assertEqual(sum(f["mechanism"] == "additive_offsets" for f in self.fixtures), 12)
        by_id = {f["fixture_id"]: f for f in self.fixtures}
        self.assertEqual({f["split"] for f in self.fixtures}, {"calibration"})
        self.assertEqual(len({f["world_id"] for f in self.fixtures}), 20)
        for fixture in self.fixtures:
            for prerequisite in fixture["prerequisites"]:
                probe = by_id[prerequisite]
                self.assertFalse(probe["prerequisites"])
                self.assertNotEqual(probe["world_id"], fixture["world_id"])

    def test_every_fixed_offset_has_an_independently_checked_certificate(self):
        for fixture in self.fixtures:
            if fixture["mechanism"] == "additive_offsets":
                with self.subTest(fixture=fixture["fixture_id"]):
                    audit = calibration.offset_audit(fixture["premises"], fixture["target"])
                    self.assertEqual(audit["answer"], fixture["expected"])
                    self.assertTrue(calibration.verify_offset_certificate(fixture["premises"], fixture["target"], **audit))

    def test_independent_difference_graph_matches_all_fixed_instrument_cases(self):
        for fixture in self.fixtures:
            if fixture["mechanism"] == "additive_offsets" and fixture["premises"]["offset_scope"] == "instrument":
                with self.subTest(fixture=fixture["fixture_id"]):
                    self.assertEqual(graph_offset_answer(fixture), calibration.solve_fixture(fixture))

    def test_independent_simple_path_enumeration_matches_badge_bfs(self):
        for fixture in self.fixtures:
            if fixture["mechanism"] == "badge_navigation":
                with self.subTest(fixture=fixture["fixture_id"]):
                    self.assertEqual(exhaustive_badge_distance(fixture), calibration.solve_fixture(fixture)["distance"])

    def test_solver_and_renderer_do_not_consult_answers_or_metadata(self):
        for fixture in self.fixtures:
            changed = copy.deepcopy(fixture)
            changed["expected"] = {"secret": "EXPECTED_ANSWER_MARKER"}
            changed["fixture_id"] = "SECRET_ID"
            changed["prerequisites"] = ["SECRET_PREREQUISITE_RESULT"]
            self.assertEqual(calibration.solve_fixture(fixture), calibration.solve_fixture(changed))
            for condition in ("premises_only", "minimal_bridge", "irrelevant", "wrong_bridge"):
                self.assertEqual(calibration.render_prompt(fixture, condition), calibration.render_prompt(changed, condition))
                self.assertNotIn("SECRET", calibration.render_prompt(changed, condition))

    def test_primary_arms_have_identical_facts_and_bridge_no_target_answer(self):
        for fixture in self.fixtures:
            plain = calibration.render_prompt(fixture)
            bridge = calibration.render_prompt(fixture, "minimal_bridge")
            self.assertTrue(bridge.startswith(plain + "\nReasoning cue: "))
            self.assertIn("Available fact A:", plain)
            self.assertIn("Available fact B:", plain)
            cue = bridge[len(plain):]
            self.assertFalse(any(character.isdigit() for character in cue))
        self.assertEqual(calibration.render_prompt(self.fixtures[0], "bridge"), calibration.render_prompt(self.fixtures[0], "minimal_bridge"))
        self.assertEqual(calibration.render_prompt(self.fixtures[0], "unguided"), calibration.render_prompt(self.fixtures[0], "premises_only"))
        with self.assertRaises(ValueError):
            calibration.render_prompt(self.fixtures[0], "unknown")

    def test_shared_offset_facts_do_not_imply_per_reading_cancellation(self):
        fixture = next(f for f in self.fixtures if f["fixture_id"] == "offset-per-reading")
        prompt = calibration.render_prompt(fixture, "minimal_bridge")
        self.assertIn("Each reading has its own unknown additive offset", prompt)
        self.assertIn("when both terms use the same additive offset b", prompt)
        self.assertIn("different unknown offsets cannot be cancelled", prompt)
        self.assertEqual(calibration.solve_fixture(fixture), {"status": "UNKNOWN", "value": None})

    def test_irrelevant_control_is_true_and_unrelated_to_both_mechanisms(self):
        cue = "Reasoning cue: A paragraph can contain several sentences, and a sentence can contain several words."
        for fixture in self.fixtures:
            self.assertEqual(calibration.render_prompt(fixture, "irrelevant"), calibration.render_prompt(fixture) + "\n" + cue)

    def test_offset_outputs_have_strict_shapes_and_types(self):
        fixture = offset_case([("i", "A", "4"), ("i", "B", "1")], {"A": "1", "B": "-1"})
        valid = {"status": "IDENTIFIED", "value": "6/2"}
        self.assertTrue(calibration.verify_response(fixture, valid))
        malformed = [None, "3", {"status": "IDENTIFIED"}, {"status": "IDENTIFIED", "value": 3},
            {"status": "IDENTIFIED", "value": 3.0}, {"status": "IDENTIFIED", "value": True},
            {"status": "IDENTIFIED", "value": "3.0"}, {"status": "IDENTIFIED", "value": " 3"},
            {"status": "IDENTIFIED", "value": "3/0"}, {"status": "IDENTIFIED", "value": "-3/-1"},
            {"status": "IDENTIFIED", "value": "03"}, {"status": "identified", "value": "3"},
            {"status": "IDENTIFIED", "value": "3", "proof": "extra"},
            {"status": "UNKNOWN", "value": None}, {"status": "IDENTIFIED", "value": None}]
        for response in malformed:
            with self.subTest(response=response):
                self.assertFalse(calibration.verify_response(fixture, response))
        unknown = offset_case([("i", "A", "4")], {"A": "1"})
        self.assertFalse(calibration.verify_response(unknown, {"status": "UNKNOWN", "value": "null"}))

    def test_badge_outputs_have_strict_shapes_and_types(self):
        fixture = next(f for f in self.fixtures if f["fixture_id"] == "badge-transition-probe")
        valid = fixture["expected"]
        malformed = [None, "REACHABLE", {"status": "REACHABLE", "distance": 1},
            dict(valid, extra="x"), dict(valid, distance=True), dict(valid, distance=1.0),
            dict(valid, path=[["A", False], ["B", 1]]), dict(valid, path=[["A", 0], ["B", True]]),
            dict(valid, path=[("A", 0), ("B", 1)]), dict(valid, path=[["A", 0], ["B", 1, 2]]),
            dict(valid, path=[["A", 0], ["unknown", 1]]), dict(valid, path=[["B", 1], ["A", 0]]),
            dict(valid, path=[]), dict(valid, path=[["A", 0]]), dict(valid, path=None),
            {"status": "UNREACHABLE", "distance": None, "path": None}]
        for response in malformed:
            with self.subTest(response=response):
                self.assertFalse(calibration.verify_response(fixture, response))

    def test_fixture_load_rejects_wrong_gold_and_bad_references(self):
        payload = json.loads(calibration.DEFAULT_FIXTURES.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixtures.json"
            for modification in ("wrong_gold", "unknown_prerequisite", "noncalibration", "duplicate_world", "extra_field"):
                bad = copy.deepcopy(payload)
                if modification == "wrong_gold":
                    bad["fixtures"][0]["expected"]["value"] = "999"
                elif modification == "unknown_prerequisite":
                    bad["fixtures"][0]["prerequisites"] = ["missing"]
                elif modification == "noncalibration":
                    bad["fixtures"][0]["split"] = "confirmation"
                elif modification == "duplicate_world":
                    bad["fixtures"][1]["world_id"] = bad["fixtures"][0]["world_id"]
                else:
                    bad["fixtures"][0]["hidden_prompt"] = "not allowed"
                path.write_text(json.dumps(bad), encoding="utf-8")
                with self.subTest(modification=modification), self.assertRaises(ValueError):
                    calibration.load_fixtures(path)

    def test_fixture_load_rejects_duplicate_keys_and_nonstandard_json(self):
        text = calibration.DEFAULT_FIXTURES.read_text(encoding="utf-8")
        malformed = [
            '{"schema_version":"ground-truth-v0.1","schema_version":"ground-truth-v0.1","fixtures":[]}',
            text.replace('"value": "11"', '"value": "11", "value": "11"', 1),
            '{"schema_version":"ground-truth-v0.1","fixtures":NaN}',
            '{"schema_version":"ground-truth-v0.1","fixtures":Infinity}',
            text + " trailing text",
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixtures.json"
            for index, content in enumerate(malformed):
                path.write_text(content, encoding="utf-8")
                with self.subTest(index=index), self.assertRaises(ValueError):
                    calibration.load_fixtures(path)

    def test_malformed_visible_worlds_are_rejected(self):
        fixture = offset_case([("i", "A", "4")], {"A": "1"})
        fixture["premises"]["readings"][0]["value"] = 4.0
        with self.assertRaises(ValueError):
            calibration.solve_fixture(fixture)
        fixture = copy.deepcopy(next(f for f in self.fixtures if f["fixture_id"] == "badge-transition-probe"))
        fixture["premises"]["doors"][0]["requires"] = False
        with self.assertRaises(ValueError):
            calibration.solve_fixture(fixture)


if __name__ == "__main__":
    unittest.main()
