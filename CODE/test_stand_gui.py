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

"""
CONST
"""

# Graphics
window_width    = 1389
window_height   = 781
window_image_path = './IMG/PnID_GUI.png'
#serial_status = {'good': , 'bad': }
async_delay = 17                        # Delay time [ms]

"""
GLOBAL VARS
"""
# Logic
relay_states = [False,  False,  False,  False,  False,  False,  False,  False] # Relay states 0 - nominal, 1 - inverted

"""
TKINTER INIT
"""
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

"""
CLASSES
"""
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
        
"""
FUNCTIONS
"""
def update_graphics(relay_states):
    for b in buttons:
        if (b.btn_type != 'state'):
            disp_text = '?'
            if (relay_states[b.pointers[0]] == True):
                disp_text = '0'
            else:
                disp_text = 'X'
            b.btn.configure(text=disp_text)
    pass

def state_change(b: button, relay_states):
    # Update relay_states array
    if (b.btn_type == 'invert'):
        for i in b.pointers:
            relay_states[i] = not(relay_states[i])
    elif (b.btn_type == 'driven'):
        pass
    elif (b.btn_type == 'state'):
        if (len(relay_states) == len(b.pointers)):
            relay_states = b.pointers
        else:
            print('Error, length missmatch. %s expected a length of %i, but got %i instead.' %(b.name, len(relay_states), len(b.pointers)))
    else:
        print('Button type error. %s expected a type of invert, driven or state, but got %s instead.' %(b.name, b.btn_type))
    # Encode relay_states to a byte
    byte_states = sum([int(relay_states[i]) << i for i in range(len(relay_states))])
    decode_states = [byte_states & (1 << i) != 0 for i in range(8)]
    print(byte_states)
    print(relay_states)
    print(decode_states)
    # Put serial coms here
    update_graphics(relay_states)

# Redundand 
def button_invert(b: button):
    for i in b.pointers:
        relay_states[i] = not(relay_states[i])

def button_state(b: button):
    if (len(relay_states) == len(b.pointers)):
        relay_states = b.pointers
    else:
        print('Error, length missmatch. %s expected a length of %i, but got %i instead.' %(b.name, len(relay_states), len(b.pointers)))

"""
TK-LOOP
"""
valve_size  = (40, 40)
state_size  = (40, 40)
# Define buttons,   (name,          position,       size,           color,          relay_pointers,                                             btn_type,   text)
PR_SV_001   = button('PR_SV_001',   (481, 100),     valve_size,     '#FFC336',      [0],                                                        'invert',   '?',        ("Helvetica", 18))  
PR_SV_002   = button('PR_SV_002',   (484, 0),       valve_size,     '#FFC336',      [1],                                                        'invert',   '?',        ("Helvetica", 18)) 
PR_SV_003   = button('PR_SV_003',   (610, 361),     valve_size,     '#FFC336',      [2],                                                        'invert',   '?',        ("Helvetica", 18)) 
PR_SV_004   = button('PR_SV_004',   (610, 247),     valve_size,     '#FFC336',      [3],                                                        'invert',   '?',        ("Helvetica", 18)) 
PG_SV_001   = button('PG_SV_001',   (406, 382),     valve_size,     '#FFC336',      [4],                                                        'invert',   '?',        ("Helvetica", 18)) 
K_PV_001    = button('K_PV_001',    (1026, 101),    valve_size,     '#FF2424',      [3],                                                        'driven',   '?',        ("Helvetica", 18))
O2_PV_001   = button('O2_PV_001',   (350, 621),     valve_size,     '#2C9E10',      [2],                                                        'driven',   '?',        ("Helvetica", 18)) 
SAFE        = button('safe',        (1000, 0),      valve_size,     '#8132A8',      [False, False, False, False, False, False, False, False],   'state',    'SAFE',     ("Helvetica", 10))
FILL        = button('fill',        (1050, 0),      valve_size,     '#8132A8',      [False, True,  False, False, False, False, False, False],   'state',    'FILL',     ("Helvetica", 10))
PRESS       = button('press',       (1100, 0),      valve_size,     '#8132A8',      [True,  False, False, False, False, False, False, False],   'state',    'PRESS',    ("Helvetica", 10))
FIRE        = button('fire',        (1150, 0),      valve_size,     '#8132A8',      [True,  False, True,  True,  False, False, False, False],   'state',    'FIRE',     ("Helvetica", 10))
PURGE       = button('purge',       (1200, 0),      valve_size,     '#8132A8',      [False, False, True,  True,  True,  False, False, False],   'state',    'PURGE',    ("Helvetica", 10))
DEPRES      = button('depres',      (1250, 0),      valve_size,     '#8132A8',      [False, True,  False, False, False, False, False, False],   'state',    'DEPRES',   ("Helvetica", 10))
ESTOP       = button('depres',      (1324, 0),      valve_size,     '#8132A8',      [6, 7],                                                     'invert',   'E-STOP',   ("Helvetica", 10))

buttons     = [PR_SV_001, PR_SV_002, PR_SV_003, PR_SV_004, PG_SV_001, K_PV_001, O2_PV_001, SAFE, FILL, PRESS, FIRE, PURGE, DEPRES, ESTOP]

# Generate buttons  
update_graphics(relay_states)

"""
LOOPED FUNCTIONS
"""
#mainloop_fn(relay_states)
window.mainloop()


"""
PROGRAM TERMINATION
"""
# Close out serial port at finish
print('Thanks for playing...')