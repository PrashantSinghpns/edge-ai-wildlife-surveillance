# Architecture

## Design goals

The architecture separates computer vision, device I/O, event policy and transport so each component can be tested or replaced independently.

Primary goals:

- low-latency local inference;
- graceful operation during intermittent connectivity;
- clear boundaries between AI, networking and MCU responsibilities;
- configuration-driven deployment;
- small and explainable modules;
- observability for field debugging.

## Data flow

1. Camera frames are captured by the Linux edge device.
2. OpenCV handles frame acquisition and pre-processing.
3. YOLO inference returns class labels, confidence values and bounding boxes.
4. EventPolicy applies class filtering, confidence thresholds and cooldown.
5. Accepted detections become normalized DetectionEvent objects.
6. Events are published over MQTT and recorded locally if desired.
7. Device health is published on a separate topic.
8. ESP32/STM32 nodes can exchange sensor data and commands over UART, SPI, I2C or Modbus RS-485.
9. RTSP is treated as the video transport layer and remains separate from event telemetry.

## Component boundaries

### CameraSource
Owns camera/video input and reconnect behavior.

### YoloDetector
Wraps model-specific inference and converts framework output into a stable internal representation.

### EventPolicy
Prevents downstream systems from being flooded by low-confidence or repeated detections.

### DetectionEvent
Defines the transport-neutral event schema.

### MqttPublisher
Owns broker connectivity, topics, QoS and online/offline status.

### SerialGateway
Provides a simple newline-delimited JSON interface for a companion MCU.

### Health telemetry
Reports host CPU, memory and temperature signals without coupling them to model inference.

## Failure domains

A production implementation should isolate and recover from:

- camera disconnects;
- RTSP timeout or authentication failure;
- inference exceptions;
- MQTT broker loss;
- serial framing errors;
- invalid configuration;
- low storage;
- thermal throttling;
- abrupt power loss.

The public reference implementation includes basic camera and MQTT recovery patterns while keeping deployment-specific policies out of the repository.

## Deployment topology

Typical topology:

    Camera -> Raspberry Pi / Linux Edge Computer -> MQTT Broker -> Monitoring Service
                                      |
                                      +-> ESP32 / STM32 -> Sensors / Relays
                                      |
                                      +-> RTSP video path

The MQTT broker may be local, site-level or remote depending on connectivity and security requirements.
