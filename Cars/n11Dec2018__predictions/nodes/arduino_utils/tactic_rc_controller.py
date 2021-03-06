from kzpy3.utils3 import *
exec(identify_file_str)
import rospy
import default_values

def TACTIC_RC_controller(P):
    threading.Thread(target=_TACTIC_RC_controller_run_loop,args=[P]).start()
    
def _TACTIC_RC_controller_run_loop(P):

    print('_TACTIC_RC_controller_run_loop')
    if 'MSE' not in P['Arduinos']:
        assert False
    time.sleep(0.1)
    P['Arduinos']['MSE'].flushInput()
    time.sleep(0.1)
    P['Arduinos']['MSE'].flushOutput()
    flush_seconds = 0.25
    flush_timer = Timer(flush_seconds)
    in_this_mode_timer = Timer()
    Pid_processing_motor = Pid_Processing_Motor()
    _servo_pwm = -1

    P['button_number'] = 0
    bn = P['button_number']
    button_number_prev = 0
    write_str = ''
    sound_timer = Timer(0.05)

    while (not P['ABORT']) and (not rospy.is_shutdown()):

        time.sleep(0.01)

        try:
            read_str = P['Arduinos']['MSE'].readline()

            if flush_timer.check():
                P['Arduinos']['MSE'].flushInput()
                P['Arduinos']['MSE'].flushOutput()
                flush_timer.reset()

            if not P['Desktop version']:
                try:
                    exec('serial_input = list({0})'.format(read_str))
                    if len(serial_input) < 3:
                        assert False
                    assert serial_input[0] == 'mse'
                except:
                    continue
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

            P['button_number'] = bn

            if P['button_number'] == 4:
                P['time_since_button_4'].reset()

            P['button_time'] = P['button_timer'].time()

            if P['button_number'] != button_number_prev:
                pd2s("P['button_number'] =",P['button_number'])
                if 'SOUND' in P['Arduinos']:
                    P['Arduinos']['SOUND'].write(d2n(""" "(""",P['button_number'],""")" """))

            button_number_prev = P['button_number']

            s = P['HUMAN_SMOOTHING_PARAMETER_1']

            P['servo_pwm_smooth'] = (1.0-s)*P['servo_pwm'] + s*P['servo_pwm_smooth']
            P['motor_pwm_smooth'] = (1.0-s)*P['motor_pwm'] + s*P['motor_pwm_smooth']
            P['encoder_smooth'] = (1.0-s)*P['encoder'] + s*P['encoder_smooth']

            if P['calibrated'] == True:
                P['human']['servo_percent'] = servo_pwm_to_percent(P['servo_pwm_smooth'],P)
                P['human']['motor_percent'] = motor_pwm_to_percent(P['motor_pwm_smooth'],P)



            P['temporary_human_control'] = False


            if P['agent_is_human'] == True:
                if P['use_motor_PID']:# and P['human']['motor_percent'] > 47:
                    _motor_pwm = motor_percent_to_pwm( Pid_processing_motor['do'](P['human_PID_motor_percent'],P['encoder_smooth'],P),P)
                else:
                    _motor_pwm = P['motor_pwm_smooth']
                write_str = get_write_str(P['servo_pwm_smooth'],P['servo_pwm_smooth'],_motor_pwm,P)
                in_this_mode = False

            elif P['agent_is_human'] == False and P['button_number']<4:#P['selector_mode'] == 'drive_mode':
                if np.abs(P['human']['motor_percent']-49) > 8:
                    P['temporary_human_control'] = True
                    if False: #checking if this gives unwanted inertia
                        if sound_timer.check():
                            if 'SOUND' in P['Arduinos']:
                                P['Arduinos']['SOUND'].write("(100)") # red taillights
                            sound_timer.reset()
                    in_this_mode = False
                    write_str = get_write_str(P['servo_pwm_smooth'],P['servo_pwm_smooth'],P['motor_pwm_smooth'],P)
                    P['time_since_button_4'].reset()
                
                elif P['time_since_button_4'].time() > 2.0:

                    if np.abs(P['human']['servo_percent']-49) > 8:
                        P['temporary_human_control'] = True
                        if sound_timer.check():
                            if 'SOUND' in P['Arduinos']:
                                P['Arduinos']['SOUND'].write("(100)") # red taillights
                            sound_timer.reset()
                        if in_this_mode == False:
                            in_this_mode = True
                            in_this_mode_timer.reset()
                        q = 1/(1.0+5*in_this_mode_timer.time())
                        if _servo_pwm < 0:
                            _servo_pwm = P['servo_pwm_smooth']
                        _servo_pwm = (1-q)*P['servo_pwm_smooth'] + q*_servo_pwm
                        _camera_pwm = _servo_pwm
                    else:
                        if False:  #checking if this gives unwanted inertia
                            if sound_timer.check():
                                if 'SOUND' in P['Arduinos']:
                                    P['Arduinos']['SOUND'].write("(101)") # green taillights
                                sound_timer.reset()
                        _camera_pwm = servo_percent_to_pwm(P['network']['camera_percent'],P)
                        _servo_pwm = servo_percent_to_pwm(P['network']['servo_percent'],P)
                        in_this_mode = False

                        
                    if P['use_motor_PID'] and P['network']['motor_percent'] > 49: # This because of flex
                        _motor_pwm = motor_percent_to_pwm( Pid_processing_motor['do'](P['network']['motor_percent'],P['encoder_smooth'],P),P)
                    else:
                        _motor_pwm = motor_percent_to_pwm(P['network']['motor_percent'],P)
            
                    write_str = get_write_str(_servo_pwm,_camera_pwm,_motor_pwm,P)
                else: # when is this condition reached?
                    in_this_mode = False
                    # write_str = get_write_str(P['servo_pwm_null'],P['servo_pwm_null'],P['motor_pwm_null'],P)
                    #CS("write_str = get_write_str(P['servo_pwm_null'],P['servo_pwm_null'],P['motor_pwm_null'],P)",emphasis=True)
            if P['button_number'] < 4:
                if P['calibrated']:
                    if P['drive_mode'] == 1:
                            P['Arduinos']['MSE'].write(write_str)
                            if P['MSE/print_timer'].check():
                                #print write_str,P['calibrated'],P['temporary_human_control'],P['agent_is_human']
                                P['MSE/print_timer'] = Timer(P['print_timer time'])
            else:
                pass
                #write_str = get_write_str(P['servo_pwm_null'],P['servo_pwm_null'],P['motor_pwm_null'],P)
                #P['Arduinos']['MSE'].write(write_str)
                        
            #print write_str

            if P['USE_ROS']:
                #print 2,P['publish_MSE_data']
                P['publish_MSE_data'](P)

            if False:
                if P['MSE/print_timer'].check():
                    #pd2s("MSE:",read_str)
                    #if 'acc' in read_str:
                    #    print "!!!!!!!!!!!!!!!!!"
                    print write_str,P['calibrated'],P['temporary_human_control'],P['agent_is_human']
                    P['MSE/print_timer'] = Timer(P['print_timer time'])

        except Exception as e:
            print('_TACTIC_RC_controller_run_loop')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',exception=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),exception=False)
            if True:
                print '_TACTIC_RC_controller_run_loop',e
            
            pass            
    print 'end _TACTIC_RC_controller_run_loop.'
    CS_("doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))")
    time.sleep(0.01)
    unix(opjh('kzpy3/scripts/kill_ros.sh'))

def get_write_str(servo_pwm,camera_pwm,motor_pwm,P):
    #print 'get_write_str'
    ws = d2n( '(',
        int(P['servo_pwm_smooth_manual_offset']+servo_pwm),',',
        int(P['camera_pwm_manual_offset']+camera_pwm+5000),',',
        int(motor_pwm+10000),')')
        #,
        #-np.abs(P['LED_number']['current']),
        #int(P['Arduinos']['SIG/write']),
        #')' )
    #print P['LED_number']['current']
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
    if P['agent_is_human'] == True:
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
        if P['button_number'] == 4:
            D['pid_motor_percent'] = 49
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
        #cg(D['pid_motor_percent'],motor_value,dp(encoder),dp(encoder_target))
        return D['pid_motor_percent']
    D['do'] = _do
    return D



#EOF