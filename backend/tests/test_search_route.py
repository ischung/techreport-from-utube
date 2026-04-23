from __future__ import annotations

from typing import Any

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
def reset_overrides() -> None:
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


def _override_with(fake: FakeService) -> None:
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


def test_empty_result_returns_404_with_no_results_code() -> None:
    _override_with(FakeService([]))
    client = TestClient(app)
    response = client.post("/api/search", json={"keyword": "zzzxxxyyy"})
    assert response.status_code == 404
    body = response.json()
    assert body["detail"]["code"] == "NO_RESULTS"
