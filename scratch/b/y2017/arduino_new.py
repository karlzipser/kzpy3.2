import os, serial, threading, Queue
import threading
from kzpy3.utils import *

"""
Get rid of the idea of functions tied to particular Arduinos.
Set up way to travese complex state diagram with time dependence in order to use different
patterns to code function modes.
Test how much I can get into the servo arduino, especially the LED panel.
"""

def filter_1(states,state_times):
    t1 = state_times[1]
    t2 = state_times[4]
    dt = t2-t1
    if dt < 0.5 * 4:
        if states[0] == 20:
            if states[1] == 10:
                if states[2] == 20:
                    if states[3] == 10:
                        if states[4] == 20:
                            states[4] = -999
                            return True
    return False

def filter_2(states,state_times):
    t1 = state_times[1]
    t2 = state_times[4]
    dt = t2-t1
    if dt < 0.5 * 4:
        if states[0] == 40:
            if states[1] == 30:
                if states[2] == 40:
                    if states[3] == 30:
                        if states[4] == 40:
                            states[4] = -999
                            return True
    return False


def filter_3(states,state_times):
    t1 = state_times[1]
    t2 = state_times[4]
    dt = t2-t1
    if dt < 0.5 * 4:
        if states[0] == 20:
            if states[1] == 30:
                if states[2] == 20:
                    if states[3] == 30:
                        if states[4] == 20:
                            states[4] = -999
                            return True
    return False


ACM_port='/dev/tty.usbmodem1411'
baudrate=115200
timeout=0.25
Arduinos = {}
Arduinos['motor'] = serial.Serial(ACM_port,baudrate=baudrate,timeout=timeout)


caffe_mode = 1
timer = Timer(1)
states = []
state_times = []
t0 = time.time()
while True:
    """
    if timer.check():
        caffe_mode += 1
        timer.reset()
    if caffe_mode > 3:
        caffe_mode = -3
    if caffe_mode == 0:
        caffe_mode = 1
    """
    try:        
        read_str = Arduinos['motor'].readline()
        #print read_str
        exec('motor_data = list({0})'.format(read_str))
        
        write_int = caffe_mode * 10000
        write_str = '( {0} )'.format(write_int)
        #print motor_data,write_str,caffe_mode
        Arduinos['motor'].write(write_str)

        if time.time()-t0 > 5: # let system settle
            if len(states) == 0:
                t = time.time()-t0
                states.append(motor_data[1])
                state_times.append(dp(0,2))
            elif states[-1] == motor_data[1]:
                pass
            else:
                t = time.time()-t0
                t1 = state_times[-1]
                states.append(motor_data[1])
                state_times.append(dp(t,2))
   
            print zip(states,state_times)

            if filter_1(states,state_times):
                if caffe_mode == 1:
                    caffe_mode = 3
                elif caffe_mode == 3:
                    caffe_mode = 1

            elif filter_2(states,state_times):
                if caffe_mode == 1:
                    caffe_mode = -3
                elif caffe_mode == -3:
                    caffe_mode = 1

            elif filter_3(states,state_times):
                if caffe_mode == 1:
                    caffe_mode = 2
                elif caffe_mode == 2:
                    caffe_mode = 1
            elif states[-1] == 10 and caffe_mode == 2:
                caffe_mode = 1
            elif states[-1] == 30 and caffe_mode == 2:
                caffe_mode = 1
            elif states[-1] == 30 and caffe_mode == 2:
                caffe_mode = 1

            elif states[-1] == 30 and caffe_mode == -3:
                caffe_mode = 1
            elif states[-1] == 40 and caffe_mode == 3:
                caffe_mode = 1
            if len(states) > 5:
                states = states[-5:]
                state_times = state_times[-5:]

    except Exception as e:
        print e






