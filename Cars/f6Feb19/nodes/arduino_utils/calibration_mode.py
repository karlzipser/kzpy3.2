from kzpy3.utils3 import *
exec(identify_file_str)
import rospy

def Calibration_Mode(P):
    threading.Thread(target=_calibrate_run_loop,args=[P]).start()

start = Timer(2)
start.trigger()
print_timer = Timer(1)

def _calibrate_run_loop(P):

    CS_("_calibrate_run_loop")

    P['calibration mode timer'] = Timer()

    prev = False

    while (not P['ABORT']) and (not rospy.is_shutdown()):

        if P['now in calibration mode']:
            if prev == False:
                P['calibration mode timer'].reset()
                prev = True
            else:
                pass
        elif not P['now in calibration mode']:
            prev = False
            time.sleep(0.25)
            continue
        
        if P['calibrated']:
            P['Arduinos']['LIGHTS'].write(P['Lights']['purple'])
        else:
            P['Arduinos']['LIGHTS'].write(P['Lights']['purple blink'])
        
        if P['calibration mode timer'].time() < P['CALIBRATION_NULL_START_TIME']:
            time.sleep(0.01)

        elif P['calibration mode timer'].time() < P['CALIBRATION_NULL_START_TIME']+0.1:
            P['calibrated'] = False
            P['servo_pwm_null'] = P['servo_pwm']
            P['motor_pwm_null'] = P['motor_pwm']

        elif P['calibration mode timer'].time() < P['CALIBRATION_START_TIME']:
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
            start.message('Calibrate now.')
            if P['servo_pwm_max'] < P['servo_pwm']:
                P['servo_pwm_max'] = P['servo_pwm']
            if P['servo_pwm_min'] > P['servo_pwm']:
                P['servo_pwm_min'] = P['servo_pwm']
            if P['motor_pwm_max'] < P['motor_pwm']:
                P['motor_pwm_max'] = P['motor_pwm']
            if P['motor_pwm_min'] > P['motor_pwm']:
                P['motor_pwm_min'] = P['motor_pwm']
            print_timer.message(
                d2s(P['calibrated'],
                    int(P['servo_pwm_max'] - P['servo_pwm_min']),
                    int(P['motor_pwm_max'] - P['motor_pwm_min']),))
            if P['servo_pwm_max'] - P['servo_pwm_min'] > P['delta servo_pwm for calibration']:
                if P['motor_pwm_max'] - P['motor_pwm_min'] > P['delta motor_pwm for calibration']:
                    P['calibrated'] = True
           
    print 'end _calibrate_run_loop.'

#EOF
