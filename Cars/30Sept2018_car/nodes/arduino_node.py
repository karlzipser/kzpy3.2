#!/usr/bin/env python
"""
python kzpy3/Cars/30Sept2018_car/nodes/arduino_node.py
"""
from kzpy3.utils3 import *

from arduino_utils.serial_init import *
from arduino_utils.tactic_rc_controller import *
from arduino_utils.calibration_mode import *
from arduino_utils.selector_mode import *
if False:
    from arduino_utils.FLEX_arduino import *

exec(identify_file_str)

import Default_values.arduino.default_values

P = Default_values.arduino.default_values.Parameters

import std_msgs.msg
import geometry_msgs.msg
import rospy

def cmd_steer_callback(msg):
    P['network']['servo_percent'] = msg.data
def cmd_camera_callback(msg):
    P['network']['camera_percent'] = msg.data
def cmd_motor_callback(msg):
    P['network']['motor_percent'] = msg.data

rospy.init_node('run_arduino',anonymous=True,disable_signals=True)
rospy.Subscriber('cmd/steer', std_msgs.msg.Int32, callback=cmd_steer_callback)
rospy.Subscriber('cmd/camera', std_msgs.msg.Int32, callback=cmd_camera_callback)
rospy.Subscriber('cmd/motor', std_msgs.msg.Int32, callback=cmd_motor_callback)

P['human_agent_pub'] = rospy.Publisher('human_agent', std_msgs.msg.Int32, queue_size=5) 
P['drive_mode_pub'] = rospy.Publisher('drive_mode', std_msgs.msg.Int32, queue_size=5) 
P['behavioral_mode_pub'] = rospy.Publisher('behavioral_mode', std_msgs.msg.String, queue_size=5)
P['place_choice_pub'] = rospy.Publisher('place_choice', std_msgs.msg.String, queue_size=5)
P['button_number_pub'] = rospy.Publisher('button_number', std_msgs.msg.Int32, queue_size=5) 
P['steer_pub'] = rospy.Publisher('steer', std_msgs.msg.Int32, queue_size=5) 
P['motor_pub'] = rospy.Publisher('motor', std_msgs.msg.Int32, queue_size=5) 
P['encoder_pub'] = rospy.Publisher('encoder', std_msgs.msg.Float32, queue_size=5)
P['gyro_pub'] = rospy.Publisher('gyro', geometry_msgs.msg.Vector3, queue_size=10)
P['gyro_heading_pub'] = rospy.Publisher('gyro_heading', geometry_msgs.msg.Vector3, queue_size=10)
P['acc_pub'] = rospy.Publisher('acc', geometry_msgs.msg.Vector3, queue_size=10)
P['servo_pwm_min_pub'] = rospy.Publisher('servo_pwm_min', std_msgs.msg.Int32, queue_size=5) 
P['servo_pwm_max_pub'] = rospy.Publisher('servo_pwm_max', std_msgs.msg.Int32, queue_size=5) 
P['servo_pwm_null_pub'] = rospy.Publisher('servo_pwm_null', std_msgs.msg.Int32, queue_size=5) 
P['motor_pwm_min_pub'] = rospy.Publisher('motor_pwm_min', std_msgs.msg.Int32, queue_size=5) 
P['motor_pwm_null_pub'] = rospy.Publisher('motor_pwm_null', std_msgs.msg.Int32, queue_size=5) 
P['motor_pwm_max_pub'] = rospy.Publisher('motor_pwm_max', std_msgs.msg.Int32, queue_size=5)

if False:
    P['GPS_latitudeDegrees_pub'] = rospy.Publisher('GPS_latitudeDegrees', std_msgs.msg.Float64, queue_size=5)
    P['GPS_longitudeDegrees_pub'] = rospy.Publisher('GPS_longitudeDegrees', std_msgs.msg.Float64, queue_size=5)
    P['GPS_speed_pub'] = rospy.Publisher('GPS_speed', std_msgs.msg.Float32, queue_size=5)
    P['GPS_angle_pub'] = rospy.Publisher('GPS_angle', std_msgs.msg.Float32, queue_size=5)
    P['GPS_altitude_pub'] = rospy.Publisher('GPS_altitude', std_msgs.msg.Float32, queue_size=5)
    P['GPS_fixquality_pub'] = rospy.Publisher('GPS_fixquality', std_msgs.msg.Int32, queue_size=5)
    P['GPS_satellites_pub'] = rospy.Publisher('GPS_satellites', std_msgs.msg.Int32, queue_size=5)

if False:
    from Default_values.arduino.default_values import flex_names
    for name in flex_names:
        P[d2n(name,'_pub')] = rospy.Publisher(name,std_msgs.msg.Int32,queue_size=5)

imu_dic = {}
imu_dic['gyro'] = 'gyro_pub'
imu_dic['acc'] = 'acc_pub'
imu_dic['head'] = 'gyro_heading_pub'

IMU_low_frequency_pub_timer = Timer(0.5)
MSE_low_frequency_pub_timer = Timer(0.1)
MSE_very_low_frequency_pub_timer = Timer(2)
No_Arduino_data_low_frequency_pub_timer = Timer(0.5)
No_Arduino_data_very_low_frequency_pub_timer = Timer(2)

