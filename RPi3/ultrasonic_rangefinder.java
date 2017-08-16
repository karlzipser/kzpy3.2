// http://www.circuitbasics.com/how-to-set-up-an-ultrasonic-range-finder-on-an-arduino/
// see http://blog.oscarliang.net/connect-raspberry-pi-and-arduino-usb-cable/
// http://randomnerdtutorials.com/complete-guide-for-ultrasonic-sensor-hc-sr04/

#define trigPin 10
#define echoPin 13

void setup() {
  Serial.begin (9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  float duration, distance;
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(5); // was 2
  pinMode(echoPin, OUTPUT);
  digitalWrite(echoPin, LOW);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH,10000);
  distance = (duration / 2) * 0.0344;
  
  if (distance >= 400 || distance <= 2){
    Serial.print("Distance = ");
    Serial.print(distance);
    Serial.println(", Out of range");
    pinMode(echoPin, OUTPUT);
    digitalWrite(echoPin, LOW);
  }
  else {
    Serial.print("Distance = ");
    Serial.print(distance);
    Serial.println(" cm");
  }
  delay(1000/15);
}
