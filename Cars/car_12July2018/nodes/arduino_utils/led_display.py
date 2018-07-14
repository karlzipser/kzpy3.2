from kzpy3.utils2 import *
import threading

def LED_Display(arduino,P):
    D = {}
    D['ctr'] = 0
    D['button_delta'] = 50
    D['button_number'] = 0
    D['button_timer'] = Timer()
    D['arduino'] = arduino
    if 'Initial values...':
        P['servo_pwm_smooth'] = 1000
        P['motor_pwm_smooth'] = 1000
        P['selector_mode'] = False
    threading.Thread(target=_LED_Display_run_loop,args=[D,P]).start()
    return D
    
def _LED_Display_run_loop(D,P):
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
            if 'Do smoothing...':
                s = P['SMOOTHING_PARAMETER_1']
                P['servo_pwm_smooth'] = (1.0-s)*D['servo_pwm'] + s*P['servo_pwm_smooth']
                P['motor_pwm_smooth'] = (1.0-s)*D['motor_pwm'] + s*P['motor_pwm_smooth']

            if 'Send servo/motor commands to Arduino...':
                write_str = d2n( '(', int(P['servo_pwm_smooth']), ',', int(P['motor_pwm_smooth']+10000), ')')
                if D['button_number'] != 4:
                    if P['calibrated']:
                        if P['selector_mode'] == 'drive_mode':
                            D['arduino'].write(write_str)
            # ros publish here
            if print_timer.check():
                pprint(P)
                pprint(D)
                print_timer.reset()
        except Exception as e:
            print e
            pass            
    print 'end _TACTIC_RC_controller_run_loop.'

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
