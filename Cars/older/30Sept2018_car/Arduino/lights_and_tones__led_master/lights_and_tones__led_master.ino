/////////////////////// LIGHTS ///////////////////////////////
//

int LEFT_YELLOW = 9;
int RIGHT_YELLOW = 12;
int BLUE = 5;
int WHITE = 7;
int PURPLE = 4;
int GREEN = 6;
int LEFT_RED = 11;
int RIGHT_RED = 10;
int LEFT_GREEN = 13;
int RIGHT_GREEN = 8;
int ZED = WHITE;
int LIDAR = GREEN;
int BAG = BLUE;
//
//////////////////////////////////////////////////////
int button;
int lights_out = 0;
int mute = 0;
int human_driver = 1;
int AA;

const int buttonPin = 2;
const int buttonLED = A0;
long unsigned int button_press_time = millis();
long unsigned int button_press_time_prev = 0;

#include <Wire.h>


void begin_serial()
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
}

void setup()
{
    Wire.begin(); // join i2c bus (address optional for master)
    for (int i=4; i<14;++i){
      pinMode(i, OUTPUT);digitalWrite(i, LOW);
    }
    pinMode(buttonPin,INPUT);
    pinMode(buttonLED,OUTPUT);
    begin_serial();
    Serial.println("Master setup()");    
}


int toggle(int t) {
  if (t==0) t=1;
  else t = 0;
  return t;
}
int ___tic___=1;
long unsigned int ___prev_time___ = millis();
int tic_toc(int delay_time)
{
  long unsigned int now = millis();
  if (now-___prev_time___ > delay_time){
    ___prev_time___ = now;
    ___tic___ = toggle(___tic___);
  }
  return ___tic___;
}


long unsigned int __start_time__;
int __duration__;
int start_stopwatch(int t)
{
  __start_time__ = millis();
  __duration__ = t;
}
int check_stopwatch()
{
  if (millis() - __start_time__ > __duration__) return 1;
  return 0;
}


long unsigned int now_sound = millis();



void loop() {
  
  int A;


  if (millis()-now_sound > 1000) {
    now_sound = millis();
    Serial.println("('sound',0,0,0)");
  }


  A = Serial.parseInt();

  if (mute == 0) {
    Wire.beginTransmission(8); // transmit to device #8
    Wire.write(A);              // sends one byte
    Wire.endTransmission();
  }


  if (A == 21) {
    lights_out = 0;
  }
  if (lights_out==1) {
    for (int i=0; i<14;++i){
        pinMode(i, OUTPUT);digitalWrite(i, LOW);
    }
    delay(100);
    return;
  }

  if (A == 22) {
    lights_out = 1;
  }
  else if (A == 100) { // 100 means human driver
    human_driver = 1;
  }
  else if (A == 101) { // 101 means network driver
    human_driver = 0;
  }
  else if (A == 50) { // 1930 indicates new rosbag is being written to
    digitalWrite(BAG, HIGH);
    start_stopwatch(2500);
  }
  else if (A == 30) { // zed found
    digitalWrite(ZED, HIGH);
  }
  else if (A == 31) { // lidar
    digitalWrite(LIDAR, HIGH);
  }
  else if (A == 60) { // 60 indicates no zed found yet
    digitalWrite(ZED, LOW);
  }
  else if (A == 61) { // no lidar
    digitalWrite(LIDAR, LOW);
  }
  else if (A == 4) { // button 4 reached
    button = 4;
    Serial.println("A==4");
    digitalWrite(LEFT_YELLOW, LOW);
    digitalWrite(RIGHT_YELLOW, LOW);
    digitalWrite(LEFT_RED, LOW);
    digitalWrite(RIGHT_RED, LOW);
    digitalWrite(LEFT_GREEN, LOW);
    digitalWrite(RIGHT_GREEN, LOW);
    digitalWrite(PURPLE, HIGH);
  }
  else if (A == 3) { // button 3 reached
    button = 3;
  }
  else if (A == 2) { // button 2 reached
    button = 2;
    digitalWrite(LEFT_YELLOW, LOW);
    digitalWrite(RIGHT_YELLOW, LOW);
  }
  else if (A == 1) { // button 1 reached
    button = 1;
  }
  
  if (check_stopwatch()) {
    digitalWrite(BAG, LOW);
  }
  
  if (button<4) {
    digitalWrite(PURPLE, LOW);
    if (button==2) {
      if (human_driver) {
        digitalWrite(LEFT_RED, HIGH);
        digitalWrite(LEFT_GREEN, LOW);
        digitalWrite(RIGHT_RED, HIGH);
        digitalWrite(RIGHT_GREEN, LOW);
      } else {
        digitalWrite(LEFT_RED, LOW);
        digitalWrite(LEFT_GREEN, HIGH);
        digitalWrite(RIGHT_RED, LOW);
        digitalWrite(RIGHT_GREEN, HIGH);
      }
    } else {
        digitalWrite(LEFT_RED, LOW);
        digitalWrite(LEFT_GREEN, LOW);
        digitalWrite(RIGHT_RED, LOW);
        digitalWrite(RIGHT_GREEN, LOW);     
    }

    int level = tic_toc(250);

    if (button==1) {
      digitalWrite(LEFT_YELLOW, LOW);
      digitalWrite(RIGHT_YELLOW, level);
    } else if (button==3) {
      digitalWrite(LEFT_YELLOW, level);
      digitalWrite(RIGHT_YELLOW, LOW);   
    }    
  }

  if (mute==1) {
    digitalWrite(buttonLED,HIGH);
  }
  else {
    digitalWrite(buttonLED,LOW);
  }
  
  int buttonState = digitalRead(buttonPin);

  if (buttonState == HIGH){
    Serial.println("button being pressed!");
    button_press_time_prev = button_press_time;
    button_press_time = millis();
    if (button_press_time - button_press_time_prev > 500) {
      mute = toggle(mute);
    }
  }
}


void receiveEvent(int __dummy__) {
  AA = Wire.read();    // receive byte as an integer
}

//EOF
