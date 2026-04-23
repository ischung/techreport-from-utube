from __future__ import annotations

from datetime import UTC, datetime

import httpx
import pytest
import respx

from app.adapters.youtube_data_adapter import YouTubeDataAdapter


def _mock_payload(n: int) -> dict[str, object]:
    return {
        "items": [
            {
                "id": {"videoId": f"vid{i}"},
                "snippet": {
                    "title": f"Video {i}",
                    "channelTitle": f"Channel {i}",
                    "publishedAt": "2026-04-15T10:00:00Z",
                },
            }
            for i in range(n)
        ]
    }


@pytest.mark.anyio
@respx.mock
async def test_search_parses_happy_response() -> None:
    respx.get("https://www.googleapis.com/youtube/v3/search").mock(
        return_value=httpx.Response(200, json=_mock_payload(5))
    )
    adapter = YouTubeDataAdapter(api_key="dummy")
    results = await adapter.search_recent("react")
    assert len(results) == 5
    assert results[0].video_id == "vid0"
    assert results[0].url == "https://www.youtube.com/watch?v=vid0"
    assert results[0].channel_title == "Channel 0"


@pytest.mark.anyio
@respx.mock
async def test_search_caps_at_max_results() -> None:
    respx.get("https://www.googleapis.com/youtube/v3/search").mock(
        return_value=httpx.Response(200, json=_mock_payload(20))
    )
    adapter = YouTubeDataAdapter(api_key="dummy")
    results = await adapter.search_recent("react", max_results=5)
    assert len(results) == 5


def test_published_after_is_30_days_ago() -> None:
    now = datetime(2026, 4, 24, tzinfo=UTC)
    ts = YouTubeDataAdapter._published_after(now)
    assert ts.startswith("2026-03-25")


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
