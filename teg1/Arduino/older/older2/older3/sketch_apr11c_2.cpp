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

int motor_null = 1528;
int servo_null = 1376;

int servo_max_cpu = 2000; //1888
int servo_min_cpu = 800; //928
int motor_max_cpu = 2100; //2012
int motor_min_cpu = 1100; //1220

Servo servo;  
Servo motor;  
 
// choose a valid PinChangeInterrupt pin of your Arduino board
#define pinTick 10 // motor radio in
#define pinTock 11 // steer radio in
#define pinButtonIn 12 // steer radio in



volatile int motor_pwm_value = motor_null;
volatile int motor_prev_time = 0;
volatile int servo_pwm_value = servo_null;
volatile int servo_prev_time = 0;
volatile int button_pwm_value = 1204;
volatile int button_prev_time = 0;
volatile int lock = 1;

int cpu_lock = 0;

void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(100);

  pinMode(pinTick, INPUT_PULLUP);
  pinMode(pinTock, INPUT_PULLUP);
  pinMode(pinButtonIn, INPUT_PULLUP);

  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pinTick), motor_interrupt, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pinTock), servo_interrupt, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pinButtonIn), button_interrupt, CHANGE);

  servo.attach(servoPin); 
  motor.attach(motorPin);
}

int cpu_mode = 0;
int cpu_steer = 0;
int cpu_motor = 0;

void loop() {
  lock_stop_if_signal_break();
  
  int cpu_int = Serial.parseInt();

  // here we decode three signals from single int
  if (cpu_int > 0) {
    cpu_mode = cpu_int/10000;
    cpu_steer = (cpu_int-cpu_mode*10000)/100;
    cpu_motor = (cpu_int-cpu_steer*100-cpu_mode*10000);
  } else if (cpu_int < 0) {
    cpu_mode = cpu_int/10000;
  }

  if (cpu_mode == -3) cpu_lock = 1;
  else cpu_lock = 0;



  Serial.print("(");
  Serial.print(motor_pwm_value);
  Serial.print(",");
  Serial.print(servo_pwm_value);
  Serial.print(",");
  Serial.print(button_pwm_value);
  Serial.print(", ");
  Serial.print(cpu_lock);
  Serial.print(", ");
  Serial.print(cpu_mode);
  Serial.print(",");
  Serial.print(cpu_steer);
  Serial.print(",");
  Serial.print(cpu_motor);
  Serial.println(")");
  
/*
int motor_null = 1528;
int servo_null = 1376;

int servo_max_cpu = 2000; //1888
int servo_min_cpu = 800; //928
int motor_max_cpu = 2100; //2012
int motor_min_cpu = 1100; //1220


  cpu_steer = 
*/

  delay(100);
}

void motor_interrupt(void) {
  int m = micros();
  int dt = m - motor_prev_time;
  if (dt>motor_min && dt<motor_max) {
    motor_pwm_value = dt;
    if(!lock) {
      if (!cpu_lock) {
        motor.writeMicroseconds(motor_pwm_value);
      }
    }
    if (cpu_lock) lock_stop();
  } 
  motor_prev_time = m;
}
void servo_interrupt(void) {
  int m = micros();
  int dt = m-servo_prev_time;
  if (dt>servo_min && dt<servo_max) {
    servo_pwm_value = dt;
    if (!lock) {
      if (!cpu_lock) {
        servo.writeMicroseconds(servo_pwm_value);
      }
    }
    if (cpu_lock) lock_stop();
  } 
  servo_prev_time = m;
}
void button_interrupt(void) {
  int m = micros();
  int dt = m-servo_prev_time;
  if (dt>button_min && dt<button_max) {
    button_pwm_value = dt;
    if (abs(button_pwm_value-bottom_button)<50) {
      lock_stop();
    }
    if (abs(button_pwm_value-top_button)<50) {
      lock = 0;
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
}





