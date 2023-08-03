#!/usr/bin/env python3

# ---------------------------------------- #
# test_stand_gui [Python File]
# Written By: Thomas Bement
# Created On: 2023-07-12
# ---------------------------------------- #

"""
IMPORTS
"""
from contextlib import nullcontext
from doctest import master
import os
import sys
import time
import serial
import struct
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import random

from PIL import ImageTk, Image
from tkinter import LEFT, filedialog

import serial_helper as sh
import logger_helper as lh

""" -------------------------------------------------------------------------------------
CONST
------------------------------------------------------------------------------------- """ 
# Graphics
window_width        = 1400                                  # GUI window width          [px]
window_height       = 850                                   # GUI window height         [px]
window_image_path   = './IMG/PnID_GUI_1400_850.png'         # Main GUI background       [str]
async_delay         = 1000                                  # Interval for serial check [ms]

""" -------------------------------------------------------------------------------------
GLOBAL VARS
------------------------------------------------------------------------------------- """
# Logic
relay_states        = [False,  False,  False,  False,  False,  False,  False,  False]   # Relay states False - nominal, True - inverted
serial_status       = False                                                             # Serial conection status, Flase - disconnected, True - connected

""" -------------------------------------------------------------------------------------
Initialize serial port to talk with arduino
------------------------------------------------------------------------------------- """
port = "/dev/ttyUSB0"
if len(sys.argv) > 1: port = sys.argv[1]
baud_rate = '9600'
if len(sys.argv) > 2: baud_rate = sys.argv[2]

print(sys.argv[0] + " started...", end='')
log_name = os.path.splitext(sys.argv[0])[0]+'.log'
g_log = lh.setup_custom_logger(log_name)
already_logged_termios_error = False
print('Log on: ' + log_name)
print("Open serial port (resets Arduino)...", end='')
s = sh.open_serial_port(port, baud_rate, g_log)
print("Wait on Arduino...", end='')
time.sleep(2) # Wait for Arduino to reset and initialize.
print('OK')

""" -------------------------------------------------------------------------------------
TKINTER INIT
------------------------------------------------------------------------------------- """
window = tk.Tk()
window.wm_title('Test Stand GUI')
window.geometry('%ix%i' %(window_width, window_height))
window.resizable(0, 0)
frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
px_img = tk.PhotoImage(master=window, width=1, height=1)

# Load P&ID diagram as background
canvas = tk.Canvas(window, width=window_width, height=window_height)
canvas.pack()
background_image = ImageTk.PhotoImage(master = canvas, file = window_image_path)
canvas.create_image(0, 0, image = background_image, anchor = "nw")

# Add status label and locate it in the GUI
status_label = tk.Label(canvas, text='', fg='#000000', font=("Helvetica", 10))
status_label.place(x=885, y=70)

""" -------------------------------------------------------------------------------------
CLASSES
------------------------------------------------------------------------------------- """
class button:
    def __init__(self, name, position, size, color, relay_pointers, btn_type = 'invert', text = '', font = ("Helvetica", 18)):
        # Determine types for variables inside the button class
        type_list = [[name,             str,    'name'],
                    [position,         tuple,  'position'],
                    [size,             tuple,  'size'], 
                    [color,            str,    'color'], 
                    [relay_pointers,   list,   'relay_pointers'],
                    [btn_type,          str,   'btn_type'],
                    [text,              str,   'text'],
                    [font,              tuple,   'font']]
        # Perform type check and assign nan/inf for all variables that don't comply 
        for i in range(len(type_list)):
            variable            =   type_list[i][0]
            variable_type       =   type_list[i][1]
            variable_name       =   type_list[i][2]
            if type(variable) != variable_type:
                print('Type error, button %s expected to recive a %s for variable %s, but got %s instead' %(self, variable_type, variable_name, type(variable)))
                type_list[i][0] = float('NAN')
        # Font to px conversion for centering label
        font_sz = font[1]
        font_px = int(font_sz*(16/12))
        # Assign basic init variables to button object
        self.name               = type_list[0][0]
        self.x_pos              = type_list[1][0][0]
        self.y_pos              = type_list[1][0][1]
        self.width              = type_list[2][0][0]
        self.height             = type_list[2][0][1]
        self.color              = type_list[3][0]
        self.pointers           = type_list[4][0]
        self.btn_type           = type_list[5][0]
        self.text               = type_list[6][0]
        self.font               = type_list[7][0]
        # Assign tkinter specific attributes
        if (self.btn_type == 'driven'):
            self.btn = tk.Button(canvas, width=self.width, height=self.height, bg=self.color, image=px_img, state="disabled", 
                                 text=self.text, font=self.font, fg='#000000', compound=LEFT, command=lambda b=self: state_change(b, relay_states))
        else:
            self.btn = tk.Button(canvas, width=self.width, height=self.height, bg=self.color, image=px_img, 
                                 text=self.text, font=self.font, fg='#000000', compound=LEFT, command=lambda b=self: state_change(b, relay_states))
        self.btn.place(x=self.x_pos, y=self.y_pos)
        
""" -------------------------------------------------------------------------------------
FUNCTIONS
------------------------------------------------------------------------------------- """

def send_command_check_resp(s, byte_val):
    try:    
        send_string = 'b' + format(byte_val, '08b') + '\n'
        sh.send_line_to_serial(s, send_string)
        response = sh.read_line_from_serial(s)
        if (response == send_string): return True 
        return False
            
    except BaseException as e:
        g_log.error(f'Exception/Error during send_command_check_resp: {type(e)}: {e}')
        return False

