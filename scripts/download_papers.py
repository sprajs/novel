#!/usr/bin/env python3
"""Retrieve explicit manifest entries into the ignored, bounded local PDF cache.

Only the standard library is used. The manifest is read-only: receipts printed by
an initial unpinned acquisition must be reviewed before committing a checksum.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "papers" / "manifest.json"
CACHE = ROOT / ".cache" / "papers"
MAX_FILE_BYTES = 25_000_000
MAX_CACHE_BYTES = 90_000_000
SOCKET_TIMEOUT_SECONDS = 20
TRANSFER_DEADLINE_SECONDS = 60
ALLOWED_HOSTS = frozenset({"arxiv.org", "aclanthology.org", "proceedings.mlr.press", "openreview.net"})
ID_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
SHA_RE = re.compile(r"[a-f0-9]{64}\Z")


class PaperError(ValueError):
    """A request failed its provenance, integrity, or resource constraints."""


def validate_url(url: str) -> None:
    if not isinstance(url, str):
        raise PaperError("Paper URL must be a string")
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS
            or parsed.username is not None or parsed.password is not None
            or parsed.port not in (None, 443) or parsed.fragment):
        raise PaperError(f"Disallowed paper URL: {url}")


class OfficialRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def load_manifest(path: Path = MANIFEST) -> dict:
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("schema_version") != 1 or not isinstance(document.get("papers"), list):
        raise PaperError("Expected manifest schema_version 1 with a papers list")
    seen = set()
    for paper in document["papers"]:
        if not isinstance(paper, dict):
            raise PaperError("Each paper record must be an object")
        paper_id = paper.get("id", "")
        if not isinstance(paper_id, str) or not ID_RE.fullmatch(paper_id) or paper_id in seen:
            raise PaperError(f"Invalid or duplicate paper ID: {paper_id!r}")
        seen.add(paper_id)
        validate_url(paper["pdf_url"])
        checksum = paper.get("sha256")
        if checksum is not None and (not isinstance(checksum, str) or not SHA_RE.fullmatch(checksum)):
            raise PaperError(f"Invalid SHA-256 for {paper_id}")
        size = paper.get("bytes")
        if size is not None and (type(size) is not int or not 0 < size <= MAX_FILE_BYTES):
            raise PaperError(f"Invalid size for {paper_id}")
        # Selected versions are fixed rather than the moving arXiv /pdf/ID alias.
        if urlsplit(paper["pdf_url"]).hostname == "arxiv.org" and not re.fullmatch(
                r"/pdf/\d{4}\.\d{4,5}v\d+", urlsplit(paper["pdf_url"]).path):
            raise PaperError(f"arXiv PDF must pin a version for {paper_id}")
        if urlsplit(paper["pdf_url"]).hostname == "arxiv.org" and paper.get("version") != (
                "arXiv:" + urlsplit(paper["pdf_url"]).path.removeprefix("/pdf/")):
            raise PaperError(f"PDF URL and bibliographic version disagree for {paper_id}")
    return document


def select_papers(document: dict, ids: list[str]) -> list[dict]:
    indexed = {paper["id"]: paper for paper in document["papers"]}
    if len(ids) != len(set(ids)):
        raise PaperError("Duplicate requested IDs")
    unknown = [paper_id for paper_id in ids if paper_id not in indexed]
    if unknown:
        raise PaperError(f"Unknown paper IDs: {', '.join(unknown)}")
    return [indexed[paper_id] for paper_id in ids]


def cache_path(paper: dict, cache: Path = CACHE) -> Path:
    paper_id = paper["id"]
    if not ID_RE.fullmatch(paper_id):
        raise PaperError("Invalid paper ID")
    # Refuse symlinked parents, including .cache and the output itself. A local
    # user must not be able to redirect a retrieval outside this cache directory.
    for parent in [cache, *cache.parents]:
        if parent.is_symlink():
            raise PaperError(f"Symlinked cache directory: {parent}")
    path = cache / f"{paper_id}.pdf"
    if path.is_symlink():
        raise PaperError(f"Symlinked cached PDF: {path}")
    return path


def cache_size(cache: Path) -> int:
    total = 0
    if cache.exists():
        for path in cache.rglob("*"):
            if path.is_symlink():
                raise PaperError(f"Symlink in paper cache: {path}")
            if path.is_file():
                total += path.stat().st_size
    return total


def file_receipt(path: Path) -> dict:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        if handle.read(5) != b"%PDF-":
            raise PaperError(f"Cached file is not a PDF: {path}")
        handle.seek(0)
        for chunk in iter(lambda: handle.read(65_536), b""):
            digest.update(chunk)
            size += len(chunk)
            if size > MAX_FILE_BYTES:
                raise PaperError(f"Cached file exceeds byte cap: {path}")
    return {"sha256": digest.hexdigest(), "bytes": size}


def check_receipt(paper: dict, receipt: dict) -> None:
    if paper.get("sha256") is not None and receipt["sha256"] != paper["sha256"]:
        raise PaperError(f"SHA-256 mismatch for {paper['id']}; existing files are never overwritten")
    if paper.get("bytes") is not None and receipt["bytes"] != paper["bytes"]:
        raise PaperError(f"Byte count mismatch for {paper['id']}")


def verify_paper(paper: dict, cache: Path = CACHE) -> dict:
    path = cache_path(paper, cache)
    if paper.get("sha256") is None:
        raise PaperError(f"No reviewed checksum for {paper['id']}")
    receipt = file_receipt(path)
    check_receipt(paper, receipt)
    return {"id": paper["id"], "status": "verified", **receipt}


def download_paper(paper: dict, cache: Path = CACHE, opener=None) -> dict:
    validate_url(paper["pdf_url"])
    destination = cache_path(paper, cache)
    if destination.exists():
        if paper.get("sha256") is None:
            raise PaperError(f"Existing unpinned PDF for {paper['id']}; review its checksum first")
        return verify_paper(paper, cache)
    cache.mkdir(parents=True, exist_ok=True)
    occupied = cache_size(cache)
    available = min(MAX_FILE_BYTES, MAX_CACHE_BYTES - occupied)
    if available <= 0:
        raise PaperError("Paper cache has exhausted its 90,000,000-byte budget")
    if paper.get("bytes") is not None and paper["bytes"] > available:
        raise PaperError("Selected paper would exceed the remaining cache budget")
    opener = opener or build_opener(OfficialRedirects())
    request = Request(paper["pdf_url"], headers={
        "User-Agent": "novel-research-paper-reader/0.1 (bounded primary-paper retrieval)",
        "Accept": "application/pdf", "Accept-Encoding": "identity",
    })
    started = time.monotonic()
    temporary = None
    try:
        with opener.open(request, timeout=SOCKET_TIMEOUT_SECONDS) as response:
            validate_url(response.geturl())
            if response.status != 200:
                raise PaperError(f"Expected HTTP 200, received {response.status}")
            length = response.headers.get("Content-Length")
            if length is not None and (not length.isdecimal() or int(length) > available):
                raise PaperError("Content-Length is invalid or exceeds byte budget")
            digest = hashlib.sha256()
            size = 0
            signature = b""
            with tempfile.NamedTemporaryFile(dir=cache, prefix=".partial-", delete=False) as handle:
                temporary = Path(handle.name)
                while True:
                    if time.monotonic() - started > TRANSFER_DEADLINE_SECONDS:
                        raise PaperError("Transfer exceeded its deadline")
                    # Read at most one excess byte so unknown/chunked sizes are bounded.
                    chunk = response.read(min(65_536, available - size + 1))
                    if time.monotonic() - started > TRANSFER_DEADLINE_SECONDS:
                        raise PaperError("Transfer exceeded its deadline")
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > available:
                        raise PaperError("PDF exceeded file or cache byte budget")
                    signature = (signature + chunk)[:5]
                    digest.update(chunk)
                    handle.write(chunk)
                if signature != b"%PDF-":
                    raise PaperError("Response is not a PDF (possibly an error/login page)")
                if length is not None and size != int(length):
                    raise PaperError("Truncated response: Content-Length mismatch")
                receipt = {"sha256": digest.hexdigest(), "bytes": size}
                check_receipt(paper, receipt)
                handle.flush()
                os.fsync(handle.fileno())
            # Hard-link publication is atomic and refuses an existing destination,
            # including one created concurrently. Never clobber another artifact.
            if cache_size(cache) > MAX_CACHE_BYTES:
                raise PaperError("Paper cache budget exceeded before publication")
            os.link(temporary, destination)
            return {"id": paper["id"], "status": "downloaded" if paper.get("sha256") else "downloaded-unpinned", **receipt}
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--list", action="store_true", help="List IDs and pinned versions; offline")
    actions.add_argument("--dry-run", nargs="+", metavar="ID", help="Show explicit retrieval URLs; offline")
    actions.add_argument("--download", nargs="+", metavar="ID", help="Retrieve only these explicit IDs")
    actions.add_argument("--verify", nargs="+", metavar="ID", help="Verify cached hashes; offline")
    args = parser.parse_args(argv)
    try:
        document = load_manifest()
        if args.list:
            for paper in document["papers"]:
                print(f"{paper['id']}\t{paper['version']}\t{paper['title']}")
            return 0
        selected = select_papers(document, args.dry_run or args.download or args.verify)
        for paper in selected:
            if args.dry_run:
                print(json.dumps({"id": paper["id"], "pdf_url": paper["pdf_url"], "sha256": paper.get("sha256")}, sort_keys=True))
            else:
                receipt = download_paper(paper) if args.download else verify_paper(paper)
                print(json.dumps(receipt, sort_keys=True), flush=True)
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f"Paper retrieval failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
