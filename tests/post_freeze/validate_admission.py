"""Offline structural checks for the illustrative post-freeze admission record.

The assertion subset below is deliberately finite and fail-closed. It is not a
general Draft 2020-12 implementation or an operational admission authority.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "post_freeze"
ADMITTED = {"admitted_development", "admitted_confirmation"}
ASSERTIONS = {
    "$ref", "type", "enum", "const", "required", "properties",
    "additionalProperties", "items", "minItems", "maxItems", "uniqueItems",
    "minLength", "pattern", "format", "allOf", "anyOf", "if", "then", "else",
}
ANNOTATIONS = {"$schema", "$id", "$defs", "title", "description", "$comment"}
MUTABLE = {"main", "master", "latest", "head"}


def read_json(path: Path):
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError(f"nonfinite JSON constant: {value}")

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_constant=invalid_constant)


def check_vocabulary(spec):
    """Reject unsupported assertions rather than silently giving false assurance."""
    if not isinstance(spec, dict):
        raise ValueError("only object schemas are supported")
    unknown = set(spec) - ASSERTIONS - ANNOTATIONS
    if unknown:
        raise ValueError(f"unsupported schema keywords: {sorted(unknown)}")
    if "$ref" in spec and not re.fullmatch(r"#/[\$]defs/[A-Za-z_]+", spec["$ref"]):
        raise ValueError("only local #/$defs/name references are supported")
    if "format" in spec and spec["format"] not in {"date", "date-time"}:
        raise ValueError(f"unsupported format: {spec['format']}")
    if "type" in spec:
        names = spec["type"] if isinstance(spec["type"], list) else [spec["type"]]
        if any(name not in {"object", "array", "string", "boolean", "null"} for name in names):
            raise ValueError("unsupported schema type")
    if "additionalProperties" in spec and spec["additionalProperties"] is not False:
        raise ValueError("only additionalProperties:false is supported")
    for key in ("$defs", "properties"):
        for child in spec.get(key, {}).values():
            check_vocabulary(child)
    for key in ("items", "if", "then", "else"):
        if key in spec:
            check_vocabulary(spec[key])
    for key in ("allOf", "anyOf"):
        for child in spec.get(key, []):
            check_vocabulary(child)


def _same_json(left, right):
    # Python's True == 1 must not make a boolean match an integer constant.
    return json.dumps(left, sort_keys=True) == json.dumps(right, sort_keys=True)


def check_schema(value, spec, root, location="$", errors=None):
    """Apply the bundled schema's documented assertion subset."""
    errors = [] if errors is None else errors
    if "$ref" in spec:
        check_schema(value, root["$defs"][spec["$ref"].split("/")[-1]], root,
                     location, errors)
    for child in spec.get("allOf", []):
        check_schema(value, child, root, location, errors)
    if "anyOf" in spec and not any(
        not check_schema(value, child, root, location, []) for child in spec["anyOf"]
    ):
        errors.append(f"{location}: no allowed shape matched")
    if "if" in spec:
        branch = "else" if check_schema(value, spec["if"], root, location, []) else "then"
        if branch in spec:
            check_schema(value, spec[branch], root, location, errors)
    types = {
        "object": lambda v: isinstance(v, dict),
        "array": lambda v: isinstance(v, list),
        "string": lambda v: isinstance(v, str),
        "boolean": lambda v: isinstance(v, bool),
        "null": lambda v: v is None,
    }
    if "type" in spec:
        allowed = spec["type"] if isinstance(spec["type"], list) else [spec["type"]]
        if any(name not in types for name in allowed):
            raise ValueError("unsupported schema type")
        if not any(types[name](value) for name in allowed):
            errors.append(f"{location}: expected type {allowed}")
            return errors
    if "const" in spec and not _same_json(value, spec["const"]):
        errors.append(f"{location}: wrong constant")
    if "enum" in spec and not any(_same_json(value, item) for item in spec["enum"]):
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
            check_schema(value[key], properties[key], root, f"{location}.{key}", errors)
    if isinstance(value, list):
        if len(value) < spec.get("minItems", 0):
            errors.append(f"{location}: insufficient items")
        if len(value) > spec.get("maxItems", len(value)):
            errors.append(f"{location}: excessive items")
        if spec.get("uniqueItems"):
            canonical = [json.dumps(v, sort_keys=True) for v in value]
            if len(set(canonical)) != len(value):
                errors.append(f"{location}: duplicate items")
        if "items" in spec:
            for i, child in enumerate(value):
                check_schema(child, spec["items"], root, f"{location}[{i}]", errors)
    if isinstance(value, str):
        if len(value) < spec.get("minLength", 0):
            errors.append(f"{location}: too short")
        if "pattern" in spec and not re.search(spec["pattern"], value):
            errors.append(f"{location}: pattern mismatch")
        try:
            if spec.get("format") == "date":
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                    raise ValueError("date precision")
                date.fromisoformat(value)
            if spec.get("format") == "date-time":
                _parse_second(value)
        except ValueError:
            errors.append(f"{location}: invalid {spec['format']}")
    return errors


