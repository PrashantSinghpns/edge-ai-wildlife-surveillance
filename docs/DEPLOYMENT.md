# Deployment Guide

This guide describes a representative Linux / Raspberry Pi deployment.

## 1. Operating system

Use a supported 64-bit Linux distribution and keep packages current.

Recommended operational practices:

- dedicated non-root service user;
- read-only or restricted application permissions where possible;
- SSH key authentication;
- firewall enabled;
- time synchronization enabled.

## 2. Install

    git clone https://github.com/PrashantSinghpns/edge-ai-wildlife-surveillance.git
    cd edge-ai-wildlife-surveillance
    bash scripts/install.sh

## 3. Configure

    cp config/config.example.yaml config/config.yaml

Update:

- device ID;
- camera source;
- model path;
- confidence threshold;
- class allow-list;
- MQTT broker;
- TLS settings.

Never commit config/config.yaml if it contains credentials or private network details.

## 4. Camera validation

Before starting AI inference, verify the video source independently.

For a local camera, confirm the device appears under /dev/video*.

For RTSP, test the URL with an appropriate video client or FFmpeg/GStreamer and confirm authentication, reachability and codec support.

## 5. MQTT validation

Verify the broker separately using a local MQTT client. Confirm:

- DNS/IP reachability;
- port;
- TLS;
- authentication;
- publish permissions;
- expected topic ACLs.

## 6. Run interactively

    source .venv/bin/activate
    edge-ai-surveillance --config config/config.yaml --log-level INFO

Use interactive execution first so configuration and hardware failures are visible.

## 7. Run as a service

A systemd template is included under systemd/.

Typical production steps:

1. install the repository under /opt;
2. create a dedicated edgeai user/group;
3. grant only required camera/serial permissions;
4. copy and review the service file;
5. reload systemd;
6. enable and start the service;
7. inspect logs with journalctl.

Example:

    sudo systemctl daemon-reload
    sudo systemctl enable edge-ai-surveillance
    sudo systemctl start edge-ai-surveillance
    journalctl -u edge-ai-surveillance -f

## 8. Field validation checklist

- camera survives reconnect;
- network loss does not crash the process;
- MQTT reconnects;
- timestamps remain correct;
- device temperatures remain acceptable;
- event cooldown prevents alert storms;
- storage does not grow without bounds;
- reboot restores the service;
- power supply is stable under load;
- remote access is secured.

## PoE and power

For PoE HAT / SMPS deployments, validate voltage/current headroom and behavior during camera + CPU load. Power instability can present as camera, storage or networking failures.
