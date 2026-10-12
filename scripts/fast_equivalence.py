#!/usr/bin/env python3
"""Persisted sequential HF/native comparison; no scientific certification."""
import argparse
import gc
import hashlib
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from novel.artifacts import environment_record, json_bytes, sha256_file, strict_json
from novel.fast_runtime import (checked_completion, complete_with_termination, completion_request,
                                full_logprobs, logprob_metrics, server, write_new)
from novel.models import model_entry, snapshot_path, verify_snapshot


def reference_phase(args, config, entry, snapshot, report):
    """Return no model/device tensors; only persisted CPU evidence escapes this phase."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from safetensors.torch import save
    from novel.activation import prepare_reference_model
    from novel.diagnostics import comparison_failure, tensor_sha256
    from novel.generation import generate_reference
    tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(snapshot, local_files_only=True, trust_remote_code=False,
        use_safetensors=True, dtype=getattr(torch, args.dtype), attn_implementation="eager").to(args.device)
    prepare_reference_model(model)
    eos = tuple(entry["token_ids"]["generation_eos_token_ids"])
    for case in config["cases"]:
        rendered = tokenizer.apply_chat_template(case["messages"], tokenize=False, add_generation_prompt=True, enable_thinking=False)
        ids = tokenizer(rendered, add_special_tokens=False)["input_ids"]
        target = tokenizer(case["continuation"], add_special_tokens=False)["input_ids"]
        if not 1 <= len(target) <= 8 or len(ids) + len(target) > 128:
            raise ValueError("Probe requires 1..8 target tokens and at most 128 total tokens")
        complete_ids = tokenizer(rendered + case["continuation"], add_special_tokens=False)["input_ids"]
        if complete_ids != ids + target:
            raise ValueError("Reference continuation boundary changes tokenization")
        result = {"id": case["id"], "messages": case["messages"], "rendered_prompt": rendered,
                  "prompt_ids": ids, "target_ids": target, "continuation": case["continuation"],
                  "complete_ids": complete_ids, "steps": [], "generation": {}}
        report["cases"].append(result)
        for position, token in enumerate(target):
            inputs = torch.tensor([ids + target[:position]], dtype=torch.long, device=args.device)
            with torch.no_grad():
                clean = model(inputs, use_cache=False, logits_to_keep=1).logits[0, -1].float()
                repeat = model(inputs, use_cache=False, logits_to_keep=1).logits[0, -1].float()
            if not torch.equal(clean, repeat):
                report["reference_repeat_failure"] = comparison_failure(clean, repeat, atol=0, rtol=0)
                raise ValueError("Exact HF forward repeat failed; no retry")
            lp = torch.log_softmax(clean.double(), dim=-1).cpu()
            path = args.output / f"reference-{len(report['cases'])}-{position}.safetensors"
            with path.open("xb") as handle:
                handle.write(save({"logprobs": lp}))
            result["steps"].append({"position": position, "target_id": token,
                "reference_logits_sha256": tensor_sha256(clean), "reference_logprobs_path": path.name,
                "reference_logprobs_sha256": sha256_file(path), "reference_target_logprob": float(lp[token])})
        for cache in (False, True):
            started = time.perf_counter()
            generated = generate_reference(model, torch.tensor([ids], device=args.device), seed=17,
                max_new_tokens=8, do_sample=False, eos_token_ids=eos, use_cache=cache)
            if args.device.startswith("cuda"):
                torch.cuda.synchronize()
            result["generation"]["hf_cached" if cache else "hf_full_prefix"] = {
                "ids": generated.generated_ids, "raw_text": tokenizer.decode(generated.generated_ids, skip_special_tokens=False),
                "stop": generated.stop_reason, "wall_seconds": time.perf_counter() - started}
    # Fixed boundary spellings use the original tokenizer and include all special tokens.
    report["reference_boundary_text"] = {str(t): tokenizer.decode([t], skip_special_tokens=False)
        for t in (128247, 151643, 151645, 151662, 151663, 151664) if t < model.config.vocab_size}
    write_new(args.output / "reference-phase.json", {"cases": report["cases"],
        "snapshot_hashes": report["snapshot_hashes"], "reference": report["reference"],
        "config_sha256": report["config_sha256"], "reference_boundary_text": report["reference_boundary_text"]})


def release_reference(device, baseline):
    """Called only after the reference function has returned and lost its model locals."""
    import torch
    gc.collect()
    if device == "cpu":
        return {"status": "PASS", "device": "cpu", "gpu_allocated_bytes": None,
                "contract": "Reference phase returned only persisted evidence before native startup"}
    torch.cuda.synchronize(device)
    torch.cuda.empty_cache()
    allocated = torch.cuda.memory_allocated(device)
    if allocated > baseline:
        raise ValueError("Reference CUDA tensors remain allocated; native server was not started")
    return {"status": "PASS", "device": device, "gpu_allocated_bytes": allocated,
            "baseline_allocated_bytes": baseline, "reserved_bytes": torch.cuda.memory_reserved(device),
            "gpu_execution_tested_here": True}


def native_phase(args, config, entry, report):
    from safetensors.torch import load_file
    eos = tuple(entry["token_ids"]["generation_eos_token_ids"])
    with server(ROOT / ".cache/fast" / args.profile, args.gguf.resolve(), args.profile,
                args.output / "server.log") as (client, info):
        report["runtime"] = info
        artifact = info["artifact"]
        if (artifact["model_key"], artifact["revision"], artifact["source_file_sha256"]) != (args.model, entry["revision"], report["snapshot_hashes"]):
            raise ValueError("GGUF does not descend from the exact reference snapshot")
        if info["props"]["chat_template"] != entry["chat_template"]["text"]:
            raise ValueError("Template source differs from reference registry")
        if artifact["gguf_metadata"]["tokenizer.ggml.eos_token_id"] != entry["token_ids"]["config_eos_token_id"]:
            raise ValueError("Primary EOS metadata differs")
        native_stops = info["eog_token_ids"]
        raw_stop_match = set(native_stops) == set(eos)
        policy_supported = args.termination == "hf-eos" and set(eos) <= set(native_stops)
        report["stop_contract"] = {"reference_eos_ids": eos, "native_eog_ids": native_stops,
            "native_stop_set_match": raw_stop_match, "policy": args.termination,
            "effective_eos_ids": list(eos) if policy_supported else native_stops,
            "pass": raw_stop_match or policy_supported,
            "scope": "Greedy token-ID termination only; native tokenizer attributes unchanged"}
        for index, result in enumerate(report["cases"], 1):
            rendered, ids = client.prompt(result["messages"])
            if (rendered, ids) != (result["rendered_prompt"], result["prompt_ids"]):
                write_new(args.output / "template-mismatch.json", {"reference": result,
                    "native_text": rendered, "native_ids": ids})
                raise ValueError("Rendered template or token IDs differ")
            complete_ids = client.call("/tokenize", {"content": rendered + result["continuation"],
                "add_special": False, "parse_special": True})["tokens"]
            if complete_ids != result["complete_ids"]:
                raise ValueError("Native full-string tokenization differs across phases")
            for step in result["steps"]:
                path = args.output / step["reference_logprobs_path"]
                if sha256_file(path) != step["reference_logprobs_sha256"]:
                    raise ValueError("Persisted reference vector changed between phases")
                lp = load_file(str(path), device="cpu")["logprobs"].tolist()
                prefix = ids + result["target_ids"][:step["position"]]
                request = completion_request(prefix, tokens=1, n_probs=entry["model_config"]["vocab_size"])
                response = checked_completion(client, request, info["profile"]["context"])
                fast_lp = full_logprobs(response, len(lp))
                repeated = checked_completion(client, request, info["profile"]["context"])
                repeat_lp = full_logprobs(repeated, len(lp))
                step.update(logprob_metrics(lp, fast_lp, repeat_lp, step["target_id"]))
                step["fast_logprob_sha256"] = hashlib.sha256(json_bytes(fast_lp)).hexdigest()
                step["pass"] = (step["max_abs_logprob"] <= config["max_abs_logprob"]
                    and abs(step["kl_reference_to_fast"]) <= config["max_kl_reference_to_fast"]
                    and step["repeat_max_abs_logprob"] <= config["max_repeat_abs_logprob"] and step["top1_match"])
                write_new(args.output / f"step-{index}-{step['position']}.json", step)
            result["sequence_logprob_delta"] = sum(s["fast_target_logprob"] - s["reference_target_logprob"] for s in result["steps"])
            result["pass"] = all(s["pass"] for s in result["steps"]) and abs(result["sequence_logprob_delta"]) <= config["max_abs_sequence_logprob_delta"]
            started = time.perf_counter()

            def receive_generation(req, res):
                receipts = result["generation"].setdefault("native_receipts", [])
                write_new(args.output / f"generation-{index}-{len(receipts)}.json", {"request": req, "raw_response": res})
                receipts.append(res)

            response, chunks = complete_with_termination(client, completion_request(ids, n_probs=0), info["profile"]["context"],
                policy=args.termination, eos_ids=eos, native_eog_ids=native_stops,
                on_response=receive_generation)
            result["generation"]["fast"] = {"response": response, "native_chunks": chunks,
                "wall_seconds": time.perf_counter() - started}
            result["generation"]["raw_ids_match"] = list(result["generation"]["hf_cached"]["ids"]) == response["tokens"]
            result["generation"]["stop_match"] = result["generation"]["hf_cached"]["stop"] == ("eos" if response["stop_type"] == "eos" else "max_new_tokens")
            if args.termination == "hf-eos":
                result["generation"]["raw_text_match"] = result["generation"]["hf_cached"]["raw_text"] == response["content"]
                result["pass"] = (result["pass"] and result["generation"]["raw_ids_match"]
                    and result["generation"]["stop_match"] and result["generation"]["raw_text_match"])
        report["workload_gate_passed"] = report["stop_contract"]["pass"] and all(c["pass"] for c in report["cases"])
        report["status"] = "PASS" if report["workload_gate_passed"] else "FAIL"


def execute_phases(args, config, entry, snapshot, report):
    import torch
    baseline = torch.cuda.memory_allocated(args.device) if args.device.startswith("cuda") else 0
    reference_phase(args, config, entry, snapshot, report)
    report["reference_release"] = release_reference(args.device, baseline)
    report["reference_phase_sha256"] = sha256_file(args.output / "reference-phase.json")
    write_new(args.output / "reference-release.json", report["reference_release"])
    # No model/device tensor returned by reference_phase is kept across this boundary.
    native_phase(args, config, entry, report)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("cloud-cpu", "local-2080ti", "rental"), required=True)
    parser.add_argument("--model", choices=("qwen3_0_6b", "qwen3_1_7b", "qwen3_8b"), required=True)
    parser.add_argument("--gguf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/fast-equivalence.json")
    parser.add_argument("--cache", type=Path, default=ROOT / ".cache/models")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--dtype", choices=("float32", "float16", "bfloat16"), default="float32")
    parser.add_argument("--termination", choices=("native", "hf-eos"), default="native")
    args = parser.parse_args()
    os.chdir(ROOT)
    import torch
    from novel.diagnostics import numerical_runtime
    from novel.profiles import ProfileRequest, configure_determinism, initialize_device, inspect_hardware, resolve_profile, validate_environment
    config = strict_json(args.config.read_text())
    if set(config) != {"schema_version", "max_abs_logprob", "max_kl_reference_to_fast", "max_abs_sequence_logprob_delta", "max_repeat_abs_logprob", "cases"} or config["schema_version"] != 1:
        raise ValueError("Unknown equivalence configuration")
    for name in ("max_abs_logprob", "max_kl_reference_to_fast", "max_abs_sequence_logprob_delta", "max_repeat_abs_logprob"):
        if type(config[name]) not in (int, float) or not 0 <= config[name] <= 1:
            raise ValueError("Finite bounded predeclared tolerances required")
    if not 1 <= len(config["cases"]) <= 8:
        raise ValueError("At most eight cases")
    args.output.mkdir(parents=True, exist_ok=False)
    report = {"status": "FAIL", "scientific_interchangeability": False, "config": config, "cases": [],
        "config_sha256": sha256_file(args.config), "environment": environment_record(),
        "likelihood_object": "Raw p of fixed token prefixes without terminal token; not semantic mass or decoder q",
        "kl_convention": "Normalize full native logprobs in FP64 for KL; retain raw scores/mass error",
        "interpretation": "Bounded workload gate only; no GPU or general scientific equivalence certificate"}
    try:
        entry = model_entry(ROOT / "configs/models.json", args.model)
        report["determinism"] = configure_determinism()
        resolved = resolve_profile(ProfileRequest(profile=args.profile, model=args.model, dtype=args.dtype), inspect_hardware(), entry)
        if resolved.device != args.device:
            raise ValueError(f"Reference profile requires --device {resolved.device}")
        report["locked_reference_packages"] = validate_environment(resolved)
        # Initialize cuBLAS before execute_phases records its allocation baseline.
        # Its persistent workspace is not a retained model tensor. The unchanged
        # release guard still rejects any allocation above that measured baseline.
        report["reference_device_preflight"] = initialize_device(resolved)
        snapshot = snapshot_path(args.cache, args.model, entry)
        report["snapshot_hashes"] = verify_snapshot(snapshot, entry)
        torch.set_num_threads(5)
        torch.manual_seed(42)
        report["reference_runtime"] = numerical_runtime()
        report["reference"] = {"dtype": args.dtype, "device": args.device, "attention": "eager", "teacher_forced_cache": False}
        execute_phases(args, config, entry, snapshot, report)
    except Exception as exc:
        report["error"] = {"type": type(exc).__name__, "message": str(exc)}
    finally:
        write_new(args.output / "report.json", report)
    print(json.dumps({"status": report["status"], "report": str(args.output / "report.json")}))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
