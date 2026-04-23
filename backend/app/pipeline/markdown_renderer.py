"""Renders a ``ReportSection`` into the Markdown that ships to disk."""

from __future__ import annotations

from datetime import UTC, datetime

from app.ports.llm_provider import ReportSection
from app.schemas import AnalyzeRequest


def render(
    *,
    request: AnalyzeRequest,
    sections: ReportSection,
    llm_provider: str,
    generated_at: datetime | None = None,
) -> str:
    ts = (generated_at or datetime.now(tz=UTC)).strftime("%Y-%m-%dT%H:%M:%SZ")

    parts: list[str] = [
        f"# {request.title}",
        "",
        f"> **원본 영상**: [{request.url}]({request.url})",
        f"> **업로드 일자**: {request.published_at or '알 수 없음'}",
        f"> **보고서 생성**: {ts} · LLM={llm_provider}",
        "",
        "---",
        "",
        "## 개요",
        "",
        sections.overview.strip() or "_개요 정보가 비어 있습니다._",
        "",
        "## 핵심 개념",
        "",
    ]

    if sections.core_concepts:
        parts.extend(f"- {item.strip()}" for item in sections.core_concepts)
    else:
        parts.append("_추출된 핵심 개념이 없습니다._")

    parts.extend(
        [
            "",
            "## 상세 내용",
            "",
            sections.detailed_content.strip() or "_상세 내용이 비어 있습니다._",
            "",
            "## 강의 활용 팁",
            "",
            sections.lecture_tips.strip() or "_강의 활용 팁이 비어 있습니다._",
            "",
            "## 참고",
            "",
        ]
    )

    if sections.references:
        parts.extend(f"- {ref.strip()}" for ref in sections.references)
    else:
        parts.append(f"- 원본 영상: {request.url}")

    parts.append("")
    return "\n".join(parts)
