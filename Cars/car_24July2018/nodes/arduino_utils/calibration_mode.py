from kzpy3.utils2 import *
exec(identify_file_str)

def Calibration_Mode(P):
    threading.Thread(target=_calibrate_run_loop,args=[P]).start()

def _calibrate_run_loop(P):
    CS_("_calibrate_run_loop")
    print_timer = Timer(1)
    frequency_timer = Timer(1)
    while (not P['ABORT']) and (not rospy.is_shutdown()):
        frequency_timer.freq(name='_calibrate_run_loop',do_print=P['print_calibration_freq'])
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.02)
        if P['button_number'] != 4:
            time.sleep(0.1)
            continue
        if P['button_time'] < P['CALIBRATION_NULL_START_TIME']:
            time.sleep(0.01)
            continue
        if True:
            if P['button_time'] < P['CALIBRATION_NULL_START_TIME']+0.1:
                P['calibrated'] = False
                P['servo_pwm_null'] = P['servo_pwm']
                P['motor_pwm_null'] = P['motor_pwm']
            elif P['button_time'] < P['CALIBRATION_START_TIME']:
                s = P['HUMAN_SMOOTHING_PARAMETER_1']
                P['servo_pwm_null'] = (1.0-s)*P['servo_pwm'] + s*P['servo_pwm_null']
                P['motor_pwm_null'] = (1.0-s)*P['motor_pwm'] + s*P['motor_pwm_null']
                P['servo_pwm_min'] = P['servo_pwm_null']
                P['servo_pwm_max'] = P['servo_pwm_null']
                P['motor_pwm_min'] = P['motor_pwm_null']
                P['motor_pwm_max'] = P['motor_pwm_null']
                P['servo_pwm_smooth'] = P['servo_pwm_null']
                P['motor_pwm_smooth'] = P['motor_pwm_null']
            else:
                if P['servo_pwm_max'] < P['servo_pwm']:
                    P['servo_pwm_max'] = P['servo_pwm']
                if P['servo_pwm_min'] > P['servo_pwm']:
                    P['servo_pwm_min'] = P['servo_pwm']
                if P['motor_pwm_max'] < P['motor_pwm']:
                    P['motor_pwm_max'] = P['motor_pwm']
                if P['motor_pwm_min'] > P['motor_pwm']:
                    P['motor_pwm_min'] = P['motor_pwm']
                if P['servo_pwm_max'] - P['servo_pwm_min'] > 300:
                    if P['motor_pwm_max'] - P['motor_pwm_min'] > 300:
                        P['calibrated'] = True
        if print_timer.check():
            print_timer.reset()           
    print 'end _calibrate_run_loop.'
