# Edge AI Wildlife Surveillance

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%20%7C%20Linux-lightgrey)](#)
[![Edge AI](https://img.shields.io/badge/Edge%20AI-YOLOv8%20%7C%20OpenCV-success)](#)
[![IoT](https://img.shields.io/badge/IoT-MQTT%20%7C%20TCP%2FIP-orange)](#)
[![CI](https://github.com/PrashantSinghpns/edge-ai-wildlife-surveillance/actions/workflows/ci.yml/badge.svg)](https://github.com/PrashantSinghpns/edge-ai-wildlife-surveillance/actions)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-oriented **Edge AI + IoT surveillance architecture** for real-time wildlife and intrusion monitoring using **Raspberry Pi / Embedded Linux, Python, OpenCV, YOLOv8, ESP32, MQTT, RTSP, TCP/IP, UART, SPI, I2C and Modbus RS-485**.

This repository demonstrates an end-to-end engineering pipeline: **camera capture → edge inference → event filtering → telemetry → device control → remote monitoring**.

> **Portfolio reconstruction:** This repository is an independently developed technical reconstruction based on professional experience building and deploying Edge AI camera systems. It contains **no proprietary source code, customer data, credentials, model weights, deployment coordinates, or confidential intellectual property** from any employer.

---
<img width="510" height="324" alt="IMG-20260116-WA0025" src="https://github.com/user-attachments/assets/6ba409c3-d329-400d-813e-8660507726fb" /> <img width="510" height="324" alt="IMG-20260116-WA0023" src="https://github.com/user-attachments/assets/93c80daf-c79a-482b-b1bb-469a7b6a5cfd" />


## Why this project matters

Remote surveillance systems often operate with limited compute, unreliable connectivity, constrained power budgets and the need for low-latency local decisions. This project demonstrates how those constraints can be handled with a modular edge architecture that keeps inference close to the camera while using lightweight IoT protocols for telemetry and control.

### Representative use cases

- Wildlife detection near human settlements
- Restricted-area intrusion monitoring
- Forest-boundary surveillance
- Remote camera health monitoring
- Sensor-triggered event capture
- Relay / actuator control after validated events
- RTSP-based remote video access

---

## System Architecture

The current Python pipeline runs on Raspberry Pi / Linux. It accepts a local camera, video file, or RTSP camera input, then performs inference, event filtering, and MQTT publication.

```mermaid
flowchart TD
    INPUT["Local camera, video file, or RTSP input"] --> CAMERA
    CONFIG["YAML configuration"] --> CAMERA
    CONFIG --> MODEL
    CONFIG --> POLICY
    CONFIG --> MQTT

    subgraph EDGE["Raspberry Pi / Linux edge pipeline"]
        CAMERA["CameraSource: OpenCV capture and reconnect"]
        CAMERA --> STRIDE["Frame stride: select frames for inference"]
        STRIDE --> MODEL["YoloDetector: YOLOv8 inference"]
        MODEL --> POLICY["EventPolicy: labels, confidence, cooldown"]
        POLICY --> EVENT["DetectionEvent: JSON serialization"]
        EVENT --> MQTT["MqttPublisher"]
        EVENT --> LOG["Python log: label, confidence, event ID"]
        HEALTH["Periodic host health collection"] --> MQTT
    end

    MQTT --> BROKER["MQTT broker: event and health topics"]
    BROKER --> MONITOR["External monitoring subscriber"]
```

- **Implemented:** capture/reconnect, frame skipping, YOLO inference, label/confidence filtering, cooldown, JSON detection events, MQTT publication, periodic health telemetry, and Python logging.
- **Reference extension:** `serial_gateway.py` provides newline-delimited JSON over UART; ESP32 example firmware demonstrates sensor/relay handling. Neither is connected to `EdgePipeline` yet.
- **Planned extensions:** RTSP output server, command-topic handling, persistent event storage, and monitoring dashboard. RTSP camera **input** is already supported; RTSP video **output** is not implemented.
- OpenCV acquires frames; model preprocessing is handled by the Ultralytics inference call. Local logs contain event summaries rather than a persistent copy of every JSON event.

See [Architecture](docs/ARCHITECTURE.md) for component design context.

---

## Engineering Scope

| Layer | Technologies / Concepts |
|---|---|
| **Edge Compute** | Raspberry Pi, Embedded Linux, Python |
| **Computer Vision** | OpenCV, YOLOv8, TensorFlow Lite deployment path |
| **Embedded / MCU** | ESP32, STM32, sensor interfacing, relay control |
| **Device Interfaces** | UART, SPI, I2C, Modbus RS-485 |
| **Networking** | TCP/IP, Ethernet, Wi-Fi, RTSP |
| **IoT Messaging** | MQTT, JSON telemetry |
| **Software Design** | Modular architecture, configuration management, structured logging, exception handling |
| **Reliability** | Health monitoring, reconnect logic, event cooldown, local logging |
| **Deployment** | Linux service management, field configuration, validation and troubleshooting |
| **Optimization** | Resolution tuning, frame skipping, model sizing, quantization path, memory-aware processing |

---

## Repository Structure

The paths below reflect the current repository. Runtime components live under `src/edge_ai_surveillance/`.

| Path | Responsibility |
|---|---|
| `src/edge_ai_surveillance/main.py` | CLI entry point and pipeline startup |
| `src/edge_ai_surveillance/config.py` | Configuration loading and validation |
| `src/edge_ai_surveillance/pipeline.py` | Capture, frame stride, inference, events, and health orchestration |
| `src/edge_ai_surveillance/camera.py` | OpenCV camera/video input and reconnect handling |
| `src/edge_ai_surveillance/detector.py` | Ultralytics YOLO inference adapter |
| `src/edge_ai_surveillance/policy.py` | Label filtering, confidence threshold, and cooldown |
| `src/edge_ai_surveillance/events.py` | Detection event dataclass and JSON serialization |
| `src/edge_ai_surveillance/mqtt_client.py` | MQTT event/health publication, TLS options, and Last Will |
| `src/edge_ai_surveillance/health.py` | Host health collection |
| `src/edge_ai_surveillance/serial_gateway.py` | Standalone UART JSON gateway; not wired into the pipeline |
| `src/edge_ai_surveillance/__init__.py` | Python package initialization |
| `config/config.example.yaml` | Example device, camera, inference, policy, and MQTT settings |
| `firmware/esp32/` | Sensor/relay example firmware and its README |
| `examples/` | Sample JSON event and telemetry simulation |
| `models/README.md` | Model setup guidance; weights are not included |
| `docs/` | Architecture, communication, deployment, optimization, security, and troubleshooting guides |
| `Images/` | Project photos and screenshots |
| `scripts/` | Installation and startup helpers |
| `systemd/edge-ai-surveillance.service` | Linux service template |
| `tests/` | Configuration, event serialization, and policy tests |
| `.github/workflows/ci.yml` | Continuous integration workflow |
| `.env.example`, `.gitignore` | Environment-variable reference and ignore rules |
| `pyproject.toml`, `requirements.txt` | Package metadata and dependencies |
| `CONTRIBUTING.md`, `LICENSE`, `README.md` | Contribution guidance, license, and project overview |

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/PrashantSinghpns/edge-ai-wildlife-surveillance.git
cd edge-ai-wildlife-surveillance
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure

```bash
cp config/config.example.yaml config/config.yaml
```

Update camera source, MQTT broker, detection labels and model settings in `config/config.yaml`.

### 4. Run a telemetry-only simulation

```bash
python examples/simulate_event.py
```

### 5. Run the Edge AI pipeline

```bash
python -m edge_ai_surveillance.main --config config/config.yaml
```

For an RTSP camera, set:

```yaml
camera:
  source: "rtsp://USER:PASSWORD@CAMERA_IP:554/stream"
```

Never commit real credentials. Prefer environment variables or a local untracked configuration file.

---

## Detection Event Schema

Each detection accepted by `EventPolicy` becomes one `DetectionEvent` and is serialized as a JSON object. This example matches the fields emitted by `pipeline.py`:

```json
{
  "event_id": "7f3cb870-5ad7-45e6-91e8-2f512bf2d3cf",
  "timestamp": "2026-09-30T12:00:00+00:00",
  "source": "edge-camera-01",
  "label": "dog",
  "confidence": 0.92,
  "bbox": [104.0, 88.0, 322.0, 360.0],
  "metadata": {
    "site": "demo",
    "pipeline": "yolov8",
    "frame_index": 120
  }
}
```

| Field | JSON type | Meaning |
|---|---|---|
| `event_id` | string | UUID v4 generated for the event |
| `timestamp` | string | UTC ISO 8601 event-creation time, including the timezone offset |
| `source` | string | Device identifier from `device.id` |
| `label` | string | Class name returned by the loaded model |
| `confidence` | number | Detector confidence score, normally between 0 and 1 |
| `bbox` | array of four numbers | `[x_min, y_min, x_max, y_max]` in pixels relative to the frame passed to inference |
| `metadata` | object | Context; the pipeline adds `site`, `pipeline`, and `frame_index` |

`frame_index` counts captured frames, including frames skipped by the configured inference stride. The event class defaults `metadata` to an empty object and generates `event_id` and `timestamp` when omitted. It serializes the supplied values; it does not enforce field types, confidence bounds, or bounding-box validity.

The default `yolov8n.pt` model uses its trained class names, such as `dog`; a generic `animal` label or species-specific wildlife labels require an appropriate model or an explicit mapping.

| MQTT topic | Status and payload |
|---|---|
| `edge/<device_id>/events` | Implemented: one detection JSON object per publication, configured QoS, `retain=False` |
| `edge/<device_id>/health` | Implemented: host health telemetry plus online/offline status messages and Last Will |
| `edge/<device_id>/commands` | Proposed convention; command subscription and dispatch are not implemented |

Health/status messages have a different payload from detection events. Consumers should subscribe and parse them separately.

See [Communication Design](docs/COMMUNICATION.md) and [Sample Event](examples/sample_event.json). The sample file demonstrates the base event fields; the live pipeline additionally includes `metadata.frame_index`.

---

## Edge Optimization Strategy

The repository documents a practical optimization path for resource-constrained devices:

1. Select the smallest model that satisfies the detection requirement.
2. Reduce camera resolution before inference where acceptable.
3. Decouple capture, inference and telemetry.
4. Skip frames when the application does not require inference on every frame.
5. Avoid unnecessary frame copies.
6. Apply event cooldown / deduplication to reduce network traffic.
7. Export to an optimized runtime such as TensorFlow Lite where appropriate.
8. Consider FP16 / INT8 quantization after validating accuracy.
9. Monitor CPU, memory and temperature continuously.
10. Benchmark on target hardware instead of relying on desktop measurements.

See [Edge Optimization](docs/EDGE_OPTIMIZATION.md).

---

## Hardware Integration

Representative hardware used by this class of system:

- Raspberry Pi 4 / Linux edge computer
- Arducam or compatible camera module
- ESP32 / STM32 microcontroller
- Environmental / digital sensors
- Relay modules / actuators
- PoE HAT
- SMPS / regulated power supply
- Ethernet / Wi-Fi networking

The public repository intentionally abstracts production wiring and deployment-specific hardware.

---

## Reliability & Field Engineering

A deployable edge system needs more than model inference. The architecture includes patterns for:

- Camera reconnect handling
- MQTT reconnects and Last Will messages
- Structured local logs
- Device health telemetry
- Event throttling / cooldown
- Configuration-driven behavior
- Graceful shutdown
- Linux `systemd` service execution
- Offline-friendly local event generation
- Network and serial troubleshooting

---

## Security Notes

Production deployments should use:

- MQTT over TLS
- Per-device credentials
- Certificate-based authentication where possible
- Principle of least privilege
- Firewall rules limiting exposed services
- No hard-coded secrets
- Secure remote access
- Signed / controlled firmware and application updates
- Credential rotation
- Network segmentation between camera, device and management networks

See [Security](docs/SECURITY.md).

---

## Testing

```bash
pytest -q
```

The test suite focuses on deterministic components such as configuration parsing, event serialization and policy behavior. Hardware, camera and model tests should be separated as integration tests on target devices.
<img width="310" height="324" alt="20251226_172110" src="https://github.com/user-attachments/assets/a5aa45a6-bf77-4cb3-8a1c-a5a98af67ee6" />
<img width="310" height="324" alt="20251223_134838" src="https://github.com/user-attachments/assets/0a56a198-9b8f-4cce-9f1a-0b748145c574" />

---

## Professional Experience Context

This project reflects experience across:

- Embedded software and hardware–software integration
- Raspberry Pi / Embedded Linux development
- ESP32 / STM32 device integration
- Real-time computer vision and Edge AI
- RTSP video streaming
- MQTT / TCP-IP communication
- Sensor and relay interfacing
- System debugging and validation
- Edge performance optimization
- Field deployment and troubleshooting

The goal of this repository is to present those engineering concepts in a **clean, reproducible and non-confidential portfolio implementation**.

---

## Roadmap

- [x] Modular Python edge pipeline
- [x] YOLOv8 inference adapter
- [x] MQTT event telemetry
- [x] Event policy and cooldown
- [x] Health monitoring
- [x] ESP32 reference firmware
- [x] Linux service template
- [x] Unit tests and CI
- [ ] TensorFlow Lite runtime adapter
- [ ] RTSP server integration example
- [ ] Web monitoring dashboard
- [ ] Device provisioning utility
- [ ] Persistent event store
- [ ] OTA update demonstration

---

## Author

**Prashant Singh**

- GitHub: [@PrashantSinghpns](https://github.com/PrashantSinghpns)
- LinkedIn: [Prashant Singh](https://www.linkedin.com/in/prashant-s-559a622b8)
- Email: prashantwrk82@gmail.com

---

## License

This portfolio implementation is released under the [MIT License](LICENSE).

Third-party models, datasets, hardware SDKs and libraries remain subject to their respective licenses.
