from __future__ import annotations

import json
import logging
from typing import Any

import serial

LOGGER = logging.getLogger(__name__)


class SerialGateway:
    """Line-delimited JSON bridge for an ESP32/STM32 companion controller."""

    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        timeout: float = 1.0,
    ) -> None:
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
        )

    def read_message(self) -> dict[str, Any] | None:
        raw = self.serial.readline().decode("utf-8", errors="replace").strip()
        if not raw:
            return None
        try:
            message = json.loads(raw)
            if not isinstance(message, dict):
                LOGGER.warning("Ignoring serial payload that is not a JSON object")
                return None
            return message
        except json.JSONDecodeError:
            LOGGER.warning("Ignoring malformed serial JSON payload")
            return None

    def send_command(self, command: dict[str, Any]) -> None:
        payload = json.dumps(command, separators=(",", ":")) + "\n"
        self.serial.write(payload.encode("utf-8"))

    def close(self) -> None:
        self.serial.close()
