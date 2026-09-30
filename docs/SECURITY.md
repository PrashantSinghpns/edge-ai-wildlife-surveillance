# Security

This repository is a portfolio implementation, not a hardened production appliance. The following controls should be considered before real deployment.

## Secrets

Do not commit:

- MQTT passwords;
- RTSP credentials;
- private keys;
- certificates;
- Wi-Fi credentials;
- private IP inventories;
- deployment coordinates.

Use a secrets manager, protected environment file, provisioning system or OS credential store.

## Network security

- use MQTT over TLS;
- restrict broker ACLs by device and topic;
- firewall unused inbound ports;
- segment camera/IoT networks from management networks;
- disable password-based SSH where practical;
- avoid exposing RTSP directly to the public internet;
- rotate credentials.

## Application permissions

Run the service as a dedicated non-root account and grant only the groups/capabilities required for camera and serial access.

## Supply chain

- pin and review dependencies for production;
- monitor CVEs;
- verify model and dataset licensing;
- verify downloaded model checksums;
- protect the update channel.

## Device identity

For fleet deployments, prefer unique device identity and per-device credentials instead of a shared global password.

## Logging

Logs should never contain raw passwords, tokens or private keys. Consider whether image/event metadata is sensitive before storing or exporting it.

## Reporting vulnerabilities

For issues in this public portfolio repository, open a GitHub issue only when the report contains no secret or exploitable private deployment detail. Sensitive production vulnerabilities should be handled through a private disclosure channel.
