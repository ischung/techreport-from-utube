"""Shared Pydantic DTOs — mirror of shared/types.ts on the frontend side.

Kept deliberately flat. Each enlargement should be motivated by a TechSpec
section number so the mirror stays in sync.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class HealthData(BaseModel):
    """Data payload for /api/health — TechSpec §5-3."""

    status: Literal["up", "degraded", "down"] = "up"
    llm_provider: str = Field(..., alias="llmProvider")
    version: str

    model_config = {"populate_by_name": True}


class HealthResponse(BaseModel):
    ok: bool = True
    data: HealthData


class VideoSearchResult(BaseModel):
    """Video metadata returned by /api/search — TechSpec §4-1."""

    video_id: str = Field(..., alias="videoId")
    title: str
    url: str
    published_at: str = Field(..., alias="publishedAt")
    channel_title: str = Field(..., alias="channelTitle")

    model_config = {"populate_by_name": True}


class SearchRequest(BaseModel):
    keyword: str = Field(..., min_length=2, max_length=100)


class SearchData(BaseModel):
    videos: list[VideoSearchResult]


class SearchResponse(BaseModel):
    ok: bool = True
    data: SearchData


class AnalyzeRequest(BaseModel):
    video_id: str = Field(..., alias="videoId", min_length=1)
    title: str = Field(..., min_length=1)
    url: str = Field(..., min_length=1)
    published_at: str = Field(default="", alias="publishedAt")

    model_config = {"populate_by_name": True}


class ReportSectionDTO(BaseModel):
    """Structured output the pipeline writes into the final report."""

    overview: str
    core_concepts: list[str] = Field(default_factory=list, alias="coreConcepts")
    detailed_content: str = Field(default="", alias="detailedContent")
    lecture_tips: str = Field(default="", alias="lectureTips")
    references: list[str] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class AnalysisReport(BaseModel):
    video_id: str = Field(..., alias="videoId")
    title: str
    source_url: str = Field(..., alias="sourceUrl")
    published_at: str = Field(default="", alias="publishedAt")
    generated_at: str = Field(..., alias="generatedAt")
    llm_provider: str = Field(..., alias="llmProvider")
    sections: ReportSectionDTO
    markdown: str
    saved_path: str = Field(..., alias="savedPath")

    model_config = {"populate_by_name": True}


class AnalyzeResponse(BaseModel):
    ok: bool = True
    data: AnalysisReport


class ApiError(BaseModel):
    code: str
    message: str
    retryable: bool = False


class ApiErrorResponse(BaseModel):
    ok: bool = False
    error: ApiError
