# Separate fast prediction runtime

Use the existing **PyTorch / Transformers eager path** for weights, architectures,
actual residual captures, activation gradients and interventions. Use the new
**native llama.cpp server** for repeated predictions from a resident GGUF model.
Neither matching answers nor equal seeds establish equal logits, likelihoods or
causal effects. The reference locks, registry, hooks and failed CPU evidence are
unchanged. See [reference profiles](execution-profiles.md),
[the unresolved repeatability anomaly](../validation/cpu-repeatability-investigation.md)
and [executed CPU evidence](../validation/fast-cpu.md).

## Backend choice, checked 11 October 2026

[llama.cpp](https://github.com/ggml-org/llama.cpp) uses GGML and provides native
CPU/CUDA kernels, GGUF conversion, quantization and a resident HTTP server.
It directly matches the requested lean CPU/GPU path. The prediction client uses
only Python's standard library; it installs neither Torch nor a Python inference
wrapper. Offline conversion uses a separate CPU environment with the same reference pins
and one extra pinned SentencePiece dependency.

| Option | Official latest stable observed | Decision |
| --- | --- | --- |
| llama.cpp | `v0.6.0`, 5 October | Selected; inspectable native build, artifact and probability semantics. |
| Ollama | `v0.40.3`, 11 October | Convenient managed distribution in the GGML ecosystem. Native llama.cpp gives this project direct control over exact conversion and backend flags; Ollama release/model tags are a separate provenance contract. |
| vLLM | `v0.31.0`, 5 October | Possible later GPU batching competitor. Current [requirements](https://docs.vllm.ai/en/latest/getting_started/installation/gpu/) include SM75, but release dependencies require a different Torch/Transformers stack. No blanket Turing incompatibility claim. |
| SGLang | `v0.5.21`, 2 October | Deferred; substantial compiled serving/attention dependencies. No installation or GPU comparison performed here. |

Release APIs, dependency observations and source hashes are retained in
[fast-sources.json](fast-sources.json). Selection is about scope and CPU coverage,
not an unmeasured throughput ranking.

**The actual stable source pin is
`d81235049384534c167caea52b85a694f6103d14`.** The release API's
`target_commitish=8345f333951c661d166b00e6f9362e553768f292` differs from the
commit behind the annotated tag. The official [tag reference](https://api.github.com/repos/ggml-org/llama.cpp/git/ref/tags/v0.6.0)
points to object `69ecae922d2b60c1fa8c590279f4e2099af75111`; its
[peeled object](https://api.github.com/repos/ggml-org/llama.cpp/git/tags/69ecae922d2b60c1fa8c590279f4e2099af75111)
is `d812350...`. Actual Git checkout agrees. Scripts verify that full commit and
reject dirty source; rolling releases and mutable model tags are excluded.

## Explicit installation and builds

Run commands from the repository root on Linux x86-64. Prerequisites are Python
**3.12.14**, uv **0.12.23**, Git, a C/C++ compiler and OpenMP. The tested CPU host
uses Debian 13 and GNU **14.2.0**. The separate build lock pins
`cmake==4.1.3` and `ninja==1.13.0`, including distribution hashes.

```bash
export UV_CACHE_DIR="$PWD/.cache/uv"
uv sync --locked --project environments/fast-build
environments/fast-build/.venv/bin/python scripts/fast_build.py --profile cloud-cpu
```

The script clones the tagged source into `.cache/llama.cpp`, checks the commit,
and builds server/benchmark/quantizer targets under `.cache/fast/cloud-cpu`.
CUDA, HTTPS, examples and upstream tests are disabled for this CPU build.
Receipts hash executables/shared libraries and record commands, compiler,
linkage and CMake cache. Host compiler/libc/OpenMP, CUDA and driver are recorded
prerequisites, not a hermetic system-image lock. Native CPU builds target the
build host's ISA; rebuild when moving to a different CPU.

| Profile | Default model | Build / starting server condition |
| --- | --- | --- |
| `cloud-cpu` | Qwen3-0.6B | Native CPU, 5 threads, 512 tokens per slot, GPU layers 0 |
| `local-2080ti` | Qwen3-1.7B; first test 0.6B | CUDA 12.8 Update 1, `CMAKE_CUDA_ARCHITECTURES=75`, 2048 tokens per slot |
| `rental` | Qwen3-8B; first test 0.6B | CUDA 12.8 Update 1, `CMAKE_CUDA_ARCHITECTURES=120`, 2048 tokens per slot |

On an **already provisioned** selected GPU host:

```bash
environments/fast-build/.venv/bin/python scripts/fast_build.py --profile local-2080ti
# Or, on the RTX5090 host:
environments/fast-build/.venv/bin/python scripts/fast_build.py --profile rental
```

The recipe requires CUDA **12.8.1**, specifically `nvcc V12.8.90`, a supported
host compiler and Linux driver **570.124.06 or newer**. This is separate from
reference cu126/cu128 PyTorch wheels: a wheel does not supply a complete native
build toolkit. [NVIDIA's component and driver table](https://docs.nvidia.com/cuda/archive/12.8.1/cuda-toolkit-release-notes/index.html)
distinguishes toolkit components from the CUDA minor-compatibility floor.
No system installer or GPU rental is included.

[NVIDIA lists](https://developer.nvidia.com/cuda/gpus) RTX2080Ti as **SM75** and
RTX5090 as **SM120**. Both appear in the pinned
[CUDA build source](https://github.com/ggml-org/llama.cpp/blob/d81235049384534c167caea52b85a694f6103d14/ggml/src/ggml-cuda/CMakeLists.txt),
which requires CUDA 12.8 for SM120. The
[Turing guide](https://docs.nvidia.com/cuda/turing-tuning-guide/index.html)
describes FP16/integer tensor-core support; native BF16 tensor-core arithmetic
is absent. F16 weights and F16 KV are the starting recipe on both cards.
Blackwell-specific low-bit kernels do not make Q4_K_M equivalent to NVFP4.

GPU prediction checks physical GPU0's exact name/capability/capacity, records
free/total MiB and driver, and requires a log confirming full layer offload.
It rejects other device mappings, implicit unified memory and automatic fit
adjustment. A planning allowance includes artifact bytes, F16 KV across all
slots and a 2 GiB reserve, within 80% of free VRAM. This is an estimate, not an
OOM/fit guarantee. **No GPU build, execution, throughput or measured fit is
established in this cloud.** Successful builds are reverified; failed logs and
incomplete artifacts are preserved. Inspect and deliberately remove an incomplete
local build/artifact before another attempt.

## Exact artifacts and quantization provenance

The offline converter uses [the existing registry](../../configs/models.json):

| Model | HF model/tokenizer revision |
| --- | --- |
| Qwen3-0.6B | `c1899de289a04d12100db370d81485cdf75e47ca` |
| Qwen3-1.7B | `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e` |
| Qwen3-8B | `b968826d9c46dd6066d109eabc6255188de91218` |

```bash
uv sync --locked                         # existing CPU reference environment
uv run --locked novel-model download --model qwen3_0_6b --max-bytes 3221225472
uv sync --locked --project environments/fast-convert
environments/fast-convert/.venv/bin/python scripts/fast_convert.py --model qwen3_0_6b --type F16
environments/fast-convert/.venv/bin/python scripts/fast_convert.py --model qwen3_0_6b --type Q8_0
```

Conversion verifies all source file hashes and never downloads. Its separate lock
retains Torch2.8/Transformers4.57.6 and adds `sentencepiece==0.2.1`: the upstream
Qwen converter imports SentencePiece before its missing-file fallback to BPE.
The original reference lock and environment are not modified. Receipts preserve
source revision/tokenizer/template hashes, source tree and converter hash,
commands, selected GGUF metadata and resulting artifact SHA256. Q8_0 and optional
Q4_K_M derive explicitly from the verified F16 parent with a hashed quantizer,
**without an importance matrix**. Mixed tensor types are part of those recipes;
the label does not mean every tensor has the same bit width. F16 conversion of
BF16 source weights is itself a numerical condition; CPU reference FP32 loading
preserves the original BF16 values.

Larger source downloads are explicit user-run operations on the selected host:
existing example budgets are 5 GiB for 1.7B and 20 GiB for 8B. Allow storage for source
weights plus F16 and any extra quantized artifact, and transient conversion RAM.
The converter uses the isolated CPU converter environment even for GPU artifacts. Only 0.6B was
downloaded in this cloud; no 1.7B/8B weights, rental or installation on the user's
computers occurred.

Official Qwen GGUF repos are a separate distribution option. Their full immutable
revisions, file sizes and expected Hub hashes are in the source ledger. Small
repos currently provide Q8_0; 8B also provides Q4_K_M/Q5/Q6 variants. Those older
repos do not establish derivation from this registry's July complete snapshots
and tokenizer/templates, so this adapter uses verified local conversions.

## Resident server, batching and traces

```bash
MODEL_DIR="$PWD/.cache/gguf/qwen3_0_6b-c1899de289a04d12100db370d81485cdf75e47ca"
python scripts/fast_predict.py --profile cloud-cpu --gguf "$MODEL_DIR/Q8_0.gguf" \
  --inputs configs/fast-prompts.jsonl --repeats 3 --tokens 32 --output runs/fast-q8
python scripts/fast_predict.py --profile cloud-cpu --gguf "$MODEL_DIR/F16.gguf" \
  --inputs configs/fast-structured.jsonl --schema configs/fast-schema.json \
  --tokens 32 --repeats 1 --output runs/fast-json
```

Each invocation loads one model into one loopback server and submits the entire
JSONL batch. `--slots 2` enables concurrent requests/continuous batching and
scales context/KV allocation; measure that separate condition. `--context 4096`
is an explicit per-slot override (128..8192), and `--tokens` allows 1..2048.
Prompt plus output cap must fit; larger traces require an explicit smaller
`--n-probs` or splitting the workload within the saved trace budget. The default is
one slot, F16 K/V, Flash Attention off, no shifting, no startup warmup, no prompt
reuse and greedy decoding. Output directories must be new. Completed observations
and failed reports survive; input and token/probability budgets bound output.

For stochastic non-thinking predictions add `--temperature 0.7 --top-k 20
--top-p 0.8 --min-p 0 --seed 17`. Seed increases by repeat index and each request
is saved. Identical HF/native seeds do not imply identical RNG or samplers.
`--thinking` enables generated thinking text in the template. `--cache-prompt`
and `--flash-attention` are explicit performance conditions outside the default
likelihood gate's scope.

The client saves `/apply-template` text and `/tokenize` IDs, then passes exact
IDs to `/completion`. Unexpected truncation or prompt counts fail. JSON schema
uses the native grammar builder's [documented subset](https://github.com/ggml-org/llama.cpp/blob/d81235049384534c167caea52b85a694f6103d14/tools/server/README.md);
returned text is parsed as strict JSON. This client is not a general semantic
JSON Schema validator. Grammar constraints change the generation distribution;
these are not unconstrained likelihood samples. Raw responses are retained.

| Output | Meaning / limit |
| --- | --- |
| `content`, including possible `<think>` text | Generated reasoning/answer text, not hidden activations. |
| `tokens` | Raw native output IDs; text retokenization need not recover them. HF and native EOG retention conventions need inspection. |
| `completion_probabilities` | Pre-sampling model logprobs/top-N entries (`post_sampling_probs=false`), not raw logits or hidden states. Partial traces cannot establish full KL or score missing target IDs. |
| Timings/logs | Native counts, performance and config evidence. Non-streaming request wall time does not measure time-to-first-token. |
| Reference SafeTensors | Actual named residual captures from the retained validated HF hook path. |

## Benchmarks and likelihood gates

```bash
python scripts/fast_bench.py --profile cloud-cpu --gguf "$MODEL_DIR/F16.gguf" \
  --prompt-tokens 32 --decode-tokens 8 --repetitions 3 --output runs/bench-f16
python scripts/fast_bench.py --profile cloud-cpu --gguf "$MODEL_DIR/Q8_0.gguf" \
  --prompt-tokens 32 --decode-tokens 8 --repetitions 3 --output runs/bench-q8
.venv/bin/python scripts/fast_equivalence.py --profile cloud-cpu --model qwen3_0_6b \
  --gguf "$MODEL_DIR/F16.gguf" --output runs/equivalence-f16
.venv/bin/python scripts/fast_equivalence.py --profile cloud-cpu --model qwen3_0_6b \
  --gguf "$MODEL_DIR/Q8_0.gguf" --output runs/equivalence-q8
```

The native benchmark retains synthetic-token prefill/decode samples,
mean/dispersion, receipts and peak child RSS. Native warmup is retained/labeled.
These microbenchmarks are separate from task throughput, identical HF workloads
and cold latency. Resident request timings exclude startup/model load.

Run equivalence in the selected **reference** lock/interpreter: root CPU, cu126
for 2080Ti, cu128 for 5090. On GPU pass `--device cuda:0 --dtype float16`, after
passing the reference profile smoke. The checker verifies source hashes,
template source/rendered bytes, IDs and complete stop/EOG sets. Each fixed target
continuation token uses a teacher-forced full prefix. HF cache is disabled and
two exact clean forwards are required. A repeat discrepancy preserves raw
failure evidence and stops; it is never retried into a passing observation.

One native unconstrained greedy step requests `n_probs=vocab_size` with
pre-sampling probabilities and no prompt reuse. The pinned server computes
softmax on the full pre-sampler logits. The checker requires a complete matching
vocabulary and normalized finite logprobs, rejecting partial tails and float
underflow sentinels. It repeats the request and reports maximum absolute logprob
error, reference-to-fast KL, target/summed sequence logprob deltas, top-1 agreement,
repeat drift and hashes. KL renormalizes the complete server distribution in
FP64; raw logprobs, its log normalizer and probability-mass error are retained
separately. This accounts for rounding in the native FP32 softmax and does not
rewrite the actual sampled output. Raw logits are not exposed by this HTTP adapter.
Full-vocabulary extraction is an expensive diagnostic, not the default fast trace.

[Predeclared engineering thresholds](../../configs/fast-equivalence.json) are
0.1 maximum absolute logprob error, 1e-4 KL, 0.05 absolute sequence-logprob delta
and exact native repeat probabilities. These are smoke gates, **not calibrated
scientific tolerances**. Quantization never relaxes them automatically. The same
script times eight-token greedy HF cached, HF full-prefix and native generation
from identical prompt IDs; inspect their separate cache arithmetic/token paths.

A pass covers only those prefixes, artifact, kernels, threads, cache and context.
`scientific_interchangeability` remains **false** even on a pass. Before scientific
likelihood measurement, extend the predeclared workload to actual scored
sequences/token boundaries and calibrate effect-relevant error budgets. Stop-set mismatches keep the aggregate gate failed while the
predeclared fixed-prefix diagnostics continue to quantify probability drift. Changing
quantization, template, stops, sampling, cache reuse, batching, KV precision,
Flash Attention or kernels requires another named condition and validation.
No hidden-activation or intervention equivalence is certified. The documented
CPU repeatability anomaly and all untested GPU caveats remain open.

## Alignment with the observational protocol

The [merged measurement protocol](../../Plan/measurement-protocol.md) distinguishes
raw model probability `p`, decoder-induced sampling probability `q`, exact token
paths and semantic event recovery. This adapter is measurement infrastructure;
it admits no historical candidates, labels no discoveries and estimates no
semantic event mass. There are still zero certified historical candidates.

The engineering continuation probes omit a terminal token and score **prefix
cylinders**, not complete stopped trajectories. They compare unfiltered raw `p`,
while sampling filters/temperature/grammar define a different `q`. A top-N
probability trace, one reference realization, or an average sampled-string
likelihood does not marginalize over meanings or possible reasoning paths.
Native EOG retention and extra stop tokens must be resolved before treating any
free-generation record as the protocol's full trajectory. Longer study runs
require a separately frozen seed schedule, token/stop contract, runtime budget,
scored spans and artifact custody. The default short CPU fixtures establish none
of those study gates.

## Observed stop-policy blocker in the selected stable runtime

The executed 0.6B startup log lists native EOG IDs
`[128247,151643,151645,151662,151663,151664]`; the canonical HF generation
configuration stops on `[151645,151643]`. The extra native stops are the ordinary
BPE token `</s>` and FIM/repository markers. The pinned native vocabulary loader
uses token-text heuristics and marks these as EOG, including a logged attribute
override for `</s>`. The checker preserves that difference and fails the aggregate
gate even when a short greedy output matches. No tokenizer patch, logit bias,
ignore-EOS workaround, or scientific stopping-rule substitution is applied.

Fast prediction is usable under its own explicitly recorded native stop law.
It is not yet a substitute for the protocol's HF stopped-trajectory law.
Fixed-prefix raw-probability diagnostics remain possible because they request
the full pre-sampling distribution before stopping is interpreted. Actual
limits and measurements, including Q8 drift, are in the CPU validation report.
