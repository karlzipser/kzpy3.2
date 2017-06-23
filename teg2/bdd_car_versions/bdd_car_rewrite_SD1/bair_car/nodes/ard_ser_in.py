from kzpy3.utils2 import *


 

class DUMMY_SER():
    def __init__(self):
        pass
    def write(self):
        pass
dummy_ser = DUMMY_SER()

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
                elif ser_tuple[0] in ['acc','gyro','head']:
                    print(d2s('Port',ser.port,'is the IMU:',ser_str))
                    Arduinos['IMU'] = ser
                    break
                elif ser_tuple[0] in ['GPS2']:
                    print(d2s('Port',ser.port,'is the SIG:',ser_str))
                    Arduinos['SIG'] = ser
                    break
            except:
                pass
        else:
            print('Unable to identify port {0}'.format(ser.port))
            print('Is transmitter turned on?')
            print('Is MSE battery plugged in?')
            if 'SIG' not in Arduinos.keys():
                print"WARNING: 'SIG' not found, using dummy serial port"
                time.sleep(1)
                Arduinos['SIG'] = dummy_ser
            #M['Stop_Arduinos'] = True
    return Arduinos