def send_relay_state_to_arduino_update_graphics():
    # Encode relay_states to a byte and send as binary string to arduino
    byte_states = sum([int(relay_states[i]) << i for i in range(len(relay_states))])
    if send_command_check_resp(s, byte_states): serial_status = True
    else: serial_status = False
    update_graphics(relay_states, serial_status)

def update_graphics(relay_states, serial_status):
    # Update serial status status
    if serial_status:
        status_text = 'CONNECTED'
        status_color = '#2C9E10'
    else:
        status_text = 'DISCONNECTED'
        status_color = '#FF2424'
    status_label.configure(text='Serial Status: %s' %(status_text), bg=status_color)    
    # Update relay valve buttons
    for b in buttons:
        if (b.btn_type != 'state'):
            disp_text = '?'
            if serial_status:
                if (relay_states[b.pointers[0]] == True):
                    disp_text = '0'
                else:
                    disp_text = 'X'
            b.btn.configure(text=disp_text)
    # Update status indicator box
    for b in buttons:
        if (b.btn_type == 'state'):
            b.btn.configure(bg='#8132A8')
            if (relay_states == b.pointers):
                b.btn.configure(bg='#2C9E10')    

def state_change(b: button, relay_states):
    # Update relay_states array
    if (b.btn_type == 'invert'):
        for i in b.pointers:
            relay_states[i] = not(relay_states[i])
    elif (b.btn_type == 'driven'):
        pass
    elif (b.btn_type == 'state'):
        if (len(relay_states) == len(b.pointers)):
            for i in range(len(relay_states)):
                relay_states[i] = b.pointers[i]
        else:
            print('Error, length missmatch. %s expected a length of %i, but got %i instead.' %(b.name, len(relay_states), len(b.pointers)))
    else:
        print('Button type error. %s expected a type of invert, driven or state, but got %s instead.' %(b.name, b.btn_type))
    send_relay_state_to_arduino_update_graphics()

""" -------------------------------------------------------------------------------------
TK-LOOP
------------------------------------------------------------------------------------- """
valve_size  = (32, 32)
state_size  = (65, 30)
# Define buttons,   (name,          position,       size,           color,          relay_pointers,                                             btn_type,   text)
PR_SV_001   = button('PR_SV_001',   (485, 159),     valve_size,     '#FFC336',      [0],                                                        'invert',   '?',        ("Helvetica", 18))  
PR_SV_002   = button('PR_SV_002',   (488, 59),      valve_size,     '#FFC336',      [1],                                                        'invert',   '?',        ("Helvetica", 18)) 
PR_SV_003   = button('PR_SV_003',   (614, 419),     valve_size,     '#FFC336',      [2],                                                        'invert',   '?',        ("Helvetica", 18)) 
PR_SV_004   = button('PR_SV_004',   (614, 305),     valve_size,     '#FFC336',      [3],                                                        'invert',   '?',        ("Helvetica", 18)) 
PG_SV_001   = button('PG_SV_001',   (410, 440),     valve_size,     '#FFC336',      [4],                                                        'invert',   '?',        ("Helvetica", 18)) 
K_PV_001    = button('K_PV_001',    (1030, 159),    valve_size,     '#FF2424',      [3],                                                        'driven',   '?',        ("Helvetica", 18))
O2_PV_001   = button('O2_PV_001',   (354, 679),     valve_size,     '#2C9E10',      [2],                                                        'driven',   '?',        ("Helvetica", 18)) 
SAFE        = button('safe',        (885, 0),       state_size,     '#8132A8',      [False, False, False, False, False, False, False, False],   'state',    'SAFE',     ("Helvetica", 10))
FILL        = button('fill',        (960, 0),       state_size,     '#8132A8',      [False, True,  False, False, False, False, False, False],   'state',    'FILL',     ("Helvetica", 10))
PRESS       = button('press',       (1035, 0),      state_size,     '#8132A8',      [True,  False, False, False, False, False, False, False],   'state',    'PRESS',    ("Helvetica", 10))
FIRE        = button('fire',        (1110, 0),      state_size,     '#8132A8',      [True,  False, True,  True,  False, False, False, False],   'state',    'FIRE',     ("Helvetica", 10))
PURGE       = button('purge',       (1185, 0),      state_size,     '#8132A8',      [False, False, False, False, True,  False, False, False],   'state',    'PURGE',    ("Helvetica", 10))
DEPRES      = button('depres',      (1260, 0),      state_size,     '#8132A8',      [False, True,  False, False, False, False, False, False],   'state',    'DEPRESS',  ("Helvetica", 10))
ESTOP       = button('depres',      (1335, 0),      state_size,     '#8132A8',      [False, False, False, False, False, False, True,  True ],   'state',    'E-STOP',   ("Helvetica", 10))

buttons     = [PR_SV_001, PR_SV_002, PR_SV_003, PR_SV_004, PG_SV_001, K_PV_001, O2_PV_001, SAFE, FILL, PRESS, FIRE, PURGE, DEPRES, ESTOP]

# Send relay state to arduino first time and generate buttons
send_relay_state_to_arduino_update_graphics()

"""
LOOPED FUNCTIONS, called once per frame.
"""
def serial_check():
    send_relay_state_to_arduino_update_graphics() # Check that arduino is still responding.
    window.after(async_delay, serial_check)       # Request subsequent serial checks.

window.after(async_delay, serial_check) # Request first serial check.
window.mainloop()                       # Blocks untill window distroyed.


""" -------------------------------------------------------------------------------------
PROGRAM TERMINATION
------------------------------------------------------------------------------------- """
# Close out serial port at finish
print('Thanks for playing...')
