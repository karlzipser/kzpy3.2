from kzpy3.utils2 import *



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
    for ser in sers:
        for _ in xrange(100):
            try:
                ser_str = ser.readline()
                exec('ser_tuple = list({0})'.format(ser_str))
                if ser_tuple[0] in ['mse']:
                    print(d2s('Port',ser.port,'is the MSE:',ser_str))
                    Arduinos['MSE'] = ser
                    break
            except:
                pass
        else:
            print('Unable to identify port {0}'.format(ser.port))
            print('Is transmitter turned on?')
            print('Is MSE battery plugged in?')
            stop_ros()

    return Arduinos


