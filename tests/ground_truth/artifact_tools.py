"""Offline research contracts, leakage guards, and byte-level inventory.

This file intentionally uses only the standard library and never invokes a model.
The schema checker supports only the assertions used by the bundled schema;
it is not a general implementation of JSON Schema Draft 2020-12.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "ground_truth"
VERSION = "ground-truth-v0.1"
OWNED = ("data/ground_truth", "docs/ground_truth", "tests/ground_truth")
BASE_REVISION = "36b7f6bff70f79642b1ab6d65e591c1b96a44738"
VISIBLE_KEYS = {"task", "premises_a", "premises_b", "observations", "question", "response_format"}
CONDITIONS = {"premises_only", "minimal_bridge", "alternate_bridge", "scaffold", "worked_example", "full_explanation", "wrong_bridge", "irrelevant", "answer_only", "generic_reasoning"}
CUE = "Continue with the requested response."


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_json(raw: str):
    """Reject repeated JSON keys and nonfinite constants rather than losing data."""
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError(f"nonfinite JSON constant: {value}")

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid_constant)


def read_json(path: Path):
    return strict_json(path.read_text(encoding="utf-8"))


def check_schema(value, spec, root_schema, location="$", errors=None):
    """Check the finite assertion vocabulary used by schema.json."""
    errors = [] if errors is None else errors
    if "$ref" in spec:
        ref = spec["$ref"]
        if not ref.startswith("#/$defs/"):
            raise ValueError(f"unsupported schema reference {ref}")
        return check_schema(value, root_schema["$defs"][ref.split("/")[-1]], root_schema, location, errors)
    if "anyOf" in spec:
        if not any(not check_schema(value, option, root_schema, location, []) for option in spec["anyOf"]):
            errors.append(f"{location}: no allowed shape matched")
        return errors
    types = {
        "object": lambda v: isinstance(v, dict),
        "array": lambda v: isinstance(v, list),
        "string": lambda v: isinstance(v, str),
        "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
        "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
        "boolean": lambda v: isinstance(v, bool),
        "null": lambda v: v is None,
    }
    if "type" in spec:
        allowed = spec["type"] if isinstance(spec["type"], list) else [spec["type"]]
        if not any(types[k](value) for k in allowed):
            errors.append(f"{location}: expected type {allowed}")
            return errors
    if "const" in spec and value != spec["const"]:
        errors.append(f"{location}: wrong constant/version")
    if "enum" in spec and value not in spec["enum"]:
        errors.append(f"{location}: value outside enum")
    if isinstance(value, dict):
        for key in spec.get("required", []):
            if key not in value:
                errors.append(f"{location}: missing {key}")
        properties = spec.get("properties", {})
        if spec.get("additionalProperties") is False:
            for key in value.keys() - properties.keys():
                errors.append(f"{location}: forbidden key {key}")
        for key in value.keys() & properties.keys():
            check_schema(value[key], properties[key], root_schema, f"{location}.{key}", errors)
    if isinstance(value, list):
        if len(value) < spec.get("minItems", 0):
            errors.append(f"{location}: insufficient items")
        if "items" in spec:
            for i, item in enumerate(value):
                check_schema(item, spec["items"], root_schema, f"{location}[{i}]", errors)
    if isinstance(value, str):
        if len(value) < spec.get("minLength", 0):
            errors.append(f"{location}: too short")
        if "pattern" in spec and not re.search(spec["pattern"], value):
            errors.append(f"{location}: pattern mismatch")
        if spec.get("format") == "date":
            try:
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                    raise ValueError("date precision")
                date.fromisoformat(value)
            except ValueError:
                errors.append(f"{location}: invalid ISO date")
        if spec.get("format") == "date-time":
            try:
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})", value):
                    raise ValueError("timestamp needs explicit zone and seconds")
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                errors.append(f"{location}: invalid ISO timestamp")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in spec and value < spec["minimum"]:
            errors.append(f"{location}: below minimum")
        if "maximum" in spec and value > spec["maximum"]:
            errors.append(f"{location}: above maximum")
    return errors


def validate_split_rows(rows):
    errors = []
    seen = {"world_id": {}, "family_id": {}, "template_lineage": {}}
    ids = set()
    for row in rows:
        fixture_id = row["fixture_id"]
        if fixture_id in ids:
            errors.append(f"duplicate fixture_id: {fixture_id}")
        ids.add(fixture_id)
        for field in seen:
            if field not in row or row[field] is None:
                continue
            old_split = seen[field].setdefault(row[field], row["split"])
            if old_split != row["split"]:
                errors.append(f"{field} {row[field]} spans {old_split} and {row['split']}")
        parent = row.get("counterfactual_parent_id")
        if parent is not None:
            old_split = seen["world_id"].setdefault(parent, row["split"])
            if old_split != row["split"]:
                errors.append(f"counterfactual parent {parent} spans {old_split} and {row['split']}")
    return errors


def check_donor_pair(donor, recipient, donor_answer_key, recipient_answer_key):
    """Require prospectively assigned verifier-defined answer-equivalence keys.

    Keys are not taken from filenames, surface room names, or arbitrary prose.
    Shared uncertainty labels must be analyzed as guardrails outside this API.
    """
    errors = []
    if donor["split"] != "development":
        errors.append("primary donor must be development")
    if donor["world_id"] == recipient["world_id"]:
        errors.append("donor and recipient share latent world")
    if recipient["split"] == "confirmation" and donor["family_id"] == recipient["family_id"]:
        errors.append("primary confirmation shares donor structural family")
    if not donor_answer_key or not recipient_answer_key:
        errors.append("missing answer equivalence key")
    elif donor_answer_key == recipient_answer_key:
        errors.append("same answer class: not different-answer transfer")
    return errors


def build_prompt_record(visible, condition="premises_only", treatment="", *, diagnostic=False):
    """Render only approved visible fields; never accept an evaluator fixture."""
    if set(visible) != VISIBLE_KEYS:
        raise ValueError("visible prompt must contain exactly the six approved fields")
    if condition not in CONDITIONS:
        raise ValueError("unknown condition")
    if condition in {"answer_only", "full_explanation"} and not diagnostic:
        raise ValueError("answer-bearing condition requires explicit diagnostic=True")
    if not isinstance(treatment, str):
        raise ValueError("treatment must be text")
    if (condition == "premises_only") != (not treatment):
        raise ValueError("premises_only has no treatment; other conditions need text")
    if any(not isinstance(visible[k], str) for k in VISIBLE_KEYS - {"observations"}):
        raise ValueError("visible text fields must be strings")
    if not isinstance(visible["observations"], list) or not all(isinstance(v, str) for v in visible["observations"]):
        raise ValueError("observations must be a list of strings")
    common = "\n\n".join([
        visible["task"], "Premise A: " + visible["premises_a"],
        "Premise B: " + visible["premises_b"],
        "Observations:\n" + "\n".join(visible["observations"]),
        "Question: " + visible["question"], "Response format: " + visible["response_format"],
    ])
    treatment_prefix = "\n\n" + treatment if treatment else ""
    text = common + treatment_prefix + "\n\n" + CUE
    return {
        "schema_version": VERSION,
        "condition": condition,
        "text": text,
        "sha256": digest(text.encode("utf-8")),
        "common_prefix_sha256": digest(common.encode("utf-8")),
        "treatment_character_span": [len(common) + 2, len(common + treatment_prefix)] if treatment else None,
        "capture_character_boundary": len(text),
        "token_alignment_status": "requires_infrastructure_tokenization",
        "diagnostic": diagnostic,
    }


def artifact_paths(root=ROOT):
    paths = []
    for prefix in OWNED:
        for path in (root / prefix).rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts or "local_cache" in path.parts:
                continue
            if path.suffix == ".pyc" or path == root / "data/ground_truth/manifest.json":
                continue
            paths.append(path)
    return sorted(paths)


def make_manifest(root=ROOT):
    return {
        "schema_version": VERSION,
        "collection_id": "ground-truth-research-2026-10-11",
        "base_revision": BASE_REVISION,
        "base_verification": "origin/main fetched and compared on 2026-10-11; Plan/research-plan.md has a narrow CUSP evidence correction",
        "scope": list(OWNED),
        "public_content": "calibration_and_development_only",
        "model_runs_performed": False,
        "historically_admitted_candidates": 0,
        "confirmation_materialized": False,
        "hash_method": "sha256_raw_file_bytes",
        "source_provenance_note": "Upstream URLs/revisions are in individual audits. Unacquired upstream files have no asserted content hash. Local hashes certify file identity, not historical truth.",
        "license_status": "Original artifact licensing awaits repository-owner choice; upstream rights remain separate. No copyrighted PDFs or restricted corpora redistributed.",
        "files": [{"path": str(p.relative_to(root)), "bytes": p.stat().st_size, "sha256": digest(p.read_bytes())} for p in artifact_paths(root)],
    }


def validate_collection(root=ROOT):
    data = root / "data/ground_truth"
    schema = read_json(data / "schema.json")
    errors = []
    collections = []
    for filename, definition in (("candidate_registry.json", "candidate_registry"), ("calibration_fixtures.json", "fixture_collection"), ("research_fixtures.json", "fixture_collection"), ("meanflow_fixtures.json", "fixture_collection")):
        value = read_json(data / filename)
        file_errors = check_schema(value, schema["$defs"][definition], schema, filename)
        errors.extend(file_errors)
        if not file_errors:
            collections.append((filename, value))
    if errors:
        return errors
    registry = collections[0][1]["candidates"]
    candidate_ids = set()
    for c in registry:
        if c["candidate_id"] in candidate_ids:
            errors.append("duplicate candidate: " + c["candidate_id"])
        candidate_ids.add(c["candidate_id"])
        if c["status"] == "rejected" and not c["exclusion_reason"]:
            errors.append(c["candidate_id"] + ": rejected without reason")
    fixtures = [f for _, col in collections[1:] for f in col["fixtures"]]
    errors.extend(validate_split_rows(fixtures))
    fixture_ids = {f["fixture_id"] for f in fixtures}
    by_id = {f["fixture_id"]: f for f in fixtures}
    for f in fixtures:
        if f["candidate_id"] not in candidate_ids | {"synthetic-offset", "synthetic-badge"}:
            errors.append(f["fixture_id"] + ": unknown candidate")
        for probe_id in f.get("prerequisites", []):
            if probe_id not in fixture_ids:
                errors.append(f["fixture_id"] + ": missing prerequisite " + probe_id)
            elif by_id[probe_id]["world_id"] == f["world_id"]:
                errors.append(f["fixture_id"] + ": prerequisite shares target world")
    policy = read_json(data / "split_policy.json")
    if policy["confirmation"]["materialized"] or policy["confirmation"]["items"]:
        errors.append("public collection must not pretend to contain sealed confirmation")
    for path in artifact_paths(root):
        if path.suffix.lower() in {".pdf", ".bin", ".safetensors", ".pt", ".pkl"}:
            errors.append("unexpected upstream/binary artifact: " + str(path.relative_to(root)))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "manifest"])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.command == "validate":
        errors = validate_collection()
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print("Ground-truth schemas, references, split boundaries and public-content checks passed.")
        return 0
    result = make_manifest()
    manifest_path = DATA / "manifest.json"
    if args.check:
        if not manifest_path.exists() or read_json(manifest_path) != result:
            print("Manifest mismatch: review changed files, then rebuild intentionally.", file=sys.stderr)
            return 1
        print(f"Verified {len(result['files'])} artifact hashes.")
        return 0
    manifest_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(result['files'])} artifact hashes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
