

const int led_LEFT =  2;
const int led_RIGHT = 11;
const int led_DATA =  3;
const int led_STATE_1 = 8;
const int led_STATE_2 = 9;
const int led_STATE_3 = 10;
const int led_STATE_4 = 12;

const int button_A =  5;
const int button_B =  6;
const int button_C =  7;
const int button_D =  4;

int button_A_state = LOW;
int button_B_state = LOW;
int button_C_state = LOW;
int button_D_state = LOW;


void setup() {
  Serial.begin(115200);
  Serial.setTimeout(5);
  pinMode(button_A, INPUT);
  pinMode(button_B, INPUT);
  pinMode(button_C, INPUT);
  pinMode(button_D, INPUT);
  pinMode(led_LEFT, OUTPUT);
  pinMode(led_RIGHT, OUTPUT);
  pinMode(led_STATE_1, OUTPUT);
  pinMode(led_STATE_2, OUTPUT);
  pinMode(led_STATE_3, OUTPUT);
  pinMode(led_STATE_4, OUTPUT);


}
int sig_data = 0;
int sig_state = 0;
int sig_left_right = 0;
int a = 0;
int b = 0;
int c = 0;
int d = 0;
int e = 0;

void loop() {

  int parsed_int = Serial.parseInt();

  
  int I = 0;
  
  if (parsed_int > 0) {
    I = parsed_int;
  }

  button_A_state = digitalRead(button_A);
  button_B_state = digitalRead(button_B);
  button_C_state = digitalRead(button_C);
  button_D_state = digitalRead(button_D);
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


  if (button_A_state == HIGH) {
    digitalWrite(led_LEFT, HIGH);
    Serial.println("('left_right',-1)");
  }
  else if (button_B_state == HIGH) {
    digitalWrite(led_RIGHT, HIGH);
    Serial.println("('left_right',1)");
  }
  else {
    Serial.println("('left_right',0)");
  }
  if (button_A_state == LOW) {
    digitalWrite(led_LEFT, LOW);
  }
  if (button_B_state == LOW) {
    digitalWrite(led_RIGHT, LOW);
  }

  
  if (sig_data == 2) {
    digitalWrite(led_DATA, HIGH);
  }
  else {
    digitalWrite(led_DATA, LOW);
  }

  if (sig_state == 4) {
    digitalWrite(led_STATE_1, HIGH);
    digitalWrite(led_STATE_2, HIGH);
    digitalWrite(led_STATE_3, HIGH);
    digitalWrite(led_STATE_4, HIGH);
  }
  else if (sig_state == 3) {
    digitalWrite(led_STATE_1, HIGH);
    digitalWrite(led_STATE_2, HIGH);
    digitalWrite(led_STATE_3, HIGH);
    digitalWrite(led_STATE_4, LOW);
  }
  else if (sig_state > 4) {
    digitalWrite(led_STATE_1, HIGH);
    digitalWrite(led_STATE_2, HIGH);
    digitalWrite(led_STATE_3, HIGH);
    digitalWrite(led_STATE_4, LOW);
  }
  else if (sig_state == 2) {
    digitalWrite(led_STATE_1, HIGH);
    digitalWrite(led_STATE_2, HIGH);
    digitalWrite(led_STATE_3, LOW);
    digitalWrite(led_STATE_4, LOW);
  }
  else if (sig_state == 1) {
    digitalWrite(led_STATE_1, HIGH);
    digitalWrite(led_STATE_2, LOW);
    digitalWrite(led_STATE_3, LOW);
    digitalWrite(led_STATE_4, LOW);
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




