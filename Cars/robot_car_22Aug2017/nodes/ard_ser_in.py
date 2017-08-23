from kzpy3.utils2 import *

import runtime_parameters as rp


def get_arduino_serial_connections(baudrate, timeout):
    sers = []
    ACM_ports = [os.path.join('/dev', p) for p in os.listdir('/dev') if 'ttyACM' in p]
    for ACM_port in ACM_ports:
        try:
            sers.append(serial.Serial(ACM_port, baudrate=baudrate, timeout=timeout))
            print('Opened {0}'.format(ACM_port))
        except:
            pass
    return sers

def assign_serial_connections(sers):
    spd2s('Looking for Arduinos . . .')
    Arduinos = {}
    ser_timer = Timer(30)
    while not ser_timer.check() or not len(sers) == 0:
        for ser in sers:
            try:
                ser_str = ser.readline()
                exec('ser_tuple = list({0})'.format(ser_str))
                if ser_tuple[0] in ['mse']:
                    print(d2s('Port',ser.port,'is the MSE:',ser_str))
                    Arduinos['MSE'] = ser
                    sers.remove(ser)
                    break
                elif ser_tuple[0] in ['acc','gyro','head']:
                    print(d2s('Port',ser.port,'is the IMU:',ser_str))
                    Arduinos['IMU'] = ser
                    sers.remove(ser)
                    break
                elif ser_tuple[0] in ['GPS2']:
                    print(d2s('Port',ser.port,'is the SIG:',ser_str))
                    Arduinos['SIG'] = ser
                    sers.remove(ser)
                    break
            except:
                pass
    if rp.require_Arudinos_MSE:
        if 'MSE' not in Arduinos:
            srpd2s('Fatal error\nArduino MSE not found!',
                '\nUnable to identify port {0}'.format(ser.port),
                '\nIs transmitter turned on?',
                '\nIs MSE battery plugged in?')
            stop_ros()

    return Arduinos


