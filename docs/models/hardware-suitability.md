# Model suitability for CPU, 11 GB and rented GPUs

This is a capacity and instrumentation recommendation, not a measured GPU fit,
model-quality ranking or scientific result. CPU execution is tested; RTX2080Ti
and the primary rental target, RTX5090 32 GB, require the user-run diagnostic. See
[execution profiles and exact commands](../tooling/execution-profiles.md).

| Mode | Mechanics model | Primary candidate | Larger-model gate |
| --- | --- | --- | --- |
| Cloud CPU | Qwen3-0.6B FP32 | 0.6B for bounded mechanics, not a demonstrated scientific baseline | 1.7B can be explicitly selected but costs substantially more RAM/time; CPU throughput is not extrapolated |
| RTX2080Ti 11 GB | Qwen3-0.6B FP16 | Qwen3-1.7B FP16, batch 1, 128 input / 8 new token caps | First measure 1.7B forward/capture, then short selected gradients; do not start with 4B or quantization |
| RTX5090 32 GB, full detected capacity | Same 0.6B FP16 checks | **Qwen3-8B FP16**, eager, batch 1, 128 input / 8 new token caps; optional selected-activation gradient after forward validation | Start with the actual 8B short-context report; longer contexts and backward workloads need measured peaks, with no largest-fit promise |

The [immutable registry](../../configs/models.json) preserves both original entries
and adds the 8B rental candidate:

- `qwen3_0_6b`: `Qwen/Qwen3-0.6B` at
  `c1899de289a04d12100db370d81485cdf75e47ca`.
- `qwen3_1_7b`: `Qwen/Qwen3-1.7B` at
  `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`.
- `qwen3_8b`: `Qwen/Qwen3-8B` at
  `b968826d9c46dd6066d109eabc6255188de91218`.

