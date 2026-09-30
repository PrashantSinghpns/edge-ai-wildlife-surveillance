#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate

CONFIG_PATH="${1:-config/config.yaml}"
exec edge-ai-surveillance --config "$CONFIG_PATH"
