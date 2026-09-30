from __future__ import annotations

from edge_ai_surveillance.events import DetectionEvent


def main() -> None:
    event = DetectionEvent(
        source="edge-camera-01",
        label="animal",
        confidence=0.92,
        bbox=[104.0, 88.0, 322.0, 360.0],
        metadata={
            "site": "demo",
            "pipeline": "simulation",
        },
    )
    print(event.to_json())


if __name__ == "__main__":
    main()