Each model and tokenizer share their revision, license is Apache-2.0, and every
allowlisted file is hashed before loading. **26 July 2025 remains the selected
complete-snapshot date; training cutoff remains undocumented.** This PR does not
backdate changed templates, substitute `main`, or infer historical eligibility
from GPU/model size. See the full [model provenance](selection.md) for weight,
template, license and public-release distinctions. The [pinned 8B license](https://huggingface.co/Qwen/Qwen3-8B/blob/b968826d9c46dd6066d109eabc6255188de91218/LICENSE)
was verified from metadata bytes; five weight-shard hashes come from immutable
official Hub metadata and will be verified against actual bytes at download/load.
No 8B weights were downloaded here. Its [source and validation evidence](rtx5090-evidence.json)
records this distinction.

The primary profile requires a detected RTX5090/SM120 and takes its full detected
memory up to a 32 GiB ceiling. NVIDIA's **32 GB** product label is separate from
CUDA-reported total/free bytes and their binary GiB conversion. The old 24 GiB
default is removed. The existing 20% allocation headroom remains: using the full
card does not make every byte safely available for tensors. An explicit optional
24 GiB custom rental defaults to 1.7B; it does not shape the 5090 recommendation.

## Weight arithmetic versus runtime memory

All GiB below use 2^30 bytes. These are arithmetic estimates, not GPU benchmarks.
Unique tied-weight counts differ from serialized tensor counts and download
sizes. The pinned [0.6B config](https://huggingface.co/Qwen/Qwen3-0.6B/blob/c1899de289a04d12100db370d81485cdf75e47ca/config.json)
and [1.7B config](https://huggingface.co/Qwen/Qwen3-1.7B/blob/70d244cc86ccca08cf5af4e1e306ecf908b1ad5e/config.json),
plus the [8B config](https://huggingface.co/Qwen/Qwen3-8B/blob/b968826d9c46dd6066d109eabc6255188de91218/config.json),
are the sources; the loader verifies actual unique parameter counts. A CPU
test constructs all three full architectures on PyTorch's metadata-only device,
checking counts and embedding ties without allocating or downloading weights.

| Quantity | Qwen3-0.6B | Qwen3-1.7B | Qwen3-8B |
| --- | ---: | ---: | ---: |
| Unique parameters | 596,049,920 | 1,720,574,976 | 8,190,735,360 |
| FP32 weights alone | 2.22 GiB | 6.41 GiB | 30.51 GiB |
| FP16/BF16 weights alone | 1.11 GiB | 3.20 GiB | 15.26 GiB |
| FP16/BF16 KV per token, batch 1 | 112 KiB | 112 KiB | 144 KiB |
| KV at 128 / 512 / 1024 tokens | 14 / 56 / 112 MiB | 14 / 56 / 112 MiB | 18 / 72 / 144 MiB |
| Current guard's forward planning envelope, 128 input + 8 new | 3.60 GiB | 5.71 GiB | 17.80 GiB |
| Current guard's optional-gradient envelope at same caps | 6.08 GiB | 8.53 GiB | 21.91 GiB |

The last two rows include conservative allowances and are neither measured peaks
nor upper-bound guarantees. The gradient estimate intentionally allows all layers
although the selected leaf only builds a graph downstream of its site. This
can reject workloads that might fit; it is an explicit conservative gate, not
permission to loosen the budget automatically.

KV arithmetic is `2 × layers × KV heads × head dimension × tokens × batch × bytes`.
The two small models have 28 layers, eight KV heads and head dimension 128, so
their KV cost is equal despite different hidden widths. The 8B has **36 layers**,
32 query heads, eight KV heads and head dimension 128; its hidden width is 4096
and MLP intermediate width is 12288. Its input embedding and language-model head
are **untied**, so both 622,329,856-element matrices count as unique weights.
Cache is off for canonical
forwards and gradients; the clean cache-parity condition allocates it separately.

Weight-only arithmetic omits several material costs:

- **Logits:** vocabulary 151,936; full sequence logits at 512 tokens consume
  about 148 MiB in FP16 or 297 MiB in FP32. The smoke briefly retains several
  full-logit comparisons. Generation requests last-position logits only.
- **Attention/workspaces:** eager attention is quadratic in sequence length.
  All 28 layers' 16-head attention maps alone at 4096 tokens would be 14 GiB
  at 16 bits; the reference does not retain them all. For 8B, all 36 layers'
  32-head maps at 128 tokens alone would be 36 MiB in FP16, with quadratic
  growth as context increases. Softmax/normalization may
  use FP32 temporaries. Capturing all attention maps is not enabled.
- **Activations/backward:** selected detached residual capture is small, but
  a selected leaf's downstream autograd graph retains intermediate activations.
  Frozen weights remove parameter-gradient and optimizer tensors, not those
  intermediates. No training/optimizer is created. Full 8B parameter gradients
  would add about another 15.26 GiB even in FP16; that training workload is not
  the selected-activation gradient supported here.
- **Runtime/headroom:** CUDA contexts, libraries, temporary allocations, allocator
  fragmentation, other processes and desktop VRAM use consume space. Peak
  allocated and reserved memory both matter; host RAM loading and snapshot disk
  space are separate limits.

The code's envelope includes explicit weight, KV, retained-logit, eager-workspace,
activation, backward and runtime-reserve fields. Preflight requires it to fit
within 80% of the smaller of measured free VRAM and declared capacity. At only
10 GiB free, the 1.7B default gradient estimate exceeds the resulting 8 GiB cap;
use 0.6B, a shorter input envelope or omit gradients. This is an intended refusal.
For 8B, 30 GiB free provides a 24 GiB allocation limit: the 128/8 gradient
planning envelope is 21.91 GiB, but the 256/8 envelope is 25.00 GiB and is
rejected. These are prospective estimates, not measured success. A 32 GB card
with competing jobs can still fail preflight or OOM later.

## Why these models and where larger ones stop

All three share the dense Qwen3 decoder/hook interface, so 0.6B can validate
mechanics while 1.7B remains the local 11 GB candidate and 8B becomes the
full-capacity rental candidate. The study still needs independently
verified prerequisite competence, a useful guided/unguided gap and answer-balanced
donor controls. Small-model success on an eight-token smoke establishes none of
those. CPU FP32 and GPU FP16 results are separate numerical conditions.

The reconsidered alternative is [Qwen3-4B at its immutable July snapshot](https://huggingface.co/Qwen/Qwen3-4B/blob/1cfa9a7208912126459214e8b04321603b3df60c/config.json):
4,022,468,096 unique parameters and 7.49 GiB of 16-bit weights. It leaves more
headroom, but the full 5090 capacity supports making **8B the primary candidate**
under the short-workload estimate. This is a capacity choice, not evidence that
8B has superior task competence or valid causal effects. 4B remains a metadata
comparison rather than another selectable model; 1.7B is the already-pinned
smaller alternative if the measured 8B workload fails.

8B is now pinned, allowlisted and executable through the rental CLI. It remains
unvalidated on actual hardware. Larger models, longer contexts or other
architectures still need their own immutable provenance, instrumentation checks
and measured peaks. No unpinned download or unsupported largest-fit promise is
made here. Host loading also needs about 15.26 GiB for resident FP16 weights
plus transient conversions and framework memory; plan at least 32 GiB host RAM
as a starting point and check actual availability. There is no host-RAM fit
guarantee or automatic offload.

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
