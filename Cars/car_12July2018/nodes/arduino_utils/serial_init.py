#!/usr/bin/env python
from kzpy3.utils2 import *

def get_arduino_serial_connections(baudrate, timeout):
    from sys import platform
    if platform == "linux" or platform == "linux2":
        arduino_serial_prefix = 'ttyACM'
    elif platform == "darwin":
        arduino_serial_prefix = 'tty.usbmodem141'
    else:
        spd2s('unknown system (not linux or osx)')
        assert False
    sers = []
    ACM_ports = [opj('/dev', p) for p in os.listdir('/dev') if arduino_serial_prefix in p]
    for ACM_port in ACM_ports:
        try:
            sers.append(serial.Serial(ACM_port, baudrate=baudrate, timeout=timeout))
            print('Opened {0}'.format(ACM_port))
        except:
            pass
    return sers

def assign_serial_connections(sers):
    Arduinos = {}
    for ser in sers:
        timer = Timer(6) # see that this is a good value
        for _ in xrange(100):
            if timer.check():
                continue
            try:
                ser_str = ser.readline()
                
                exec('ser_tuple = list({0})'.format(ser_str))
                if ser_tuple[0] in ['mse']:
                    print(d2s('Port',ser.port,'is the MSE:',ser_str))
                    if 'Keep this up to date...':
                        print("\tusing 'motor_servo_minimal_3July2018_test.ino'")
                    Arduinos['MSE'] = ser
                    break
                elif ser_tuple[0] in ['acc','gyro','head']:
                    print(d2s('Port',ser.port,'is the IMU:',ser_str))
                    if 'Keep this up to date...':
                        print("\tusing 'acc.ino'")
                    Arduinos['IMU'] = ser
                    break
                elif ser_tuple[0] in ['GPS2']:
                    print(d2s('Port',ser.port,'is the SIG:',ser_str))
                    if 'Keep this up to date...':
                        print("\tusing 'LED_arduino_LCR_13July2018b.ino'")
                    Arduinos['SIG'] = ser
                    break
            except:
                pass
        else:
            spd2s('Unable to identify port {0}'.format(ser.port))
    print 'Finished scanning serial ports.'
    if 'MSE' not in Arduinos.keys():
        spd2s('MSE not found: Is transmitter turned on? Is MSE battery plugged in?')
    return Arduinos






