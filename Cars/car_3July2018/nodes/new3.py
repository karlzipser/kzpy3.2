from kzpy3.utils2 import *
import threading

"""
This may be necessary:

    sudo chmod 666 /dev/ttyACM*

"""


P = {}
P['ABORT'] = False
P['AGENT'] = 'human'

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
        #P['ABORT'] = True
    return Arduinos







def IMU_setup(Arduinos,P):
    P['acc'] = {}
    P['gyro'] = {}
    P['head'] = {}
    for k in ['acc','gyro','head']:
        P[k]['ctr'] = 0
    pass
def IMU_run_loop(Arduinos,P):
    imu_dic = {}
    imu_dic['gyro'] = 'gyro_pub'
    imu_dic['acc'] = 'acc_pub'
    imu_dic['head'] = 'gyro_heading_pub'
    flush_seconds = 0.5
    flush_timer = Timer(flush_seconds)
    ctr_timer = Timer()
    Arduinos['IMU'].flushInput()

    while P['ABORT'] == False:
        try:       
            read_str = Arduinos['IMU'].readline()
            if flush_timer.check():
                Arduinos['IMU'].flushInput()
                flush_timer.reset()            
            exec('imu_input = list({0})'.format(read_str))       
            m = imu_input[0]
            assert(m in ['acc','gyro','head'])
            P[m]['x'] = imu_input[1]
            P[m]['y'] = imu_input[2]
            P[m]['z'] = imu_input[3]
            print (m,P[m])
            P[m]['ctr'] += 1
            P[m]['Hz'] = dp(P[m]['ctr']/ctr_timer.time(),1)
        
            if False:
                P[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*P[m]))
        except Exception as e:
            #print e
            pass


def MSE_setup(Arduinos,P):
    P['mse'] = {}
    P['mse']['ctr'] = 0
    pass
def MSE_run_loop(Arduinos,P):
    Arduinos['MSE'].flushInput()
    flush_seconds = 0.5
    flush_timer = Timer(flush_seconds)
    ctr_timer = Timer()
    while P['ABORT'] == False:
        try:        
            read_str = Arduinos['MSE'].readline()
            if flush_timer.check():
                Arduinos['MSE'].flushInput()
                flush_timer.reset()            
            exec('mse_input = list({0})'.format(read_str))       
            assert(mse_input[0]=='mse')
            P['mse']['button_pwm'] = mse_input[1]
            P['mse']['servo_pwm'] = mse_input[2]
            P['mse']['motor_pwm'] = mse_input[3]
            P['mse']['encoder'] = mse_input[4]
            print('mse',P['mse'])
            P['mse']['ctr'] += 1
            P['mse']['Hz'] = dp(P['mse']['ctr']/ctr_timer.time(),1)
            if False:
                P['mse_pub'].publish(geometry_msgs.msg.Vector3(*P[m]))
            if P['AGENT'] == 'human':
                write_str = d2n( '(', int(P['mse']['servo_pwm']), ',', int(P['mse']['motor_pwm']+10000), ')')
            #print write_str
            Arduinos['MSE'].write(write_str)
        except Exception as e:
            pass





def SIG_setup(Arduinos,P):
    LED_signal = d2n('(10000)')
    Arduinos['SIG'].write(LED_signal)
def SIG_run_loop(Arduinos,P):
    Arduinos['SIG'].flushInput()
    flush_seconds = 0.5
    flush_timer = Timer(flush_seconds)
    while P['ABORT'] == False:
        try: 
            read_str = Arduinos['SIG'].readline()
            print read_str
            if flush_timer.check():
                Arduinos['SIG'].flushInput()
                flush_timer.reset()   
        except Exception as e:
            pass









baudrate = 115200
timeout = 0.5
Arduinos = assign_serial_connections(get_arduino_serial_connections(baudrate,timeout))



if 'IMU' in Arduinos.keys():
    IMU_setup(Arduinos,P)
    threading.Thread(target=IMU_run_loop,args=[Arduinos,P]).start()
else:
    spd2s("!!!!!!!!!! 'IMU' not in Arduinos[] !!!!!!!!!!!")

if 'SIG' in Arduinos.keys():
    SIG_setup(Arduinos,P)
    threading.Thread(target=SIG_run_loop,args=[Arduinos,P]).start()
else:
    spd2s("!!!!!!!!!! 'SIG' not in Arduinos[] !!!!!!!!!!!")

if 'MSE' in Arduinos.keys():
    MSE_setup(Arduinos,P)
    threading.Thread(target=MSE_run_loop,args=[Arduinos,P]).start()
else:
    spd2s("!!!!!!!!!! 'MSE' not in Arduinos[] !!!!!!!!!!!")


"""
n_seconds = 1.0
timer = Timer(n_seconds)

while not timer.check():
    time.sleep(0.2)
P['ABORT'] = True
"""


q = raw_input('')
while q not in ['q','Q']:
    q = raw_input('')
P['ABORT'] = True

print 'done.'


#EOF