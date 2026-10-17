#!/usr/bin/env python3
"""Validate and package Novel's self-contained reading room (no network)."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
LEARNING = ROOT / "learning"
SOURCE = LEARNING / "site"
BASELINE = LEARNING / "baseline.json"
SOURCE_ROOTS = ("Plan", "docs", "src", "environments", "tests", "scripts", "data/discovery")
SOURCE_FILES = ("README.md", "papers/README.md", "papers/manifest.json", "pyproject.toml", "uv.lock")
SUFFIXES = {".md", ".json", ".jsonl", ".py", ".toml", ".lock"}
ID = re.compile(r"[a-z][a-z0-9-]*\Z")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    paths = {ROOT / p for p in SOURCE_FILES if (ROOT / p).is_file()}
    for folder in SOURCE_ROOTS:
        paths.update(p for p in (ROOT / folder).rglob("*") if p.is_file()
                     and p.suffix in SUFFIXES
                     and not str(p.relative_to(ROOT)).startswith(("scripts/learning/", "tests/learning/"))
                     and not any(part.startswith(".") or part == "__pycache__"
                                 for part in p.relative_to(ROOT).parts))
    return {str(p.relative_to(ROOT)): digest(p) for p in sorted(paths)}


def source_key(url):
    parsed = urlparse(url)
    if parsed.hostname == "arxiv.org":
        match = re.search(r"/(?:abs|html|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", parsed.path)
        if match:
            return "arxiv:" + match[1]
    return url.rstrip("/")


def inventory():
    urls = re.findall(r"\]\((https://[^)]+)\)", (ROOT / "Plan/reading-list.md").read_text())
    manifest = read(ROOT / "papers/manifest.json")
    urls += [p["source_url"] for p in manifest["papers"] + manifest["context_only_sources"]]
    return {source_key(url): url for url in urls}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(data):
    for key in ("title", "subtitle", "asOf", "baselineRevision", "overview", "chapters", "papers", "glossary"):
        require(key in data, f"Missing content field: {key}")
    require(len(data["chapters"]) >= 10, "The baseline needs its complete teaching path.")
    date.fromisoformat(data["asOf"])
    ids = {}
    for kind in ("chapters", "papers"):
        values = [entry["id"] for entry in data[kind]]
        require(len(set(values)) == len(values), f"Duplicate {kind} IDs")
        require(all(ID.fullmatch(value) for value in values), f"Unsafe {kind} ID")
        ids[kind] = set(values)
    widgets = set()
    for chapter in data["chapters"]:
        for field in ("title", "kicker", "summary", "whyNow", "takeaway"):
            require(isinstance(chapter.get(field), str) and chapter[field].strip(), f"Empty {chapter['id']}.{field}")
        require(chapter["status"] in {"core", "later"}, "Invalid chapter status")
        require(set(chapter["sources"]) <= ids["papers"], f"Broken sources in {chapter['id']}")
        require(set(chapter["prerequisites"]) <= ids["chapters"], f"Broken prerequisites in {chapter['id']}")
        require(chapter["id"] not in chapter["prerequisites"], "Chapter cannot require itself")
        connections = chapter.get("connections", [])
        require(all(c.get("chapter") in ids["chapters"] and c["chapter"] != chapter["id"]
                    and isinstance(c.get("reason"), str) and c["reason"].strip()
                    for c in connections), f"Broken connections in {chapter['id']}")
        require("check" not in chapter, "The reading guide does not use quizzes or completion checks")
        section_ids = [s.get("id", "") for s in chapter["sections"]]
        require(all(ID.fullmatch(s) for s in section_ids) and len(set(section_ids)) == len(section_ids),
                f"Invalid section anchors in {chapter['id']}")
        for section in chapter["sections"]:
            require(section.get("title") and section.get("paragraphs"), "Empty lesson section")
            require(all(isinstance(p, str) and p.strip() for p in section["paragraphs"]), "Empty paragraph")
            if "visual" in section:
                v = section["visual"]
                require(v["type"] in {"flow", "matrix", "table", "residual"} and v.get("caption"), "Invalid diagram")
                if v["type"] == "table":
                    require(len(v.get("headers", [])) >= 2 and v.get("rows")
                            and all(isinstance(h, str) and h.strip() for h in v["headers"])
                            and all(len(r) == len(v["headers"]) and all(isinstance(x, str) and x.strip() for x in r)
                                    for r in v["rows"]), "Invalid worked table")
                else:
                    require(len(v.get("nodes", [])) >= 2, "Invalid diagram nodes")
                if v["type"] == "matrix":
                    require(len(v["nodes"]) == 4 and len(v["rowLabels"]) == 2 and len(v["columnLabels"]) == 2, "Invalid concept matrix")
                if v["type"] == "residual":
                    require(len(v["nodes"]) == 3, "Invalid residual diagram")
                require(all(n.get("title") and n.get("text") for n in v.get("nodes", [])), "Empty diagram node")
            if "interactive" in section:
                widgets.add(section["interactive"])
    require(widgets == {"sampling", "likelihood", "intervention", "timeline"}, "Missing or unsupported interactive lesson")
    # Prerequisites must appear first: no hidden cycles or forward references.
    seen = set()
    for chapter in data["chapters"]:
        require(set(chapter["prerequisites"]) <= seen, f"Prerequisites out of order: {chapter['id']}")
        seen.add(chapter["id"])
    for paper in data["papers"]:
        for key in ("title", "authors", "url", "summary", "mechanism", "novelUse", "limits", "readFor", "readSections", "sourceScope", "stage"):
            require(isinstance(paper.get(key), str) and paper[key].strip(), f"Missing {paper['id']}.{key}")
        require(paper["status"] in {"core", "later", "context", "retired"}, "Invalid paper priority")
        url = urlparse(paper["url"])
        require(url.scheme == "https" and url.hostname and not url.username, "Only primary HTTPS source links are allowed")
        if "methodUrl" in paper:
            method_url = urlparse(paper["methodUrl"])
            require(method_url.scheme == "https" and method_url.hostname and not method_url.username,
                    "Only primary HTTPS method links are allowed")
        require(isinstance(paper.get("year"), int), "Missing source year")
        require(isinstance(paper.get("concepts"), list) and paper["concepts"], "Missing concepts")
    covered = {source_key(p["url"]) for p in data["papers"]}
    missing = {key: url for key, url in inventory().items() if key not in covered}
    require(not missing, "Reading inventory not covered: " + ", ".join(missing.values()))
    require(data["glossary"] and all(g.get("term") and g.get("definition") and g.get("example") for g in data["glossary"]), "Incomplete glossary")
    require(all(g.get("chapter") in ids["chapters"] for g in data["glossary"]), "Broken glossary explanation link")


def check_baseline(data):
    require(BASELINE.is_file(), "Missing baseline. Review content, then run --refresh-baseline.")
    baseline = read(BASELINE)
    actual = inputs()
    expected = baseline["files"]
    changed = [p for p in sorted(actual.keys() | expected.keys()) if actual.get(p) != expected.get(p)]
    require(not changed, "Learning baseline needs review; changed project inputs:\n  " + "\n  ".join(changed)
            + "\nRead learning/MAINTENANCE.md. Refresh only after reviewing the guide.")
    require(baseline["contentSha256"] == digest(LEARNING / "content.json"), "Content changed without a reviewed baseline receipt.")
    require(data["baselineRevision"] == baseline["revision"], "Content and baseline revision disagree")
    date.fromisoformat(baseline["reviewedAt"])
    return baseline


def refresh(data, revision, reviewed_at):
    require(re.fullmatch(r"[0-9a-f]{40}", revision), "Use a full reviewed research commit SHA")
    subprocess.run(["git", "cat-file", "-e", revision + "^{commit}"], cwd=ROOT, check=True, capture_output=True)
    date.fromisoformat(reviewed_at)
    data["baselineRevision"] = revision
    data["asOf"] = reviewed_at
    (LEARNING / "content.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"schemaVersion": 1, "revision": revision, "reviewedAt": reviewed_at,
               "contentSha256": digest(LEARNING / "content.json"), "files": inputs()}
    BASELINE.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")


def build(data, baseline):
    destination = SOURCE / "dist"
    require(not destination.is_symlink(), "dist must not be a symlink")
    destination.mkdir(exist_ok=True)
    # Only generated files live here; remove old output so retired assets cannot linger.
    for child in destination.iterdir():
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
    for name in ("index.html", "app.js", "style.css", "favicon.svg"):
        shutil.copyfile(SOURCE / name, destination / name)
    shutil.copytree(SOURCE / "vendor", destination / "vendor")
    for name in ("content.json", "baseline.json", "source-audit.md"):
        shutil.copyfile(LEARNING / name, destination / name)
    shutil.copyfile(LEARNING / "MAINTENANCE.md", destination / "maintenance.md")
    info = {"researchRevision": baseline["revision"], "reviewedAt": baseline["reviewedAt"],
            "contentSha256": digest(LEARNING / "content.json"),
            "files": {str(p.relative_to(destination)): digest(p) for p in sorted(destination.rglob("*")) if p.is_file()}}
    (destination / "build-info.json").write_text(json.dumps(info, indent=2) + "\n")
    print(f"Built {len(data['chapters'])} chapters, {len(data['papers'])} sources and {len(data['glossary'])} terms into {destination.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate without producing output")
    parser.add_argument("--refresh-baseline", action="store_true", help="record an explicitly reviewed baseline")
    parser.add_argument("--revision", help="full research commit reviewed, required for refresh")
    parser.add_argument("--reviewed-at", help="YYYY-MM-DD review date, required for refresh")
    args = parser.parse_args()
    try:
        data = read(LEARNING / "content.json")
        validate(data)
        if args.refresh_baseline:
            require(args.revision and args.reviewed_at, "Refresh requires --revision and --reviewed-at")
            refresh(data, args.revision, args.reviewed_at)
        baseline = check_baseline(data)
        if not args.check:
            build(data, baseline)
        else:
            print(f"Learning content valid; {len(baseline['files'])} reviewed project files match.")
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Learning check failed: {error}\n")


if __name__ == "__main__":
    main()
