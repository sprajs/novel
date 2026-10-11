"""One bounded profile smoke with a shareable PASS/FAIL/SKIP diagnostic report."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import time

from .artifacts import RunStore, environment_record, sha256_file
from .models import model_entry
from .profiles import (MODEL_KEYS, PROFILE_NAMES, ProfileRequest, configure_determinism,
                       failure_record, initialize_device, inspect_hardware, memory_record,
                       resolve_profile, validate_environment)
from .runner import run


def validate_profile(request: ProfileRequest, *, registry: Path, cache: Path,
                     runs: Path, config: Path, preflight_only: bool = False) -> tuple[int, Path]:
    store = RunStore(runs / "profile-checks", max_bytes=2 * 1024**2, max_files=1)
    started = time.perf_counter()
    report = {"schema_version": 1, "scope": "engineering mechanics only", "status": "FAIL",
              "request": asdict(request), "environment": environment_record(),
              "gpu_kernel_executed": False, "gpu_model_validated": False,
              "checks": {name: {"status": "SKIP", "reason": "Not reached"} for name in
                         ("preflight", "cuda_kernel", "pretrained_smoke", "activation_gradient")}}
    resolved = None
    stage = "preflight"
    try:
        report["determinism"] = configure_determinism()
        report["hardware"] = inspect_hardware(request.device_index)
        entry = model_entry(registry, request.model_key)
        report["model"] = {"key": request.model_key, "revision": entry["revision"],
                           "tokenizer_revision": entry["tokenizer_revision"], "license": entry["license"]["spdx_id"]}
        resolved = resolve_profile(request, report["hardware"], entry)
        report["resolved_profile"] = resolved.to_dict()
        report["dependency_lock_sha256"] = sha256_file(Path(resolved.lock_path))
        report["locked_installed_packages"] = validate_environment(resolved)
        report["registry_sha256"] = sha256_file(registry)
        report["source_files_sha256"] = {str(p): sha256_file(p) for p in sorted(Path("src/novel").glob("*.py"))}
        report["checks"]["preflight"] = {"status": "PASS"}
        stage = "cuda_kernel"
        report["checks"]["cuda_kernel"] = initialize_device(resolved)
        report["gpu_kernel_executed"] = report["checks"]["cuda_kernel"]["status"] == "PASS"
        if preflight_only:
            for name in ("pretrained_smoke", "activation_gradient"):
                report["checks"][name] = {"status": "SKIP", "reason": "--preflight-only: no snapshot loaded"}
        else:
            stage = "pretrained_smoke"
            run_path = run(config, registry, cache, runs, execution=resolved)
            report["run_path"] = str(run_path)
            report["invariants"] = json.loads((run_path / "checks.json").read_text())
            record = json.loads((run_path / "run.json").read_text())
            report["measurements"] = {key: record[key] for key in
                                      ("load_seconds", "total_wall_seconds", "peak_process_rss_bytes", "cuda_memory",
                                       "generated_tokens", "generation_forward_calls", "backward_calls")}
            report["checks"]["pretrained_smoke"] = {"status": "PASS"}
            report["checks"]["activation_gradient"] = (report["invariants"]["activation_gradient"] if request.gradient else
                                                         {"status": "SKIP", "reason": "Optional: enable --gradient"})
            report["gpu_model_validated"] = resolved.device.startswith("cuda:")
        report["status"] = "PASS"
        exit_code = 0
    except Exception as exc:
        report["error"] = failure_record(exc)
        if hasattr(exc, "run_path"):
            report["run_path"] = str(exc.run_path)
            error_path = exc.run_path / "error.json"
            if error_path.is_file():
                report["partial_run"] = json.loads(error_path.read_text())
        if "partial_run" in report:
            report["invariants"] = report["partial_run"]["checks_completed"]
            if "activation_gradient" in report["invariants"]:
                report["checks"]["activation_gradient"] = report["invariants"]["activation_gradient"]
        if getattr(exc, "validation_stage", None) == "activation_gradient":
            report["checks"]["activation_gradient"] = report["error"]
        report["checks"][stage] = report["error"]
        # Preserve hardware discovery and completed checks even when memory is exhausted.
        if resolved is not None:
            try:
                report["memory_at_failure"] = memory_record(resolved.device)
            except (RuntimeError, AssertionError):
                pass
        exit_code = 1
    report["wall_seconds"] = time.perf_counter() - started
    report["interpretation"] = "PASS covers only executed checks. SKIP never establishes GPU/model support. No cross-device token/throughput equivalence or scientific result is claimed."
    store.write_json("diagnostics.json", report)
    return exit_code, store.path / "diagnostics.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=PROFILE_NAMES, required=True)
    parser.add_argument("--model", choices=MODEL_KEYS)
    parser.add_argument("--device-index", type=int, default=0)
    parser.add_argument("--dtype", choices=("float32", "float16", "bfloat16"))
    parser.add_argument("--rental-capacity-gib", type=int, choices=(24, 32), default=24)
    parser.add_argument("--max-input-tokens", type=int, default=128)
    parser.add_argument("--max-new-tokens", type=int, default=8)
    parser.add_argument("--gradient", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--registry", type=Path, default=Path("configs/models.json"))
    parser.add_argument("--config", type=Path, default=Path("configs/cpu-smoke.json"))
    parser.add_argument("--cache", type=Path, default=Path(".cache/models"))
    parser.add_argument("--runs", type=Path, default=Path("runs"))
    args = parser.parse_args()
    try:
        request = ProfileRequest(**{key: getattr(args, key) for key in
                                   ("profile", "model", "device_index", "dtype", "rental_capacity_gib",
                                    "max_input_tokens", "max_new_tokens", "gradient")})
    except ValueError as exc:
        parser.error(str(exc))
    code, report = validate_profile(request, registry=args.registry, cache=args.cache,
                                    runs=args.runs, config=args.config, preflight_only=args.preflight_only)
    print(json.dumps({"status": "PASS" if code == 0 else "FAIL", "diagnostic_report": str(report)}))
    raise SystemExit(code)


if __name__ == "__main__":
    main()
