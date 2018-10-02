from kzpy3.utils3 import *
exec(identify_file_str)
import rospy

current_bag_number = 0

def get_bag_info():
    global current_bag_number
    print 'get_bag_info'
    try:
        latest_rosbag_folder = most_recent_file_in_folder(opjm('rosbags'))
        latest_rosbag = most_recent_file_in_folder(latest_rosbag_folder)
        bag_num = int(fname(latest_rosbag).split('_')[-1].split('.')[0])
        bag_size = os.path.getsize(latest_rosbag)
        bag_size = dp(bag_size/1000000000.)
        print latest_rosbag_folder,latest_rosbag,bag_num,bag_size,'current_bag_number=',current_bag_number
        if (bag_num == current_bag_number+1) and bag_size > 0.5:
            current_bag_number += 1
            return current_bag_number
        else:
            return 0
    except:
        return 0




cal_types = ['servo_pwm_null','servo_pwm_min','servo_pwm_max','motor_pwm_null','motor_pwm_min','motor_pwm_max']

def Calibration_Mode(P):
    threading.Thread(target=_calibrate_run_loop,args=[P]).start()

def _calibrate_run_loop(P):
    CS_("_calibrate_run_loop")
    no_sound_yet = True
    print_timer = Timer(1)
    frequency_timer = Timer(1)
    first_time_here = False
    bandwidth_check_timer = Timer(60)
    bandwidth_check_timer.trigger()
    rosbag_check_timer = Timer(3)
    rosbag_check_timer.trigger()
    while (not P['ABORT']) and (not rospy.is_shutdown()):
        if rosbag_check_timer.check():
            b = get_bag_info()
            if b > 0:
                cs('new bag file',b)
            rosbag_check_timer.reset()
        if bandwidth_check_timer.check():
            unix(d2s('bash',opjk('Cars/30Sept2018_car/scripts/bandwidth_tester.sh')))
            zed_left_bw = txt_file_to_list_of_strings(opjD('left_image_rect_color_bw.txt'))
            os1_points_bw = txt_file_to_list_of_strings(opjD('os1_node_points_bw.txt'))
            print 'left_image_rect_color_bw.txt',zed_left_bw
            print 'os1_node_points_bw.txt',os1_points_bw
            bandwidth_check_timer.reset()
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
