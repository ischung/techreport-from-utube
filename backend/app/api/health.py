from fastapi import APIRouter, Depends

from app import __version__
from app.config import Settings, get_settings
from app.observability.token_counter import TokenCounter, get_token_counter
from app.schemas import HealthData, HealthResponse

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(
    settings: Settings = Depends(get_settings),
    counter: TokenCounter = Depends(get_token_counter),
) -> HealthResponse:
    """Return a minimal status envelope + cumulative Claude token usage
    so the dashboard can display an approximate spend since process start."""
    usage = counter.snapshot()
    return HealthResponse(
        ok=True,
        data=HealthData(
            status="up",
            llmProvider=settings.llm_provider,
            version=__version__,
            tokensInput=usage.input_tokens,
            tokensOutput=usage.output_tokens,
            tokensCacheRead=usage.cache_read_tokens,
            estimatedCostUsd=usage.estimated_cost_usd(),
        ),
    )
