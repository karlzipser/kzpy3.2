"""

To run:
ssh pi@192.168.43.20
sudo python kzpy3/RPi3/RPi_server.py
python kzpy3/RPi3/osx_client.py

"""

from kzpy3.utils import *
print os.path.basename(sys.argv[0])

import serial
ser = serial.Serial('/dev/tty.usbmodem1411',9600)

import socket, errno
host = '192.168.43.20'
#host = 'localhost'
port = 5000
clientsocket = False


SPEED_NEUTRAL = 540
SPEED_MAX = 261
SPEED_MIN = 621
STEER_NEUTRAL = 514
STEER_CW = 169
STEER_CCW = 865
def process_nums(a,NEUTRAL,MIN,MAX):
    if a < NEUTRAL:
        b = (a - MAX) / (1.0*(NEUTRAL - MAX))
        if b < 0:
            b = 0
        b = 1 - b
    else:
        b = (a - NEUTRAL) / (1.0*(MIN - NEUTRAL))
        if b < 0:
            b = 0
        b = -b
        if b < -1:
            b = -1
        if b > -0.01:
            b = 0
    b = int(100*b)
    return b
def decode_serial_string(s):
    s = s.replace('\t',' ')
    s = s.replace('\r\n',' ')
    n = s.split(' ')
    steer = process_nums(int(n[0]),STEER_NEUTRAL,STEER_CCW,STEER_CW)
    speed = process_nums(int(n[1]),SPEED_NEUTRAL,SPEED_MIN,SPEED_MAX)
    cruise = int(n[2])
    return (steer,speed,cruise)



sent_t = time.time()
wait_t = 0.1
while True:
    try:
        d = decode_serial_string(ser.readline())
        t = time.time()
        if t - sent_t > wait_t:
            sent_t = t
            if not clientsocket:
                clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientsocket.connect((host, port))
            clientsocket.send(d2s(d[0],d[1],d[2],'okay'))
            print d
    except KeyboardInterrupt:
        sys.exit()
    except IOError, e:
        if e.errno == errno.EPIPE:
            print(d2s(os.path.basename(sys.argv[0]),':',e))
            sys.exit()
        else:
            print(d2s(os.path.basename(sys.argv[0]),'::::',e))
    except Exception, e:
        print(d2s(os.path.basename(sys.argv[0]),':',e))
    


