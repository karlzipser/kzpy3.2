from kzpy3.utils3 import *
exec(identify_file_str)
import rospy


cal_types = ['servo_pwm_null','servo_pwm_min','servo_pwm_max','motor_pwm_null','motor_pwm_min','motor_pwm_max']

def Calibration_Mode(P):
    threading.Thread(target=_calibrate_run_loop,args=[P]).start()

def _calibrate_run_loop(P):
    CS_("_calibrate_run_loop")
    no_sound_yet = True
    print_timer = Timer(1)
    frequency_timer = Timer(1)
    first_time_here = False
    while (not P['ABORT']) and (not rospy.is_shutdown()):
        frequency_timer.freq(name='_calibrate_run_loop',do_print=P['print_calibration_freq'])
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.02)
        if P['button_number'] != 4:
            no_sound_yet = True
            if first_time_here:
                try:
                    Cal = lo(opjD('calibrations.pkl'))
                except:
                    Cal = {}
                    for c in cal_types:
                        Cal[c] = []
                for c in cal_types:
                   Cal[c].append(int(P[c]))
                so(Cal,opjD('calibrations.pkl'))
                first_time_here = False
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
                if no_sound_yet:
                    P['Arduinos']['SOUND'].write("(1929)")
                    no_sound_yet = False
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
                        first_time_here = True
                        
        try:
            print [int(P['servo_pwm']),
                int(P['servo_pwm_null']),
                int(P['servo_pwm_min']),
                int(P['servo_pwm_max']),
                int(P['servo_pwm_max'] - P['servo_pwm_min']),
                int(P['motor_pwm_max'] - P['motor_pwm_min']),
                P['calibrated'],]
        except:
            print 'calibration print failed'

        if print_timer.check():
            print_timer.reset()           
    print 'end _calibrate_run_loop.'
