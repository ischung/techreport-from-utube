from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import httpx
import pytest
from fastapi.testclient import TestClient

from app.deps import get_search_service
from app.main import app
from app.schemas import VideoSearchResult


class FakeService:
    def __init__(self, videos: list[VideoSearchResult] | None = None) -> None:
        self._videos = videos or []

    async def search(self, keyword: str) -> list[VideoSearchResult]:  # noqa: ARG002
        return self._videos


@pytest.fixture(autouse=True)
def reset_overrides():
    app.dependency_overrides.pop(get_search_service, None)
    yield
    app.dependency_overrides.pop(get_search_service, None)


def _sample_video(i: int = 0) -> VideoSearchResult:
    return VideoSearchResult(
        videoId=f"vid{i}",
        title=f"Video {i}",
        url=f"https://www.youtube.com/watch?v=vid{i}",
        publishedAt="2026-04-15T10:00:00Z",
        channelTitle=f"Channel {i}",
    )


def _override_with(fake: object) -> None:
    app.dependency_overrides[get_search_service] = lambda: fake


def test_search_returns_envelope() -> None:
    _override_with(FakeService([_sample_video(i) for i in range(5)]))
    client = TestClient(app)
    response = client.post("/api/search", json={"keyword": "react"})
    assert response.status_code == 200
    body: dict[str, Any] = response.json()
    assert body["ok"] is True
    assert len(body["data"]["videos"]) == 5
    first = body["data"]["videos"][0]
    assert first["videoId"] == "vid0"
    assert "publishedAt" in first


def test_keyword_too_short_returns_422() -> None:
    client = TestClient(app)
    response = client.post("/api/search", json={"keyword": "x"})
    assert response.status_code == 422


def test_empty_result_returns_200_with_empty_list() -> None:
    """No-results is not an error — it's a normal 200 with data.videos=[]."""
    _override_with(FakeService([]))
    client = TestClient(app)
    response = client.post("/api/search", json={"keyword": "zzzxxxyyy"})
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["data"]["videos"] == []


def test_youtube_http_error_returns_502_with_code() -> None:
    service = AsyncMock()
    request = httpx.Request("GET", "https://example")
    response = httpx.Response(503, request=request)
    service.search.side_effect = httpx.HTTPStatusError("boom", request=request, response=response)
    _override_with(service)
    client = TestClient(app)
    resp = client.post("/api/search", json={"keyword": "react"})
    assert resp.status_code == 502
    assert resp.json()["detail"]["code"] == "YOUTUBE_API_ERROR"
    assert resp.json()["detail"]["retryable"] is True


def test_youtube_unreachable_returns_502() -> None:
    service = AsyncMock()
    request = httpx.Request("GET", "https://example")
    service.search.side_effect = httpx.ConnectError("dns fail", request=request)
    _override_with(service)
    client = TestClient(app)
    resp = client.post("/api/search", json={"keyword": "react"})
    assert resp.status_code == 502
    assert resp.json()["detail"]["code"] == "YOUTUBE_API_ERROR"
