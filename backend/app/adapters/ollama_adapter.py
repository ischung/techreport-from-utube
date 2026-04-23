"""Ollama local adapter — student exercise stub.

Runs an open model locally (llama, qwen, exaone, …) via the Ollama daemon.
Enables offline, zero-cost demos for classroom use.
"""

from __future__ import annotations

from app.ports.llm_provider import LLMProvider, ReportSection


class OllamaAdapter(LLMProvider):
    name = "ollama"

    def __init__(self, base_url: str, model: str = "qwen2.5") -> None:
        self._base_url = base_url
        self._model = model

    async def structure(
        self,
        *,
        title: str,  # noqa: ARG002
        transcript: str,  # noqa: ARG002
        system_prompt: str,  # noqa: ARG002
    ) -> ReportSection:
        # TODO(학생 실습): POST {base_url}/api/chat
        #   JSON payload: {model, messages: [system, user], format: "json"}
        # 응답 JSON 을 ReportSection 으로 매핑.
        raise NotImplementedError(
            "OllamaAdapter.structure() is a student-exercise stub. "
            "Use httpx to POST to the Ollama chat endpoint."
        )
