#!/usr/bin/env python3
"""Keep one server/model resident for bounded repeated JSONL predictions."""
import argparse
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from novel.artifacts import sha256_file, strict_json
from novel.fast_runtime import bounded_int, completion_request, server, write_new
from novel.fast_jobs import prediction_jobs
from novel.models import model_entry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("cloud-cpu", "local-2080ti", "rental"), required=True)
    parser.add_argument("--gguf", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, default=ROOT / "configs/fast-prompts.jsonl")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--tokens", type=int, default=8)
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--slots", type=int, default=1)
    parser.add_argument("--context", type=int, help="Explicit per-slot context override, 128..8192")
    parser.add_argument("--n-probs", type=int, default=20)
    parser.add_argument("--seed", type=int, default=17, help="Seed increases by repeat index; exact requests are retained")
    parser.add_argument("--temperature", type=float, default=-1, help="-1: greedy; positive: explicit sampling")
    parser.add_argument("--top-k", type=int, default=0)
    parser.add_argument("--top-p", type=float, default=1)
    parser.add_argument("--min-p", type=float, default=0)
    parser.add_argument("--cache-prompt", action="store_true")
    parser.add_argument("--flash-attention", action="store_true")
    parser.add_argument("--thinking", action="store_true")
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--termination", choices=("native", "hf-eos"), default="native")
    args = parser.parse_args()
    os.chdir(ROOT)
    bounded_int(args.repeats, "repeats", 1, 32)
    bounded_int(args.slots, "slots", 1, 8)
    bounded_int(args.n_probs, "n_probs", 0, 100)
    bounded_int(args.tokens, "tokens", 1, 2048)
    completion_request([0], tokens=args.tokens, seed=args.seed + args.repeats - 1,
                       temperature=args.temperature, top_k=args.top_k, top_p=args.top_p, min_p=args.min_p)
    if args.inputs.stat().st_size > 1024**2:
        raise ValueError("Input file exceeds 1 MiB")
    items = [strict_json(line) for line in args.inputs.read_text().splitlines() if line.strip()]
    if not 1 <= len(items) <= 64 or any(set(item) != {"id", "messages"} for item in items):
        raise ValueError("Expected 1..64 records with exactly id and messages")
    if len({item["id"] for item in items}) != len(items):
        raise ValueError("Input IDs must be unique")
    if len(items) * args.repeats * args.tokens * max(1, args.n_probs) > 65536:
        raise ValueError("Trace budget exceeds 65,536 token/probability entries; split the workload explicitly")
    schema = strict_json(args.schema.read_text()) if args.schema else None
    if args.termination == "hf-eos" and (args.temperature >= 0 or args.cache_prompt or schema is not None):
        raise ValueError("hf-eos supports greedy unconstrained generation with prompt reuse disabled")
    # An exclusive directory retains all evidence, including partial/failing runs.
    args.output.mkdir(parents=True, exist_ok=False)
    report = {"status": "FAIL", "input_sha256": sha256_file(args.inputs), "records": [],
              "schema": schema, "likelihood_measurement": False,
              "interpretation": "Generated text and token/logprob traces; no hidden activations or interventions."}
    try:
        with server(ROOT / ".cache/fast" / args.profile, args.gguf.resolve(), args.profile,
                    args.output / "server.log", slots=args.slots, flash_attention=args.flash_attention,
                    thinking=args.thinking, context=args.context) as (client, info):
            report["runtime"] = info
            entry = model_entry(ROOT / "configs/models.json", info["artifact"]["model_key"])
            if entry["revision"] != info["artifact"]["revision"]:
                raise ValueError("Artifact revision differs from termination-policy registry")
            started = time.perf_counter()
            records = prediction_jobs(client, info, items, args.output, repeats=args.repeats, slots=args.slots,
                options={"tokens": args.tokens, "seed": args.seed, "cache_prompt": args.cache_prompt,
                         "n_probs": args.n_probs, "temperature": args.temperature, "top_k": args.top_k,
                         "top_p": args.top_p, "min_p": args.min_p}, schema=schema, termination=args.termination,
                eos_ids=entry["token_ids"]["generation_eos_token_ids"])
            report["records"] = [{k: record[k] for k in ("job_index", "status", "id", "repeat", "wall_seconds") if k in record}
                                 for record in records]
            report["attempted_jobs"] = len(records)
            report["failed_jobs"] = sum(record["status"] != "PASS" for record in records)
            report["request_wall_seconds"] = time.perf_counter() - started
            report["status"] = "PASS" if report["failed_jobs"] == 0 else "FAIL"
    except Exception as exc:
        report["error"] = {"type": type(exc).__name__, "message": str(exc)}
        raise
    finally:
        write_new(args.output / "report.json", report)
    print(json.dumps({"status": report["status"], "report": str(args.output / "report.json")}))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
