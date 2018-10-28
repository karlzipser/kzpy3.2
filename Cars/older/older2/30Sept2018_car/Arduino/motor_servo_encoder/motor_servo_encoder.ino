
#define SERVO_MAX   4000
#define MOTOR_MAX   SERVO_MAX
#define BUTTON_MAX  SERVO_MAX
#define CAMERA_MAX  SERVO_MAX
#define SERVO_MIN   500
#define MOTOR_MIN   SERVO_MIN
#define BUTTON_MIN  SERVO_MIN
#define CAMERA_MIN  SERVO_MIN

#include "PinChangeInterrupt.h" // Adafruit library
#include <Servo.h> // Arduino library

// These come from the radio receiver via three black-red-white ribbons.
#define PIN_SERVO_IN 11
#define PIN_MOTOR_IN 10
#define PIN_BUTTON_IN 12

// These go out to ESC (motor controller) and steer servo via black-red-white ribbons.
#define PIN_SERVO_OUT 9
#define PIN_MOTOR_OUT 8
#define PIN_CAMERA_OUT 5

//#define A_PIN_SERVO_FEEDBACK 5


volatile int button_pwm = 1210;
volatile int servo_pwm = 0;
volatile int motor_pwm = 0;

int servo_command_pwm = 0;
int camera_command_pwm = 0;
int motor_command_pwm = 0;
int motor_null_pwm = 1500;
int servo_null_pwm = 1400;

volatile unsigned long int button_prev_interrupt_time = 0;
volatile unsigned long int servo_prev_interrupt_time  = 0;
volatile unsigned long int motor_prev_interrupt_time  = 0;

int max_communication_delay = 100;

long unsigned int servo_command_time;
long unsigned int motor_command_time;
long unsigned int camera_command_time;

Servo servo;
Servo motor; 
Servo camera; 

volatile float encoder_value_1 = 0.0;
volatile float encoder_value_2 = 0.0;

int servos_attached = 0;


long unsigned int start_time;

void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(5);

   for (int i = 0; i < 10; i++)
   {
     while (Serial.available() > 0)
     {
       char k = Serial.read();
       delay(1);
     }
     delay(1);
   }
   /*
  while(Serial.available() > 0) {
    char t = Serial.read();
  }
  */
  motor_servo_setup();
  encoder_setup();
  start_time = millis();
}



void motor_servo_setup()
{ 
  pinMode(PIN_BUTTON_IN, INPUT_PULLUP);
  pinMode(PIN_SERVO_IN, INPUT_PULLUP);
  pinMode(PIN_MOTOR_IN, INPUT_PULLUP);

  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(PIN_BUTTON_IN),
    button_interrupt_service_routine, CHANGE);

  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(PIN_SERVO_IN),
    servo_interrupt_service_routine, CHANGE);

  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(PIN_MOTOR_IN),
    motor_interrupt_service_routine, CHANGE);
  
  while(servo_pwm==0 || motor_pwm==0) {
    delay(200);
  }
  int N = 20;
  int servo_null_pwm__ = 0;
  int motor_null_pwm__ = 0;
  for( int i = 0; i < N; i = i + 1 ) {
    servo_null_pwm__ += servo_pwm;
    motor_null_pwm__ += motor_pwm;
    delay(15);
  }
  servo_null_pwm = servo_null_pwm__ / N;
  motor_null_pwm = motor_null_pwm__ / N;
}


void button_interrupt_service_routine(void) {
  volatile unsigned long int m = micros();
  volatile unsigned long int dt = m - button_prev_interrupt_time;
  button_prev_interrupt_time = m;
  if (dt>BUTTON_MIN && dt<BUTTON_MAX) {
    button_pwm = dt;
  } 
}


void servo_interrupt_service_routine(void) {
  volatile unsigned long int m = micros();
  volatile unsigned long int dt = m - servo_prev_interrupt_time;
  servo_prev_interrupt_time = m;
  if (dt>SERVO_MIN && dt<SERVO_MAX) {
    servo_pwm = dt;
    if(servo_command_pwm>0) {
      servo.writeMicroseconds(servo_command_pwm);
    } else if(servo_null_pwm>0) {
      servo.writeMicroseconds(servo_null_pwm);
    }
  }
  if (dt>CAMERA_MIN && dt<CAMERA_MAX) {
    if(camera_command_pwm>0) {
      camera.writeMicroseconds(camera_command_pwm);
    } else if(servo_null_pwm>0) {
      camera.writeMicroseconds(servo_null_pwm);
    }
  }
}



void motor_interrupt_service_routine(void) {
  volatile unsigned long int m = micros();
  volatile unsigned long int dt = m - motor_prev_interrupt_time;
  motor_prev_interrupt_time = m;
  if (dt>MOTOR_MIN && dt<MOTOR_MAX) {
    motor_pwm = dt;
    if(motor_command_pwm>0) {
      motor.writeMicroseconds(motor_command_pwm);
    } else if(motor_null_pwm>0) {
      motor.writeMicroseconds(motor_null_pwm);
    }
  }
}


