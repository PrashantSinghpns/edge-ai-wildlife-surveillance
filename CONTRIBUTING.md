# Contributing

This is a portfolio and reference implementation. Contributions that improve code quality, tests, documentation, portability or observability are welcome.

## Development setup

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

Run tests:

    pytest

## Contribution rules

- do not submit employer or customer proprietary code;
- do not commit credentials, private URLs or deployment coordinates;
- do not add model weights or datasets unless redistribution rights are clear;
- keep hardware-specific behavior behind explicit interfaces;
- add tests for deterministic logic;
- document protocol/schema changes.

Use focused commits and explain the engineering reason for each change.
