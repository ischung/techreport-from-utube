from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, HTTPException

from app.deps import get_search_service
from app.schemas import ApiError, SearchData, SearchRequest, SearchResponse
from app.services.search_service import SearchService

router = APIRouter(prefix="/api", tags=["search"])


@router.post("/search", response_model=SearchResponse)
async def search(
    body: SearchRequest,
    service: SearchService = Depends(get_search_service),
) -> SearchResponse:
    try:
        videos = await service.search(body.keyword)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=ApiError(
                code="YOUTUBE_API_ERROR",
                message=f"YouTube API returned {exc.response.status_code}.",
                retryable=True,
            ).model_dump(),
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=ApiError(
                code="YOUTUBE_API_ERROR",
                message="YouTube API unreachable.",
                retryable=True,
            ).model_dump(),
        ) from exc

    if not videos:
        raise HTTPException(
            status_code=404,
            detail=ApiError(
                code="NO_RESULTS",
                message="최근 1개월 이내 관련 영상을 찾지 못했어요.",
                retryable=False,
            ).model_dump(),
        )

    return SearchResponse(ok=True, data=SearchData(videos=videos))
