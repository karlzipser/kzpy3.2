#!/usr/bin/env python
from kzpy3.utils2 import *
import threading

P = {}
P['SMOOTHING_PARAMETER_1'] = 0.75
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
def pwm_to_percent(null_pwm,current_pwm,max_pwm,min_pwm):
    current_pwm -= null_pwm
    max_pwm -= null_pwm
    min_pwm -= null_pwm
    if current_pwm >= 0:
        p = 99*(1.0 + current_pwm/max_pwm)/2.0
    else:
        p = 99*(1.0 - current_pwm/min_pwm)/2.0
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





def _TACTIC_RC_controller_run_loop(D,P):
    print('_TACTIC_RC_controller_run_loop')
    time.sleep(0.1)
    D['arduino'].flushInput()
    time.sleep(0.1)
    D['arduino'].flushOutput()
    flush_seconds = 0.25
    flush_timer = Timer(flush_seconds)
    ctr_timer = Timer()
    print_timer = Timer(1)
    while P['ABORT'] == False:
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.0001)
        try:
            if 'Read serial and translate to list...':
                read_str = D['arduino'].readline()
                if flush_timer.check():
                    D['arduino'].flushInput()
                    D['arduino'].flushOutput()
                    flush_timer.reset()
                exec('mse_input = list({0})'.format(read_str))       
                assert(mse_input[0]=='mse')
            if 'Unpack mse list...':
                D['button_pwm'] = mse_input[1]
                D['servo_pwm'] = mse_input[2]
                D['motor_pwm'] = mse_input[3]
                D['encoder'] = mse_input[4]
            if 'Deal with ctr and rate...':
                D['ctr'] += 1
                D['Hz'] = dp(D['ctr']/ctr_timer.time(),1)
                if ctr_timer.time() > 5:
                    if D['Hz'] < 30 or D['Hz'] > 100:
                        P['ABORT'] = True
                        spd2s("\nD['Hz'] =",D['Hz'])
            if 'Assign button...':
                bpwm = D['button_pwm']
                if np.abs(bpwm - 1900) < D['button_delta']:
                    bn = 1
                elif np.abs(bpwm - 1700) < D['button_delta']:
                    bn = 2
                elif np.abs(bpwm - 1424) < D['button_delta']:
                    bn = 3
                elif np.abs(bpwm - 870) < D['button_delta']:
                    bn = 4
                if D['button_number'] != bn:
                    D['button_timer'].reset()
                D['button_number'] = bn
                D['button_time'] = D['button_timer'].time()
            if print_timer.check():
                pprint(D)
                print_timer.reset()
        except Exception as e:
            print e
            pass            
    print 'end _TACTIC_RC_controller_run_loop.'
def TACTIC_RC_controller(arduino,P):
    D = {}
    D['ctr'] = 0
    D['button_delta'] = 50
    D['button_number'] = 0
    D['button_timer'] = Timer()
    D['arduino'] = arduino
    threading.Thread(target=_TACTIC_RC_controller_run_loop,args=[D,P]).start()
    return D

# python kzpy3/Cars/car_12July2018/nodes/tactic_controller.py


def _calibrate_run_loop(D,RC,P):
    print "_calibrate_run_loop"
    print_timer = Timer(0.1)
    D['calibrated'] = False
    while P['ABORT'] == False:
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.0001)
        if D['calibrated'] == True:
            D['servo_percent'] = pwm_to_percent(
                D['servo_pwm_null'],RC['servo_pwm'],D['servo_pwm_max'],D['servo_pwm_min'])
            D['motor_percent'] = pwm_to_percent(
                D['motor_pwm_null'],RC['motor_pwm'],D['motor_pwm_max'],D['motor_pwm_min'])
        if RC['button_number'] != 4:
            continue
        if RC['button_time'] < 0.1:
            D['calibrated'] = False
            D['servo_pwm_null'] = RC['servo_pwm']
            D['motor_pwm_null'] = RC['motor_pwm']
        elif RC['button_time'] < 1.0:
            s = P['SMOOTHING_PARAMETER_1']
            D['servo_pwm_null'] = (1.0-s)*RC['servo_pwm'] + s*D['servo_pwm_null']
            D['motor_pwm_null'] = (1.0-s)*RC['motor_pwm'] + s*D['motor_pwm_null']
            D['servo_pwm_min'] = D['servo_pwm_null']
            D['servo_pwm_max'] = D['servo_pwm_null']
            D['motor_pwm_min'] = D['motor_pwm_null']
            D['motor_pwm_max'] = D['motor_pwm_null']
        else:
            if D['servo_pwm_max'] < RC['servo_pwm']:
                D['servo_pwm_max'] = RC['servo_pwm']
            if D['servo_pwm_min'] > RC['servo_pwm']:
                D['servo_pwm_min'] = RC['servo_pwm']
            if D['motor_pwm_max'] < RC['motor_pwm']:
                D['motor_pwm_max'] = RC['motor_pwm']
            if D['motor_pwm_min'] > RC['motor_pwm']:
                D['motor_pwm_min'] = RC['motor_pwm']
            if D['servo_pwm_max'] - D['servo_pwm_min'] > 300:
                if D['motor_pwm_max'] - D['motor_pwm_min'] > 300:
                    D['calibrated'] = True
 
        if print_timer.check():
            pprint(D)
            print_timer.reset()           
    print 'end _calibrate_run_loop.'
def Calibration_Mode(rc_controller,P):
    D = {}
    threading.Thread(target=_calibrate_run_loop,args=[D,rc_controller,P]).start()
    return D




P['USE_MSE'] = True

if 'Start Arduino threads...':
    baudrate = 115200
    timeout = 0.5
    Arduinos = assign_serial_connections(get_arduino_serial_connections(baudrate,timeout))
    print Arduinos.keys()

    if P['USE_MSE'] and 'MSE' in Arduinos.keys():
        Tactic_RC_controller = TACTIC_RC_controller(Arduinos['MSE'],P)
        Calibration_mode = Calibration_Mode(Tactic_RC_controller,P)
    else:
        spd2s("!!!!!!!!!! 'MSE' not in Arduinos[] !!!!!!!!!!!")    



if 'Main loop...':
    print 'main loop'
    q = '_'
    while q not in ['q','Q']:
        q = raw_input('')
        if P['ABORT']:
            break
        time.sleep(0.1)
    P['ABORT'] = True
    print 'done.'
#    print "unix(opjh('kzpy3/kill_ros.sh'))"
#    unix(opjh('kzpy3/kill_ros.sh'))

#EOF
