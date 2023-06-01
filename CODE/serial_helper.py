#!/usr/bin/python3

#*****************************************************************************
#
# serial_helper.py - Implementation of serial port helper functions.
#
# Author: Reed Bement Tue 15 Nov 2022
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
#******************************************************************************

import serial
import sys
import os
import time
import numpy as np
import logger_helper

RX_TIMEOUT = 0.1     # seconds

g_log = None

# Use list comprehension to create a list of strings with control characters
# replaced by their delimited hex representations: ['Hi', '{0xd}', '{0xa}']
#
def escape_ctrl_chars(s):
    l = [c if (ord(c) >= 0x20) else "{"+str(hex(ord(c)))+"}" for c in s]
    return ''.join(l)

def open_serial_port(port, baud_rate, log = None):
    global g_log
    if log is not None: g_log = log
    print("Opening " + port + " at " + baud_rate + " baud...", end='')
    if g_log is not None: log.info("Opening " + port + " at " + baud_rate + " baud...")
    if sys.platform == "linux": 
        if os.path.exists(port) == False:
            print("   Device not present. Exiting.")
            if g_log is not None: g_log.info("   Device not present. Exiting.")
            sys.exit(1)
    s = serial.Serial(port, int(baud_rate), timeout=RX_TIMEOUT)
    s.reset_output_buffer()
    s.reset_input_buffer()
    while (s.read(1)):
        print('.', end='')
        if g_log is not None: g_log.info('.')
        time.sleep(.1)
    print("Ok")
    if g_log is not None: g_log.info("Ok")
    return s

def read_line_from_serial(s, timeout = RX_TIMEOUT):
    global g_log
    resp = ""
    while(timeout >= 0.0):
        b = s.read(1)
        if b:
            resp += b.decode('utf-8')
            if b == b'\x0A':
                if g_log is not None: g_log.to_host(escape_ctrl_chars(resp))
                return resp
        else: timeout -= RX_TIMEOUT;
    return None

def send_line_to_serial(s, line):
    global g_log
    s.reset_output_buffer()
    s.reset_input_buffer()
    if g_log is not None: g_log.to_ard(escape_ctrl_chars(line))
    s.write(line.encode('ascii'))
    s.flush()
    return

if __name__ == "__main__":
    s = open_serial_port("/dev/ttyUSB0", '9600')
    send_line_to_serial(s, "Hello Serial!\r\n")
    print(read_line_from_serial(s))
