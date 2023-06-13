#include <errno.h>
#include <assert.h>
#include <SoftwareSerial.h>

// The following provide a mapping from Arduino digital pin to relay
// board control pins INx. The pins must be in sequential order.
// Input control pins on relay board are active low. 
//
#define RELAY_BOARD_IN1_PIN     2	// Arduino Digital Pins D2 - D9
#define NUM_RELAY_BOARD_IN_PINS 8	// Number of input pins on realy board

// Serial command protocol at 9600 baud:
// SOT, Eight characters of zero or one, EOT
// Start of text (SOT): 'b',  98, 0x62
// End   of text (EOT): '\n', 10, 0x0A
//
#define SOT 'b'
#define EOT '\n'
#define NUM_COMMAND_BYTES (1 + 8 + 1)

// States for serial command RX state machine (bRxState).
//
#define IDLE    0
#define RX_BITS 1
#define RX_EOT  3
#define DONE    4


char g_szDbg[80];

SoftwareSerial mySerial(10, 11); // RX - D10 not used, TX - D11 sends debug log at 9600 baud

void flush_serial_rc(void)
{
    while (Serial.available() > 0) Serial.read();
}

byte receive_command_byte(byte bRxState, char *pszRxCmd)
{ 
	digitalWrite(LED_BUILTIN, HIGH);
	static word wIndex;
	byte b = Serial.read();
	if (isPrintable(b)) mySerial.write(b);
	else {
		sprintf(g_szDbg, "<0x%02X>", b);
		mySerial.print(g_szDbg);
	}
	
	switch (bRxState) {
        case IDLE:				// Waiting for SOT
			if (b == SOT) {
				pszRxCmd[0] = b;
				wIndex = 0;
 		        mySerial.println("\r\nRX_BITS");
				return RX_BITS;
			}
            break;
        case RX_BITS:			// Receive binary bits
			if ((b == '0') || (b == '1')) {
				pszRxCmd[++wIndex] = b;
				if (wIndex >= 8) {
 				    mySerial.println("\r\nRX_EOT");
					return RX_EOT;
				}
				return RX_BITS;
			}
            break;
        case RX_EOT:			// Receive EOT
			if (b == EOT) {
				pszRxCmd[9] = b;
				mySerial.println("\r\nDONE");
				return DONE;
			}
            break;
        default:
			mySerial.println("\r\nUnknown state!");
            assert(0);
    }
    mySerial.println("\r\nProtocol Error. Back to IDLE");
    memset(pszRxCmd, 0, sizeof(pszRxCmd));
	flush_serial_rc();
	return IDLE;	
}

void setup() {
	digitalWrite(LED_BUILTIN, LOW);
	pinMode(LED_BUILTIN, OUTPUT);

	// Open serial communications and wait for port to open:
	Serial.begin(9600);
	while (!Serial);
	
	// Define pins as output in inactive state.
	for (int i = 0;  i < NUM_RELAY_BOARD_IN_PINS; i++) {
	  digitalWrite(i + RELAY_BOARD_IN1_PIN, HIGH);
	  pinMode(i + RELAY_BOARD_IN1_PIN, OUTPUT);
	}
	
	// Set the data rate for the SoftwareSerial port (debug log).
	mySerial.begin(9600);
	mySerial.println("Relay control firmware, version 1.2");
}

void loop()
{
    static char szRxCmd[NUM_COMMAND_BYTES + 1]; // Command + NULL 
    static byte bRxState = IDLE;
    
    if (Serial.available()) bRxState = receive_command_byte(bRxState, szRxCmd);
    if (bRxState == DONE) {    
        errno = 0;
        byte b = (byte) (strtol(&szRxCmd[1], NULL, 2) & 0xFF);
        if (errno == 0 ) {
	        // Binary format conversion and termination checks passed, set relays.
	        byte bMask = 0b00000001;
	        for (int i = 0;  i < NUM_RELAY_BOARD_IN_PINS; i++) {
	            digitalWrite(i + RELAY_BOARD_IN1_PIN, (b & bMask) ? LOW:HIGH);
	            bMask <<= 1; 
	        }
	        mySerial.println("Relays set");
	        Serial.write(szRxCmd);
        }
		else {
			sprintf(g_szDbg, "Binary format error, strtol: %d", errno);
			mySerial.println(g_szDbg); Serial.println(g_szDbg);
		}
		bRxState = IDLE;
    }
    digitalWrite(LED_BUILTIN, LOW);
}
