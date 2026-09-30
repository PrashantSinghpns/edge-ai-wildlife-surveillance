from __future__ import annotations

from typing import Any


class YoloDetector:
    """Thin Ultralytics YOLO adapter used by the edge pipeline."""

    def __init__(
        self,
        model_path: str = "yolov8n.pt",
        confidence: float = 0.5,
        device: str | None = None,
    ) -> None:
        from ultralytics import YOLO

        self.model = YOLO(model_path)
        self.confidence = float(confidence)
        self.device = device

    def predict(self, frame: Any) -> list[dict[str, Any]]:
        kwargs: dict[str, Any] = {
            "source": frame,
            "conf": self.confidence,
            "verbose": False,
        }
        if self.device:
            kwargs["device"] = self.device

        results = self.model.predict(**kwargs)
        detections: list[dict[str, Any]] = []

        for result in results:
            names = result.names
            for box in result.boxes:
                class_id = int(box.cls[0].item())
                confidence = float(box.conf[0].item())
                xyxy = [float(value) for value in box.xyxy[0].tolist()]
                detections.append(
                    {
                        "label": str(names[class_id]),
                        "confidence": confidence,
                        "bbox": xyxy,
                    }
                )

        return detections
