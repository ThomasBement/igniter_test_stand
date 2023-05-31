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
import struct
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from pySerialTransfer import pySerialTransfer as txfer

from PIL import ImageTk, Image
from tkinter import filedialog

"""
CONSTANTS
"""
refresh_delay   = 10                # Serial read/write delay in 
com             = 'COM3'            # COM port for serial connection

# Relay specific information
# UPDATE IN ARDUINO CODE
states          =   [0,             0,              0,              0,              0,              0,      0,          0]          # Relay states 0 - nominal, 1 - inverted
relay_num       =   [1,             2,              3,              4,              5,              6,      7,          8]          # Relay numbers 1 - IN1 ...
relay_arduino   =   ['PR_SV_001',   'PR_SV_002',    'PR_SV_003',    'PR_SV_004',    'PG_SV_001',    'NA',   'E-STOP',   'E-STOP']   # Relay valve wiring arduino

# Opperational states, see "relay_arduino" for valve names
system_states = {'safe': [0, 0, 0, 0, 0, 0, 0, 0],
                 'fill': [0, 1, 0, 0, 0, 0, 0, 0],
                 'press': [1, 0, 0, 0, 0, 0, 0, 0],
                 'fire': [1, 0, 1, 1, 0, 0, 0, 0],
                 'purge': [0, 0, 1, 1, 1, 0, 0, 0],
                 'depress': [0, 1, 0, 0, 0, 0, 0, 0]}

# Initialize state to "safe"
for i in range(len(states)):
    states[i] = system_states['safe'][i]
current_state = 'safe'

"""
FUNCTIONS
"""
# Function called on valve button press
def valve_press(text, name):
    # Invert bool state in master states array
    states[relay_arduino.index(name)] = int(not(states[relay_arduino.index(name)]))
    # Update dictionary bool state to match
    valves[name][4] = states[relay_arduino.index(name)]
    # Send updated state
    write = write_states()
    if write:
        # Update current state
        current_state = name
        # Update button text based on dictonary bool state
        if(valves[name][4]==0):
            valves[name][3].set('X')
        elif(valves[name][4]==1):
            valves[name][3].set('O')
        # Update arduinoed buttons based on dictonary bool state
        match name:
            case 'PR_SV_004':
                valves['K_PV_001'][3].set(valves[name][3].get())
                valves['K_PV_001'][4] = valves[name][4]
            case 'PR_SV_003':
                valves['O2_PV_001'][3].set(valves[name][3].get())
                valves['O2_PV_001'][4] = valves[name][4]
    
# Function called, serial connection: %b  %()on E-STOP button press
def command_stop():
    # Invert bool state in master states array
    idx = [i for i, x in enumerate(relay_arduino) if x=='E-STOP']
    for i in range(len(idx)):
        states[idx[i]] = int(not(states[idx[i]]))
    # Send updated state
    write_states()

# Function called when state button is pressed
def state_change(name):
    # Update states based on button
    for i in range(len(states)):
        states[i] = system_states[name][i]
    # Send updated state
    write = write_states()
    # Update all other buttons if Arduino sends back commanded states
    if write:
        for key in valves:
            if(valves[key][4]==0):
                valves[key][3].set('X')
            elif(valves[key][4]==1):
                valves[key][3].set('O')
            # Update arduinoed buttons based on dictonary bool state
            match key:
                case 'PR_SV_004':
                    valves['K_PV_001'][3].set(valves[key][3].get())
                    valves['K_PV_001'][4] = valves[key][4]
                case 'PR_SV_003':
                    valves['O2_PV_001'][3].set(valves[key][3].get())
                    valves['O2_PV_001'][4] = valves[key][4]

# Input relay number and state to array
def write_states():
    # Construct packet
    send_size = 0
    list_ = states
    list_size = arduino.tx_obj(list_, byte_format='b')
    send_size += list_size
    # Send
    arduino.send(send_size)
    # Wait for response
    while not arduino.available():
        if arduino.status < 0:
            if arduino.status == txfer.CRC_ERROR:
                print('ERROR: CRC_ERROR')
            elif arduino.status == txfer.PAYLOAD_ERROR:
                print('ERROR: PAYLOAD_ERROR')
            elif arduino.status == txfer.STOP_BYTE_ERROR:
                print('ERROR: STOP_BYTE_ERROR')
            else:
                print('ERROR: {}'.format(arduino.status))
    # Parse recived list
    rec_list_  = arduino.rx_obj(obj_type=type(list_), obj_byte_size=list_size, byte_format='b')
    print(list_size)
    print('SENT: {}'.format(list_))
    print('RCVD: {}'.format(rec_list_))
    print(' ')
    if (list_==rec_list_):
        return True
    else:
        # Debug print
        print('SENT: {}'.format(list_))
        print('RCVD: {}'.format(rec_list_))
        print(' ')
        return False
"""
MAIN
"""
# Start up serial
print('Starting up...')
try:
    arduino = txfer.SerialTransfer(com)
    arduino.open()
    time.sleep(2)

except KeyboardInterrupt:
    arduino.close()

except:
    import traceback
    traceback.print_exc()
    arduino.close()

print('Finished, serial connection secured')
print('COM: %s' %(com))
time.sleep(1)

# Open tkinter window
window = tk.Tk()
window.wm_title('Test Stand GUI')
window.geometry('1389x781')
window.resizable(0, 0)
frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)

# Contains information for all valves in the following format
# {'name': [x_pos, y_pos, color, default display state, default valve state, relay number]}
valves = {'PR_SV_001': [481, 100, '#FFC336', tk.StringVar(window, 'X'), states[relay_arduino.index('PR_SV_001')], relay_num[relay_arduino.index('PR_SV_001')]], 
          'PR_SV_002': [484, 0, '#FFC336', tk.StringVar(window, 'X'), states[relay_arduino.index('PR_SV_002')], relay_num[relay_arduino.index('PR_SV_002')]], 
          'PR_SV_003': [610, 361, '#FFC336', tk.StringVar(window, 'X'), states[relay_arduino.index('PR_SV_003')], relay_num[relay_arduino.index('PR_SV_003')]], 
          'PR_SV_004': [610, 247, '#FFC336', tk.StringVar(window, 'X'), states[relay_arduino.index('PR_SV_004')], relay_num[relay_arduino.index('PR_SV_004')]], 
          'PG_SV_001': [406, 382, '#FFC336', tk.StringVar(window, 'X'), states[relay_arduino.index('PG_SV_001')], relay_num[relay_arduino.index('PG_SV_001')]], 
          'K_PV_001': [1026, 101, '#FF2424', tk.StringVar(window, 'X'), 0, 0], 
          'O2_PV_001': [350, 621, '#2C9E10', tk.StringVar(window, 'X'), 0, 0]}



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

# Generate state buttons
for i, key in enumerate(system_states):
    name = key
    name = tk.Button(text=key, width=8, height=1, bg="blue", fg="black", command=lambda name=name: state_change(name))
    name.place(x=900+70*(i), y=0)  

"""
LOOPED FUNCTIONS
"""
# Send serial data
def serial_refresh():
    # Put looped functions here
    window.after(refresh_delay, serial_refresh)

window.after(refresh_delay, serial_refresh)
window.mainloop()

"""
PROGRAM TERMINATION
"""
# Close out serial port at finish
print('Thanks for playing...')
arduino.close()