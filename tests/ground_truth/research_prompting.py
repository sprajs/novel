"""Research-side prompt handoff and grounded DPO development transfer guards."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json

from artifact_tools import DATA, build_prompt_record, check_donor_pair, read_json
from research_verifiers import solve_fixture, visible_prompt


def load_research_fixtures():
    return {f["fixture_id"]: f for f in read_json(DATA / "research_fixtures.json")["fixtures"]}


def render_research_prompt(fixture, condition="premises_only", *, diagnostic=False):
    """No oracle calls in ordinary arms; explicitly opt in to answer diagnostics."""
    if condition == "answer_only":
        if not diagnostic:
            raise ValueError("answer_only requires diagnostic=True")
        treatment = json.dumps(solve_fixture(fixture), sort_keys=True)
    elif condition == "premises_only":
        treatment = ""
    elif condition == "generic_reasoning":
        treatment = "Check the assumptions and your calculations carefully."
    else:
        treatment = fixture["condition_text"][condition]
    return build_prompt_record(visible_prompt(fixture), condition, treatment, diagnostic=diagnostic)


def dpo_answer_key(fixture):
    """Derive the concrete answer equivalence from premises, ignoring stored gold."""
    if fixture["verifier_id"] != "dpo_exact":
        raise ValueError("this equivalence rule is only defined for the DPO task")
    result = solve_fixture(fixture)
    if result["status"] != "VALID":
        raise ValueError("uncertainty/inapplicability belongs to a guardrail stratum")
    return "dpo-probability:" + str(Fraction(result["preference_probability"]))


def validate_transfer_examples(fixtures=None, record=None):
    fixtures = load_research_fixtures() if fixtures is None else fixtures
    record = read_json(DATA / "transfer_examples.json") if record is None else record
    errors = []
    for pair in record["pairs"]:
        donor = fixtures[pair["donor_fixture_id"]]
        recipient = fixtures[pair["recipient_fixture_id"]]
        donor_key, recipient_key = dpo_answer_key(donor), dpo_answer_key(recipient)
        errors.extend(check_donor_pair(donor, recipient, donor_key, recipient_key))
        for label, computed in (("donor_answer_key", donor_key), ("recipient_answer_key", recipient_key)):
            if pair[label] != computed:
                errors.append(pair["pair_id"] + ": stale or fabricated " + label)
        if pair["structural_holdout"] and donor["family_id"] == recipient["family_id"]:
            errors.append(pair["pair_id"] + ": falsely declared structural holdout")
        for fixture_id in pair["guardrail_fixture_ids"]:
            if fixture_id not in fixtures:
                errors.append(pair["pair_id"] + ": missing guardrail fixture")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture_id")
    parser.add_argument("--condition", default="premises_only", choices=["premises_only", "minimal_bridge", "alternate_bridge", "wrong_bridge", "irrelevant", "generic_reasoning", "answer_only"])
    parser.add_argument("--diagnostic", action="store_true")
    args = parser.parse_args()
    record = render_research_prompt(load_research_fixtures()[args.fixture_id], args.condition, diagnostic=args.diagnostic)
    print(json.dumps(record, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
