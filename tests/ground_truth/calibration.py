"""Public, exact synthetic calibration checks. Standard library only.

This module never reads a fixture's expected answer while solving or rendering it.
All numeric calculations are over unbounded rationals, not a bounded world sample.
"""

from __future__ import annotations

import argparse
from collections import deque
from fractions import Fraction
import json
from pathlib import Path
import re
from typing import Any


SCHEMA_VERSION = "ground-truth-v0.1"
DEFAULT_FIXTURES = Path(__file__).resolve().parents[2] / "data/ground_truth/calibration_fixtures.json"
_RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")
_NAME = re.compile(r"[A-Za-z][A-Za-z0-9_-]*\Z")
_FIXTURE_KEYS = {
    "fixture_id", "candidate_id", "split", "family_id", "world_id", "mechanism",
    "premises", "target", "expected", "verifier_id", "prerequisites",
}


def _keys(value: Any, required: set[str], optional: set[str] | None = None) -> None:
    if not isinstance(value, dict) or not required <= value.keys() or value.keys() - required - (optional or set()):
        raise ValueError(f"Expected keys {sorted(required)}; optional {sorted(optional or set())}")


def _rational(value: Any) -> Fraction:
    if not isinstance(value, str) or _RATIONAL.fullmatch(value) is None:
        raise ValueError("Rationals must be integer or numerator/positive-denominator strings")
    return Fraction(value)


def _names(values: Any, *, nonempty: bool = False) -> list[str]:
    if not isinstance(values, list) or (nonempty and not values):
        raise ValueError("Expected a list of names")
    if any(not isinstance(v, str) or _NAME.fullmatch(v) is None for v in values):
        raise ValueError("Names must be simple identifiers")
    if len(set(values)) != len(values):
        raise ValueError("Duplicate name")
    return values


def _bit(value: Any) -> bool:
    return type(value) is int and value in (0, 1)


def _read_json(path: Path) -> Any:
    def unique_pairs(pairs: list[tuple[str, Any]]) -> dict:
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    def invalid_constant(value: str) -> None:
        raise ValueError(f"Nonstandard JSON numeric constant: {value}")

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs,
                      parse_constant=invalid_constant)


def _offset_system(premises: dict, target: dict) -> tuple[list[str], list[list[Fraction]], list[Fraction], list[Fraction], Fraction]:
    """Compile every visible reading/anchor and the queried affine functional."""
    _keys(premises, {"objects", "instruments", "offset_scope", "readings"}, {"known_offsets"})
    _keys(target, {"coefficients", "constant"})
    objects = _names(premises["objects"])
    instruments = _names(premises["instruments"])
    scope = premises["offset_scope"]
    if scope not in ("instrument", "reading"):
        raise ValueError("offset_scope must be instrument or reading")
    readings = premises["readings"]
    if not isinstance(readings, list):
        raise ValueError("readings must be a list")
    variables = ["object:" + name for name in objects]
    variables += (["offset:" + name for name in instruments] if scope == "instrument"
                  else ["reading_offset:" + str(i) for i in range(len(readings))])
    index = {v: i for i, v in enumerate(variables)}
    matrix, rhs = [], []
    for i, reading in enumerate(readings):
        _keys(reading, {"instrument", "object", "value"})
        if reading["instrument"] not in instruments or reading["object"] not in objects:
            raise ValueError("Reading names an undeclared instrument or object")
        row = [Fraction(0)] * len(variables)
        row[index["object:" + reading["object"]]] = Fraction(1)
        offset = "offset:" + reading["instrument"] if scope == "instrument" else "reading_offset:" + str(i)
        row[index[offset]] = Fraction(1)
        matrix.append(row)
        rhs.append(_rational(reading["value"]))
    anchors = premises.get("known_offsets", {})
    if not isinstance(anchors, dict) or (scope == "reading" and anchors):
        raise ValueError("known_offsets is an instrument-scope map")
    for instrument, value in anchors.items():
        if instrument not in instruments:
            raise ValueError("Anchor names an undeclared instrument")
        row = [Fraction(0)] * len(variables)
        row[index["offset:" + instrument]] = Fraction(1)
        matrix.append(row)
        rhs.append(_rational(value))
    coefficients = target["coefficients"]
    if not isinstance(coefficients, dict) or any(name not in objects for name in coefficients):
        raise ValueError("Target coefficients must name declared true object values")
    query = [Fraction(0)] * len(variables)
    for name, value in coefficients.items():
        query[index["object:" + name]] = _rational(value)
    return variables, matrix, rhs, query, _rational(target["constant"])


