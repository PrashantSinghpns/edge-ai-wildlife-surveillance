# Troubleshooting

## Camera does not open

Check:

- correct device index or RTSP URL;
- camera permissions;
- /dev/video* availability;
- network reachability;
- camera codec;
- authentication;
- whether another process already owns the device.

## RTSP stream is unstable

Investigate:

- packet loss;
- Wi-Fi signal;
- routing;
- camera bitrate;
- decoder support;
- TCP vs UDP transport behavior;
- source-side connection limits.

## MQTT does not connect

Verify:

- broker hostname/IP;
- port;
- firewall;
- TLS CA/certificate path;
- username/password;
- client ID uniqueness;
- broker ACLs.

## Events are duplicated

Increase the event cooldown or add object tracking / event correlation. The reference policy uses per-class cooldown and is intentionally simple.

## No detections

Check:

- model path;
- class allow-list;
- confidence threshold;
- input resolution;
- lighting / camera orientation;
- whether the deployed model contains the required classes.

## High CPU or temperature

Try:

- smaller model;
- lower resolution;
- larger frame stride;
- optimized runtime;
- improved cooling;
- disabling unnecessary encoding/display;
- profiling to identify the real bottleneck.

## Serial device unavailable

Check:

- correct /dev/tty* path;
- group permissions;
- baud rate;
- wiring and voltage levels;
- newline/framing assumptions;
- whether another process owns the port.

## Field debugging order

A practical order is:

1. power;
2. physical links;
3. OS device visibility;
4. IP configuration;
5. route/DNS;
6. port reachability;
7. protocol handshake;
8. application logs;
9. model/inference;
10. end-to-end event validation.

Debugging from the lowest layer upward reduces false assumptions.
