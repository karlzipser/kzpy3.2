from kzpy3.utils2 import *
import threading

"""
This may be necessary:

    sudo chmod 666 /dev/ttyACM*

"""


P = {}
P['button_delta'] = 50
P['human'] = {}
P['network'] = {}

if 'These parameters can change at runtime...':
    P['ABORT'] = False
    P['PAUSE'] = False
    P['AGENT'] = 'human'
    P['SMOOTHING_PARAMETER_1'] = 0.99

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
        if P['PAUSE'] == True:
            time.sleep(0.1)
            continue
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
            pass






def pwm_to_percent(null_pwm,current_pwm,max_pwm,min_pwm):
    current_pwm -= null_pwm
    max_pwm -= null_pwm
    min_pwm -= null_pwm
    if current_pwm >= 0:
        p = int(99*(1.0 + current_pwm/max_pwm)/2.0)
    else:
        p = int(99*(1.0 - current_pwm/min_pwm)/2.0)
    if p > 99:
        p = 99
    if p < 0:
        p = 0      
    return p
def percent_to_pwm(percent,null_pwm,max_pwm,min_pwm):
    if percent >= 49:
        p = (percent-50)/50.0 * (max_pwm-null_pwm) + null_pwm
    else:
        p = (percent-50)/50.0 * (null_pwm-min_pwm) + null_pwm
    return p


def MSE_setup(Arduinos,P):
    P['mse'] = {}
    P['mse']['ctr'] = 0
    P['mse']['button_timer'] = Timer()
    P['mse']['button_number'] = 0
    P['mse']['servo_pwm_max'] = 0
    P['mse']['motor_pwm_max'] = 0
    P['mse']['servo_pwm_min'] = 99999
    P['mse']['motor_pwm_min'] = 99999
