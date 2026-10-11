#!/usr/bin/env python3
"""Native prefill/decode microbenchmark; startup and request batching are separate."""
import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from novel.artifacts import strict_json
from novel.fast_runtime import backend_config, bounded_int, gpu_preflight, host_record, reject_implicit_overrides, verify_artifact, verify_build, verify_full_offload, write_new


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("cloud-cpu", "local-2080ti", "rental"), required=True)
    parser.add_argument("--gguf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prompt-tokens", type=int, default=32)
    parser.add_argument("--decode-tokens", type=int, default=8)
    parser.add_argument("--repetitions", type=int, default=3)
    args = parser.parse_args()
    os.chdir(ROOT)
    bounded_int(args.prompt_tokens, "prompt tokens", 1, 2048)
    bounded_int(args.decode_tokens, "decode tokens", 1, 256)
    bounded_int(args.repetitions, "repetitions", 1, 10)
    build = ROOT / ".cache/fast" / args.profile
    receipt = verify_build(build, args.profile)
    artifact = verify_artifact(args.gguf)
    profile = backend_config()["profiles"][args.profile]
    reject_implicit_overrides()
    hardware = gpu_preflight(args.profile, profile, artifact, 1)
    args.output.mkdir(parents=True, exist_ok=False)
    argv = [str(build / "bin/llama-bench"), "-m", str(args.gguf.resolve()), "-p", str(args.prompt_tokens),
            "-n", str(args.decode_tokens), "-r", str(args.repetitions), "-t", str(profile["threads"]),
            "-ngl", str(profile["gpu_layers"]), "-fa", "off", "-ctk", "f16", "-ctv", "f16", "-o", "json",
            "-dev", "none" if profile["cuda_arch"] is None else "CUDA0", "-sm", "none", "--offline"]
    if profile["cuda_arch"] is not None:
        argv.append("-v")  # Keep actual placement evidence; requested ngl is insufficient.
    start = time.perf_counter()
    with (args.output / "stderr.log").open("xb") as log:
        result = subprocess.run(argv, stdout=subprocess.PIPE, stderr=log, check=False)
    (args.output / "stdout.json").write_bytes(result.stdout)
    report = {"status": "PASS" if result.returncode == 0 else "FAIL", "argv": argv,
              "exit_code": result.returncode, "build": receipt, "artifact": artifact, "host": host_record(), "hardware": hardware,
              "wall_seconds_including_load_and_native_warmup": time.perf_counter() - start,
              "peak_child_rss_bytes": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss * 1024,
              "native_results": strict_json(result.stdout.decode()) if result.returncode == 0 else None,
              "interpretation": "Native synthetic-token prefill/decode microbenchmark, native warmup retained. Not task throughput, GPU fit, or reference equivalence."}
    if result.returncode == 0 and profile["cuda_arch"] is not None:
        try:
            report["full_gpu_offload"] = verify_full_offload((args.output / "stderr.log").read_text())
        except ValueError as exc:
            report.update(status="FAIL", error=str(exc))
    write_new(args.output / "report.json", report)
    print(json.dumps({"status": report["status"], "report": str(args.output / "report.json")}))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
