"""LLM provider port — the only thing the pipeline depends on.

Implementations live in ``app.adapters``. The pipeline constructs a provider
via ``app.deps.get_llm_provider()`` and calls ``structure()`` — nothing else.

Educational note: this is the Hexagonal (Ports & Adapters) pattern applied
to a single boundary. Students can replace ClaudeAdapter with another
adapter by flipping ``LLM_PROVIDER`` in ``.env`` — zero application-code
change. That is the Dependency Inversion Principle, made tangible.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ReportSection:
    """Structured analysis output that a provider must return."""

    overview: str
    core_concepts: list[str]
    detailed_content: str
    lecture_tips: str
    references: list[str]


class LLMProvider(ABC):
    """Contract: given a transcript, return a structured report section."""

    name: str

    @abstractmethod
    async def structure(
        self,
        *,
        title: str,
        transcript: str,
        system_prompt: str,
    ) -> ReportSection:
        """Turn a raw transcript into a structured Korean-language report."""
