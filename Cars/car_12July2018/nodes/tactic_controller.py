#!/usr/bin/env python
from kzpy3.utils2 import *
from arduino_utils import *
import threading

P = {}
P['calibrated'] = False
P['SMOOTHING_PARAMETER_1'] = 0.75
P['ABORT'] = False
#P['selector_mode'] = 'drive'







"""
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
        #if P['PAUSE'] == True:
        #    time.sleep(0.1)
        #    continue
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








def TACTIC_RC_controller(arduino,P):
    D = {}
    D['ctr'] = 0
    D['button_delta'] = 50
    D['button_number'] = 0
    D['button_timer'] = Timer()
    D['arduino'] = arduino
    threading.Thread(target=_TACTIC_RC_controller_run_loop,args=[D,P]).start()
    return D
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

            if P['calibrated'] == True:
                P['servo_percent'] = pwm_to_percent(
                    P['servo_pwm_null'],D['servo_pwm'],P['servo_pwm_max'],P['servo_pwm_min'])
                P['motor_percent'] = pwm_to_percent(
                    P['motor_pwm_null'],D['motor_pwm'],P['motor_pwm_max'],P['motor_pwm_min'])
            # ros publish here
            if print_timer.check():
                pprint(P)
                pprint(D)
                print_timer.reset()
        except Exception as e:
            print e
            pass            
    print 'end _TACTIC_RC_controller_run_loop.'


# python kzpy3/Cars/car_12July2018/nodes/tactic_controller.py




def Calibration_Mode(rc_controller,P):
    D = {}
    threading.Thread(target=_calibrate_run_loop,args=[D,rc_controller,P]).start()
    return D
def _calibrate_run_loop(D,RC,P):
    print "_calibrate_run_loop"
    print_timer = Timer(0.1)
    P['calibrated'] = False
    while P['ABORT'] == False:
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.0001)
        if RC['button_number'] != 4:
            time.sleep(0.001)
            continue
        if RC['button_time'] < 5.0:
            time.sleep(0.001)
            continue
        if True:
            if RC['button_time'] < 5.1:
                P['calibrated'] = False
                P['servo_pwm_null'] = RC['servo_pwm']
                P['motor_pwm_null'] = RC['motor_pwm']
            elif RC['button_time'] < 6.0:
                s = P['SMOOTHING_PARAMETER_1']
                P['servo_pwm_null'] = (1.0-s)*RC['servo_pwm'] + s*P['servo_pwm_null']
                P['motor_pwm_null'] = (1.0-s)*RC['motor_pwm'] + s*P['motor_pwm_null']
                P['servo_pwm_min'] = P['servo_pwm_null']
                P['servo_pwm_max'] = P['servo_pwm_null']
                P['motor_pwm_min'] = P['motor_pwm_null']
                P['motor_pwm_max'] = P['motor_pwm_null']
            else:
                if P['servo_pwm_max'] < RC['servo_pwm']:
                    P['servo_pwm_max'] = RC['servo_pwm']
                if P['servo_pwm_min'] > RC['servo_pwm']:
                    P['servo_pwm_min'] = RC['servo_pwm']
                if P['motor_pwm_max'] < RC['motor_pwm']:
                    P['motor_pwm_max'] = RC['motor_pwm']
                if P['motor_pwm_min'] > RC['motor_pwm']:
                    P['motor_pwm_min'] = RC['motor_pwm']
                if P['servo_pwm_max'] - P['servo_pwm_min'] > 300:
                    if P['motor_pwm_max'] - P['motor_pwm_min'] > 300:
                        P['calibrated'] = True
        if print_timer.check():
            pprint(P)
            print_timer.reset()           
    print 'end _calibrate_run_loop.'


A = {
    'behavioral_mode':{
        'direct':   {'button':1,'min':20,'max':60,'led':1},
        'follow':   {'button':1,'min':0,'max':40,'led':2},
        'furtive':  {'button':1,'min':60,'max':80,'led':3},
        'play':     {'button':1,'min':80,'max':100,'led':4}
        },
    'agent':{
        'human':    {'button':2,'min':40,'max':100,'led':6*100},
        'network':  {'button':2,'min':0,'max':40,'led':7*100}
        },
    'place':{
        'local':    {'button':3,'min':40,'max':60,'led':8},
        'home':     {'button':3,'min':20,'max':40,'led':9},
        'Tilden':   {'button':3,'min':0,'max':20,'led':10},
        'campus':   {'button':3,'min':60,'max':80,'led':11},
        'arena':    {'button':3,'min':80,'max':100,'led':12},
        'other':    {'button':3,'min':80,'max':100,'led':13}
        }   
    }


def Selector_Mode(RC,P):
    D = {}
    for theme in A.keys():
        P[theme] = False
    threading.Thread(target=_selector_run_loop,args=[D,RC,P]).start()
    return D
def _selector_run_loop(D,RC,P):
    print "_selector_run_loop"
    print_timer = Timer(0.25)
    while P['ABORT'] == False:
        #print "_selector_run_loop"
        try:
            if 'Brief sleep to allow other threads to process...':
                time.sleep(0.0001)
            if RC['button_number'] == 4:
                #print 'a'
                if RC['button_time'] < 3.0:
                    #print 'b'
                    if P['servo_percent'] < 10:
                        #print 'c'
                        P['selector_mode'] = 'drive_mode'
                        spd2s("P['selector_mode'] = 'drive_mode'")
                        time.sleep(0.001)
                    elif P['servo_percent'] > 90:
                        #print 'd'
                        P['selector_mode'] = 'menu_mode'
                        spd2s("P['selector_mode'] = 'menu_mode'")
                        time.sleep(0.001)
            elif P['selector_mode'] == 'menu_mode':
                for theme in A.keys():
                    if P[theme] == False:
                        for kind in A[theme].keys():
                            if RC['button_number'] == A[theme][kind]['button']:
                                if P['servo_percent']>A[theme][kind]['min'] and P['servo_percent']<A[theme][kind]['max']:
                                    if P['motor_percent'] > 80:
                                        if print_timer.check():
                                            pd2s(kind,'selected')
                                            print_timer.reset()
                                        P[theme] = kind
                                    else:
                                        if print_timer.check():
                                            print(kind)
                                            print_timer.reset()
                    else:
                        a_kind = a_key(A[theme])
                        if RC['button_number'] == A[theme][a_kind]['button']:
                            if P['motor_percent'] < 20:
                                P[theme] = False
                if print_timer.check():
                    pprint(P)
                    print_timer.reset()
        except:
            pass        
    print 'end _calibrate_run_loop.'







P['USE_MSE'] = True
P['USE_SIG'] = False

if 'Start Arduino threads...':
    baudrate = 115200
    timeout = 0.5
    Arduinos = assign_serial_connections(get_arduino_serial_connections(baudrate,timeout))
    print Arduinos.keys()

    if P['USE_MSE'] and 'MSE' in Arduinos.keys():
        Tactic_RC_controller = TACTIC_RC_controller(Arduinos['MSE'],P)
        Calibration_mode = Calibration_Mode(Tactic_RC_controller,P)
        Selector_mode = Selector_Mode(Tactic_RC_controller,P)
    else:
        spd2s("!!!!!!!!!! 'MSE' not in Arduinos[] !!!!!!!!!!!")    
    if P['USE_SIG'] and 'SIG' in Arduinos.keys():
        SIG_setup(Arduinos,P)
        threading.Thread(target=SIG_run_loop,args=[Arduinos,P]).start()
    else:
        spd2s("!!!!!!!!!! 'SIG' not in Arduinos[] !!!!!!!!!!!")



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
