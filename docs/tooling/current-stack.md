# Tooling decision for the first research increment

Checked on **11 October 2026** against maintainer documentation, tagged source,
GitHub release APIs, and package-publisher PyPI metadata. The machine for this
increment has five CPU cores, about 17 GiB RAM, 30 GB disk, and no GPU. The later
target is an RTX 2080 Ti with 11 GB VRAM. This document supports the experiments
in [the research plan](../../Plan/research-plan.md); it does not report a causal
experiment or certify an untested GPU installation.

Use **Hugging Face Transformers in eager mode, ordinary PyTorch module hooks,
uv, explicit JSON configurations and run records, and safetensors**. The retained
CPU versions passed the bounded pretrained smoke described below. Adding an
interpretability framework or serving engine should
answer a measured need. The exact source observations, release timestamps,
dependencies, licenses, and access limitations are in [sources.json](sources.json).

## Selected environment and current releases

The prepared `/workspace/research-environment/.venv` was inspected using Python
and package metadata; `uv --version` was also run. Import/version inventory is
evidence of availability, not an inference, memory, or compatibility test.

| Component | First-increment choice / observed installation | Latest stable observed on 11 October | Decision |
| --- | --- | --- | --- |
| Python | 3.12.14 | No Python latest-release claim | Keep the existing interpreter; record patch version and platform. |
| PyTorch | `2.8.0+cpu` | `2.14.1`, released 30 September | Retain the CPU wheel validated by the bounded smoke; upgrade in a separately measured environment. |
| Transformers | `4.57.6` | `5.19.0`, released 6 October | Dense Qwen3 is available in the selected version. Newer hybrid models may require a separate v5 environment. |
| safetensors | `0.8.0` | `0.8.0` | Use for selected tensor artifacts. |
| uv | `0.12.23` | `0.13.0`, released 9 October | Keep the installed tool and record its version. |
| Supporting packages | `huggingface-hub==0.36.2`, `tokenizers==0.22.2`, `numpy==2.5.4` | Not asserted latest here | Preserve the resolved environment in the lock and record actual versions. |

