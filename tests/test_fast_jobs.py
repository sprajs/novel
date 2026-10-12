import json
import io
from pathlib import Path
import threading

import pytest

from novel.fast_jobs import prediction_jobs
from novel.fast_runtime import Client, complete_with_termination, completion_request


class BatchClient:
    def prompt(self, messages):
        return "prompt", [1 if messages[0]["content"] == "bad" else 2]

    def call(self, endpoint, request, *, response_path=None):
        assert endpoint == "/completion"
        bad = request["prompt"] == [1]
        response = {"content": '{"answer":' if bad else '{"answer":"yes"}', "tokens": [5],
                    "completion_probabilities": [{"id": 5, "logprob": -0.2}],
                    "tokens_evaluated": 1, "stop_type": "limit", "truncated": False}
        if response_path:
            response_path.write_text(json.dumps(response))
        return response


def test_incomplete_structured_output_keeps_tokens_and_probs_before_parse(tmp_path, monkeypatch):
    import novel.fast_jobs as jobs
    original = jobs.strict_json

    def parse(text):
        receipt = json.loads((tmp_path / "response-0000-0000.json").read_text())
        assert receipt["raw_response"]["tokens"] == [5]
        assert receipt["raw_response"]["completion_probabilities"][0]["logprob"] == -0.2
        return original(text)

    monkeypatch.setattr(jobs, "strict_json", parse)
    records = prediction_jobs(BatchClient(), {"profile": {"context": 128}, "eog_token_ids": [8]},
        [{"id": "bad", "messages": [{"role": "user", "content": "bad"}]}], tmp_path,
        repeats=1, slots=1, options={"tokens": 1, "seed": 17}, schema={})
    assert records[0]["status"] == "FAIL"
    assert records[0]["error"]["stage"] == "output_parse"
    assert records[0]["raw_response"]["tokens"] == [5]
    assert len(records[0]["http_receipts"]) == 1


def test_earlier_failure_does_not_discard_later_success(tmp_path):
    release = threading.Event()

    class MixedClient(BatchClient):
        def call(self, endpoint, request, **kwargs):
            if request["prompt"] == [1]:
                release.set()
            else:
                assert release.wait(timeout=2)
            return super().call(endpoint, request, **kwargs)

    records = prediction_jobs(MixedClient(), {"profile": {"context": 128}, "eog_token_ids": [8]},
        [{"id": name, "messages": [{"role": "user", "content": name}]} for name in ("bad", "good")],
        tmp_path, repeats=1, slots=2, options={"tokens": 1, "seed": 17}, schema={})
    assert [r["status"] for r in records] == ["FAIL", "PASS"]
    assert records[1]["parsed_json"] == {"answer": "yes"}
    assert len(list(tmp_path.glob("record-*.json"))) == 2
    assert len(list(tmp_path.glob("response-*.http.json"))) == 2


def test_invalid_server_contract_also_keeps_received_response(tmp_path):
    class BadContract(BatchClient):
        def call(self, *args, **kwargs):
            response = super().call(*args, **kwargs)
            response["truncated"] = True
            return response

    records = prediction_jobs(BadContract(), {"profile": {"context": 128}, "eog_token_ids": []},
        [{"id": "good", "messages": [{"role": "user", "content": "good"}]}], tmp_path,
        repeats=1, slots=1, options={"tokens": 1, "seed": 17})
    assert records[0]["error"]["stage"] == "generation"
    assert records[0]["raw_response"]["truncated"] is True
    assert (tmp_path / "response-0000-0000.json").exists()


def test_invalid_http_json_is_saved_before_api_decode(tmp_path, monkeypatch):
    body = b'{"tokens":[5],'
    monkeypatch.setattr("novel.fast_runtime.urlopen", lambda *a, **k: io.BytesIO(body))
    path = tmp_path / "response.http.json"
    with pytest.raises(json.JSONDecodeError):
        Client("http://127.0.0.1:1").call("/completion", {}, response_path=path)
    assert path.read_bytes() == body


def test_http_error_response_is_saved_before_failure(tmp_path, monkeypatch):
    from urllib.error import HTTPError
    error = HTTPError("http://127.0.0.1:1", 500, "native error", {}, io.BytesIO(b'{"error":"failed"}'))

    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr("novel.fast_runtime.urlopen", fail)
    path = tmp_path / "response.http.json"
    with pytest.raises(HTTPError):
        Client("http://127.0.0.1:1").call("/completion", {}, response_path=path)
    assert json.loads(path.read_text()) == {"error": "failed"}


def test_greedy_adapter_keeps_extra_native_eog_and_resumes_exact_prefix():
    class Chunks:
        def __init__(self):
            self.requests = []

        def call(self, endpoint, request):
            if endpoint == "/detokenize":
                assert request["tokens"] == [7, 5, 8]
                return {"content": "</s>word<|im_end|>"}
            self.requests.append(request)
            tokens = [7] if len(self.requests) == 1 else [5, 8]
            return {"tokens": tokens, "content": "", "stop_type": "eos",
                    "tokens_evaluated": len(request["prompt"]), "truncated": False}

    client = Chunks()
    response, chunks = complete_with_termination(client, completion_request([1], tokens=4), 128,
        policy="hf-eos", eos_ids=[8], native_eog_ids=[7, 8])
    assert response["tokens"] == [7, 5, 8] and response["stop_type"] == "eos"
    assert client.requests[1]["prompt"] == [1, 7]
    assert client.requests[1]["n_predict"] == 3
    assert len(chunks) == 2
    assert all(not r["ignore_eos"] and "logit_bias" not in r for r in client.requests)


@pytest.mark.parametrize("kwargs", [{"temperature": 0.7}, {"cache_prompt": True}, {"schema": {}}])
def test_adapter_rejects_rng_or_grammar_reset_semantics(kwargs):
    with pytest.raises(ValueError, match="greedy unconstrained"):
        complete_with_termination(None, completion_request([1], **kwargs), 128,
                                 policy="hf-eos", eos_ids=[8], native_eog_ids=[7, 8])
