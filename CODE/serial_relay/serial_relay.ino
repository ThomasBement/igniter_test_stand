#include <errno.h>
#include <assert.h>
#include <SoftwareSerial.h>

#define IN1 2 //Relay IN1 input pin
#define IN2 3 //Relay IN2 input pin
#define IN3 4 //Relay IN3 input pin
#define IN4 5 //Relay IN4 input pin
#define IN5 6 //Relay IN5 input pin
#define IN6 7 //Relay IN6 input pin
#define IN7 8 //Relay IN7 input pin
#define IN8 9 //Relay IN8 input pin

SoftwareSerial mySerial(10, 11); // RX, TX

void flush_serial_rc(void)
{
    while (Serial.available() > 0) Serial.read();
}

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);

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

  while (!Serial);

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
        digitalWrite(IN1, ~(b & 0b00000001)); // replace with port write if possible
        digitalWrite(IN2, ~(b & 0b00000010));
        digitalWrite(IN3, ~(b & 0b00000100));
        digitalWrite(IN4, ~(b & 0b00001000));
        digitalWrite(IN5, ~(b & 0b00010000));
        digitalWrite(IN6, ~(b & 0b00100000));
        digitalWrite(IN7, ~(b & 0b01000000));
        digitalWrite(IN8, ~(b & 0b10000000));
        Serial.write(szRxCommand);
    }
}

