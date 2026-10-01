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

\`\`\`mermaid
flowchart LR
    CAM[Camera / Arducam] --> CAP[Video Capture]
    CAP --> PRE[OpenCV Pre-processing]
    PRE --> AI[YOLOv8 / Edge Inference]
    AI --> POLICY[Event Policy + Cooldown]
    POLICY --> EVENT[Structured Detection Event]

    EVENT --> MQTT[MQTT Telemetry]
    EVENT --> LOG[Local Structured Logs]
    EVENT --> CTRL[Device / Relay Control]

    MQTT --> REMOTE[Remote Monitoring]
    CAP --> RTSP[RTSP Video Stream]

    MCU[ESP32 / STM32] -->|UART / SPI / I2C / Modbus RS-485| EDGE[Raspberry Pi / Embedded Linux]
    EDGE --> CAP
    SENSORS[Sensors] --> MCU
    CTRL --> RELAY[Relay / Actuator]
\`\`\`

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

\`\`\`text
.
├── src/edge_ai_surveillance/
│   ├── camera.py
│   ├── config.py
│   ├── detector.py
│   ├── events.py
│   ├── health.py
│   ├── mqtt_client.py
│   ├── policy.py
│   ├── pipeline.py
│   └── main.py
├── firmware/esp32/
│   └── sensor_node_example.cpp
├── examples/
│   ├── sample_event.json
│   └── simulate_event.py
├── config/
│   └── config.example.yaml
├── docs/
│   ├── ARCHITECTURE.md
│   ├── COMMUNICATION.md
│   ├── DEPLOYMENT.md
│   ├── EDGE_OPTIMIZATION.md
│   ├── SECURITY.md
│   └── TROUBLESHOOTING.md
├── systemd/
│   └── edge-ai-surveillance.service
├── scripts/
│   ├── install.sh
│   └── run.sh
├── tests/
├── .github/workflows/ci.yml
├── requirements.txt
├── pyproject.toml
└── README.md
\`\`\`

---

## Quick Start

### 1. Clone

\`\`\`bash
git clone https://github.com/PrashantSinghpns/edge-ai-wildlife-surveillance.git
cd edge-ai-wildlife-surveillance
\`\`\`

### 2. Create a virtual environment

\`\`\`bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
\`\`\`

### 3. Configure

\`\`\`bash
cp config/config.example.yaml config/config.yaml
\`\`\`

Update camera source, MQTT broker, detection labels and model settings in \`config/config.yaml\`.

### 4. Run a telemetry-only simulation

\`\`\`bash
python examples/simulate_event.py
\`\`\`

### 5. Run the Edge AI pipeline

\`\`\`bash
python -m edge_ai_surveillance.main --config config/config.yaml
\`\`\`

For an RTSP camera, set:

\`\`\`yaml
camera:
  source: "rtsp://USER:PASSWORD@CAMERA_IP:554/stream"
\`\`\`

Never commit real credentials. Prefer environment variables or a local untracked configuration file.

---

## Detection Event Schema

The pipeline publishes normalized JSON events so the AI model is decoupled from downstream monitoring systems.

\`\`\`json
{
  "event_id": "7f3cb870-5ad7-45e6-91e8-2f512bf2d3cf",
  "timestamp": "2026-09-30T12:00:00+00:00",
  "source": "edge-camera-01",
  "label": "animal",
  "confidence": 0.92,
  "bbox": [104.0, 88.0, 322.0, 360.0],
  "metadata": {
    "site": "demo",
    "pipeline": "yolov8"
  }
}
\`\`\`

Default topic convention:

\`\`\`text
edge/<device_id>/events
edge/<device_id>/health
edge/<device_id>/commands
\`\`\`

See [Communication Design](docs/COMMUNICATION.md).

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
- Linux \`systemd\` service execution
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

\`\`\`bash
pytest -q
\`\`\`

The test suite focuses on deterministic components such as configuration parsing, event serialization and policy behavior. Hardware, camera and model tests should be separated as integration tests on target devices.

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
