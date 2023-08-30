# ---------------------------------------- #
# send_arr [Python File]
# Written By: Thomas Bement
# Created On: 2023-06-05
# ---------------------------------------- #

import serial
import struct
import time

arduino = serial.Serial()
arduino.baudrate = 9600
arduino.port = 'COM3'
print('Serial connection information:')
print(arduino)
arduino.open()
if (arduino.is_open):
    print('Connection secured...')
else:
    print('Connection error...')
    quit()

end_loop = False
sample          = [1,   0,  0,  0,  0,  0,  0,  0]
packet_format   = 'bbbbbbbb'

def send_serial(arr, begin='<', end='>'):
    arduino.write(struct.pack(packet_format, *arr))
    print(arduino.inWaiting())
    time.sleep(1)
    print(arduino.inWaiting())
    while arduino.inWaiting() != 0:
        print(arduino.read())
    print('Done')

while not(end_loop):
    try:
        temp = input('Send Array (Y/N): ')
        match temp:
            case 'Y':
                send_serial(sample)
            case 'y':
                send_serial(sample)
            case 'N':
                end_loop = True
            case 'n':
                end_loop = True
    except KeyboardInterrupt:
        end_loop = True

# Close port
arduino.close()

quit()
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

while True:
    num = input("Enter a number: ") # Taking input from user
    value = write_read(num)
    print(value) # printing the value