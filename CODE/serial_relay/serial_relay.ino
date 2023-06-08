#include <errno.h>
#include <assert.h>
#include <SoftwareSerial.h>

// The following provide a mapping from Arduino digital pin to relay
// board control pins INx. The pins must be in sequential order.
//
#define RELAY_BOARD_IN1_PIN     2
#define NUM_RELAY_BOARD_IN_PINS 8

SoftwareSerial mySerial(10, 11); // RX, TX

void flush_serial_rc(void)
{
    while (Serial.available() > 0) Serial.read();
}

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial);

  // Define pins as output in inactive state.
  for (int i = 0;  i < NUM_RELAY_BOARD_IN_PINS; i++) {
      digitalWrite(i + RELAY_BOARD_IN1_PIN, HIGH);
      pinMode(i + RELAY_BOARD_IN1_PIN, OUTPUT);
  }

  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);
  mySerial.println("Relay control firmware, version 1.0");
}

void loop()
{
    static char szRxCommand[8 + 2 + 1]; // Eight characters of zero or one + CR + LF + NULL 
   
    if (Serial.available() >= (8 + 2)) {
        mySerial.write("Received: ");
        for (int i = 0;  i < 8 + 2; i++) {
            szRxCommand[i] = Serial.read();
            mySerial.write(szRxCommand[i]);
        }
        assert(szRxCommand[8 + 2] == '\0');
        // Check for terminators
        if ((szRxCommand[8] != '\r') or (szRxCommand[9] != '\n')) {
            mySerial.println("Invalid terminator");
            Serial.write("Error terminator\r\n");
            flush_serial_rc();
            return;
        }
        errno = 0;
        unsigned char b = (unsigned char) (strtol(szRxCommand, NULL, 2) & 0xFF);
        if (errno != 0 ) {
            mySerial.println("Binary format error");
            Serial.write("Error format\r\n");
            flush_serial_rc();
            return;
        }

        // Binary format conversion and termination checks passed, set relays.
        unsigned char bMask = 0b00000001;
        for (int i = 0;  i < NUM_RELAY_BOARD_IN_PINS; i++) {
            digitalWrite(i + RELAY_BOARD_IN1_PIN, (b & bMask) ? LOW:HIGH);
            bMask <<= 1; 
        }
        
        Serial.write(szRxCommand);
    }
}

