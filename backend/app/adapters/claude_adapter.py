"""Default adapter — Anthropic Claude Sonnet 4.6.

Applies prompt caching to the system prompt so repeated calls within the
5-minute ephemeral window pay ~10% of the input-token rate.

Resilience: a single automatic retry on transient errors (timeout / 5xx).
The second failure bubbles up so the route handler can surface a rose-
colored LogStream entry.
"""

from __future__ import annotations

import asyncio
import json
import logging

from app.ports.llm_provider import LLMProvider, ReportSection

_LOG = logging.getLogger(__name__)

_CLIENT_TIMEOUT_SECONDS = 30.0
_RETRY_BACKOFF_SECONDS = 2.0


class ClaudeAdapter(LLMProvider):
    """Claude provider with prompt caching + one-shot retry."""

    name = "claude"

    def __init__(
        self,
        api_key: str,
        *,
        model: str = "claude-sonnet-4-6",
        max_tokens: int = 4096,
        timeout: float = _CLIENT_TIMEOUT_SECONDS,
    ) -> None:
        self._api_key = api_key
        self._model = model
        self._max_tokens = max_tokens
        self._timeout = timeout
        self._client = None

    def _get_client(self):  # type: ignore[no-untyped-def]
        if self._client is None:
            import anthropic

            self._client = anthropic.AsyncAnthropic(api_key=self._api_key, timeout=self._timeout)
        return self._client

    async def structure(
        self,
        *,
        title: str,
        transcript: str,
        system_prompt: str,
    ) -> ReportSection:
        try:
            return await self._call_once(
                title=title, transcript=transcript, system_prompt=system_prompt
            )
        except Exception as first_err:  # noqa: BLE001 — SDK exceptions vary by version
            if not _is_retryable(first_err):
                raise
            _LOG.warning("Claude call failed once (%s); retrying", type(first_err).__name__)
            await asyncio.sleep(_RETRY_BACKOFF_SECONDS)
            return await self._call_once(
                title=title, transcript=transcript, system_prompt=system_prompt
            )

    async def _call_once(self, *, title: str, transcript: str, system_prompt: str) -> ReportSection:
        client = self._get_client()
        message = await client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            system=[
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": f"제목: {title}\n\n자막:\n{transcript}",
                }
            ],
        )

        text = "".join(
            block.text for block in message.content if getattr(block, "type", None) == "text"
        ).strip()

        payload = _parse_json_payload(text)
        return ReportSection(
            overview=str(payload.get("overview", "")),
            core_concepts=list(payload.get("coreConcepts", [])),
            detailed_content=str(payload.get("detailedContent", "")),
            lecture_tips=str(payload.get("lectureTips", "")),
            references=list(payload.get("references", [])),
        )


def _is_retryable(exc: BaseException) -> bool:
    """Return True for transient errors worth a single retry."""
    if isinstance(exc, TimeoutError):
        return True
    name = type(exc).__name__
    # anthropic SDK lifts HTTP problems into its own classes; match by name so
    # we don't have to import the SDK just for isinstance checks in hot code.
    return name in {
        "APITimeoutError",
        "APIConnectionError",
        "InternalServerError",
        "RateLimitError",
    }


def _parse_json_payload(text: str) -> dict:
    """Tolerant JSON parse — strips code fences if the model wrapped them."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```", 2)[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()
    return json.loads(cleaned)
