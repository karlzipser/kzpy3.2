#!/usr/bin/env python

from kzpy3.utils3 import *
#from arduino_utils.arduino_menu_thread import *
#exec(menu_exec_str)



import kzpy3.Cars.n11Oct2018_car_with_nets.nodes.Default_values.arduino.default_values as default_values
P = default_values.P
P['ABORT'] = False

while P['ABORT'] == False:
    time.sleep(1)

from arduino_utils.serial_init import *
from arduino_utils.tactic_rc_controller import *
from arduino_utils.calibration_mode import *
import arduino_utils.IMU_arduino
#if P['use menu']:

exec(identify_file_str)


#import Default_values.arduino.default_values

#P = Default_values.arduino.default_values.P

import std_msgs.msg
import geometry_msgs.msg
import rospy
import sensor_msgs.msg

P['zed_called']['val'] = 0
P['zed_called']['time'] = 0

def zed_callback(data):
    P['zed_called']['val'] += 1
    P['zed_called']['time'] = time.time()


if P['use LIDAR']:
    P['os1_called']['val'] = 0
    P['os1_called']['time'] = 0
    def os1_callback(data):
        P['os1_called']['val'] += 1
        P['os1_called']['time'] = time.time()






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

if P['use LIDAR']:
    rospy.Subscriber("/os1_node/points",sensor_msgs.msg.PointCloud2,os1_callback,queue_size=1)
rospy.Subscriber("/bair_car/zed/right/image_rect_color",sensor_msgs.msg.Image,zed_callback,queue_size=1)

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

imu_dic = {}
imu_dic['gyro'] = 'gyro_pub'
imu_dic['acc'] = 'acc_pub'
imu_dic['head'] = 'gyro_heading_pub'

MSE_low_frequency_pub_timer = Timer(0.1)

def _publish_IMU_data(P,m):
    P[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*P[m]['xyz']))

def _publish_MSE_data(P):
    P['steer_pub'].publish(std_msgs.msg.Int32(P['human']['servo_percent']))
    P['motor_pub'].publish(std_msgs.msg.Int32(P['human']['motor_percent']))
    P['button_number_pub'].publish(std_msgs.msg.Int32(P['button_number']))
    P['encoder_pub'].publish(std_msgs.msg.Float32(P['encoder']))
    if MSE_low_frequency_pub_timer.check():
        if P['button_number'] == 1:
            behavioral_mode_choice = 'left'
        elif P['button_number'] == 2:
            behavioral_mode_choice = 'direct'
        elif P['button_number'] == 3:
            behavioral_mode_choice = 'right'
        else:
            behavioral_mode_choice = 'calibrate'
        P['behavioral_mode_pub'].publish(d2s(behavioral_mode_choice))
        if P['agent_is_human'] == True:
            P['human_agent_pub'].publish(std_msgs.msg.Int32(1))
        elif P['agent_is_human'] == False:
            P['human_agent_pub'].publish(std_msgs.msg.Int32(0))
        else:
            assert False

        if P['button_number'] == 4:
            P['drive_mode'] = 0 #drive_mode = 0
        else:
            P['drive_mode'] = 1 #drive_mode = 1
        P['drive_mode_pub'].publish(std_msgs.msg.Int32(P['drive_mode']))
        MSE_low_frequency_pub_timer.reset()

P['publish_IMU_data'] = _publish_IMU_data
P['publish_MSE_data'] = _publish_MSE_data

if 'Start Arduino threads...':
    baudrate = 115200
    timeout = 0.1
    assign_serial_connections(P,get_arduino_serial_connections(baudrate,timeout))

    if P['USE_MSE'] and 'MSE' in P['Arduinos'].keys():     
        CS("!!!!!!!!!! found 'MSE' !!!!!!!!!!!",emphasis=True)
        #print 0,P['publish_MSE_data']
        TACTIC_RC_controller(P)
        #print 1,P['publish_MSE_data']
        Calibration_Mode(P)
    else:
        assert False
        
    if P['USE_IMU'] and 'IMU' in P['Arduinos'].keys():
        arduino_utils.IMU_arduino.IMU_Arduino(P)
    else:
        CS("!!!!!!!!!! 'IMU' not in Arduinos[] or not using 'IMU' !!!!!!!!!!!",exception=True)

    #P['agent_is_human'] = 'human'



            
if 'Main loop...':
    print 'main loop'
    
    import kzpy3.Menu_app.menu2 as menu2

    parameter_file_load_timer = Timer(0.5)

    while P['ABORT'] == False:

        try:
            time.sleep(1)
            if parameter_file_load_timer.check():

                #print 'arduino load topics'

                if P['button_number'] == 4:

                    Topics = menu2.load_Topics(
                        opjk("Cars/n11Oct2018_car_with_nets/nodes/Default_values/arduino"),
                        first_load=False,
                        customer='Arduino Node')

                    if type(Topics) == dict:
                        for t in Topics['To Expose']['Arduino Node']:
                            if '!' in t:
                                pass
                            else:
                                P[t] = Topics[t]
                    parameter_file_load_timer.reset()

            else:
                time.sleep(0.1)





            #if 'SOUND' in P['Arduinos']:
            #    pass #P['Arduinos']['SOUND'].write("(22)")

            #Default_values.arduino.default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)

        except Exception as e:
            CS_(d2s('Main loop exception',e))
            #Default_values.arduino.default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)
        

CS('End arduino_node.py main loop.')
CS_("doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))")
time.sleep(0.01)
unix(opjh('kzpy3/scripts/kill_ros.sh'))
#EOF
