"""Dependency-free llama.cpp process/HTTP adapter. No PyTorch import or hooks."""

from contextlib import contextmanager
import heapq
import json
import importlib.metadata
import math
import os
from pathlib import Path
import platform
import re
import socket
import subprocess
import time
import tomllib
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .artifacts import json_bytes, sha256_file, strict_json

PIN = "d81235049384534c167caea52b85a694f6103d14"
MAX_RESPONSE_BYTES = 32 * 1024**2


def bounded_int(value, name, minimum, maximum):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{name} must be an integer in [{minimum}, {maximum}]")
    return value


def backend_config(path=Path("configs/fast-backend.json")):
    data = strict_json(path.read_text())
    if data["schema_version"] != 1 or data["commit"] != PIN:
        raise ValueError("Unsupported backend schema or source pin")
    return data


def verify_source(source: Path):
    head = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", str(source), "status", "--porcelain", "--untracked-files=normal"], text=True).strip()
    if head != PIN or dirty:
        raise ValueError("llama.cpp source must be clean and at the pinned commit")
    return head


def write_new(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(json_bytes(value))


def host_record():
    def git(*argv):
        result = subprocess.run(["git", *argv], capture_output=True, text=True, check=False)
        return result.stdout.strip() if result.returncode == 0 else None
    sources = [*Path("src/novel").glob("fast_*.py"), *Path("scripts").glob("fast_*.py")]
    return {"python": platform.python_version(), "platform": platform.platform(),
            "novel_commit": git("rev-parse", "HEAD"), "novel_dirty": bool(git("status", "--porcelain")),
            "adapter_source_sha256": {str(p): sha256_file(p) for p in sorted(sources)},
            "cpu_count": os.cpu_count(), "environment": {k: v for k, v in os.environ.items()
            if k in ("GGML_CUDA_CUBLAS_COMPUTE_TYPE", "GGML_CUDA_MMQ_PREC", "GGML_CUDA_ENABLE_UNIFIED_MEMORY",
                      "GGML_CUDA_FORCE_MMQ", "GGML_CUDA_FORCE_CUBLAS", "CUDA_FORCE_PTX_JIT", "NVIDIA_TF32_OVERRIDE",
                      "CUDA_VISIBLE_DEVICES", "OMP_NUM_THREADS", "OMP_PROC_BIND", "OMP_PLACES")}}


def validate_lock(lock):
    if platform.python_version() != "3.12.14" or platform.system() != "Linux" or platform.machine() != "x86_64":
        raise ValueError("Pinned environments require Linux x86-64 and Python 3.12.14")
    observed = {}
    for package in tomllib.loads(lock.read_text())["package"]:
        if "virtual" in package.get("source", {}):
            continue
        actual = importlib.metadata.version(package["name"])
        if actual != package["version"]:
            raise ValueError(f"Installed {package['name']} differs from lock; use uv sync --locked")
        observed[package["name"]] = actual
    return observed


def reject_implicit_overrides():
    if any(k.startswith("LLAMA_ARG_") for k in os.environ) or "GGML_CUDA_ENABLE_UNIFIED_MEMORY" in os.environ:
        raise ValueError("Remove implicit LLAMA_ARG_* and unified-memory overrides; no silent configuration/offload")


def verify_build(build: Path, profile: str):
    receipt = strict_json((build / "receipt.json").read_text())
    if receipt["commit"] != PIN or receipt["profile"] != profile:
        raise ValueError("Build receipt source/profile mismatch")
    for name, digest in receipt["runtime_hashes"].items():
        if sha256_file(build / "bin" / name) != digest:
            raise ValueError(f"Build integrity failure: {name}")
    for required in ("llama-server", "llama-bench", "llama-quantize"):
        if required not in receipt["runtime_hashes"]:
            raise ValueError("Incomplete build receipt")
    return receipt


def verify_artifact(model: Path):
    receipt = strict_json(model.with_suffix(".gguf.json").read_text())
    if receipt["llama_commit"] != PIN or receipt["artifact_sha256"] != sha256_file(model):
        raise ValueError("GGUF integrity or converter pin mismatch")
    if receipt["quantization"] not in ("F16", "Q8_0", "Q4_K_M"):
        raise ValueError("Unsupported artifact type")
    return receipt


def gpu_preflight(profile_name, profile, artifact, slots):
    if profile["cuda_arch"] is None:
        return {"status": "SKIP", "reason": "CPU profile"}
    if os.environ.get("CUDA_VISIBLE_DEVICES") not in (None, "0"):
        raise ValueError("GPU recipe targets physical GPU 0; unset CUDA_VISIBLE_DEVICES or use 0")
    raw = subprocess.check_output(["nvidia-smi", "--id=0", "--query-gpu=name,compute_cap,memory.total,memory.free,driver_version",
                                   "--format=csv,noheader,nounits"], text=True).strip()
    name, capability, total, free, driver = [x.strip() for x in raw.split(",")]
    expected = "RTX 2080 Ti" if profile_name == "local-2080ti" else "RTX 5090"
    expected_capability = "7.5" if profile_name == "local-2080ti" else "12.0"
    if not name.endswith(expected) or capability != expected_capability:
        raise ValueError("GPU name/compute capability differs from requested profile")
    minimum_mib = 10000 if profile_name == "local-2080ti" else 30000
    if float(total) < minimum_mib:
        raise ValueError("GPU capacity differs from full-card profile")
    if tuple(int(x) for x in driver.split(".")) < (570, 124, 6):
        raise ValueError("Pinned CUDA 12.8 Update 1 recipe requires Linux driver >=570.124.06")
    layers = 36 if artifact["model_key"] == "qwen3_8b" else 28
    kv_bytes = 2 * layers * 8 * 128 * 2 * slots * profile["context"]
    planning_bytes = artifact["artifact_bytes"] + kv_bytes + 2 * 1024**3
    if planning_bytes > 0.8 * float(free) * 1024**2:
        raise ValueError("Artifact + F16 KV + 2 GiB reserve exceeds 80% of free VRAM; no fit promise or automatic fallback")
    return {"status": "PASS", "name": name, "compute_capability": capability,
            "total_mib": float(total), "free_mib": float(free), "driver": driver,
            "planning_bytes": planning_bytes, "interpretation": "Conservative planning only; measure actual allocation and full GPU offload."}


def verify_full_offload(log_text):
    match = re.search(r"offloaded (\d+)/(\d+) layers to GPU", log_text)
    if match is None or match[1] != match[2] or int(match[1]) == 0:
        raise ValueError("Full GPU offload was not confirmed in runtime log")
    return {"offloaded_layers": int(match[1]), "total_layers": int(match[2])}


class Client:
    def __init__(self, url: str, timeout=180):
        self.url, self.timeout = url, timeout

    def call(self, endpoint, payload=None, *, response_path=None):
        request = Request(self.url + endpoint, data=None if payload is None else json_bytes(payload),
                          headers={"Content-Type": "application/json"})
        http_error = None
        try:
            response = urlopen(request, timeout=self.timeout)
        except HTTPError as exc:
            response, http_error = exc, exc
        with response:
            body = response.read(MAX_RESPONSE_BYTES + 1)
        if response_path is not None:
            # Retain even invalid JSON/HTTP failures before interpretation.
            with response_path.open("xb") as handle:
                handle.write(body)
        if len(body) > MAX_RESPONSE_BYTES:
            raise ValueError("Server response exceeds 32 MiB bound")
        if http_error is not None:
            raise http_error
        return strict_json(body.decode())

    def prompt(self, messages):
        if not isinstance(messages, list) or not 1 <= len(messages) <= 16:
            raise ValueError("messages must contain 1..16 text turns")
        for message in messages:
            if (set(message) != {"role", "content"} or message["role"] not in ("user", "assistant", "system")
                    or not isinstance(message["content"], str) or len(message["content"]) > 16384):
                raise ValueError("Only bounded text chat turns are supported")
        rendered = self.call("/apply-template", {"messages": messages})["prompt"]
        ids = self.call("/tokenize", {"content": rendered, "add_special": False, "parse_special": True})["tokens"]
        return rendered, ids


def completion_request(ids, *, tokens=8, seed=17, cache_prompt=False, n_probs=20, schema=None,
                       temperature=-1.0, top_k=0, top_p=1.0, min_p=0.0):
    bounded_int(tokens, "tokens", 1, 2048)
    bounded_int(seed, "seed", 0, 2**32 - 2)
    bounded_int(n_probs, "n_probs", 0, 152064)
    if not ids or any(type(x) is not int or x < 0 for x in ids):
        raise ValueError("prompt must contain explicit token IDs")
    if type(cache_prompt) is not bool:
        raise ValueError("cache_prompt must be boolean")
    bounded_int(top_k, "top_k", 0, 152064)
    for name, value, lower, upper in (("temperature", temperature, -1, 2), ("top_p", top_p, 0, 1), ("min_p", min_p, 0, 1)):
        if type(value) not in (int, float) or not math.isfinite(value) or not lower <= value <= upper:
            raise ValueError(f"Invalid {name}")
    if temperature == 0 or top_p == 0:
        raise ValueError("Use temperature=-1 for greedy, a positive value for sampling, and top_p>0")
    samplers = ["temperature"] if temperature < 0 else ["top_k", "top_p", "min_p", "temperature"]
    request = {"prompt": ids, "n_predict": tokens, "seed": seed, "temperature": temperature,
               "top_k": top_k, "top_p": top_p, "min_p": min_p, "typical_p": 1.0,
               "repeat_penalty": 1.0, "presence_penalty": 0.0, "frequency_penalty": 0.0,
               "dry_multiplier": 0.0, "mirostat": 0, "samplers": samplers,
               "cache_prompt": cache_prompt, "return_tokens": True, "n_probs": n_probs,
               "post_sampling_probs": False, "stream": False, "stop": [], "ignore_eos": False}
    if schema is not None:
        request["json_schema"] = schema
    return request


def checked_completion(client, request, context):
    validate_completion_request(request, context)
    return validate_completion(client.call("/completion", request), request)


def validate_completion_request(request, context):
    if len(request["prompt"]) + request["n_predict"] >= context:
        raise ValueError("Prompt plus generation cap must leave one token of per-slot context slack")


def validate_completion(result, request):
    if result.get("truncated") is not False or result.get("tokens_evaluated") != len(request["prompt"]):
        raise ValueError("Server truncated or changed prompt token count")
    if not isinstance(result.get("tokens"), list) or result.get("stop_type") not in ("limit", "eos", "word"):
        raise ValueError("Missing raw token/stop information")
    return result


def complete_with_termination(client, request, context, *, policy="native", eos_ids=(), native_eog_ids=(),
                              on_response=None, response_path=None):
    """Explicit greedy chunk continuation; never mask logits or edit tokenizer metadata.

    Native chunks retain their own stop reasons. The adapter resumes only extra
    native EOG IDs, preserving them in the prefix/output. Text is decoded from
    all IDs with special spellings included, matching HF skip_special_tokens=False.
    """
    validate_completion_request(request, context)
    if policy not in ("native", "hf-eos"):
        raise ValueError("Unknown termination policy")
    if policy == "hf-eos":
        if (request["temperature"] >= 0 or request["cache_prompt"] or request.get("json_schema") is not None
                or request.get("grammar") or request.get("logit_bias") or request["ignore_eos"] or request["stop"]):
            raise ValueError("hf-eos requires greedy unconstrained generation, no biases or prompt reuse")
        if not eos_ids or not set(eos_ids) <= set(native_eog_ids):
            raise ValueError("Native stops must contain all configured HF EOS IDs")
    chunks, generated, probabilities = [], [], []
    while len(generated) < request["n_predict"]:
        chunk_request = {**request, "prompt": request["prompt"] + generated,
                         "n_predict": request["n_predict"] - len(generated)}
        kwargs = {} if response_path is None else {"response_path": response_path(len(chunks))}
        response = client.call("/completion", chunk_request, **kwargs)
        # Receipt callback runs before token-contract validation or output parsing.
        if on_response is not None:
            on_response(chunk_request, response)
        chunks.append({"request": chunk_request, "response": response})
        validate_completion(response, chunk_request)
        if policy == "native":
            return response, chunks
        tokens = response["tokens"]
        if (not tokens or len(tokens) > chunk_request["n_predict"] or
                any(type(t) is not int or t < 0 for t in tokens)):
            raise ValueError("Missing/invalid raw chunk tokens; cannot align termination")
        if any(t in native_eog_ids for t in tokens[:-1]):
            raise ValueError("Native chunk contains an interior EOG token")
        last = tokens[-1]
        if (response["stop_type"] == "eos") != (last in native_eog_ids):
            raise ValueError("Native terminal token and stop reason disagree")
        if response["stop_type"] not in ("eos", "limit"):
            raise ValueError("Unexpected native stopping rule")
        generated.extend(tokens)
        probabilities.extend(response.get("completion_probabilities", []))
        if last in eos_ids or len(generated) == request["n_predict"]:
            break
        if response["stop_type"] != "eos":
            raise ValueError("Native stopped below the cap without an extra EOG")
    content = client.call("/detokenize", {"tokens": generated})["content"]
    return {"content": content, "tokens": generated, "completion_probabilities": probabilities,
            "stop_type": "eos" if generated[-1] in eos_ids else "limit", "truncated": False,
            "tokens_evaluated": len(request["prompt"]), "tokens_predicted": len(generated),
            "adapter": {"termination": "hf-eos", "eos_ids": list(eos_ids), "native_eog_ids": list(native_eog_ids),
                        "chunk_count": len(chunks), "raw_text_contract": "all token spellings, including special/EOS tokens",
                        "kernel_contract": "native KV within chunks; clean full-prefix prefill after extra EOG"}}, chunks


def server_command(binary, model, profile, *, port, slots=1, flash_attention=False, thinking=False):
    bounded_int(slots, "slots", 1, 8)
    return [str(binary), "--model", str(model), "--host", "127.0.0.1", "--port", str(port),
            "--ctx-size", str(profile["context"] * slots), "--parallel", str(slots),
            "--threads", str(profile["threads"]), "--threads-batch", str(profile["threads"]),
            "--n-gpu-layers", str(profile["gpu_layers"]), "--split-mode", "none",
            "--batch-size", "128", "--ubatch-size", "128", "--cache-type-k", "f16",
            "--cache-type-v", "f16", "--flash-attn", "on" if flash_attention else "off",
            "--no-context-shift", "--no-cache-prompt", "--no-warmup", "--jinja",
            "--reasoning", "on" if thinking else "off", "--metrics", "--verbosity", "4",
            "--device", "none" if profile["cuda_arch"] is None else "CUDA0", "--fit", "off", "--offline"]


@contextmanager
def server(build, model, profile_name, log, *, slots=1, flash_attention=False, thinking=False, context=None):
    receipt = verify_build(build, profile_name)
    artifact = verify_artifact(model)
    profile = backend_config()["profiles"][profile_name]
    if context is not None:
        profile = {**profile, "context": bounded_int(context, "context", 128, 8192)}
    reject_implicit_overrides()
    hardware = gpu_preflight(profile_name, profile, artifact, slots)
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    argv = server_command(build / "bin" / "llama-server", model, profile, port=port, slots=slots,
                          flash_attention=flash_attention, thinking=thinking)
    with log.open("xb") as handle:
        started = time.perf_counter()
        process = subprocess.Popen(argv, stdout=handle, stderr=handle)
        info = None
        try:
            client = Client(f"http://127.0.0.1:{port}")
            deadline = time.monotonic() + 180
            while True:
                if process.poll() is not None:
                    raise RuntimeError(f"llama-server exited {process.returncode}; inspect {log}")
                try:
                    client.call("/health")
                    break
                except (URLError, HTTPError):
                    if time.monotonic() > deadline:
                        raise TimeoutError("Server startup exceeded 180 seconds")
                    time.sleep(0.2)
            props = client.call("/props")
            if Path(props["model_path"]).resolve() != model.resolve() or props["total_slots"] != slots:
                raise ValueError("Server loaded model or slot configuration differs from request")
            log_text = log.read_text(errors="replace")
            eog_ids = sorted({int(x) for x in re.findall(r"EOG token\s*=\s*(\d+)", log_text)})
            offload = None
            if profile["cuda_arch"] is not None:
                offload = verify_full_offload(log_text)
            info = {"argv": argv, "build": receipt, "artifact": artifact,
                           "props": props, "host": host_record(), "profile": profile,
                           "slots": slots, "startup_warmup": False, "hardware": hardware,
                           "eog_token_ids": eog_ids, "startup_seconds": time.perf_counter() - started,
                           "full_gpu_offload": offload}
            yield client, info
        finally:
            if info is not None:
                try:
                    status = Path(f"/proc/{process.pid}/status").read_text()
                    info["server_peak_rss_bytes"] = int(re.search(r"VmHWM:\s*(\d+)", status)[1]) * 1024
                except (OSError, TypeError):
                    info["server_peak_rss_bytes"] = None
                if profile["cuda_arch"] is not None:
                    try:
                        info["gpu_memory_after_requests_mib"] = subprocess.check_output(
                            ["nvidia-smi", "--id=0", "--query-gpu=memory.used,memory.free", "--format=csv,noheader,nounits"], text=True).strip()
                    except subprocess.CalledProcessError:
                        info["gpu_memory_after_requests_mib"] = None
                    info["gpu_peak_memory_measured"] = False
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def full_logprobs(result, vocab_size):
    """Fail closed if the backend provides partial, invalid or floored distributions."""
    records = result.get("completion_probabilities", [])
    if len(records) != 1:
        raise ValueError("Expected one next-token probability record")
    top = records[0].get("top_logprobs", [])
    mapping = {item["id"]: item["logprob"] for item in top}
    if len(top) != vocab_size or set(mapping) != set(range(vocab_size)):
        raise ValueError("Backend did not return the complete matching vocabulary")
    values = [mapping[i] for i in range(vocab_size)]
    if any(type(x) not in (float, int) or not math.isfinite(x) or x <= -1e8 for x in values):
        raise ValueError("Nonfinite/floored logprobs; full likelihood comparison unsupported")
    if abs(sum(math.exp(x) for x in values) - 1.0) > 0.0001:
        raise ValueError("Unnormalized probabilities; cannot compare likelihoods")
    return values


def logprob_metrics(reference, fast, repeat, target):
    """Compare raw values; compute KL only between normalized distributions."""
    if len(reference) != len(fast) or len(fast) != len(repeat) or not reference:
        raise ValueError("Likelihood vectors must have identical nonempty support")
    if not all(math.isfinite(v) for values in (reference, fast, repeat) for v in values):
        raise ValueError("Nonfinite likelihood vector")
    mass = math.fsum(math.exp(v) for v in fast)
    reference_mass = math.fsum(math.exp(v) for v in reference)
    if abs(reference_mass - 1) > 1e-9 or abs(mass - 1) > 1e-4:
        raise ValueError("Likelihood normalization outside predeclared bound")
    log_normalizer = math.log(mass)
    errors = [f - r for r, f in zip(reference, fast, strict=True)]
    worst = heapq.nlargest(min(8, len(errors)), range(len(errors)), key=lambda i: abs(errors[i]))
    return {"target_id": target, "reference_target_logprob": reference[target],
            "fast_target_logprob": fast[target], "normalized_fast_target_logprob": fast[target] - log_normalizer,
            "fast_log_normalizer": log_normalizer, "raw_probability_mass_error": mass - 1,
            "max_abs_logprob": max(abs(x) for x in errors),
            "kl_reference_to_fast": math.fsum(math.exp(r) * (r - f + log_normalizer)
                                              for r, f in zip(reference, fast, strict=True)),
            "repeat_max_abs_logprob": max(abs(a - b) for a, b in zip(repeat, fast, strict=True)),
            "top1_match": max(range(len(reference)), key=reference.__getitem__) == max(range(len(fast)), key=fast.__getitem__),
            "worst_token_ids": worst, "worst_logprob_deltas": [errors[i] for i in worst]}
