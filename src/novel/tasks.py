"""Public-only dataset handoff. Verifier secrets never enter prompt rendering."""

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Iterator, Literal


@dataclass(frozen=True)
class TaskInput:
    """One already-rendered public condition, not a ground-truth specification."""

    item_id: str
    world_id: str
    family_id: str
    lineage_id: str
    split: Literal["mechanics", "donor", "development", "confirmation"]
    condition: str
    prompt: str
    schema_version: int = 1

    @classmethod
    def from_dict(cls, record: dict) -> "TaskInput":
        # Exact keys deliberately reject hidden answer/proof/verifier payloads.
        required = set(cls.__dataclass_fields__)
        if set(record) != required:
            raise ValueError(f"Public task keys must be exactly {sorted(required)}")
        if type(record["schema_version"]) is not int or record["schema_version"] != 1:
            raise ValueError("Unsupported task schema")
        for key in required - {"schema_version"}:
            if not isinstance(record[key], str) or not record[key].strip():
                raise ValueError(f"{key} must be nonempty text")
        if record["split"] not in {"mechanics", "donor", "development", "confirmation"}:
            raise ValueError("Unknown split")
        if len(record["prompt"].encode("utf-8")) > 65536:
            raise ValueError("Public prompt exceeds 64 KiB")
        return cls(**record)

    def to_dict(self) -> dict:
        return asdict(self)


def read_public_tasks(path: Path, *, allow_confirmation: bool = False) -> Iterator[TaskInput]:
    """Load JSONL; reject duplicate item IDs and sealed confirmation by default."""
    seen: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if len(line.encode("utf-8")) > 131072:
                raise ValueError("Task record exceeds 128 KiB")
            task = TaskInput.from_dict(json.loads(line))
            if task.item_id in seen:
                raise ValueError(f"Duplicate item_id: {task.item_id}")
            if task.split == "confirmation" and not allow_confirmation:
                raise ValueError("Confirmation is sealed; requires a separately frozen protocol")
            seen.add(task.item_id)
            yield task
