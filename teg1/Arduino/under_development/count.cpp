#include "PinChangeInterrupt.h"
// Unfortunately this code seems to conflict with the other sensor code.
const byte ledPin = 13;
const byte interruptPin = 7;
volatile byte state = LOW;
volatile int count = 0;
volatile long int prev_blink = micros();
void setup() {
  Serial.begin(115200);

  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  //attachInterrupt(digitalPinToInterrupt(interruptPin), blink, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(interruptPin), blink, HIGH);

}

void loop() {
  digitalWrite(ledPin, state);
  delay(50);
  
  Serial.println(count);
}

void blink() {
  long int m = micros();
  if (m - prev_blink > 10) { 
    state = !state;
    count += 1;
  }
  prev_blink = m;
}



  