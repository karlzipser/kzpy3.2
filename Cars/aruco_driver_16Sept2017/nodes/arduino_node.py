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

import kzpy3.teg2.bdd_car_versions.bdd_car_rewrite_SD2.runtime_params as rp

os.environ['STOP'] = 'False'

baudrate = 115200
timeout = 0.5 # before 7/9/17 was 0.1
Arduinos = ard_ser_in.assign_serial_connections(ard_ser_in.get_arduino_serial_connections(baudrate,timeout))
time_step = Timer(1)
folder_display_timer = Timer(10)
git_pull_timer = Timer(60)
reload_timer = Timer(30)


M = {}
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
M['aruco_evasion_active'] = 0
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

def arduino_motor_control_thread():
    ard_motor_control.run_loop(M)

def arduino_imu_thread():
    ard_IMU.run_loop(Arduinos,M)

def arduino_sig_thread():
    ard_SIG.run_loop(Arduinos,M)

def arduino_master_thread():
    #while M['Stop_Arduinos'] == False or not rospy.is_shutdown():
    
    try:
        if os.environ['STOP'] == 'True':
            stop_ros()
            assert(False)
        while not rospy.is_shutdown():
            if time_step.check():
                time_step.reset()
                if not folder_display_timer.check():
                    print("*** Data foldername = "+rp.foldername+ '***')

            if reload_timer.check():
                reload(rp)
                #reload(kzpy3.teg2.bdd_car_versions.bdd_car_rewrite.runtime_params)
                #from kzpy3.teg2.bdd_car_versions.bdd_car_rewrite.runtime_params import *
                #model_name_pub.publish(std_msgs.msg.String(weights_file_path))
                reload_timer.reset()
                M['steer_gain'] = rp.steer_gain
                M['motor_gain'] = rp.motor_gain
                M['acc2rd_threshold'] = rp.acc2rd_threshold
                M['gyro_freeze_threshold'] = rp.gyro_freeze_threshold
                M['acc_freeze_threshold_x'] = rp.acc_freeze_threshold_x
                M['acc_freeze_threshold_y_max'] = rp.acc_freeze_threshold_y_max
                M['acc_freeze_threshold_y_min'] = rp.acc_freeze_threshold_y_min
                M['acc_freeze_threshold_z'] = rp.acc_freeze_threshold_z
                M['motor_freeze_threshold'] = rp.motor_freeze_threshold
                M['PID_min_max'] = rp.PID_min_max
                M['n_avg_IMU'] = rp.n_avg_IMU

            if git_pull_timer.check():
                unix(opjh('kzpy3/kzpy3_git_pull.sh'))
                git_pull_timer.reset()

            #print M.keys()
            try:
                pass
                #print (shape(M['acc_lst']),M['acc_lst_mean'])
                #print(M['caffe_motor'])#,M['aruco_evasion_active'],int(M['caffe_steer_pwm']),M['current_state'].name,M['steer_pwm_lst'][-1],M['steer_percent'],M['motor_percent'],M['acc'],M['gyro'],M['head'])#,M['gyro'],M['head'],M['encoder'])
            except:
                pass

            time.sleep(0.5)
        stop_ros()
    except Exception as e:
        print("********** Exception ***********************")
        print(e.message, e.args)
        os.environ['STOP'] = 'True'
        LED_signal = d2n('(10000)')
        Arduinos['SIG'].write(LED_signal)
        rospy.signal_shutdown(d2s(e.message,e.args))
        stop_ros()





if 'MSE' in Arduinos:
    ard_MSE.setup(M,Arduinos)
    threading.Thread(target=arduino_mse_thread).start()
else:
    print("!!!!!!!!!! 'MSE' not in Arduinos[] !!!!!!!!!!!")
    stop_ros()

if 'IMU' in Arduinos.keys():
    print("'IMU' in Arduinos.keys()")
    ard_IMU.setup(M,Arduinos)
    threading.Thread(target=arduino_imu_thread).start()

if 'SIG' in Arduinos.keys():
    'SIG' in Arduinos.keys()
    threading.Thread(target=arduino_sig_thread).start()
    ard_SIG.setup(M,Arduinos)

threading.Thread(target=arduino_master_thread).start()


q = raw_input('')
while q not in ['q','Q']:
    q = raw_input('')

stop_ros()