from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.deps import get_analysis_pipeline
from app.pipeline.analysis_pipeline import AnalysisPipeline
from app.ports.transcript_port import NoTranscriptError
from app.schemas import AnalyzeRequest, AnalyzeResponse, ApiError

router = APIRouter(prefix="/api", tags=["analyze"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    body: AnalyzeRequest,
    pipeline: AnalysisPipeline = Depends(get_analysis_pipeline),
) -> AnalyzeResponse:
    try:
        report = await pipeline.run(body)
    except NoTranscriptError as exc:
        raise HTTPException(
            status_code=422,
            detail=ApiError(
                code="NO_TRANSCRIPT",
                message="해당 영상은 자막을 제공하지 않아 분석할 수 없어요. 다른 영상을 선택해주세요.",
                retryable=False,
            ).model_dump(),
        ) from exc
    except TimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail=ApiError(
                code="LLM_TIMEOUT",
                message="분석 중 시간이 초과되었어요. 다시 시도해주세요.",
                retryable=True,
            ).model_dump(),
        ) from exc
    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail=ApiError(
                code="SAVE_FAILED",
                message="보고서 저장에 실패했어요. 재시도해주세요.",
                retryable=True,
            ).model_dump(),
        ) from exc

    return AnalyzeResponse(ok=True, data=report)
