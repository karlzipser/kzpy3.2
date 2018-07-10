#!/usr/bin/env python


from kzpy3.utils2 import *
import threading
import std_msgs.msg
import geometry_msgs.msg
import rospy
"""
This may be necessary to access Arduinos when first starting:

    sudo chmod 666 /dev/ttyACM*

node files need to be made executable with chmod, e.g., chmod a+x *.py

"""


P = {}
P['button_delta'] = 50
P['human'] = {}
P['network'] = {}
P['calibrated'] = False

if 'These parameters can change at runtime...':
    P['ABORT'] = False
    P['PAUSE'] = False
    P['AGENT'] = 'human'
    P['SMOOTHING_PARAMETER_1'] = 0.75
    P['BEHAVIORAL_MODE'] = 'direct'




P['human_agent_pub'] = rospy.Publisher('human_agent', std_msgs.msg.Int32, queue_size=5) 
P['behavioral_mode_pub'] = rospy.Publisher('behavioral_mode', std_msgs.msg.String, queue_size=5)
P['button_number_pub'] = rospy.Publisher('button_number', std_msgs.msg.Int32, queue_size=5) 
P['steer_pub'] = rospy.Publisher('steer', std_msgs.msg.Int32, queue_size=5) 
P['motor_pub'] = rospy.Publisher('motor', std_msgs.msg.Int32, queue_size=5) 
P['encoder_pub'] = rospy.Publisher('encoder', std_msgs.msg.Float32, queue_size=5)
P['gyro_pub'] = rospy.Publisher('gyro', geometry_msgs.msg.Vector3, queue_size=100)
P['gyro_heading_pub'] = rospy.Publisher('gyro_heading', geometry_msgs.msg.Vector3, queue_size=100)
P['acc_pub'] = rospy.Publisher('acc', geometry_msgs.msg.Vector3, queue_size=100)





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
                        print("\tusing 'LED_arduino_LCR_8July2018b.ino'")
                    Arduinos['SIG'] = ser
                    break
            except:
                pass
        else:
            spd2s('Unable to identify port {0}'.format(ser.port))
    print 'Finished scanning serial ports.'
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
    print 'IMU_setup'
    pass
def IMU_run_loop(Arduinos,P):
    print 'IMU_run_loop'
    imu_dic = {}
    imu_dic['gyro'] = 'gyro_pub'
    imu_dic['acc'] = 'acc_pub'
    imu_dic['head'] = 'gyro_heading_pub'
    flush_seconds = 0.5
    flush_timer = Timer(flush_seconds)
    time.sleep(0.1)
    Arduinos['IMU'].flushInput()
    time.sleep(0.1)
    Arduinos['IMU'].flushOutput()
    ctr_timer = Timer()
    while P['ABORT'] == False:
        if P['PAUSE'] == True:
            time.sleep(0.1)
            continue
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.0001)
        try:
            read_str = Arduinos['IMU'].readline()
            if flush_timer.check():
                Arduinos['IMU'].flushInput()
                flush_timer.reset()            
            exec('imu_input = list({0})'.format(read_str))       
            m = imu_input[0]
            assert(m in ['acc','gyro','head'])
            if False:
                P[m]['x'] = imu_input[1]
                P[m]['y'] = imu_input[2]
                P[m]['z'] = imu_input[3]
            P[m]['xyz'] = imu_input[1:4]
            #print (m,P[m])
            #if m == 'acc':
            #    print (m,P[m])
            P[m]['ctr'] += 1
            P[m]['Hz'] = dp(P[m]['ctr']/ctr_timer.time(),1)
            if ctr_timer.time() > 5:
                if P[m]['Hz'] < 60 or P[m]['Hz'] > 100:
                    P['ABORT'] = True
                    spd2s("\nP[",m,"]['Hz'] =",P[m]['Hz'])
            if True:
                P[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*P[m]))
        except Exception as e:
            pass
    print 'end IMU_run_loop.'














def Printer_setup(P):
    pass
