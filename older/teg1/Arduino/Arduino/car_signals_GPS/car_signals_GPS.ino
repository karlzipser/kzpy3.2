#include "constants.h"

///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
//
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(5);
  GPS_setup();
  LED_setup();
}

void loop() {
  GPS_loop();
  LED_loop();
}
//
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////

#include <Wire.h>
#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"

Adafruit_BicolorMatrix matrix = Adafruit_BicolorMatrix();

const int led_LEFT =  2;
const int led_RIGHT = 11;
const int led_DATA =  3;
const int led_STATE_1 = 8;
const int led_STATE_2 = 9;
const int led_STATE_3 = 10;
const int led_STATE_4 = 12;
/*
const int button_A =  5;
const int button_B =  6;
const int button_C =  7;
const int button_D =  4;

int button_A_state = LOW;
int button_B_state = LOW;
int button_C_state = LOW;
int button_D_state = LOW;
*/

static const uint8_t PROGMEM
  left_bmp[] =
  { B10000000,
    B10000000,
    B10000000,
    B10000000,
    B10000000,
    B10000000,
    B10000000,
    B10000000 },
  right_bmp[] =
  { B00000001,
    B00000001,
    B00000001,
    B00000001,
    B00000001,
    B00000001,
    B00000001,
    B00000001 },  
  one_bmp[] =
  { B00000000,
    B00011000,
    B00111000,
    B00011000,
    B00011000,
    B00011000,
    B00111100,
    B00000000 },
   two_bmp[] =
  { B00000000,
    B00011110,
    B00110110,
    B01101100,
    B00011000,
    B00111110,
    B01111110,
    B00000000 },
    three_bmp[] =
  { B00000000,
    B00111100,
    B01100110,
    B00011100,
    B00001110,
    B01100110,
    B00111100,
    B00000000 },
    four_bmp[] =
  { B00000000,
    B00001110,
    B00011110,
    B00110110,
    B01111110,
    B00000110,
    B00000110,
    B00000000 },
  saving_data_bmp[] =
  { B00000000,
    B00000000,
    B00000000,
    B00000000,
    B00000000,
    B00000000,
    B00000000,
    B01111110 };

void left_turn() {
  matrix.drawBitmap(0, 0, left_bmp, 8, 8, LED_RED);
  matrix.writeDisplay();
}
void right_turn() {
  matrix.drawBitmap(0, 0, right_bmp, 8, 8, LED_RED);
  matrix.writeDisplay();
}
void one() {
  //matrix.clear();
  matrix.drawBitmap(0, 0, one_bmp, 8, 8, LED_GREEN);
  matrix.writeDisplay();
  matrix.blinkRate(0);
}
void two() {
  //matrix.clear();
  matrix.drawBitmap(0, 0, two_bmp, 8, 8, LED_RED);
  matrix.writeDisplay();
  matrix.blinkRate(0);
}
void three() {
  //matrix.clear();
  matrix.drawBitmap(0, 0, three_bmp, 8, 8, LED_YELLOW);
  matrix.writeDisplay();
  matrix.blinkRate(0);
}
void four() {
  //matrix.clear();
  matrix.drawBitmap(0, 0, four_bmp, 8, 8, LED_RED);
  matrix.writeDisplay();
  matrix.blinkRate(1);

}
void save_data() {
  matrix.drawBitmap(0, 0, saving_data_bmp, 8, 8, LED_YELLOW);
  matrix.writeDisplay();
  matrix.blinkRate(1);
}

void LED_setup() {

  matrix.begin(0x70);  // pass in the address
  matrix.setRotation(3);
  matrix.blinkRate(0);
}
int sig_data = 0;
int sig_state = 0;
int sig_left_right = 0;
int a = 0;
int b = 0;
int c = 0;
int d = 0;
int e = 0;

