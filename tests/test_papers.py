"""Offline regression checks for the paper cache's safety and provenance rules."""

import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "download_papers.py"
SPEC = importlib.util.spec_from_file_location("download_papers", SCRIPT)
papers = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(papers)
PDF = b"%PDF-1.7\nPrimary-paper-test-fixture\n%%EOF\n"


def entry(**changes):
    record = {
        "id": "test-paper", "version": "arXiv:2404.15255v1", "title": "Fixture",
        "pdf_url": "https://arxiv.org/pdf/2404.15255v1",
        "sha256": hashlib.sha256(PDF).hexdigest(), "bytes": len(PDF),
    }
    record.update(changes)
    return record


class Response(io.BytesIO):
    def __init__(self, body=PDF, headers=None, url=None, status=200):
        super().__init__(body)
        self.headers = headers or {}
        self.url = url or entry()["pdf_url"]
        self.status = status

    def geturl(self):
        return self.url


class PaperTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.cache = self.root / "cache"

    def opener(self, response):
        opener = Mock()
        opener.open.return_value = response
        return opener

    def assert_clean(self):
        self.assertFalse((self.cache / "test-paper.pdf").exists())
        self.assertFalse(list(self.cache.glob(".partial-*")))

    def test_repository_manifest_is_pinned_and_complete(self):
        document = papers.load_manifest()
        self.assertEqual(document["as_of"], "2026-10-11")
        self.assertEqual(document["cache_policy"]["max_cache_bytes"], papers.MAX_CACHE_BYTES)
        self.assertEqual(document["cache_policy"]["max_file_bytes"], papers.MAX_FILE_BYTES)
        self.assertTrue(6 <= len(document["papers"]) <= 10)
        for paper in document["papers"]:
            with self.subTest(paper=paper["id"]):
                self.assertRegex(paper["sha256"], r"^[a-f0-9]{64}$")
                self.assertGreater(paper["bytes"], 0)
                self.assertTrue(paper["authors"])
                self.assertTrue(paper["license"]["source_url"])
                self.assertTrue(paper["license"]["uncertainty"])
                self.assertTrue(paper["reading"]["claims"])
                self.assertTrue(paper["reading"]["controls_to_borrow"])
                self.assertTrue(paper["reading"]["limits"])
        self.assertLess(sum(p["bytes"] for p in document["papers"]), 100_000_000)

    def test_manifest_rejects_path_ids_duplicates_and_moving_versions(self):
        for records in [[entry(id="../escape")], [entry(), entry()],
                        [entry(pdf_url="https://arxiv.org/pdf/2404.15255")],
                        [entry(version="arXiv:2404.15255v2")]]:
            with self.subTest(records=records):
                manifest = self.root / "manifest.json"
                manifest.write_text(json.dumps({"schema_version": 1, "papers": records}))
                with self.assertRaises(papers.PaperError):
                    papers.load_manifest(manifest)

    def test_selection_requires_known_unique_ids(self):
        document = {"papers": [entry()]}
        for ids in [["unknown"], ["test-paper", "test-paper"], ["../escape"]]:
            with self.assertRaises(papers.PaperError):
                papers.select_papers(document, ids)

    def test_https_and_official_hosts_required_before_redirect(self):
        handler = papers.OfficialRedirects()
        for url in ["http://arxiv.org/pdf/x", "https://evil.example/x",
                    "https://arxiv.org.evil.example/x", "https://user@arxiv.org/x",
                    "https://arxiv.org:8443/x", "https://arxiv.org/x#fragment"]:
            with self.subTest(url=url):
                with self.assertRaises(papers.PaperError):
                    papers.validate_url(url)
                with self.assertRaises(papers.PaperError):
                    handler.redirect_request(None, None, 302, "Found", {}, url)

    def test_download_hash_and_idempotent_offline_reuse(self):
        opener = self.opener(Response(headers={"Content-Length": str(len(PDF))}))
        receipt = papers.download_paper(entry(), self.cache, opener)
        self.assertEqual(receipt["status"], "downloaded")
        self.assertEqual((self.cache / "test-paper.pdf").read_bytes(), PDF)
        opener.open.assert_called_once()
        with patch.object(papers, "build_opener", side_effect=AssertionError("network used")):
            self.assertEqual(papers.download_paper(entry(), self.cache)["status"], "verified")
        self.assertFalse(list(self.cache.glob(".partial-*")))

    def test_corrupt_existing_file_is_never_replaced_or_fetched(self):
        self.cache.mkdir()
        path = self.cache / "test-paper.pdf"
        corrupt = b"%PDF-1.7\nDifferent bytes\n"
        path.write_bytes(corrupt)
        opener = Mock()
        with self.assertRaisesRegex(papers.PaperError, "SHA-256 mismatch"):
            papers.download_paper(entry(), self.cache, opener)
        self.assertEqual(path.read_bytes(), corrupt)
        opener.open.assert_not_called()

    def test_download_mismatch_leaves_no_file(self):
        with self.assertRaisesRegex(papers.PaperError, "SHA-256 mismatch"):
            papers.download_paper(entry(sha256="0" * 64), self.cache, self.opener(Response()))
        self.assert_clean()

    def test_header_size_cap_rejects_before_streaming(self):
        response = Response(headers={"Content-Length": str(papers.MAX_FILE_BYTES + 1)})
        with self.assertRaisesRegex(papers.PaperError, "Content-Length"):
            papers.download_paper(entry(), self.cache, self.opener(response))
        self.assert_clean()

    def test_streamed_unknown_size_cap(self):
        with patch.object(papers, "MAX_FILE_BYTES", 20):
            with self.assertRaisesRegex(papers.PaperError, "byte budget"):
                papers.download_paper(entry(bytes=None), self.cache, self.opener(Response()))
        self.assert_clean()

    def test_total_cache_budget_counts_existing_files(self):
        self.cache.mkdir()
        (self.cache / "other.pdf").write_bytes(PDF)
        with patch.object(papers, "MAX_CACHE_BYTES", len(PDF) + 5):
            opener = Mock()
            with self.assertRaisesRegex(papers.PaperError, "remaining cache budget"):
                papers.download_paper(entry(), self.cache, opener)
            opener.open.assert_not_called()
        self.assert_clean()

    def test_error_page_truncation_status_and_redirect_are_rejected(self):
        responses = [Response(body=b"<html>sign in</html>"),
                     Response(headers={"Content-Length": str(len(PDF) + 1)}),
                     Response(url="https://evil.example/paper.pdf"), Response(status=206)]
        for response in responses:
            with self.subTest(url=response.url, status=response.status, headers=response.headers):
                with self.assertRaises(papers.PaperError):
                    papers.download_paper(entry(), self.cache, self.opener(response))
                self.assert_clean()

    def test_unpinned_acquisition_receipt_requires_review_before_reuse(self):
        record = entry(sha256=None, bytes=None)
        receipt = papers.download_paper(record, self.cache, self.opener(Response()))
        self.assertEqual(receipt["status"], "downloaded-unpinned")
        self.assertEqual(receipt["sha256"], hashlib.sha256(PDF).hexdigest())
        with self.assertRaisesRegex(papers.PaperError, "review"):
            papers.download_paper(record, self.cache)
        with self.assertRaisesRegex(papers.PaperError, "reviewed checksum"):
            papers.verify_paper(record, self.cache)

    def test_symlinked_directory_and_output_rejected(self):
        real = self.root / "real"
        real.mkdir()
        self.cache.symlink_to(real, target_is_directory=True)
        with self.assertRaisesRegex(papers.PaperError, "Symlinked cache"):
            papers.download_paper(entry(), self.cache, Mock())
        self.cache.unlink()
        self.cache.mkdir()
        (self.cache / "test-paper.pdf").symlink_to(real / "escape.pdf")
        with self.assertRaisesRegex(papers.PaperError, "Symlinked cached"):
            papers.download_paper(entry(), self.cache, Mock())
        self.assertFalse((real / "escape.pdf").exists())

    def test_deadline_and_transport_failure_remove_partial(self):
        with patch.object(papers.time, "monotonic", side_effect=[0, 0, 61]):
            with self.assertRaisesRegex(papers.PaperError, "deadline"):
                papers.download_paper(entry(), self.cache, self.opener(Response()))
        self.assert_clean()
        response = Response()
        response.read = Mock(side_effect=OSError("connection interrupted"))
        with self.assertRaisesRegex(OSError, "interrupted"):
            papers.download_paper(entry(), self.cache, self.opener(response))
        self.assert_clean()

    def test_atomic_publication_refuses_a_concurrently_created_destination(self):
        original_link = papers.os.link

        def concurrent_link(source, destination):
            destination.write_bytes(b"other process artifact")
            return original_link(source, destination)

        with patch.object(papers.os, "link", side_effect=concurrent_link):
            with self.assertRaises(FileExistsError):
                papers.download_paper(entry(), self.cache, self.opener(Response()))
        self.assertEqual((self.cache / "test-paper.pdf").read_bytes(), b"other process artifact")
        self.assertFalse(list(self.cache.glob(".partial-*")))

    def test_list_and_dry_run_do_not_access_network_or_cache(self):
        with patch.object(papers, "load_manifest", return_value={"papers": [entry()]}), \
                patch.object(papers, "build_opener", side_effect=AssertionError("network used")), \
                patch.object(papers, "cache_path", side_effect=AssertionError("cache used")), \
                patch("sys.stdout", new_callable=io.StringIO):
            self.assertEqual(papers.main(["--list"]), 0)
            self.assertEqual(papers.main(["--dry-run", "test-paper"]), 0)


if __name__ == "__main__":
    unittest.main()
