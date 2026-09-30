from __future__ import annotations

import os
import socket
from datetime import datetime, timezone

import psutil


def _temperature_c() -> float | None:
    try:
        temperatures = psutil.sensors_temperatures()
    except (AttributeError, OSError):
        return None

    for entries in temperatures.values():
        if entries:
            return float(entries[0].current)
    return None


def collect_health(device_id: str) -> dict:
    memory = psutil.virtual_memory()
    return {
        "device_id": device_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "pid": os.getpid(),
        "cpu_percent": psutil.cpu_percent(interval=None),
        "memory_percent": memory.percent,
        "temperature_c": _temperature_c(),
    }
