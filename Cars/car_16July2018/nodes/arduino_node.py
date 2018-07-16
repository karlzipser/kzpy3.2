#!/usr/bin/env python
"""
python kzpy3/Cars/car_16July2018/nodes/arduino_node.py
"""
from kzpy3.utils2 import *

Parameters = {}
Parameters['calibrated'] = False
Parameters['SMOOTHING_PARAMETER_1'] = 0.75
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
Parameters['newtork'] = {}
Parameters['newtork']['servo_percent'] = 49
Parameters['newtork']['motor_percent'] = 49

if Parameters['USE_ROS']:
    import std_msgs.msg
    import geometry_msgs.msg
    import rospy
    P = Parameters
    s = Parameters['SMOOTHING_PARAMETER_1']
    def cmd_steer_callback(msg):
        global P
        P['network']['servo_percent'] = (1.0-s)*msg.data + s*P['network']['servo_percent']
    def cmd_motor_callback(msg):
        global P
        P['network']['motor_percent'] = (1.0-s)*msg.data + s*P['network']['motor_percent']
    rospy.init_node('run_arduino',anonymous=True)
    rospy.Subscriber('cmd/steer', std_msgs.msg.Int32, callback=cmd_steer_callback)
    rospy.Subscriber('cmd/motor', std_msgs.msg.Int32, callback=cmd_motor_callback)
    P['human_agent_pub'] = rospy.Publisher('human_agent', std_msgs.msg.Int32, queue_size=5) 
    P['behavioral_mode_pub'] = rospy.Publisher('behavioral_mode', std_msgs.msg.String, queue_size=5)
    P['button_number_pub'] = rospy.Publisher('button_number', std_msgs.msg.Int32, queue_size=5) 
    P['steer_pub'] = rospy.Publisher('steer', std_msgs.msg.Int32, queue_size=5) 
    P['motor_pub'] = rospy.Publisher('motor', std_msgs.msg.Int32, queue_size=5) 
    P['encoder_pub'] = rospy.Publisher('encoder', std_msgs.msg.Float32, queue_size=5)
    P['gyro_pub'] = rospy.Publisher('gyro', geometry_msgs.msg.Vector3, queue_size=100)
    P['gyro_heading_pub'] = rospy.Publisher('gyro_heading', geometry_msgs.msg.Vector3, queue_size=100)
    P['acc_pub'] = rospy.Publisher('acc', geometry_msgs.msg.Vector3, queue_size=100)

    imu_dic = {}
    imu_dic['gyro'] = 'gyro_pub'
    imu_dic['acc'] = 'acc_pub'
    imu_dic['head'] = 'gyro_heading_pub'

    def publish_IMU_data(P,m):
        P[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*P[m]['xyz']))

    print_timer = Timer(1)
    def publish_MSE_data(P):
        print_timer.message('publish_MSE_data')
        if P['agent_choice'] == 'human':
            human_val = 1
        else:
            human_val = 0           
        P['steer_pub'].publish(std_msgs.msg.Int32(P['human']['servo_percent']))
        P['motor_pub'].publish(std_msgs.msg.Int32(P['human']['motor_percent']))
        P['button_number_pub'].publish(std_msgs.msg.Int32(P['button_number']))
        P['behavioral_mode_pub'].publish(P['behavioral_mode_choice'])
        P['encoder_pub'].publish(std_msgs.msg.Float32(P['encoder']))
        P['human_agent_pub'].publish(std_msgs.msg.Int32(human_val))

    P['publish_IMU_data'] = publish_IMU_data
    P['publish_MSE_data'] = publish_MSE_data


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
    if False:#Parameters['USE_ROS']:
        print "doing... unix(opjh('kzpy3/kill_ros.sh'))"
        unix(opjh('kzpy3/kill_ros.sh'))

#EOF
