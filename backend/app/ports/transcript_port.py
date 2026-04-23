"""Transcript retrieval port — plumbing for the analysis pipeline."""

from __future__ import annotations

from abc import ABC, abstractmethod


class NoTranscriptError(RuntimeError):
    """Raised when the video does not expose a transcript we can consume."""


class TranscriptPort(ABC):
    @abstractmethod
    async def fetch(self, video_id: str, *, languages: tuple[str, ...] = ("ko", "en")) -> str:
        """Return the full transcript as a single newline-joined string.

        Raises ``NoTranscriptError`` when no acceptable transcript exists.
        """
