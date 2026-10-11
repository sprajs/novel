#!/usr/bin/env python3
"""Keep one server/model resident for bounded repeated JSONL predictions."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from novel.artifacts import sha256_file, strict_json
from novel.fast_runtime import bounded_int, checked_completion, completion_request, server, write_new


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
            jobs = []
            for item in items:
                rendered, ids = client.prompt(item["messages"])
                for repeat in range(args.repeats):
                    jobs.append((item["id"], repeat, rendered, ids))

            def predict(job):
                identity, repeat, rendered, ids = job
                request = completion_request(ids, tokens=args.tokens, seed=args.seed + repeat, cache_prompt=args.cache_prompt,
                    n_probs=args.n_probs, schema=schema, temperature=args.temperature,
                    top_k=args.top_k, top_p=args.top_p, min_p=args.min_p)
                start = time.perf_counter()
                response = checked_completion(client, request, info["profile"]["context"])
                parsed = strict_json(response["content"]) if schema else None
                return {"id": identity, "repeat": repeat, "rendered_prompt": rendered, "prompt_ids": ids,
                        "request": request, "raw_response": response, "parsed_json": parsed,
                        "wall_seconds": time.perf_counter() - start}

            started = time.perf_counter()
            with ThreadPoolExecutor(max_workers=args.slots) as pool:
                for record in pool.map(predict, jobs):
                    # Persist every completed ordered observation before proceeding.
                    write_new(args.output / f"record-{len(report['records']):04d}.json", record)
                    report["records"].append({"id": record["id"], "repeat": record["repeat"],
                                              "wall_seconds": record["wall_seconds"],
                                              "tokens": len(record["raw_response"]["tokens"])})
            report["request_wall_seconds"] = time.perf_counter() - started
            report["status"] = "PASS"
    except Exception as exc:
        report["error"] = {"type": type(exc).__name__, "message": str(exc)}
        raise
    finally:
        write_new(args.output / "report.json", report)
    print(json.dumps({"status": report["status"], "report": str(args.output / "report.json")}))


if __name__ == "__main__":
    main()
