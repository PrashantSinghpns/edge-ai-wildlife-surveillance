from __future__ import annotations

import time
import math
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
        if not math.isfinite(self.min_confidence) or not 0 <= self.min_confidence <= 1:
            raise ValueError("min_confidence must be finite and between 0 and 1")
        if not math.isfinite(self.cooldown_seconds) or self.cooldown_seconds < 0:
            raise ValueError("cooldown_seconds must be finite and nonnegative")
        self._last_emit: dict[str, float] = defaultdict(lambda: float("-inf"))

    def should_emit(
        self,
        label: str,
        confidence: float,
        now: float | None = None,
    ) -> bool:
        if not math.isfinite(confidence) or not 0 <= confidence <= 1:
            return False
        if self.labels and label not in self.labels:
            return False
        if confidence < self.min_confidence:
            return False

        timestamp = time.monotonic() if now is None else now
        if timestamp - self._last_emit[label] < self.cooldown_seconds:
            return False

        self._last_emit[label] = timestamp
        return True
