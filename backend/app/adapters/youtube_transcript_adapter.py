"""Adapter for ``youtube-transcript-api`` (the de-facto community library).

Runs the blocking library in a thread via ``asyncio.to_thread`` so the
FastAPI event loop isn't blocked.
"""

from __future__ import annotations

import asyncio
from typing import Any

from app.ports.transcript_port import NoTranscriptError, TranscriptPort


class YouTubeTranscriptAdapter(TranscriptPort):
    async def fetch(self, video_id: str, *, languages: tuple[str, ...] = ("ko", "en")) -> str:
        segments = await asyncio.to_thread(self._blocking_fetch, video_id, languages)
        if not segments:
            raise NoTranscriptError(f"No transcript available for video {video_id!r}")
        return "\n".join(seg["text"].strip() for seg in segments if seg.get("text"))

    @staticmethod
    def _blocking_fetch(video_id: str, languages: tuple[str, ...]) -> list[dict[str, Any]]:
        try:
            from youtube_transcript_api import (
                NoTranscriptFound,
                TranscriptsDisabled,
                YouTubeTranscriptApi,
            )
        except ImportError as exc:  # pragma: no cover - import guard
            raise NoTranscriptError("youtube-transcript-api not installed") from exc

        try:
            return YouTubeTranscriptApi.get_transcript(video_id, languages=list(languages))
        except (TranscriptsDisabled, NoTranscriptFound) as exc:
            raise NoTranscriptError(str(exc)) from exc
