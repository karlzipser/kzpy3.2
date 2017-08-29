from kzpy3.utils2 import *

import runtime_parameters as rp
# original

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
    Arduinos = {}
    ser_timer = Timer(5)
    while not ('MSE' in Arduinos and ser_timer.check()) or not len(sers) == 0:
        if ser_timer.check():
            spd2s('Looking for Arduinos . . .')
            ser_timer.reset()
        for ser in sers:
            try:
                ser_str = ser.readline()
                exec('ser_tuple = list({0})'.format(ser_str))
                if ser_tuple[0] in ['mse']:
                    spd2s('Port',ser.port,'is the MSE:',ser_str,ser_timer.time())
                    Arduinos['MSE'] = ser
                    sers.remove(ser)
                    break
                elif ser_tuple[0] in ['acc','gyro','head']:
                    spd2s('Port',ser.port,'is the IMU:',ser_str,ser_timer.time())
                    Arduinos['IMU'] = ser
                    sers.remove(ser)
                    break
                elif ser_tuple[0] in ['GPS2']:
                    spd2s('Port',ser.port,'is the SIG:',ser_str,ser_timer.time())
                    Arduinos['SIG'] = ser
                    sers.remove(ser)
                    break
            except:
                pass
        time.sleep(0.1)
    spd2s('Done looking for Arduinos.')
    if rp.require_Arudinos_MSE:
        if 'MSE' not in Arduinos:
            srpd2s('Fatal error\nArduino MSE not found!',
                #'\nUnable to identify port {0}'.format(ser.port),
                '\nIs transmitter turned on?',
                '\nIs MSE battery plugged in?')
            stop_ros()
    else:
        spd2s('Using dummy Arduino MSE.')
        Arduinos['MSE'] = 'Dummy MSE'

    return Arduinos


