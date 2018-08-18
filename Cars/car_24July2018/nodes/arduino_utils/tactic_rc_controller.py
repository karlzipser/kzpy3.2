from kzpy3.utils2 import *
exec(identify_file_str)

#encoder_list_min_length = 5

def TACTIC_RC_controller(P):
    P['button_delta'] = 50
    P['button_number'] = 0
    P['button_timer'] = Timer()
    P['time_since_button_4'] = Timer()
    P['servo_pwm_smooth'] = 1000
    P['motor_pwm_smooth'] = 1000
    P['selector_mode'] = False
    P['encoder_smooth'] = 0.0
    P['network']['camera_percent'] = 49 # why I'm not sure
    threading.Thread(target=_TACTIC_RC_controller_run_loop,args=[P]).start()
    
def _TACTIC_RC_controller_run_loop(P):
    print('_TACTIC_RC_controller_run_loop')
    time.sleep(0.1)
    P['Arduinos']['MSE'].flushInput()
    time.sleep(0.1)
    P['Arduinos']['MSE'].flushOutput()
    P['Hz']['mse'] = 0
    flush_seconds = 0.25
    flush_timer = Timer(flush_seconds)
    frequency_timer = Timer(1)
    print_timer = Timer(0.1)
    in_this_mode_timer = Timer()
    very_low_freq_timer = Timer(30)
    ctr_timer = Timer()
    Pid_processing_motor = Pid_Processing_Motor()
    Pid_processing_steer = Pid_Processing_Steer()

    while P['ABORT'] == False:
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.01)
        try:
            if 'Read serial and translate to list...':
                read_str = P['Arduinos']['MSE'].readline()
                if flush_timer.check():
                    P['Arduinos']['MSE'].flushInput()
                    P['Arduinos']['MSE'].flushOutput()
                    flush_timer.reset()
                exec('mse_input = list({0})'.format(read_str))       
                assert(mse_input[0]=='mse')
            if 'Unpack mse list...':
                P['button_pwm'] = mse_input[1]
                P['servo_pwm'] = mse_input[2]
                P['motor_pwm'] = mse_input[3]
                P['encoder'] = mse_input[4]
                P['servo_feedback'] = mse_input[5]

            if 'Assign button...':
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


            s = P['HUMAN_SMOOTHING_PARAMETER_1']


            P['servo_pwm_smooth'] = (1.0-s)*P['servo_pwm'] + s*P['servo_pwm_smooth']
            P['motor_pwm_smooth'] = (1.0-s)*P['motor_pwm'] + s*P['motor_pwm_smooth']
            P['encoder_smooth'] = (1.0-s)*P['encoder'] + s*P['encoder_smooth']

            P['servo_pwm_smooth']

            if P['calibrated'] == True:
                P['human']['servo_percent'] = servo_pwm_to_percent(P['servo_pwm_smooth'],P)
                P['human']['motor_percent'] = motor_pwm_to_percent(P['motor_pwm_smooth'],P)

            P['servo_feedback_percent'] = servo_feedback_to_percent(P['servo_feedback'],P)




            if P['agent_choice'] == 'human':
                write_str = get_write_str(P['servo_pwm_smooth'],P['servo_pwm_smooth'],P['motor_pwm_smooth'],P)
                #_servo_pwm = servo_percent_to_pwm( Pid_processing_steer['do'](P['network']['camera_percent'],P['human']['servo_percent']), P )
                #write_str = get_write_str(_servo_pwm,P['servo_pwm_smooth'],P['motor_pwm_smooth'],P)
                in_this_mode = False


            elif P['agent_choice'] == 'network' and P['selector_mode'] == 'drive_mode':
                if np.abs(P['human']['motor_percent']-49) > 4:
                    in_this_mode = False
                    write_str = get_write_str(P['servo_pwm_smooth'],P['servo_pwm_smooth'],P['motor_pwm_smooth'],P)
                    P['time_since_button_4'].reset()
                
                elif P['time_since_button_4'].time() > 2.0:

                    

                    if np.abs(P['human']['servo_percent']-49) > 4:
                        if in_this_mode == False:
                            in_this_mode = True
                            in_this_mode_timer.reset()
                        q = 1/(1.0+5*in_this_mode_timer.time())
                        _servo_pwm = (1-q)*P['servo_pwm_smooth'] + q*_servo_pwm
                        _camera_pwm = _servo_pwm
                    else:
                        _camera_pwm = servo_percent_to_pwm(P['network']['camera_percent'],P)
                        if False:
                            _servo_pwm = servo_percent_to_pwm(P['network']['servo_percent'],P)
                        if True:
                            if P['use_servo_feedback']:
                                _servo_percent = P['servo_feedback_percent']
                            else:
                                _servo_percent = P['network']['servo_percent']
                            _servo_pwm = servo_percent_to_pwm( Pid_processing_steer['do'](P['network']['camera_percent'],_servo_percent,P ),P)
            
                        _camera_pwm = servo_percent_to_pwm(P['network']['camera_percent'],P)
                        in_this_mode = False

                    if False:
                        _motor_pwm = motor_percent_to_pwm(P['network']['motor_percent'],P)
                    if True:
                        _motor_pwm = motor_percent_to_pwm( Pid_processing_motor['do'](P['network']['motor_percent'],P['encoder_smooth'],P),P)
            
                    write_str = get_write_str(_servo_pwm,_camera_pwm,_motor_pwm,P)
                else:
                    in_this_mode = False
                    #print_timer.message('Waiting before giving network control...') ############
                    write_str = get_write_str(P['servo_pwm_null'],P['servo_pwm_null'],P['motor_pwm_null'],P)


            if P['button_number'] != 4:
                if P['calibrated']:
                    #print(write_str)
                    if P['selector_mode'] == 'drive_mode':
                        if True:
                            P['Arduinos']['MSE'].write(write_str)
                        pass
                        

            
                
            Hz = frequency_timer.freq(name='_TACTIC_RC_controller_run_loop',do_print=P['print_mse_freq'])
            if is_number(Hz):
                P['Hz']['mse'] = Hz
                if ctr_timer.time() > 5 and P['selector_mode'] == 'drive_mode':
                    if Hz < 30 or Hz > 90:
                        spd2s('MSE Hz =',Hz,'...aborting...')
            if P['USE_ROS']:
                P['publish_MSE_data'](P)

            if print_timer.check():
                #print write_str
                pd2s(int(P['human']['servo_percent']),P['servo_feedback_percent'],int(P['network']['camera_percent']))
                #print(P['network']['motor_percent'],dp(Pid_processing_motor['pid_motor_percent'],1),dp(P['encoder_smooth'],1))
                print_timer.reset()

            if very_low_freq_timer.check():
                pd2s('servo:',int(P['servo_pwm_min']),int(P['servo_pwm_null']),int(P['servo_pwm_max']),'motor:',int(P['motor_pwm_min']),int(P['motor_pwm_null']),int(P['motor_pwm_max']))
                very_low_freq_timer.reset()
        except Exception as e:
            print '_TACTIC_RC_controller_run_loop',e #######
            pass            
    print 'end _TACTIC_RC_controller_run_loop.'

