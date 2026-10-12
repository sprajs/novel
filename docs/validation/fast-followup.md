# Bounded runtime follow-up, 12 October 2026

The exact F16 artifact passes the unchanged supplied-prefix likelihood gates
with an **explicit greedy HF EOS adapter**. This establishes limited token-ID
termination and the tested IDs/text/probability conditions, not general scientific
interchangeability. Default native mode remains a different stop law. Q8 still
fails numerical gates. [Original failures](fast-cpu.md) remain unaltered;
[new evidence](fast-followup-evidence.json) and [raw records](fast-followup-traces.jsonl) record this separate condition.

## Termination and tokenizer investigation

Pinned source checks establish two separate mechanisms:

- The vocabulary loader assigns six native EOG IDs using token-text/FIM heuristics.
- Server `process_token` ends a request on native EOG, without a replaceable
  stop-ID list. `ignore_eos` inserts negative-infinity logit biases via the sampler
  schema; it does not provide faithful ID-specific termination. String stops
  strip text and cannot specify the desired token paths. Metadata overrides
  would change runtime tokenizer interpretation and would not remove all heuristics.

Sources: [native vocabulary](https://github.com/ggml-org/llama.cpp/blob/d81235049384534c167caea52b85a694f6103d14/src/llama-vocab.cpp),
[server EOG/limit enforcement](https://github.com/ggml-org/llama.cpp/blob/d81235049384534c167caea52b85a694f6103d14/tools/server/server-context.cpp),
[sampler schema](https://github.com/ggml-org/llama.cpp/blob/d81235049384534c167caea52b85a694f6103d14/tools/server/server-schema.cpp).

The optional `--termination hf-eos` adapter retains each native response before
validation and resumes after an extra native EOG, using the exact raw token
prefix and remaining cap. It stops on `[151645,151643]`, retaining the terminal
ID. No model, artifact, tokenizer metadata, logits or upstream source is edited.
Its text includes all special/EOS spellings, matching HF decode with
`skip_special_tokens=False` on these fixtures. Raw native responses and the
adapted response remain distinct. Clean native prefill after a resumed EOG and
KV decoding within chunks are recorded as separate cache/kernel conditions.

This mode supports greedy unconstrained generation only. Sampling, grammar and
cross-request prompt reuse are rejected because chunk restarts would reset RNG,
grammar state or change numerical reuse. The native mode retains its original
performance/decoder contract. No new throughput or GPU claim is made.

All six actual F16 boundary fixtures pass:

| Forced first ID | Adapter output IDs | End condition |
| --- | --- | --- |
| 128247, ordinary `</s>` | `[128247,151645]` | Resume extra native stop, then HF EOS |
| 151643 | `[151643]` | HF EOS immediately |
| 151645 | `[151645]` | HF EOS immediately |
| 151662, FIM padding | `[151662,151645]` | Resume, then HF EOS |
| 151663, repository name | `[151663,151645]` | Resume, then HF EOS |
| 151664, file separator | `[151664,151645]` | Resume, then HF EOS |

The probe deliberately forces tokens with logged transport logit biases. These
are boundary/custody fixtures, **not** model-probability or behavioral equivalence
measurements. Neither production generation nor the likelihood probe uses them.
Every complete decoded fixture matches the HF raw-text convention.

A separate unresolved tokenizer difference is exposed: literal `</s>` encodes
as HF `[522,82,29]`, while native special parsing gives `[128247]`. The other
five tested EOG spellings encode identically. The adapter preserves raw emitted
IDs instead of retokenizing decoded text, so its boundary handling is faithful
to those paths. It does not establish global input tokenizer equivalence.
New scientific prompts must pass exact template/input-ID checks; semantic mass
and canonical-text versus emitted-token-path probabilities remain distinct.

## Exact artifact and unchanged numerical gates

The F16 file remains **1,509,347,648 bytes**, SHA256
`fc090d6b5617b1b8578cd4816bbabd48d8987aa49baecbb024942956b1af1a01`.
The Q8 file remains **804,753,728 bytes**, SHA256
`0392d70678044c268e122876a3b3742059969bd9b00dce7994579baa83d3e110`.
Both descend from the same pinned registry snapshot and native source.
The original equivalence configuration/hash is unchanged: 0.1 max logprob
error, 1e-4 KL, 0.05 sequence-score delta and exact native probability repeats.

| Greedy `hf-eos` condition | Maximum logprob error | Maximum normalized KL | Largest absolute continuation delta | Bounded gate |
| --- | ---: | ---: | ---: | --- |
| F16 | 0.0248674 | 1.09449e-6 | 0.00307081 nats | PASS |
| Q8_0 | 0.987039 | 8.92309e-4 | 0.126141 nats | FAIL |

Both fixtures' eight-token IDs, raw decoded text and administrative stop reasons
match HF. The native stop set still differs; only the configured effective ID
termination aligns. Raw LP/mass errors remain separate from normalized KL.
These are six positions/two short prompts, not calibrated tolerances for subtle
scientific effects. `scientific_interchangeability` remains false in every report.

## Three independent review fixes

**Response custody:** a job manifest is persisted before batch launch. Raw HTTP
bodies survive invalid API JSON and HTTP failures. Decoded native responses are
saved before token validation or output JSON parsing. Each worker writes its own
success/failure record; completion collection waits for every submitted job and
retains later successes after earlier failures. No output is repaired or silently
retried. A real two-job token-limited structured-output check intentionally fails
parsing, while both `[515]` token paths, probabilities, requests and HTTP bodies
remain saved. Mixed success/failure, malformed HTTP/API JSON and contract failure
regressions verify custody and denominators.

**Model lifecycle:** HF reference probabilities are saved as hashed CPU FP64
SafeTensors plus exact prompt/target IDs, settings, source hashes and generation
records. The reference function returns no model/device tensors. Garbage
collection and CUDA synchronization/cache release precede native startup; CUDA
allocated bytes must return to baseline. Native rereads/hash-verifies those
vectors, then checks actual free VRAM. A real tiny CPU Qwen model weak-reference
test proves release before native phase; tampered vectors block inference. CUDA
release checks are mocked, not GPU evidence. This avoids retaining two 8B weight
copies; actual GPU fit/execution remains untested.

**Context equality:** the pinned server checks `prompt.n_tokens()+1 >= n_ctx`
before the ordinary generation cap. The adapter now requires
`prompt_length + n_predict < context`, leaving one token of slack. Equality is
rejected before inference. True native truncation still fails validation, with
its raw response retained. An equality-boundary regression covers this case.

The initial CPU repeatability anomaly, GPU/kernel caveats, stochastic-decoder
alignment and all research admission gates remain open. No new model download,
GPU rental, long benchmark or merge occurred in this follow-up.

Final validation against this implementation passes **306 tests and 118 subtests**
with two documented skips (GPU and optional JSON Schema validator), in 5.38s.
The separate final CLI checks pass both greedy `hf-eos` predictions and ordinary
native structured JSON. Their job manifests, raw HTTP/native responses and
records are retained. Focused tests cover phase-release order, vector tampering,
all-job custody, malformed API/HTTP responses, equality-context rejection and
greedy adapter restrictions. No hosted CI result is claimed.
