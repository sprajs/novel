"""Retain all batch observations before interpreting output content."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import time

from .artifacts import sha256_file, strict_json
from .fast_runtime import complete_with_termination, completion_request, write_new


def prediction_jobs(client, info, items, output: Path, *, repeats, slots, options,
                    schema=None, termination="native", eos_ids=()):
    jobs = [(item, repeat) for item in items for repeat in range(repeats)]
    write_new(output / "jobs.json", {"inputs": items, "options": options, "schema": schema,
        "termination_policy": termination, "eos_ids": list(eos_ids),
        "jobs": [{"job_index": index, "input_index": index // repeats, "id": item["id"],
                  "repeat": repeat, "seed": options["seed"] + repeat}
                 for index, (item, repeat) in enumerate(jobs)]})

    def predict(index, item, repeat):
        started = time.perf_counter()
        record = {"job_index": index, "id": item["id"], "repeat": repeat, "status": "FAIL",
                  "messages": item["messages"], "raw_response": None, "response_receipts": [],
                  "parsed_json": None, "termination_policy": termination, "received_tokens": []}
        stage = "prompt"
        try:
            rendered, ids = client.prompt(item["messages"])
            record.update(rendered_prompt=rendered, prompt_ids=ids)
            request = completion_request(ids, **{**options, "seed": options["seed"] + repeat}, schema=schema)
            record["request"] = request
            stage = "generation"

            def receive(chunk_request, response):
                chunk = len(record["response_receipts"])
                path = output / f"response-{index:04d}-{chunk:04d}.json"
                write_new(path, {"job_index": index, "id": item["id"], "repeat": repeat,
                                 "request": chunk_request, "raw_response": response})
                record["response_receipts"].append({"path": path.name, "sha256": sha256_file(path)})
                if isinstance(response.get("tokens"), list):
                    record["received_tokens"].extend(response["tokens"])
                if termination == "native":
                    record["raw_response"] = response

            response, chunks = complete_with_termination(client, request, info["profile"]["context"],
                policy=termination, eos_ids=eos_ids, native_eog_ids=info["eog_token_ids"], on_response=receive,
                response_path=lambda chunk: output / f"response-{index:04d}-{chunk:04d}.http.json")
            if termination == "hf-eos":
                record["adapted_response"] = response
            stage = "output_parse"
            record["parsed_json"] = strict_json(response["content"]) if schema is not None else None
            record["status"] = "PASS"
        except Exception as exc:
            record["error"] = {"stage": stage, "type": type(exc).__name__, "message": str(exc)}
        finally:
            record["wall_seconds"] = time.perf_counter() - started
            record["http_receipts"] = [{"path": p.name, "sha256": sha256_file(p)}
                                      for p in sorted(output.glob(f"response-{index:04d}-*.http.json"))]
            write_new(output / f"record-{index:04d}.json", record)
        return record

    results = []
    with ThreadPoolExecutor(max_workers=slots) as pool:
        futures = {pool.submit(predict, index, item, repeat): index for index, (item, repeat) in enumerate(jobs)}
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as exc:
                # A persistence failure must not abandon other completed jobs.
                results.append({"job_index": futures[future], "status": "FAIL", "received_tokens": [],
                                "error": {"stage": "persistence", "type": type(exc).__name__, "message": str(exc)}})
    return sorted(results, key=lambda record: record["job_index"])
