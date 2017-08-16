import os, serial, threading, Queue
import threading
from kzpy3.utils import *

"""
Get rid of the idea of functions tied to particular Arduinos.
Set up way to travese complex state diagram with time dependence in order to use different
patterns to code function modes.
Test how much I can get into the servo arduino, especially the LED panel.
"""



ACM_port='/dev/tty.usbmodem1411'
baudrate=115200
timeout=0.25
ser = serial.Serial(ACM_port, baudrate=baudrate, timeout=timeout)

while True:
    try:        
        servos_str = ser.readline()
        #print servos_str
        exec('servos_tuple = list({0})'.format(servos_str))
        print servos_tuple
        servos_write_int = 10000
        servos_write_str = '( {0} )'.format(servos_write_int)
        ser.write(servos_write_str)
                
    except Exception as e:
        print e

