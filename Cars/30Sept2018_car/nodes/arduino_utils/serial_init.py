#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)
from Default_values.arduino.default_values import flex_names
import rospy

def get_arduino_serial_connections(baudrate, timeout):
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
    return sers

def assign_serial_connections(P,sers):
    ctr = 0
    P['Arduinos'] = {}
    P['Arduinos']['SIG/write'] = -11119
    for ser in sers:
        for _ in xrange(100000):
            try:
                ser_str = ser.readline()
                print ctr,ser_str
                ctr += 1
                exec('ser_tuple = list({0})'.format(ser_str))
                if ser_tuple[0] in ['mse']:
                    spd2s('Port',ser.port,'is the MSE:',ser_str)
                    CS("\tusing 'motor_servo_encoder.ino'",exception=True)
                    P['Arduinos']['MSE'] = ser
                    break
                elif ser_tuple[0] in ['sound']:
                    print(d2s('Port',ser.port,'is the SOUND:',ser_str))
                    print("\tusing '?.ino'")
                    P['Arduinos']['SOUND'] = ser
                    break     
                else:
                    continue               
                """
                elif ser_tuple[0] in ['acc','gyro','head']:
                    print(d2s('Port',ser.port,'is the IMU:',ser_str))
                    print("\tusing 'acc.ino'")
                    P['Arduinos']['IMU'] = ser
                    break
                elif ser_tuple[0] in ['GPS3']:
                    print(d2s('Port',ser.port,'is the SIG:',ser_str))
                    print("\tusing 'LED2_GPS3.ino'")
                    P['Arduinos']['SIG'] = ser
                    break
                #################
                #
                elif ser_tuple[0] in flex_names:
                    print(d2s('Port',ser.port,'is the FLEX:',ser_str))
                    print("\tusing 'Flex_Sensors_0_12Sept2018.ino'")
                    P['Arduinos']['FLEX'] = ser
                    break
                #
                #################
                """


            except:
                pass
        else:
            CS_('Unable to identify port {0}'.format(ser.port))
    print 'Finished scanning serial ports.'
    if 'MSE' not in P['Arduinos'].keys():
        spd2s('MSE not found: Is transmitter turned on? Is MSE battery plugged in?')
    #return Arduinos

#EOF
