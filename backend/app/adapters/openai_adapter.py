"""OpenAI adapter — student exercise stub.

Part of the Port-Adapter educational exercise (see CLAUDE.md). A student who
wants to swap providers sets ``LLM_PROVIDER=openai`` in ``.env`` and fills
in the three TODOs below — no other application code changes.
"""

from __future__ import annotations

from app.ports.llm_provider import LLMProvider, ReportSection


class OpenAIAdapter(LLMProvider):
    name = "openai"

    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self._api_key = api_key  # TODO(학생 실습 1): 공식 OpenAI SDK 클라이언트 생성
        self._model = model

    async def structure(
        self,
        *,
        title: str,  # noqa: ARG002
        transcript: str,  # noqa: ARG002
        system_prompt: str,  # noqa: ARG002
    ) -> ReportSection:
        # TODO(학생 실습 2): OpenAI chat.completions API 호출
        #   system=system_prompt, user={title, transcript}, json_object 응답 형식
        # TODO(학생 실습 3): 응답 JSON을 ReportSection 으로 매핑
        raise NotImplementedError(
            "OpenAIAdapter.structure() is a student-exercise stub. "
            "Implement three TODOs above to complete the provider swap."
        )
