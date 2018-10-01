from kzpy3.utils3 import *
exec(identify_file_str)
import rospy
import Default_values.arduino.default_values

def TACTIC_RC_controller(P):

    threading.Thread(target=_TACTIC_RC_controller_run_loop,args=[P]).start()
    
def _TACTIC_RC_controller_run_loop(P):


    print('_TACTIC_RC_controller_run_loop')
    time.sleep(0.1)
    P['Arduinos']['MSE'].flushInput()
    time.sleep(0.1)
    P['Arduinos']['MSE'].flushOutput()
    flush_seconds = 0.25
    flush_timer = Timer(flush_seconds)
    #frequency_timer = Timer(1)
    print_timer = Timer(0.1)
    in_this_mode_timer = Timer()
    #very_low_freq_timer = Timer(30)
    ctr_timer = Timer()
    Pid_processing_motor = Pid_Processing_Motor()
    time_since_successful_read_from_arduino = Timer();_timer = Timer(0.2)
    acc_smoothed = [0,0,0]
    _servo_pwm = -1

    while (not P['ABORT']) and (not rospy.is_shutdown()):
        if False:
            if time_since_successful_read_from_arduino.time() > 1.0:
                _timer.message(d2s("time_since_successful_read_from_arduino.time()",time_since_successful_read_from_arduino.time()))
            if time_since_successful_read_from_arduino.time() > 2.0:
                CS_("time_since_successful_read_from_arduino.time() > 2, ABORT",emphasis=True)
                #Default_values.arduino.default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)

        time.sleep(0.01)
        try:
            read_str = P['Arduinos']['MSE'].readline()
            #print read_str
            if flush_timer.check():
                P['Arduinos']['MSE'].flushInput()
                P['Arduinos']['MSE'].flushOutput()
                flush_timer.reset()
            exec('serial_input = list({0})'.format(read_str))


            if serial_input[0] in ['acc','gyro','head']:
                #Hz = frequency_timers[m].freq(name=m,do_print=False)
                m = serial_input[0]
                if m == 'acc':
                    s = P['IMU_SMOOTHING_PARAMETER']
                    for i in range(3):
                        acc_smoothed[i] = (1.0-s)*serial_input[i+1] + s*acc_smoothed[i]
                    if acc_smoothed[1] < -9.0:
                        spd2s('acc_smoothed[1] < -9.0, ABORTING, SHUTTING DOWN!!!!!')
                        P['ABORT'] = True
                        default_values.EXIT(restart=False,shutdown=True,kill_ros=True,_file_=__file__)
                    #if is_number(Hz):
                    #    P['Hz'][m] = Hz
                    #    if Hz < 30 or Hz > 90:
                    #        if ctr_timer.time() > 5:
                    #            spd2s(m,'Hz =',Hz,'...aborting...')
                    #        else:
                    #            pass
                P[m]['xyz'] = serial_input[1:4]
                if P['USE_ROS']:
                    P['publish_IMU_data'](P,m)

            elif serial_input[0] == 'mse':

                P['button_pwm'] = serial_input[1]
                P['servo_pwm'] = serial_input[2]
                P['motor_pwm'] = serial_input[3]
                P['encoder'] = serial_input[4]

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
                if P['button_number'] == 4:
                    P['time_since_button_4'].reset()
                P['button_number'] = bn
                P['button_time'] = P['button_timer'].time()

                time_since_successful_read_from_arduino.reset()

                s = P['HUMAN_SMOOTHING_PARAMETER_1']

                P['servo_pwm_smooth'] = (1.0-s)*P['servo_pwm'] + s*P['servo_pwm_smooth']
                P['motor_pwm_smooth'] = (1.0-s)*P['motor_pwm'] + s*P['motor_pwm_smooth']
                if 'encoder' in P:
                    P['encoder_smooth'] = (1.0-s)*P['encoder'] + s*P['encoder_smooth']

                #P['servo_pwm_smooth']

                if P['calibrated'] == True:
                    P['human']['servo_percent'] = servo_pwm_to_percent(P['servo_pwm_smooth'],P)
                    P['human']['motor_percent'] = motor_pwm_to_percent(P['motor_pwm_smooth'],P)



            P['temporary_human_control'] = False
            
            if P['agent_choice'] == 'human':
                write_str = get_write_str(P['servo_pwm_smooth'],P['servo_pwm_smooth'],P['motor_pwm_smooth'],P)
                in_this_mode = False

            elif P['agent_choice'] == 'network' and P['selector_mode'] == 'drive_mode':
                if np.abs(P['human']['motor_percent']-49) > 4:
                    P['temporary_human_control'] = True
                    in_this_mode = False
                    write_str = get_write_str(P['servo_pwm_smooth'],P['servo_pwm_smooth'],P['motor_pwm_smooth'],P)
                    P['time_since_button_4'].reset()
                
                elif P['time_since_button_4'].time() > 2.0:

                    if np.abs(P['human']['servo_percent']-49) > 4:
                        P['temporary_human_control'] = True
                        if in_this_mode == False:
                            in_this_mode = True
                            in_this_mode_timer.reset()
                        q = 1/(1.0+5*in_this_mode_timer.time())
                        if _servo_pwm < 0:
                            _servo_pwm = P['servo_pwm_smooth']
                        _servo_pwm = (1-q)*P['servo_pwm_smooth'] + q*_servo_pwm
                        _camera_pwm = _servo_pwm
                    else:
                        _camera_pwm = servo_percent_to_pwm(P['network']['camera_percent'],P)
                        if True:
                            _servo_pwm = servo_percent_to_pwm(P['network']['servo_percent'],P)

                        _camera_pwm = servo_percent_to_pwm(P['network']['camera_percent'],P)
                        in_this_mode = False

                    if False:
                        _motor_pwm = motor_percent_to_pwm(P['network']['motor_percent'],P)
                    if True:
                        _motor_pwm = motor_percent_to_pwm( Pid_processing_motor['do'](P['network']['motor_percent'],P['encoder_smooth'],P),P)
            
                    write_str = get_write_str(_servo_pwm,_camera_pwm,_motor_pwm,P)
                else:
                    in_this_mode = False
                    write_str = get_write_str(P['servo_pwm_null'],P['servo_pwm_null'],P['motor_pwm_null'],P)

            if P['button_number'] != 4:
                if P['calibrated']:
                    if P['selector_mode'] == 'drive_mode':
                        if True:
                            P['Arduinos']['MSE'].write(write_str)
                        
            #Hz = frequency_timer.freq(name='_TACTIC_RC_controller_run_loop',do_print=P['print_mse_freq'])
            #if is_number(Hz):
            #    P['Hz']['mse'] = Hz
            #    if ctr_timer.time() > 5 and P['selector_mode'] == 'drive_mode':
            #        if Hz < 30 or Hz > 90:
            #            spd2s('MSE Hz =',Hz,'...aborting...')
            if P['USE_ROS']:
                P['publish_MSE_data'](P)

            if print_timer.check():
                print_timer.reset()

            #if very_low_freq_timer.check():
            #    pass
            #    if False:
            #        pd2s('servo:',int(P['servo_pwm_min']),int(P['servo_pwm_null']),int(P['servo_pwm_max']),'motor:',int(P['motor_pwm_min']),int(P['motor_pwm_null']),int(P['motor_pwm_max']))
            #    very_low_freq_timer.reset()
        except Exception as e:
            if True:
                print '_TACTIC_RC_controller_run_loop',e
            pass            
    print 'end _TACTIC_RC_controller_run_loop.'

