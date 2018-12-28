


   void setup() {
    pinMode(9, OUTPUT);
    Serial.begin(115200);
   }
    void loop() {
    int output = 0;
    for (int i = 0; i <999999; i++) {
      analogWrite(9, output);  // analogRead values go from 0 to 1023, analogWrite values from 0 to 255
      output += 1;
      if (output >170) output = 0;
      // 170 --> 3.3V
      float currentReading = analogRead(A5)*5/1024.0;
      Serial.print(5); Serial.print('\t');
      Serial.print(0); Serial.print('\t');
      Serial.println(currentReading);
      delay(10);
    }
    while (1) {
      int a = 1;//Serial.println("Done.");
    }
  }
