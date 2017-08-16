/*
  Copyright (c) 2014-2015 NicoHood
  See the readme for credit to other people.

  PinChangeInterrupt_TickTock
  Demonstrates how to use the library

  Connect a button/cable to pin 10/11 and ground.
  The value printed on the serial port will increase
  if pin 10 is rising and decrease if pin 11 is falling.

  PinChangeInterrupts are different than normal Interrupts.
  See readme for more information.
  Dont use Serial or delay inside interrupts!
  This library is not compatible with SoftSerial.

  The following pins are usable for PinChangeInterrupt:
  Arduino Uno/Nano/Mini: All pins are usable
  Arduino Mega: 10, 11, 12, 13, 50, 51, 52, 53, A8 (62), A9 (63), A10 (64),
               A11 (65), A12 (66), A13 (67), A14 (68), A15 (69)
  Arduino Leonardo/Micro: 8, 9, 10, 11, 14 (MISO), 15 (SCK), 16 (MOSI)
  HoodLoader2: All (broken out 1-7) pins are usable
  Attiny 24/44/84: All pins are usable
  Attiny 25/45/85: All pins are usable
  Attiny 13: All pins are usable
  ATmega644P/ATmega1284P: All pins are usable
*/

#include "PinChangeInterrupt.h"
#include <Servo.h> 
 
int servoPin = 9;
int motorPin = 8;
 
Servo servo;  
Servo motor;  
 
// choose a valid PinChangeInterrupt pin of your Arduino board
#define pinTick 10
#define pinTock 11

volatile int pwm_value = 0;
volatile int prev_time = 0;
volatile int pwm_value2 = 0;
volatile int prev_time2 = 0;

void setup()
{
  // start serial debug output
  Serial.begin(9600);
  //Serial.println(F("Startup"));

  // set pins to input with a pullup
  pinMode(pinTick, INPUT_PULLUP);
  pinMode(pinTock, INPUT_PULLUP);

  // attach the new PinChangeInterrupts and enable event functions below
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pinTick), tick, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pinTock), tock, CHANGE);

  servo.attach(servoPin); 
  motor.attach(motorPin); 
}


// See: http://forum.arduino.cc/index.php?topic=99336.0
void loop() {
  delay(10);
  Serial.print("(");
  Serial.print(pwm_value);
  Serial.print(",");
  Serial.print(pwm_value2);
  Serial.println(")");
  int steer = Serial.parseInt();
  int throttle = Serial.parseInt();
  if (steer>180) { steer = 180; }
  if (steer<0) { steer = 0; }
  servo.write(steer);
  if (throttle>180) { throttle = 180; }
  if (throttle<0) { throttle = 0; }
  motor.write(throttle);

}



void tick(void) {
  int temp = micros()-prev_time;
  if (temp<2500) {
    pwm_value = temp;
  }  
  prev_time = micros();
}



void tock(void) {
  int temp = micros()-prev_time2;
  if (temp<2500) {
    pwm_value2 = temp;
  } 
  prev_time2 = micros();
}