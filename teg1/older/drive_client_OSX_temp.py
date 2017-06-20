"""

To run:
ssh pi@192.168.43.20
sudo python kzpy3/RPi3/RPi_server.py
python kzpy3/RPi3/osx_client.py

"""

from kzpy3.utils import *

import serial

ser = serial.Serial('/dev/tty.usbmodem1461',9600)#115200)#
#ser = serial.Serial('/dev/ttyACM0',9600)
#ser = serial.Serial('/dev/tty.usbmodem1411',9600)

STEER_MIN = 1096
STEER_MAX = 1872
THROTTLE_MIN = 1280
THROTTLE_MAX = 1600

def unpack_serial_data_as_tuple(ser_line):
    try:
        exec('t = '+ser_line)
        return t
    except Exception,e:
        print e
        print ' unpack_serial_data_as_tuple:invalid ser_line'
        return False

def validate_tuple_values(t):
    if STEER_MIN <= t[0] <= STEER_MAX:
        if  THROTTLE_MIN <= t[1] <= THROTTLE_MAX:
            return True
    return False

def get_steer(steer):
    steer -= STEER_MIN
    steer /= (1.0*(STEER_MAX-STEER_MIN))
    steer *= 180.0
    steer = int(steer)
    if steer < 0:
        steer = 0
    if steer > 180:
        steer = 180
    return steer
    
def get_throttle(throttle):
    throttle -= THROTTLE_MIN
    throttle /= (1.0*(THROTTLE_MAX-THROTTLE_MIN))
    throttle *= 180.0
    throttle = int(throttle)
    if throttle < 0:
        throttle = 0
    if throttle > 180:
        throttle = 180
    return throttle

ctr = 0
sent_t = time.time()
wait_t = 0.1
while True:
    try:
        ser_line = ser.readline()
        t = unpack_serial_data_as_tuple(ser_line)
        if validate_tuple_values(t):
            print t
            ser_str = d2s(get_steer(t[0]),get_throttle(t[1]),'\n')
            print ser_str
            ser.write(ser_str)
        else:
            print(d2s('invalid data:',t))
    except Exception,e:
        print e

        
