from pathlib import Path

import pytest

from edge_ai_surveillance.config import load_config


def test_load_config(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text(
        """
device:
  id: edge-01
camera:
  source: 0
inference:
  model: yolov8n.pt
mqtt:
  host: localhost
policy:
  labels: []
""".strip(),
        encoding="utf-8",
    )

    config = load_config(path)
    assert config["device"]["id"] == "edge-01"
    assert config["mqtt"]["host"] == "localhost"


def test_missing_sections_raise(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("device: {id: edge-01}", encoding="utf-8")

    with pytest.raises(ValueError):
        load_config(path)
