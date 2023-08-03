#!/usr/bin/env python3
'''
python tkinter mainloop non blocking
https://pythonguides.com/python-tkinter-mainloop/
https://duckduckgo.com/?t=ffab&q=python+tkinter+countdown+example&ia=web


'''
import tkinter as tk
from tkinter import ttk

state = 0

# root window
root = tk.Tk()
root.geometry('300x200')
root.resizable(False, False)
root.title('Relay Demo')

def handle_relay_button():
    relay_button.text.set('Relay 0: ON')
    print("handle_relay_button")

# exit button
relay_button = ttk.Button(
    root,
    text='Relay 0: OFF',
    command=handle_relay_button
)

relay_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)

root.mainloop()
