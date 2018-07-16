#!/usr/bin/env python
"""
python kzpy3/Cars/car_12July2018/nodes/arduino_node.py
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
#Parameters['LED_number']['previous'] = 0
Parameters['LED_number']['current'] = 0
Parameters['CALIBRATION_NULL_START_TIME'] = 3.0
Parameters['CALIBRATION_START_TIME'] = 4.0
Parameters['print_mse_freq'] = False
Parameters['print_imu_freq'] = False
Parameters['print_calibration_freq'] = False
Parameters['print_selector_freq'] = False
Parameters['print_led_freq'] = False
Parameters['USE_ROS'] = True

if Parameters['USE_ROS']:
    import std_msgs.msg
    import geometry_msgs.msg
    import rospy
    P = Parameters
    def cmd_steer_callback(msg):
        global P
        P['network']['servo_percent'] = msg.data
    def cmd_motor_callback(msg):
        global P
        P['network']['motor_percent'] = msg.data
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
        if print_timer.message('publish_MSE_data')
        if P['agent_choice'] == 'human':
            human_val = 1
        else:
            human_val = 0
        P['human_agent_pub'].publish(std_msgs.msg.Int32(human_val))            
        P['steer_pub'].publish(std_msgs.msg.Int32(P['human']['servo_percent']))
        P['motor_pub'].publish(std_msgs.msg.Int32(P['human']['motor_percent']))
        P['button_number_pub'].publish(std_msgs.msg.Int32(P['mse']['button_number']))
        P['behavioral_mode_pub'].publish(P['behavioral_mode_choice'])
        P['encoder_pub'].publish(std_msgs.msg.Float32(P['mse']['encoder']))

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
    Arduinos = assign_serial_connections(get_arduino_serial_connections(baudrate,timeout))
    if Parameters['USE_MSE'] and 'MSE' in Arduinos.keys():
        Tactic_RC_controller = TACTIC_RC_controller(Arduinos['MSE'],Parameters)
        Calibration_mode = Calibration_Mode(Tactic_RC_controller,Parameters)
        Selector_mode = Selector_Mode(Tactic_RC_controller,Parameters)
    else:
        spd2s("!!!!!!!!!! 'MSE' not in Arduinos[] or not using 'MSE' !!!!!!!!!!!")
    if Parameters['USE_SIG'] and 'SIG' in Arduinos.keys():
        pass
        LED_display = LED_Display(Arduinos['SIG'],Parameters)
    else:
        spd2s("!!!!!!!!!! 'SIG' not in Arduinos[] or not using 'SIG' !!!!!!!!!!!")
    if Parameters['USE_IMU'] and 'IMU' in Arduinos.keys():
        pass
        IMU_arduino = IMU_Arduino(Arduinos['IMU'],Parameters)
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
    #if 'SIG' in Arduinos:
    #    Arduinos['SIG'].write('(11119)')
    #    time.sleep(0.5)
    Parameters['ABORT'] = True
    print 'done.'
    #if Parameters['USE_ROS']:
    #    print "doing... unix(opjh('kzpy3/kill_ros.sh'))"
    #    unix(opjh('kzpy3/kill_ros.sh'))

#EOF
