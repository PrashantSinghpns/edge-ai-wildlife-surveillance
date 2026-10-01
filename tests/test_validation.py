import math
import pytest
from edge_ai_surveillance.events import DetectionEvent
from edge_ai_surveillance.policy import EventPolicy

@pytest.mark.parametrize("confidence", [math.nan, math.inf, -0.1, 1.1])
def test_invalid_detector_confidence_cannot_emit(confidence):
    assert not EventPolicy().should_emit("dog", confidence)
    with pytest.raises(ValueError):
        DetectionEvent(source="camera", label="dog", confidence=confidence, bbox=[0., 0., 10., 10.])

@pytest.mark.parametrize("bbox", [[1., 1., 0., 2.], [-1., 0., 2., 2.], [0., 0., math.nan, 2.], [0., 2.]])
def test_invalid_geometry_is_rejected(bbox):
    with pytest.raises(ValueError):
        DetectionEvent(source="camera", label="dog", confidence=0.9, bbox=bbox)

def test_policy_rejects_invalid_configuration():
    with pytest.raises(ValueError):
        EventPolicy(cooldown_seconds=-1)
    with pytest.raises(ValueError):
        EventPolicy(min_confidence=math.nan)
