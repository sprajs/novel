"""Real tiny CPU reference model verifies phase release and persisted provenance."""
import importlib.util
from contextlib import contextmanager
import json
from pathlib import Path
from types import SimpleNamespace
import weakref

import pytest
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Qwen3Config, Qwen3ForCausalLM


def module():
    spec = importlib.util.spec_from_file_location("fast_equivalence", "scripts/fast_equivalence.py")
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def test_reference_model_is_gone_before_native_phase_and_vectors_are_persisted(tmp_path, monkeypatch):
    eq = module()
    references = []

    def load(*args, **kwargs):
        assert kwargs["local_files_only"] and kwargs["attn_implementation"] == "eager"
        cfg = Qwen3Config(vocab_size=31, hidden_size=16, intermediate_size=32, num_hidden_layers=2,
                         num_attention_heads=2, num_key_value_heads=1, head_dim=8, max_position_embeddings=64)
        cfg._attn_implementation = "eager"
        model = Qwen3ForCausalLM(cfg)
        references.append(weakref.ref(model))
        return model

    class Tokenizer:
        def apply_chat_template(self, *args, **kwargs):
            return "P"

        def __call__(self, text, **kwargs):
            return {"input_ids": {"P": [1, 2], "C": [3], "PC": [1, 2, 3]}[text]}

        def decode(self, ids, **kwargs):
            assert kwargs["skip_special_tokens"] is False
            return repr(list(ids))

    monkeypatch.setattr(AutoModelForCausalLM, "from_pretrained", load)
    monkeypatch.setattr(AutoTokenizer, "from_pretrained", lambda *a, **k: Tokenizer())
    args = SimpleNamespace(output=tmp_path, device="cpu", dtype="float32")
    config = {"cases": [{"id": "fixture", "messages": [{"role": "user", "content": "test"}], "continuation": "C"}]}
    entry = {"token_ids": {"generation_eos_token_ids": [29, 30]}}
    report = {"cases": [], "snapshot_hashes": {"fixture": "pinned"}, "reference": {"dtype": "float32"}, "config_sha256": "config"}

    def native(args, config, entry, report):
        assert references[0]() is None, "HF model still resident when native phase starts"
        assert report["reference_release"]["status"] == "PASS"
        saved = json.loads((tmp_path / "reference-phase.json").read_text())
        assert saved["cases"][0]["prompt_ids"] == [1, 2]
        step = saved["cases"][0]["steps"][0]
        assert eq.sha256_file(tmp_path / step["reference_logprobs_path"]) == step["reference_logprobs_sha256"]
        from safetensors.torch import load_file
        vector = load_file(str(tmp_path / step["reference_logprobs_path"]), device="cpu")["logprobs"]
        assert vector.shape == (31,) and vector.dtype == torch.float64 and vector.device.type == "cpu"

    monkeypatch.setattr(eq, "native_phase", native)
    before = torch.get_num_threads()
    try:
        torch.set_num_threads(1)
        eq.execute_phases(args, config, entry, tmp_path, report)
    finally:
        torch.set_num_threads(before)


def test_cuda_allocations_block_native_startup_without_gpu_execution(monkeypatch):
    eq = module()
    calls = []
    monkeypatch.setattr(torch.cuda, "synchronize", lambda device: calls.append("sync"))
    monkeypatch.setattr(torch.cuda, "empty_cache", lambda: calls.append("empty"))
    monkeypatch.setattr(torch.cuda, "memory_allocated", lambda device: 1024)
    with pytest.raises(ValueError, match="native server was not started"):
        eq.release_reference("cuda:0", 0)
    assert calls == ["sync", "empty"]


def test_persisted_reference_tampering_blocks_native_inference(tmp_path, monkeypatch):
    eq = module()
    path = tmp_path / "reference.safetensors"
    path.write_bytes(b"original reference")
    expected = eq.sha256_file(path)
    path.write_bytes(b"tampered reference")
    calls = []

    class Client:
        def prompt(self, messages):
            return "P", [1, 2]

        def call(self, endpoint, payload):
            calls.append(endpoint)
            assert endpoint == "/tokenize", "Model inference occurred after tampering"
            return {"tokens": [1, 2, 3]}

    @contextmanager
    def native(*args, **kwargs):
        yield Client(), {"artifact": {"model_key": "fixture", "revision": "pin", "source_file_sha256": {},
                                      "gguf_metadata": {"tokenizer.ggml.eos_token_id": 8}},
                         "props": {"chat_template": "template"}, "eog_token_ids": [8], "profile": {"context": 128}}

    monkeypatch.setattr(eq, "server", native)
    args = SimpleNamespace(output=tmp_path, gguf=tmp_path / "fixture.gguf", model="fixture", profile="cloud-cpu", termination="hf-eos")
    entry = {"revision": "pin", "chat_template": {"text": "template"}, "token_ids": {"generation_eos_token_ids": [8], "config_eos_token_id": 8}}
    report = {"snapshot_hashes": {}, "cases": [{"messages": [], "rendered_prompt": "P", "prompt_ids": [1, 2],
        "continuation": "C", "complete_ids": [1, 2, 3], "steps": [{"reference_logprobs_path": path.name, "reference_logprobs_sha256": expected}]}]}
    with pytest.raises(ValueError, match="changed between phases"):
        eq.native_phase(args, {}, entry, report)
    assert calls == ["/tokenize"]
