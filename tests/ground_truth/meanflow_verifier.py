"""Exact MeanFlow calculus probes; no model calls, response code, or gold lookup.

Endpoint evaluation and integration of the polynomial derivative are separate
routes. Finite examples do not prove a universal theorem or historical novelty.
"""

from fractions import Fraction
import json
from pathlib import Path

VERSION = "ground-truth-v0.1"
VERIFIER_ID = "meanflow-polynomial-exact-v1"
DEFAULT_FIXTURES = Path(__file__).resolve().parents[2] / "data/ground_truth/meanflow_fixtures.json"
VALID_FIELDS = ("average_velocity", "instantaneous_velocity", "partial_time",
                "partial_state", "total_derivative", "identity_rhs",
                "displacement", "endpoint_r")


def rational(value):
    if type(value) not in (int, str):
        raise ValueError("Expected an integer or exact rational string")
    return Fraction(value)


def strict_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON key")
            result[key] = value
        return result
    def bad_constant(value):
        raise ValueError("Nonfinite JSON constant")
    return json.loads(text, object_pairs_hook=pairs, parse_constant=bad_constant)


def polynomial_endpoint(coefficients, time):
    """Horner evaluation of the explicit position polynomial."""
    value = Fraction(0)
    for coefficient in reversed(coefficients):
        value = value * time + coefficient
    return value


def integrated_velocity(coefficients, r, t):
    """Differentiate position coefficients, then integrate each velocity term."""
    velocity_coefficients = [degree * coefficient
                             for degree, coefficient in enumerate(coefficients)][1:]
    return sum((coefficient * (t ** (degree + 1) - r ** (degree + 1)) / (degree + 1)
                for degree, coefficient in enumerate(velocity_coefficients)), Fraction(0))


def _world(premises):
    family = premises["flow_family"]
    r, t = rational(premises["r"]), rational(premises["t"])
    rho = rational(premises.get("lower_time_rate", "0"))
    if r > t:
        raise ValueError("This subfamily requires r <= t")
    if family == "quadratic_time_field":
        coefficients = [rational(premises[key]) for key in ("a", "b", "c")]
    elif family == "positive_square_field":
        shift = rational(premises["shift"])
        coefficients = [shift ** 2, 2 * shift, Fraction(1)]
    else:
        raise ValueError("Unknown flow family")
    return family, coefficients, r, t, rho


def solve_fixture(fixture):
    """Compute from premises only; fixture expected labels are never consulted."""
    if fixture["verifier_id"] != VERIFIER_ID:
        raise ValueError("Unknown verifier")
    family, coefficients, r, t, rho = _world(fixture["premises"])
    if family == "positive_square_field":
        shift = rational(fixture["premises"]["shift"])
        if shift + r <= 0 or shift + t <= 0:
            return {"status": "INAPPLICABLE", "reason": "positive_branch_required"}
    a, b, c = coefficients
    zr = polynomial_endpoint(coefficients, r)
    zt = polynomial_endpoint(coefficients, t)
    displacement = zt - zr
    integral = integrated_velocity(coefficients, r, t)
    if displacement != integral:
        raise ArithmeticError("Endpoint and integrated-velocity routes disagree")
    v, vr = b + 2 * c * t, b + 2 * c * r
    # The quotient is undefined at the diagonal; explicitly use its C1 extension.
    average = displacement / (t - r) if t != r else v
    if family == "quadratic_time_field":
        partial_time, partial_state, partial_lower = c, Fraction(0), c
    else:
        partial_time, partial_lower = Fraction(-1), Fraction(1)
        partial_state = 1 / (rational(fixture["premises"]["shift"]) + t)
    total = partial_time + v * partial_state + rho * partial_lower
    # A second derivative route differentiates b+c*(r(t)+t) along the path.
    if total != c * (1 + rho):
        raise ArithmeticError("Field chain rule and trajectory derivative disagree")
    # For moving r, both sides of the generalized Leibniz equation must agree.
    if (1 - rho) * average + (t - r) * total != v - rho * vr:
        raise ArithmeticError("Generalized moving-boundary identity failed")
    rhs = v - (t - r) * total
    result = {"status": "VALID", "average_velocity": average,
              "instantaneous_velocity": v, "partial_time": partial_time,
              "partial_state": partial_state, "total_derivative": total,
              "identity_rhs": rhs, "identity_holds": average == rhs,
              "displacement": displacement, "endpoint_r": zr}
    return {key: str(value) if isinstance(value, Fraction) else value
            for key, value in result.items()}


def verify_response(fixture, submitted):
    """Accept exact equivalent rationals; reject wrong shape, floats and booleans."""
    expected = solve_fixture(fixture)
    try:
        if isinstance(submitted, str):
            submitted = strict_json(submitted)
        if not isinstance(submitted, dict) or set(submitted) != set(expected):
            return False
        for key, value in expected.items():
            if key in VALID_FIELDS:
                if rational(submitted[key]) != rational(value):
                    return False
            elif type(submitted[key]) is not type(value) or submitted[key] != value:
                return False
        return True
    except (ValueError, TypeError, KeyError, ZeroDivisionError):
        return False


def load_fixtures(path=DEFAULT_FIXTURES):
    payload = strict_json(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != VERSION or not isinstance(payload.get("fixtures"), list):
        raise ValueError("Unknown fixture collection version or shape")
    ids, worlds = set(), set()
    for fixture in payload["fixtures"]:
        for key in ("fixture_id", "family_id", "world_id"):
            if not isinstance(fixture[key], str) or not fixture[key]:
                raise ValueError("Missing fixture identity")
        if fixture["candidate_id"] != "meanflow" or fixture["split"] != "development":
            raise ValueError("Only public MeanFlow development fixtures are permitted")
        if fixture["fixture_id"] in ids or fixture["world_id"] in worlds:
            raise ValueError("Duplicate fixture or world")
        ids.add(fixture["fixture_id"])
        worlds.add(fixture["world_id"])
        if not isinstance(fixture["target"], dict):
            raise ValueError("Target must be a structured object")
        if not verify_response(fixture, fixture["expected"]):
            raise ValueError("Incorrect expected response: " + fixture["fixture_id"])
    return payload["fixtures"]


def visible_prompt(fixture):
    """Six-field contract; read only declared premise/target fields."""
    family, coefficients, r, t, rho = _world(fixture["premises"])
    p = fixture["premises"]
    if family == "quadratic_time_field":
        observations = [f"z(s)=a+b*s+c*s^2 with a={p['a']}, b={p['b']}, c={p['c']}.",
                        "For every endpoint, the flow field is v(z,s)=b+2*c*s."]
    else:
        observations = [f"z(s)=(k+s)^2 with k={p['shift']}.",
                        "The field is v(z,s)=2*sqrt(z); the intended trajectory requires k+s>0 over the whole interval."]
    observations += [f"Lower time r={p['r']}; upper time t={p['t']}; dr/dt={p.get('lower_time_rate', '0')} locally."]
    visible = {"task": "Analyze the average of a scalar velocity along the given trajectory.",
               "premises_a": p["prerequisite_A"], "premises_b": p["prerequisite_B"],
               "observations": observations, "question": fixture["target"]["question"],
               "response_format": fixture["target"]["response_format"]}
    return visible


def render_prompt(fixture, condition="premises_only"):
    """Use the common cue and named treatment through the shared renderer."""
    from artifact_tools import build_prompt_record
    treatment = "" if condition == "premises_only" else fixture["condition_text"][condition]
    return build_prompt_record(visible_prompt(fixture), condition, treatment)