def Printer_run_loop(P):
    while P['ABORT'] == False:
        if P['PAUSE'] == True:
            time.sleep(0.1)
            continue
        #print 'Printer_run_loop'
        if True:     
            #m = 'acc'
            for m in ['acc',P['AGENT']]:
                print (m,P[m])#,'mse',P['mse']['Hz'])
            time.sleep(10/10.0)
        else:#except Exception as e:
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
    time.sleep(0.1)
    Arduinos['MSE'].flushInput()
    time.sleep(0.1)
    Arduinos['MSE'].flushOutput()
    flush_seconds = 0.25
    flush_timer = Timer(flush_seconds)
    ctr_timer = Timer()
    while P['ABORT'] == False:
        if P['PAUSE'] == True:
            time.sleep(0.1)
            continue
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.0001)
        try:
            if 'Read serial and translate to list...':
                read_str = Arduinos['MSE'].readline()
                if flush_timer.check():
                    Arduinos['MSE'].flushInput()
                    Arduinos['MSE'].flushOutput()
                    flush_timer.reset()
                exec('mse_input = list({0})'.format(read_str))       
                assert(mse_input[0]=='mse')

            if 'Unpack mse list...':
                P['mse']['button_pwm'] = mse_input[1]
                P['mse']['servo_pwm'] = mse_input[2]
                P['mse']['motor_pwm'] = mse_input[3]
                P['mse']['encoder'] = mse_input[4]

            if 'Deal with ctr and rate...':
                P['mse']['ctr'] += 1
                P['mse']['Hz'] = dp(P['mse']['ctr']/ctr_timer.time(),1)
                if ctr_timer.time() > 5:
                    if P['mse']['Hz'] < 30 or P['mse']['Hz'] > 100:
                        P['ABORT'] = True
                        spd2s("\nP[mse]['Hz'] =",P['mse']['Hz'])

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
                    if P['mse']['button_time'] < 0.1:
                        P['calibrated'] = False
                        P['mse']['servo_pwm_null'] = P['mse']['servo_pwm']
                        P['mse']['motor_pwm_null'] = P['mse']['motor_pwm']
                    elif P['mse']['button_time'] < 1.0:
                        s = P['SMOOTHING_PARAMETER_1']
                        P['mse']['servo_pwm_null'] = (1.0-s)*P['mse']['servo_pwm'] + s*P['mse']['servo_pwm_null']
                        P['mse']['motor_pwm_null'] = (1.0-s)*P['mse']['motor_pwm'] + s*P['mse']['motor_pwm_null']
                        P['mse']['servo_pwm_min'] = P['mse']['servo_pwm_null']
                        P['mse']['servo_pwm_max'] = P['mse']['servo_pwm_null']
                        P['mse']['motor_pwm_min'] = P['mse']['motor_pwm_null']
                        P['mse']['motor_pwm_max'] = P['mse']['motor_pwm_null']
                        P['human']['servo_pwm'] = P['mse']['servo_pwm_null']
                        P['human']['motor_pwm'] = P['mse']['motor_pwm_null']
                        P['network']['servo_percent'] = 49
                        P['network']['motor_percent'] = 49
                    else:
                        if P['mse']['servo_pwm_max'] < P['mse']['servo_pwm']:
                            P['mse']['servo_pwm_max'] = P['mse']['servo_pwm']
                        if P['mse']['servo_pwm_min'] > P['mse']['servo_pwm']:
                            P['mse']['servo_pwm_min'] = P['mse']['servo_pwm']
                        if P['mse']['motor_pwm_max'] < P['mse']['motor_pwm']:
                            P['mse']['motor_pwm_max'] = P['mse']['motor_pwm']
                        if P['mse']['motor_pwm_min'] > P['mse']['motor_pwm']:
                            P['mse']['motor_pwm_min'] = P['mse']['motor_pwm']
                        if P['mse']['servo_pwm_max'] - P['mse']['servo_pwm_min'] > 300:
                            if P['mse']['motor_pwm_max'] - P['mse']['motor_pwm_min'] > 300:
                                P['calibrated'] = True

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
                        if 'Deal with smoothing of percentages, then translate to pwms...':

                            P['network']['servo_percent'] = (1.0-s)*np.round((np.cos(P['mse']['button_time']/10.0)/2.0+0.5)*99) + s*P['network']['servo_percent']
                            P['network']['servo_percent'] = bound_value(P['network']['servo_percent'],5,94)
                            P['network']['motor_percent'] = (1.0-s)*56 + s*P['network']['motor_percent']
                            P['network']['servo_pwm'] = percent_to_pwm(
                                P['network']['servo_percent'],P['mse']['servo_pwm_null'],P['mse']['servo_pwm_max'],P['mse']['servo_pwm_min'])
                            P['network']['motor_pwm'] = percent_to_pwm(
                                P['network']['motor_percent'],P['mse']['motor_pwm_null'],P['mse']['motor_pwm_max'],P['mse']['motor_pwm_min'])

            if 'Send servo/motor commands to Arduino...':
                write_str = d2n( '(', int(P[P['AGENT']]['servo_pwm']), ',', int(P[P['AGENT']]['motor_pwm']+10000), ')')
                if P['mse']['button_number'] != 4:
                    if P['calibrated']:
                        Arduinos['MSE'].write(write_str)
            if P['AGENT'] == 'human':
                human_val = 1
            else:
                human_val = 0
            P['human_agent_pub'].publish(std_msgs.msg.Int32(human_val))            
            P['steer_pub'].publish(std_msgs.msg.Int32(P['human']['servo_percent']))
            P['motor_pub'].publish(std_msgs.msg.Int32(P['human']['motor_percent']))
            P['button_number_pub'].publish(std_msgs.msg.Int32(P['mse']['button_number']))
            P['behavioral_mode_pub'].publish(P['BEHAVIORAL_MODE'])
            P['encoder_pub'].publish(std_msgs.msg.Float32(P['mse']['encoder']))

        except Exception as e:
            pass
    print 'end MSE_run_loop.'
















