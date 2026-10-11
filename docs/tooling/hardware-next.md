# GPU implementation and remaining hardware gates

The stacked profiles increment now implements separate cu126/cu128 locks,
strict detected-device/runtime/capacity checks, CUDA loading, capture/patching,
raw-token generation, cache validation, optional activation gradients and
shareable PASS/FAIL/SKIP diagnostics. Follow the executable
[profile guide](execution-profiles.md) and [model sizing](../models/hardware-suitability.md).
The CPU lock and original model snapshots are preserved; rental adds a pinned 8B snapshot.

Real GPU validation remains open: this cloud exposes no CUDA device. Run the
provided preflight and 0.6B forward commands on the selected host, then optional
0.6B gradients and 1.7B forward on the 2080 Ti or 8B forward on the RTX 5090.
Review exact no-op checks, numerical parity
errors and allocated/reserved peaks before expanding. Prospective FP16/BF16
tolerances are not empirical calibration. No GPU throughput or largest-fit claim
is supported. Rental defaults target the real RTX5090's full 32 GB capacity,
clamped to detected CUDA bytes with normal allocation headroom. The optional
24 GiB custom profile is explicit and separate from that primary recommendation.

Fast inference can wait: there is no GPU evidence that justifies an extra large
backend install now. The minimal later comparison is HF unquantized eager FP16,
then a pinned llama.cpp F16 GGUF derived from the same canonical snapshot. Q8 is
a separate numerical condition. vLLM is a conditional competitor: current docs
include SM75, but release-specific attention kernels, wheel architectures,
dependency constraints and 11 GB fit need actual tests. SGLang is deferred.

For each backend preserve conversion/build commits, tokenizer/template/stop
settings, exact input token IDs, and fixed-prefix logit or log-probability parity
before free generation. Equal seeds do not imply identical samplers across
engines. Measure load separately from warm prefill, time to first token, decode,
total latency, peak VRAM and tokens processed. Include three short warmups and
five repetitions of one fixed workload before expanding. Run in an isolated
backend environment; retain its own lock/build receipt. A replay of quantized
text through HF is analysis of that text, not HF-generated baseline behavior.

Do not rent compute, create credentials or change device security as part of
these gates. Those decisions remain outside this increment's authorization.
