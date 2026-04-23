"""Adapter over YouTube Data API v3 (search.list).

Uses ``httpx`` directly rather than ``google-api-python-client`` so that
requests are easy to mock in tests via ``respx``.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import httpx

from app.ports.youtube_search_port import YouTubeSearchPort
from app.schemas import VideoSearchResult


class YouTubeDataAdapter(YouTubeSearchPort):
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    def __init__(self, api_key: str, *, timeout: float = 5.0) -> None:
        self._api_key = api_key
        self._timeout = timeout

    @staticmethod
    def _published_after(now: datetime | None = None) -> str:
        """Return an RFC3339 timestamp 30 days before ``now`` (UTC)."""
        ref = now or datetime.now(tz=UTC)
        return (ref - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")

    async def search_recent(self, keyword: str, *, max_results: int = 5) -> list[VideoSearchResult]:
        params = {
            "key": self._api_key,
            "q": keyword,
            "part": "snippet",
            "type": "video",
            "order": "date",
            "maxResults": max_results,
            "publishedAfter": self._published_after(),
        }
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            payload = response.json()

        results: list[VideoSearchResult] = []
        for item in payload.get("items", [])[:max_results]:
            vid = item["id"]["videoId"]
            snippet = item["snippet"]
            results.append(
                VideoSearchResult(
                    videoId=vid,
                    title=snippet["title"],
                    url=f"https://www.youtube.com/watch?v={vid}",
                    publishedAt=snippet["publishedAt"],
                    channelTitle=snippet["channelTitle"],
                )
            )
        return results