void LED_loop() {

  int parsed_int = Serial.parseInt();

  
  int I = 0;
  
  if (parsed_int > 0) {
    I = parsed_int;
  }
/*
  button_A_state = digitalRead(button_A);
  button_B_state = digitalRead(button_B);
  button_C_state = digitalRead(button_C);
  button_D_state = digitalRead(button_D);
*/
  /*
  Serial.println(button_A_state);
  Serial.println(button_B_state);
  Serial.println(button_C_state);
  Serial.println(button_D_state);
  */
  
  if (I > 0) {
      a = I/10000;
      b = (I-a*10000)/1000;
      c = (I-a*10000-b*1000)/100;
      d = (I-a*10000-b*1000-c*100)/10;
      e = (I-a*10000-b*1000-c*100-d*10);
      sig_state = d;
      sig_data = e;
  }

  matrix.clear();
  /*
  if (button_A_state == HIGH) {
    left_turn();
    //digitalWrite(led_LEFT, HIGH);
    //Serial.println("('left_right',-1)");
  }
  else if (button_B_state == HIGH) {
    right_turn();
    //digitalWrite(led_RIGHT, HIGH);
    //Serial.println("('left_right',1)");
  }
  else {

    //Serial.println("('left_right',0)");
  }
  if (button_A_state == LOW) {
    digitalWrite(led_LEFT, LOW);
  }
  if (button_B_state == LOW) {
    digitalWrite(led_RIGHT, LOW);
  }
*/
  
  if (sig_data == 2) {
    save_data();
    //digitalWrite(led_DATA, HIGH);
  }
  else {
    //digitalWrite(led_DATA, LOW);
  }

  if (sig_state == 4) {
    four();
    /*
    digitalWrite(led_STATE_1, HIGH);
    digitalWrite(led_STATE_2, HIGH);
    digitalWrite(led_STATE_3, HIGH);
    digitalWrite(led_STATE_4, HIGH);
    */
  }
  else if (sig_state == 3) {
    three();
    /*
    digitalWrite(led_STATE_1, HIGH);
    digitalWrite(led_STATE_2, HIGH);
    digitalWrite(led_STATE_3, HIGH);
    digitalWrite(led_STATE_4, LOW);
    */
  }
  else if (sig_state > 4) {
    three();
    /*
    digitalWrite(led_STATE_1, HIGH);
    digitalWrite(led_STATE_2, HIGH);
    digitalWrite(led_STATE_3, HIGH);
    digitalWrite(led_STATE_4, LOW);
    */
  }
  else if (sig_state == 2) {
    two();
    /*
    digitalWrite(led_STATE_1, HIGH);
    digitalWrite(led_STATE_2, HIGH);
    digitalWrite(led_STATE_3, LOW);
    digitalWrite(led_STATE_4, LOW);
    */
  }
  else if (sig_state == 1) {
    one();
    /*
    digitalWrite(led_STATE_1, HIGH);
    digitalWrite(led_STATE_2, LOW);
    digitalWrite(led_STATE_3, LOW);
    digitalWrite(led_STATE_4, LOW);
    */
  }
/*
    Serial.print("(");
    Serial.print(I);
    Serial.print(",");    
    Serial.print(a);
    Serial.print(",");
    Serial.print(b);
    Serial.print(",");
    Serial.print(sig_state);
    Serial.print(",");
    Serial.print(sig_left_right);
    Serial.print(",");
     Serial.print(sig_data);
    Serial.print(button_A_state);
    Serial.print(",");
    Serial.print(button_B_state);    
    Serial.println(")");
*/   
  delay(100);
}


/*
I = 12345
a = I / 10000
b = (I - a * 10000)/1000
c = (I - a * 10000 - b * 1000)/100
d = (I - a * 10000 - b * 1000 - c * 100)/10
e = (I - a * 10000 - b * 1000 - c * 100 - d * 10)
*/


///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
///////////// GPS /////////////////////////////////////////////////////////
//    ------> http://www.adafruit.com/products/746
//Adafruit ultimage GPS
//https://learn.adafruit.com/adafruit-ultimate-gps/arduino-wiring
//VIN to +5V
//GND to Ground
//RX to digital 2
//TX to digital 3
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerial(3, 2);
Adafruit_GPS GPS(&mySerial);
#define GPSECHO  false
boolean usingInterrupt = true; // Determine whether or not to use this
void useInterrupt(boolean); // Func prototype keeps Arduino 0023 happy
void GPS_setup()  
{
  
  //Serial.begin(115200);
  //Serial.println("Adafruit GPS library basic test!");
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
  GPS.sendCommand(PGCMD_ANTENNA);
  useInterrupt(true);
  delay(1000);
//  mySerial.println(PMTK_Q_RELEASE);
  
}
SIGNAL(TIMER0_COMPA_vect) {
  char c = GPS.read();
#ifdef UDR0
  if (GPSECHO)
    if (c) UDR0 = c;  
#endif
}
void useInterrupt(boolean v) {
  if (v) {
    OCR0A = 0xAF;
    TIMSK0 |= _BV(OCIE0A);
    usingInterrupt = true;
  } else {
    TIMSK0 &= ~_BV(OCIE0A);
    usingInterrupt = false;
  }
}
uint32_t timer = millis();
void GPS_loop()                     // run over and over again
{
  if (! usingInterrupt) {
    char c = GPS.read();
    if (GPSECHO)
      if (c) Serial.print(c);
  }
  if (GPS.newNMEAreceived()) {
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }
  if (timer > millis())  timer = millis();
  if (millis() - timer > 250) { 
    timer = millis(); // reset the timer
    if (1) { //GPS.fix) {
      Serial.print("(");
      Serial.print(STATE_GPS);
      Serial.print(",");
      Serial.print(GPS.latitudeDegrees, 5);
      Serial.print(", "); 
      Serial.print(GPS.longitudeDegrees, 5);
      Serial.println(")"); 
    }
  }
}
//
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////




