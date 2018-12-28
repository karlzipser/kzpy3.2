#!/usr/bin/env python

from kzpy3.utils3 import *
import default_values
_ = default_values.P
import std_msgs.msg
import geometry_msgs.msg
import rospy
import sensor_msgs.msg
exec(identify_file_str)

###########################################################################################
#
def cmd_steer_callback(msg):
    _['network']['servo_percent'] = msg.data
def cmd_camera_callback(msg):
    _['network']['camera_percent'] = msg.data
def cmd_motor_callback(msg):
    _['network']['motor_percent'] = msg.data

rospy.init_node('run_arduino',anonymous=True,disable_signals=True)
rospy.Subscriber('cmd/steer', std_msgs.msg.Int32, callback=cmd_steer_callback)
rospy.Subscriber('cmd/camera', std_msgs.msg.Int32, callback=cmd_camera_callback)
rospy.Subscriber('cmd/motor', std_msgs.msg.Int32, callback=cmd_motor_callback)

_['human_agent_pub'] = rospy.Publisher('human_agent', std_msgs.msg.Int32, queue_size=5) 
_['drive_mode_pub'] = rospy.Publisher('drive_mode', std_msgs.msg.Int32, queue_size=5) 
_['behavioral_mode_pub'] = rospy.Publisher('behavioral_mode', std_msgs.msg.String, queue_size=5)
_['place_choice_pub'] = rospy.Publisher('place_choice', std_msgs.msg.String, queue_size=5)
_['button_number_pub'] = rospy.Publisher('button_number', std_msgs.msg.Int32, queue_size=5) 
_['steer_pub'] = rospy.Publisher('steer', std_msgs.msg.Int32, queue_size=5) 
_['motor_pub'] = rospy.Publisher('motor', std_msgs.msg.Int32, queue_size=5) 
_['encoder_pub'] = rospy.Publisher('encoder', std_msgs.msg.Float32, queue_size=5)
_['gyro_pub'] = rospy.Publisher('gyro', geometry_msgs.msg.Vector3, queue_size=10)
_['gyro_heading_pub'] = rospy.Publisher('gyro_heading', geometry_msgs.msg.Vector3, queue_size=10)
_['acc_pub'] = rospy.Publisher('acc', geometry_msgs.msg.Vector3, queue_size=10)
_['servo_pwm_min_pub'] = rospy.Publisher('servo_pwm_min', std_msgs.msg.Int32, queue_size=5) 
_['servo_pwm_max_pub'] = rospy.Publisher('servo_pwm_max', std_msgs.msg.Int32, queue_size=5) 
_['servo_pwm_null_pub'] = rospy.Publisher('servo_pwm_null', std_msgs.msg.Int32, queue_size=5) 
_['motor_pwm_min_pub'] = rospy.Publisher('motor_pwm_min', std_msgs.msg.Int32, queue_size=5) 
_['motor_pwm_null_pub'] = rospy.Publisher('motor_pwm_null', std_msgs.msg.Int32, queue_size=5) 
_['motor_pwm_max_pub'] = rospy.Publisher('motor_pwm_max', std_msgs.msg.Int32, queue_size=5)

from default_values import flex_names
for name in flex_names:
    _[d2n(name,'_pub')] = rospy.Publisher(name,std_msgs.msg.Int32,queue_size=5)

imu_rename_dic = {}
imu_rename_dic['gyro'] = 'gyro_pub'
imu_rename_dic['acc'] = 'acc_pub'
imu_rename_dic['head'] = 'gyro_heading_pub'

MSE_low_frequency_pub_timer = Timer(0.1)

def _publish_IMU_data(_,m):
    _[imu_rename_dic[m]].publish(geometry_msgs.msg.Vector3(*_[m]['xyz']))

def _publish_FLEX_data(_,m):
    _[d2n(m,'_pub')].publish(std_msgs.msg.Int32(_[m]))

def _publish_MSE_data(_):
    _['steer_pub'].publish(std_msgs.msg.Int32(_['human']['servo_percent']))
    _['motor_pub'].publish(std_msgs.msg.Int32(_['human']['motor_percent']))
    _['button_number_pub'].publish(std_msgs.msg.Int32(_['button_number']))
    _['encoder_pub'].publish(std_msgs.msg.Float32(_['encoder']))

    if MSE_low_frequency_pub_timer.check():

        if _['agent_is_human'] == True:
            _['human_agent_pub'].publish(std_msgs.msg.Int32(1))
        elif _['agent_is_human'] == False:
            _['human_agent_pub'].publish(std_msgs.msg.Int32(0))
        else:
            assert False

        _['drive_mode_pub'].publish(std_msgs.msg.Int32(_['drive_mode']))
        MSE_low_frequency_pub_timer.reset()

