from __future__ import annotations

import logging
import signal
import time
from typing import Any

from .camera import CameraSource
from .detector import YoloDetector
from .events import DetectionEvent
from .health import collect_health
from .mqtt_client import MqttPublisher
from .policy import EventPolicy

LOGGER = logging.getLogger(__name__)


class EdgePipeline:
    """Coordinates capture, inference, filtering, telemetry and health reporting."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.device_id = str(config["device"].get("id", "edge-camera-01"))
        self.site = str(config["device"].get("site", "demo"))

        camera_cfg = config["camera"]

        inference_cfg = config["inference"]
        self.detector = YoloDetector(
            model_path=str(inference_cfg.get("model", "yolov8n.pt")),
            confidence=float(inference_cfg.get("confidence", 0.50)),
            device=inference_cfg.get("device"),
        )
        self.frame_stride = max(1, int(inference_cfg.get("frame_stride", 1)))

        policy_cfg = config["policy"]
        self.policy = EventPolicy(
            labels=list(policy_cfg.get("labels", [])),
            min_confidence=float(policy_cfg.get("min_confidence", 0.50)),
            cooldown_seconds=float(policy_cfg.get("cooldown_seconds", 10.0)),
        )

        self.mqtt = MqttPublisher(config["mqtt"], self.device_id)
        self.health_interval = float(
            config.get("monitoring", {}).get("health_interval_seconds", 30.0)
        )
        self.camera = CameraSource(
            source=camera_cfg.get("source", 0),
            width=camera_cfg.get("width"),
            height=camera_cfg.get("height"),
            reconnect_seconds=float(camera_cfg.get("reconnect_seconds", 2.0)),
        )
        self.running = True

    def _stop(self, *_: object) -> None:
        self.running = False

    def run(self) -> None:
        signal.signal(signal.SIGINT, self._stop)
        signal.signal(signal.SIGTERM, self._stop)

        frame_index = 0
        last_health = 0.0

        LOGGER.info("Edge pipeline started for device=%s", self.device_id)

        try:
            self.mqtt.connect()
            while self.running:
                frame = self.camera.read()
                frame_index += 1

                now = time.monotonic()
                if now - last_health >= self.health_interval:
                    self.mqtt.publish_health(collect_health(self.device_id))
                    last_health = now

                if frame_index % self.frame_stride != 0:
                    continue

                for detection in self.detector.predict(frame):
                    label = detection["label"]
                    confidence = float(detection["confidence"])

                    if not self.policy.should_emit(label, confidence):
                        continue

                    event = DetectionEvent(
                        source=self.device_id,
                        label=label,
                        confidence=confidence,
                        bbox=detection["bbox"],
                        metadata={
                            "site": self.site,
                            "pipeline": "yolov8",
                            "frame_index": frame_index,
                        },
                    )
                    self.mqtt.publish_event(event.to_json())
                    LOGGER.info(
                        "event label=%s confidence=%.3f id=%s",
                        label,
                        confidence,
                        event.event_id,
                    )
        finally:
            LOGGER.info("Stopping edge pipeline")
            try:
                self.camera.close()
            finally:
                self.mqtt.close()
