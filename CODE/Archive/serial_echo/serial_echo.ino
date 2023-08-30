// DEFINES
// https://forum.arduino.cc/t/serial-input-basics-updated/382007/10
//#define packet_start '<'
//#define packet_end '>'

// pins for the LEDs:
const byte numChars = 32;
int packet = 0;

const byte num_relays         =   8;                          // Number of relays to define static array lengths
byte states[num_relays]       =   {0, 0, 0, 0, 0, 0, 0, 0};   // Relay states as described by Python code
byte num_received             =   0;                          // Number of bytes recived
int relay_pins[num_relays]    =   {2, 3, 4, 5, 6, 7, 8, 9};   // Relay link to Arduino pins

boolean new_data = false;

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
    recvBytesWithStartpacket_ends();
}

void recvBytesWithStartpacket_ends() {
    static boolean receiving = false;
    static byte i = 0;
    byte packet_start = 0x3C;   // '<'
    byte packet_end = 0x3E;     // '>'
    byte read_byte;
   

    while (Serial.available() > 0 && new_data == false) {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(1000);
      digitalWrite(LED_BUILTIN, LOW);
      read_byte = Serial.read();
      // ADD CONDITION TO CHECK LENGTH OF ARRAY, MUST MATCH num_relays
      if (receiving == true) {
          if (read_byte != packet_end) {
            states[i] = read_byte;
            i++;
            if (i >= num_relays) {
              i = num_relays - 1;
            }
          }
          else {
            receiving = false;
            num_received = i;  // save the number for use when printing
            i = 0;
            new_data = true;
          }
        }

        else if (read_byte == packet_start) {
            receiving = true;
        }
    }
}