def get_write_str(servo_pwm,camera_pwm,motor_pwm,P):
    #print 'get_write_str'
    ws = d2n( '(',
        int(P['servo_pwm_smooth_manual_offset']+servo_pwm),',',
        int(P['camera_pwm_manual_offset']+camera_pwm+5000),',',
        int(motor_pwm+10000),',',
        int(P['Arduinos']['SIG/write']),
        ')' )
    #cs(ws)
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
    if P['agent_choice'] == 'human':
        if P['drive_mode'] == 1:
            s_pwm = P['human']['servo_pwm_smooth']
            s_from_percent = servo_percent_to_pwm(P['human']['servo_percent'],P)
            m_pwm = P['human']['motor_pwm_smooth']
            m_from_percent = motor_percent_to_pwm(P['human']['motor_percent'],P)
            print dp(s_from_percent/(0.01+s_pwm),2),dp(m_from_percent/(0.01+m_pwm),2)


def Pid_Processing_Motor():#slope=(60-49)/3.0,gain=0.05,encoder_max=4.0,delta_max=0.05,pid_motor_percent_max=99,pid_motor_percent_min=0):
    D = {}
    D['pid_motor_percent'] = 49
    def _do(motor_value,encoder,P):
        encoder_target = (motor_value-49.0) / P['pid_motor_slope']
        encoder_target = min(encoder_target,P['pid_motor_encoder_max'])
        delta = P['pid_motor_gain'] * (encoder_target - encoder)
        if delta > 0:
            delta = min(delta,P['pid_motor_delta_max'])
        else:
            delta = max(delta,-P['pid_motor_delta_max'])
        D['pid_motor_percent'] += delta
        D['pid_motor_percent'] = min(D['pid_motor_percent'],P['pid_motor_percent_max'])
        D['pid_motor_percent'] = max(D['pid_motor_percent'],P['pid_steer_steer_percent_min'])
        return D['pid_motor_percent']
    D['do'] = _do
    return D



#EOF