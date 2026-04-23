"""Orchestrates Retrieval → Analysis → Rendering → Save for a single video."""

from __future__ import annotations

from datetime import UTC, datetime

from app.pipeline import markdown_renderer
from app.pipeline.system_prompt import SYSTEM_PROMPT_KR
from app.ports.llm_provider import LLMProvider
from app.ports.transcript_port import NoTranscriptError, TranscriptPort
from app.repository.file_repository import FileRepository
from app.schemas import AnalysisReport, AnalyzeRequest, ReportSectionDTO


class AnalysisPipeline:
    def __init__(
        self,
        *,
        transcript_port: TranscriptPort,
        llm: LLMProvider,
        repository: FileRepository,
    ) -> None:
        self._transcript = transcript_port
        self._llm = llm
        self._repo = repository

    async def run(self, request: AnalyzeRequest) -> AnalysisReport:
        transcript = await self._transcript.fetch(request.video_id)
        if not transcript.strip():
            raise NoTranscriptError(f"Empty transcript for {request.video_id!r}")

        sections = await self._llm.structure(
            title=request.title,
            transcript=transcript,
            system_prompt=SYSTEM_PROMPT_KR,
        )

        generated_at = datetime.now(tz=UTC)
        markdown = markdown_renderer.render(
            request=request,
            sections=sections,
            llm_provider=self._llm.name,
            generated_at=generated_at,
        )

        saved_path = await self._repo.save(
            title=request.title,
            video_id=request.video_id,
            markdown=markdown,
            generated_at=generated_at,
        )

        return AnalysisReport(
            videoId=request.video_id,
            title=request.title,
            sourceUrl=request.url,
            publishedAt=request.published_at,
            generatedAt=generated_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            llmProvider=self._llm.name,
            sections=ReportSectionDTO(
                overview=sections.overview,
                coreConcepts=list(sections.core_concepts),
                detailedContent=sections.detailed_content,
                lectureTips=sections.lecture_tips,
                references=list(sections.references),
            ),
            markdown=markdown,
            savedPath=saved_path,
        )
