"""Public TaskInput v1 export and separate exact evaluation, no model execution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from artifact_tools import CUE, DATA, VERSION, digest, read_json, strict_json
import calibration
import meanflow_verifier
import research_verifiers
from research_prompting import render_research_prompt

INFRASTRUCTURE_REVISION = "c5a361363de8bb08aacc5119f1f435a847ad44d3"
TASK_KEYS = {"schema_version", "item_id", "world_id", "family_id", "lineage_id", "split", "condition", "prompt"}


def fixtures_for(collection):
    if collection == "calibration":
        return calibration.load_fixtures()
    if collection == "research":
        return read_json(DATA / "research_fixtures.json")["fixtures"]
    if collection == "meanflow":
        return meanflow_verifier.load_fixtures()
    raise ValueError("unknown collection")


def export_task(fixture, condition="premises_only"):
    """Only metadata permitted by sibling TaskInput plus projected public text."""
    if fixture["split"] == "calibration":
        split = "mechanics"
        prompt = calibration.render_prompt(fixture, condition) + "\n\n" + CUE
    elif fixture["split"] == "development":
        split = "development"
        prompt = (meanflow_verifier.render_prompt(fixture, condition)["text"]
                  if fixture["candidate_id"] == "meanflow"
                  else render_research_prompt(fixture, condition)["text"])
    else:
        raise ValueError("public exporter rejects confirmation and unknown native splits")
    return {
        "schema_version": 1,
        "item_id": fixture["fixture_id"] + "--" + condition,
        "world_id": fixture["world_id"],
        "family_id": fixture["family_id"],
        "lineage_id": fixture.get("template_lineage") or fixture["family_id"],
        "split": split,
        "condition": condition,
        "prompt": prompt,
    }


def evaluator_index(collections=("calibration", "research", "meanflow")):
    index = {}
    for collection in collections:
        for fixture in fixtures_for(collection):
            if fixture["world_id"] in index:
                raise ValueError("world_id ambiguous for evaluator; use item-specific mapping before export")
            index[fixture["world_id"]] = fixture
    return index


def evaluate_raw(world_id, raw_text, index=None):
    """Strictly parse one JSON answer; do not strip fences or repair outputs.

    Return a grading record only after generation. Verifier exceptions propagate
    as specification failures and must stop interpretation, not count as errors
    made by a model. The caller retains unmodified raw text and token IDs.
    """
    index = evaluator_index() if index is None else index
    fixture = index[world_id]
    synthetic = fixture["candidate_id"].startswith("synthetic-")
    module = (calibration if synthetic else meanflow_verifier
              if fixture["candidate_id"] == "meanflow" else research_verifiers)
    fixture_bytes = json.dumps(fixture, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    result = {
        "world_id": world_id,
        "fixture_id": fixture["fixture_id"],
        "verifier_id": fixture["verifier_id"],
        "verifier_version": VERSION,
        "verifier_sha256": digest(Path(module.__file__).read_bytes()),
        "fixture_sha256": digest(fixture_bytes),
        "fixture_hash_encoding": "sorted_keys_compact_utf8_json",
        "parse_valid": False,
        "correct": False,
        "status": "INVALID_OUTPUT",
        "failure_reason": "malformed_json",
        "audit_status": "not_applicable" if synthetic else "pending",
    }
    try:
        parsed = strict_json(raw_text)
    except (ValueError, TypeError):
        return result
    if not isinstance(parsed, dict):
        result["failure_reason"] = "answer_is_not_object"
        return result
    result["parse_valid"] = True
    result["status"] = parsed.get("status") if isinstance(parsed.get("status"), str) else "INVALID_OUTPUT"
    result["correct"] = (research_verifiers.verify_fixture(fixture, parsed)
                         if module is research_verifiers else module.verify_response(fixture, parsed))
    result["failure_reason"] = None if result["correct"] else "verifier_rejected_answer_or_shape"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    export = subparsers.add_parser("export")
    export.add_argument("--collection", choices=("calibration", "research", "meanflow"), required=True)
    export.add_argument("--condition", choices=("premises_only", "minimal_bridge", "wrong_bridge", "irrelevant"), default="premises_only")
    evaluate = subparsers.add_parser("evaluate")
    evaluate.add_argument("world_id")
    evaluate.add_argument("--response-file", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "export":
        for fixture in fixtures_for(args.collection):
            print(json.dumps(export_task(fixture, args.condition), ensure_ascii=False, allow_nan=False))
    else:
        print(json.dumps(evaluate_raw(args.world_id, args.response_file.read_text(encoding="utf-8")), sort_keys=True))


if __name__ == "__main__":
    main()
