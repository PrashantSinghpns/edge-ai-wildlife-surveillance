from __future__ import annotations

import json
import logging
import ssl
from typing import Any

import paho.mqtt.client as mqtt

LOGGER = logging.getLogger(__name__)


class MqttPublisher:
    """MQTT publisher with reconnect support and optional TLS."""

    def __init__(self, config: dict[str, Any], device_id: str) -> None:
        self.host = str(config.get("host", "localhost"))
        self.port = int(config.get("port", 1883))
        self.qos = int(config.get("qos", 1))
        self.device_id = device_id

        client_id = str(config.get("client_id", device_id))
        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=client_id,
            protocol=mqtt.MQTTv311,
        )

        username = config.get("username")
        password = config.get("password")
        if username:
            self.client.username_pw_set(
                str(username),
                None if password is None else str(password),
            )

        tls = config.get("tls", {})
        if tls.get("enabled", False):
            self.client.tls_set(
                ca_certs=tls.get("ca_file"),
                certfile=tls.get("cert_file"),
                keyfile=tls.get("key_file"),
                tls_version=ssl.PROTOCOL_TLS_CLIENT,
            )

        will_topic = f"edge/{device_id}/health"
        self.client.will_set(
            will_topic,
            payload=json.dumps({"device_id": device_id, "status": "offline"}),
            qos=self.qos,
            retain=True,
        )

    def connect(self) -> None:
        LOGGER.info("Connecting to MQTT broker %s:%s", self.host, self.port)
        self.client.connect(self.host, self.port, keepalive=60)
        self.client.loop_start()
        self.publish_health(
            {"device_id": self.device_id, "status": "online"},
            retain=True,
        )

    def publish_event(self, payload: str) -> None:
        topic = f"edge/{self.device_id}/events"
        info = self.client.publish(
            topic,
            payload=payload,
            qos=self.qos,
            retain=False,
        )
        info.wait_for_publish(timeout=5)

    def publish_health(self, payload: dict[str, Any], retain: bool = False) -> None:
        topic = f"edge/{self.device_id}/health"
        self.client.publish(
            topic,
            json.dumps(payload),
            qos=self.qos,
            retain=retain,
        )

    def close(self) -> None:
        try:
            self.publish_health(
                {"device_id": self.device_id, "status": "offline"},
                retain=True,
            )
        finally:
            self.client.loop_stop()
            self.client.disconnect()
