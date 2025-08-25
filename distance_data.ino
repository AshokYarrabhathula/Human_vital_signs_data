#include <NewPing.h>

// Define pins and maximum distance
#define TRIG_PIN  9
#define ECHO_PIN  10
#define MAX_DISTANCE 300  // in centimeters

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);

void setup() {
  Serial.begin(9600);
  delay(1000);
}

void loop() {
 // Delay between measurements

  // Read distance in centimeters
  unsigned int distance = sonar.ping_cm();

    Serial.println(distance);
  delay(1000);
}
