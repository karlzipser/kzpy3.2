#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)

baudrate = 115200
timeout = 0.1

if using_linux():
    arduino_serial_prefix = 'ttyACM'
elif using_osx():
    arduino_serial_prefix = 'tty.usbmodem141'
sers = []
ACM_ports = [opj('/dev', p) for p in os.listdir('/dev') if arduino_serial_prefix in p]
for ACM_port in ACM_ports:
    try:
        sers.append(serial.Serial(ACM_port, baudrate=baudrate, timeout=timeout))
        print('Opened {0}'.format(ACM_port))
    except:
        pass

timer = Timer(1)
long_timer = Timer(10)

ctr = 0
ctr2 = 0
for ser in sers:
    while not long_timer.check():
        #print 'a'
        if True:#timer.check():
            #print 'b'
            #ser.write(d2n("(",ctr,",",ctr+5000,",",ctr+10000,")"))
            ctr += 1

            read_str = ser.readline()

            cg(ctr2,') ',read_str)
    ctr2 += 1
    long_timer.reset()