def _parse_second(value):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        raise ValueError("UTC seconds precision required")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def time_interval(event):
    """Expand source precision to a half-open UTC uncertainty interval."""
    precision, value = event["precision"], event["value"]
    if precision == "unknown":
        if value is not None:
            raise ValueError("unknown precision requires null value")
        return None
    if value is None:
        raise ValueError("known precision requires a value")
    if precision == "second":
        start = _parse_second(value)
        return start, start + timedelta(seconds=1)
    formats = {"year": r"\d{4}", "month": r"\d{4}-\d{2}", "day": r"\d{4}-\d{2}-\d{2}"}
    if not re.fullmatch(formats[precision], value):
        raise ValueError("value does not match declared precision")
    expanded = value + {"year": "-01-01", "month": "-01", "day": ""}[precision]
    start = datetime.fromisoformat(expanded).replace(tzinfo=timezone.utc)
    if precision == "year":
        end = start.replace(year=start.year + 1)
    elif precision == "month":
        end = start.replace(year=start.year + (start.month == 12), month=start.month % 12 + 1)
    else:
        end = start + timedelta(days=1)
    return start, end


def _walk(value, path="$"):
    if isinstance(value, dict):
        yield path, value
        for key, child in value.items():
            yield from _walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from _walk(child, f"{path}[{i}]")


def _local_path(root, relative):
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("repository reference must be a relative path without '..'")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError("repository reference escapes the repository")
    return resolved


