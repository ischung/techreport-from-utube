"""Default adapter — Anthropic Claude Sonnet 4.6.

Applies prompt caching to the system prompt so repeated calls within the
5-minute ephemeral window pay ~10% of the input-token rate.
"""

from __future__ import annotations

import json

from app.ports.llm_provider import LLMProvider, ReportSection


class ClaudeAdapter(LLMProvider):
    """Claude provider with prompt caching."""

    name = "claude"

    def __init__(
        self,
        api_key: str,
        *,
        model: str = "claude-sonnet-4-6",
        max_tokens: int = 4096,
    ) -> None:
        self._api_key = api_key
        self._model = model
        self._max_tokens = max_tokens
        self._client = None

    def _get_client(self):  # type: ignore[no-untyped-def]
        if self._client is None:
            import anthropic

            self._client = anthropic.AsyncAnthropic(api_key=self._api_key)
        return self._client

    async def structure(
        self,
        *,
        title: str,
        transcript: str,
        system_prompt: str,
    ) -> ReportSection:
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
