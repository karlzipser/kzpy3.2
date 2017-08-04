// This sketch drives the Jetson car well, use as starting point for next step.
// There is servo jitter sound, but the car is stable and does not make unexpected moves.
// Continuing with the work of 11, 12 April

#include "PinChangeInterrupt.h"
#include <Servo.h> 

#define pin_motor_in 10 // motor radio in
#define pin_servo_in 11 // steer radio in
#define pin_button_in 12 // steer radio in
#define pin_servo_out 9
#define pin_motor_out 8

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
int servo_max_cpu = 1888; //1888
int servo_min_cpu = 928; //928
int motor_max_cpu = 2012; //2012
int motor_min_cpu = 1220; //1220

Servo servo;  
Servo motor;  
 
volatile int motor_pwm_value = motor_null;
volatile int motor_prev_time = 0;
volatile int servo_pwm_value = servo_null;
volatile int servo_prev_time = 0;
volatile int button_pwm_value = 1204;
volatile int button_prev_time = 0;
volatile int lock = 1;
volatile int control_human = 1;

int cpu_lock = 0;

void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(20); // was 100 during successful test

  pinMode(pin_motor_in, INPUT_PULLUP);
  pinMode(pin_servo_in, INPUT_PULLUP);
  pinMode(pin_button_in, INPUT_PULLUP);

  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pin_motor_in), motor_interrupt, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pin_servo_in), servo_interrupt, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(pin_button_in), button_interrupt, CHANGE);

  servo.attach(pin_servo_out); 
  motor.attach(pin_motor_out);
}

int cpu_mode = -3;
int cpu_steer = 49;
int cpu_motor = 49;
volatile int cpu_servo_pwm_value = servo_null;
volatile int cpu_motor_pwm_value = motor_null;
long int last_cpu_int_read_time = 0;

void loop() {
  lock_stop_if_signal_break();
  //Serial.print(micros()/1000 - last_cpu_int_read_time);
  if (!control_human) {
    // during cpu control, we need to test for transmission failure
    // not sure the best way to do this right now
    // this is important because cpu control is not interrupt driven
    // the question is how to recover from the lock. as written below,
    // it will require manual intervention.

    if (micros()/1000 - last_cpu_int_read_time > 100) {
      //Serial.print("micros()/1000 - last_cpu_int_read_time > 50*1000)");
      //lock_stop();
      cpu_lock = 1;
      cpu_motor_pwm_value = motor_null;
      cpu_servo_pwm_value = servo_null;
      cpu_mode = -3;
      cpu_steer = 49;
      cpu_motor = 49;
    }
  }
  int cpu_int = Serial.parseInt();
  
  // here we decode three signals from single int
  if (cpu_int > 0) {
      last_cpu_int_read_time = micros()/1000;
      cpu_mode = cpu_int/10000;
      cpu_steer = (cpu_int-cpu_mode*10000)/100;
      cpu_motor = (cpu_int-cpu_steer*100-cpu_mode*10000);
    } else if (cpu_int < 0) {
      cpu_mode = cpu_int/10000;
  }  

  if (cpu_mode == -3) cpu_lock = 1;
  else cpu_lock = 0;

  if (cpu_mode == 2) control_human = 0;
  else control_human = 1;

  if (cpu_mode > 0) {
    if (cpu_steer >= 49) cpu_servo_pwm_value = (cpu_steer-49)/50.0 * (servo_max_cpu - servo_null) + servo_null;
    else cpu_servo_pwm_value = (cpu_steer - 50)/50.0 * (servo_null - servo_min_cpu) + servo_null;
    if (cpu_motor >= 49) cpu_motor_pwm_value = (cpu_motor-49)/50.0 * (motor_max_cpu - motor_null) + motor_null;
    else cpu_motor_pwm_value = (cpu_motor - 50)/50.0 * (motor_null - motor_min_cpu) + motor_null;
  }
  if (cpu_motor_pwm_value > motor_max_cpu) cpu_lock = 1;
  if (cpu_motor_pwm_value < motor_min_cpu) cpu_lock = 1;
  if (cpu_servo_pwm_value > servo_max_cpu) cpu_lock = 1;
  if (cpu_servo_pwm_value < servo_min_cpu) cpu_lock = 1;
  

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
  Serial.print(",");
  Serial.print(cpu_servo_pwm_value);
  Serial.print(",");
  Serial.print(cpu_motor_pwm_value);
  Serial.print(",");
  Serial.print(control_human);
  Serial.println(")");

  delay(10); // how long should this be?
}

void motor_interrupt(void) {
  int m = micros();
  int dt = m - motor_prev_time;
  if (dt>motor_min && dt<motor_max) {
    motor_pwm_value = dt;
    if(!lock) {
      if (!cpu_lock) {
        if (control_human) motor.writeMicroseconds(motor_pwm_value);
        else motor.writeMicroseconds(cpu_motor_pwm_value);
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
        if (control_human) servo.writeMicroseconds(servo_pwm_value);
        else servo.writeMicroseconds(cpu_servo_pwm_value);
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
      control_human = 1;
      cpu_lock = 0;
      lock = 0;
    }
    if (abs(button_pwm_value-1000)<50) {
      lock = 0;
      control_human = 0;
    }
    if (abs(button_pwm_value-888)<50) {
      lock = 0;
      control_human = 0;
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