def _rref(matrix: list[list[Fraction]], rhs: list[Fraction], width: int) -> tuple[list[list[Fraction]], list[Fraction], list[list[Fraction]], list[int]]:
    """Gaussian elimination, carrying row-operation weights for certificates."""
    rows = [row[:] + [b] for row, b in zip(matrix, rhs)]
    transform = [[Fraction(i == j) for j in range(len(rows))] for i in range(len(rows))]
    pivots: list[int] = []
    next_row = 0
    for col in range(width):
        pivot = next((r for r in range(next_row, len(rows)) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[next_row], rows[pivot] = rows[pivot], rows[next_row]
        transform[next_row], transform[pivot] = transform[pivot], transform[next_row]
        divisor = rows[next_row][col]
        rows[next_row] = [v / divisor for v in rows[next_row]]
        transform[next_row] = [v / divisor for v in transform[next_row]]
        for r in range(len(rows)):
            if r == next_row:
                continue
            multiple = rows[r][col]
            rows[r] = [v - multiple * p for v, p in zip(rows[r], rows[next_row])]
            transform[r] = [v - multiple * p for v, p in zip(transform[r], transform[next_row])]
        pivots.append(col)
        next_row += 1
        if next_row == len(rows):
            break
    return [row[:width] for row in rows], [row[width] for row in rows], transform, pivots


def _dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def offset_audit(premises: dict, target: dict) -> dict:
    """Return the exact answer plus a separately checkable algebraic certificate."""
    variables, matrix, rhs, query, constant = _offset_system(premises, target)
    reduced, values, transform, pivots = _rref(matrix, rhs, len(variables))
    for i, (row, value) in enumerate(zip(reduced, values)):
        if not any(row) and value:
            return {"answer": {"status": "INCONSISTENT", "value": None},
                    "certificate": {"kind": "contradiction", "weights": list(map(str, transform[i]))}}
    particular = [Fraction(0)] * len(variables)
    for i, col in enumerate(pivots):
        particular[col] = values[i]
    for free in set(range(len(variables))) - set(pivots):
        direction = [Fraction(0)] * len(variables)
        direction[free] = Fraction(1)
        for i, col in enumerate(pivots):
            direction[col] = -reduced[i][free]
        if _dot(query, direction):
            other = [v + d for v, d in zip(particular, direction)]
            return {"answer": {"status": "UNKNOWN", "value": None},
                    "certificate": {"kind": "two_worlds", "variables": variables,
                                    "worlds": [list(map(str, particular)), list(map(str, other))]}}
    weights = [Fraction(0)] * len(matrix)
    for i, col in enumerate(pivots):
        weights = [v + query[col] * w for v, w in zip(weights, transform[i])]
    return {"answer": {"status": "IDENTIFIED", "value": str(_dot(query, particular) + constant)},
            "certificate": {"kind": "row_combination", "weights": list(map(str, weights)),
                            "variables": variables, "world": list(map(str, particular))}}


def solve_offset(premises: dict, target: dict) -> dict:
    return offset_audit(premises, target)["answer"]


def verify_offset_certificate(premises: dict, target: dict, answer: dict, certificate: dict) -> bool:
    """Check raw equations/witnesses, without calling Gaussian elimination.

    A row combination proves identification. Two exact satisfying worlds prove
    uncertainty. A nonzero linear combination 0 = b proves inconsistency.
    """
    variables, matrix, rhs, query, constant = _offset_system(premises, target)
    try:
        _keys(answer, {"status", "value"})
        if answer["status"] == "UNKNOWN":
            _keys(certificate, {"kind", "variables", "worlds"})
            if answer["value"] is not None or certificate["kind"] != "two_worlds" or certificate["variables"] != variables:
                return False
            worlds = certificate["worlds"]
            if not isinstance(worlds, list) or len(worlds) != 2 or any(not isinstance(w, list) or len(w) != len(variables) for w in worlds):
                return False
            parsed = [[_rational(v) for v in world] for world in worlds]
            return (all(_dot(row, world) == value for world in parsed for row, value in zip(matrix, rhs))
                    and _dot(query, parsed[0]) != _dot(query, parsed[1]))
        if answer["status"] == "IDENTIFIED":
            _keys(certificate, {"kind", "weights", "variables", "world"})
            if certificate["variables"] != variables:
                return False
            world = certificate["world"]
            if not isinstance(world, list) or len(world) != len(variables):
                return False
            world = [_rational(v) for v in world]
            if not all(_dot(row, world) == value for row, value in zip(matrix, rhs)):
                return False
        else:
            _keys(certificate, {"kind", "weights"})
        weights = certificate["weights"]
        if not isinstance(weights, list) or len(weights) != len(matrix):
            return False
        weights = [_rational(v) for v in weights]
        combination = [sum((w * row[col] for w, row in zip(weights, matrix)), Fraction(0))
                       for col in range(len(variables))]
        combined_rhs = _dot(weights, rhs)
        if answer["status"] == "INCONSISTENT":
            return (answer["value"] is None and certificate["kind"] == "contradiction"
                    and not any(combination) and bool(combined_rhs))
        if answer["status"] == "IDENTIFIED":
            return (certificate["kind"] == "row_combination" and combination == query
                    and _rational(answer["value"]) == combined_rhs + constant)
        return False
    except (ValueError, TypeError, KeyError):
        return False


def _badge_graph(premises: dict, target: dict) -> tuple[dict, tuple[str, int]]:
    _keys(premises, {"rooms", "doors", "start"})
    _keys(target, {"room", "badge"})
    rooms = _names(premises["rooms"], nonempty=True)
    start = premises["start"]
    if not isinstance(start, list) or len(start) != 2 or start[0] not in rooms or not _bit(start[1]):
        raise ValueError("start must be [declared_room, integer_bit]")
    if target["room"] not in rooms or not (_bit(target["badge"]) or target["badge"] == "any"):
        raise ValueError("Invalid goal room or badge")
    graph = {(room, bit): [] for room in rooms for bit in (0, 1)}
    if not isinstance(premises["doors"], list):
        raise ValueError("doors must be a list")
    for door in premises["doors"]:
        _keys(door, {"from", "to", "requires", "toggle"})
        if door["from"] not in rooms or door["to"] not in rooms:
            raise ValueError("Door names an undeclared room")
        if not (_bit(door["requires"]) or door["requires"] == "any") or type(door["toggle"]) is not bool:
            raise ValueError("Door requires integer 0/1 or any, and a boolean toggle")
        for bit in (0, 1):
            if door["requires"] == "any" or door["requires"] == bit:
                graph[door["from"], bit].append((door["to"], bit ^ int(door["toggle"])))
    return graph, tuple(start)


def _goal(state: tuple[str, int], target: dict) -> bool:
    return state[0] == target["room"] and (target["badge"] == "any" or state[1] == target["badge"])


def solve_badge(premises: dict, target: dict) -> dict:
    """BFS over full states; the returned shortest path is only one exemplar."""
    graph, start = _badge_graph(premises, target)
    queue = deque([start])
    parent = {start: None}
    while queue:
        state = queue.popleft()
        if _goal(state, target):
            path = []
            while state is not None:
                path.append(list(state))
                state = parent[state]
            path.reverse()
            return {"status": "REACHABLE", "distance": len(path) - 1, "path": path}
        for neighbor in graph[state]:
            if neighbor not in parent:
                parent[neighbor] = state
                queue.append(neighbor)
    return {"status": "UNREACHABLE", "distance": None, "path": None}


def solve_fixture(fixture: dict) -> dict:
    mechanism = fixture.get("mechanism")
    if mechanism == "additive_offsets":
        return solve_offset(fixture["premises"], fixture["target"])
    if mechanism == "badge_navigation":
        return solve_badge(fixture["premises"], fixture["target"])
    raise ValueError("Unknown mechanism")


def verify_response(fixture: dict, response: Any) -> bool:
    """Accept exact numeric answers or any legal shortest state path.

    Responses are decoded dictionaries, with exact keys and types. Malformed
    outputs return False; malformed fixture specifications raise ValueError.
    """
    answer = solve_fixture(fixture)
    try:
        if fixture["mechanism"] == "additive_offsets":
            _keys(response, {"status", "value"})
            if response["status"] != answer["status"]:
                return False
            if answer["status"] == "IDENTIFIED":
                return _rational(response["value"]) == _rational(answer["value"])
            return response["value"] is None
        _keys(response, {"status", "distance", "path"})
        if response["status"] != answer["status"]:
            return False
        if answer["status"] == "UNREACHABLE":
            return response["distance"] is None and response["path"] is None
        if type(response["distance"]) is not int or response["distance"] != answer["distance"]:
            return False
        path = response["path"]
        if not isinstance(path, list) or len(path) != response["distance"] + 1:
            return False
        graph, start = _badge_graph(fixture["premises"], fixture["target"])
        for state in path:
            if not isinstance(state, list) or len(state) != 2 or not isinstance(state[0], str) or not _bit(state[1]):
                return False
            if tuple(state) not in graph:
                return False
        states = [tuple(state) for state in path]
        return (states[0] == start and _goal(states[-1], fixture["target"])
                and all(b in graph[a] for a, b in zip(states, states[1:])))
    except (ValueError, TypeError, KeyError):
        return False


def load_fixtures(path: str | Path | None = None) -> list[dict]:
    payload = _read_json(Path(path or DEFAULT_FIXTURES))
    _keys(payload, {"schema_version", "fixtures"})
    if payload["schema_version"] != SCHEMA_VERSION or not isinstance(payload["fixtures"], list):
        raise ValueError("Unsupported calibration file schema")
    ids, worlds = set(), set()
    fixtures = payload["fixtures"]
    for fixture in fixtures:
        _keys(fixture, _FIXTURE_KEYS)
        for field in ("fixture_id", "candidate_id", "split", "family_id", "world_id", "mechanism", "verifier_id"):
            if not isinstance(fixture[field], str) or not fixture[field]:
                raise ValueError(f"Invalid {field}")
        if fixture["split"] != "calibration":
            raise ValueError("This public fixture file contains calibration only")
        required = {"additive_offsets": ("synthetic-offset", "exact-rational-offset-v1"),
                    "badge_navigation": ("synthetic-badge", "exact-badge-bfs-v1")}.get(fixture["mechanism"])
        if required is None or (fixture["candidate_id"], fixture["verifier_id"]) != required:
            raise ValueError("Candidate/verifier does not match mechanism")
        if fixture["fixture_id"] in ids or fixture["world_id"] in worlds:
            raise ValueError("Fixture and world IDs must be unique")
        ids.add(fixture["fixture_id"])
        worlds.add(fixture["world_id"])
        if not isinstance(fixture["prerequisites"], list) or any(not isinstance(v, str) for v in fixture["prerequisites"]):
            raise ValueError("prerequisites must be fixture ID strings")
        if len(set(fixture["prerequisites"])) != len(fixture["prerequisites"]):
            raise ValueError("Duplicate prerequisite")
        if not verify_response(fixture, fixture["expected"]):
            raise ValueError(f"Incorrect expected answer: {fixture['fixture_id']}")
    by_id = {fixture["fixture_id"]: fixture for fixture in fixtures}
    for fixture in fixtures:
        for prerequisite in fixture["prerequisites"]:
            if prerequisite not in by_id or prerequisite == fixture["fixture_id"]:
                raise ValueError("Unknown or self-referential prerequisite")
            if by_id[prerequisite]["prerequisites"]:
                raise ValueError("Prerequisite probes must be standalone fresh contexts")
            if by_id[prerequisite]["candidate_id"] != fixture["candidate_id"]:
                raise ValueError("Prerequisite belongs to another mechanism")
    return fixtures


def render_prompt(fixture: dict, condition: str = "premises_only") -> str:
    """Render only validated premises, target, and a declared mechanism cue.

    Metadata, expected answers, certificates, and prerequisite results are never
    inserted. Run each probe separately; no conversation state is carried here.
    """
    condition = {"unguided": "premises_only", "bridge": "minimal_bridge", "control": "irrelevant"}.get(condition, condition)
    if condition not in {"premises_only", "minimal_bridge", "irrelevant", "wrong_bridge"}:
        raise ValueError("Unknown prompt condition")
    premises, target = fixture["premises"], fixture["target"]
    if fixture["mechanism"] == "additive_offsets":
        _offset_system(premises, target)
        scope = ("Each instrument adds one unknown fixed offset to all its readings."
                 if premises["offset_scope"] == "instrument"
                 else "Each reading has its own unknown additive offset, even readings by the same instrument.")
        parts = ["True object values and offsets are unbounded rational numbers.", scope,
                 "Available fact A: (x + b) - (y + b) = x - y when both terms use the same additive offset b; different unknown offsets cannot be cancelled this way.",
                 "Available fact B: (x - y) + (y - z) = x - z.",
                 "Declared objects: " + ", ".join(premises["objects"]) + ".",
                 "Declared instruments: " + ", ".join(premises["instruments"]) + "."]
        for instrument, value in premises.get("known_offsets", {}).items():
            parts.append(f"The offset of {instrument} is known to equal {value}.")
        for reading in premises["readings"]:
            parts.append(f"{reading['instrument']} reads {reading['object']} = {reading['value']} (true value plus the applicable offset).")
        terms = [f"({coefficient}) * {name}" for name, coefficient in target["coefficients"].items()]
        terms.append(f"({target['constant']})")
        parts.append("Find " + " + ".join(terms) + ".")
        parts.append('Return JSON with exactly status and value: IDENTIFIED with an exact rational string if this target is equal in every consistent world; UNKNOWN with null if consistent worlds give different target values; INCONSISTENT with null if no world satisfies all facts.')
        cues = {"minimal_bridge": "Compare readings made with the same fixed offset before combining comparisons.",
                "irrelevant": "A paragraph can contain several sentences, and a sentence can contain several words.",
                "wrong_bridge": "Treat readings made by different instruments as though their unknown offsets were equal."}
    elif fixture["mechanism"] == "badge_navigation":
        _badge_graph(premises, target)
        parts = ["Rooms: " + ", ".join(premises["rooms"]) + ".",
                 "Your badge is a bit (0 or 1). All listed doors are directed; no other moves exist. Check a door's badge requirement before moving, then toggle the badge after moving if specified. Each move costs one.",
                 "Available fact A: A lawful single step satisfies the listed requirement before the move; toggling changes bit b to 1 - b, and keeping leaves b unchanged.",
                 "Available fact B: A route is valid exactly when every consecutive move is lawful; a shortest route minimizes its number of unit-cost moves.",
                 f"Start in {premises['start'][0]} with badge {premises['start'][1]}."]
        for door in premises["doors"]:
            requirement = "either badge" if door["requires"] == "any" else f"badge {door['requires']}"
            action = "toggle" if door["toggle"] else "keep"
            parts.append(f"Door {door['from']} -> {door['to']} requires {requirement}; {action} the badge.")
        goal_badge = "either badge" if target["badge"] == "any" else f"badge {target['badge']}"
        parts.append(f"Reach {target['room']} with {goal_badge} in the fewest moves.")
        parts.append('Return JSON with exactly status, distance, and path: REACHABLE with an integer distance and a shortest path of [room, badge] states including the start and goal; UNREACHABLE with null distance and null path.')
        cues = {"minimal_bridge": "Search over (room, badge) states; revisiting a room with another badge can matter.",
                "irrelevant": "A paragraph can contain several sentences, and a sentence can contain several words.",
                "wrong_bridge": "Mark each room visited the first time it is reached and never revisit it with another badge."}
    else:
        raise ValueError("Unknown mechanism")
    if condition != "premises_only":
        parts.append("Reasoning cue: " + cues[condition])
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check-fixtures", "solve", "render"))
    parser.add_argument("fixture_id", nargs="?")
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES)
    parser.add_argument("--condition", default="premises_only")
    args = parser.parse_args(argv)
    fixtures = load_fixtures(args.fixtures)
    if args.command == "check-fixtures":
        certificates = 0
        for fixture in fixtures:
            if fixture["mechanism"] == "additive_offsets":
                audit = offset_audit(fixture["premises"], fixture["target"])
                if not verify_offset_certificate(fixture["premises"], fixture["target"], **audit):
                    raise ValueError("Invalid generated certificate")
                certificates += 1
        print(json.dumps({"schema_version": SCHEMA_VERSION, "fixtures_checked": len(fixtures), "offset_certificates_checked": certificates}))
        return 0
    fixture = next((f for f in fixtures if f["fixture_id"] == args.fixture_id), None)
    if fixture is None:
        parser.error("solve/render requires a known fixture_id")
    if args.command == "render":
        print(render_prompt(fixture, args.condition))
    elif fixture["mechanism"] == "additive_offsets":
        print(json.dumps(offset_audit(fixture["premises"], fixture["target"]), indent=2))
    else:
        print(json.dumps(solve_fixture(fixture), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
