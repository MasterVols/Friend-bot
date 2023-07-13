#include <Arduino.h>

#define DIR1 6
#define STEP1 2
#define DIR2 7
#define STEP2 13

bool reversed = false;
unsigned long lastFaceDetected = 0;
float x = -1.0; // stores the last received x position, initialized to an invalid value

void setup() {
  pinMode(DIR1, OUTPUT);
  pinMode(STEP1, OUTPUT);
  pinMode(DIR2, OUTPUT);
  pinMode(STEP2, OUTPUT);
  
  Serial.begin(9600); // match the baud rate with the Raspberry Pi
}

void loop() {
  if (Serial.available()) {
    // format should be (x,y)
    String input = Serial.readStringUntil('\n');
    int commaIndex = input.indexOf(',');
    if (commaIndex != -1) {
      String xStr = input.substring(1, commaIndex); // start at index 1 to skip '('
      x = xStr.toFloat();
      lastFaceDetected = millis();
    }
  }
  
  if (millis() - lastFaceDetected < 1000) { // if a face has been detected in the last second
    if (x < 0.5) { // face is on the left side
      digitalWrite(DIR1, reversed ? HIGH : LOW);
      digitalWrite(DIR2, reversed ? LOW : HIGH);
    } else { // face is on the right side
      digitalWrite(DIR1, reversed ? LOW : HIGH);
      digitalWrite(DIR2, reversed ? HIGH : LOW);
    }
    digitalWrite(STEP1, HIGH);
    digitalWrite(STEP2, HIGH);
    delayMicroseconds(2000); // delay for stepper motor speed
    digitalWrite(STEP1, LOW);
    digitalWrite(STEP2, LOW);
    delayMicroseconds(2000);
  } else { // no face detected in the last second, stop moving
    digitalWrite(STEP1, LOW);
    digitalWrite(STEP2, LOW);

  }
}
