#!/usr/bin/env python3
"""CPU F16 forced-token boundary/custody test; never a probability measurement."""
import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from novel.fast_runtime import complete_with_termination, completion_request, server, write_new
from novel.models import model_entry, snapshot_path, verify_snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gguf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    os.chdir(ROOT)
    from transformers import AutoTokenizer
    entry = model_entry(ROOT / "configs/models.json", "qwen3_0_6b")
    snapshot = snapshot_path(ROOT / ".cache/models", "qwen3_0_6b", entry)
    hashes = verify_snapshot(snapshot, entry)
    tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True, trust_remote_code=False)
    args.output.mkdir(parents=True, exist_ok=False)
    report = {"status": "FAIL", "cases": [], "snapshot_hashes": hashes,
        "purpose": "Forced-token termination/custody fixtures only. Logged transport logit biases alter sampling; these are not raw-probability or behavioral equivalence observations."}
    try:
        with server(ROOT / ".cache/fast/cloud-cpu", args.gguf.resolve(), "cloud-cpu", args.output / "server.log") as (client, info):
            report["runtime"] = info
            if info["artifact"]["quantization"] != "F16" or info["artifact"]["source_file_sha256"] != hashes:
                raise ValueError("Probe requires the exact registry-derived CPU F16 artifact")
            messages = [{"role": "user", "content": "Return a short reply."}]
            rendered, ids = client.prompt(messages)
            report.update(rendered_prompt=rendered, prompt_ids=ids)
            eos = entry["token_ids"]["generation_eos_token_ids"]
            primary_eos = entry["token_ids"]["config_eos_token_id"]
            for token in info["eog_token_ids"]:
                result = {"first_token": token, "transport_requests": []}
                report["cases"].append(result)

                class ForcedTransport:
                    def call(self, endpoint, request):
                        if endpoint != "/completion":
                            return client.call(endpoint, request)
                        forced = token if not result["transport_requests"] else primary_eos
                        actual = {**request, "logit_bias": [[forced, 10000.0]]}
                        response = client.call(endpoint, actual,
                            response_path=args.output / f"forced-{token}-{len(result['transport_requests'])}.http.json")
                        result["transport_requests"].append({"request": actual, "response": response})
                        return response

                response, chunks = complete_with_termination(ForcedTransport(), completion_request(ids, tokens=2, n_probs=2),
                    info["profile"]["context"], policy="hf-eos", eos_ids=eos, native_eog_ids=info["eog_token_ids"])
                expected = [token] if token in eos else [token, primary_eos]
                expected_text = tokenizer.decode(expected, skip_special_tokens=False)
                result.update(response=response, native_chunks=chunks, expected_tokens=expected, expected_text=expected_text)
                literal = tokenizer.decode([token], skip_special_tokens=False)
                reference_encoding = tokenizer(literal, add_special_tokens=False)["input_ids"]
                native_encoding = client.call("/tokenize", {"content": literal, "add_special": False,
                    "parse_special": True})["tokens"]
                result["literal_tokenization"] = {"text": literal, "reference_ids": reference_encoding,
                    "native_ids": native_encoding, "match": reference_encoding == native_encoding,
                    "interpretation": "Diagnostic only; adapter continuation uses retained raw IDs without retokenization"}
                result["pass"] = response["tokens"] == expected and response["content"] == expected_text and response["stop_type"] == "eos"
                write_new(args.output / f"case-{token}.json", result)
            report["status"] = "PASS" if all(c["pass"] for c in report["cases"]) else "FAIL"
    except Exception as exc:
        report["error"] = {"type": type(exc).__name__, "message": str(exc)}
    finally:
        write_new(args.output / "report.json", report)
    print(json.dumps({"status": report["status"], "report": str(args.output / "report.json")}))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