Release evidence: [PyTorch 2.14.1](https://github.com/pytorch/pytorch/releases/tag/v2.14.1),
[Transformers 5.19.0](https://github.com/huggingface/transformers/releases/tag/v5.19.0),
[safetensors package metadata](https://pypi.org/pypi/safetensors/json), and
[uv 0.13.0](https://github.com/astral-sh/uv/releases/tag/0.13.0).
The selected Transformers patch was published on 16 January 2026; it is
deliberately distinct from the current release. [Selected package metadata](https://pypi.org/pypi/transformers/4.57.6/json).

CPU reference runs use **FP32** with short sequences, batch one, and
bounded capture. FP16 is the explicit precision for the later Turing GPU path.
A CPU run cannot measure GPU memory, driver compatibility, or GPU throughput.
Neither the initial environment nor this table substitutes for a committed
dependency lock and passing replay/invariant checks.

## Instrumentation options

| Tool | Current release / upstream license | What it provides | Fit and installation tradeoff |
| --- | --- | --- | --- |
| PyTorch + Transformers | PyTorch 2.14.1: BSD-style upstream license with additional bundled-license metadata; Transformers 5.19.0: Apache-2.0 | Native modules, hooks, generation, activation gradients, checkpoint and tokenizer loading | Selected. No architecture conversion layer. Pin model-specific hook semantics and test them. |
| NNsight | Stable `0.7.0` (5 May), MIT; newer `0.8.0.rc1` is a prerelease (9 September) | Trace blocks expose internal inputs/outputs, mutation, and saved tensors; optional vLLM/remote intervention integration | Strong later ergonomic option. Adds its tracing runtime and broadly constrained dependencies; the release candidate rewrites execution and needs fresh parity checks. |
| TransformerLens | `4.2.0` (10 October), MIT | `TransformerBridge`, named hook aliases, activation caching, patching and circuit-analysis tools on HF models | Relevant for later component/path studies. Requires `torch>=2.6` and `transformers>=5.9.0`, so installing it changes the selected reference environment. |
| pyvene | `0.1.8` (26 May **2025**), Apache-2.0 | Declarative intervention configurations, model/component mappings, interchange and trainable interventions | Useful if a large intervention matrix or trained alignment becomes necessary. Its tagged Qwen mapping is Qwen2; do not infer Qwen3/hybrid support from a generic Qwen announcement. |

Sources: [PyTorch license](https://github.com/pytorch/pytorch/blob/v2.14.1/LICENSE),
[Transformers license](https://github.com/huggingface/transformers/blob/main/LICENSE),
[NNsight stable notes](https://github.com/ndif-team/nnsight/releases/tag/v0.7.0),
[NNsight prerelease notes](https://github.com/ndif-team/nnsight/releases/tag/v0.8.0.rc1),
[TransformerLens 4.2.0 metadata](https://pypi.org/pypi/transformer-lens/4.2.0/json), and
[pyvene tagged mapping](https://github.com/stanfordnlp/pyvene/blob/v0.1.8/pyvene/models/qwen2/modelings_intervenable_qwen2.py).
License observations cover upstream software; checkpoints, datasets, and bundled
dependencies retain their own terms.

TransformerLens has changed substantially: v4 recommends
`TransformerBridge.boot_transformers`, preserves raw HF weights by default,
and removed legacy `HookedTransformer.from_pretrained`. Optional compatibility
mode changes its numerical convention. Older concerns about mandatory weight
conversion or narrow architecture coverage therefore do not describe this
release. Its tagged adapters include Qwen3, Qwen3.5, Qwen3-Next and LFM2.
Architecture support is still different from passing this project's causal
checks. [Current tagged README](https://github.com/TransformerLensOrg/TransformerLens/blob/v4.2.0/README.md).

For the selected Transformers **4.57.6**, `model.model.layers[i]` on a dense
Qwen3 causal LM returns a **Tensor**, after both attention and MLP residual
additions. Treating every block output as `output[0]` would slice away the batch
dimension. Check shape and output type, name the operation precisely, clone
captured tensors when required, and remove handles reliably. An attention-output
hook and a block-output hook have different causal meanings.
[Tagged Qwen3 implementation](https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/models/qwen3/modeling_qwen3.py),
[PyTorch hook API](https://docs.pytorch.org/docs/2.8/generated/torch.nn.Module.html).

New small architectures deserve explicit treatment. Qwen3.5 uses a hybrid
Gated DeltaNet/full-attention stack with recurrent state and optional fast-kernel
dependencies; the tagged v5.19 documentation describes a slower PyTorch fallback.
LFM2 combines short convolutions and attention. Residual block capture may be
possible in both, but not every layer has a conventional attention head or KV
cache. Reusing dense-Qwen3 hook paths, head analyses, or cache-reset assumptions
would be incorrect. Add a model-specific adapter and validate full-prefix versus
incremental state before changing the reference model.
[Qwen3.5 v5.19 documentation source](https://github.com/huggingface/transformers/blob/v5.19.0/docs/source/en/model_doc/qwen3_5.md),
[TransformerLens Qwen3.5 adapter](https://github.com/TransformerLensOrg/TransformerLens/blob/v4.2.0/transformer_lens/model_bridge/supported_architectures/qwen3_5.py),
[LFM2 adapter](https://github.com/TransformerLensOrg/TransformerLens/blob/v4.2.0/transformer_lens/model_bridge/supported_architectures/lfm2.py).

## Generation backends and the RTX 2080 Ti

| Backend | Current release / license | Hardware and architecture evidence | Decision |
| --- | --- | --- | --- |
| HF eager | Selected versions above | Dense Qwen3 in tagged source; ordinary CPU and CUDA tensors/hooks | Canonical causal reference. First use CPU FP32; later validate GPU FP16 separately. |
| llama.cpp | Latest designated stable `v0.6.0` (5 October), MIT; newer rolling prerelease `b11552` observed (10 October) | Tagged build docs permit explicit CUDA architecture selection; serving and GGUF conversion are separate from HF instrumentation | First later efficient-generation candidate. Pin stable commit `8345f333951c661d166b00e6f9362e553768f292`, conversion recipe and GGUF hashes; initially compare F16, then label quantization separately. |
| vLLM | `0.31.0` (5 October), Apache-2.0 | Current official GPU requirements include compute capability 7.5 and RTX20xx; model and attention-backend support require their own checks | Conditional GPU benchmark only, in a separate environment. The release pins `torch==2.13.0` and `transformers>=5.10.4,<5.18.0`; latest Transformers 5.19.0 cannot be combined with it. |
| SGLang | `0.5.21` (GitHub: 2 October; PyPI: 1 October), Apache-2.0 | Current installation has substantial compiled dependencies; an upstream SM75 deprecation RFC exists | Defer. Metadata pins torch 2.13.0, Transformers 5.12.1, CUDA/FlashInfer/FlashAttention dependencies. Neither installation docs nor a closed RFC certify a working complete SM75 stack. |

Sources: [llama.cpp stable release](https://github.com/ggml-org/llama.cpp/releases/tag/v0.6.0),
[rolling release](https://github.com/ggml-org/llama.cpp/releases/tag/b11552),
[vLLM requirements](https://docs.vllm.ai/en/latest/getting_started/installation/gpu/),
[vLLM 0.31.0 package metadata](https://pypi.org/pypi/vllm/0.31.0/json),
[SGLang 0.5.21 metadata](https://pypi.org/pypi/sglang/0.5.21/json),
[SGLang installation](https://docs.sglang.io/docs/get-started/install), and
[SM75 RFC](https://github.com/sgl-project/sglang/issues/6006).
Publication times are recorded separately rather than forcing GitHub and PyPI
dates to agree.

Turing is SM75 and supports FP16 tensor-core operations. Use explicit FP16;
native BF16 tensor-core acceleration is absent on this generation. Inspect the
actual CUDA wheel's architecture list and driver requirements on the GPU host.
`torch==2.8.0` with a suitable CUDA wheel is a candidate for preserving reference
semantics, not a GPU configuration tested here. Mainstream FlashAttention-2
targets Ampere/Ada/Hopper and links a separate Turing subset implementation;
that restriction does not describe every kernel with a similar name.
[NVIDIA Turing guide](https://docs.nvidia.com/cuda/turing-tuning-guide/index.html),
[FlashAttention maintainer README](https://github.com/Dao-AILab/flash-attention).

For a future llama.cpp build, target `CMAKE_CUDA_ARCHITECTURES=75` with CUDA
enabled, subject to the pinned toolchain. Start with one slot, a bounded context,
explicit F16 K/V, context shifting disabled, and prompt reuse disabled for parity.
The v0.6.0 server documents `--cache-type-k`, `--cache-type-v`,
`--no-context-shift`, `--no-cache-prompt` and `--chat-template-kwargs`.
Re-check its own `--help` before execution.
[Pinned build documentation](https://github.com/ggml-org/llama.cpp/blob/v0.6.0/docs/build.md),
[pinned server documentation](https://github.com/ggml-org/llama.cpp/blob/v0.6.0/tools/server/README.md).

Serving token IDs, log probabilities, or textual reasoning does not establish
validated residual intervention support. NNsight does offer a vLLM intervention
integration, so the absolute claim that optimized engines cannot be instrumented
is outdated. This project still needs to test hook order, batching, state and
no-op equivalence for any such integration. Match immutable checkpoint/tokenizer
revision, rendered template, thinking mode, input token IDs, stop rules,
sampling filters and precision before comparing engines. Equal seeds do not
guarantee equal generated paths. [NNsight vLLM integration notes](https://github.com/ndif-team/nnsight/releases/tag/v0.7.0).

## Configuration, records and reproducibility

Use JSON plus small explicit validators/dataclasses for the initial fixed schema.
Reject unknown fields, duplicate keys, invalid bounds and nonfinite numbers;
freeze the resolved configuration before execution and hash its canonical
representation. The implemented increment writes **per-run JSON** files for
configuration, inventory, tokens, run metadata, checks and the tensor index;
dataset input uses JSONL. Append-only JSONL event logs are a later option as run
volume grows. Safetensors stores selected, detached CPU tensors with
shape/dtype/site metadata and hashes.
Use `allow_nan=False` when writing JSON. Standard-library JSON and logging
provide these basic building blocks without another configuration framework.
[Python JSON documentation](https://docs.python.org/3.12/library/json.html),
[Python logging documentation](https://docs.python.org/3.12/library/logging.html),
[safetensors format](https://github.com/safetensors/safetensors/blob/v0.8.0/README.md).

| Alternative | Current publisher release observed | When it would justify added dependencies |
| --- | --- | --- |
| Hydra / OmegaConf | Hydra `1.3.7`, OmegaConf `2.4.0` | Hierarchical composition and bounded sweeps across many configurations. Useful later; avoid implicit overrides in a small confirmatory study. |
| Pydantic | `2.14.0` | Richer nested schemas and reusable validation interfaces. Set strict validation deliberately. |
| MLflow | `3.17.0` | Local experiment UI and artifact registry when plain records become hard to navigate. |
| Weights & Biases | `0.30.0` | Collaborative tracking if needed; choose offline/local behavior explicitly before any later synchronization. |

These are optional, **not installed or compatibility-tested for this decision**.
Version and publisher-declared license fields are retained in the source ledger.
Feature evidence: [Hydra introduction](https://hydra.cc/docs/intro/),
[Pydantic models](https://docs.pydantic.dev/latest/concepts/models/),
[MLflow tracking](https://mlflow.org/docs/latest/ml/tracking/),
[W&B runs](https://docs.wandb.ai/models/track/run).

Use an explicit CPU PyTorch index in uv's package sources, retain the resolved
lock, and run with `--locked` to fail on stale project metadata instead of
silently changing the lock. A future CUDA reference and each optimized backend
need separate resolved environments. A lock is stronger than a list of top-level
versions but does not pin checkpoint files or a GPU driver.
[uv/PyTorch integration](https://docs.astral.sh/uv/guides/integration/pytorch/),
[locking behavior](https://docs.astral.sh/uv/concepts/projects/sync/).

Record repository commit/dirty status, lock/config hashes, Python and package
versions, model/tokenizer/template hashes, dtype, attention implementation,
device, CPU thread counts, hardware/driver details, every RNG stream, cache
policy, raw tokens, stop/truncation reasons, passes, timings and artifact bytes.
Separate world, donor, perturbation and sampling randomness. Keep no-op checks
on the same execution path and calibrate numerical tolerances rather than
requiring bitwise agreement across engines or releases. PyTorch explicitly
limits reproducibility across versions/platforms and describes the cost of
deterministic settings. [PyTorch reproducibility notes](https://docs.pytorch.org/docs/2.8/notes/randomness.html).

Start with weights frozen, eval mode, cache off, no quantization or compilation,
and selected semantic-position captures. Later gradient experiments must leave
inference mode, explicitly make the relevant activation require gradients, and
use a local scalar objective. Frozen weights and integer token IDs alone do not
create an activation-gradient graph. Cache retention, clean re-prefill and clean
refinement remain distinct treatments. [Autograd notes](https://docs.pytorch.org/docs/2.8/notes/autograd.html),
[Transformers cache explanation](https://huggingface.co/docs/transformers/v4.57.1/en/cache_explanation).

## Evidence limits and next gates

Current release APIs and all cited tagged source files were accessible. The
browser could not open the versioned Qwen3.5 documentation page; its exact
v5.19.0 Markdown source was successfully retrieved instead. An initial guessed
TransformerLens migration URL failed; the maintainer README linked the working
[`migrating_to_v4.html`](https://transformerlensorg.github.io/TransformerLens/content/migrating_to_v4.html)
page. Mutable `latest` documentation and main-branch license links are dated
observations, not immutable implementation pins.

The actual pretrained **Qwen3-0.6B CPU FP32 eager smoke passed** in
`runs/20261011T102648Z-e94a5c040d65`. Its immutable model/tokenizer revision is
`c1899de289a04d12100db370d81485cdf75e47ca`; source commit was
`501b96add89625b0bcf788e4530ec27d0ce23b37` with a dirty working tree and per-source
hashes recorded. Capture-only, identity and zero-strength logits had maximum
absolute error zero. Prefix-causality checks also had zero error; cached versus
full-prefix logits differed by at most `1.90735e-5` and passed the recorded
`atol=1e-4`, `rtol=1e-5` criterion. Seeded identity generation, RNG preservation,
hook cleanup and frozen/unmutated parameters passed. The run generated 32 tokens
across four bounded conditions in **20.73 seconds**, with peak process RSS
**4.56 GiB**, and retained one `[1, 1, 1024]` residual tensor. This is engineering
validation, with no competence, transfer or novelty claim. See the coordinator's
[validation record](../validation.md) for the durable evidence and test scope.

The 0.6B snapshot and file hashes were acquired and verified; the 1.7B snapshot
was not downloaded. Remaining gates include an RTX 2080 Ti inventory, driver/
wheel architecture checks and FP16 measurement, and behavioral competence and
bridge-headroom calibration before a causal pilot. No GPU benchmark,
serving-engine installation, large trace capture, compute rental or 1.7B
hardware-fit claim is established by this review.
