import importlib
import signal
import sys
from unittest.mock import Mock
import pytest
from edge_ai_surveillance.camera import CameraSource

def test_failed_camera_open_releases_handle_and_redacts_source(monkeypatch):
    cv2 = Mock()
    capture = cv2.VideoCapture.return_value
    capture.isOpened.return_value = False
    monkeypatch.setitem(sys.modules, "cv2", cv2)
    with pytest.raises(RuntimeError) as error:
        CameraSource("rtsp://secret:password@camera/stream")
    capture.release.assert_called_once()
    assert "password" not in str(error.value)

def test_mqtt_startup_failure_runs_both_cleanup_paths(monkeypatch):
    pytest.importorskip("paho.mqtt.client")
    pytest.importorskip("psutil")
    from edge_ai_surveillance.pipeline import EdgePipeline
    pipeline = EdgePipeline.__new__(EdgePipeline)
    pipeline.device_id = "test-camera"
    pipeline.camera = Mock()
    pipeline.mqtt = Mock()
    pipeline.mqtt.connect.side_effect = RuntimeError("broker unavailable")
    monkeypatch.setattr(signal, "signal", lambda *args: None)
    with pytest.raises(RuntimeError):
        pipeline.run()
    pipeline.camera.close.assert_called_once()
    pipeline.mqtt.close.assert_called_once()
