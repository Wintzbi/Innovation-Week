#include <TFT_eSPI.h>
#include <FastLED.h>

#define MAX_BUFF_LEN  255
#define pin_avant 22
#define NUM_LEDS 144
#define DATA_PIN 27

CRGB leds[NUM_LEDS];

TFT_eSPI tft = TFT_eSPI();

void close_led() {
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();
}

void open_led(float DATA) {
  uint8_t hue = constrain(map(DATA, 0, 180, 95, 0), 0, 160);
  fill_solid(leds, NUM_LEDS, CHSV(hue, 255, 255));
  FastLED.show();
}

void setup() {
  Serial.begin(115200);
  pinMode(pin_avant, OUTPUT);
  pinMode(DATA_PIN, OUTPUT);

  tft.init();
  tft.setRotation(2);
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  digitalWrite(pin_avant, HIGH);

  tft.fillRect(5, 5, 230, 30, TFT_BLUE);
  tft.fillRect(5, 40, 230, 30, TFT_BLUE);
  tft.fillRect(5, 75, 230, 30, TFT_BLUE);
  tft.fillRect(5, 110, 230, 30, TFT_BLUE);
  tft.fillRect(5, 145, 230, 30, TFT_BLUE);
  tft.fillRect(5, 180, 230, 30, TFT_BLUE);

  tft.setTextColor(TFT_WHITE, TFT_BLUE);
  tft.drawString("Vitesse (km/h):", 10, 10, 2);
  tft.drawString("Puissance (W):", 10, 45, 2);
  tft.drawString("Calories (kj):", 10, 80, 2);
  tft.drawString("Cardiaque (bpm):", 10, 115, 2);
  tft.drawString("Distance (km):", 10, 150, 2);
  tft.drawString("Cadence (rpm):", 10, 185, 2);

  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
  close_led();
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');

    float speed = data.substring(0, data.indexOf(',')).toFloat();
    int index1 = data.indexOf(',') + 1;
    int index2 = data.indexOf(',', index1);
    float power = data.substring(index1, index2).toFloat();

    int index3 = data.indexOf(',', index2 + 1);
    float calories = data.substring(index2 + 1, index3).toFloat();

    int index4 = data.indexOf(',', index3 + 1);
    float heartrate = data.substring(index3 + 1, index4).toFloat();

    int index5 = data.indexOf(',', index4 + 1);
    float distance = data.substring(index4 + 1, index5).toFloat();

    float cadence = data.substring(index5 + 1).toFloat();

    tft.fillRect(150, 10, 80, 20, TFT_BLUE);
    tft.fillRect(150, 45, 80, 20, TFT_BLUE);
    tft.fillRect(150, 80, 80, 20, TFT_BLUE);
    tft.fillRect(150, 115, 80, 20, TFT_BLUE);
    tft.fillRect(150, 150, 80, 20, TFT_BLUE);
    tft.fillRect(150, 185, 80, 20, TFT_BLUE);

    tft.setTextColor(TFT_WHITE, TFT_BLUE);
    tft.drawString(String(round(speed * 100.0) / 100.0) + " km/h", 150, 10, 2);
    tft.drawString(String(round(power * 100.0) / 100.0) + " W", 150, 45, 2);
    tft.drawString(String(round(calories * 100.0) / 100.0) + " kj", 150, 80, 2);
    tft.drawString(String(round(heartrate * 100.0) / 100.0) + " bpm", 150, 115, 2);
    tft.drawString(String(round(distance * 100.0) / 100.0) + " km", 150, 150, 2);
    tft.drawString(String(round(cadence * 100.0) / 100.0) + " rpm", 150, 185, 2);

    if (speed > 20.0f) {
      digitalWrite(pin_avant, HIGH);
    } else {
      digitalWrite(pin_avant, LOW);
    }

    open_led(power);
  }
}
