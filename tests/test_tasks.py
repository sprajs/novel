import json

import pytest

from novel.tasks import TaskInput, read_public_tasks


def record(**kwargs):
    return dict(schema_version=1, item_id="fixture-1", world_id="world-1",
                family_id="fixture", lineage_id="lineage-1", split="mechanics",
                condition="unmodified", prompt="Reply with a short greeting.", **kwargs)


def test_public_roundtrip_and_no_hidden_answer(tmp_path):
    data = record()
    assert TaskInput.from_dict(data).to_dict() == data
    with pytest.raises(ValueError):
        TaskInput.from_dict({**data, "answer": "secret"})
    path = tmp_path / "tasks.jsonl"
    path.write_text(json.dumps(data) + "\n")
    assert len(list(read_public_tasks(path))) == 1


def test_confirmation_and_duplicates_are_rejected(tmp_path):
    data = record()
    path = tmp_path / "tasks.jsonl"
    path.write_text(json.dumps({**data, "split": "confirmation"}) + "\n")
    with pytest.raises(ValueError, match="sealed"):
        list(read_public_tasks(path))
    path.write_text((json.dumps(data) + "\n") * 2)
    with pytest.raises(ValueError, match="Duplicate"):
        list(read_public_tasks(path))
