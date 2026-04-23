from __future__ import annotations

import os

import pytest

from app.config import Settings, get_settings


def test_settings_default_llm_provider_is_claude(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("LLM_PROVIDER", "ANTHROPIC_API_KEY", "YOUTUBE_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    settings = Settings(_env_file=None)
    assert settings.llm_provider == "claude"


def test_settings_reads_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-dummy")
    settings = Settings(_env_file=None)
    assert settings.llm_provider == "openai"
    assert settings.openai_api_key == "sk-dummy"


def test_get_settings_returns_a_settings_instance() -> None:
    assert isinstance(get_settings(), Settings)


def test_reports_dir_default() -> None:
    os.environ.pop("REPORTS_DIR", None)
    s = Settings(_env_file=None)
    assert s.reports_dir.endswith("reports")
