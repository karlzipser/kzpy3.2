/* d *****************************************************************************

Based on:
    Flex_Sensor_Example.ino
    Example sketch for SparkFun's flex sensors
      (https://www.sparkfun.com/products/10264)
    Jim Lindblom @ SparkFun Electronics
    April 28, 2016

    Create a voltage divider circuit combining a flex sensor with a 47k resistor.
    - The resistor should connect from A0 to GND.
    - The flex sensor should connect from A0 to 3.3V
    As the resistance of the flex sensor increases (meaning it's being bent), the
    voltage at A0 should decrease.

    Development environment specifics:
    Arduino 1.6.7
******************************************************************************/


char* Flexes[]={"FL0","FL1", "FL2","FL3", "FR0","FR1", "FR2","FR3", "FC0","FC1", "FC2","FC3"};

int flex_pins[] = {A0,A1, A2,A3, A6,A7, A8,A9,  A4,A5,  A10,A11};

float slow_baselines[] = {0,0,0,0,0,0,0,0,0,0,0,0};
float s = 0.999;

int num_pins = 12;
const float VCC = 5.0; // Estimated voltage of Ardunio 5V line
const float R_DIV = 10000.0; // Estimated resistance of 10k resistor

const int TAB_FORMAT = 0;

float get_flexR(int pin)
{
  int flexADC;
  float flexV;
  float flexR;
  flexADC = analogRead(flex_pins[pin]);
  flexV = flexADC * VCC / 1023.0;
  flexR = R_DIV * (VCC / flexV - 1.0);
  return flexR;
}

void setup() 
{
  Serial.begin(115200);
  for( int i = 0; i < num_pins; i = i + 1 ) {
        pinMode(flex_pins[i], INPUT);
        slow_baselines[i] = get_flexR(i);
  }
  for(int j = 0; j < 100; j = j+1) {
    for( int i = 0; i < num_pins; i = i + 1 ) {
      slow_baselines[i] = s * slow_baselines[i] + (1.0-s) * get_flexR(i);
    }
    delay(10);
  }
}


void loop() 
{
  float bflexR;

  for( int i = 0; i < num_pins; i = i + 1 ) {

    bflexR = get_flexR(i);

    slow_baselines[i] = s * slow_baselines[i] + (1.0-s) * bflexR;

    if (not TAB_FORMAT) Serial.print("('");
    if (not TAB_FORMAT) Serial.print(Flexes[i]);
    if (not TAB_FORMAT) Serial.print("',");
    
    Serial.print(bflexR - slow_baselines[i]);
    //Serial.print(bflexR);
    if (TAB_FORMAT) Serial.print('\t');
    else Serial.println(")");
  }

  if (TAB_FORMAT) Serial.println("");
  
  
  delay(10);
  

}

