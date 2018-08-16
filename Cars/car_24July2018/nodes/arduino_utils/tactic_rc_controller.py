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


    threading.Thread(target=_TACTIC_RC_controller_run_loop,args=[P]).start()
    #return P
    
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
    print_timer = Timer(1)
    in_this_mode_timer = Timer()
    very_low_freq_timer = Timer(30)
    ctr_timer = Timer()
    Pid_processing = Pid_Processing()
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
                #advance(P['encoder_list'],P['encoder'],min_len=encoder_list_min_length)
                #P['encoder_median'] = np.median()

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

            if P['calibrated'] == True:
                P['human']['servo_percent'] = servo_pwm_to_percent(P['servo_pwm_smooth'],P)
                P['human']['motor_percent'] = motor_pwm_to_percent(P['motor_pwm_smooth'],P)



            if P['agent_choice'] == 'human':
                write_str = d2n( '(', int(P['servo_pwm_smooth']), int(P['servo_pwm_smooth']+5000), ',', int(P['motor_pwm_smooth']+10000), ')')
                in_this_mode = False


            elif P['agent_choice'] == 'network' and P['selector_mode'] == 'drive_mode':
                if np.abs(P['human']['motor_percent']-49) > 4:
                    in_this_mode = False
                    #_servo_pwm = servo_percent_to_pwm(P['human']['servo_percent'],P)
                    #_motor_pwm = motor_percent_to_pwm(P['human']['motor_percent'],P)
                    #write_str = d2n( '(', int(_servo_pwm), ',', int(_motor_pwm+10000), ')')
                    write_str = d2n( '(', int(P['servo_pwm_smooth']), ',', int(P['servo_pwm_smooth']+5000), ',', int(P['motor_pwm_smooth']+10000), ')')
                    P['time_since_button_4'].reset()
                    #print_timer.message(d2s('Temporary human control control...',P['human']['servo_percent'],P['human']['motor_percent']))###
                
                elif P['time_since_button_4'].time() > 2.0:

                    

                    if np.abs(P['human']['servo_percent']-49) > 4:
                        if in_this_mode == False:
                            in_this_mode = True
                            in_this_mode_timer.reset()
                        q = 1/(1.0+5*in_this_mode_timer.time())
                        #print_timer.message(d2s(q,dp(in_this_mode_timer.time(),2)))
                        _servo_pwm = (1-q)*P['servo_pwm_smooth'] + q*_servo_pwm
                        _camera_pwm = _servo_pwm
                    else:
                        _servo_pwm = servo_percent_to_pwm(P['network']['servo_percent'],P)
                        _camera_pwm = servo_percent_to_pwm(P['network']['camera_percent'],P)
                        in_this_mode = False

                    if False:
                        _motor_pwm = motor_percent_to_pwm(P['network']['motor_percent'],P)
                    if True:
                        _motor_pwm = motor_percent_to_pwm( Pid_processing['do'](P['network']['motor_percent'],P['encoder_smooth']), P )
                    # insert PID here, motor 60% = 1.4 m/s, measure wheel circumferance,
                    # num magnets, use P['encoder'], maybe median of -5: of list of values
                    ###
                    write_str = d2n( '(', int(_servo_pwm), ',', int(_camera_pwm+5000), ',',int(_motor_pwm+10000), ')')
                else:
                    in_this_mode = False
                    #print_timer.message('Waiting before giving network control...') ############
                    write_str = d2n( '(',int(P['servo_pwm_null']),',',int(P['servo_pwm_null'])+5000,int(P['motor_pwm_null'])+10000,')') #?? this make no sense


            if P['button_number'] != 4:
                if P['calibrated']:
                    print(write_str)
                    if P['selector_mode'] == 'drive_mode':
                        pass
                        #P['Arduinos']['MSE'].write(write_str)
            
                
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
                print(P['network']['motor_percent'],dp(Pid_processing['pid_motor_percent'],1),dp(P['encoder_smooth'],1))
                print_timer.reset()

            if very_low_freq_timer.check():
                pd2s('servo:',int(P['servo_pwm_min']),int(P['servo_pwm_null']),int(P['servo_pwm_max']),'motor:',int(P['motor_pwm_min']),int(P['motor_pwm_null']),int(P['motor_pwm_max']))
                very_low_freq_timer.reset()
        except Exception as e:
            print '_TACTIC_RC_controller_run_loop',e #######
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





def Pid_Processing(slope=(60-49)/3.0,gain=0.05,encoder_max=4.0,delta_max=0.05,pid_motor_percent_max=99,pid_motor_percent_min=0):
    D = {}
    D['pid_motor_percent'] = 49
    def _do(motor_value,encoder):
        encoder_target = (motor_value-49.0) / slope
        encoder_target = min(encoder_target,encoder_max)
        delta = gain * (encoder_target - encoder)
        if delta > 0:
            delta = min(delta,delta_max)
        else:
            delta = max(delta,-delta_max)
        D['pid_motor_percent'] += delta
        D['pid_motor_percent'] = min(D['pid_motor_percent'],pid_motor_percent_max)
        D['pid_motor_percent'] = max(D['pid_motor_percent'],pid_motor_percent_min)
        return D['pid_motor_percent']
    D['do'] = _do
    return D



#EOF