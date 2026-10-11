"""Exact, local oracles for exposed research development fixtures.

No source lookup, model call, floating-point tolerance, or expected-label access.
These finite checks do not establish historical novelty or grade arbitrary proofs.
"""

from fractions import Fraction
import json
from math import isqrt


def rational(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise ValueError("Use integers or rational strings, never floats/bools")
    return Fraction(value)


def vector(values):
    return [rational(value) for value in values]


def distribution(values):
    result = vector(values)
    if not result or any(x < 0 for x in result) or sum(result) != 1:
        raise ValueError("A distribution must be nonnegative and sum to one")
    return result


def rational_sqrt(value):
    if value < 0:
        raise ValueError("Negative square")
    num, den = isqrt(value.numerator), isqrt(value.denominator)
    if num * num != value.numerator or den * den != value.denominator:
        raise ValueError("Irrational norm is outside this exact verifier subfamily")
    return Fraction(num, den)


def encode(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, list):
        return [encode(item) for item in value]
    return value


def dpo(premises):
    q = distribution(premises["reference"])
    pi = distribution(premises["policy"])
    if len(q) != len(pi):
        raise ValueError("Mismatched action alphabets")
    beta = premises["beta"]
    if isinstance(beta, bool) or not isinstance(beta, int) or beta <= 0:
        raise ValueError("The exact fixture subfamily uses positive integer beta")
    if type(premises["same_context"]) is not bool:
        raise ValueError("same_context must be a boolean")
    pair = premises["pair"]
    if not isinstance(pair, list) or len(pair) != 2 or any(type(i) is not int for i in pair):
        raise ValueError("Pair needs two integer action indices")
    a, b = pair
    if not (0 <= a < len(pi) and 0 <= b < len(pi)) or a == b:
        raise ValueError("Pair needs two distinct valid action indices")
    if any(x <= 0 for x in q + pi):
        return {"status": "INAPPLICABLE", "reason": "positive_support_required"}
    if not premises["same_context"]:
        return {"status": "UNKNOWN", "reason": "relative_reward_offset_missing"}
    # Direct strength substitution is independent of a log-odds derivation.
    strength_a = (pi[a] / q[a]) ** beta
    strength_b = (pi[b] / q[b]) ** beta
    return {"status": "VALID", "preference_probability": strength_a / (strength_a + strength_b),
            "odds": strength_a / strength_b}


def speculative(premises):
    p = distribution(premises["target_distribution"])
    q = distribution(premises["actual_proposal"])
    scores = distribution(premises.get("reported_proposal", premises["actual_proposal"]))
    if len(p) != len(q) or len(q) != len(scores):
        raise ValueError("Mismatched symbol alphabets")
    if any(qi > 0 and si == 0 for qi, si in zip(q, scores)):
        return {"status": "INAPPLICABLE", "reason": "undefined_acceptance_ratio"}
    acceptance = [min(Fraction(1), pi / si) if qi else None
                  for pi, qi, si in zip(p, q, scores)]
    accepted = [qi * ai if qi else Fraction(0) for qi, ai in zip(q, acceptance)]
    rejection = 1 - sum(accepted)
    residual_mass = [max(pi - si, Fraction(0)) for pi, si in zip(p, scores)]
    total_residual = sum(residual_mass)
    if rejection and not total_residual:
        return {"status": "INAPPLICABLE", "reason": "fallback_undefined_on_reachable_branch"}
    residual = [x / total_residual for x in residual_mass] if total_residual else None
    output = [mass + rejection * ri for mass, ri in zip(accepted, residual)] if residual else accepted
    return {"status": "VALID", "acceptance": acceptance, "rejection_probability": rejection,
            "residual": residual, "output": output, "target_equal": output == p}


def dora_derivative(premises):
    v, h = vector(premises["v"]), vector(premises["dv"])
    if len(v) != len(h) or not v:
        raise ValueError("Direction and perturbation must have matching positive dimensions")
    m, mu = rational(premises["m"]), rational(premises["dm"])
    if m <= 0:
        raise ValueError("This fixture convention requires positive magnitude")
    squared_norm = sum(x * x for x in v)
    if not squared_norm:
        return {"status": "UNDEFINED", "reason": "zero_direction"}
    norm = rational_sqrt(squared_norm)
    unit = [x / norm for x in v]
    projection = sum(ui * hi for ui, hi in zip(unit, h))
    mode = premises["derivative_mode"]
    if mode == "ordinary":
        derivative = [mu * ui + m / norm * (hi - ui * projection) for ui, hi in zip(unit, h)]
    elif mode == "detached_denominator_autodiff":
        derivative = [mu * ui + m / norm * hi for ui, hi in zip(unit, h)]
    else:
        raise ValueError("Derivative semantics must be explicit")
    return {"status": "VALID", "dw": derivative,
            "radial_rate": sum(ui * dwi for ui, dwi in zip(unit, derivative))}


def dora_forward(premises):
    w0, b, a = [[vector(row) for row in premises[key]] for key in ("W0", "B", "A")]
    m = vector(premises["magnitudes"])
    rows, cols, rank = len(w0), len(m), len(a)
    if not rows or not cols or not rank or len(b) != rows or any(x <= 0 for x in m):
        raise ValueError("Invalid factor dimensions or magnitudes")
    if any(len(row) != cols for row in w0 + a) or any(len(row) != rank for row in b):
        raise ValueError("Invalid factor dimensions")
    v = [[w0[i][j] + sum(b[i][k] * a[k][j] for k in range(rank))
          for j in range(cols)] for i in range(rows)]
    norms = [rational_sqrt(sum(v[i][j] ** 2 for i in range(rows))) for j in range(cols)]
    if any(n == 0 for n in norms):
        return {"status": "UNDEFINED", "reason": "zero_direction"}
    weight = [[m[j] * v[i][j] / norms[j] for j in range(cols)] for i in range(rows)]
    return {"status": "VALID", "weight": weight,
            "column_norm_squares": [sum(weight[i][j] ** 2 for i in range(rows)) for j in range(cols)]}


def flashattention(premises):
    if "normalized_outputs_only" in premises:
        outputs = [vector(row) for row in premises["normalized_outputs_only"]]
        if not outputs or not outputs[0] or any(len(row) != len(outputs[0]) for row in outputs):
            raise ValueError("Invalid local outputs")
        if all(row == outputs[0] for row in outputs):
            return {"status": "VALID", "output": outputs[0]}
        return {"status": "UNKNOWN", "reason": "relative_block_masses_missing"}
    summaries = []
    width = None
    for block in premises["blocks"]:
        scores, values = block["score_exponents"], [vector(row) for row in block["values"]]
        masks = block.get("included", [True] * len(scores))
        if len(scores) != len(values) or len(scores) != len(masks):
            raise ValueError("Mismatched scores, values, or masks")
        if any(isinstance(k, bool) or not isinstance(k, int) for k in scores):
            raise ValueError("Score exponents must be integers")
        if any(not isinstance(mask, bool) for mask in masks):
            raise ValueError("Masks must be booleans")
        for value in values:
            if not value or (width is not None and len(value) != width):
                raise ValueError("Mismatched value dimensions")
            width = len(value)
        kept = [(k, val) for k, val, use in zip(scores, values, masks) if use]
        if not kept:
            continue
        maximum = max(k for k, _ in kept)
        weights = [Fraction(2) ** (k - maximum) for k, _ in kept]
        numerator = [sum(w * val[j] for w, (_, val) in zip(weights, kept)) for j in range(width)]
        summaries.append((maximum, sum(weights), numerator))
    if not summaries:
        return {"status": "UNDEFINED", "reason": "empty_attention_support"}
    maximum, denominator, numerator = summaries[0]
    for next_maximum, next_denominator, next_numerator in summaries[1:]:
        merged_maximum = max(maximum, next_maximum)
        left = Fraction(2) ** (maximum - merged_maximum)
        right = Fraction(2) ** (next_maximum - merged_maximum)
        denominator = left * denominator + right * next_denominator
        numerator = [left * x + right * y for x, y in zip(numerator, next_numerator)]
        maximum = merged_maximum
    return {"status": "VALID", "maximum_exponent": maximum,
            "denominator": denominator, "numerator": numerator,
            "output": [x / denominator for x in numerator]}


VERIFIERS = {"dpo_exact": dpo, "speculative_exact": speculative,
             "dora_derivative_exact": dora_derivative, "dora_forward_exact": dora_forward,
             "flashattention_exact": flashattention}


OBSERVATION_FIELDS = {
    "dpo_exact": ("reference", "policy", "beta", "same_context", "pair"),
    "speculative_exact": ("target_distribution", "actual_proposal", "reported_proposal"),
    "dora_derivative_exact": ("v", "dv", "m", "dm", "derivative_mode"),
    "dora_forward_exact": ("W0", "B", "A", "magnitudes"),
    "flashattention_exact": ("blocks", "normalized_outputs_only"),
}


def _numeric_payload(value):
    """Validate visible numeric leaves without solving the task or reading gold."""
    if isinstance(value, list):
        for item in value:
            _numeric_payload(item)
    elif type(value) in (int, str):
        rational(value)
    else:
        raise ValueError("Visible numeric fields cannot contain records or nonnumeric metadata")


def visible_prompt(fixture):
    """Convert through a strict allowlist to the shared visible-prompt contract.

    Call artifact_tools.build_prompt_record on this return value. Only the
    separately selected treatment belongs in a guided condition. Expected
    answers, candidate/source names, dependence metadata, and verifier IDs
    never become model text.
    """
    premises = fixture["premises"]
    fields = OBSERVATION_FIELDS[fixture["verifier_id"]]
    observations = []
    for key in fields:
        if key not in premises:
            continue
        value = premises[key]
        if key == "blocks":
            # Blocks are records too: an outer allowlist must not serialize
            # ignored nested evaluator fields into the model's observations.
            value = [{field: block[field] for field in ("score_exponents", "values", "included")
                      if field in block} for block in value]
            for block in value:
                for field in ("score_exponents", "values"):
                    _numeric_payload(block[field])
                if "included" in block and (not isinstance(block["included"], list)
                                            or any(type(mask) is not bool for mask in block["included"])):
                    raise ValueError("Visible masks must be boolean lists")
        elif key == "same_context":
            if type(value) is not bool:
                raise ValueError("same_context must be a boolean")
        elif key == "derivative_mode":
            if value not in ("ordinary", "detached_denominator_autodiff"):
                raise ValueError("Unknown derivative mode")
        else:
            _numeric_payload(value)
        observations.append(key + " = " + json.dumps(value, sort_keys=True))
    return {
        "task": "Solve the finite mathematical task from the supplied premises.",
        "premises_a": premises["prerequisite_A"],
        "premises_b": premises["prerequisite_B"],
        "observations": observations,
        "question": fixture["target"]["question"],
        "response_format": fixture["target"]["response_format"],
    }


def solve_fixture(fixture):
    """Compute from premises only; never consume fixture expected output."""
    return encode(VERIFIERS[fixture["verifier_id"]](fixture["premises"]))


def same_answer(expected, submitted):
    """Compare the structured result while allowing equivalent rational spelling."""
    if isinstance(expected, dict):
        return (isinstance(submitted, dict) and expected.keys() == submitted.keys()
                and all(same_answer(value, submitted[key]) for key, value in expected.items()))
    if isinstance(expected, list):
        return (isinstance(submitted, list) and len(expected) == len(submitted)
                and all(same_answer(x, y) for x, y in zip(expected, submitted)))
    if isinstance(expected, str):
        try:
            value = rational(expected)
        except (ValueError, ZeroDivisionError):
            return type(submitted) is str and expected == submitted
        try:
            return value == rational(submitted)
        except (ValueError, TypeError, ZeroDivisionError):
            return False
    return type(expected) is type(submitted) and expected == submitted


def verify_fixture(fixture, submitted):
    return same_answer(solve_fixture(fixture), submitted)
