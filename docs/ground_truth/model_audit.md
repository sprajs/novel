# Frozen checkpoint release audit

Audited 11 October 2026. This is a public-source provenance audit; no model weights were downloaded, no inference was run, and no checkpoint was declared contamination-free. The companion [JSON evidence](../../data/ground_truth/model_audit.json) contains exact revisions, file identities, dates, source URLs, and unresolved gates.

**Decision:** two April 2023 Pythia base snapshots have strong release evidence before the DPO paper's 29 May 2023 submission. They are candidates for a *DPO algebra reconstruction* assay, conditional on the target's earlier-disclosure audit and prerequisite competence. Qwen3-1.7B and 0.6B are suitable modern mechanics references; both are chronologically ineligible for a 2023 historical claim. Pythia also postdates FlashAttention (2022) and LoRA (2021).

| Role | Exact model revision | Evidence-backed date | Decision |
| --- | --- | --- | --- |
| Historical candidate | `EleutherAI/pythia-1.4b` / `8f0af839162ddb466006494a08733ee9cfa2d338` | Complete main-branch upload recorded 2023-04-03 18:33:31 UTC | Provisionally eligible relative to DPO's recorded submission; target disclosure remains open |
| Historical candidate, more capacity | `EleutherAI/pythia-2.8b` / `f20536c52a97faea73b8997cc789bd913853f14a` | Complete main-branch upload recorded 2023-04-03 18:51:39 UTC | Same condition; local feasibility unmeasured |
| May 2025 historical candidate | `Qwen/Qwen3-1.7B` / `d3e258980a49b060055ea9038dad99d75923f7c4` | Full revision dated 2025-04-29 08:55:53 UTC; publisher release April 29 | Provisionally eligible relative to recorded MeanFlow/AlphaEvolve disclosures; earlier target channels remain open |
| Smaller May 2025 historical candidate | `Qwen/Qwen3-0.6B` / `6130ef31402718485ca4d80a6234f70d9a4cf362` | Full revision dated 2025-04-29 08:56:31 UTC; publisher release April 29 | Same condition; original tokenizer differs from modern mechanics |
| Modern mechanics | `Qwen/Qwen3-1.7B` / `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e` | Weights uploaded 2025-04-28; selected full revision dated 2025-07-26 | Ineligible for 2023 historical claims |
| Smaller modern mechanics | `Qwen/Qwen3-0.6B` / `c1899de289a04d12100db370d81485cdf75e47ca` | Weights uploaded 2025-04-28; selected full revision dated 2025-07-26 | Ineligible for 2023 historical claims |

