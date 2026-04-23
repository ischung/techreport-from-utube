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
