#include <Arduino.h>

void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 Test OK");
}

void loop() {
  delay(1000);
  Serial.println("Running...");
}