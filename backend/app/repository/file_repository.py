"""Writes the final Markdown report to ``REPORTS_DIR``."""

from __future__ import annotations

import asyncio
import re
import unicodedata
from datetime import UTC, datetime
from pathlib import Path


class FileRepository:
    def __init__(self, reports_dir: str | Path) -> None:
        self._dir = Path(reports_dir)

    @staticmethod
    def _slugify(value: str, *, max_length: int = 50) -> str:
        normalized = unicodedata.normalize("NFKD", value)
        ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
        cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_only).strip("-").lower()
        if not cleaned:
            cleaned = "report"
        return cleaned[:max_length]

    async def save(
        self,
        *,
        title: str,
        video_id: str,
        markdown: str,
        generated_at: datetime | None = None,
    ) -> str:
        ts = generated_at or datetime.now(tz=UTC)
        slug = self._slugify(title) or video_id
        base = f"{ts.strftime('%Y-%m-%d')}-{slug}.md"

        await asyncio.to_thread(self._dir.mkdir, parents=True, exist_ok=True)
        target = self._dir / base
        if target.exists():
            target = self._dir / f"{ts.strftime('%Y-%m-%d')}-{slug}-{video_id}.md"

        await asyncio.to_thread(target.write_text, markdown, encoding="utf-8")
        return str(target)
