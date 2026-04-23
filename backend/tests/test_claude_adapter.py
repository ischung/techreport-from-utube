"""Unit tests for ClaudeAdapter — only the parsing helper is exercised here,
since the real network call is mocked at the integration layer."""

from __future__ import annotations

import json

import pytest

from app.adapters.claude_adapter import _parse_json_payload


def test_parse_json_payload_strips_code_fence() -> None:
    payload = """```json
    {"overview": "hi", "coreConcepts": ["a"]}
    ```"""
    parsed = _parse_json_payload(payload)
    assert parsed["overview"] == "hi"
    assert parsed["coreConcepts"] == ["a"]


def test_parse_json_payload_plain_object() -> None:
    assert _parse_json_payload('{"a": 1}') == {"a": 1}


def test_parse_json_payload_rejects_garbage() -> None:
    with pytest.raises(json.JSONDecodeError):
        _parse_json_payload("not json")
