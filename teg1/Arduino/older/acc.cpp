#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>


Adafruit_MMA8451 mma = Adafruit_MMA8451();


void setup()  
{
  Serial.begin(115200);

  //Serial.println("Adafruit MMA8451 test!");
  if (! mma.begin()) {
    //Serial.println("Couldnt start");
    while (1);
  }
  //Serial.println("MMA8451 found!");
  mma.setRange(MMA8451_RANGE_2_G);
  Serial.print("Range = "); Serial.print(2 << mma.getRange());  
  Serial.println("G");
}



//////////////////////////////////////////////////////


uint32_t timer = millis();
void loop() {

 
  if (timer > millis())  timer = millis();

  if (millis() - timer > 1000) { 
    timer = millis();
  }  

  sensors_event_t event; 
  mma.getEvent(&event);
  Serial.print("(acc,");
  Serial.print(event.acceleration.x); Serial.print(",");
  Serial.print(event.acceleration.y); Serial.print(",");
  Serial.print(event.acceleration.z); Serial.print(")");
  Serial.println();
  delay(1000/100);

}