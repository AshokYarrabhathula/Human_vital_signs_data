#include <Arduino.h>
#include "Seeed_Arduino_mmWave.h"

// If the board is an ESP32, include the HardwareSerial library and create a
// HardwareSerial object for the mmWave serial communication
#ifdef ESP32
#  include <HardwareSerial.h>
HardwareSerial mmWaveSerial(0);
#else
// Otherwise, define mmWaveSerial as Serial1
#  define mmWaveSerial Serial1
#endif

SEEED_MR60BHA2 mmWave;

void setup() {
  Serial.begin(115200);
  mmWave.begin(&mmWaveSerial);
}

void loop() {
  float datavalue[3]={0,0,0};
  int index[3]={0,0,0};
  for(int i=0;i<10;i++){
    if (mmWave.update(100)) {
      float breath_rate;
      if (mmWave.getBreathRate(breath_rate)) {
        if(breath_rate!=0.0){
          datavalue[0]=datavalue[0]+breath_rate;
          index[0]++;
        }
      }
      float heart_rate;
      if (mmWave.getHeartRate(heart_rate)) {
        if(heart_rate!=0.0){
          datavalue[1]=datavalue[1]+heart_rate;
          index[1]++;
        }
      }
      float distance;
      if (mmWave.getDistance(distance)) {
        if(distance!=0.0){
          datavalue[2]=datavalue[2]+distance;
          index[2]++;
        }
      }
    }
    delay(200);
  }
  Serial.printf("breath rate:%.2f\n",datavalue[0]/index[0]);
  Serial.printf("heart rate:%.2f\n",datavalue[1]/index[1]);
  Serial.printf("distance:%.2f\n",datavalue[2]/index[2]);
  delay(1000);
}
