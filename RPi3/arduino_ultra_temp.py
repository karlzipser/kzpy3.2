RPI = True
if RPI:
    import sys
    sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
import serial

ser = []
while True:
    print 'setup ser'
    buf = ''
    del ser
    
    if RPI:
        ser = serial.Serial('/dev/ttyACM0',9600)#,timeout=0.2)
    else:
        ser = serial.Serial('/dev/tty.usbmodem1421',9600)#,timeout=0.2)
    while True: #'Out of range' not in buf:
        try:
            buf = ser.readline()
            print ". "+buf
        except KeyboardInterrupt:
            sys.exit()
        except Exception, e:
            print(d2s(os.path.basename(sys.argv[0]),':',e))
    


