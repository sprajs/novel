import hashlib
import json

import pytest

from novel.models import download_snapshot, model_entry, verify_snapshot


def manifest():
    return {"repo_id": "example/model", "revision": "a" * 40,
            "tokenizer_repo_id": "example/model", "tokenizer_revision": "a" * 40,
            "files": {"config.json": {"size_bytes": 2, "sha256": hashlib.sha256(b"{}").hexdigest()}}}


def test_registry_requires_pins_and_safe_filenames(tmp_path):
    entry = manifest()
    path = tmp_path / "registry.json"
    path.write_text(json.dumps({"models": {"test": entry}}))
    assert model_entry(path, "test")["revision"] == "a" * 40
    entry["revision"] = "main"
    path.write_text(json.dumps({"models": {"test": entry}}))
    with pytest.raises(ValueError, match="immutable"):
        model_entry(path, "test")


def test_corruption_and_download_budget_prevent_network(tmp_path):
    entry = manifest()
    (tmp_path / "config.json").write_bytes(b"{}")
    assert verify_snapshot(tmp_path, entry)
    (tmp_path / "config.json").write_bytes(b"[]")
    with pytest.raises(ValueError, match="hash mismatch"):
        verify_snapshot(tmp_path, entry)
    with pytest.raises(ValueError, match="above download cap"):
        download_snapshot(tmp_path, entry, max_bytes=1)
    with pytest.raises(ValueError, match="fails integrity"):
        download_snapshot(tmp_path, entry, max_bytes=100)
