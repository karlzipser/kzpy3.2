#!/usr/bin/env python
"""
python kzpy3/Cars/car_16July2018/nodes/arduino_node.py
"""
from kzpy3.utils3 import *

from arduino_utils.serial_init import *
from arduino_utils.tactic_rc_controller import *
from arduino_utils.calibration_mode import *
from arduino_utils.selector_mode import *
from arduino_utils.led_display import *
from arduino_utils.IMU_arduino import *
from arduino_utils.FLEX_arduino import *

exec(identify_file_str)

import Default_values.arduino.default_values

Parameters = Default_values.arduino.default_values.Parameters

"""
import kzpy3.Menu_app.menu
menu_path = Parameters['The menu path.']
if not os.path.exists(menu_path):
    os.makedirs(menu_path)
try:
    os.remove(opj(path,'ready'))
except:
    pass
threading.Thread(target=kzpy3.Menu_app.menu.load_menu_data,args=[menu_path,Parameters]).start()
"""

import std_msgs.msg
import geometry_msgs.msg
import rospy
import sensor_msgs.msg

zed_called = 0
def zed_callback(data):
    global zed_called
    zed_called += 1

os1_called = 0
def os1_callback(data):
    global os1_called
    os1_called += 1
    
rospy.Subscriber("/os1_node/points",sensor_msgs.msg.PointCloud2,os1_callback,queue_size=1)
rospy.Subscriber("/bair_car/zed/right/image_rect_color",sensor_msgs.msg.Image,zed_callback,queue_size=1)





def cmd_steer_callback(msg):
    Parameters['network']['servo_percent'] = msg.data
def cmd_camera_callback(msg):
    Parameters['network']['camera_percent'] = msg.data
def cmd_motor_callback(msg):
    Parameters['network']['motor_percent'] = msg.data

rospy.init_node('run_arduino',anonymous=True,disable_signals=True)
rospy.Subscriber('cmd/steer', std_msgs.msg.Int32, callback=cmd_steer_callback)
rospy.Subscriber('cmd/camera', std_msgs.msg.Int32, callback=cmd_camera_callback)
rospy.Subscriber('cmd/motor', std_msgs.msg.Int32, callback=cmd_motor_callback)

Parameters['human_agent_pub'] = rospy.Publisher('human_agent', std_msgs.msg.Int32, queue_size=5) 
Parameters['drive_mode_pub'] = rospy.Publisher('drive_mode', std_msgs.msg.Int32, queue_size=5) 
Parameters['behavioral_mode_pub'] = rospy.Publisher('behavioral_mode', std_msgs.msg.String, queue_size=5)
Parameters['place_choice_pub'] = rospy.Publisher('place_choice', std_msgs.msg.String, queue_size=5)
Parameters['button_number_pub'] = rospy.Publisher('button_number', std_msgs.msg.Int32, queue_size=5) 
Parameters['steer_pub'] = rospy.Publisher('steer', std_msgs.msg.Int32, queue_size=5) 
Parameters['motor_pub'] = rospy.Publisher('motor', std_msgs.msg.Int32, queue_size=5) 
Parameters['encoder_pub'] = rospy.Publisher('encoder', std_msgs.msg.Float32, queue_size=5)
Parameters['Hz_acc_pub'] = rospy.Publisher('Hz_acc', std_msgs.msg.Float32, queue_size=5)
Parameters['Hz_mse_pub'] = rospy.Publisher('Hz_mse', std_msgs.msg.Float32, queue_size=5)
Parameters['gyro_pub'] = rospy.Publisher('gyro', geometry_msgs.msg.Vector3, queue_size=10)
Parameters['gyro_heading_pub'] = rospy.Publisher('gyro_heading', geometry_msgs.msg.Vector3, queue_size=10)
Parameters['acc_pub'] = rospy.Publisher('acc', geometry_msgs.msg.Vector3, queue_size=10)
Parameters['servo_pwm_min_pub'] = rospy.Publisher('servo_pwm_min', std_msgs.msg.Int32, queue_size=5) 
Parameters['servo_pwm_max_pub'] = rospy.Publisher('servo_pwm_max', std_msgs.msg.Int32, queue_size=5) 
Parameters['servo_pwm_null_pub'] = rospy.Publisher('servo_pwm_null', std_msgs.msg.Int32, queue_size=5) 
Parameters['motor_pwm_min_pub'] = rospy.Publisher('motor_pwm_min', std_msgs.msg.Int32, queue_size=5) 
Parameters['motor_pwm_null_pub'] = rospy.Publisher('motor_pwm_null', std_msgs.msg.Int32, queue_size=5) 
Parameters['motor_pwm_max_pub'] = rospy.Publisher('motor_pwm_max', std_msgs.msg.Int32, queue_size=5)

