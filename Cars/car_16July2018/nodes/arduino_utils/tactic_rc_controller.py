from kzpy3.utils2 import *
import threading
if P['USE_ROS']:
    import std_msgs.msg
    import rospy

def TACTIC_RC_controller(P):
    P['button_delta'] = 50
    P['button_number'] = 0
    P['button_timer'] = Timer()
    P['time_since_button_4'] = Timer()
    P['servo_pwm_smooth'] = 1000
    P['motor_pwm_smooth'] = 1000
    P['selector_mode'] = False

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
    print_timer = Timer(0.25)
    ctr_timer = Timer()
    freq_timer = Timer(3) #####
    while P['ABORT'] == False:
        if freq_timer.check(): ####
            pprint(P['Hz']) ####
            freq_timer.reset()
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

            if 'Do smoothing...':
                s = P['HUMAN_SMOOTHING_PARAMETER_1']
                P['servo_pwm_smooth'] = (1.0-s)*P['servo_pwm'] + s*P['servo_pwm_smooth']
                P['motor_pwm_smooth'] = (1.0-s)*P['motor_pwm'] + s*P['motor_pwm_smooth']

            if P['calibrated'] == True:
                P['human']['servo_percent'] = pwm_to_percent(
                    P['servo_pwm_null'],P['servo_pwm_smooth'],P['servo_pwm_max'],P['servo_pwm_min'])
                P['human']['motor_percent'] = pwm_to_percent(
                    P['motor_pwm_null'],P['motor_pwm_smooth'],P['motor_pwm_max'],P['motor_pwm_min'])

            if 'Send servo/motor commands to Arduino...':
                if P['agent_choice'] == 'human':
                    write_str = d2n( '(', int(P['servo_pwm_smooth']), ',', int(P['motor_pwm_smooth']+10000), ')')
                elif P['agent_choice'] == 'network':
                    if np.abs(P['human']['motor_percent']-49) > 4:
                        write_str = d2n( '(', int(P['servo_pwm_smooth']), ',', int(P['motor_pwm_smooth']+10000), ')')
                        P['time_since_button_4'].reset()
                        print_timer.message(d2s('Temporary human control control...',P['human']['servo_percent'],P['human']['motor_percent']))
                    elif P['time_since_button_4'].time() > 2.0:
                        if np.abs(P['human']['servo_percent']-49) > 4:
                            _servo_pwm = P['servo_pwm_smooth']
                        else:
                            _servo_pwm = percent_to_pwm(P['network']['servo_percent'],P['servo_pwm_null'],P['servo_pwm_max'],P['servo_pwm_min'])
                        _motor_pwm = percent_to_pwm(P['network']['motor_percent'],P['motor_pwm_null'],P['motor_pwm_max'],P['motor_pwm_min'])
                        write_str = d2n( '(', int(_servo_pwm), ',', int(_motor_pwm+10000), ')')
                    else:
                        print_timer.message('Waiting before giving network control...')
                        write_str = d2n( '(',49,',',49+10000,')')
                if P['button_number'] != 4:
                    if P['calibrated']:
                        if P['selector_mode'] == 'drive_mode':
                            P['Arduinos']['MSE'].write(write_str)
            
            if frequency_timer.check() and P['USE_ROS']:
                P['Hz_mse_pub'].publish(std_msgs.msg.Float32(P['Hz']['mse']))
            Hz = frequency_timer.freq(name='_TACTIC_RC_controller_run_loop',do_print=P['print_mse_freq'])
            if is_number(Hz):
                P['Hz']['mse'] = Hz
                if ctr_timer.time() > 5 and P['selector_mode'] == 'drive_mode':
                    if Hz < 30 or Hz > 90:
                        spd2s('MSE Hz =',Hz,'...aborting...')
            if P['USE_ROS']:
                P['publish_MSE_data'](P)           
        except Exception as e:
            print '_TACTIC_RC_controller_run_loop',e
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
