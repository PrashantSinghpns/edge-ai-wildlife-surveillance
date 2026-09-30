# Models

Model weights are intentionally **not committed** to this repository.

For local experimentation, configure a compatible YOLO model in config/config.yaml. Ultralytics can resolve standard model names such as yolov8n.pt.

For a production edge deployment:

- verify the model license and dataset rights;
- benchmark on target hardware;
- validate detection quality on the deployment domain;
- consider ONNX or TensorFlow Lite export;
- evaluate FP16 or INT8 quantization only after accuracy validation;
- store model artifacts in a versioned artifact registry rather than Git.

No employer-owned model weights or private datasets are included here.
