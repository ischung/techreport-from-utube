"""Default adapter — Anthropic Claude Sonnet 4.6.

The full implementation (actual API call + prompt caching) lands in issue
#12 (CI-11). This file exists now so dependency injection can resolve the
provider during #8 without pulling the anthropic SDK's network stack into
import time.
"""

from __future__ import annotations

from app.ports.llm_provider import LLMProvider, ReportSection


class ClaudeAdapter(LLMProvider):
    """Claude provider — wiring only at this stage; real `structure()` in #12."""

    name = "claude"

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6") -> None:
        self._api_key = api_key
        self._model = model

    async def structure(
        self,
        *,
        title: str,  # noqa: ARG002 — keeps the signature stable for #12
        transcript: str,  # noqa: ARG002
        system_prompt: str,  # noqa: ARG002
    ) -> ReportSection:
        raise NotImplementedError(
            "ClaudeAdapter.structure() lands in issue #12 (US-02 slice). "
            "For now, health-check and provider-selection code paths only "
            "need the adapter's identity (`.name`) and constructor."
        )