def _publish_IMU_data(P,m):
    P[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*P[m]['xyz']))

def _publish_FLEX_data(P,m):
    P[d2n(m,'_pub')].publish(std_msgs.msg.Int32(P[m]))

if False:
    def _publish_GPS_data(P):
        P['GPS_latitudeDegrees_pub'].publish(std_msgs.msg.Float64(P['GPS_latitudeDegrees']))
        P['GPS_longitudeDegrees_pub'].publish(std_msgs.msg.Float64(P['GPS_longitudeDegrees']))
        P['GPS_speed_pub'].publish(std_msgs.msg.Float32(P['GPS_speed']))
        P['GPS_angle_pub'].publish(std_msgs.msg.Float32(P['GPS_angle']))
        P['GPS_altitude_pub'].publish(std_msgs.msg.Float32(P['GPS_altitude']))
        P['GPS_fixquality_pub'].publish(std_msgs.msg.Int32(P['GPS_fixquality']))
        P['GPS_satellites_pub'].publish(std_msgs.msg.Int32(P['GPS_satellites']))

def _publish_MSE_data(P):
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
        if P['button_number'] == 1:
            behavioral_mode_choice = 'left'
        elif P['button_number'] == 3:
            behavioral_mode_choice = 'right'
        else:
            behavioral_mode_choice = P['behavioral_mode_choice']
        P['behavioral_mode_pub'].publish(d2s(behavioral_mode_choice))
        P['human_agent_pub'].publish(std_msgs.msg.Int32(human_val))
        P['drive_mode_pub'].publish(std_msgs.msg.Int32(drive_mode))
        P['Hz_mse_pub'].publish(std_msgs.msg.Float32(P['Hz']['mse']))
        MSE_low_frequency_pub_timer.reset()

    if MSE_very_low_frequency_pub_timer.check():
        P['place_choice_pub'].publish(d2s(P['place_choice']))
        P['servo_pwm_min_pub'].publish(std_msgs.msg.Int32(P['servo_pwm_min']))
        P['servo_pwm_max_pub'].publish(std_msgs.msg.Int32(P['servo_pwm_max']))
        P['servo_pwm_null_pub'].publish(std_msgs.msg.Int32(int(P['servo_pwm_null'])))
        P['motor_pwm_min_pub'].publish(std_msgs.msg.Int32(P['motor_pwm_min']))
        P['motor_pwm_max_pub'].publish(std_msgs.msg.Int32(P['motor_pwm_max']))
        P['motor_pwm_null_pub'].publish(std_msgs.msg.Int32(int(P['motor_pwm_null'])))
        MSE_very_low_frequency_pub_timer.reset()

def _publish_No_Arduino_data(P):
    human_val = 0
    drive_mode = 1
    while (not P['ABORT']) and (not rospy.is_shutdown()):
        time.sleep(0.001)
        if No_Arduino_data_low_frequency_pub_timer.check():
            P['behavioral_mode_pub'].publish(std_msgs.msg.String(Default_values.arduino.default_values.NO_Mse['behavioral_mode_choice'])) 
            P['place_choice_pub'].publish(std_msgs.msg.String(Default_values.arduino.default_values.NO_Mse['place_choice']))
            P['human_agent_pub'].publish(std_msgs.msg.Int32(human_val))
            P['drive_mode_pub'].publish(std_msgs.msg.Int32(drive_mode))
            No_Arduino_data_low_frequency_pub_timer.reset()
        if No_Arduino_data_very_low_frequency_pub_timer.check():
            No_Arduino_data_very_low_frequency_pub_timer.reset()

P['publish_IMU_data'] = _publish_IMU_data
P['publish_MSE_data'] = _publish_MSE_data
P['publish_FLEX_data'] = _publish_FLEX_data
#P['publish_GPS_data'] = _publish_GPS_data

if 'Start Arduino threads...':
    baudrate = 115200
    timeout = 0.1
    assign_serial_connections(P,get_arduino_serial_connections(baudrate,timeout))

    if P['USE_MSE'] and 'MSE' in P['Arduinos'].keys():
        CS("!!!!!!!!!! found 'MSE' !!!!!!!!!!!",emphasis=True)
        P['Arduinos']['MSE'].write("(-1,-1,-1,-1,-1,-1,-1)")
        # signal success with sound
        TACTIC_RC_controller(P)
        Calibration_Mode(P)
        Selector_Mode(P)
    else:
        # signal failure with sound
        CS("!!!!!!!!!! 'MSE' not in Arduinos[] or not using 'MSE' !!!!!!!!!!!",exception=True)
        #P['Arduinos']['MSE'].write("(-2)")
        threading.Thread(target=_publish_No_Arduino_data,args=[P]).start()

            
if 'Main loop...':
    print 'main loop'
    q = '_'
    try:
        while q not in ['q','Q']:
            q = raw_input('')
            if P['ABORT']:
                break
            time.sleep(0.1)
        Default_values.arduino.default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)
    except Exception as e:
        CS_(d2s('Main loop exception',e))
CS_('End arduino_node.py main loop.')

#EOF
