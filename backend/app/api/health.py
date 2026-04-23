from fastapi import APIRouter, Depends

from app import __version__
from app.config import Settings, get_settings
from app.schemas import HealthData, HealthResponse

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """Return a minimal status envelope so the frontend dashboard can
    prove end-to-end connectivity without invoking any external API."""
    return HealthResponse(
        ok=True,
        data=HealthData(
            status="up",
            llmProvider=settings.llm_provider,
            version=__version__,
        ),
    )
