"""Search orchestration + in-memory LRU cache.

Keeps the YouTube API budget low by caching the most-recent queries for five
minutes. A plain dict protected by ``asyncio.Lock`` is enough at this scale;
we can swap in ``cachetools.TTLCache`` later if contention becomes a thing.
"""

from __future__ import annotations

import asyncio
import time
from collections import OrderedDict

from app.ports.youtube_search_port import YouTubeSearchPort
from app.schemas import VideoSearchResult

_DEFAULT_TTL_SECONDS = 300.0
_DEFAULT_CAPACITY = 64


class SearchService:
    def __init__(
        self,
        port: YouTubeSearchPort,
        *,
        ttl_seconds: float = _DEFAULT_TTL_SECONDS,
        capacity: int = _DEFAULT_CAPACITY,
    ) -> None:
        self._port = port
        self._ttl = ttl_seconds
        self._capacity = capacity
        self._cache: OrderedDict[str, tuple[float, list[VideoSearchResult]]] = OrderedDict()
        self._lock = asyncio.Lock()

    async def search(self, keyword: str) -> list[VideoSearchResult]:
        key = keyword.strip().lower()
        now = time.monotonic()

        async with self._lock:
            entry = self._cache.get(key)
            if entry is not None:
                expires_at, cached = entry
                if expires_at > now:
                    self._cache.move_to_end(key)
                    return cached
                del self._cache[key]

        results = await self._port.search_recent(keyword)

        async with self._lock:
            self._cache[key] = (now + self._ttl, results)
            self._cache.move_to_end(key)
            while len(self._cache) > self._capacity:
                self._cache.popitem(last=False)

        return results
