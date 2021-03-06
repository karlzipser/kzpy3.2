#!/usr/bin/env python

from kzpy3.utils3 import *
#from arduino_utils.arduino_menu_thread import *
#exec(menu_exec_str)


import default_values
P = default_values.P
P['ABORT'] = False


from arduino_utils.serial_init import *
from arduino_utils.tactic_rc_controller import *
from arduino_utils.calibration_mode import *
import arduino_utils.IMU_arduino
from arduino_utils.FLEX_arduino import *
# if P['use menu']:

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



if P['Desktop version']:
    P['motor_pwm_null'] = 1100
    P['motor_pwm_max'] = 1900
    P['motor_pwm_min'] = 200
    P['servo_pwm_null'] = 1100
    P['servo_pwm_max'] = 1750
    P['servo_pwm_min'] = 300
    P['servo_pwm'] = P['servo_pwm_null']
    P['motor_pwm'] = P['motor_pwm_null']
    P['button_pwm'] = 1700
    P['encoder'] = 3.0
    P['calibrated'] = True
    P['drive_mode'] = 1
    def steer__callback(msg):
        P['servo_pwm'] = servo_percent_to_pwm(msg.data,P)
    def motor__callback(msg):
        P['motor_pwm'] = motor_percent_to_pwm(msg.data,P)
    def button_number__callback(msg):
        if msg.data == 1:
            P['button_pwm'] = 1900
        elif msg.data == 2:
            P['button_pwm'] = 1700 
        elif msg.data == 3:
            P['button_pwm'] = 1424 
        elif msg.data == 4:
            P['button_pwm'] = 870 
    def encoder__callback(msg):
        P['encoder'] = msg.data
    rospy.Subscriber('/bair_car/steer', std_msgs.msg.Int32, callback=steer__callback)
    rospy.Subscriber('/bair_car/motor', std_msgs.msg.Int32, callback=motor__callback)
    rospy.Subscriber('/bair_car/encoder', std_msgs.msg.Float32, callback=encoder__callback)
    rospy.Subscriber('/bair_car/button_number', std_msgs.msg.Int32, callback=button_number__callback)




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

from default_values import flex_names
for name in flex_names:
    P[d2n(name,'_pub')] = rospy.Publisher(name,std_msgs.msg.Int32,queue_size=5)


imu_dic = {}
imu_dic['gyro'] = 'gyro_pub'
imu_dic['acc'] = 'acc_pub'
imu_dic['head'] = 'gyro_heading_pub'

MSE_low_frequency_pub_timer = Timer(0.1)

def _publish_IMU_data(P,m):
    if P['Desktop version']:
        return
    P[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*P[m]['xyz']))

def _publish_FLEX_data(P,m):
    if P['Desktop version']:
        return
    P[d2n(m,'_pub')].publish(std_msgs.msg.Int32(P[m]))

def _publish_MSE_data(P):
    if P['Desktop version']:
        return
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
P['publish_FLEX_data'] = _publish_FLEX_data
#cr("P['publish_FLEX_data'] = _publish_FLEX_data")


if P['Desktop version']:
    class Mock_Arduino:
        def __init__(self):
            pass
        def write(self,write_str):
            pass
        def readline(self):
            return "('invalid arduino line')"
        def flushInput(self):
            pass
        def flushOutput(self):
            pass
    P['Arduinos'] = {}
    P['Arduinos']['MSE'] = Mock_Arduino()
    P['Arduinos']['IMU'] = Mock_Arduino()
    P['Arduinos']['SOUND'] = Mock_Arduino()
    P['Arduinos']['FLEX'] = Mock_Arduino()

else:
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

if 'FLEX' in P['Arduinos'].keys():
    FLEX_Arduino(P)
else:
    spd2s("!!!!!!!!!! 'FLEX' not in Arduinos[] or not using 'FLEX' !!!!!!!!!!!")




            
if 'Main loop...':
    print 'main loop'
    
    import kzpy3.Menu_app.menu2 as menu2

    parameter_file_load_timer = Timer(0.5)

    while P['ABORT'] == False:

        try:
            time.sleep(1)
            if parameter_file_load_timer.check():

                #print 'arduino load topics'

                if P['button_number'] == 4 or P['Desktop version']:
                    #cr('temp. reloading')
                    Topics = menu2.load_Topics(
                        opjk("Cars/n11Dec2018/nodes"),
                        first_load=False,
                        customer='Arduino')

                    if type(Topics) == dict:
                        for t in Topics['To Expose']['Arduino']:
                            if '!' in t:
                                pass
                            else:
                                P[t] = Topics[t]
                    parameter_file_load_timer.reset()

            else:
            
                time.sleep(0.1)

        except Exception as e:
            CS_(d2s('Main loop exception',e))
        

CS('End arduino_node.py main loop.')
CS_("doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))")
time.sleep(0.01)
os.system(opjh('kzpy3/scripts/kill_ros.sh'))


#EOF
