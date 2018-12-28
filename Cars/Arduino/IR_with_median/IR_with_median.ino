//
//    based on: FILE: runningMedianTest1.ino
//  AUTHOR: Rob Tillaart
// VERSION: 0.1.00
// PURPOSE: test functionality
//    DATE: 2013-10-28
//     URL:
//
// Released to the public domain
//

// RunningMedianTest1.ino

#include <RunningMedian.h>

float IR_median[] = {0,0,0,0,0,0,0,0,0,0,0,0};
int num_sensors = 1;
int run_len = 39;
int pins[] = {A0,A1,A2,A3};
RunningMedian samples = {RunningMedian(run_len),RunningMedian(run_len)};
long unsigned int now = millis();

void setup()
{
  Serial.begin(115200);
}

void loop() 
{
    for (int i=0;i<num_sensors;i++){ //works now only if num_sensors == 1
      float raw_sample = analogRead(pins[i]);
      samples.add(raw_sample);
    }
    if (millis()-50 > now) {
      for (int i=0;i<num_sensors;i++){
        IR_median[i] = samples.getMedian();
        //Serial.print(raw_sample);Serial.print("\t");
        Serial.print(IR_median[i]);Serial.print("\t");
      }
      Serial.println("");
      now = millis();
    }
}
