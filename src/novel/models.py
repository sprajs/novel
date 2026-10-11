"""Acquire only allowlisted, immutable, hash-verified public model artifacts."""

import argparse
import json
from pathlib import Path
import re
import shutil
from urllib.parse import quote
from urllib.request import Request, urlopen

from novel.artifacts import sha256_file


def model_entry(registry: Path, key: str) -> dict:
    data = json.loads(registry.read_text())
    entry = data["models"][key]
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", key):
        raise ValueError("Invalid model key")
    if not re.fullmatch(r"[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+", entry["repo_id"]):
        raise ValueError("Invalid Hugging Face repository ID")
    if not re.fullmatch(r"[0-9a-f]{40}", entry["revision"]):
        raise ValueError("Model revision must be an immutable commit")
    if (entry["tokenizer_repo_id"], entry["tokenizer_revision"]) != (entry["repo_id"], entry["revision"]):
        raise ValueError("This adapter requires model and tokenizer from one snapshot")
    for name, info in entry["files"].items():
        if Path(name).name != name or name in {"", ".", ".."}:
            raise ValueError("Model filenames must be flat")
        if not re.fullmatch(r"[0-9a-f]{64}", info["sha256"]):
            raise ValueError(f"Missing SHA256 for {name}")
        if type(info["size_bytes"]) is not int or info["size_bytes"] <= 0:
            raise ValueError("Invalid file size")
    return entry


def snapshot_path(cache: Path, key: str, entry: dict) -> Path:
    return cache / f"{key}-{entry['revision']}"


def verify_snapshot(path: Path, entry: dict) -> dict:
    hashes = {}
    for name, info in entry["files"].items():
        file = path / name
        if not file.is_file() or file.stat().st_size != info["size_bytes"]:
            raise ValueError(f"Missing/wrong-size snapshot file: {name}; run novel-model download")
        digest = sha256_file(file)
        if digest != info["sha256"]:
            raise ValueError(f"Snapshot hash mismatch: {name}")
        hashes[name] = digest
    return hashes


def download_snapshot(path: Path, entry: dict, *, max_bytes: int) -> None:
    expected = sum(info["size_bytes"] for info in entry["files"].values())
    if expected > max_bytes:
        raise ValueError(f"Snapshot needs {expected} bytes, above download cap {max_bytes}")
    path.mkdir(parents=True, exist_ok=True)
    needed = sum(info["size_bytes"] for name, info in entry["files"].items() if not (path / name).exists())
    if shutil.disk_usage(path).free < needed + 512 * 1024**2:
        raise ValueError("Insufficient free storage including 512 MiB reserve")
    for name, info in entry["files"].items():
        destination = path / name
        if destination.exists():
            if destination.stat().st_size != info["size_bytes"] or sha256_file(destination) != info["sha256"]:
                raise ValueError(f"Existing snapshot file fails integrity: {name}; preserved for inspection")
            continue
        url = f"https://huggingface.co/{entry['repo_id']}/resolve/{entry['revision']}/{quote(name)}"
        temporary = destination.with_name(destination.name + ".part")
        if temporary.exists():
            raise ValueError(f"Partial download already exists: {temporary}; inspect/remove before retry")
        try:
            request = Request(url, headers={"User-Agent": "novel-research/0.1-public-snapshot"})
            with urlopen(request, timeout=60) as response, temporary.open("xb") as handle:
                total = 0
                while chunk := response.read(1024 * 1024):
                    total += len(chunk)
                    if total > info["size_bytes"]:
                        raise ValueError(f"Download larger than registry: {name}")
                    handle.write(chunk)
            if total != info["size_bytes"] or sha256_file(temporary) != info["sha256"]:
                raise ValueError(f"Downloaded file failed integrity: {name}")
            temporary.rename(destination)
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    verify_snapshot(path, entry)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["inspect", "download", "verify"])
    parser.add_argument("--model", default="qwen3_0_6b")
    parser.add_argument("--registry", type=Path, default=Path("configs/models.json"))
    parser.add_argument("--cache", type=Path, default=Path(".cache/models"))
    parser.add_argument("--max-bytes", type=int, default=3 * 1024**3)
    args = parser.parse_args()
    entry = model_entry(args.registry, args.model)
    path = snapshot_path(args.cache, args.model, entry)
    if args.action == "download":
        download_snapshot(path, entry, max_bytes=args.max_bytes)
    if args.action == "verify":
        verify_snapshot(path, entry)
    print(json.dumps({"model": args.model, "revision": entry["revision"], "path": str(path),
                      "expected_bytes": sum(f["size_bytes"] for f in entry["files"].values()),
                      "action": args.action}, indent=2))


if __name__ == "__main__":
    main()
