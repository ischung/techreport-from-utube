"""FastAPI dependency factories.

Keeping these in a separate module makes overriding trivial in tests
(via ``app.dependency_overrides``).
"""

from __future__ import annotations

from functools import lru_cache

from fastapi import Depends

from app.adapters.claude_adapter import ClaudeAdapter
from app.adapters.ollama_adapter import OllamaAdapter
from app.adapters.openai_adapter import OpenAIAdapter
from app.adapters.youtube_data_adapter import YouTubeDataAdapter
from app.adapters.youtube_transcript_adapter import YouTubeTranscriptAdapter
from app.config import Settings, get_settings
from app.pipeline.analysis_pipeline import AnalysisPipeline
from app.ports.llm_provider import LLMProvider
from app.ports.transcript_port import TranscriptPort
from app.ports.youtube_search_port import YouTubeSearchPort
from app.repository.file_repository import FileRepository
from app.services.search_service import SearchService


def get_llm_provider(settings: Settings = Depends(get_settings)) -> LLMProvider:
    match settings.llm_provider:
        case "claude":
            return ClaudeAdapter(api_key=settings.anthropic_api_key)
        case "openai":
            return OpenAIAdapter(api_key=settings.openai_api_key)
        case "ollama":
            return OllamaAdapter(base_url=settings.ollama_base_url)
        case unknown:
            raise ValueError(
                f"Unknown LLM_PROVIDER: {unknown!r}. Valid values: claude | openai | ollama"
            )


def get_youtube_search_port(settings: Settings = Depends(get_settings)) -> YouTubeSearchPort:
    return YouTubeDataAdapter(api_key=settings.youtube_api_key)


@lru_cache(maxsize=1)
def _cached_search_service(api_key: str) -> SearchService:
    return SearchService(YouTubeDataAdapter(api_key=api_key))


def get_search_service(settings: Settings = Depends(get_settings)) -> SearchService:
    return _cached_search_service(settings.youtube_api_key)


def get_transcript_port() -> TranscriptPort:
    return YouTubeTranscriptAdapter()


def get_file_repository(settings: Settings = Depends(get_settings)) -> FileRepository:
    return FileRepository(settings.reports_dir)


def get_analysis_pipeline(
    settings: Settings = Depends(get_settings),
) -> AnalysisPipeline:
    return AnalysisPipeline(
        transcript_port=YouTubeTranscriptAdapter(),
        llm=get_llm_provider(settings),
        repository=FileRepository(settings.reports_dir),
    )
