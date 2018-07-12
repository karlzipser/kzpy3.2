#!/usr/bin/env python
from kzpy3.utils2 import *
import threading

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





def _TACTIC_RC_controller_run_loop(D,P):
    print('_run_loop')
    time.sleep(0.1)
    D['arduino'].flushInput()
    time.sleep(0.1)
    D['arduino'].flushOutput()
    flush_seconds = 0.25
    flush_timer = Timer(flush_seconds)
    ctr_timer = Timer()
    print_timer = Timer(0.01)
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


P['USE_MSE'] = True

if 'Start Arduino threads...':
    baudrate = 115200
    timeout = 0.5
    Arduinos = assign_serial_connections(get_arduino_serial_connections(baudrate,timeout))
    print Arduinos.keys()

    if P['USE_MSE'] and 'MSE' in Arduinos.keys():
        Tactic_RC_controller = TACTIC_RC_controller(Arduinos['MSE'],P)
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
