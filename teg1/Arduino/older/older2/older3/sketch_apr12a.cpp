// This sketch produces unstable behavior -- the car jerks and moves with no input command.

#include "PinChangeInterrupt.h"
#include <Servo.h> 

#define pin_in_rc_motor 10
#define pin_in_rc_servo 11
#define pin_in_rc_button 12

#define pin_out_servo 9
#define pin_out_motor 8
#define pin_out_led 13


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

int loop_delay = 10; // ms
 
volatile int motor_pwm_value = motor_null;
volatile int servo_pwm_value = servo_null;
volatile int button_pwm_value = button_min;

volatile int motor_prev_time = 0;
volatile int servo_prev_time = 0;
volatile int button_prev_time = 0;
volatile int human_control = 1;
volatile int lock = 1;

Servo servo;  
Servo motor;  





void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(1000);
  pinMode(pin_out_led, OUTPUT);
  
  pinMode(pin_in_rc_motor, INPUT_PULLUP);
  pinMode(pin_in_rc_servo, INPUT_PULLUP);
  pinMode(pin_in_rc_button, INPUT_PULLUP);

  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pin_in_rc_motor), motor_interrupt, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pin_in_rc_servo), servo_interrupt, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pin_in_rc_button), button_interrupt, CHANGE);

  servo.attach(pin_out_servo); 
  motor.attach(pin_out_motor);

  motor.writeMicroseconds(motor_pwm_value);
  servo.writeMicroseconds(servo_pwm_value);

}


void loop() {
  lock_stop_if_signal_break();
  Serial.print("(");
  Serial.print(lock);
  Serial.print(",");
  Serial.print(motor_pwm_value);
  Serial.print(",");
  Serial.print(servo_pwm_value);
  Serial.print(",");
  Serial.print(button_pwm_value);
  Serial.println(")");

  delay(loop_delay);
}





void motor_interrupt(void) {
  lock_stop_if_signal_break();
  int m = micros();
  int dt = m - motor_prev_time;
  if (dt>0.8*motor_min && dt<1.2*motor_max) {
    motor_pwm_value = dt;
    if (abs(motor_pwm_value - motor_null) > 200) human_control = 1;
    if(!lock) {
      motor.writeMicroseconds(motor_pwm_value);
    }
  } 
  motor_prev_time = m;
}

void servo_interrupt(void) {
  lock_stop_if_signal_break();
  int m = micros();
  int dt = m - servo_prev_time;
  if (dt>0.8*servo_min && dt<1.2*servo_max) {
    servo_pwm_value = dt;
    if (abs(servo_pwm_value - servo_null) > 200) human_control = 1;
    if (!lock) {
      servo.writeMicroseconds(servo_pwm_value);
    }
  } 
  servo_prev_time = m;
}

void button_interrupt(void) {
  lock_stop_if_signal_break();
  int m = micros();
  int dt = m - servo_prev_time;
  if (dt>0.8*button_min && dt<1.2*button_max) {
    button_pwm_value = dt;
    if (abs(button_pwm_value-bottom_button)<50) {
      lock_stop();
    }
    if (abs(button_pwm_value-top_button)<50) {
      unlock();
    }
  } 
  button_prev_time = m;
}





void lock_stop_if_signal_break(void) {
  int m = micros();
  if (m - servo_prev_time > 100000) lock_stop();
  if (m - motor_prev_time > 100000) lock_stop();
  if (m - button_prev_time > 100000) lock_stop();
}

void lock_stop(void) {
  lock = 1;
  motor.writeMicroseconds(motor_null);
  servo.writeMicroseconds(servo_null);

}

void unlock(void) {
  lock = 0;
  digitalWrite(pin_out_led, LOW);
}

