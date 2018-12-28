from kzpy3.utils3 import *
exec(identify_file_str)
import rospy

def Calibration_Mode(P):
    threading.Thread(target=_calibrate_run_loop,args=[P]).start()

def _calibrate_run_loop(P):

    CS_("_calibrate_run_loop")

    P['calibration mode timer'] = Timer()

    prev = False

    while (not P['ABORT']) and (not rospy.is_shutdown()):

        if P['now in calibration mode']:
            if prev == False:
                P['calibration mode timer'].reset()
                P['Arduinos']['SOUND'].write(_['sound/calibrate tune'])
                prev = True
            else:
                pass
        elif not P['now in calibration mode']:
            prev = False
            time.sleep(0.25)
            continue

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
           
    print 'end _calibrate_run_loop.'
    #CS_("doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))")
    time.sleep(0.01)
    #unix(opjh('kzpy3/scripts/kill_ros.sh'))

#EOF
