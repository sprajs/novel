# Fast backend CPU validation, 11 October 2026

**Fast generation works. Scientific interchangeability remains blocked.**
The native stop policy differs from HF even for F16, and Q8_0 also fails the
predeclared probability thresholds. No GPU execution or scientific discovery
is claimed. [Exact setup and commands](../tooling/fast-prediction.md),
[full evidence](fast-cpu-evidence.json), and [raw generation/token/probability records](fast-cpu-traces.jsonl)
make these observations inspectable.

The branch incorporates merged research main
`58783ea4e96d61483103c75ccb56533aad22fd56`. Runs used dirty working trees with
recorded source hashes for the reference and corrected likelihood runs; this
evidence is not presented as a clean-commit hosted
CI run. The new main's Plan, README, corpus/specifications and observational
measurement protocol were not modified. Zero historical candidates are certified.

## Executed conditions

AMD EPYC 9V45 host, five exposed CPUs/affinity 0..4, Linux x86-64, Python 3.12.14,
GNU 14.2, CMake 4.1.3, Ninja 1.13.0; no GPU. Native llama.cpp stable v0.6.0 peels to
`d81235049384534c167caea52b85a694f6103d14`, not the release API's target field.
The CPU build uses its native ISA, OpenMP and CUDA off. Binary/library hashes,
commands, compiler, linkage, cache and lock hashes are retained.

Only hash-verified Qwen3-0.6B HF revision
`c1899de289a04d12100db370d81485cdf75e47ca` was downloaded. Offline conversions:

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| F16 | 1,509,347,648 | `fc090d6b5617b1b8578cd4816bbabd48d8987aa49baecbb024942956b1af1a01` |
| Q8_0 | 804,753,728 | `0392d70678044c268e122876a3b3742059969bd9b00dce7994579baa83d3e110` |

Q8_0 derives from that F16 parent without an importance matrix. The serialized
GGUF retains both source embedding/head tensors, so artifact size differs from
the reference's unique tied-parameter arithmetic. No 1.7B/8B weights were acquired.
The first converter attempt failed because upstream imports SentencePiece before
its missing-file BPE fallback. That log/hash remains in the evidence. The separate
converter lock adds SentencePiece 0.2.1 and records its own transitive versions
(filelock 4.1.1 versus reference 4.1.0); no reference dependency was replaced.

## Tests and smoke checks

The full suite against merged main passed **293 tests and 118 subtests** in 38.95s;
two skips are the optional JSON Schema validator and the explicitly enabled GPU
reference test. Twenty-one new fast-runtime tests exercise probability support,
normalization, stop/token evidence, context bounds, artifact/library hashes,
GPU planning via mocks, and secret-free environment records. GPU mocks are not
hardware validation. The client also runs with Python `-S`, without site packages. A final native
CPU interface check passed after sharing the full-offload guard with GPU
benchmarking; its timing overlaps tests and is not a benchmark.

The unchanged pretrained HF CPU profile passed its forward/capture/no-op,
cache-prefix, raw-token identity and hook-cleanup checks. It generated 32 tokens
across four reference conditions. This individual pass does **not** resolve the
[original CPU repeatability anomaly](cpu-repeatability-investigation.md).
The reference smoke overlapped conversion work; its wall time is not used for
backend performance comparison.

Native F16 repeated predictions passed: two prompts, two repeats, eight tokens.
That earliest interface-only run predates adapter source-hash enrichment; its raw
responses are retained, but it is not used as a scientifically equivalent run.
Structured JSON passed with `{"answer":"yes"}` and terminal token 151645 retained
in the raw token list. Q8 stochastic requests passed with seeds 17/18 and explicit
temperature 0.7/top-k 20/top-p 0.8; both café outputs are retained, including their
different token paths. A two-slot Q8 batch passed on both prompts. These short
traces establish interfaces, not task competence, long-output support, independent
semantic samples or a historical recovery claim.

## Microbenchmarks, native warmup and three samples

Five threads, F16 KV, Flash Attention off, GPU layers 0. Prefill uses 32 synthetic
tokens; decode uses 8. Native warmup is retained. Model load/startup is excluded
from each native token-rate statistic and separately present in wall/RSS records.
These short workloads have substantial dispersion; do not extrapolate to longer
prompts, 1.7B/8B, RTX2080Ti or RTX5090.

| CPU artifact | Prefill mean ± sample SD, tokens/s | Decode mean ± sample SD, tokens/s | Peak benchmark process RSS |
| --- | ---: | ---: | ---: |
| F16 | 419.60 ± 123.66 | 35.99 ± 2.92 | 1.49 GiB |
| Q8_0 | 289.61 ± 60.90 | 48.73 ± 5.45 | 0.83 GiB |

