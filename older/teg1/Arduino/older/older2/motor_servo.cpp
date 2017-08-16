#include "PinChangeInterrupt.h"
#include <Servo.h> 


#define PIN_SERVO_IN 11
#define PIN_MOTOR_IN 10
#define PIN_SERVO_OUT 9
#define PIN_MOTOR_OUT 8
#define PIN_BUTTON_IN 12

#define BUTTON_MAX 2000
#define BUTTON_MIN 500
#define SERVO_MAX 2000
#define SERVO_MIN 500
#define MOTOR_MAX 2000
#define MOTOR_MIN 500

#define STATE_LOCK 2
#define STATE_LOCK_CALIBRATE 4
#define STATE_HUMAN_FULL_CONTROL 1
#define STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR 3
#define STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR 5

volatile int servo_null_pwm_value = 1500;
volatile int servo_max_pwm_value = 1600;
volatile int servo_min_pwm_value = 1400;

volatile int motor_null_pwm_value = 1528;
volatile int motor_max_pwm_value = 1600;
volatile int motor_min_pwm_value = 1400;

volatile int button_pwm_value;
volatile int servo_pwm_value;
volatile int motor_pwm_value;



volatile long int button_prev_interrupt_time = 0;
volatile long int servo_prev_interrupt_time = 0;
volatile long int motor_prev_interrupt_time = 0;

volatile int state = STATE_LOCK;
volatile int previous_state = 0;
volatile int state_transition_time = 0;


long int caffe_last_int_read_time;
int caffe_mode;
int caffe_steer;
int caffe_motor;
int caffe_servo_pwm_value = servo_null_pwm_value;
int caffe_motor_pwm_value = motor_null_pwm_value;

int servo_percent;
int motor_percent;

Servo servo;
Servo motor; 

void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(5);

  pinMode(PIN_BUTTON_IN, INPUT_PULLUP);
  pinMode(PIN_SERVO_IN, INPUT_PULLUP);
  pinMode(PIN_MOTOR_IN, INPUT_PULLUP);

  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(PIN_BUTTON_IN),
    button_interrupt_service_routine, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(PIN_SERVO_IN),
    servo_interrupt_service_routine, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(PIN_MOTOR_IN),
    motor_interrupt_service_routine, CHANGE);

  servo.attach(PIN_SERVO_OUT); 
  motor.attach(PIN_MOTOR_OUT); 
}



void button_interrupt_service_routine(void) {
  long int m = micros();
  int dt = m-button_prev_interrupt_time;
  if (dt>BUTTON_MIN && dt<BUTTON_MAX) {
    button_pwm_value = dt;
    if (abs(button_pwm_value-1710)<50) {
      if (state != STATE_HUMAN_FULL_CONTROL) {
        previous_state = state;
        state = STATE_HUMAN_FULL_CONTROL;
        state_transition_time = m;
      }
    }
    else if (abs(button_pwm_value-1200)<50) {
      if (state != STATE_LOCK) {
        previous_state = state;
        state = STATE_LOCK;
        state_transition_time = m;
      }
    }
    else if (abs(button_pwm_value-1000)<50) {
      if (state != STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR) {
        previous_state = state;
        state = STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR;
        state_transition_time = m;
      }
    }
    else if (abs(button_pwm_value-888)<50) {
      if (state != STATE_LOCK_CALIBRATE) {
        previous_state = state;
        state = STATE_LOCK_CALIBRATE;
        state_transition_time = m;
        servo_null_pwm_value = servo_pwm_value;
        servo_max_pwm_value = servo_null_pwm_value;
        servo_min_pwm_value = servo_null_pwm_value;
        motor_null_pwm_value = motor_pwm_value;
        motor_max_pwm_value = motor_null_pwm_value;
        motor_min_pwm_value = motor_null_pwm_value;
      }
      if (servo_pwm_value > servo_max_pwm_value) {
        servo_max_pwm_value = servo_pwm_value;
      }
      if (servo_pwm_value < servo_min_pwm_value) {
        servo_min_pwm_value = servo_pwm_value;
      }
      if (motor_pwm_value > motor_max_pwm_value) {
        motor_max_pwm_value = motor_pwm_value;
      }
      if (motor_pwm_value < motor_min_pwm_value) {
        motor_min_pwm_value = motor_pwm_value;
      }
    }
  }
  button_prev_interrupt_time = m;
}



