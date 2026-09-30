# Edge Optimization

Edge AI performance should be measured on the target device. This repository intentionally avoids unverified FPS, latency or accuracy claims.

## Optimization sequence

### 1. Establish a baseline

Record:

- input resolution;
- model variant;
- CPU/GPU/NPU target;
- inference latency;
- end-to-end event latency;
- memory use;
- CPU utilization;
- device temperature.

### 2. Reduce unnecessary work

- infer only on required frames;
- crop regions of interest when the use case permits;
- avoid repeated frame copies;
- avoid encoding frames unless needed;
- decouple telemetry from the inference loop.

### 3. Select the model for the hardware

Start with a smaller model and increase capacity only when detection quality requires it.

### 4. Tune resolution

Resolution directly affects compute and memory. Validate the smallest resolution that preserves the required detection quality.

### 5. Runtime optimization

Potential deployment paths:

- native framework runtime;
- ONNX Runtime;
- TensorFlow Lite;
- hardware-specific acceleration.

Do not assume that export alone improves performance; benchmark the exact runtime on the target.

### 6. Quantization

FP16 or INT8 can reduce compute and memory use, but quantization can change model accuracy. Validate against a representative dataset before deployment.

### 7. Pipeline concurrency

Capture, inference, telemetry and logging can be decoupled using bounded queues or worker threads/processes. Bounded queues are important so overload creates controlled frame dropping rather than unbounded memory growth.

### 8. Thermal behavior

Long-running Raspberry Pi deployments should monitor temperature and CPU frequency. Thermal throttling can create latency spikes even when short benchmarks appear healthy.

## Metrics worth reporting

For a real deployment, report only measured values:

- median / p95 inference latency;
- end-to-end alert latency;
- frames processed per second;
- peak RSS memory;
- CPU utilization;
- detection precision/recall on a representative validation set;
- uptime / reconnect behavior.

No fabricated benchmark numbers are included in this portfolio repository.
