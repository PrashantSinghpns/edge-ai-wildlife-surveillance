# Validation boundaries

Unit checks cover configuration loading, JSON event serialization, confidence/geometry validation, class filtering and cooldown. Camera and broker lifecycle still require integration testing.

The default YOLO model is not a wildlife-specialized detector. Record label coverage, precision/recall, missed detections, false alerts, inference latency and temperature on the actual target device before claiming wildlife performance. Published event summaries are not a durable local event store.

Camera-open failures release the capture handle. MQTT startup failures now enter pipeline cleanup. This is bounded cleanup, not indefinite camera recovery, offline buffering, or verified message delivery.