_['publish_IMU_data'] = _publish_IMU_data
_['publish_MSE_data'] = _publish_MSE_data
_['publish_FLEX_data'] = _publish_FLEX_data
#
#########################################


#########################################
#
if not _['desktop version']:
    baudrate = 115200
    timeout = 0.1
    import arduino_utils.serial_init
    assign_serial_connections(_,arduino_utils.serial_init.get_arduino_serial_connections(baudrate,timeout))

else:
    import arduino_utils.mock_arduino
    arduino_utils.mock_arduino.put_mock_Arduinos_into_P(_)
    if username != 'nvidia':
        _['desktop version/L'],_['desktop version/O'],___ = open_run(
            run_name='tegra-ubuntu_19Oct18_08h55m02s',
            h5py_path=opjD('Data/1_TB_Samsung_n1/tu_18to19Oct2018/locations/local/left_right_center/h5py'),
            want_list=['L','O'],
            verbose=True
        )
        _['desktop version/index'] = _['desktop version/start index']
    else:
        _['desktop version/L'],_['desktop version/O'],___ = open_run(
            run_name='tegra-ubuntu_19Oct18_08h55m02s',
            h5py_path=opjm('rosbags'),
            want_list=['L','O'],
            verbose=True
        )
        _['desktop version/index'] = _['desktop version/start index']
if _['USE_MSE'] and 'MSE' in _['Arduinos'].keys():
    import arduino_utils.tactic_rc_controller
    arduino_utils.tactic_rc_controller.TACTIC_RC_controller(_)
    CS("!!!!!!!!!! found 'MSE' !!!!!!!!!!!",emphasis=True)

    if not _['desktop version']:
        import arduino_utils.calibration_mode
        arduino_utils.calibration_mode.Calibration_Mode(_)
    else:
        _['servo_pwm_null'] = 1200
        _['motor_pwm_null'] = 1200
        _['servo_pwm_min'] = 800
        _['servo_pwm_max'] = 1600
        _['motor_pwm_min'] = 800
        _['motor_pwm_max'] = 1600
        _['servo_pwm_smooth'] = _['servo_pwm_null']
        _['motor_pwm_smooth'] = _['motor_pwm_null']
        _['calibrated'] = True
else:
    assert False
    
if _['USE_IMU'] and 'IMU' in _['Arduinos'].keys():
    import arduino_utils.IMU_arduino
    arduino_utils.IMU_arduino.IMU_Arduino(_)

else:
    spd2s("!!!!!!!!!! 'IMU' not in Arduinos[] or not using 'IMU' !!!!!!!!!!!",exception=True)

if _['use flex'] and 'FLEX' in _['Arduinos'].keys():
    import arduino_utils.FLEX_arduino
    arduino_utils.FLEX_arduino.FLEX_Arduino(_)
else:
    spd2s("!!!!!!!!!! 'FLEX' not in Arduinos[] or not using 'FLEX' !!!!!!!!!!!")
#
#########################################


#########################################
#
#if _['desktop version']:

#
#########################################





#########################################
#
print 'arduino_node.py main loop'

import kzpy3.Menu_app.menu2 as menu2

parameter_file_load_timer = Timer(0.5)

while _['ABORT'] == False:

    try:
        time.sleep(1)

        if parameter_file_load_timer.check():

            if True:#_['button_number'] == 4:

                Topics = menu2.load_Topics(
                    opjk("Cars/n26Dec18/nodes"),
                    first_load=False,
                    customer='Arduino')

                if type(Topics) == dict:
                    for t in Topics['To Expose']['Arduino']:
                        if '!' in t:
                            pass
                        else:
                            _[t] = Topics[t]
                parameter_file_load_timer.reset()

        else:
            time.sleep(0.1)
    except KeyboardInterrupt:
        _['ABORT'] = True
        #sys.exit()
    except Exception as e:
        print '*********** here ************'
        CS_(d2s('Main loop exception',e))
        
#
#########################################
       



CS('End arduino_node.py main loop.')
#CS_("doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))")
time.sleep(0.01)
#os.system(opjh('kzpy3/scripts/kill_ros.sh'))


#EOF