Parameters['GPS_latitudeDegrees_pub'] = rospy.Publisher('GPS_latitudeDegrees', std_msgs.msg.Float64, queue_size=5)
Parameters['GPS_longitudeDegrees_pub'] = rospy.Publisher('GPS_longitudeDegrees', std_msgs.msg.Float64, queue_size=5)
Parameters['GPS_speed_pub'] = rospy.Publisher('GPS_speed', std_msgs.msg.Float32, queue_size=5)
Parameters['GPS_angle_pub'] = rospy.Publisher('GPS_angle', std_msgs.msg.Float32, queue_size=5)
Parameters['GPS_altitude_pub'] = rospy.Publisher('GPS_altitude', std_msgs.msg.Float32, queue_size=5)
Parameters['GPS_fixquality_pub'] = rospy.Publisher('GPS_fixquality', std_msgs.msg.Int32, queue_size=5)
Parameters['GPS_satellites_pub'] = rospy.Publisher('GPS_satellites', std_msgs.msg.Int32, queue_size=5)

from Default_values.arduino.default_values import flex_names
for name in flex_names:
    Parameters[d2n(name,'_pub')] = rospy.Publisher(name,std_msgs.msg.Int32,queue_size=5)

imu_dic = {}
imu_dic['gyro'] = 'gyro_pub'
imu_dic['acc'] = 'acc_pub'
imu_dic['head'] = 'gyro_heading_pub'

IMU_low_frequency_pub_timer = Timer(0.5)
MSE_low_frequency_pub_timer = Timer(0.1)
MSE_very_low_frequency_pub_timer = Timer(2)
No_Arduino_data_low_frequency_pub_timer = Timer(0.5)
No_Arduino_data_very_low_frequency_pub_timer = Timer(2)

def _publish_IMU_data(Parameters,m):
    Parameters[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*Parameters[m]['xyz']))
    if IMU_low_frequency_pub_timer.check():
        Parameters['Hz_acc_pub'].publish(std_msgs.msg.Float32(Parameters['Hz']['acc']))
        IMU_low_frequency_pub_timer.reset()

def _publish_FLEX_data(Parameters,m):
    Parameters[d2n(m,'_pub')].publish(std_msgs.msg.Int32(Parameters[m]))

def _publish_GPS_data(Parameters):
    Parameters['GPS_latitudeDegrees_pub'].publish(std_msgs.msg.Float64(Parameters['GPS_latitudeDegrees']))
    Parameters['GPS_longitudeDegrees_pub'].publish(std_msgs.msg.Float64(Parameters['GPS_longitudeDegrees']))
    Parameters['GPS_speed_pub'].publish(std_msgs.msg.Float32(Parameters['GPS_speed']))
    Parameters['GPS_angle_pub'].publish(std_msgs.msg.Float32(Parameters['GPS_angle']))
    Parameters['GPS_altitude_pub'].publish(std_msgs.msg.Float32(Parameters['GPS_altitude']))
    Parameters['GPS_fixquality_pub'].publish(std_msgs.msg.Int32(Parameters['GPS_fixquality']))
    Parameters['GPS_satellites_pub'].publish(std_msgs.msg.Int32(Parameters['GPS_satellites']))

