#!/usr/bin/env python3
"""Bounded, teacher-forced HF/llama.cpp comparison. No scientific certification."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from novel.artifacts import environment_record, json_bytes, sha256_file, strict_json
from novel.fast_runtime import checked_completion, completion_request, full_logprobs, logprob_metrics, server, write_new
from novel.models import model_entry, snapshot_path, verify_snapshot


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
    args = parser.parse_args()
    os.chdir(ROOT)
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from novel.activation import prepare_reference_model
    from novel.diagnostics import comparison_failure, numerical_runtime, tensor_sha256
    from novel.generation import generate_reference
    from novel.profiles import (ProfileRequest, configure_determinism, inspect_hardware, resolve_profile, validate_environment)
    config = strict_json(args.config.read_text())
    if set(config) != {"schema_version", "max_abs_logprob", "max_kl_reference_to_fast",
                       "max_abs_sequence_logprob_delta", "max_repeat_abs_logprob", "cases"} or config["schema_version"] != 1:
        raise ValueError("Unknown equivalence configuration")
    for name in ("max_abs_logprob", "max_kl_reference_to_fast", "max_abs_sequence_logprob_delta", "max_repeat_abs_logprob"):
        if type(config[name]) not in (int, float) or not 0 <= config[name] <= 1:
            raise ValueError("Finite bounded predeclared tolerances required")
    if not 1 <= len(config["cases"]) <= 8:
        raise ValueError("At most eight cases")
    args.output.mkdir(parents=True, exist_ok=False)
    report = {"status": "FAIL", "scientific_interchangeability": False, "config": config,
              "config_sha256": sha256_file(args.config), "environment": environment_record(), "cases": [],
              "likelihood_object": "Raw p of fixed token prefixes without a terminal token; not semantic event mass or decoder q",
              "kl_convention": "KL uses full-vocabulary server logprobs renormalized in FP64; raw logprobs, normalizer and mass error are retained separately",
              "interpretation": "A passing bounded workload gate covers only these exact prefixes/artifact/runtime. Quantization, hooks, and other workloads remain separate conditions."}
    try:
        entry = model_entry(ROOT / "configs/models.json", args.model)
        report["determinism"] = configure_determinism()
        resolved = resolve_profile(ProfileRequest(profile=args.profile, model=args.model, dtype=args.dtype),
                                   inspect_hardware(), entry)
        if resolved.device != args.device:
            raise ValueError(f"Reference profile requires --device {resolved.device}")
        report["locked_reference_packages"] = validate_environment(resolved)
        snapshot = snapshot_path(args.cache, args.model, entry)
        report["snapshot_hashes"] = verify_snapshot(snapshot, entry)
        torch.set_num_threads(5)
        torch.use_deterministic_algorithms(True)
        torch.manual_seed(42)
        report["reference_runtime"] = numerical_runtime()
        report["reference"] = {"dtype": args.dtype, "device": args.device, "attention": "eager", "teacher_forced_cache": False}
        tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True, trust_remote_code=False)
        model = AutoModelForCausalLM.from_pretrained(snapshot, local_files_only=True, trust_remote_code=False,
                                                    use_safetensors=True, dtype=getattr(torch, args.dtype), attn_implementation="eager").to(args.device)
        prepare_reference_model(model)
        with server(ROOT / ".cache/fast" / args.profile, args.gguf.resolve(), args.profile,
                    args.output / "server.log") as (client, info):
            report["runtime"] = info
            if (info["artifact"]["model_key"], info["artifact"]["revision"], info["artifact"]["source_file_sha256"]) != (args.model, entry["revision"], report["snapshot_hashes"]):
                raise ValueError("GGUF does not descend from the exact reference snapshot")
            if info["props"]["chat_template"] != entry["chat_template"]["text"]:
                raise ValueError("GGUF chat template source differs from registry")
            eos = tuple(entry["token_ids"]["generation_eos_token_ids"])
            report["stop_contract"] = {"reference_eos_ids": eos, "fast_eog_ids": info["eog_token_ids"]}
            metadata = info["artifact"]["gguf_metadata"]
            if metadata["tokenizer.ggml.eos_token_id"] != entry["token_ids"]["config_eos_token_id"]:
                raise ValueError("GGUF EOS differs from reference")
            # Quantify fixed-prefix probabilities even if free-generation stop semantics differ.
            # The aggregate gate still fails on that mismatch; this is not an override.
            report["stop_contract"]["pass"] = set(info["eog_token_ids"]) == set(eos)
            for case in config["cases"]:
                rendered = tokenizer.apply_chat_template(case["messages"], tokenize=False, add_generation_prompt=True, enable_thinking=False)
                ids = tokenizer(rendered, add_special_tokens=False)["input_ids"]
                fast_rendered, fast_ids = client.prompt(case["messages"])
                if (rendered, ids) != (fast_rendered, fast_ids):
                    write_new(args.output / "template-mismatch.json", {"reference_text": rendered, "fast_text": fast_rendered, "reference_ids": ids, "fast_ids": fast_ids})
                    raise ValueError("Rendered template or token IDs differ")
                target = tokenizer(case["continuation"], add_special_tokens=False)["input_ids"]
                if not 1 <= len(target) <= 8:
                    raise ValueError("Continuations must contain 1..8 fixed tokens")
                if len(ids) + len(target) > 128:
                    raise ValueError("Equivalence probe is bounded to 128 prompt/continuation tokens")
                complete_ids = tokenizer(rendered + case["continuation"], add_special_tokens=False)["input_ids"]
                fast_complete_ids = client.call("/tokenize", {"content": rendered + case["continuation"],
                    "add_special": False, "parse_special": True})["tokens"]
                if complete_ids != ids + target or fast_complete_ids != complete_ids:
                    raise ValueError("Continuation token boundary or full-string tokenization differs")
                result = {"id": case["id"], "rendered_prompt": rendered, "prompt_ids": ids, "target_ids": target, "steps": []}
                report["cases"].append(result)
                for position, token in enumerate(target):
                    prefix = ids + target[:position]
                    inputs = torch.tensor([prefix], dtype=torch.long, device=args.device)
                    with torch.no_grad():
                        clean = model(inputs, use_cache=False, logits_to_keep=1).logits[0, -1].float()
                        repeat = model(inputs, use_cache=False, logits_to_keep=1).logits[0, -1].float()
                    if not torch.equal(clean, repeat):
                        report["reference_repeat_failure"] = comparison_failure(clean, repeat, atol=0, rtol=0)
                        raise ValueError("Exact HF forward repeat failed; preserve anomaly, no retry")
                    reference_lp = torch.log_softmax(clean.double(), dim=-1).cpu()
                    request = completion_request(prefix, tokens=1, n_probs=entry["model_config"]["vocab_size"])
                    response = checked_completion(client, request, info["profile"]["context"])
                    fast_lp = full_logprobs(response, len(reference_lp))
                    repeated = checked_completion(client, request, info["profile"]["context"])
                    repeat_lp = full_logprobs(repeated, len(reference_lp))
                    step = {"position": position, **logprob_metrics(reference_lp.tolist(), fast_lp, repeat_lp, token),
                            "reference_logits_sha256": tensor_sha256(clean),
                            "fast_logprob_sha256": hashlib.sha256(json_bytes(fast_lp)).hexdigest()}
                    step["pass"] = (step["max_abs_logprob"] <= config["max_abs_logprob"]
                        and abs(step["kl_reference_to_fast"]) <= config["max_kl_reference_to_fast"]
                        and step["repeat_max_abs_logprob"] <= config["max_repeat_abs_logprob"] and step["top1_match"])
                    result["steps"].append(step)
                    write_new(args.output / f"step-{len(report['cases'])}-{position}.json", step)
                result["sequence_logprob_delta"] = sum(s["fast_target_logprob"] - s["reference_target_logprob"] for s in result["steps"])
                result["pass"] = all(s["pass"] for s in result["steps"]) and abs(result["sequence_logprob_delta"]) <= config["max_abs_sequence_logprob_delta"]
                # Same exact raw-token prompt; compare greedy reference cached/uncached and resident fast generation.
                result["generation"] = {}
                for cache in (False, True):
                    start = time.perf_counter()
                    generation = generate_reference(model, torch.tensor([ids], device=args.device), seed=17,
                        max_new_tokens=8, do_sample=False, eos_token_ids=eos, use_cache=cache)
                    if args.device.startswith("cuda"):
                        torch.cuda.synchronize()
                    result["generation"]["hf_cached" if cache else "hf_full_prefix"] = {
                        "ids": generation.generated_ids, "stop": generation.stop_reason, "wall_seconds": time.perf_counter() - start}
                start = time.perf_counter()
                generated = checked_completion(client, completion_request(ids, n_probs=0), info["profile"]["context"])
                result["generation"]["fast"] = {"raw_response": generated, "wall_seconds": time.perf_counter() - start}
                result["generation"]["raw_ids_match"] = list(result["generation"]["hf_cached"]["ids"]) == generated["tokens"]
            report["workload_gate_passed"] = all(c["pass"] for c in report["cases"]) and report["stop_contract"]["pass"]
            report["status"] = "PASS" if report["workload_gate_passed"] else "FAIL"
    except Exception as exc:
        report["error"] = {"type": type(exc).__name__, "message": str(exc)}
    finally:
        write_new(args.output / "report.json", report)
    print(json.dumps({"status": report["status"], "report": str(args.output / "report.json")}))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
