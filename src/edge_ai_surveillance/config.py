from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml

_ENV_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)(?::-([^}]*))?\}")


def _expand_env(value: Any) -> Any:
    """Recursively expand environment-variable placeholders."""
    if isinstance(value, dict):
        return {key: _expand_env(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_expand_env(item) for item in value]
    if not isinstance(value, str):
        return value

    def replace(match: re.Match[str]) -> str:
        name, default = match.group(1), match.group(2)
        resolved = os.getenv(name, default)
        if resolved is None:
            raise ValueError(f"Missing required environment variable: {name}")
        return resolved

    return _ENV_PATTERN.sub(replace, value)


def load_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    data = _expand_env(data)

    required = ("device", "camera", "inference", "mqtt", "policy")
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"Missing configuration sections: {', '.join(missing)}")

    return data
