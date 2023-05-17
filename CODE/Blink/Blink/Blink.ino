const int IN1 = 1; //Relay IN1 input pin

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  digitalWrite(IN1, HIGH);
  pinMode(IN1, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(IN1, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(2000);                       // wait for a second
  digitalWrite(IN1, LOW);    // turn the LED off by making the voltage LOW
  delay(2000);                       // wait for a second
}
