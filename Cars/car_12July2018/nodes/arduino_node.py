#!/usr/bin/env python
"""
python kzpy3/Cars/car_12July2018/nodes/arduino_node.py
"""
from kzpy3.utils2 import *
import threading
from arduino_utils.serial_init import *
from arduino_utils.tactic_rc_controller import *
from arduino_utils.calibration_mode import *
from arduino_utils.selector_mode import *
from arduino_utils.led_display import *
from arduino_utils.IMU_arduino import *

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
    if 'SIG' in Arduinos:
        Arduinos['SIG'].write('(11119)')
    Parameters['ABORT'] = True
    print 'done.'
    if Parameters['USE_ROS']:
        print "doing... unix(opjh('kzpy3/kill_ros.sh'))"
        unix(opjh('kzpy3/kill_ros.sh'))

#EOF
