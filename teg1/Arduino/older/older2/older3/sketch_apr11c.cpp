// This sketch drives the Jetson car well, use as starting point for next step.
// There is servo jitter sound, but the car is stable and does not make unexpected moves.

#include "PinChangeInterrupt.h"
#include <Servo.h> 


int servoPin = 9;
int motorPin = 8;
int servo_max = 2000; //1888
int servo_min = 800; //928
int button_max = 2000; //1888
int button_min = 800; //928
int motor_max = 2100; //2012
int motor_min = 1100; //1220
int top_button = 1710;
int bottom_button = 1204;

Servo servo;  
Servo motor;  
 
// choose a valid PinChangeInterrupt pin of your Arduino board
#define pinTick 10 // motor radio in
#define pinTock 11 // steer radio in
#define pinButtonIn 12 // steer radio in

#define motor_null  1528
#define servo_null  1376
volatile int motor_pwm_value = motor_null;
volatile int motor_prev_time = 0;
volatile int servo_pwm_value = servo_null;
volatile int servo_prev_time = 0;
volatile int button_pwm_value = 1204;
volatile int button_prev_time = 0;
volatile int lock = 1;

void setup()
{
  Serial.begin(9600);

  pinMode(pinTick, INPUT_PULLUP);
  pinMode(pinTock, INPUT_PULLUP);
  pinMode(pinButtonIn, INPUT_PULLUP);

  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pinTick), motor_interrupt, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pinTock), servo_interrupt, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pinButtonIn), button_interrupt, CHANGE);

  servo.attach(servoPin); 
  motor.attach(motorPin); 
}

void loop() {
  delay(10);
  Serial.print("(");
  Serial.print(motor_pwm_value);
  Serial.print(",");
  Serial.print(servo_pwm_value);
  Serial.print(",");
  Serial.print(button_pwm_value);
  Serial.println(")");
}

void motor_interrupt(void) {
  int m = micros();
  int dt = m - motor_prev_time;
  if (dt>motor_min && dt<motor_max) {
    motor_pwm_value = dt;
    if(!lock) {
      motor.writeMicroseconds(motor_pwm_value);
    }
  } 
  motor_prev_time = m;
}
void servo_interrupt(void) {
  int m = micros();
  int dt = m-servo_prev_time;
  if (dt>servo_min && dt<servo_max) {
    servo_pwm_value = dt;
    if (!lock) {
      servo.writeMicroseconds(servo_pwm_value);
    }
  } 
  servo_prev_time = m;
}
void button_interrupt(void) {
  int m = micros();
  int dt = m-servo_prev_time;
  if (dt>button_min && dt<button_max) {
    button_pwm_value = dt;
    if (abs(button_pwm_value-bottom_button)<50) {
      lock = 1;
      motor.writeMicroseconds(motor_null);
      servo.writeMicroseconds(servo_null);
    }
    if (abs(button_pwm_value-top_button)<50) {
      lock = 0;
    }
    
  } 
  button_prev_time = m;
}