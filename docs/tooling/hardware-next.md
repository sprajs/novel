# Next hardware gates

The cloud test condition is CPU FP32. No NVIDIA GPU is exposed; no CUDA kernel,
FP16 memory limit, RTX 2080 Ti runtime, or optimized backend was measured here.
See [current tooling evidence](current-stack.md) for dated primary sources.

1. On an explicitly authorized GPU machine, record driver, free VRAM, CUDA wheel
   build and `torch.cuda.get_arch_list()`. RTX 2080 Ti is SM75/Turing: use FP16;
   native BF16 tensor-core execution is unsuitable. Retain an FP32 short check.
2. Create a **separate** CUDA environment. PyTorch 2.8.0 cu126 is a candidate,
   not a tested binary in this repository. Confirm official wheel architecture
   and driver support, then generate its own exact lock. Do not replace the
   checked CPU lock or copy a current CUDA13 default blindly.
3. Run the `gpu` marked tests in that CUDA environment, then a pinned 0.6B FP16
   adaptation of the smoke at batch one and short sequence. Save actual dtype,
   device, per-invariant errors, peak allocated/reserved memory and synchronized
   timing. Establish tolerances from repeated clean measurements before testing
   causal hypotheses. This runner currently rejects CUDA configs deliberately;
   extending it is part of this prospective validation, not an existing command.
4. Only after that passes, test 1.7B at 256/512/1024 total tokens sequentially.
   Keep selected positions only, no full logits/attention artifacts. A source
   checkpoint fitting in VRAM does not establish that gradients fit.
5. Gradients come after exact forward baselines: disable inference mode, create
   a selected activation leaf with `requires_grad=True` while keeping parameters
   frozen, test a short scalar objective against finite differences, and record
   backward memory/cost. No gradient implementation is claimed in this increment.

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