def validate_record(record, *, root=ROOT):
    schema = read_json(DATA / "admission.schema.json")
    check_vocabulary(schema)
    errors = check_schema(record, schema, schema)
    if errors:
        return errors
    sources = record["provenance"]["sources"]
    source_ids = [source["source_id"] for source in sources]
    if len(source_ids) != len(set(source_ids)):
        errors.append("provenance: duplicate source_id")
    known_refs = set(source_ids) | set(record["provenance"]["audit_refs"])
    for path, item in _walk(record):
        for field in ("evidence_refs", "competence_evidence_refs", "result_evidence_refs"):
            for reference in item.get(field, []):
                if reference not in known_refs:
                    errors.append(f"{path}.{field}: unknown evidence reference {reference}")
        if {"kind", "value", "precision", "caveats"} <= item.keys():
            try:
                time_interval(item)
            except (ValueError, OverflowError) as exc:
                errors.append(f"{path}: invalid date precision: {exc}")
    for source in sources:
        if source["version"].lower() in MUTABLE or re.search(
            r"/(?:blob|tree|resolve)/(?:main|master|latest|HEAD)(?:[/?#]|$)", source["url"]
        ):
            errors.append(f"source {source['source_id']}: mutable source alias")
        if re.fullmatch(r"v\d+", source["version"]) and not re.search(
            re.escape(source["version"]) + r"(?:[/?#]|$)", source["url"]
        ):
            errors.append(f"source {source['source_id']}: URL omits the declared paper version")
        if re.fullmatch(r"[a-f0-9]{40}", source["version"]) and source["version"] not in source["url"]:
            errors.append(f"source {source['source_id']}: URL omits the declared immutable revision")
    for log in record["provenance"]["prior_art_log"]:
        if log["status"] == "planned" and log["searched_on"] is not None:
            errors.append("prior_art_log: a planned query cannot have a performed date")
        if log["status"] != "planned" and (log["searched_on"] is None or not log["evidence_refs"]):
            errors.append("prior_art_log: completed/inherited queries need date and evidence")
    if record["provenance"]["prior_art_search_complete"] and any(
        log["status"] == "planned" for log in record["provenance"]["prior_art_log"]
    ):
        errors.append("prior_art_log: a pending query prevents a completed search declaration")
    for path in set(record["provenance"]["audit_refs"]) | set(record["protocol_refs"].values()):
        try:
            if not _local_path(root, path).is_file():
                errors.append(f"missing repository evidence/protocol: {path}")
        except ValueError as exc:
            errors.append(str(exc))
    snapshot = record["model_snapshot"]
    try:
        audit = read_json(_local_path(root, snapshot["audit_path"]))
    except (OSError, ValueError) as exc:
        errors.append(f"model_snapshot: unavailable or invalid model audit: {exc}")
        return errors
    audited = next((m for m in audit["models"] if m["audit_id"] == snapshot["audit_id"]), None)
    if audited is None:
        errors.append("model_snapshot: unknown model audit identity")
    else:
        template = audited["tokenizer_interface"].get("chat_template")
        expected = {
            "model_id": audited["model_id"], "full_revision": audited["selected_revision"],
            "tokenizer_revision": audited["selected_revision"],
            "chat_template_revision": audited["selected_revision"] if template else None,
            "tokenizer_config_sha256": audited["tokenizer_interface"]["tokenizer_config_sha256"],
            "decoded_chat_template_sha256": template["decoded_utf8_sha256"] if template else None,
        }
        for key, value in expected.items():
            if snapshot[key] != value:
                errors.append(f"model_snapshot: {key} disagrees with the pinned audit")
        model_sources = [s for s in sources if s["url"] == audited["immutable_card"]["url"]]
        if not model_sources or any(s["version"] != snapshot["full_revision"] for s in model_sources):
            errors.append("model_snapshot: missing consistent immutable model-card source")
    for key, kind in (("recorded_git_commit", "recorded_git_commit"),
                      ("publisher_release_announcement", "publisher_release_announcement")):
        if snapshot[key]["kind"] != kind:
            errors.append(f"model_snapshot: {key} must preserve its evidence kind")
    if record["chronology"]["submission"] and record["chronology"]["submission"]["kind"] != "submission":
        errors.append("chronology: submission must preserve its evidence kind")
    if record["chronology"]["eligibility"] == "eligible" or record["status"] in ADMITTED:
        release = snapshot["verified_full_public_release"]
        disclosure = record["chronology"]["first_public_disclosure"]
        if not release or not disclosure:
            errors.append("chronology: eligibility requires full public release and first public disclosure evidence")
        else:
            if release["kind"] != "public_visibility" or disclosure["kind"] != "first_public_disclosure":
                errors.append("chronology: commit, announcement, or submission proxies cannot establish eligibility")
            if release["precision"] not in {"day", "second"} or disclosure["precision"] not in {"day", "second"}:
                errors.append("chronology: coarse or unknown dates cannot establish eligibility in this subset")
            try:
                before, after = time_interval(release), time_interval(disclosure)
                if before is None or after is None or before[1] > after[0]:
                    errors.append("chronology: model/disclosure intervals overlap or are not ordered")
            except (ValueError, OverflowError):
                pass  # Already reported by precision validation.
        if not record["chronology"]["earlier_channel_search_complete"]:
            errors.append("chronology: unresolved earlier public channels prevent eligibility")
    for role, review in record["independent_human_reviews"].items():
        if review is not None:
            if review["review_role"] != role:
                errors.append(f"human_reviews: {role} review has the wrong role")
            if review["reviewed_artifacts"] != record["frozen_artifacts"]:
                errors.append(f"human_reviews: {role} sign-off is not bound to the frozen artifacts")
    reviews = record["independent_human_reviews"]
    if all(reviews.values()) and reviews["domain"]["reviewer_id"] == reviews["temporal"]["reviewer_id"]:
        errors.append("human_reviews: domain and temporal reviewers must be distinct humans")
    for artifact in record["frozen_artifacts"].values():
        try:
            path = _local_path(root, artifact["path"])
            if not path.is_file():
                errors.append(f"frozen_artifacts: missing {artifact['path']}")
            elif artifact["sha256"] is not None and hashlib.sha256(path.read_bytes()).hexdigest() != artifact["sha256"]:
                errors.append(f"frozen_artifacts: bytes differ from declared digest for {artifact['path']}")
        except ValueError as exc:
            errors.append(str(exc))
    exposure, custody = record["exposure"], record["split_custody"]
    if exposure["public"] and not custody["ever_public"]:
        errors.append("split_custody: a public fixture cannot claim it was never public")
    if custody["ever_public"] and (exposure["split"] == "confirmation" or exposure["confirmation_eligible"]):
        errors.append("exposure: public development material cannot become confirmation")
    for status, refs_key in (("scientific_competence", "competence_evidence_refs"),
                             ("scientific_results", "result_evidence_refs")):
        judgment = record["judgment"]
        if judgment[status] == "measured" and not judgment[refs_key]:
            errors.append(f"judgment: measured {status} requires evidence")
        if judgment[status] != "measured" and judgment[refs_key]:
            errors.append(f"judgment: unmeasured {status} cannot carry result evidence")
    return errors


def validate_collection():
    errors = []
    ids = set()
    paths = sorted(DATA.glob("*_admission.json"))
    if not paths:
        return ["no illustrative admission records found"]
    for path in paths:
        record = read_json(path)
        errors.extend(f"{path.name}: {error}" for error in validate_record(record))
        if record.get("status") != "exploratory":
            errors.append(f"{path.name}: shipped illustrative records must remain exploratory")
        exposure = record.get("exposure", {})
        if exposure.get("split") != "development" or exposure.get("public") is not True:
            errors.append(f"{path.name}: shipped examples must be public development")
        if record.get("record_id") in ids:
            errors.append("duplicate record_id")
        ids.add(record.get("record_id"))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    errors = validate_collection()
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Structural consistency passed for exploratory public development records only.")
    print("This does not establish historical novelty, source truth, or scientific validity.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
