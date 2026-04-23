"""Unit tests for ClaudeAdapter — parsing helper + retry policy."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import pytest

from app.adapters.claude_adapter import ClaudeAdapter, _is_retryable, _parse_json_payload


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


def test_is_retryable_timeout_is_retryable() -> None:
    assert _is_retryable(TimeoutError("slow")) is True


def test_is_retryable_value_error_not_retryable() -> None:
    assert _is_retryable(ValueError("nope")) is False


def test_is_retryable_matches_anthropic_class_names_by_name() -> None:
    class APITimeoutError(Exception):
        pass

    class RateLimitError(Exception):
        pass

    class RandomError(Exception):
        pass

    assert _is_retryable(APITimeoutError()) is True
    assert _is_retryable(RateLimitError()) is True
    assert _is_retryable(RandomError()) is False


@pytest.mark.anyio
async def test_structure_retries_once_then_succeeds() -> None:
    adapter = ClaudeAdapter(api_key="dummy", timeout=1.0)
    calls = {"n": 0}
    good = AsyncMock(
        return_value=type(
            "Fake",
            (),
            {
                "content": [
                    type(
                        "Block",
                        (),
                        {
                            "type": "text",
                            "text": json.dumps(
                                {
                                    "overview": "ok",
                                    "coreConcepts": ["c"],
                                    "detailedContent": "",
                                    "lectureTips": "",
                                    "references": [],
                                }
                            ),
                        },
                    )
                ]
            },
        )(),
    )

    async def flaky(*args, **kwargs):  # noqa: ARG001
        calls["n"] += 1
        if calls["n"] == 1:
            raise TimeoutError("first shot")
        return await good()

    # Patch _call_once's client.messages.create by patching _get_client to
    # return an object whose messages.create is our flaky coroutine.
    fake_client = type(
        "Client",
        (),
        {"messages": type("M", (), {"create": flaky})()},
    )()
    with patch.object(adapter, "_get_client", return_value=fake_client):
        result = await adapter.structure(title="t", transcript="x", system_prompt="s")
    assert calls["n"] == 2
    assert result.overview == "ok"


@pytest.mark.anyio
async def test_structure_raises_after_second_failure() -> None:
    adapter = ClaudeAdapter(api_key="dummy", timeout=1.0)

    async def always_fail(*args, **kwargs):  # noqa: ARG001
        raise TimeoutError("still slow")

    fake_client = type(
        "Client",
        (),
        {"messages": type("M", (), {"create": always_fail})()},
    )()
    with (
        patch.object(adapter, "_get_client", return_value=fake_client),
        pytest.raises(TimeoutError),
    ):
        await adapter.structure(title="t", transcript="x", system_prompt="s")


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
