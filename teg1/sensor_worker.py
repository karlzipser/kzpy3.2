from kzpy3.utils import *
import serial

"""
This program simply gathers sensor data from an Arduino and saves it.
"""

if '/Users/' in home_path:
    ser = serial.Serial('/dev/tty.usbmodem1411',115200) #115200)
else:
    ser = serial.Serial('/dev/ttyACM1',115200)
    # Note, this is a numberically higher port than used by the motor_servo_worker_2.py program
    # If the order of the ports gets reversed for some reason, there will be general malfunctioning.
ctr = 0
t0 = time.time()

f = open(opjD('teg_data','_'+time_str()+'.GPS_acc.txt'), 'w')

while True:
    ctr += 1
    try:
        s = ser.readline()
        exec('t = ' + s)
        assert(type(t) == tuple)
        t = list(t)
        t.append(time.time())
        if t[0] == -3:
            t[0] = 'gyr'
        elif t[0] == -1:
            t[0] = 'GPS'
        elif t[0] == -4:
            t[0] = 'son'
        f.write(d2s(t,'\n'))
        # print t
        
    except Exception,e:
        print e

