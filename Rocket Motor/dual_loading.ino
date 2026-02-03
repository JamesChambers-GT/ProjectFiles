#include <HX711_ADC.h>

// Pins:
const int HX711_dout_1 = 4;
const int HX711_sck_1  = 5;
const int HX711_dout_2 = 6;
const int HX711_sck_2  = 7;

// HX711 modules
HX711_ADC LoadCell_1(HX711_dout_1, HX711_sck_1);
HX711_ADC LoadCell_2(HX711_dout_2, HX711_sck_2);

// Timing
unsigned long t = 0;
const unsigned long interval = 50;   // ms between readings

void setup() {
  Serial.begin(57600);
  Serial.println("timestamp_ms,loadcell1,loadcell2,sum"); // CSV HEADER

  float calibrationValue_1 = 214.0;
  float calibrationValue_2 = 210.0;

  LoadCell_1.begin();
  LoadCell_2.begin();

  // Stabilize and tare automatically
  const unsigned long stabilizingtime = 2000;
  bool _tare = true;

  byte rdy1 = 0, rdy2 = 0;
  while ((rdy1 + rdy2) < 2) {
    if (!rdy1) rdy1 = LoadCell_1.startMultiple(stabilizingtime, _tare);
    if (!rdy2) rdy2 = LoadCell_2.startMultiple(stabilizingtime, _tare);
  }

  LoadCell_1.setCalFactor(calibrationValue_1);
  LoadCell_2.setCalFactor(calibrationValue_2);
}

void loop() {
  static bool newDataReady = false;

  // Update ADC modules
  if (LoadCell_1.update()) newDataReady = true;
  LoadCell_2.update();

  // Automatically output CSV forever
  if (newDataReady && millis() > t + interval) {
    unsigned long ts = millis();
    float a = LoadCell_1.getData();
    float b = LoadCell_2.getData();

    Serial.print(ts);
    Serial.print(",");
    Serial.print(a);
    Serial.print(",");
    Serial.print(b);
    Serial.print(",");
    Serial.println(a+b);
    

    newDataReady = false;
    t = millis();
  }
}