int led_command = 0;


void loop() {

  int A;
  int num_serial_reads = 3;
  long unsigned int now;
  
  for( int i = 0; i < num_serial_reads; i = i + 1 ) {
    A = Serial.parseInt();
    //A = servo_pwm+5000;
    now = millis();
    if (A>500 && A<3000) {
      servo_command_pwm = A;
      servo_command_time = now;
    } else if (A>=5000 && A<10000) {
      camera_command_pwm = A-5000;
      camera_command_time = now;
    } else if (A>=10000 && A<30000) {
      motor_command_pwm = A-10000;
      motor_command_time = now;
    } else if (A<0) {
      led_command = -A;
    }
  }
  
  if(now-servo_command_time > max_communication_delay || now-motor_command_time > max_communication_delay || now-camera_command_time > max_communication_delay) {
    servo_command_pwm = 0;
    motor_command_pwm = 0;
    //Serial.println("AAAAA");
    if(now-servo_command_time > 4*max_communication_delay || now-motor_command_time > 4*max_communication_delay || now-camera_command_time > 4*max_communication_delay) {
      servo.detach(); 
      motor.detach(); 
      camera.detach(); 
      servos_attached = 0;
      //Serial.println("BBBBB");     
    }
  } else{
    if(servos_attached==0) {
      servo.attach(PIN_SERVO_OUT); 
      motor.attach(PIN_MOTOR_OUT); 
      camera.attach(PIN_CAMERA_OUT); 
      servos_attached = 1;
      //Serial.println("CCCCC");
    }
  }
  
  encoder_loop();

  if (millis()-start_time > 1*1000) {
    //Serial.println(millis()-start_time);
    //Serial.println(now-servo_command_time);
    //Serial.println(max_communication_delay);
    Serial.print("('mse',");
    Serial.print(button_pwm);
    Serial.print(",");
    Serial.print(servo_pwm);
    Serial.print(",");
    Serial.print(motor_pwm);
    Serial.print(",");
    Serial.print(encoder_value_1);
    //Serial.print(",");
    //Serial.print(analogRead(A_PIN_SERVO_FEEDBACK));
    Serial.println(")");
  }
  
  delay(10);
}














////////////// ENCODER //////////////////
//PIN's definition
#include "RunningAverage.h"
#define encoder0PinA  2
#define encoder0PinB  3

RunningAverage enc_avg(10);

volatile int encoder0Pos = 0;
volatile boolean PastA = 0;
volatile boolean PastB = 0;
volatile unsigned long int a = 0;
volatile unsigned long int b = 0;
volatile unsigned long int t1 = micros();
volatile unsigned long int t2 = 0;
volatile unsigned long int last_t2 = 0;
volatile unsigned long int dt = 0;


void encoder_setup() 
{
  //Serial.begin(9600);
  pinMode(encoder0PinA, INPUT);
  //turn on pullup resistor
  //digitalWrite(encoder0PinA, HIGH); //ONLY FOR SOME ENCODER(MAGNETIC)!!!! 
  pinMode(encoder0PinB, INPUT); 
  //turn on pullup resistor
  //digitalWrite(encoder0PinB, HIGH); //ONLY FOR SOME ENCODER(MAGNETIC)!!!! 
  PastA = (boolean)digitalRead(encoder0PinA); //initial value of channel A;
  PastB = (boolean)digitalRead(encoder0PinB); //and channel B

//To speed up even more, you may define manually the ISRs
// encoder A channel on interrupt 0 (arduino's pin 2)
  attachInterrupt(0, doEncoderA, CHANGE);
// encoder B channel pin on interrupt 1 (arduino's pin 3)
  attachInterrupt(1, doEncoderB, CHANGE); 

  enc_avg.clear();
}

volatile unsigned long int doEncoderAdtSum = 1;

void encoder_loop()
{  
  dt = micros()-t1;
  if (doEncoderAdtSum > 0) {
    enc_avg.addValue(1000.0*1000.0/12.0 * a / doEncoderAdtSum); //6 magnets
    encoder_value_1 = enc_avg.getAverage();
    t1 = micros();
    a = 0;
    doEncoderAdtSum = 0;
  } else if (dt > 100000) {
    enc_avg.clear();
    encoder_value_1 = 0;
    t1 = micros();
    a = 0;
    doEncoderAdtSum = 0;
  }
}

//you may easily modify the code  get quadrature..
//..but be sure this whouldn't let Arduino back! 
volatile float doEncoderAdt = 0.;
void doEncoderA()
{
  t2 = micros();
  a = a + 1;
  doEncoderAdtSum += t2 - last_t2; 
  //doEncoderAdt = float(t2 - last_t2);
  //enc_avg.addValue(62500. / doEncoderAdt);
  //encoder_value_1 = enc_avg.getAverage();
  last_t2 = t2;
}

void doEncoderB()
{
     b += 1;
}
//
///////////////////





//EOF