The Pythia dates come from the [1.4B commit history](https://huggingface.co/api/models/EleutherAI/pythia-1.4b/commits/main) and [2.8B commit history](https://huggingface.co/api/models/EleutherAI/pythia-2.8b/commits/main), corroborated by the publisher's release announcement in an [April 4, 2023 README revision](https://github.com/EleutherAI/pythia/blob/ceb8e5234db499def6759c54195cd87f465cfb3d/README.md) and the [Pythia v1 paper](https://arxiv.org/abs/2304.01373v1), submitted April 3 at 20:58:15 UTC. The [DPO record](https://arxiv.org/abs/2305.18290) records v1 submission on May 29 at 17:57:46 UTC. A submission timestamp is not an independently measured first public announcement time; it is a conservative comparison boundary here.

**April 3 is a replacement-suite release, not Pythia's first release.** The contemporaneous README reports retraining, uniform batch sizes, added early checkpoints, a revised learning-rate floor, and use of FlashAttention. The older v0 repositories contain 2022 weight-upload history. For example, [1.4B-v0 history](https://huggingface.co/api/models/EleutherAI/pythia-1.4b-v0/commits/main) records a weight upload in October 2022; [2.8B-v0 history](https://huggingface.co/api/models/EleutherAI/pythia-2.8b-v0/commits/main) records one in November 2022. Those timestamps establish historical repository records, not independently archived public visibility on the upload day. The v0 weight object IDs differ from the replacement suite. Do not silently substitute v0, deduplicated variants, later seeds, or a final-step branch under the same family name.

**The branch names have moved.** On this audit date:

| Mutable reference | Observed head | Material issue |
| --- | --- | --- |
| 1.4B `main` | `fedc38a16eea3bd36a96b906d78d11d2ce18ed79` | Adds safetensors on 2023-07-09, after DPO |
| 2.8B `main` | `2a259cdd96a4beb1cdf467512e3904197345f6a9` | Adds safetensors on 2023-06-09, after DPO |
| 1.4B `step143000` | `9cc5c8c8148a4e0115d9e29c6b4f21124cfe748a` | Adds safetensors shards on 2026-02-11 |
| 2.8B `step143000` | `dbe7ae300a54abcdc475a33907b3dff81d25709f` | Replaces `.bin` and safetensors objects on 2026-02-11 |

Sources are the public [1.4B refs](https://huggingface.co/api/models/EleutherAI/pythia-1.4b/refs), [2.8B refs](https://huggingface.co/api/models/EleutherAI/pythia-2.8b/refs), [1.4B final-step history](https://huggingface.co/api/models/EleutherAI/pythia-1.4b/commits/step143000), and [2.8B final-step history](https://huggingface.co/api/models/EleutherAI/pythia-2.8b/commits/step143000). Current main retains the April `.bin` object in both cases; a modern repository head is therefore not evidence that the original weights were post-trained. However, a loader can prefer the later safetensors file. The 2.8B final-step `.bin` object itself changed, so that branch cannot be described as a metadata-only update. Tensor equivalence was not tested. Pin the complete April main revision and its original file identities.

**The historical Pythia snapshots are base pretrained models.** Their immutable [1.4B card](https://huggingface.co/EleutherAI/pythia-1.4b/blob/8f0af839162ddb466006494a08733ee9cfa2d338/README.md) and [2.8B card](https://huggingface.co/EleutherAI/pythia-2.8b/blob/f20536c52a97faea73b8997cc789bd913853f14a/README.md) document Pile pretraining and absence of downstream instruction/chat fine-tuning. The selected trees contain a full `.bin` checkpoint, model config, tokenizer JSON, tokenizer config, and special-token map. There is no adapter artifact or chat template in these trees. This supports base-checkpoint selection; it does not independently audit every training example or prove the absence of undocumented operations.

The supplied tokenizer config names GPT-NeoX-20B and contains a publisher-local cache path. Load the co-located tokenizer files from the same pinned Pythia snapshot. Do not resolve a contemporary external tokenizer by that convenience field. Both Pythia candidates have identical tokenizer bytes:

| File | SHA-256 | Verification |
| --- | --- | --- |
| `tokenizer.json` | `c24618a1b3e6a38167beff1c72cffd126c3a66254347304b50547d12c5f25624` | Downloaded tokenizer bytes hashed locally |
| `tokenizer_config.json` | `70e38394e494931c6f773ba41e19460dd4436526b852207367f04341b4066d3f` | Downloaded metadata bytes hashed locally |
| `special_tokens_map.json` | `6f50ab5a5a509a1c309d6171f339b196a900dc9c99ad0408ff23bb615fdae7ad` | Downloaded metadata bytes hashed locally |
| 1.4B `pytorch_model.bin` | `056766b124a4ac70afcc722084d7c2b6cab80581e0d066709d72ae5c1a8640d8` | Publisher-reported LFS SHA-256; weights not acquired |
| 2.8B `pytorch_model.bin` | `36f0f93d1f5d44ca9c48a602c0788001a36ec10db9d1b84a40b81799d724c4f6` | Publisher-reported LFS SHA-256; weights not acquired |

The [1.4B immutable tree](https://huggingface.co/api/models/EleutherAI/pythia-1.4b/tree/8f0af839162ddb466006494a08733ee9cfa2d338?recursive=true&expand=true) and [2.8B immutable tree](https://huggingface.co/api/models/EleutherAI/pythia-2.8b/tree/f20536c52a97faea73b8997cc789bd913853f14a?recursive=true&expand=true) supply weight sizes, Git blob identities, and LFS object identities. The JSON also includes model-config hashes. A Git blob SHA-1 and a payload SHA-256 are different identities; they are labeled separately.

**Qwen is a distinct modern condition.** The [official Qwen3 announcement](https://qwenlm.github.io/blog/qwen3/) is dated April 29, 2025. Its account describes a four-stage post-training pipeline. The pinned [1.7B card](https://huggingface.co/Qwen/Qwen3-1.7B/blob/70d244cc86ccca08cf5af4e1e306ecf908b1ad5e/README.md) and [0.6B card](https://huggingface.co/Qwen/Qwen3-0.6B/blob/c1899de289a04d12100db370d81485cdf75e47ca/README.md) identify pretraining plus post-training. [1.7B history](https://huggingface.co/api/models/Qwen/Qwen3-1.7B/commits/main) and [0.6B history](https://huggingface.co/api/models/Qwen/Qwen3-0.6B/commits/main) show tokenizer-config edits on May 19 after the April weight uploads. A weights-only revision is insufficient to reproduce the modern prompting interface.

At the selected Qwen revisions, tokenizer-config SHA-256 is `d5d09f07b48c3086c508b30d1c9114bd1189145b74e982a265350c923acd8101` for both sizes. The embedded Jinja template, hashed as its decoded UTF-8 string, has SHA-256 `a55ee1b1660128b7098723e0abcd92caa0788061051c62d51cbe87d9cf1974d8`; it includes `enable_thinking`. Pin these files and record the thinking argument, generation config, rendered prompt, and any precision conversion. Current configs advertise BF16; local FP16 conversion would be an explicit experimental condition. No adapter or quantization config is present in the inspected Qwen trees. These observations do not imply that training data are historically eligible for older targets.

**A separate April Qwen condition is available for May 2025 targets.** The [full 1.7B April 29 tree](https://huggingface.co/api/models/Qwen/Qwen3-1.7B/tree/d3e258980a49b060055ea9038dad99d75923f7c4?recursive=true&expand=true) and [full 0.6B April 29 tree](https://huggingface.co/api/models/Qwen/Qwen3-0.6B/tree/6130ef31402718485ca4d80a6234f70d9a4cf362?recursive=true&expand=true) include weights, tokenizer JSON, merges, vocabulary, tokenizer config with thinking template, model config, and generation config. Their weight object identities match those reported for the modern revisions. Neither April tree contains the later standalone July `LICENSE`; the original cards and April publisher announcement declare Apache 2.0.

| April snapshot file/interface | 1.7B SHA-256 | 0.6B SHA-256 |
| --- | --- | --- |
| `tokenizer_config.json` | `5a7303fcb1a27ede63134a2cbd61d5282c247ca6d769ce4746d4ffa124aedd63` | `bbc2c089e3bef8753f63348c10595767be8998bc6ca7c7ebcaada346d401fba8` |
| Embedded UTF-8 chat template | `87a2728cb8dc9fe424d624542f6060ec05a1d285ebbec578bb078900e33396b5` | `87a2728cb8dc9fe424d624542f6060ec05a1d285ebbec578bb078900e33396b5` |
| `tokenizer.json` | `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4` | `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4` |

The April template is 4,116 characters; the modern template is 4,168. The May 19 edit adds string-type handling and changes reasoning-content handling. Template hashes differ even though weight identities match. No rendered-prompt parity was tested. Use the April tokenizer alongside April weights for historical runs; applying the modern template is a distinct interface intervention.

The [MeanFlow record](https://arxiv.org/abs/2505.13447) gives v1 submission as 2025-05-19 17:59:42 UTC. The [AlphaEvolve official announcement](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) is dated May 14, 2025. The April Qwen release precedes both recorded channels; exact earlier equivalent methods, prerelease code, talks, theses, and abstracts remain target-specific gates. This is a conditional date comparison, not certification of either target or Qwen's training corpus.

**Remaining admission gates:** an independently dated archive tying exact Pythia revisions to public availability has not been located; publisher release statements plus public paper and repository history are the current corroboration. Earlier equivalent DPO algebra, preprint announcements, author slides/talks/theses, and other public channels still require target-specific review. Capability, numerical replay, runtime, tensor identity after any conversion, and prompt leakage have not been measured. A later adapter, instruction tune, merged checkpoint, or external retrieval corpus must pass its own timing audit. No scientific-discovery claim is admitted by this document.
