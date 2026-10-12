"""Checks the maintenance contract, not paper results or model behavior."""
import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("learning_build", ROOT / "scripts/learning/build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class BaselineContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = build.read(ROOT / "learning/content.json")

    def test_real_reading_inventory_and_dependency_order(self):
        build.validate(self.content)
        build.check_baseline(self.content)

    def test_missing_selected_paper_cannot_publish(self):
        content = copy.deepcopy(self.content)
        key = next(iter(build.inventory()))
        removed = {p["id"] for p in content["papers"] if build.source_key(p["url"]) == key}
        content["papers"] = [p for p in content["papers"] if p["id"] not in removed]
        for chapter in content["chapters"]:
            chapter["sources"] = [s for s in chapter["sources"] if s not in removed]
        with self.assertRaisesRegex(ValueError, "inventory not covered"):
            build.validate(content)

    def test_changed_added_and_deleted_research_inputs_need_review(self):
        expected = build.read(build.BASELINE)["files"]
        first = next(iter(expected))
        cases = [dict(expected, **{first: "changed"}), dict(expected, **{"Plan/new-direction.md": "new"}), {p:h for p,h in expected.items() if p != first}]
        for actual in cases:
            with self.subTest(actual_count=len(actual)), patch.object(build, "inputs", return_value=actual):
                with self.assertRaisesRegex(ValueError, "baseline needs review"):
                    build.check_baseline(self.content)

    def test_content_edits_require_a_new_review_receipt(self):
        original_digest = build.digest
        with patch.object(build, "digest", side_effect=lambda p: "edited" if p == ROOT / "learning/content.json" else original_digest(p)):
            with self.assertRaisesRegex(ValueError, "Content changed"):
                build.check_baseline(self.content)

    def test_external_link_cannot_execute_code(self):
        content = copy.deepcopy(self.content)
        content["papers"][0]["url"] = "javascript:alert(1)"
        with self.assertRaisesRegex(ValueError, "HTTPS"):
            build.validate(content)

    def test_prerequisite_cycle_is_rejected(self):
        content = copy.deepcopy(self.content)
        content["chapters"][0]["prerequisites"] = [content["chapters"][-1]["id"]]
        with self.assertRaisesRegex(ValueError, "out of order"):
            build.validate(content)

    def test_broken_reference_links_cannot_publish(self):
        for kind in ("chapter", "glossary", "method"):
            content = copy.deepcopy(self.content)
            if kind == "chapter":
                content["chapters"][0]["connections"][0]["chapter"] = "missing-chapter"
                message = "Broken connections"
            elif kind == "glossary":
                content["glossary"][0]["chapter"] = "missing-chapter"
                message = "Broken glossary"
            else:
                content["papers"][0]["methodUrl"] = "javascript:alert(1)"
                message = "HTTPS method"
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, message):
                build.validate(content)

    def test_duplicate_section_anchors_cannot_publish(self):
        content = copy.deepcopy(self.content)
        sections = content["chapters"][0]["sections"]
        sections[1]["id"] = sections[0]["id"]
        with self.assertRaisesRegex(ValueError, "section anchors"):
            build.validate(content)

    def test_ragged_worked_table_cannot_publish(self):
        content = copy.deepcopy(self.content)
        table = next(s["visual"] for c in content["chapters"] for s in c["sections"]
                     if s.get("visual", {}).get("type") == "table")
        table["rows"][0].pop()
        with self.assertRaisesRegex(ValueError, "worked table"):
            build.validate(content)

    def test_artifact_hashes_match_and_stale_assets_disappear(self):
        baseline = build.check_baseline(self.content)
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            for name in ("index.html", "app.js", "style.css", "favicon.svg"):
                (source / name).write_bytes((build.SOURCE / name).read_bytes())
            shutil.copytree(build.SOURCE / "vendor", source / "vendor")
            (source / "dist").mkdir()
            (source / "dist/obsolete.txt").write_text("retired")
            with patch.object(build, "SOURCE", source):
                # The builder logs a repo-relative output path; use a temporary root.
                with patch.object(build, "ROOT", source.parent):
                    build.build(self.content, baseline)
            info = json.loads((source / "dist/build-info.json").read_text())
            self.assertFalse((source / "dist/obsolete.txt").exists())
            for name, expected in info["files"].items():
                self.assertEqual(build.digest(source / "dist" / name), expected)


if __name__ == "__main__":
    unittest.main()
