#include <Arduino.h>

const int MOTOR_PIN = 19;

void setup() {
  pinMode(MOTOR_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  Serial.println("Slow");
  analogWrite(MOTOR_PIN, 80);
  delay(2000);

  Serial.println("Medium");
  analogWrite(MOTOR_PIN, 160);
  delay(2000);

  Serial.println("Full");
  analogWrite(MOTOR_PIN, 255);
  delay(2000);

  Serial.println("Off");
  analogWrite(MOTOR_PIN, 0);
  delay(2000);
}
