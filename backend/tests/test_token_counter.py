from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.observability.token_counter import TokenCounter, get_token_counter


def test_record_accumulates_across_calls() -> None:
    counter = TokenCounter()
    counter.record(input_tokens=100, output_tokens=50)
    counter.record(input_tokens=200, output_tokens=150, cache_read_tokens=80)

    snap = counter.snapshot()
    assert snap.input_tokens == 300
    assert snap.output_tokens == 200
    assert snap.cache_read_tokens == 80


def test_cost_calculation_matches_public_pricing() -> None:
    counter = TokenCounter()
    # 1M input + 1M output + 1M cache-read = $3 + $15 + $0.30 = $18.30
    counter.record(input_tokens=1_000_000, output_tokens=1_000_000, cache_read_tokens=1_000_000)
    cost = counter.snapshot().estimated_cost_usd()
    assert cost == 18.30


def test_reset_zeroes_the_counter() -> None:
    counter = TokenCounter()
    counter.record(input_tokens=100, output_tokens=50)
    counter.reset()
    snap = counter.snapshot()
    assert snap.input_tokens == 0
    assert snap.output_tokens == 0
    assert snap.estimated_cost_usd() == 0.0


def test_negative_inputs_are_clamped_to_zero() -> None:
    counter = TokenCounter()
    counter.record(input_tokens=-10, output_tokens=-5)
    snap = counter.snapshot()
    assert snap.input_tokens == 0
    assert snap.output_tokens == 0


def test_health_endpoint_exposes_counter_snapshot() -> None:
    counter = TokenCounter()
    counter.record(input_tokens=1500, output_tokens=600)
    app.dependency_overrides[get_token_counter] = lambda: counter
    try:
        client = TestClient(app)
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["tokensInput"] == 1500
        assert data["tokensOutput"] == 600
        assert data["estimatedCostUsd"] > 0
    finally:
        app.dependency_overrides.pop(get_token_counter, None)
