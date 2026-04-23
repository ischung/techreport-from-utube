from __future__ import annotations

from datetime import UTC, datetime

from app.pipeline import markdown_renderer
from app.ports.llm_provider import ReportSection
from app.schemas import AnalyzeRequest


def _request() -> AnalyzeRequest:
    return AnalyzeRequest(
        videoId="abc123",
        title="LLM 에이전트 만들기",
        url="https://www.youtube.com/watch?v=abc123",
        publishedAt="2026-04-15T10:00:00Z",
    )


def test_render_builds_five_sections_with_metadata() -> None:
    req = _request()
    sections = ReportSection(
        overview="개요 문장.",
        core_concepts=["개념 A", "개념 B"],
        detailed_content="상세 본문 Markdown.",
        lecture_tips="강의에 쓰기 좋음.",
        references=["https://example.com/link1"],
    )
    ts = datetime(2026, 4, 24, 8, 0, tzinfo=UTC)
    md = markdown_renderer.render(
        request=req, sections=sections, llm_provider="claude", generated_at=ts
    )
    assert md.splitlines()[0] == "# LLM 에이전트 만들기"
    assert "2026-04-24T08:00:00Z" in md
    assert "## 개요" in md
    assert "## 핵심 개념" in md
    assert "- 개념 A" in md
    assert "## 상세 내용" in md
    assert "## 강의 활용 팁" in md
    assert "## 참고" in md
    assert "- https://example.com/link1" in md


def test_render_substitutes_placeholders_when_sections_empty() -> None:
    req = _request()
    sections = ReportSection(
        overview="", core_concepts=[], detailed_content="", lecture_tips="", references=[]
    )
    md = markdown_renderer.render(request=req, sections=sections, llm_provider="claude")
    assert "_개요 정보가 비어 있습니다._" in md
    assert "_추출된 핵심 개념이 없습니다._" in md
    # the fallback reference must point back at the original URL
    assert "- 원본 영상: https://www.youtube.com/watch?v=abc123" in md
