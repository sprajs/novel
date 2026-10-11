"""Replay a read-only compatibility check against a fetched infrastructure commit.

Only two already-reviewed sibling Python files are copied into a temporary
directory. No branch is merged or switched, no dependency is installed, and no
model is loaded. The source commit must already exist in the local object store.
"""

import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from artifact_tools import ROOT, digest
from infrastructure_adapter import INFRASTRUCTURE_REVISION, export_task, fixtures_for


def main():
    hashes = {}
    with tempfile.TemporaryDirectory(prefix="novel-interface-") as temp:
        source_root = Path(temp)
        package = source_root / "novel"
        package.mkdir()
        (package / "__init__.py").write_text("", encoding="utf-8")
        for filename in ("tasks.py", "artifacts.py"):
            source = subprocess.run(["git", "show", INFRASTRUCTURE_REVISION + ":src/novel/" + filename], cwd=ROOT, check=True, capture_output=True).stdout
            (package / filename).write_bytes(source)
            hashes[filename] = digest(source)
        sys.path.insert(0, str(source_root))
        tasks = importlib.import_module("novel.tasks")
        records = [export_task(fixture, condition)
                   for collection in ("calibration", "research", "meanflow")
                   for fixture in fixtures_for(collection)
                   for condition in ("premises_only", "minimal_bridge", "wrong_bridge", "irrelevant")]
        for record in records:
            assert tasks.TaskInput.from_dict(record).to_dict() == record
        export_path = source_root / "public.jsonl"
        export_path.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")
        assert len(list(tasks.read_public_tasks(export_path))) == len(records)
    print(json.dumps({"status": "passed", "infrastructure_revision": INFRASTRUCTURE_REVISION,
                      "source_sha256": hashes, "public_conditions_checked": len(records),
                      "model_execution": False, "branch_merged": False}, sort_keys=True))


if __name__ == "__main__":
    main()
