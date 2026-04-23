from __future__ import annotations

import pytest

from app.adapters.claude_adapter import ClaudeAdapter
from app.adapters.ollama_adapter import OllamaAdapter
from app.adapters.openai_adapter import OpenAIAdapter
from app.config import Settings
from app.deps import get_llm_provider


@pytest.mark.parametrize(
    ("provider", "cls"),
    [
        ("claude", ClaudeAdapter),
        ("openai", OpenAIAdapter),
        ("ollama", OllamaAdapter),
    ],
)
def test_deps_returns_matching_adapter(
    provider: str, cls: type, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("LLM_PROVIDER", provider)
    settings = Settings(_env_file=None)
    adapter = get_llm_provider(settings)
    assert isinstance(adapter, cls)
    assert adapter.name == provider


def test_deps_rejects_unknown_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "definitely-not-a-provider")
    settings = Settings(_env_file=None)
    with pytest.raises(ValueError, match="Unknown LLM_PROVIDER"):
        get_llm_provider(settings)
