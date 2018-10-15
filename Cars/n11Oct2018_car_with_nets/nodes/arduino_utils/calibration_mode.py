from kzpy3.utils3 import *
exec(identify_file_str)
import rospy

current_bag_number = 0

def get_bag_info():
    global current_bag_number
    try:
        latest_rosbag_folder = most_recent_file_in_folder(opjm('rosbags'))
        latest_rosbag = most_recent_file_in_folder(latest_rosbag_folder)
        bag_num = int(fname(latest_rosbag).split('_')[-1].split('.')[0])
        bag_size = os.path.getsize(latest_rosbag)
        bag_size = dp(bag_size/1000000000.)
        if (bag_num == current_bag_number+1) and bag_size > 0.5:
            current_bag_number += 1
            return current_bag_number
        else:
            return 0
    except:
        return 0

def Calibration_Mode(P):
    threading.Thread(target=_calibrate_run_loop,args=[P]).start()

def _calibrate_run_loop(P):
    CS_("_calibrate_run_loop")
    no_sound_yet = True
    print_timer = Timer(1)
    frequency_timer = Timer(1)
    bandwidth_check_timer = Timer(10)
    bandwidth_check_timer.trigger()
    rosbag_check_timer = Timer(3)
    rosbag_overdue_timer = Timer(45)
    rosbag_check_timer.trigger()
    if P['use LIDAR']:
        os1_okay = False
        os1_called_prev = 100
    zed_okay = False
    zed_called_prev = 100    
    while (not P['ABORT']) and (not rospy.is_shutdown()):


        if rosbag_check_timer.check():
            b = get_bag_info()
            if b > 0:
                cs('new bag file',b)
                if 'SOUND' in P['Arduinos']:
                    P['Arduinos']['SOUND'].write("(50)")
                rosbag_overdue_timer.reset()
            rosbag_check_timer.reset()

        if rosbag_overdue_timer.check():
            CS('Rosbag overdue!',exception=True)
            for i in range(10):
                if 'SOUND' in P['Arduinos']:
                    P['Arduinos']['SOUND'].write("(60)")
                    P['Arduinos']['SOUND'].write("(61)")
            rosbag_overdue_timer.reset()

        if bandwidth_check_timer.check():

            if P['zed_called']['val'] > zed_called_prev:
                zed_okay = True
                zed_called_prev = P['zed_called']['val']
            if P['use LIDAR']:
                if P['os1_called']['val'] > os1_called_prev:
                    os1_okay = True
                    os1_called_prev = P['os1_called']['val']

            if not zed_okay:
                for i in range(4):
                    CS('No ZED!',exception=True)
                    if 'SOUND' in P['Arduinos']:
                        P['Arduinos']['SOUND'].write("(60)")
                    time.sleep(2)
                time.sleep(2)
            else:
                if 'SOUND' in P['Arduinos']:
                    P['Arduinos']['SOUND'].write("(30)")
                time.sleep(1)
            if P['use LIDAR']:
                if not os1_okay:
                    for i in range(3):
                        CS('No LIDAR!',exception=True)
                        if 'SOUND' in P['Arduinos']:
                            P['Arduinos']['SOUND'].write("(61)")
                        time.sleep(2)
                    time.sleep(2)
                else:
                    if 'SOUND' in P['Arduinos']:
                        P['Arduinos']['SOUND'].write("(31)")

            if P['use LIDAR']:
                if os1_okay and zed_okay:
                    bandwidth_check_timer = Timer(60)
            elif zed_okay:
                bandwidth_check_timer = Timer(60)

            bandwidth_check_timer.reset()
        
        frequency_timer.freq(name='_calibrate_run_loop',do_print=P['print_calibration_freq'])
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.02)
        if P['button_number'] != 4:
            if P['agent_is_human'] == True:
                if 'SOUND' in P['Arduinos']:
                    P['Arduinos']['SOUND'].write("(100)") # red taillights
            elif P['agent_is_human'] == False and P['temporary_human_control'] == False:
                if 'SOUND' in P['Arduinos']:
                    P['Arduinos']['SOUND'].write("(101)") # green taillights
            else:
                pass # assert False
            no_sound_yet = True
            time.sleep(0.1)
            continue
        if P['button_time'] < P['CALIBRATION_NULL_START_TIME']:
            time.sleep(0.01)
            continue
        #print "calibration_mode.py A"
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
                    CS("Calibrate now!",emphasis=True)
                    if 'SOUND' in P['Arduinos']:
                        P['Arduinos']['SOUND'].write("(51)")
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
        #print "calibration_mode.py B"            
        try:
            pass
            """
            print [int(P['servo_pwm']),
                int(P['servo_pwm_null']),
                int(P['servo_pwm_min']),
                int(P['servo_pwm_max']),
                int(P['servo_pwm_max'] - P['servo_pwm_min']),
                int(P['motor_pwm_max'] - P['motor_pwm_min']),
                P['calibrated'],]
            """
        except:
            print 'calibration print failed'
        #print "calibration_mode.py C"
        if print_timer.check():
            print_timer.reset()           
    print 'end _calibrate_run_loop.'
    CS_("doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))")
    time.sleep(0.01)
    unix(opjh('kzpy3/scripts/kill_ros.sh'))