void servo_interrupt_service_routine(void) {
  long int m = micros();
  int dt = m-servo_prev_interrupt_time;
  if (dt>SERVO_MIN && dt<SERVO_MAX) {
    servo_pwm_value = dt;
    if (state == STATE_HUMAN_FULL_CONTROL) {
      servo.writeMicroseconds(servo_pwm_value);
    }
    else if (state == STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR) {
      if (abs(servo_pwm_value-servo_null_pwm_value)<=50 && (m-state_transition_time)>500*1000) {
        previous_state = state;
        state = STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR;
        state_transition_time = m;
        servo.writeMicroseconds((caffe_servo_pwm_value+servo_pwm_value)/2);
      }
      else {
        servo.writeMicroseconds(servo_pwm_value);
      }
    }
    else if (state == STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR) {
      if (abs(servo_pwm_value-servo_null_pwm_value)>50) {
        previous_state = state;
        state = STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR;
        state_transition_time = m;
        servo.writeMicroseconds(servo_pwm_value);   
      }
      else {
        servo.writeMicroseconds(caffe_servo_pwm_value);
      }
    }
    else {
      servo.writeMicroseconds(servo_null_pwm_value);
    }
  } 
  servo_prev_interrupt_time = m;
}



void motor_interrupt_service_routine(void) {
  long int m = micros();
  int dt = m-motor_prev_interrupt_time;
  if (dt>MOTOR_MIN && dt<MOTOR_MAX) {
    motor_pwm_value = dt;
    if (state == STATE_HUMAN_FULL_CONTROL) {
      motor.writeMicroseconds(motor_pwm_value);
    }
    else if (state == STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR) {
      motor.writeMicroseconds(motor_pwm_value);
    }
    else if (state == STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR) {
      motor.writeMicroseconds(motor_pwm_value);
    }
    else {
      motor.writeMicroseconds(motor_null_pwm_value);
    }
  } 
  motor_prev_interrupt_time = m;
}









void loop() {

  int caffe_int = Serial.parseInt();

  if (caffe_int > 0) {
      caffe_last_int_read_time = micros()/1000;
      caffe_mode = caffe_int/10000;
      caffe_steer = (caffe_int-caffe_mode*10000)/100;
      caffe_motor = (caffe_int-caffe_steer*100-caffe_mode*10000);
    } else if (caffe_int < 0) {
      caffe_mode = caffe_int/10000;
  }


  if (caffe_mode > 0) {
    if (caffe_steer >= 49) {
      caffe_servo_pwm_value = (caffe_steer-49)/50.0 * (servo_max_pwm_value - servo_null_pwm_value) + servo_null_pwm_value;
    }
    else {
      caffe_servo_pwm_value = (caffe_steer - 50)/50.0 * (servo_null_pwm_value - servo_min_pwm_value) + servo_null_pwm_value;
    }
    if (caffe_motor >= 49) {
      caffe_motor_pwm_value = (caffe_motor-49)/50.0 * (motor_max_pwm_value - motor_null_pwm_value) + motor_null_pwm_value;
    }
    else {
      caffe_motor_pwm_value = (caffe_motor - 50)/50.0 * (motor_null_pwm_value - motor_min_pwm_value) + motor_null_pwm_value;
    }
  }




  if (servo_pwm_value >= servo_null_pwm_value) {
    servo_percent = 49+50.0*(servo_pwm_value-servo_null_pwm_value)/(servo_max_pwm_value-servo_null_pwm_value);
  }
  else {
    servo_percent = 49 - 49.0*(servo_null_pwm_value-servo_pwm_value)/(servo_null_pwm_value-servo_min_pwm_value);
  }

  if (motor_pwm_value >= motor_null_pwm_value) {
    motor_percent = 49+50.0*(motor_pwm_value-motor_null_pwm_value)/(motor_max_pwm_value-motor_null_pwm_value);
  }
  else {
    motor_percent = 49 - 49.0*(motor_null_pwm_value-motor_pwm_value)/(motor_null_pwm_value-motor_min_pwm_value);
  }


  if (false) {
    Serial.print("(");
    Serial.print(state);
    Serial.print(",");
    Serial.print(button_pwm_value);
    Serial.print(",");
    Serial.print(servo_pwm_value);
    Serial.print(",[");
    Serial.print(servo_min_pwm_value);
    Serial.print(",");
    Serial.print(servo_null_pwm_value);
    Serial.print(",");
    Serial.print(servo_max_pwm_value);  
    Serial.print("],[");
    Serial.print(motor_min_pwm_value);
    Serial.print(",");
    Serial.print(motor_null_pwm_value);
    Serial.print(",");
    Serial.print(motor_max_pwm_value);
    Serial.print("],");
    Serial.print(caffe_mode);
    Serial.print(",");
    Serial.print(caffe_steer);
    Serial.print(",");
    Serial.print(caffe_motor);
    Serial.print(",");
    Serial.print(caffe_servo_pwm_value);
    Serial.print(",");
    Serial.print(caffe_motor_pwm_value);
    Serial.println(")");
  }
  else {
    Serial.print("(");
    Serial.print(state);
    Serial.print(",");
    Serial.print(servo_percent);
    Serial.print(",");
    Serial.print(motor_percent);
    Serial.println(")");
  }

  delay(10); // how long should this be?
}

