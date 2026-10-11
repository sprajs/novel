"""Bounded JSON/SafeTensors records; immutable run directories."""

from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import uuid


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


class RunStore:
    """Reserve a unique run; never overwrite existing observations."""

    def __init__(self, root: Path, *, max_bytes: int, max_files: int = 12):
        if max_bytes <= 0 or max_files <= 0:
            raise ValueError("Storage limits must be positive")
        root.mkdir(parents=True, exist_ok=True)
        self.path = root / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:12])
        self.path.mkdir(exist_ok=False)
        self.max_bytes, self.max_files = max_bytes, max_files
        self.bytes_written = 0
        self.inventory = []

    def write_bytes(self, name: str, content: bytes) -> dict:
        if Path(name).name != name or name in {"", ".", ".."}:
            raise ValueError("Artifact name must be a plain filename")
        if self.bytes_written + len(content) > self.max_bytes or len(self.inventory) >= self.max_files:
            raise ValueError("Run storage budget exceeded; artifact was not silently truncated")
        with (self.path / name).open("xb") as handle:
            handle.write(content)
        item = {"path": name, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
        self.inventory.append(item)
        self.bytes_written += len(content)
        return item

    def write_json(self, name: str, value) -> dict:
        return self.write_bytes(name, json_bytes(value))


def environment_record() -> dict:
    def git(*args):
        result = subprocess.run(["git", *args], text=True, capture_output=True, check=False)
        return result.stdout.strip() if result.returncode == 0 else None

    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "platform": platform.platform(),
        "cpu_count": os.cpu_count(),
        "packages": {name: importlib.metadata.version(name) for name in
                     ["torch", "transformers", "huggingface-hub", "safetensors", "numpy"]},
        "git_commit": git("rev-parse", "HEAD"),
        "git_branch": git("branch", "--show-current"),
        "git_dirty": bool(git("status", "--porcelain")),
    }
