"""One bounded pretrained engineering smoke, never a scientific evaluation."""

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import resource
import time

import torch
from safetensors.torch import save as save_tensors
from transformers import AutoModelForCausalLM, AutoTokenizer

from .activation import (AdditiveIntervention, IdentityIntervention, ResidualSite,
                         SemanticAnchor, forward_reference, prepare_reference_model)
from .artifacts import RunStore, environment_record, sha256_file, strict_json
from .generation import generate_reference
from .gradients import activation_gradient
from .profiles import ResolvedProfile, memory_record, synchronize
from .models import model_entry, snapshot_path, verify_snapshot
from .tasks import TaskInput


def load_config(path: Path) -> dict:
    config = strict_json(path.read_text())
    fields = {"schema_version", "name", "model_key", "device", "dtype", "attention_implementation",
              "enable_thinking", "prompt", "max_input_tokens", "max_new_tokens", "sampling", "seeds",
              "layer", "threads", "atol", "rtol", "max_artifact_bytes", "task", "budget"}
    if set(config) != fields:
        raise ValueError("Unknown or missing configuration fields")
    nested = {"sampling": {"temperature", "top_p", "top_k", "do_sample"},
              "seeds": {"sampling", "fixture", "perturbation", "donor_selection", "world_generation"},
              "task": {"item_id", "world_id", "family_id", "lineage_id", "split", "condition"},
              "budget": {"maximum_generation_conditions", "maximum_total_generated_tokens", "scientific_sweep"}}
    for field, expected in nested.items():
        if not isinstance(config[field], dict) or set(config[field]) != expected:
            raise ValueError(f"Unknown or missing {field} fields")
    for seed in config["seeds"].values():
        if type(seed) is not int or not 0 <= seed <= 2**63 - 1:
            raise ValueError("Seeds must be nonnegative signed 64-bit integers")
    if config["schema_version"] != 1 or config["device"] != "cpu" or config["dtype"] != "float32":
        raise ValueError("This tested runner is the named CPU FP32 condition only")
    if config["attention_implementation"] != "eager" or config["enable_thinking"] is not False:
        raise ValueError("The bounded engineering smoke requires eager/non-thinking mode")
    for field, maximum in [("max_input_tokens", 256), ("max_new_tokens", 16), ("threads", 5)]:
        if type(config[field]) is not int or not 1 <= config[field] <= maximum:
            raise ValueError(f"Invalid bounded {field}")
    if config["task"]["split"] != "mechanics":
        raise ValueError("Smoke runner cannot open scientific or sealed evaluation splits")
    if config["budget"]["maximum_total_generated_tokens"] < 4 * config["max_new_tokens"]:
        raise ValueError("The four engineering generations exceed the declared token budget")
    if config["budget"]["maximum_generation_conditions"] != 4 or config["budget"]["scientific_sweep"] is not False:
        raise ValueError("Smoke requires exactly four engineering generation conditions")
    if not 1024 <= config["max_artifact_bytes"] <= 10 * 1024**2:
        raise ValueError("Artifact budget must be between 1 KiB and 10 MiB")
    for field in ("atol", "rtol"):
        if not 0 <= config[field] <= 0.001:
            raise ValueError("Numerical tolerance must be finite and at most 0.001")
    return config


