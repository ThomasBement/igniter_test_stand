#!/usr/bin/env python3
import sys
import os
from datetime import datetime as dt
import asyncio
import tkinter as tk

from async_tkinter_loop import async_handler, async_mainloop

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

"""
CONSTANTS
"""
port = 'COM3'                       # Serial port for commands, Windoz
port = '/dev/ttyUSB0'               # Serial port for commands, Linux
baud_rate = '9600'

# Start up serial w/ command line params, if present.
if len(sys.argv) > 1: port = sys.argv[1]
if len(sys.argv) > 2: baud_rate = sys.argv[2]

'''
print("Test started...", end='')
log_name = os.path.splitext(sys.argv[0])[0]+'.log'
g_log = lh.setup_custom_logger(log_name)
print('Log on: ' + log_name)
print("Open serial port (resets Arduino)...", end='')
s = sh.open_serial_port(port, baud_rate, g_log)
print("Wait on Arduino...", end='')
time.sleep(2) # Wait for Arduino to reset and initialize.
print('OK')
send_command_check_resp(s, 'b00000000\n')   # All relays off to start.
'''

async def counter():
    i = 0
    while True:
        i += 1
        label.config(text=str(i))
        await asyncio.sleep(1.0)


root = tk.Tk()

label = tk.Label(root)
label.pack()

tk.Button(root, text="Start", command=async_handler(counter)).pack()

async_mainloop(root)
