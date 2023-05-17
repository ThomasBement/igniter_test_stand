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

int myArray[10];
byte* ddata = reinterpret_cast<byte*>(&myArray); // pointer for transferData()
pcDataLen = sizeof(myArray);

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
    packet = Serial.read();
    Serial.print("I received: ");
    Serial.println(packet, DEC);
  }
}