def run(config_path: Path, registry: Path, cache: Path, runs: Path,
        *, execution: ResolvedProfile | None = None) -> Path:
    config = load_config(config_path)
    device, dtype = "cpu", "float32"
    if execution is not None:
        device, dtype = execution.device, execution.dtype
        config.update(model_key=execution.request.model_key, device=device, dtype=dtype,
                      name=f"{execution.request.profile}_{execution.request.model_key}_{dtype}_mechanics",
                      max_input_tokens=execution.request.max_input_tokens,
                      max_new_tokens=execution.request.max_new_tokens)
        config["budget"]["maximum_total_generated_tokens"] = 4 * config["max_new_tokens"]
        # Prospective numerical guardrails, not a calibration or cross-device guarantee.
        if dtype != "float32":
            config.update(atol=0.02 if dtype == "float16" else 0.1,
                          rtol=0.002 if dtype == "float16" else 0.01)
    entry = model_entry(registry, config["model_key"])
    snapshot = snapshot_path(cache, config["model_key"], entry)
    store = RunStore(runs, max_bytes=config["max_artifact_bytes"])
    started = time.perf_counter()
    checks = {}
    store.write_json("config.json", config)
    try:
        hashes = verify_snapshot(snapshot, entry)  # No implicit network/model download.
        torch.set_num_threads(config["threads"])
        torch.manual_seed(config["seeds"]["fixture"])
        torch.use_deterministic_algorithms(True)
        load_started = time.perf_counter()
        tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True, trust_remote_code=False)
        model = AutoModelForCausalLM.from_pretrained(
            snapshot, local_files_only=True, trust_remote_code=False,
            use_safetensors=True, dtype=getattr(torch, dtype), attn_implementation="eager",
        )
        model.to(device)
        prepare_reference_model(model)
        synchronize(device)
        actual_dtypes = sorted({str(p.dtype) for p in model.parameters()})
        actual_devices = sorted({str(p.device) for p in model.parameters()})
        if actual_dtypes != [f"torch.{dtype}"] or actual_devices != [device]:
            raise ValueError("Loaded parameters do not match the declared device/precision")
        if any(str(buffer.device) != device for buffer in model.buffers()):
            raise ValueError("Loaded buffers do not match the declared device")
        if sum(p.numel() for p in model.parameters()) != entry["parameters"]["unique_config_implied"]:
            raise ValueError("Loaded unique parameter count differs from the pinned registry")
        load_seconds = time.perf_counter() - load_started
        parameter_state = [(id(p), p._version) for p in model.parameters()]
        task = TaskInput.from_dict({"schema_version": 1, **config["task"], "prompt": config["prompt"]})
        template_args = {"tokenize": False, "add_generation_prompt": True, "enable_thinking": False}
        rendered = tokenizer.apply_chat_template([{"role": "user", "content": task.prompt}], **template_args)
        inputs = tokenizer(rendered, add_special_tokens=False, return_tensors="pt").input_ids.to(device)
        if inputs.shape[1] > config["max_input_tokens"]:
            raise ValueError("Prompt exceeds input cap; no silent truncation")
        position = inputs.shape[1] - 1
        site = ResidualSite(config["layer"], (position,))
        anchor = SemanticAnchor(
            role="assistant_response_boundary", start=position,
            token_ids=tuple(inputs[0, position:].tolist()), prefix_token_ids=tuple(inputs[0].tolist()),
            rationale="Final template token at the assistant response boundary, before any generated continuation. Single-input mechanics only; not a certified donor alignment.",
        )

        def compare(name, left, right, *, exact=False):
            error = float((left.float() - right.float()).abs().max())
            atol, rtol = (0.0, 0.0) if exact else (config["atol"], config["rtol"])
            passed = bool(torch.allclose(left, right, atol=atol, rtol=rtol))
            checks[name] = {"passed": passed, "max_abs_error": error, "atol": atol, "rtol": rtol, "status": "PASS" if passed else "FAIL"}
            if not passed:
                raise AssertionError(f"Engineering invariant failed: {name}, max_abs_error={error}")

        baseline = forward_reference(model, inputs)
        compare("clean_repeat_logits", baseline.logits, forward_reference(model, inputs).logits, exact=True)
        captured = forward_reference(model, inputs, capture_site=site)
        compare("capture_logits", baseline.logits, captured.logits, exact=True)
        identity = IdentityIntervention(site)
        zero = AdditiveIntervention(site, torch.ones(model.config.hidden_size, device=device), anchor, strength=0.0)
        compare("identity_logits", baseline.logits, forward_reference(model, inputs, intervention=identity).logits, exact=True)
        compare("zero_strength_logits", baseline.logits, forward_reference(model, inputs, intervention=zero).logits, exact=True)
        suffixes = [tokenizer.encode(text, add_special_tokens=False) for text in (" A", " B")]
        if suffixes[0] == suffixes[1]:
            raise ValueError("Causal prefix probe suffixes must differ")
        for i, suffix in enumerate(suffixes):
            extended = torch.cat([inputs, torch.tensor([suffix], dtype=torch.long, device=device)], dim=1)
            later = forward_reference(model, extended, capture_site=site)
            compare(f"causal_prefix_residual_{i}", captured.residual, later.residual)
            compare(f"causal_prefix_logits_{i}", baseline.logits, later.logits[:, :inputs.shape[1]])

        # Multiple teacher-forced cache steps; sampled text agreement is not parity evidence.
        positions = torch.arange(inputs.shape[1], device=device)
        extended = inputs
        with torch.no_grad():
            prefill = model(input_ids=inputs, attention_mask=torch.ones_like(inputs),
                            position_ids=positions[None], cache_position=positions,
                            use_cache=True, logits_to_keep=1)
            past = prefill.past_key_values
            del prefill
            for step, token in enumerate([suffixes[0][0], suffixes[1][0], suffixes[0][0]]):
                length = extended.shape[1]
                current = torch.tensor([[token]], dtype=torch.long, device=device)
                extended = torch.cat([extended, current], dim=1)
                cached = model(input_ids=current, past_key_values=past,
                               attention_mask=torch.ones_like(extended),
                               position_ids=torch.tensor([[length]], device=device),
                               cache_position=torch.tensor([length], device=device),
                               use_cache=True, logits_to_keep=1)
                past = cached.past_key_values
                compare(f"clean_cache_logits_{step}",
                        forward_reference(model, extended, last_logits_only=True).logits, cached.logits)
            del cached, past
        gradient = None
        if execution is not None and execution.request.gradient:
            objective_tokens = baseline.logits[0, -1].topk(2).indices.tolist()
            synchronize(device)
            gradient_started = time.perf_counter()
            try:
                gradient = activation_gradient(model, inputs, site, *objective_tokens)
            except Exception as exc:
                exc.validation_stage = "activation_gradient"
                checks["activation_gradient"] = {"passed": False, "status": "FAIL", "message": str(exc)}
                raise
            synchronize(device)
            checks["activation_gradient"] = {
                "passed": True, "status": "PASS", "score": gradient.score,
                "objective": "last-position top-1 minus top-2 clean logit; diagnostic only",
                "positive_token_id": gradient.positive_token_id, "negative_token_id": gradient.negative_token_id,
                "gradient_l2": float(gradient.gradient.float().norm()),
                "site": asdict(site), "shape": list(gradient.gradient.shape),
                "dtype": str(gradient.gradient.dtype), "detached": True,
                "artifact": "gradient.safetensors",
                "wall_seconds": time.perf_counter() - gradient_started,
                "finite_difference": "SKIP: checked on tiny FP32 model in offline tests; not calibrated on this pretrained/device condition",
            }
            store.write_bytes("gradient.safetensors", save_tensors({"selected_block_output_gradient": gradient.gradient.contiguous()}))
        del baseline
        eos = model.generation_config.eos_token_id
        eos = tuple(eos if isinstance(eos, list) else [eos]) if eos is not None else ()
        generations = []
        global_rng = torch.random.get_rng_state().clone()
        cuda_rng = torch.cuda.get_rng_state(device).clone() if device.startswith("cuda:") else None
        for name, intervention in [("clean", None), ("clean_repeat", None), ("identity", identity), ("zero_strength", zero)]:
            synchronize(device)
            generation_started = time.perf_counter()
            result = generate_reference(model, inputs, seed=config["seeds"]["sampling"],
                                        max_new_tokens=config["max_new_tokens"], eos_token_ids=eos,
                                        intervention=intervention, **config["sampling"])
            synchronize(device)
            generations.append({"condition": name, **asdict(result),
                                "raw_text": tokenizer.decode(result.generated_ids, skip_special_tokens=False),
                                "wall_seconds": time.perf_counter() - generation_started})
        checks["seeded_generation_identity"] = {"passed": all(g["generated_ids"] == generations[0]["generated_ids"] for g in generations)}
        checks["global_sampling_rng_unchanged"] = {"passed": bool(torch.equal(global_rng, torch.random.get_rng_state()))}
        if cuda_rng is not None:
            checks["global_cuda_rng_unchanged"] = {"passed": bool(torch.equal(cuda_rng, torch.cuda.get_rng_state(device)))}
        checks["parameter_gradients_absent"] = {"passed": all(p.grad is None for p in model.parameters())}
        checks["parameters_frozen_unmutated"] = {"passed": parameter_state == [(id(p), p._version) for p in model.parameters()] and all(not p.requires_grad for p in model.parameters())}
        checks["hooks_removed"] = {"passed": all(not layer._forward_hooks for layer in model.model.layers)}
        for check in checks.values():
            check.setdefault("status", "PASS" if check["passed"] else "FAIL")
        if not all(check["passed"] for check in checks.values()):
            raise AssertionError("Engineering invariant failed")
        tensor_record = store.write_bytes("residual.safetensors", save_tensors({"block_output": captured.residual.contiguous()}))
        store.write_json("tokens.json", {
            "task": task.to_dict(), "rendered_prompt": rendered, "input_ids": inputs[0].tolist(),
            "attention_mask": [1] * inputs.shape[1], "position_ids": list(range(inputs.shape[1])),
            "template_arguments": template_args, "chat_template": tokenizer.chat_template,
            "chat_template_sha256": hashlib.sha256(tokenizer.chat_template.encode()).hexdigest(),
            "eos_token_ids": eos, "generations": generations,
        })
        store.write_json("checks.json", checks)
        store.write_json("tensor-index.json", {
            "artifact": tensor_record, "site": asdict(site), "anchor": asdict(anchor),
            "module_path": site.module_path, "operation": "decoder block output after both residual additions, before next/final normalization",
            "shape": list(captured.residual.shape), "dtype": str(captured.residual.dtype),
            "detached": True, "capture_before_patch": True, "captured_condition": "capture_only",
            "tested_intervention": {"strength": 0.0, "direction": "all-ones",
                                    "amplitude_units": "raw residual units", "delta_normalization": "none",
                                    "patch_schedule": "fixed original cue re-applied on every full-prefix recomputation"},
            "cache_policy": "full_prefix_cache_disabled",
        })
        record = {
            "schema_version": 1, "status": "passed", "scope": "engineering only; no transfer, reasoning-accuracy, or novelty claim",
            "environment": environment_record(), "config_sha256": sha256_file(config_path),
            "registry_sha256": sha256_file(registry), "uv_lock_sha256": sha256_file(Path("uv.lock")),
            "model_key": config["model_key"], "model_repo": entry["repo_id"], "model_revision": entry["revision"],
            "tokenizer_revision": entry["tokenizer_revision"], "snapshot_files_sha256": hashes,
            "unique_parameter_count": sum(p.numel() for p in model.parameters()),
            "device": device, "dtype": dtype, "gpu_tested": device.startswith("cuda:"), "quantization": None,
            "execution_profile": execution.to_dict() if execution is not None else None,
            "dependency_lock_path": execution.lock_path if execution else "uv.lock",
            "dependency_lock_sha256": sha256_file(Path(execution.lock_path if execution else "uv.lock")),
            "effective_config_sha256": sha256_file(store.path / "config.json"),
            "buffer_dtypes": sorted({str(b.dtype) for b in model.buffers()}),
            "cuda_memory": memory_record(device),
            "tolerance_note": "GPU tolerances are prospective guardrails; record errors and calibrate before causal studies. No-op comparisons are exact.",
            "actual_parameter_dtypes": actual_dtypes, "actual_parameter_devices": actual_devices,
            "attention_implementation": "eager", "deterministic_algorithms": True,
            "seeds": config["seeds"], "unused_seed_streams": ["perturbation", "donor_selection", "world_generation"],
            "load_seconds": load_seconds, "total_wall_seconds": time.perf_counter() - started,
            "peak_process_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
            "generated_tokens": sum(len(g["generated_ids"]) for g in generations),
            "generation_forward_calls": sum(g["forward_calls"] for g in generations),
            "generation_processed_tokens": sum(g["processed_tokens"] for g in generations),
            "validation_forward_calls": 14 + int(gradient is not None), "backward_calls": int(gradient is not None), "verifier_calls": 0,
            "donor_ids": [], "parent_experiment_id": None,
            "storage_limit_bytes": config["max_artifact_bytes"], "max_files": store.max_files,
            "source_files_sha256": {str(path): sha256_file(path) for path in sorted(Path("src/novel").glob("*.py"))},
        }
        store.write_json("run.json", record)
        store.write_json("inventory.json", {"artifacts": list(store.inventory), "note": "Inventory excludes its own checksum"})
    except BaseException as exc:
        exc.run_path = store.path
        try:
            store.write_json("error.json", {"status": "failed", "type": type(exc).__name__, "message": str(exc),
                                            "wall_seconds": time.perf_counter() - started, "checks_completed": checks})
        except (ValueError, OSError):
            pass
        raise
    return store.path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/cpu-smoke.json"))
    parser.add_argument("--registry", type=Path, default=Path("configs/models.json"))
    parser.add_argument("--cache", type=Path, default=Path(".cache/models"))
    parser.add_argument("--runs", type=Path, default=Path("runs"))
    args = parser.parse_args()
    path = run(args.config, args.registry, args.cache, args.runs)
    print(json.dumps({"status": "passed", "run_path": str(path), "scope": "CPU FP32 engineering only"}))


if __name__ == "__main__":
    main()
