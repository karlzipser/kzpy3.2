from kzpy3.utils3 import *
exec(identify_file_str)
import rospy
import default_values


def TACTIC_RC_controller(P):
    threading.Thread(target=_TACTIC_RC_controller_run_loop,args=[P]).start()


def Pid_Processing_Motor():
    D = {}
    D['pid_motor_percent'] = 49
    def _do(motor_value,encoder,P):
        assert P['button_number'] != 4
        encoder_target = (motor_value-49.0) / P['pid_motor_slope']
        encoder_target = min(encoder_target,P['pid_motor_encoder_max'])
        delta = P['pid_motor_gain'] * (encoder_target - encoder)
        if delta > 0:
            delta = min(delta,P['pid_motor_delta_max'])
        else:
            delta = max(delta,-P['pid_motor_delta_max'])
        D['pid_motor_percent'] += delta
        D['pid_motor_percent'] = min(D['pid_motor_percent'],P['pid_motor_percent_max'])
        D['pid_motor_percent'] = max(D['pid_motor_percent'],P['pid_motor_percent_min'])
        if D['pid_motor_percent'] > P['max motor']:
             # 49 #25 April 2019
            try:
                cr("*** D['pid_motor_percent'] ==",D['pid_motor_percent'],"was >",P['max motor'],"i.e., P['max motor']")
            except:
                cr('oops!')
            D['pid_motor_percent'] = P['max motor']
            #if 'LIGHTS' in P['Arduinos']:
            #    P['Arduinos']['LIGHTS'].write(P['lights/failure 1'])
        return D['pid_motor_percent']
    D['do'] = _do
    return D
    
Pid_processing_motor = Pid_Processing_Motor()


sound_timer = Timer(0.05)
def _TACTIC_RC_controller_run_loop(P):

    print('_TACTIC_RC_controller_run_loop')
    if 'MSE' not in P['Arduinos']:
        assert False
    time.sleep(0.1)
    P['Arduinos']['MSE'].flushInput()
    time.sleep(0.1)
    P['Arduinos']['MSE'].flushOutput()

    #_servo_pwm = -1

    P['button_number_prev'] = 0
    P['button_number'] = 0
    bn = P['button_number']
    write_str = ''
    

    while (not P['ABORT']) and (not rospy.is_shutdown()):

        time.sleep(0.001)

        try:
            update_button_servo_motor_encoder(P)

        except Exception as e:
            print('_TACTIC_RC_controller_run_loop')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',exception=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),exception=False)
          
        drive_car(P)

        if P['USE_ROS']:
            P['publish_MSE_data'](P)

    print 'end _TACTIC_RC_controller_run_loop.'




def drive_car(P):

    write_str = ''

    if P['data_saving changed up']:
        P['data_saving changed up'] = False
        cy("drive_car(P):: P['data_saving changed up']",int(time.time()))
        #if 'LIGHTS' in P['Arduinos']:
        #    P['Arduinos']['LIGHTS'].write(P['lights/save tune'])

    if P['calibrated'] == True:
        P['human']['servo_percent'] = servo_pwm_to_percent(P['servo_pwm_smooth'],P)
        P['human']['motor_percent'] = motor_pwm_to_percent(P['motor_pwm_smooth'],P)
    else:
        pass


    if (P['agent_is_human'] or P['button_number'] == 4) and not P['now in calibration mode']:

        if sound_timer.check():
            if 'LIGHTS' in P['Arduinos']:
                P['Arduinos']['LIGHTS'].write(P['lights/human, YES'])
            sound_timer.reset()
        else:
            pass

        if P['use_human_motor_PID'] and P['button_number'] != 4:
            #_motor_pwm = motor_percent_to_pwm(
            #        Pid_processing_motor['do'](P['human_PID_motor_percent'],P['encoder_smooth'],P),P)
            human_pid_motor_percent = Pid_processing_motor['do'](
                P['human_PID_motor_percent'],P['encoder_smooth'],P)
            _motor_pwm = motor_percent_to_pwm(human_pid_motor_percent,P)
            P['human']['motor_percent'] = human_pid_motor_percent # now this can be published
        else:
            _motor_pwm = P['motor_pwm_smooth']
        write_str = get_write_str(P['servo_pwm_smooth'],P['servo_pwm_null'],_motor_pwm,P)

    elif (not P['agent_is_human'] and P['button_number'] != 4) and not P['now in calibration mode']:

        if sound_timer.check():
            if 'LIGHTS' in P['Arduinos']:
                P['Arduinos']['LIGHTS'].write(P['lights/human, NO'])
            sound_timer.reset()
        else:
            pass

        _camera_pwm = servo_percent_to_pwm(P['cmd/camera'],P)
        _servo_pwm = servo_percent_to_pwm(P['cmd/steer'],P)
  
        if P['use_net_motor_PID'] and P['cmd/motor'] > 49: # This because of flex
            _motor_pwm = motor_percent_to_pwm(
                Pid_processing_motor['do'](P['cmd/motor'],P['encoder_smooth'],P),P)
        else:
            _motor_pwm = motor_percent_to_pwm(P['cmd/motor'],P)
        write_str = get_write_str(_servo_pwm,_camera_pwm,_motor_pwm,P)
    else:
        time.sleep(0.1)

    
    if P['calibrated'] and not P['now in calibration mode']:
        P['drive_mode'] = 1
        P['Arduinos']['MSE'].write(write_str)
        if P['MSE/print_timer'].check():
            P['MSE/print_timer'] = Timer(P['print_timer time'])
    else:
        P['drive_mode'] = 0





