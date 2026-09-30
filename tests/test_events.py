import json

from edge_ai_surveillance.events import DetectionEvent


def test_event_serialization() -> None:
    event = DetectionEvent(
        source="edge-camera-01",
        label="animal",
        confidence=0.91,
        bbox=[1.0, 2.0, 3.0, 4.0],
        metadata={"site": "test"},
    )

    payload = json.loads(event.to_json())

    assert payload["source"] == "edge-camera-01"
    assert payload["label"] == "animal"
    assert payload["confidence"] == 0.91
    assert payload["bbox"] == [1.0, 2.0, 3.0, 4.0]
    assert payload["metadata"]["site"] == "test"
    assert payload["event_id"]
    assert payload["timestamp"]
