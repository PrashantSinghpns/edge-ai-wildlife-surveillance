# ESP32 Companion Node

This folder contains a **clean-room reference implementation** showing how an ESP32 can act as a sensor and relay companion to the Linux edge computer.

## Demonstrated concepts

- UART device communication
- Newline-delimited JSON telemetry
- Sensor acquisition
- Relay command handling
- Acknowledgement messages
- Separation of MCU responsibilities from AI inference

The example intentionally avoids production wiring, proprietary commands, real credentials and deployment-specific logic.

## Example messages

Sensor telemetry:

    {"type":"sensor","sensor":"analog_0","value":1875}

Relay command:

    {"relay":true}

Acknowledgement:

    {"type":"ack","relay":true}

For production firmware, use a real JSON parser, watchdog handling, command validation, CRC/checksums where appropriate, non-blocking I/O and a documented protocol version.
