"""YouTube search port — the pipeline's only contract for retrieval."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas import VideoSearchResult


class YouTubeSearchPort(ABC):
    """Given a keyword, return up to 5 recent videos (last 30 days)."""

    @abstractmethod
    async def search_recent(self, keyword: str, *, max_results: int = 5) -> list[VideoSearchResult]:
        """Return at most ``max_results`` videos published within the last month.

        Ordering: most-recent upload first.
        """
