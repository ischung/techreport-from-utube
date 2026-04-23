from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from app.repository.file_repository import FileRepository


@pytest.mark.anyio
async def test_save_creates_slugged_file(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    saved = await repo.save(
        title="LLM 에이전트 만들기: 2026년 최신 동향",
        video_id="abc123",
        markdown="# hello",
        generated_at=datetime(2026, 4, 24, tzinfo=UTC),
    )
    path = Path(saved)
    assert path.exists()
    assert path.read_text(encoding="utf-8") == "# hello"
    # slug strips non-ASCII; Korean characters drop out, ":" becomes "-"
    assert path.name.startswith("2026-04-24-")
    assert path.suffix == ".md"


@pytest.mark.anyio
async def test_save_appends_video_id_on_collision(tmp_path: Path) -> None:
    repo = FileRepository(tmp_path)
    ts = datetime(2026, 4, 24, tzinfo=UTC)
    first = await repo.save(title="Same Title", video_id="vid1", markdown="one", generated_at=ts)
    second = await repo.save(title="Same Title", video_id="vid2", markdown="two", generated_at=ts)
    assert Path(first).exists()
    assert Path(second).exists()
    assert first != second
    assert "vid2" in Path(second).name


def test_slugify_falls_back_to_report_for_empty_input() -> None:
    assert FileRepository._slugify("") == "report"
    assert FileRepository._slugify("!!!") == "report"


def test_slugify_truncates() -> None:
    slug = FileRepository._slugify("a" * 200, max_length=10)
    assert slug == "a" * 10


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
