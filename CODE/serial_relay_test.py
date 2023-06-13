#!/usr/bin/env python3

#*****************************************************************************
#
# serial_echo_test.py - Implementation of serial port echo test.
#
# Author: Reed Bement Sun 02 Apr 2023
#
#    Notes:
#    ----
#
#  https://pyserial.readthedocs.io/en/latest/pyserial_api.html
#
#  Install: pip3 install pyserial
#
#  Get USB serial port info from linux:
#    lsusb
#    dmesg | grep tty
#    ls -la /dev/ttyUSB*
#    ls -la /dev/ttyACM*
#    udevadm info /dev/ttyUSB0
#
#  Run:
#   ./serial_echo_test.py com3 9600            Windows
#   ./serial_echo_test.py /dev/ttyUSB0 9600    Linux
#
#  Create a virtual loopback port under unix-like OS (https://pypi.org/project/PyVirtualSerialPorts/):
#   virtualserialports -l 1&
#   
#******************************************************************************

import os
import sys
import time
import serial_helper as sh
import logger_helper as lh

def send_command_check_resp(s, send_string):
	sh.send_line_to_serial(s, send_string)
	response = sh.read_line_from_serial(s)
	if (response == send_string): print("Command string echoed correctly: "  + response) 
	else: 
		print("Error! Command string not echoed correctly")
		print("Sent:     " + send_string)
		if (response): print("Received: " + response)
		else: print("Received: no response")
	
port = "/dev/ttyUSB0"
if len(sys.argv) > 1: port = sys.argv[1]
baud_rate = '9600'
if len(sys.argv) > 2: baud_rate = sys.argv[2]

print("Test started...", end='')
log_name = os.path.splitext(sys.argv[0])[0]+'.log'
g_log = lh.setup_custom_logger(log_name)
print('Log on: ' + log_name)
print("Open serial port (resets Arduino)...", end='')
s = sh.open_serial_port(port, baud_rate, g_log)
print("Wait on Arduino...", end='')
time.sleep(2) # Wait for Arduino to reset and initialize.
print('OK')

# Iterate over each relay on alone, all on, all off.
for r in [0b00000001,0b00000010,0b00000100,0b00001000,0b00010000,0b00100000,0b01000000,0b10000000,0b11111111,0b00000000]:
	# format command string as 8 bit binary value with end of line character terminating.
	send_string = 'b' + format(r, '08b') + '\n'
	send_command_check_resp(s, send_string)
	time.sleep(2)

print('OK')