flush_seconds = 0.25
flush_timer = Timer(flush_seconds)
def update_button_servo_motor_encoder(P):
    
    read_str = P['Arduinos']['MSE'].readline()

    if flush_timer.check():
        P['Arduinos']['MSE'].flushInput()
        P['Arduinos']['MSE'].flushOutput()
        flush_timer.reset()
    try:
        exec('serial_input = list({0})'.format(read_str))
        if len(serial_input) < 3:
            assert False
        assert serial_input[0] == 'mse'
    except:
        return

    P['button_pwm'] = serial_input[1]
    P['servo_pwm'] = serial_input[2]
    P['motor_pwm'] = serial_input[3]
    P['encoder'] = serial_input[4]
    #if P['motor_pwm'] < P['motor_pwm_null']:
    #    P['encoder'] *= -1.0

    bpwm = P['button_pwm']
    
    if np.abs(bpwm - 1900) < P['button_delta']:
        bn = 1
    elif np.abs(bpwm - 1700) < P['button_delta']:
        bn = 2
    elif np.abs(bpwm - 1424) < P['button_delta']:
        bn = 3
    elif np.abs(bpwm - 870) < P['button_delta']:
        bn = 4

    if P['button_number'] != bn:
        P['button_timer'].reset()

    P['button_number'] = bn

    P['button_time'] = P['button_timer'].time()

    if P['button_number'] != P['button_number_prev']:
        pd2s("P['button_number'] =",P['button_number'])
        if 'LIGHTS' in P['Arduinos']:
            P['Arduinos']['LIGHTS'].write(d2n(""" "(""",P['button_number'],""")" """))

    P['button_number_prev'] = P['button_number']

    s = P['HUMAN_SMOOTHING_PARAMETER_1']

    P['servo_pwm_smooth'] = (1.0-s)*P['servo_pwm'] + s*P['servo_pwm_smooth']
    P['motor_pwm_smooth'] = (1.0-s)*P['motor_pwm'] + s*P['motor_pwm_smooth']
    P['encoder_smooth'] = (1.0-s)*P['encoder'] + s*P['encoder_smooth']






def get_write_str(servo_pwm,camera_pwm,motor_pwm,P):
    ws = d2n( '(',
        int(P['servo_pwm_smooth_manual_offset']+servo_pwm),',',
        int(P['camera_pwm_manual_offset']+camera_pwm+5000),',',
        int(motor_pwm+10000),')')
    return ws

def pwm_to_percent(null_pwm,current_pwm,max_pwm,min_pwm):
    current_pwm -= null_pwm
    max_pwm -= null_pwm
    min_pwm -= null_pwm
    if current_pwm >= 0:
        p = 99*(1.0 + current_pwm/max_pwm)/2.0
    else:
        p = 99*(1.0 - current_pwm/min_pwm)/2.0
    p = bound_value(p,0,99)     
    return p
    
def percent_to_pwm(percent,null_pwm,max_pwm,min_pwm):
    if percent >= 49:
        p = (percent-50)/50.0 * (max_pwm-null_pwm) + null_pwm
    else:
        p = (percent-50)/50.0 * (null_pwm-min_pwm) + null_pwm
    return p

def servo_pwm_to_percent(current_pwm,P):
    return pwm_to_percent(P['servo_pwm_null'],current_pwm,P['servo_pwm_max'],P['servo_pwm_min'])

def motor_pwm_to_percent(current_pwm,P):
    return pwm_to_percent(P['motor_pwm_null'],current_pwm,P['motor_pwm_max'],P['motor_pwm_min'])

def servo_percent_to_pwm(percent,P):
    return percent_to_pwm(percent,P['servo_pwm_null'],P['servo_pwm_max'],P['servo_pwm_min'])

def motor_percent_to_pwm(percent,P):
    return percent_to_pwm(percent,P['motor_pwm_null'],P['motor_pwm_max'],P['motor_pwm_min'])

def compare_percents_and_pwms(P):
    if P['agent_is_human'] == True:
        if P['drive_mode'] == 1:
            s_pwm = P['human']['servo_pwm_smooth']
            s_from_percent = servo_percent_to_pwm(P['human']['servo_percent'],P)
            m_pwm = P['human']['motor_pwm_smooth']
            m_from_percent = motor_percent_to_pwm(P['human']['motor_percent'],P)
            print dp(s_from_percent/(0.01+s_pwm),2),dp(m_from_percent/(0.01+m_pwm),2)






#EOF

