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


def run(config_path: Path, registry: Path, cache: Path, runs: Path) -> Path:
    config = load_config(config_path)
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
            use_safetensors=True, dtype=torch.float32, attn_implementation="eager",
        )
        prepare_reference_model(model)
        actual_dtypes = sorted({str(p.dtype) for p in model.parameters()})
        actual_devices = sorted({str(p.device) for p in model.parameters()})
        if actual_dtypes != ["torch.float32"] or actual_devices != ["cpu"]:
            raise ValueError("Loaded parameters do not match the declared CPU FP32 condition")
        load_seconds = time.perf_counter() - load_started
        parameter_state = [(id(p), p._version) for p in model.parameters()]
        task = TaskInput.from_dict({"schema_version": 1, **config["task"], "prompt": config["prompt"]})
        template_args = {"tokenize": False, "add_generation_prompt": True, "enable_thinking": False}
        rendered = tokenizer.apply_chat_template([{"role": "user", "content": task.prompt}], **template_args)
        inputs = tokenizer(rendered, add_special_tokens=False, return_tensors="pt").input_ids
        if inputs.shape[1] > config["max_input_tokens"]:
            raise ValueError("Prompt exceeds input cap; no silent truncation")
        position = inputs.shape[1] - 1
        site = ResidualSite(config["layer"], (position,))
        anchor = SemanticAnchor(
            role="assistant_response_boundary", start=position,
            token_ids=tuple(inputs[0, position:].tolist()), prefix_token_ids=tuple(inputs[0].tolist()),
            rationale="Final template token at the assistant response boundary, before any generated continuation. Single-input mechanics only; not a certified donor alignment.",
        )

        def compare(name, left, right):
            error = float((left.float() - right.float()).abs().max())
            passed = bool(torch.allclose(left, right, atol=config["atol"], rtol=config["rtol"]))
            checks[name] = {"passed": passed, "max_abs_error": error, "atol": config["atol"], "rtol": config["rtol"]}
            if not passed:
                raise AssertionError(f"Engineering invariant failed: {name}, max_abs_error={error}")

        baseline = forward_reference(model, inputs)
        captured = forward_reference(model, inputs, capture_site=site)
        compare("capture_logits", baseline.logits, captured.logits)
        identity = IdentityIntervention(site)
        zero = AdditiveIntervention(site, torch.ones(model.config.hidden_size), anchor, strength=0.0)
        compare("identity_logits", baseline.logits, forward_reference(model, inputs, intervention=identity).logits)
        compare("zero_strength_logits", baseline.logits, forward_reference(model, inputs, intervention=zero).logits)
        suffixes = [tokenizer.encode(text, add_special_tokens=False) for text in (" A", " B")]
        if suffixes[0] == suffixes[1]:
            raise ValueError("Causal prefix probe suffixes must differ")
        for i, suffix in enumerate(suffixes):
            extended = torch.cat([inputs, torch.tensor([suffix], dtype=torch.long)], dim=1)
            later = forward_reference(model, extended, capture_site=site)
            compare(f"causal_prefix_residual_{i}", captured.residual, later.residual)
            compare(f"causal_prefix_logits_{i}", baseline.logits, later.logits[:, :inputs.shape[1]])

        # Same forced token prefix; this measures numerical parity, not sampled-text agreement.
        token = suffixes[0][0]
        positions = torch.arange(inputs.shape[1])
        with torch.no_grad():
            prefill = model(input_ids=inputs, attention_mask=torch.ones_like(inputs),
                            position_ids=positions[None], cache_position=positions,
                            use_cache=True, logits_to_keep=1)
            cached = model(input_ids=torch.tensor([[token]]), past_key_values=prefill.past_key_values,
                           attention_mask=torch.ones((1, inputs.shape[1] + 1), dtype=torch.long),
                           position_ids=torch.tensor([[inputs.shape[1]]]),
                           cache_position=torch.tensor([inputs.shape[1]]), use_cache=True,
                           logits_to_keep=1)
        extended = torch.cat([inputs, torch.tensor([[token]])], dim=1)
        compare("clean_cache_logits", forward_reference(model, extended, last_logits_only=True).logits, cached.logits)
        eos = model.generation_config.eos_token_id
        eos = tuple(eos if isinstance(eos, list) else [eos]) if eos is not None else ()
        generations = []
        global_rng = torch.random.get_rng_state().clone()
        for name, intervention in [("clean", None), ("clean_repeat", None), ("identity", identity), ("zero_strength", zero)]:
            generation_started = time.perf_counter()
            result = generate_reference(model, inputs, seed=config["seeds"]["sampling"],
                                        max_new_tokens=config["max_new_tokens"], eos_token_ids=eos,
                                        intervention=intervention, **config["sampling"])
            generations.append({"condition": name, **asdict(result),
                                "raw_text": tokenizer.decode(result.generated_ids, skip_special_tokens=False),
                                "wall_seconds": time.perf_counter() - generation_started})
        checks["seeded_generation_identity"] = {"passed": all(g["generated_ids"] == generations[0]["generated_ids"] for g in generations)}
        checks["global_sampling_rng_unchanged"] = {"passed": bool(torch.equal(global_rng, torch.random.get_rng_state()))}
        checks["parameters_frozen_unmutated"] = {"passed": parameter_state == [(id(p), p._version) for p in model.parameters()] and all(not p.requires_grad for p in model.parameters())}
        checks["hooks_removed"] = {"passed": all(not layer._forward_hooks for layer in model.model.layers)}
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
            "device": "cpu", "dtype": "float32", "gpu_tested": False, "quantization": None,
            "actual_parameter_dtypes": actual_dtypes, "actual_parameter_devices": actual_devices,
            "attention_implementation": "eager", "deterministic_algorithms": True,
            "seeds": config["seeds"], "unused_seed_streams": ["perturbation", "donor_selection", "world_generation"],
            "load_seconds": load_seconds, "total_wall_seconds": time.perf_counter() - started,
            "peak_process_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
            "generated_tokens": sum(len(g["generated_ids"]) for g in generations),
            "generation_forward_calls": sum(g["forward_calls"] for g in generations),
            "generation_processed_tokens": sum(g["processed_tokens"] for g in generations),
            "validation_forward_calls": 9, "backward_calls": 0, "verifier_calls": 0,
            "donor_ids": [], "parent_experiment_id": None,
            "storage_limit_bytes": config["max_artifact_bytes"], "max_files": store.max_files,
            "source_files_sha256": {str(path): sha256_file(path) for path in sorted(Path("src/novel").glob("*.py"))},
        }
        store.write_json("run.json", record)
        store.write_json("inventory.json", {"artifacts": list(store.inventory), "note": "Inventory excludes its own checksum"})
    except BaseException as exc:
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
