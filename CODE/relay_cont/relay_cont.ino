//Control relays with arduino
// #include <Keyboard.h>

const int IN1 = 2; //Relay IN1 input pin
const int IN2 = 3; //Relay IN2 input pin
const int IN3 = 4; //Relay IN3 input pin
const int IN4 = 5; //Relay IN4 input pin
const int IN5 = 6; //Relay IN5 input pin
const int IN6 = 7; //Relay IN6 input pin
const int IN7 = 8; //Relay IN7 input pin
const int IN8 = 9; //Relay IN8 input pin

void setup() {
  // Define output pins
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, HIGH);
  digitalWrite(IN5, HIGH);
  digitalWrite(IN6, HIGH);
  digitalWrite(IN7, HIGH);
  digitalWrite(IN8, HIGH);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(IN5, OUTPUT);
  pinMode(IN6, OUTPUT);
  pinMode(IN7, OUTPUT);
  pinMode(IN8, OUTPUT);
  // Initialize keyboard
  // Keyboard.begin();
  // Start up serial
  Serial.begin(9600);
}

void loop() {
  // Keyboard input logic
  if (Serial.available()) 
  {
    switch (Serial.read())
    {
      case '1': 
        digitalWrite(IN1, !digitalRead(IN1));
        Serial.print("IN1 ");
        Serial.println(digitalRead(IN1));
        break;
      case '2': 
        digitalWrite(IN2, !digitalRead(IN2));
        Serial.print("IN2 ");
        Serial.println(digitalRead(IN2));
        break;
      case '3':
        digitalWrite(IN3, !digitalRead(IN3));
        Serial.print("IN3 ");
        Serial.println(digitalRead(IN3));
        break;
      case '4':
        digitalWrite(IN4, !digitalRead(IN4));
        Serial.print("IN4 ");
        Serial.println(digitalRead(IN4));
        break;
      case '5':
        digitalWrite(IN5, !digitalRead(IN5));
        Serial.print("IN5 ");
        Serial.println(digitalRead(IN5));
        break;
      case '6':
        digitalWrite(IN6, !digitalRead(IN6));
        Serial.print("IN6 ");
        Serial.println(digitalRead(IN6));
        break;
      case '7':
        digitalWrite(IN7, !digitalRead(IN7));
        Serial.print("IN7 ");
        Serial.println(digitalRead(IN7));
        break;
      case '8':
        digitalWrite(IN8, !digitalRead(IN8));
        Serial.print("IN8 ");
        Serial.println(digitalRead(IN8));
        break;
    }
  }
}
