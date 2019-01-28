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
_['data_saving'] = 0
_['data_saving_prev'] = 0
_['data_saving changed up'] = False
def cmd_steer_callback(msg):
    _['cmd/steer'] = msg.data
def cmd_camera_callback(msg):
    _['cmd/camera'] = msg.data
def cmd_motor_callback(msg):
    _['cmd/motor'] = msg.data
def data_saving_callback(msg):
    _['data_saving_prev'] = _['data_saving']
    _['data_saving'] = msg.data
    if _['data_saving'] == 1 and _['data_saving_prev'] == 0:
        _['data_saving changed up'] = True

rospy.init_node('run_arduino',anonymous=True,disable_signals=True)
rospy.Subscriber('cmd/steer', std_msgs.msg.Int32, callback=cmd_steer_callback)
rospy.Subscriber('cmd/camera', std_msgs.msg.Int32, callback=cmd_camera_callback)
rospy.Subscriber('cmd/motor', std_msgs.msg.Int32, callback=cmd_motor_callback)
rospy.Subscriber('/data_saving', std_msgs.msg.Int32, callback=data_saving_callback)

bcs = ''
if _['MOCK_ARDUINO_VERSION']:
    bcs = '/bair_car/'

_['human_agent_pub'] = rospy.Publisher(bcs+'human_agent', std_msgs.msg.Int32, queue_size=5) 
_['drive_mode_pub'] = rospy.Publisher(bcs+'drive_mode', std_msgs.msg.Int32, queue_size=5) 
_['behavioral_mode_pub'] = rospy.Publisher(bcs+'behavioral_mode', std_msgs.msg.String, queue_size=5)
_['place_choice_pub'] = rospy.Publisher(bcs+'place_choice', std_msgs.msg.String, queue_size=5)
_['button_number_pub'] = rospy.Publisher(bcs+'button_number', std_msgs.msg.Int32, queue_size=5) 
_['steer_pub'] = rospy.Publisher(bcs+'steer', std_msgs.msg.Int32, queue_size=5) 
_['motor_pub'] = rospy.Publisher(bcs+'motor', std_msgs.msg.Int32, queue_size=5) 
_['encoder_pub'] = rospy.Publisher(bcs+'encoder', std_msgs.msg.Float32, queue_size=5)
_['gyro_pub'] = rospy.Publisher(bcs+'gyro', geometry_msgs.msg.Vector3, queue_size=10)
_['gyro_heading_pub'] = rospy.Publisher(bcs+'gyro_heading', geometry_msgs.msg.Vector3, queue_size=10)
_['acc_pub'] = rospy.Publisher(bcs+'acc', geometry_msgs.msg.Vector3, queue_size=10)
_['servo_pwm_min_pub'] = rospy.Publisher(bcs+'servo_pwm_min', std_msgs.msg.Int32, queue_size=5) 
_['servo_pwm_max_pub'] = rospy.Publisher(bcs+'servo_pwm_max', std_msgs.msg.Int32, queue_size=5) 
_['servo_pwm_null_pub'] = rospy.Publisher(bcs+'servo_pwm_null', std_msgs.msg.Int32, queue_size=5) 
_['motor_pwm_min_pub'] = rospy.Publisher(bcs+'motor_pwm_min', std_msgs.msg.Int32, queue_size=5) 
_['motor_pwm_null_pub'] = rospy.Publisher(bcs+'motor_pwm_null', std_msgs.msg.Int32, queue_size=5) 
_['motor_pwm_max_pub'] = rospy.Publisher(bcs+'motor_pwm_max', std_msgs.msg.Int32, queue_size=5)

from default_values import flex_names
for name in flex_names:
    _[d2n(name,'_pub')] = rospy.Publisher(bcs+name,std_msgs.msg.Int32,queue_size=5)


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
    _['behavioral_mode_pub']
    if MSE_low_frequency_pub_timer.check():

        if _['button_number'] == 1:
            behavioral_mode_choice = 'left'
        elif _['button_number'] == 2:
            behavioral_mode_choice = 'direct'
        elif _['button_number'] == 3:
            behavioral_mode_choice = 'right'
        else:
            behavioral_mode_choice = 'ghost'
        _['behavioral_mode_pub'].publish(d2s(behavioral_mode_choice))


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
if not _['MOCK_ARDUINO_VERSION']:
    baudrate = 115200
    timeout = 0.1
    import arduino_utils.serial_init
    arduino_utils.serial_init.assign_serial_connections(_,
        arduino_utils.serial_init.get_arduino_serial_connections(baudrate,timeout))

else:
    import arduino_utils.mock_arduino
    arduino_utils.mock_arduino.put_mock_Arduinos_into_P(_)
    if username != 'nvidia':
        _['desktop version/L'],_['desktop version/O'],___ = open_run(
            run_name=_['MOCK_ARDUINO_VERSION/run_name'],
            h5py_path=_['MOCK_ARDUINO_VERSION/h5py_path'],
            want_list=['L','O'],
            verbose=True
        )
        _['desktop version/index'] = _['desktop version/start index']
    else:
        _['desktop version/L'],_['desktop version/O'],___ = open_run(
            #run_name='tegra-ubuntu_19Oct18_08h55m02s',
            run_name=_['MOCK_ARDUINO_VERSION/nvidia_run_name'],
            h5py_path=_['MOCK_ARDUINO_VERSION/nvidia_h5py_path'],
            want_list=['L','O'],
            verbose=True
        )
        _['desktop version/index'] = _['desktop version/start index']
if _['USE_MSE'] and 'MSE' in _['Arduinos'].keys():
    import arduino_utils.tactic_rc_controller
    arduino_utils.tactic_rc_controller.TACTIC_RC_controller(_)
    CS("!!!!!!!!!! found 'MSE' !!!!!!!!!!!",emphasis=True)

    if not _['MOCK_ARDUINO_VERSION']:
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
print 'arduino_node.py main loop'

import kzpy3.Menu_app.menu2 as menu2

parameter_file_load_timer = Timer(2.0)

while _['ABORT'] == False:

    try:
        time.sleep(1)

        if parameter_file_load_timer.check():

            if True:#_['button_number'] == 4 or _['MOCK_ARDUINO_VERSION']:

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
    except Exception as e:
        print '*********** here ************'
        CS_(d2s('Main loop exception',e))
#
#########################################
       



CS('End arduino_node.py main loop.')


#EOF
