# Model suitability for CPU, 11 GB and rented GPUs

This is a capacity and instrumentation recommendation, not a measured GPU fit,
model-quality ranking or scientific result. CPU execution is tested; RTX2080Ti,
24 GB cards and RTX5090 require the provided user-run diagnostic. See
[execution profiles and exact commands](../tooling/execution-profiles.md).

| Mode | Mechanics model | Primary candidate | Larger-model gate |
| --- | --- | --- | --- |
| Cloud CPU | Qwen3-0.6B FP32 | 0.6B for bounded mechanics, not a demonstrated scientific baseline | 1.7B can be explicitly selected but costs substantially more RAM/time; CPU throughput is not extrapolated |
| RTX2080Ti 11 GB | Qwen3-0.6B FP16 | Qwen3-1.7B FP16, batch 1, 128 input / 8 new token caps | First measure 1.7B forward/capture, then short selected gradients; do not start with 4B or quantization |
| Rental 24 GiB budget (or explicit 32 GiB override) | Same 0.6B FP16 checks | Same 1.7B FP16 instrumented baseline, then optional native BF16 as a separately recorded condition | Consider 4B only if competence/causal workload requires it; 8B needs stronger measurement evidence and room for gradients |

The existing [immutable registry](../../configs/models.json) is unchanged:

- `qwen3_0_6b`: `Qwen/Qwen3-0.6B` at
  `c1899de289a04d12100db370d81485cdf75e47ca`.
- `qwen3_1_7b`: `Qwen/Qwen3-1.7B` at
  `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`.

Each model and tokenizer share their revision, license is Apache-2.0, and every
allowlisted file is hashed before loading. **26 July 2025 remains the selected
complete-snapshot date; training cutoff remains undocumented.** This PR does not
backdate changed templates, substitute `main`, or infer historical eligibility
from GPU/model size. See the full [model provenance](selection.md) for weight,
template, license and public-release distinctions.

## Weight arithmetic versus runtime memory

All GiB below use 2^30 bytes. These are arithmetic estimates, not GPU benchmarks.
Unique tied-weight counts differ from serialized tensor counts and download
sizes. The pinned [0.6B config](https://huggingface.co/Qwen/Qwen3-0.6B/blob/c1899de289a04d12100db370d81485cdf75e47ca/config.json)
and [1.7B config](https://huggingface.co/Qwen/Qwen3-1.7B/blob/70d244cc86ccca08cf5af4e1e306ecf908b1ad5e/config.json)
are the source; the loader verifies actual unique parameter counts.

| Quantity | Qwen3-0.6B | Qwen3-1.7B |
| --- | ---: | ---: |
| Unique parameters | 596,049,920 | 1,720,574,976 |
| FP32 weights alone | 2.22 GiB | 6.41 GiB |
| FP16/BF16 weights alone | 1.11 GiB | 3.20 GiB |
| FP16/BF16 KV per token, batch 1 | 112 KiB | 112 KiB |
| KV at 128 / 512 / 1024 tokens | 14 / 56 / 112 MiB | 14 / 56 / 112 MiB |
| Current guard's forward planning envelope, 128 input + 8 new | 3.60 GiB | 5.71 GiB |
| Current guard's optional-gradient envelope at same caps | 6.08 GiB | 8.53 GiB |

The last two rows include conservative allowances and are neither measured peaks
nor upper-bound guarantees. The gradient estimate intentionally allows all layers
although the selected leaf only builds a graph downstream of its site. This
can reject workloads that might fit; it is an explicit conservative gate, not
permission to loosen the budget automatically.

KV arithmetic is `2 × layers × KV heads × head dimension × tokens × batch × bytes`.
Both models have 28 layers, eight KV heads and head dimension 128, so their KV
cost is equal despite different hidden widths. Cache is off for canonical
forwards and gradients; the clean cache-parity condition allocates it separately.

Weight-only arithmetic omits several material costs:

- **Logits:** vocabulary 151,936; full sequence logits at 512 tokens consume
  about 148 MiB in FP16 or 297 MiB in FP32. The smoke briefly retains several
  full-logit comparisons. Generation requests last-position logits only.
- **Attention/workspaces:** eager attention is quadratic in sequence length.
  All 28 layers' 16-head attention maps alone at 4096 tokens would be 14 GiB
  at 16 bits; the reference does not retain them all. Softmax/normalization may
  use FP32 temporaries. Capturing all attention maps is not enabled.
- **Activations/backward:** selected detached residual capture is small, but
  a selected leaf's downstream autograd graph retains intermediate activations.
  Frozen weights remove parameter-gradient and optimizer tensors, not those
  intermediates. No training/optimizer is created.
- **Runtime/headroom:** CUDA contexts, libraries, temporary allocations, allocator
  fragmentation, other processes and desktop VRAM use consume space. Peak
  allocated and reserved memory both matter; host RAM loading and snapshot disk
  space are separate limits.

The code's envelope includes explicit weight, KV, retained-logit, eager-workspace,
activation, backward and runtime-reserve fields. Preflight requires it to fit
within 80% of the smaller of measured free VRAM and declared capacity. At only
10 GiB free, the 1.7B default gradient estimate exceeds the resulting 8 GiB cap;
use 0.6B, a shorter input envelope or omit gradients. This is an intended refusal.

## Why these models and where larger ones stop

The selected pair shares the same dense Qwen3 decoder/hook interface, so 0.6B
can validate mechanics while 1.7B offers a provisional competence increase
without introducing a new architecture. The study still needs independently
verified prerequisite competence, a useful guided/unguided gap and answer-balanced
donor controls. Small-model success on an eight-token smoke establishes none of
those. CPU FP32 and GPU FP16 results are separate numerical conditions.

For scale only, the official [Qwen3-4B config](https://huggingface.co/Qwen/Qwen3-4B/blob/main/config.json)
implies roughly 7.49 GiB of unique 16-bit weights, and [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B/blob/main/config.json)
roughly 15.26 GiB. Those live metadata links support approximate sizing, **not
executable or historically pinned model choices**. A 4B model leaves poor
instrumentation headroom on 11 GB; an 8B model's weights can consume most of a
24 GiB budget before backward work. Even a real 32 GB RTX5090 does not establish
that a chosen 8B gradient/context workload fits.

These larger candidates are **not added to the download registry or selectable
CLI**. Enabling one requires an immutable model/tokenizer revision, verified
license and file hashes, revised memory envelope, architecture/hook checks,
short-context measured peaks, and a scientific reason beyond chat throughput.
No unpinned model download or unsupported largest-fit promise is made here.

Start at the provided 128/8 caps and batch one. A later 256-token mechanics
configuration is supported; 512/1024 ladders need a separately bounded validation
change. On OOM: preserve the failed report, release other GPU jobs, shorten input
and generation, remove gradients, reduce captured sites, or choose 0.6B. Record
every changed condition. Sequential donor/recipient passes avoid two resident
models. Do not silently quantize or offload and interpret it as the same causal
experiment.

Fast serving backends and quantization can change activations, logits, cache
precision, sampling and accessible hooks. Keep them optional and separate from
canonical causal instrumentation. No throughput ranking or rented-GPU performance
claim is supported until an actual GPU run produces the diagnostic artifact.