LED_yellow_line = '(10005)'
LED_red_X = '(10108)'

def SIG_setup(Arduinos,P):
    Arduinos['SIG'].write(LED_yellow_line)
def SIG_run_loop(Arduinos,P):
    time.sleep(0.1)
    Arduinos['SIG'].flushInput()
    time.sleep(0.1)
    Arduinos['SIG'].flushOutput()
    flush_seconds = 0.5
    flush_timer = Timer(flush_seconds)
    while P['ABORT'] == False:
        if P['PAUSE'] == True:
            time.sleep(0.1)
            continue
        if 'This brief sleep to allows other threads to process; without this other threads run much too slowly...':
            time.sleep(0.0001)
        try:

            led_num = 10000

            if P['AGENT'] == 'human':
                led_num += 100
            else:
                assert P['AGENT'] == 'network'
                led_num += 200

            if P['mse']['button_number'] == 4:
                button_offset = 4
            else:
                if P['BEHAVIORAL_MODE'] == 'direct':
                    offset = 0
                elif P['BEHAVIORAL_MODE'] == 'follow':
                    offset = 10
                elif P['BEHAVIORAL_MODE'] == 'furtive':
                    offset = 20
                elif P['BEHAVIORAL_MODE'] == 'play':
                    offset = 30

                led_num += offset

                if P['mse']['button_number'] == 1:
                    button_offset = 2
                elif P['mse']['button_number'] == 2:
                    button_offset = 1
                elif P['mse']['button_number'] == 3:
                    button_offset = 3


            led_num += button_offset

            LED_signal = d2s('(',led_num,')')
            if P['calibrated'] or P['mse']['button_number'] == 4:
                Arduinos['SIG'].write(LED_signal)
            else:
                Arduinos['SIG'].write(LED_yellow_line)
            read_str = Arduinos['SIG'].readline()
            if flush_timer.check():
                Arduinos['SIG'].flushInput()
                Arduinos['SIG'].flushOutput()
                flush_timer.reset()
        except Exception as e:
            pass
    Arduinos['SIG'].write(LED_red_X)
    print 'end SIG_run_loop.'












"""

P['USE_SIG'] = True
P['USE_IMU'] = True
P['USE_MSE'] = True
P['USE_PRINTER'] = True

if 'Start Arduino threads...':
    baudrate = 115200
    timeout = 0.5
    Arduinos = assign_serial_connections(get_arduino_serial_connections(baudrate,timeout))
    print 'here'
    print Arduinos.keys()
    if P['USE_IMU'] and 'IMU' in Arduinos.keys():
        IMU_setup(Arduinos,P)
        threading.Thread(target=IMU_run_loop,args=[Arduinos,P]).start()
    else:
        spd2s("!!!!!!!!!! 'IMU' not in Arduinos[] !!!!!!!!!!!")
    
    if P['USE_SIG'] and 'SIG' in Arduinos.keys():
        SIG_setup(Arduinos,P)
        threading.Thread(target=SIG_run_loop,args=[Arduinos,P]).start()
    else:
        spd2s("!!!!!!!!!! 'SIG' not in Arduinos[] !!!!!!!!!!!")
    
    if P['USE_MSE'] and 'MSE' in Arduinos.keys():
        MSE_setup(Arduinos,P)
        threading.Thread(target=MSE_run_loop,args=[Arduinos,P]).start()
    else:
        spd2s("!!!!!!!!!! 'MSE' not in Arduinos[] !!!!!!!!!!!")
    
    
    
    if P['USE_PRINTER']:
        Printer_setup(P)
        threading.Thread(target=Printer_run_loop,args=[P]).start()
    






# put in tests for rate controls



if 'Main loop...':
    print 'main loop'
    q = '_'
    while q not in ['q','Q']:
        if P['ABORT']:
            break
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
        elif q == 'd':
            P['BEHAVIORAL_MODE'] = 'direct'
        elif q == 'f':
            P['BEHAVIORAL_MODE'] = 'follow'
        elif q == 'r':
            P['BEHAVIORAL_MODE'] = 'furtive'
        elif q == 'p':
            P['BEHAVIORAL_MODE'] = 'play'


    P['ABORT'] = True

    print 'done.'
    print "unix(opjh('kzpy3/kill_ros.sh'))"
    unix(opjh('kzpy3/kill_ros.sh'))
"""
#EOF
