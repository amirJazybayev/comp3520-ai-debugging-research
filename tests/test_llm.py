import io
import json
import urllib.error

import pytest

from repair import llm as llm_mod
from repair.llm import ChatClient


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def ok_body():
    return json.dumps({"choices": [{"message": {"content": "```java\nclass Foo {}\n```"}}],
                       "usage": {"prompt_tokens": 12, "completion_tokens": 7}}).encode()


def test_request_and_response(monkeypatch):
    seen = {}

    def fake_urlopen(req, timeout):
        seen["url"], seen["body"], seen["auth"] = req.full_url, json.loads(req.data), req.get_header("Authorization")
        return FakeResponse(ok_body())

    monkeypatch.setattr(llm_mod.urllib.request, "urlopen", fake_urlopen)
    client = ChatClient(base_url="http://x/v1/", api_key="k", model="m", temperature=0.0)
    out = client([{"role": "user", "content": "hi"}])
    assert seen["url"] == "http://x/v1/chat/completions"
    assert seen["body"]["model"] == "m" and seen["body"]["temperature"] == 0.0
    assert seen["auth"] == "Bearer k"
    assert out["text"].startswith("```java") and out["prompt_tokens"] == 12 and out["completion_tokens"] == 7


def test_retries_on_rate_limit(monkeypatch):
    calls = []

    def fake_urlopen(req, timeout):
        calls.append(1)
        if len(calls) == 1:
            raise urllib.error.HTTPError(req.full_url, 429, "Too Many Requests", {}, io.BytesIO(b"slow down"))
        return FakeResponse(ok_body())

    monkeypatch.setattr(llm_mod.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(llm_mod.time, "sleep", lambda s: None)
    assert ChatClient(base_url="http://x", model="m")([])["completion_tokens"] == 7
    assert len(calls) == 2


def test_retries_on_read_timeout_then_gives_up(monkeypatch):
    calls = []

    def fake_urlopen(req, timeout):
        calls.append(timeout)
        raise TimeoutError("The read operation timed out")

    monkeypatch.setattr(llm_mod.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(llm_mod.time, "sleep", lambda s: None)
    with pytest.raises(RuntimeError, match="after 3 tries"):
        ChatClient(base_url="http://x", model="m", timeout=7, retries=2)([])
    assert calls == [7, 7, 7]


def test_timeout_and_reasoning_effort_from_environment(monkeypatch):
    seen = {}

    def fake_urlopen(req, timeout):
        seen["timeout"], seen["body"] = timeout, json.loads(req.data)
        return FakeResponse(ok_body())

    monkeypatch.setattr(llm_mod.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setenv("LLM_TIMEOUT", "42")
    monkeypatch.setenv("LLM_REASONING_EFFORT", "low")
    ChatClient(base_url="http://x", model="m")([])
    assert seen["timeout"] == 42 and seen["body"]["reasoning_effort"] == "low"
    monkeypatch.delenv("LLM_REASONING_EFFORT")
    ChatClient(base_url="http://x", model="m")([])
    assert "reasoning_effort" not in seen["body"]


def test_client_error_is_not_retried(monkeypatch):
    def fake_urlopen(req, timeout):
        raise urllib.error.HTTPError(req.full_url, 401, "Unauthorized", {}, io.BytesIO(b"bad key"))

    monkeypatch.setattr(llm_mod.urllib.request, "urlopen", fake_urlopen)
    with pytest.raises(RuntimeError, match="401"):
        ChatClient(base_url="http://x", model="m")([])


def test_missing_configuration(monkeypatch):
    monkeypatch.delenv("LLM_BASE_URL", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)
    with pytest.raises(RuntimeError, match="LLM_BASE_URL"):
        ChatClient()