def MSE_run_loop(Arduinos,P):
    Arduinos['MSE'].flushInput()
    flush_seconds = 0.5
    flush_timer = Timer(flush_seconds)
    ctr_timer = Timer()
    while P['ABORT'] == False:
        if P['PAUSE'] == True:
            time.sleep(0.1)
            continue
        try:
            if 'Read serial and translate to list...':
                read_str = Arduinos['MSE'].readline()
                if flush_timer.check():
                    Arduinos['MSE'].flushInput()
                    flush_timer.reset()
                exec('mse_input = list({0})'.format(read_str))       
                assert(mse_input[0]=='mse')

            if 'Unpack mse list...':
                P['mse']['button_pwm'] = mse_input[1]
                P['mse']['servo_pwm'] = mse_input[2]
                P['mse']['motor_pwm'] = mse_input[3]
                P['mse']['encoder'] = mse_input[4]

            print('mse',P['mse'])

            if 'Deal with ctr and rate...':
                P['mse']['ctr'] += 1
                P['mse']['Hz'] = dp(P['mse']['ctr']/ctr_timer.time(),1)

            if 'Assign button...':
                bpwm = P['mse']['button_pwm']
                if np.abs(bpwm - 1900) < P['button_delta']:
                    bn = 1
                elif np.abs(bpwm - 1700) < P['button_delta']:
                    bn = 2
                elif np.abs(bpwm - 1424) < P['button_delta']:
                    bn = 3
                elif np.abs(bpwm - 870) < P['button_delta']:
                    bn = 4
                if P['mse']['button_number'] != bn:
                    P['mse']['button_timer'].reset()
                P['mse']['button_number'] = bn
                P['mse']['button_time'] = P['mse']['button_timer'].time()

            if 'Deal with button 4 calibration...':
                if P['mse']['button_number'] == 4:
                    if P['mse']['button_time'] < 1.0:
                        P['mse']['servo_pwm_null'] = P['mse']['servo_pwm'] # time averaging here
                        P['mse']['motor_pwm_null'] = P['mse']['motor_pwm']
                        P['mse']['servo_pwm_min'] = P['mse']['servo_pwm_null']
                        P['mse']['servo_pwm_max'] = P['mse']['servo_pwm_null']
                        P['mse']['motor_pwm_min'] = P['mse']['motor_pwm_null']
                        P['mse']['motor_pwm_max'] = P['mse']['motor_pwm_null']
                        P['human']['servo_pwm'] = P['mse']['servo_pwm_null']
                        P['human']['motor_pwm'] = P['mse']['motor_pwm_null']
                    else:
                        if P['mse']['servo_pwm_max'] < P['mse']['servo_pwm']:
                            P['mse']['servo_pwm_max'] = P['mse']['servo_pwm']
                        if P['mse']['servo_pwm_min'] > P['mse']['servo_pwm']:
                            P['mse']['servo_pwm_min'] = P['mse']['servo_pwm']
                        if P['mse']['motor_pwm_max'] < P['mse']['motor_pwm']:
                            P['mse']['motor_pwm_max'] = P['mse']['motor_pwm']
                        if P['mse']['motor_pwm_min'] > P['mse']['motor_pwm']:
                            P['mse']['motor_pwm_min'] = P['mse']['motor_pwm']


            if 'Deal with various agents...':
                if 'First null out non-current agent...':
                    for agent in ['human','network']:
                        if P['AGENT'] != agent:
                            P[agent]['servo_pwm'] = P['mse']['servo_pwm_null']
                            P[agent]['motor_pwm'] = P['mse']['motor_pwm_null']                   
                            P[agent]['servo_percent'] = 49
                            P[agent]['motor_percent'] = 49
                if 'Then process current agent...':
                    s = P['SMOOTHING_PARAMETER_1'] 
                    if P['AGENT'] == 'human':
                        if 'Do smoothing of pwms...':
                            P['human']['servo_pwm'] = (1.0-s)*P['mse']['servo_pwm'] + s*P['human']['servo_pwm']
                            P['human']['motor_pwm'] = (1.0-s)*P['mse']['motor_pwm'] + s*P['human']['motor_pwm']
                        if 'The smoothing carries to percents...':
                            P['human']['servo_percent'] = pwm_to_percent(
                                P['mse']['servo_pwm_null'],P['human']['servo_pwm'],P['mse']['servo_pwm_max'],P['mse']['servo_pwm_min'])
                            P['human']['motor_percent'] = pwm_to_percent(
                                P['mse']['motor_pwm_null'],P['human']['motor_pwm'],P['mse']['motor_pwm_max'],P['mse']['motor_pwm_min'])
                    else:
                        assert(P['AGENT']=='network')
                        P['network']['servo_percent'] = np.round((np.sin(P['mse']['button_time']/10.0)/2.0+0.5)*99)

                        P['network']['servo_percent'] = bound_value(P['network']['servo_percent'],5,94)
                        print P['network']['servo_percent']

                        P['network']['motor_percent'] = 59
                        P['network']['servo_pwm'] = percent_to_pwm(
                            P['network']['servo_percent'],P['mse']['servo_pwm_null'],P['mse']['servo_pwm_max'],P['mse']['servo_pwm_min'])
                        P['network']['motor_pwm'] = percent_to_pwm(
                            P['network']['motor_percent'],P['mse']['motor_pwm_null'],P['mse']['motor_pwm_max'],P['mse']['motor_pwm_min'])

            if 'Send servo/motor commands to Arduino...':
                write_str = d2n( '(', int(P[P['AGENT']]['servo_pwm']), ',', int(P[P['AGENT']]['motor_pwm']+10000), ')')
                if P['mse']['button_number'] != 4:
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
        if P['PAUSE'] == True:
            time.sleep(0.1)
            continue
        try:
            LED_signal = d2n('(',10000+P['mse']['button_number'],')')
            Arduinos['SIG'].write(LED_signal)
            read_str = Arduinos['SIG'].readline()
            print read_str
            if flush_timer.check():
                Arduinos['SIG'].flushInput()
                flush_timer.reset()   
        except Exception as e:
            pass








if 'Start Arduino threads...':
    baudrate = 115200
    timeout = 0.5
    Arduinos = assign_serial_connections(get_arduino_serial_connections(baudrate,timeout))

    if False:#'IMU' in Arduinos.keys():
        IMU_setup(Arduinos,P)
        threading.Thread(target=IMU_run_loop,args=[Arduinos,P]).start()
    else:
        spd2s("!!!!!!!!!! 'IMU' not in Arduinos[] !!!!!!!!!!!")

    if False:#'SIG' in Arduinos.keys():
        SIG_setup(Arduinos,P)
        threading.Thread(target=SIG_run_loop,args=[Arduinos,P]).start()
    else:
        spd2s("!!!!!!!!!! 'SIG' not in Arduinos[] !!!!!!!!!!!")

    if 'MSE' in Arduinos.keys():
        MSE_setup(Arduinos,P)
        threading.Thread(target=MSE_run_loop,args=[Arduinos,P]).start()
    else:
        spd2s("!!!!!!!!!! 'MSE' not in Arduinos[] !!!!!!!!!!!")






if 'Main loop...':
    q = '_'
    while q not in ['q','Q']:
        q = raw_input('')
        if q == ' ':
            if P['PAUSE'] == False:
                P['PAUSE'] = True
            else:
                P['PAUSE'] = False
        elif q == 'h':
            P['AGENT'] = 'human'
        elif q == 'n':
            P['AGENT'] = 'network'

    P['ABORT'] = True

    print 'done.'


#EOF
