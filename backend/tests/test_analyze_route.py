from __future__ import annotations

from fastapi.testclient import TestClient

from app.deps import get_analysis_pipeline
from app.main import app
from app.ports.transcript_port import NoTranscriptError
from app.schemas import AnalysisReport, AnalyzeRequest, ReportSectionDTO


class FakePipelineOk:
    async def run(self, body: AnalyzeRequest) -> AnalysisReport:
        return AnalysisReport(
            videoId=body.video_id,
            title=body.title,
            sourceUrl=body.url,
            publishedAt=body.published_at,
            generatedAt="2026-04-24T08:00:00Z",
            llmProvider="claude",
            sections=ReportSectionDTO(
                overview="개요",
                coreConcepts=["c1", "c2"],
                detailedContent="상세",
                lectureTips="팁",
                references=[body.url],
            ),
            markdown="# hello",
            savedPath="./reports/2026-04-24-test.md",
        )


class FakePipelineNoTranscript:
    async def run(self, body: AnalyzeRequest) -> AnalysisReport:  # noqa: ARG002
        raise NoTranscriptError("no transcript")


def _override(fake: object) -> None:
    app.dependency_overrides[get_analysis_pipeline] = lambda: fake


def teardown_function() -> None:
    app.dependency_overrides.pop(get_analysis_pipeline, None)


def test_analyze_happy_path() -> None:
    _override(FakePipelineOk())
    client = TestClient(app)
    response = client.post(
        "/api/analyze",
        json={"videoId": "abc123", "title": "My Video", "url": "https://yt/x"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["data"]["videoId"] == "abc123"
    assert body["data"]["llmProvider"] == "claude"
    assert body["data"]["savedPath"].endswith(".md")


def test_analyze_missing_transcript_maps_to_422() -> None:
    _override(FakePipelineNoTranscript())
    client = TestClient(app)
    response = client.post(
        "/api/analyze",
        json={"videoId": "abc123", "title": "My Video", "url": "https://yt/x"},
    )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "NO_TRANSCRIPT"


def test_analyze_validates_payload() -> None:
    client = TestClient(app)
    response = client.post("/api/analyze", json={"videoId": "", "title": "", "url": ""})
    assert response.status_code == 422