def _publish_MSE_data(Parameters):
    if Parameters['agent_choice'] == 'human':
        human_val = 1
    else:
        human_val = 0
    if Parameters['selector_mode'] == 'drive_mode':
        drive_mode = 1
    else:
        drive_mode = 0
    Parameters['steer_pub'].publish(std_msgs.msg.Int32(Parameters['human']['servo_percent']))
    Parameters['motor_pub'].publish(std_msgs.msg.Int32(Parameters['human']['motor_percent']))
    Parameters['button_number_pub'].publish(std_msgs.msg.Int32(Parameters['button_number']))
    Parameters['encoder_pub'].publish(std_msgs.msg.Float32(Parameters['encoder']))

    if MSE_low_frequency_pub_timer.check():
        if Parameters['button_number'] == 1:
            behavioral_mode_choice = 'left'
        elif Parameters['button_number'] == 3:
            behavioral_mode_choice = 'right'
        else:
            behavioral_mode_choice = Parameters['behavioral_mode_choice']
        Parameters['behavioral_mode_pub'].publish(d2s(behavioral_mode_choice))
        Parameters['human_agent_pub'].publish(std_msgs.msg.Int32(human_val))
        Parameters['drive_mode_pub'].publish(std_msgs.msg.Int32(drive_mode))
        Parameters['Hz_mse_pub'].publish(std_msgs.msg.Float32(Parameters['Hz']['mse']))
        MSE_low_frequency_pub_timer.reset()

    if MSE_very_low_frequency_pub_timer.check():
        Parameters['place_choice_pub'].publish(d2s(Parameters['place_choice']))
        Parameters['servo_pwm_min_pub'].publish(std_msgs.msg.Int32(Parameters['servo_pwm_min']))
        Parameters['servo_pwm_max_pub'].publish(std_msgs.msg.Int32(Parameters['servo_pwm_max']))
        Parameters['servo_pwm_null_pub'].publish(std_msgs.msg.Int32(int(Parameters['servo_pwm_null'])))
        Parameters['motor_pwm_min_pub'].publish(std_msgs.msg.Int32(Parameters['motor_pwm_min']))
        Parameters['motor_pwm_max_pub'].publish(std_msgs.msg.Int32(Parameters['motor_pwm_max']))
        Parameters['motor_pwm_null_pub'].publish(std_msgs.msg.Int32(int(Parameters['motor_pwm_null'])))
        MSE_very_low_frequency_pub_timer.reset()
def _publish_No_Arduino_data(Parameters):
    human_val = 0
    drive_mode = 1
    while (not Parameters['ABORT']) and (not rospy.is_shutdown()):
        time.sleep(0.001)
        if No_Arduino_data_low_frequency_pub_timer.check():
            Parameters['behavioral_mode_pub'].publish(std_msgs.msg.String(Default_values.arduino.default_values.NO_Mse['behavioral_mode_choice'])) 
            Parameters['place_choice_pub'].publish(std_msgs.msg.String(Default_values.arduino.default_values.NO_Mse['place_choice']))
            Parameters['human_agent_pub'].publish(std_msgs.msg.Int32(human_val))
            Parameters['drive_mode_pub'].publish(std_msgs.msg.Int32(drive_mode))
            No_Arduino_data_low_frequency_pub_timer.reset()
        if No_Arduino_data_very_low_frequency_pub_timer.check():
            No_Arduino_data_very_low_frequency_pub_timer.reset()

Parameters['publish_IMU_data'] = _publish_IMU_data
Parameters['publish_MSE_data'] = _publish_MSE_data
Parameters['publish_FLEX_data'] = _publish_FLEX_data
Parameters['publish_GPS_data'] = _publish_GPS_data

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
        threading.Thread(target=_publish_No_Arduino_data,args=[Parameters]).start()
    if Parameters['USE_SIG'] and 'SIG' in Parameters['Arduinos'].keys():
        LED_Display(Parameters)
    else:
        spd2s("!!!!!!!!!! 'SIG' not in Arduinos[] or not using 'SIG' !!!!!!!!!!!")
    if Parameters['USE_IMU'] and 'IMU' in Parameters['Arduinos'].keys():
        IMU_Arduino(Parameters)
    else:
        spd2s("!!!!!!!!!! 'IMU' not in Arduinos[] or not using 'IMU' !!!!!!!!!!!")
    if 'FLEX' in Parameters['Arduinos'].keys():
        FLEX_Arduino(Parameters)
    else:
        spd2s("!!!!!!!!!! 'FLEX' not in Arduinos[] or not using 'FLEX' !!!!!!!!!!!")
            
if 'Main loop...':
    print 'main loop'
    q = '_'
    try:
        while q not in ['q','Q']:
            q = raw_input('')
            if Parameters['ABORT']:
                break
            time.sleep(0.1)
        Default_values.arduino.default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)
    except Exception as e:
        CS_(d2s('Main loop exception',e))
CS_('End arduino_node.py main loop.')

#EOF