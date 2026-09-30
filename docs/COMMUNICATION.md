# Communication Design

## MQTT

MQTT carries low-bandwidth structured telemetry independently of the video stream.

### Topic convention

    edge/<device_id>/events
    edge/<device_id>/health
    edge/<device_id>/commands

Example:

    edge/edge-camera-01/events

Recommended production settings:

- QoS 1 for important telemetry;
- Last Will and Testament for device-offline status;
- TLS for broker transport;
- per-device credentials;
- retained online/offline status only where appropriate;
- bounded message sizes.

## Detection event

Representative payload:

    {
      "event_id": "uuid",
      "timestamp": "ISO-8601 UTC",
      "source": "edge-camera-01",
      "label": "animal",
      "confidence": 0.92,
      "bbox": [104.0, 88.0, 322.0, 360.0],
      "metadata": {
        "site": "demo",
        "pipeline": "yolov8"
      }
    }

## RTSP

RTSP is appropriate for remote video transport while MQTT is better suited for events and device state. Keeping the two paths separate avoids coupling high-bandwidth streaming to telemetry delivery.

Possible RTSP components include:

- camera-native RTSP;
- GStreamer;
- FFmpeg;
- MediaMTX or equivalent streaming gateway.

Production credentials must never be embedded in source control.

## MCU communication

A companion ESP32/STM32 can connect to the Linux edge node using:

- UART for simple local serial links;
- SPI for high-rate board-level communication;
- I2C for peripheral-style buses;
- Modbus RS-485 for longer-distance industrial links.

The public example uses newline-delimited JSON over UART because it is easy to inspect and test. Production systems may require:

- binary framing;
- CRC;
- message sequence numbers;
- timeouts;
- retries;
- protocol versioning;
- watchdog recovery.

## TCP/IP

TCP/IP underpins MQTT, RTSP and remote management. Field debugging should verify:

1. physical link / Wi-Fi association;
2. interface address;
3. routing table and default gateway;
4. DNS if hostnames are used;
5. port reachability;
6. application protocol handshake;
7. authentication and TLS.
