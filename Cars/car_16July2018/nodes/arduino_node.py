#!/usr/bin/env python
"""
python kzpy3/Cars/car_16July2018/nodes/arduino_node.py
"""
from kzpy3.utils2 import *

Parameters = {}
Parameters['calibrated'] = False
Parameters['ABORT'] = False
Parameters['USE_MSE'] = True
Parameters['USE_SIG'] = True
Parameters['USE_IMU'] = True
Parameters['agent_choice'] = 'human'
Parameters['servo_percent'] = 49
Parameters['motor_percent'] = 49
Parameters['LED_number'] = {}
Parameters['LED_number']['current'] = 0
Parameters['CALIBRATION_NULL_START_TIME'] = 3.0
Parameters['CALIBRATION_START_TIME'] = 4.0
Parameters['print_mse_freq'] = False
Parameters['print_imu_freq'] = False
Parameters['print_calibration_freq'] = False
Parameters['print_selector_freq'] = False
Parameters['print_led_freq'] = False
Parameters['USE_ROS'] = using_linux()
Parameters['human'] = {}
Parameters['human']['servo_percent'] = 49
Parameters['human']['motor_percent'] = 49
Parameters['network'] = {}
Parameters['network']['servo_percent'] = 49
Parameters['network']['motor_percent'] = 49
Parameters['Hz'] = {}

import default_values
for k in default_values.Mse.keys():
    Parameters[k] = default_values.Mse[k]

