#!/usr/bin/env python
"""
python kzpy3/Cars/car_16July2018/nodes/arduino_node.py
"""
from kzpy3.utils2 import *
exec(identify_file_str)

Parameters = {}
Parameters['calibrated'] = False
Parameters['ABORT'] = False

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
Parameters['IMU_SMOOTHING_PARAMETER'] = 0.99
Parameters['Hz'] = {}




from arduino_utils.serial_init_temp import *


if 'Start Arduino threads...':
    baudrate = 9600
    timeout = 0.1
    assign_serial_connections(Parameters,get_arduino_serial_connections(baudrate,timeout))
    read_str = Parameters['Arduinos']['IMU'].readline()
    print read_str



#EOF
