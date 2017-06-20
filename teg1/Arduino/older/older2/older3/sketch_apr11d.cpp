#include "PinChangeInterrupt.h"
#include <Servo.h> 

#define pinMotorIn 10
#define pinServoIn 11
#define pinButtonIn 12
#define servoPin 9
#define motorPin 8
#define ledPin 13

int servo_max = 1888;
int servo_min = 928;

int button_max = 1710;
int button_min = 1204;

int motor_max = 2012;
int motor_min = 1220;

int top_button = 1710;
int bottom_button = 1204;

int motor_null = 1528;
int servo_null = 1376;

 
volatile int motor_pwm_value = motor_null;
volatile int servo_pwm_value = servo_null;
volatile int button_pwm_value = button_min;

volatile int motor_prev_time = 0;
volatile int servo_prev_time = 0;
volatile int button_prev_time = 0;

volatile int lock = 1;


Servo servo;  
Servo motor;  





void setup()
{
  Serial.begin(9600);
  Serial.print("setup()");
  pinMode(ledPin, OUTPUT);
  
  pinMode(pinMotorIn, INPUT_PULLUP);
  pinMode(pinServoIn, INPUT_PULLUP);
  pinMode(pinButtonIn, INPUT_PULLUP);

  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pinMotorIn), motor_interrupt, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pinServoIn), servo_interrupt, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pinButtonIn), button_interrupt, CHANGE);

  servo.attach(servoPin); 
  motor.attach(motorPin); 
}





void loop() {
  Serial.print("(");
  Serial.print(motor_pwm_value);
  Serial.print(",");
  Serial.print(servo_pwm_value);
  Serial.print(",");
  Serial.print(button_pwm_value);
  Serial.println(")");
  delay(10);
}




void motor_interrupt(void) {
  int m = micros();
  int dt = m - motor_prev_time;
  if (dt>0.8*motor_min && dt<1.2*motor_max) {
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
  if (dt>0.8*servo_min && dt<1.2*servo_max) {
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
  if (dt>0.8*button_min && dt<1.2*button_max) {
    button_pwm_value = dt;
    if (abs(button_pwm_value-bottom_button)<50) {
      lock = 1;
      motor.writeMicroseconds(motor_null);
      servo.writeMicroseconds(servo_null);
      digitalWrite(ledPin, HIGH);
    }
    if (abs(button_pwm_value-top_button)<50) {
      lock = 0;
      digitalWrite(ledPin, LOW);
    }
  } 
  button_prev_time = m;
}


