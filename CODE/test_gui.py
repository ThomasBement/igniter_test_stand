# ---------------------------------------- #
# test_gui [Python File]
# Written By: Thomas Bement
# Created On: 2023-05-16
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

"""
FUNCTIONS
"""
def valve_press(text, name):
    # Invert bool state
    valves[name][4] = not(valves[name][4])
    # Update button text based on state
    if(valves[name][4]==0):
        valves[name][3].set('X')
    elif(valves[name][4]==1):
        valves[name][3].set('O')
    # Update linked buttons
    match name:
        case 'PR_SV_004':
            valves['K_PV_001'][3].set(valves[name][3].get())
            valves['K_PV_001'][4] = valves[name][4]
        case 'PR_SV_003':
            valves['O2_PV_001'][3].set(valves[name][3].get())
            valves['O2_PV_001'][4] = valves[name][4]
    # Debug print
    #print(name, valves[name][4])

def command_stop():
    print('STOP')

# Input relay number and state to array
def package_packet(valves):
    ans = []
    for key in valves:
        ans.append((valves[key][5], valves[key][4]))
    return ans

"""
MAIN
"""
# Start up serial
print('Starting up...')
arduino = serial.Serial(port=com, baudrate=baud)
time.sleep(5)
print('Finished')


# Open tkinter window
window = tk.Tk()
window.wm_title('Test Stand GUI')
window.geometry('1389x781')
window.resizable(False, False)
frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)

states = ['safe', 'fill', 'full', 'press', 'flow', 'purge']
buttons = ['progress', 'estop']
# Contains information for all valves in the following format
# {'name': [x_pos, y_pos, color, default display state, default valve state, relay number]}
valves = {'PR_SV_001': [481, 100, '#FFC336', tk.StringVar(window, 'X'), False, 1], 'PR_SV_002': [484, 0, '#FFC336', tk.StringVar(window, 'X'), False, 2], 
          'PR_SV_003': [610, 361, '#FFC336', tk.StringVar(window, 'X'), False, 3], 'PR_SV_004': [610, 247, '#FFC336', tk.StringVar(window, 'X'), False, 4], 
          'PG_SV_001': [406, 382, '#FFC336', tk.StringVar(window, 'X'), False, 5], 'K_PV_001': [1026, 101, '#FF2424', tk.StringVar(window, 'X'), False, 0], 
          'O2_PV_001': [350, 621, '#2C9E10', tk.StringVar(window, 'X'), False, 0]}

# Load P&ID diagram as background
img = ImageTk.PhotoImage(Image.open('./IMG/PnID_GUI.png'))
panel = tk.Label(window, image = img)
#panel.place(x=0, y=0)
panel.pack(side = "bottom", fill = "both", expand = "no")

# Generate valve buttons
for key in valves:
    name = key
    if '_PV_' in name:
        name = tk.Button(textvariable=valves[key][3], width=4, height=2, bg=valves[key][2], fg="black", state="disabled")
        name.place(x=valves[key][0], y=valves[key][1])
    else: 
        name = tk.Button(textvariable=valves[key][3], width=4, height=2, bg=valves[key][2], fg="black", command=lambda name=name, text=valves[key][3]: valve_press(text, name))
        name.place(x=valves[key][0], y=valves[key][1])

# Generate estop
estop = tk.Button(textvariable=tk.StringVar(window, 'E-Stop'), width=8, height=3, bg="red", fg="black", command=command_stop)
estop.place(x=1324, y=0)

"""
LOOPED FUNCTIONS
"""
# Send serial data
def serial_refresh():
    # Get state data from valves array
    states = package_packet(valves)
    # Format into char packet
    temp = []    
    for i in range(len(states)):
        if (states[i][0] != 0):
            temp.append('%i,%i_' %(states[i][0], states[i][1]))
    packet = '<_%s>' %(''.join(temp))
    #arduino.write(bytes(packet, 'utf-8'))
    #data = arduino.readline()
    print(packet)
    window.after(refresh_delay, serial_refresh)

window.after(refresh_delay, serial_refresh)
window.mainloop()