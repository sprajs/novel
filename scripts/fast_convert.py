#!/usr/bin/env python3
"""Offline conversion from an existing hash-verified registry snapshot. Never download."""
import argparse
import importlib.metadata
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from novel.artifacts import sha256_file
from novel.fast_runtime import validate_lock, verify_artifact, verify_build, verify_source, write_new
from novel.models import model_entry, snapshot_path, verify_snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / ".cache/llama.cpp")
    parser.add_argument("--model", choices=("qwen3_0_6b", "qwen3_1_7b", "qwen3_8b"), required=True)
    parser.add_argument("--type", choices=("F16", "Q8_0", "Q4_K_M"), default="F16")
    parser.add_argument("--cache", type=Path, default=ROOT / ".cache/models")
    parser.add_argument("--quantizer-profile", choices=("cloud-cpu", "local-2080ti", "rental"), default="cloud-cpu")
    args = parser.parse_args()
    os.chdir(ROOT)
    source = args.source.resolve()
    pin = verify_source(source)
    packages = validate_lock(ROOT / "environments/fast-convert/uv.lock")
    # The converter imports SentencePiece before testing whether its tokenizer file exists.
    # Keep that extra dependency out of the hookable reference environment.
    for name, version in (("torch", "2.8.0+cpu"), ("transformers", "4.57.6"), ("numpy", "2.5.4"), ("sentencepiece", "0.2.1")):
        if importlib.metadata.version(name) != version:
            raise ValueError("Use environments/fast-convert/.venv/bin/python after uv sync --locked")
    entry = model_entry(ROOT / "configs/models.json", args.model)
    snapshot = snapshot_path(args.cache, args.model, entry).resolve()
    hashes = verify_snapshot(snapshot, entry)
    folder = ROOT / ".cache/gguf" / f"{args.model}-{entry['revision']}"
    folder.mkdir(parents=True, exist_ok=True)
    model = folder / f"{args.type}.gguf"
    if model.exists():
        verify_artifact(model)
        print(model)
        return
    f16 = folder / "F16.gguf"
    if args.type != "F16" and not f16.exists():
        raise ValueError("Convert F16 first, then explicitly select quantization")
    estimate = entry["memory_estimates_bytes"]["unique_weights_fp16"] + 512 * 1024**2
    if shutil.disk_usage(folder).free < estimate:
        raise ValueError("Insufficient disk for artifact plus reserve")
    env = {**os.environ, "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"}
    quantizer = None
    if args.type == "F16":
        argv = [sys.executable, str(source / "convert_hf_to_gguf.py"), str(snapshot), "--outtype", "f16", "--outfile", str(model)]
        parent_hash = None
    else:
        verify_artifact(f16)
        build = ROOT / ".cache/fast" / args.quantizer_profile
        verify_build(build, args.quantizer_profile)
        quantizer = build / "bin/llama-quantize"
        argv = [str(quantizer), str(f16), str(model), args.type, "5"]
        parent_hash = sha256_file(f16)
    with (folder / f"{args.type}.conversion.log").open("xb") as log:
        subprocess.run(argv, env=env, stdout=log, stderr=log, check=True)
    # Read metadata without making the serving/client environment depend on gguf or torch.
    sys.path.insert(0, str(source / "gguf-py"))
    import gguf
    reader = gguf.GGUFReader(str(model))
    fields = {key: field.contents() for key, field in reader.fields.items()
              if key in ("general.architecture", "general.file_type", "general.quantization_version",
                         "tokenizer.ggml.bos_token_id", "tokenizer.ggml.eos_token_id",
                         "tokenizer.ggml.add_bos_token", "tokenizer.chat_template")}
    receipt = {"schema_version": 1, "model_key": args.model, "repo_id": entry["repo_id"],
               "revision": entry["revision"], "tokenizer_revision": entry["tokenizer_revision"],
               "source_file_sha256": hashes, "source_template_sha256": entry["chat_template"]["sha256"],
               "llama_commit": pin, "converter_sha256": sha256_file(source / "convert_hf_to_gguf.py"),
               "conversion_lock_sha256": sha256_file(ROOT / "environments/fast-convert/uv.lock"),
               "source_tree": subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD^{tree}"], text=True).strip(),
               "command": argv, "quantization": args.type, "importance_matrix": None,
               "parent_f16_sha256": parent_hash, "quantizer_sha256": sha256_file(quantizer) if quantizer else None,
               "artifact_sha256": sha256_file(model), "artifact_bytes": model.stat().st_size,
               "gguf_metadata": fields,
               "packages": packages}
    write_new(model.with_suffix(".gguf.json"), receipt)
    print(model)


if __name__ == "__main__":
    main()
