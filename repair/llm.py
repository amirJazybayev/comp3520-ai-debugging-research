"""Minimal client for any OpenAI-compatible chat-completions endpoint (stdlib only).

Works with OpenAI, Google Gemini (OpenAI-compatible endpoint), Groq, OpenRouter, Ollama, LM Studio,
and Anthropic's OpenAI-compatible endpoint. Configure with environment variables:
  LLM_BASE_URL  e.g. https://api.openai.com/v1  or  http://localhost:11434/v1 (Ollama)
  LLM_API_KEY   API key (any non-empty string for Ollama)
  LLM_MODEL     model name
"""
import json
import os
import time
import urllib.error
import urllib.request


class ChatClient:
    def __init__(self, base_url=None, api_key=None, model=None, temperature=0.2, timeout=None, retries=7):
        self.base_url = (base_url or os.environ.get("LLM_BASE_URL", "")).rstrip("/")
        self.api_key = api_key or os.environ.get("LLM_API_KEY", "")
        self.model = model or os.environ.get("LLM_MODEL", "")
        if not (self.base_url and self.model):
            raise RuntimeError("Set LLM_BASE_URL and LLM_MODEL (and LLM_API_KEY) - see README")
        self.timeout = timeout or float(os.environ.get("LLM_TIMEOUT", "300"))
        # optional, e.g. "low": limits hidden "thinking" time on reasoning models
        self.reasoning_effort = os.environ.get("LLM_REASONING_EFFORT", "")
        self.temperature, self.retries = temperature, retries

    def __call__(self, messages):
        payload = {"model": self.model, "messages": messages, "temperature": self.temperature}
        if self.reasoning_effort:
            payload["reasoning_effort"] = self.reasoning_effort
        body = json.dumps(payload).encode()
        req = urllib.request.Request(
            self.base_url + "/chat/completions", data=body, method="POST",
            # Groq's Cloudflare front end rejects the default "Python-urllib" agent (error 1010)
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}",
                     "User-Agent": "comp3520-repair-harness/1.0"})
        start = time.monotonic()
        for attempt in range(self.retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as e:
                # rate limits and server errors are common on free tiers: back off and retry
                if e.code in (429, 500, 502, 503, 504) and attempt < self.retries:
                    wait = min(60, 5 * 2 ** attempt)
                    print(f"  LLM busy (HTTP {e.code}); retry {attempt + 1}/{self.retries} in {wait}s", flush=True)
                    time.sleep(wait)
                    continue
                raise RuntimeError(f"LLM request failed: HTTP {e.code} {e.read()[:500]!r}") from e
            except (TimeoutError, urllib.error.URLError) as e:
                # slow or dropped connections: retry, then give up with a clear message
                if attempt < self.retries:
                    print(f"  LLM call failed ({e}); retry {attempt + 1}/{self.retries}", flush=True)
                    time.sleep(min(60, 5 * 2 ** attempt))
                    continue
                raise RuntimeError(f"LLM request failed after {self.retries + 1} tries: {e}") from e
        usage = data.get("usage") or {}
        return {
            "text": data["choices"][0]["message"]["content"] or "",
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
            "seconds": round(time.monotonic() - start, 2),
        }
