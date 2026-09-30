from __future__ import annotations

import logging
import time
from typing import Any

LOGGER = logging.getLogger(__name__)


def normalize_source(source: Any) -> int | str:
    if isinstance(source, int):
        return source
    text = str(source)
    return int(text) if text.isdigit() else text


class CameraSource:
    """OpenCV capture wrapper with basic reconnect support."""

    def __init__(
        self,
        source: int | str,
        width: int | None = None,
        height: int | None = None,
        reconnect_seconds: float = 2.0,
    ) -> None:
        import cv2

        self.cv2 = cv2
        self.source = normalize_source(source)
        self.width = width
        self.height = height
        self.reconnect_seconds = reconnect_seconds
        self.capture = None
        self._open()

    def _open(self) -> None:
        if self.capture is not None:
            self.capture.release()

        self.capture = self.cv2.VideoCapture(self.source)
        if self.width:
            self.capture.set(self.cv2.CAP_PROP_FRAME_WIDTH, self.width)
        if self.height:
            self.capture.set(self.cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        if not self.capture.isOpened():
            raise RuntimeError(f"Unable to open camera source: {self.source}")

    def read(self):
        ok, frame = self.capture.read()
        if ok:
            return frame

        LOGGER.warning("Camera read failed; attempting reconnect")
        time.sleep(self.reconnect_seconds)
        self._open()
        ok, frame = self.capture.read()
        if not ok:
            raise RuntimeError("Camera read failed after reconnect")
        return frame

    def close(self) -> None:
        if self.capture is not None:
            self.capture.release()
