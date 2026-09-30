from __future__ import annotations

import time
from collections import defaultdict


class EventPolicy:
    """Confidence, class allow-list and per-label cooldown policy."""

    def __init__(
        self,
        labels: list[str] | None = None,
        min_confidence: float = 0.50,
        cooldown_seconds: float = 10.0,
    ) -> None:
        self.labels = set(labels or [])
        self.min_confidence = float(min_confidence)
        self.cooldown_seconds = float(cooldown_seconds)
        self._last_emit: dict[str, float] = defaultdict(lambda: float("-inf"))

    def should_emit(
        self,
        label: str,
        confidence: float,
        now: float | None = None,
    ) -> bool:
        if self.labels and label not in self.labels:
            return False
        if confidence < self.min_confidence:
            return False

        timestamp = time.monotonic() if now is None else now
        if timestamp - self._last_emit[label] < self.cooldown_seconds:
            return False

        self._last_emit[label] = timestamp
        return True
