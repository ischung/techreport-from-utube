"""Process-local running total of Claude token usage.

Deliberately minimal: no file persistence (restarts reset to zero), no
background flush, no per-request storage. The goal is "the professor can
see roughly how much the day's demo cost" on the `/api/health` response
without standing up a metrics backend.
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock

# Claude Sonnet 4.6 public pricing (2026-04)
# https://www.anthropic.com/pricing
_COST_INPUT_PER_MTOK = 3.0
_COST_OUTPUT_PER_MTOK = 15.0
_COST_CACHE_READ_PER_MTOK = 0.30  # 10% of input rate


@dataclass
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0

    def estimated_cost_usd(self) -> float:
        return round(
            (self.input_tokens / 1_000_000.0) * _COST_INPUT_PER_MTOK
            + (self.output_tokens / 1_000_000.0) * _COST_OUTPUT_PER_MTOK
            + (self.cache_read_tokens / 1_000_000.0) * _COST_CACHE_READ_PER_MTOK,
            6,
        )


class TokenCounter:
    """Thread-safe in-memory cumulative counter — singleton per process."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._usage = TokenUsage()

    def record(
        self,
        *,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cache_read_tokens: int = 0,
    ) -> None:
        with self._lock:
            self._usage.input_tokens += max(0, input_tokens)
            self._usage.output_tokens += max(0, output_tokens)
            self._usage.cache_read_tokens += max(0, cache_read_tokens)

    def snapshot(self) -> TokenUsage:
        with self._lock:
            return TokenUsage(
                input_tokens=self._usage.input_tokens,
                output_tokens=self._usage.output_tokens,
                cache_read_tokens=self._usage.cache_read_tokens,
            )

    def reset(self) -> None:
        with self._lock:
            self._usage = TokenUsage()


# Process-global singleton — instance identity matters so the same counter
# is shared between the adapter and the health route.
_counter = TokenCounter()


def get_token_counter() -> TokenCounter:
    return _counter
