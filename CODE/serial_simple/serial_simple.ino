const byte num_relays         =   8;                          // Number of relays to define static array lengths
byte states[num_relays]       =   {0, 0, 0, 0, 0, 0, 0, 0};   // Relay states as described by Python code
byte num_received             =   0;                          // Number of bytes recived
int relay_pins[num_relays]    =   {2, 3, 4, 5, 6, 7, 8, 9};   // Relay link to Arduino pins


void setup() {
 // make the pins outputs:
  pinMode(LED_BUILTIN, OUTPUT);
  // initialize serial:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
 byte read_byte;
 int i = 0;
 while ((Serial.available() > 0)) {
  if (i > (num_relays-1)) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(2000);
    digitalWrite(LED_BUILTIN, LOW);
    delay(2000);
    
    serial_flush();
    i = 0;
  }
  else if (i == (num_relays-1)) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(50);
    digitalWrite(LED_BUILTIN, LOW);
    delay(50);
    
    read_byte = Serial.read();
    states[i] = read_byte;
    i++;
    
    Serial.write(states, num_relays);
    serial_flush();
    i = 0;
  }
  else {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(50);
    digitalWrite(LED_BUILTIN, LOW);
    delay(50);
    
    read_byte = Serial.read();
    states[i] = read_byte;
    i++;
  }
 }
}

void serial_flush(void) {
  while (Serial.available()) Serial.read();
}
