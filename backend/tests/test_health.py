from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_returns_expected_envelope() -> None:
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    data = body["data"]
    assert data["status"] == "up"
    assert "llmProvider" in data
    assert "version" in data
    assert isinstance(data["llmProvider"], str)
    assert isinstance(data["version"], str)


def test_health_response_time_is_fast() -> None:
    import time

    client = TestClient(app)
    start = time.perf_counter()
    response = client.get("/api/health")
    elapsed = time.perf_counter() - start
    assert response.status_code == 200
    assert elapsed < 3.0, f"/api/health took {elapsed:.3f}s (expected <3s)"
