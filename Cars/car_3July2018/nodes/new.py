from kzpy3.utils2 import *
import threading

"""
This may be necessary:

    sudo chmod 666 /dev/ttyACM*

"""


P = {}
P['ABORT'] = False

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
            spd2s('Unable to identify port {0}'.format(ser.port))
    if 'MSE' not in Arduinos.keys():
        spd2s('MSE not found: Is transmitter turned on? Is MSE battery plugged in?')
        P['ABORT'] = True
    return Arduinos







def IMU_setup(Arduinos,P):
    pass

def IMU_run_loop(Arduinos,P):
    imu_dic = {}
    imu_dic['gyro'] = 'gyro_pub'
    imu_dic['acc'] = 'acc_pub'
    imu_dic['head'] = 'gyro_heading_pub'
    print_timer = Timer(0.001)
    Arduinos['IMU'].flushInput()
    while P['ABORT'] == False:
        try: 
            read_str = Arduinos['IMU'].readline()
            exec('imu_input = list({0})'.format(read_str))       
            m = imu_input[0]
            P[m] = imu_input[1:4]
            if True and m == 'acc' and print_timer.check():
                print (m,P[m])
                print_timer.reset()
            if False:
                P[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*P[m]))
        except Exception as e:
            pass



def SIG_setup(Arduinos,P):
    LED_signal = d2n('(10000)')
    Arduinos['SIG'].write(LED_signal)

def SIG_run_loop(Arduinos,P):
    Arduinos['SIG'].flushInput()
    while P['ABORT'] == False:
        try: 
            read_str = Arduinos['SIG'].readline()
        except Exception as e:
            pass









baudrate = 115200
timeout = 0.5
Arduinos = assign_serial_connections(get_arduino_serial_connections(baudrate,timeout))


if 'IMU' in Arduinos.keys():
    IMU_setup(Arduinos,P)
    def arduino_imu_thread():
        IMU_run_loop(Arduinos,P)
    threading.Thread(target=arduino_imu_thread).start()
else:
    spd2s("!!!!!!!!!! 'IMU' not in Arduinos[] !!!!!!!!!!!")



timer = Timer(5)
while not timer.check():
    pass
P['ABORT'] = True

"""
q = raw_input('')
while q not in ['q','Q']:
    q = raw_input('')
P['ABORT'] = True

print P['ABORT']
"""
P['ABORT'] = True