if Parameters['USE_ROS']:
    import std_msgs.msg
    import geometry_msgs.msg
    import rospy
    P = Parameters
    s = Parameters['HUMAN_SMOOTHING_PARAMETER_1']
    def cmd_steer_callback(msg):
        P['network']['servo_percent'] = msg.data
    def cmd_motor_callback(msg):
        P['network']['motor_percent'] = msg.data
    rospy.init_node('run_arduino',anonymous=True)
    rospy.Subscriber('cmd/steer', std_msgs.msg.Int32, callback=cmd_steer_callback)
    rospy.Subscriber('cmd/motor', std_msgs.msg.Int32, callback=cmd_motor_callback)
    P['human_agent_pub'] = rospy.Publisher('human_agent', std_msgs.msg.Int32, queue_size=5) 
    P['drive_mode_pub'] = rospy.Publisher('drive_mode', std_msgs.msg.Int32, queue_size=5) 
    P['behavioral_mode_pub'] = rospy.Publisher('behavioral_mode', std_msgs.msg.String, queue_size=5)
    P['place_choice_pub'] = rospy.Publisher('place_choice', std_msgs.msg.String, queue_size=5)
    P['button_number_pub'] = rospy.Publisher('button_number', std_msgs.msg.Int32, queue_size=5) 
    P['steer_pub'] = rospy.Publisher('steer', std_msgs.msg.Int32, queue_size=5) 
    P['motor_pub'] = rospy.Publisher('motor', std_msgs.msg.Int32, queue_size=5) 
    P['encoder_pub'] = rospy.Publisher('encoder', std_msgs.msg.Float32, queue_size=5)
    P['Hz_acc_pub'] = rospy.Publisher('Hz_acc', std_msgs.msg.Float32, queue_size=5)
    P['Hz_mse_pub'] = rospy.Publisher('Hz_mse', std_msgs.msg.Float32, queue_size=5)
    P['gyro_pub'] = rospy.Publisher('gyro', geometry_msgs.msg.Vector3, queue_size=100)
    P['gyro_heading_pub'] = rospy.Publisher('gyro_heading', geometry_msgs.msg.Vector3, queue_size=100)
    P['acc_pub'] = rospy.Publisher('acc', geometry_msgs.msg.Vector3, queue_size=100)

    imu_dic = {}
    imu_dic['gyro'] = 'gyro_pub'
    imu_dic['acc'] = 'acc_pub'
    imu_dic['head'] = 'gyro_heading_pub'

    IMU_low_frequency_pub_timer = Timer(0.5)
    MSE_low_frequency_pub_timer = Timer(0.5)
    No_Arduino_data_low_frequency_pub_timer = Timer(0.5)

    def publish_IMU_data(P,m):
        P[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*P[m]['xyz']))
        if IMU_low_frequency_pub_timer.check():
            P['Hz_acc_pub'].publish(std_msgs.msg.Float32(P['Hz']['acc']))
            IMU_low_frequency_pub_timer.reset()


    def publish_MSE_data(P):
        if P['agent_choice'] == 'human':
            human_val = 1
        else:
            human_val = 0
        if P['selector_mode'] == 'drive_mode':
            drive_mode = 1
        else:
            drive_mode = 0         
        P['steer_pub'].publish(std_msgs.msg.Int32(P['human']['servo_percent']))
        P['motor_pub'].publish(std_msgs.msg.Int32(P['human']['motor_percent']))
        P['button_number_pub'].publish(std_msgs.msg.Int32(P['button_number']))
        P['encoder_pub'].publish(std_msgs.msg.Float32(P['encoder']))
        if MSE_low_frequency_pub_timer.check():
            P['behavioral_mode_pub'].publish(d2s(P['behavioral_mode_choice']))
            P['place_choice_pub'].publish(d2s(P['place_choice']))
            P['human_agent_pub'].publish(std_msgs.msg.Int32(human_val))
            P['drive_mode_pub'].publish(std_msgs.msg.Int32(drive_mode))
            P['Hz_mse_pub'].publish(std_msgs.msg.Float32(P['Hz']['mse']))
            MSE_low_frequency_pub_timer.reset()

    def publish_No_Arduino_data(P):
        human_val = 0
        drive_mode = 1
        if No_Arduino_data_low_frequency_pub_timer.check():
            P['behavioral_mode_pub'].publish(d2s('direct')
            P['place_choice_pub'].publish(d2s('local')
            P['human_agent_pub'].publish(std_msgs.msg.Int32(human_val))
            P['drive_mode_pub'].publish(std_msgs.msg.Int32(drive_mode))
            No_Arduino_data_low_frequency_pub_timer.reset()


    P['publish_IMU_data'] = publish_IMU_data
    P['publish_MSE_data'] = publish_MSE_data
    P['publish_No_Arduino_data'] = publish_No_Arduino_data

import threading
from arduino_utils.serial_init import *
from arduino_utils.tactic_rc_controller import *
from arduino_utils.calibration_mode import *
from arduino_utils.selector_mode import *
from arduino_utils.led_display import *
from arduino_utils.IMU_arduino import *

if 'Start Arduino threads...':
    baudrate = 115200
    timeout = 0.1
    assign_serial_connections(Parameters,get_arduino_serial_connections(baudrate,timeout))
    if Parameters['USE_MSE'] and 'MSE' in Parameters['Arduinos'].keys():
        TACTIC_RC_controller(Parameters)
        Calibration_Mode(Parameters)
        Selector_Mode(Parameters)
    else:
        spd2s("!!!!!!!!!! 'MSE' not in Arduinos[] or not using 'MSE' !!!!!!!!!!!")
    if Parameters['USE_SIG'] and 'SIG' in Parameters['Arduinos'].keys():
        LED_Display(Parameters)
    else:
        spd2s("!!!!!!!!!! 'SIG' not in Arduinos[] or not using 'SIG' !!!!!!!!!!!")
    if Parameters['USE_IMU'] and 'IMU' in Parameters['Arduinos'].keys():
        IMU_Arduino(Parameters)
    else:
        spd2s("!!!!!!!!!! 'IMU' not in Arduinos[] or not using 'IMU' !!!!!!!!!!!")


if 'Main loop...':
    print 'main loop'
    q = '_'
    while q not in ['q','Q']:
        q = raw_input('')
        if Parameters['ABORT']:
            break
        time.sleep(0.1)
    Parameters['ABORT'] = True
    print 'done.'
    if Parameters['USE_ROS']:
        P['drive_mode_pub'].publish(std_msgs.msg.Int32(-999))
        print "doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))"
        time.sleep(0.5)
        unix(opjh('kzpy3/scripts/kill_ros.sh'))

#EOF
