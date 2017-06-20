//////////////////////////////////////////////////////////////////////
// PINS: 7
// Baud: ---
// http://playground.arduino.cc/Main/MaxSonar
//Author: Bruce Allen
//Digital pin 7 for reading in the pulse width from the MaxSonar device.
//This variable is a constant because the pin will not change throughout execution of this code.
const int pwPin = 7;
long pulse, inches, cm;
void sonar_setup()
{
  //This opens up a serial connection to shoot the results back to the PC console
  //Serial.begin(9600);
  ;
}
void sonar_loop()
{
  pinMode(pwPin, INPUT);
  pulse = pulseIn(pwPin, HIGH);
  inches = pulse / 147;
  cm = inches * 2.54;
  Serial.print(inches);
  Serial.print("in, ");
  Serial.print(cm);
  Serial.print("cm");
  Serial.println();
  delay(500);
}
//////////////////////////////////////////////////////////////////////

