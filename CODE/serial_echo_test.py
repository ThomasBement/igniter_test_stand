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

import sys
import serial_helper as sh
import logger_helper as lh

port = "/dev/ttyUSB0"
if len(sys.argv) > 1: port = sys.argv[1]
baud_rate = '9600'
if len(sys.argv) > 2: baud_rate = sys.argv[2]

print("Test started...")

g_log = lh.setup_custom_logger('serial_echo_test.log')
s = sh.open_serial_port(port, baud_rate, g_log)

# 0b00000000 => all relays off
#
r      = 0b00000000
relay0 = 0b00000001 
relay1 = 0b00000010

# Relay 0 and 1 on.
r |= relay0
r |= relay1    

# format command string as 8 bit binary value with end of line character terminating.
send_string = format(r, '08b') + '\r\n'

sh.send_line_to_serial(s, send_string)
response = sh.read_line_from_serial(s)
if (response == send_string): print("Command string echoed correctly") 
else: print("Error! Command string not echoed correctly")

# Turn relay 0 off:
r &= ~relay0

send_string = format(r, '08b') + '\r\n'
sh.send_line_to_serial(s, send_string)
response = sh.read_line_from_serial(s)
if (response == send_string): print("Command string echoed correctly") 
else: print("Error! Command string not echoed correctly")

print('OK')
