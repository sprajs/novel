import hashlib

import pytest

from novel.artifacts import RunStore, sha256_file


def test_budget_and_integrity(tmp_path):
    store = RunStore(tmp_path, max_bytes=4, max_files=2)
    record = store.write_bytes("one", b"1234")
    assert record["sha256"] == hashlib.sha256(b"1234").hexdigest()
    assert sha256_file(store.path / "one") == record["sha256"]
    with pytest.raises(ValueError, match="budget"):
        store.write_bytes("two", b"a")
    assert not (store.path / "two").exists()


def test_no_overwrite_and_no_path_traversal(tmp_path):
    store = RunStore(tmp_path, max_bytes=100)
    store.write_bytes("one", b"a")
    with pytest.raises(FileExistsError):
        store.write_bytes("one", b"b")
    with pytest.raises(ValueError):
        store.write_bytes("../escape", b"c")
