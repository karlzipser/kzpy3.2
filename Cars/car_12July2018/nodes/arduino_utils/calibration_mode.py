from kzpy3.utils2 import *
import threading

def Calibration_Mode(rc_controller,P):
    D = {}
    threading.Thread(target=_calibrate_run_loop,args=[D,rc_controller,P]).start()
    return D
def _calibrate_run_loop(D,RC,P):
    print "_calibrate_run_loop"
    print_timer = Timer(0.1)
    P['calibrated'] = False
    frequency_timer = Timer(1)
    while P['ABORT'] == False:
        frequency_timer.freq(name='_calibrate_run_loop')
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.02)
        if RC['button_number'] != 4:
            time.sleep(0.1)
            continue
        if RC['button_time'] < P['CALIBRATION_NULL_START_TIME']:
            time.sleep(0.01)
            continue
        if True:
            if RC['button_time'] < P['CALIBRATION_NULL_START_TIME']+0.1:
                P['calibrated'] = False
                P['servo_pwm_null'] = RC['servo_pwm']
                P['motor_pwm_null'] = RC['motor_pwm']
            elif RC['button_time'] < P['CALIBRATION_START_TIME']:
                s = P['SMOOTHING_PARAMETER_1']
                P['servo_pwm_null'] = (1.0-s)*RC['servo_pwm'] + s*P['servo_pwm_null']
                P['motor_pwm_null'] = (1.0-s)*RC['motor_pwm'] + s*P['motor_pwm_null']
                P['servo_pwm_min'] = P['servo_pwm_null']
                P['servo_pwm_max'] = P['servo_pwm_null']
                P['motor_pwm_min'] = P['motor_pwm_null']
                P['motor_pwm_max'] = P['motor_pwm_null']
                P['servo_pwm_smooth'] = P['servo_pwm_null']
                P['motor_pwm_smooth'] = P['motor_pwm_null']
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
            #pprint(P)
            print_timer.reset()           
    print 'end _calibrate_run_loop.'