Q8 improved decode and used less resident memory in these samples; F16 prefill
was faster. This is not a universal backend ranking. On the exact bridge prompt,
eight greedy tokens took 1.789s in HF full-prefix, 1.201s in HF cached, and 0.443s
in the resident native F16 server. On the café prompt those times were 1.827s,
1.258s and0.358s. The generated IDs matched in both. These comparisons exclude
load, follow the probability diagnostics, include different cache/kernel
conditions and have one timing sample per condition; they are not stable speedup
estimates or GPU throughput promises. Time-to-first-token was not measured.

## Full probability diagnostics and failed equivalence gate

Both backends use the same exact template source/rendered bytes, prompt IDs,
and stable continuation token boundaries. There are six fixed teacher-forced
positions: two for `A bridge`, four for `Café tables`. HF uses FP32 eager, cache
disabled, and two exact forwards at each position. Native uses F16 KV, one slot,
no prompt reuse, unfiltered pre-sampling full-vocabulary logprobs and a repeated
request. Within these executed pairs, HF repeats and native logprob repeats were
exact. This bounded result is not a repeatability certificate.

| Artifact | Largest absolute raw logprob delta over vocabulary | Largest normalized KL, reference to native | Largest absolute fixed-continuation logprob delta | Numerical smoke subgate |
| --- | ---: | ---: | ---: | --- |
| F16 | 0.0248674 | 1.09449e-6 | 0.00307081 nats | PASS for both supplied prefixes |
| Q8_0 | 0.987039 | 8.92309e-4 | 0.126141 nats | FAIL |

The raw Q8 café-prefix score changes by +0.126141 nats (about a 13.4% path-probability
ratio). Even identical eight-token greedy outputs therefore do not imply
likelihood equivalence. The predeclared thresholds remain 0.1 maximum logprob
error, 1e-4 KL, 0.05 sequence-score delta, and exact native repeats. They are
engineering gates, not calibrated tolerances for subtle scientific effects.

Native FP32 softmax returned probability sums slightly above 1: maximum observed
mass errors 3.23931e-5 for F16 and 3.84091e-5 for Q8. The initial diagnostic used
these raw values directly in a KL expression and produced negative results.
Those initial reports are preserved and labeled as invalid KL calculations.
The corrected calculation normalizes the full native distribution in FP64
before calculating KL; raw logprobs, normalizer and mass error remain separate.
An analytical regression test confirms that normalization does not erase raw
likelihood error. Model arithmetic, prompts, seeds and thresholds were unchanged.
Fresh corrected observations were named separately; failures were not erased.

The aggregate gate is **FAIL for both** artifacts. The startup log exposes native
EOG IDs `[128247,151643,151645,151662,151663,151664]`, versus HF stops
`[151645,151643]`. The extra IDs are ordinary BPE `</s>` and FIM/repository tokens,
assigned EOG semantics by the pinned native vocabulary heuristics. In particular,
the loader logs a control-type override for `</s>`. No tokenizer patch, probability
bias or stopping-rule substitution is applied. The short supplied outputs did
not hit these extra stops, so output agreement cannot resolve that contract gap.

The scored continuation probes omit terminal tokens: they are raw-`p` prefix
cylinders, not completed stopped trajectories, decoder-`q` scores or semantic
idea probabilities. Structured output and truncated sampling change `q`.
No hidden activation, residual patch, gradient or causal intervention is exposed
by the fast adapter. `scientific_interchangeability` remains false.

## Remaining limits

GPU builds and all actual CUDA behavior remain untested. The separate recipes
check SM75/SM120, pinned toolkit/compiler prerequisites and conservative free-VRAM
planning, then demand full offload evidence; no throughput or fit is promised.
Q4_K_M conversion is implemented but not executed here. Long contexts, 2048-token
outputs, Flash Attention and prompt reuse are explicit unvalidated conditions.
The first two require suitable measured capacity; the latter two require new
probability comparisons. The default server's KV decode cache is distinct from
cross-request prompt reuse, which is disabled in these probability probes.

Resolve the native stop contract and measure effect-relevant numerical fidelity
before replacing reference likelihoods or the protocol's generation law. Preserve
all native outputs under their own declared law meanwhile. Real study admission,
semantic grading, independent sampling schedules and frozen budgets remain the
research protocol's gates; this tooling increment supplies no confirmation data.
