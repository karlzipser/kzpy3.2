#!/usr/bin/env python

from kzpy3.utils2 import *
import ard_MSE
import ard_IMU
import ard_SIG
import ard_ser_in
import threading
import std_msgs.msg
import geometry_msgs.msg
import rospy
import runtime_parameters as rp

os.environ['STOP'] = 'False'

baudrate = 115200
timeout = 0.5 # before 7/9/17 was 0.1
Arduinos = ard_ser_in.assign_serial_connections(ard_ser_in.get_arduino_serial_connections(baudrate,timeout))
time_step = Timer(1)
folder_display_timer = Timer(10)
git_pull_timer = Timer(60)
reload_timer = Timer(30)

M = {}
"""
steer_gain = 1.0
motor_gain = 1.0
motor_offset = 5

acc2rd_threshold = 150
gyro_freeze_threshold = 150
acc_freeze_threshold_x = 14
acc_freeze_threshold_y_max = 30
acc_freeze_threshold_y_min = 0
acc_freeze_threshold_z = 14
motor_freeze_threshold = 55
n_avg_IMU = 10
"""

M['acc2rd_threshold'] = rp.acc2rd_threshold
M['gyro_freeze_threshold'] = rp.gyro_freeze_threshold
M['acc_freeze_threshold_x'] = rp.acc_freeze_threshold_x
M['acc_freeze_threshold_y_max'] = rp.acc_freeze_threshold_y_max
M['acc_freeze_threshold_y_min'] = rp.acc_freeze_threshold_y_min
M['acc_freeze_threshold_z'] = rp.acc_freeze_threshold_z
M['motor_freeze_threshold'] = rp.motor_freeze_threshold
M['steer_gain'] = rp.steer_gain
M['motor_gain'] = rp.motor_gain
M['Stop_Arduinos'] = False
M['PID_min_max'] = rp.PID_min_max
#M['aruco_evasion_active'] = 0
M['n_avg_IMU'] = rp.n_avg_IMU


def caffe_steer_callback(msg):
    global M
    M['caffe_steer'] = msg.data

def caffe_motor_callback(msg):
    global M
    M['caffe_motor'] = msg.data

def data_saving_callback(msg):
    global M
    M['data_saving'] = msg.data


rospy.init_node('run_arduino',anonymous=True)
rospy.Subscriber('cmd/steer', std_msgs.msg.Int32, callback=caffe_steer_callback)
rospy.Subscriber('cmd/motor', std_msgs.msg.Int32, callback=caffe_motor_callback)

M['state_pub'] = rospy.Publisher('state', std_msgs.msg.Int32, queue_size=5) 
M['steer_pub'] = rospy.Publisher('steer', std_msgs.msg.Int32, queue_size=5) 
M['motor_pub'] = rospy.Publisher('motor', std_msgs.msg.Int32, queue_size=5) 
M['encoder_pub'] = rospy.Publisher('encoder', std_msgs.msg.Float32, queue_size=5)
M['gyro_pub'] = rospy.Publisher('gyro', geometry_msgs.msg.Vector3, queue_size=100)
M['gyro_heading_pub'] = rospy.Publisher('gyro_heading', geometry_msgs.msg.Vector3, queue_size=100)
M['acc_pub'] = rospy.Publisher('acc', geometry_msgs.msg.Vector3, queue_size=100)


def arduino_mse_thread():
    ard_MSE.run_loop(Arduinos,M)

def arduino_imu_thread():
    ard_IMU.run_loop(Arduinos,M)

def arduino_sig_thread():
    ard_SIG.run_loop(Arduinos,M)


if 'MSE' in Arduinos:
    print("MSE in Arduinos[].keys()")
    ard_MSE.setup(M,Arduinos)
    threading.Thread(target=arduino_mse_thread).start()
else:
    print("!!!!!!!!!! 'MSE' not in Arduinos[] !!!!!!!!!!!")
    stop_ros()

if 'IMU' in Arduinos.keys():
    print("'IMU' in Arduinos.keys()")
    ard_IMU.setup(M,Arduinos)
    threading.Thread(target=arduino_imu_thread).start()
else:
    print("!!!!!!!!!! 'IMU' not in Arduinos[] !!!!!!!!!!!")
    raw_enter()

if 'SIG' in Arduinos.keys():
    print("MSE in Arduinos[].keys()")
    ard_SIG.setup(M,Arduinos)
    threading.Thread(target=arduino_sig_thread).start()
else:
    print("!!!!!!!!!! 'SIG' not in Arduinos[] !!!!!!!!!!!")
    raw_enter()


q = raw_input('')
while q not in ['q','Q']:
    q = raw_input('')

stop_ros()