def get_write_str(servo_pwm,camera_pwm,motor_pwm,P):
    return d2n( '(',int(P['servo_pwm_smooth_manual_offset']+servo_pwm),',',int(P['camera_pwm_manual_offset']+camera_pwm+5000),',',int(motor_pwm+10000),')' )

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


def servo_feedback_to_percent(current_feedback,P):
    return 99-int(pwm_to_percent(float(P['servo_feedback_center']),float(current_feedback),float(P['servo_feedback_right']),float(P['servo_feedback_left'])))




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



def Pid_Processing_Steer():#gain=0.05,delta_max=0.05,pid_steer_percent_max=99,pid_steer_percent_min=0):
    D = {}
    D['pid_steer_percent'] = 49
    def _do(camera_value,servo_feedback_percent,P):
        delta = P['pid_steer_gain'] * (camera_value - servo_feedback_percent)
        if delta > 0:
            delta = min(delta,P['pid_steer_delta_max'])
        else:
            delta = max(delta,-P['pid_steer_delta_max'])
        D['pid_steer_percent'] += delta
        D['pid_steer_percent'] = min(D['pid_steer_percent'],P['pid_steer_steer_percent_max'])
        D['pid_steer_percent'] = max(D['pid_steer_percent'],P['pid_steer_steer_percent_min'])
        return D['pid_steer_percent']
    D['do'] = _do
    return D









#EOF