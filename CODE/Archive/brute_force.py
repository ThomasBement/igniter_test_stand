# ---------------------------------------- #
# brute_force [Python File]
# Written By: Thomas Bement
# Created On: 2023-05-18
# ---------------------------------------- #

"""
IMPORTS
"""
import os
import time
import serial
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt

from PIL import ImageTk, Image
from tkinter import filedialog

"""
CONSTANTS
"""
refresh_delay = 10
com = 'COM3'
baud = 9600

# INDEX [0,1,2,3,4,5,6,7]
relay = [1,2,3,4,5,6,7,8]
state = [0,0,0,0,0,0,0,0]
btn_link = ['PR_SV_001','PR_SV_002','PR_SV_003','PR_SV_004',
            'PG_SV_001','NONE','E-STOP','E-STOP']

"""
FUNCTIONS
"""
def valve_press(name, text):
    valve_idx = btn_link.index(name)
    # Invert bool state
    state[valve_idx] = not(state[valve_idx])
    text.set(valve_state_to_text(state[valve_idx]))
    # Update dependancies
    match name:
        case 'PR_SV_003':
            dept_idx = btn_link.index('PR_SV_003')
            state[dept_idx] = state[valve_idx]
            text.set(valve_state_to_text(state[dept_idx]))
        case 'PR_SV_004':
            dept_idx = btn_link.index('PR_SV_004')
            state[dept_idx] = state[valve_idx]
            text.set(valve_state_to_text(state[dept_idx]))

def valve_state_to_text(state):
    if (state == 0):
        return 'X'
    elif (state == 1):
        return 'O'
    else:
        return '!'

"""
GUI
"""
# Open tkinter window
window = tk.Tk()
window.wm_title('Test Stand GUI')
window.geometry('1389x781')
window.resizable(False, False)
frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)

# Load P&ID diagram as background
img = ImageTk.PhotoImage(Image.open('./IMG/PnID_GUI.png'))
panel = tk.Label(window, image = img)
#panel.place(x=0, y=0)
panel.pack(side = "bottom", fill = "both", expand = "no")

# Generate switchable valve buttons
PR_SV_001_vars = [481, 100, '#FFC336', tk.StringVar(window, 'X')]
PR_SV_001 = tk.Button(textvariable=PR_SV_001_vars[3], width=4, height=2, bg=PR_SV_001_vars[2], fg="black", command=lambda name='PR_SV_001', text=PR_SV_001_vars[3]: valve_press(name, text))
PR_SV_001.place(x=PR_SV_001_vars[0], y=PR_SV_001_vars[1])

PR_SV_002_vars = [484, 0, '#FFC336', tk.StringVar(window, 'X')]
PR_SV_002 = tk.Button(textvariable=PR_SV_002_vars[3], width=4, height=2, bg=PR_SV_002_vars[2], fg="black", command=lambda name='PR_SV_002', text=PR_SV_002_vars[3]: valve_press(name, text))
PR_SV_002.place(x=PR_SV_002_vars[0], y=PR_SV_002_vars[1])

PR_SV_003_vars = [610, 361, '#FFC336', tk.StringVar(window, 'X')]
PR_SV_003 = tk.Button(textvariable=PR_SV_003_vars[3], width=4, height=2, bg=PR_SV_003_vars[2], fg="black", command=lambda name='PR_SV_003', text=PR_SV_003_vars[3]: valve_press(name, text))
PR_SV_003.place(x=PR_SV_003_vars[0], y=PR_SV_003_vars[1])

PR_SV_004_vars = [610, 247, '#FFC336', tk.StringVar(window, 'X')]
PR_SV_004 = tk.Button(textvariable=PR_SV_004_vars[3], width=4, height=2, bg=PR_SV_004_vars[2], fg="black", command=lambda name='PR_SV_004', text=PR_SV_004_vars[3]: valve_press(name, text))
PR_SV_004.place(x=PR_SV_004_vars[0], y=PR_SV_004_vars[1])

PG_SV_001_vars = [406, 382, '#FFC336', tk.StringVar(window, 'X')]
PG_SV_001 = tk.Button(textvariable=PG_SV_001_vars[3], width=4, height=2, bg=PG_SV_001_vars[2], fg="black", command=lambda name='PG_SV_001', text=PG_SV_001_vars[3]: valve_press(name, text))
PG_SV_001.place(x=PG_SV_001_vars[0], y=PG_SV_001_vars[1])

# Generate dependant valve buttons
K_PV_001_vars = [1026, 101, '#FF2424', tk.StringVar(window, 'X')]
K_PV_001 = tk.Button(textvariable=K_PV_001_vars[3], width=4, height=2, bg=K_PV_001_vars[2], fg="black", state="disabled")
K_PV_001.place(x=K_PV_001_vars[0], y=K_PV_001_vars[1])

O2_PV_001_vars = [350, 621, '#2C9E10', tk.StringVar(window, 'X')]
O2_PV_001 = tk.Button(textvariable=O2_PV_001_vars[3], width=4, height=2, bg=O2_PV_001_vars[2], fg="black", state="disabled")
O2_PV_001.place(x=O2_PV_001_vars[0], y=O2_PV_001_vars[1])

window.mainloop()