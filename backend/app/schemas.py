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


class ApiError(BaseModel):
    code: str
    message: str
    retryable: bool = False


class ApiErrorResponse(BaseModel):
    ok: bool = False
    error: ApiError
