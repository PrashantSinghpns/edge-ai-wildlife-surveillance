/*
 * ESP32 reference sensor/relay node for the portfolio architecture.
 *
 * This is a clean-room demonstration and is not production or employer code.
 * It exchanges newline-delimited JSON with a Linux edge computer over UART.
 */

#include <Arduino.h>

static constexpr uint32_t SERIAL_BAUD = 115200;
static constexpr int SENSOR_PIN = 34;
static constexpr int RELAY_PIN = 26;
static constexpr uint32_t TELEMETRY_INTERVAL_MS = 2000;

uint32_t lastTelemetryMs = 0;

void publishTelemetry() {
  const int raw = analogRead(SENSOR_PIN);

  Serial.print("{\"type\":\"sensor\",\"sensor\":\"analog_0\",\"value\":");
  Serial.print(raw);
  Serial.println("}");
}

void handleCommand(const String& command) {
  // Minimal demonstration parser. A production implementation should use
  // a JSON library, schema validation, timeouts and explicit error handling.
  if (command.indexOf("\"relay\":true") >= 0) {
    digitalWrite(RELAY_PIN, HIGH);
    Serial.println("{\"type\":\"ack\",\"relay\":true}");
  } else if (command.indexOf("\"relay\":false") >= 0) {
    digitalWrite(RELAY_PIN, LOW);
    Serial.println("{\"type\":\"ack\",\"relay\":false}");
  }
}

void setup() {
  Serial.begin(SERIAL_BAUD);
  pinMode(SENSOR_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  Serial.println("{\"type\":\"status\",\"state\":\"booted\"}");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command.length() > 0) {
      handleCommand(command);
    }
  }

  const uint32_t now = millis();
  if (now - lastTelemetryMs >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryMs = now;
    publishTelemetry();
  }
}
