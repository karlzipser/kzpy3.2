//////////////////////////////////////////////////////////////////////
// PINS: 4,5 //2,3
// Baud: 9600
#define encoder0PinA  4 //2
#define encoder0PinB  5 //3
volatile int encoder0Pos = 0;
volatile boolean PastA = 0;
volatile boolean PastB = 0;
volatile unsigned long int a = 0;
volatile unsigned long int b = 0;
volatile unsigned long int t1 = millis();
volatile unsigned long int t2 = 0;
volatile unsigned long int dt = 0;
volatile float rate_1 = 0.0;
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
}
void encoder_loop()
{  
  dt = millis()-t1;
  if (dt > 100) {
    rate_1 = 1000.0/16.0 * a / dt;
    t1 = millis();
    a = 0;
  }
 //your staff....ENJOY! :D
  //Serial.print('(');
  //Serial.print(b);
  //Serial.print(' ');
  Serial.println(rate_1);
  //Serial.println(')');
  delay(100);
}
//you may easily modify the code  get quadrature..
//..but be sure this whouldn't let Arduino back! 
void doEncoderA()
{
     t2 = micros();
     a = a + 1;
}
void doEncoderB()
{
     b += 1;
}
//////////////////////////////////////////////////////////////////////

