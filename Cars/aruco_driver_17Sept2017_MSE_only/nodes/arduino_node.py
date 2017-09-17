#!/usr/bin/env python

from kzpy3.utils2 import *
import runtime_parameters as rp

if 'Back' not in rp.computer_name:
    import ard_MSE
    import ard_ser_in
    import threading
    import std_msgs.msg
    import geometry_msgs.msg
    import rospy



    os.environ['STOP'] = 'False'

    baudrate = 115200
    timeout = 0.5 # before 7/9/17 was 0.1
    Arduinos = ard_ser_in.assign_serial_connections(ard_ser_in.get_arduino_serial_connections(baudrate,timeout))
    time_step = Timer(1)
    folder_display_timer = Timer(10)
    git_pull_timer = Timer(60)
    reload_timer = Timer(30)


    M = {}
    M['steer_gain'] = rp.steer_gain
    M['motor_gain'] = rp.motor_gain
    M['Stop_Arduinos'] = False


    def caffe_steer_callback(msg):
        global M
        M['caffe_steer'] = msg.data

    def caffe_motor_callback(msg):
        global M
        M['caffe_motor'] = msg.data


    rospy.init_node('run_arduino',anonymous=True)
    rospy.Subscriber('cmd/steer', std_msgs.msg.Int32, callback=caffe_steer_callback)
    rospy.Subscriber('cmd/motor', std_msgs.msg.Int32, callback=caffe_motor_callback)

    M['state_pub'] = rospy.Publisher('state', std_msgs.msg.Int32, queue_size=5) 
    M['steer_pub'] = rospy.Publisher('steer', std_msgs.msg.Int32, queue_size=5) 
    M['motor_pub'] = rospy.Publisher('motor', std_msgs.msg.Int32, queue_size=5) 


    def arduino_mse_thread():
        ard_MSE.run_loop(Arduinos,M)

    def arduino_motor_control_thread():
        ard_motor_control.run_loop(M)


    def arduino_master_thread():
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
                    reload_timer.reset()
                    M['steer_gain'] = rp.steer_gain
                    M['motor_gain'] = rp.motor_gain

                if git_pull_timer.check():
                    unix(opjh('kzpy3/kzpy3_git_pull.sh'))
                    git_pull_timer.reset()

                time.sleep(0.5)
            stop_ros()
        except Exception as e:
            print("********** Exception ***********************")
            print(e.message, e.args)
            os.environ['STOP'] = 'True'
            rospy.signal_shutdown(d2s(e.message,e.args))
            stop_ros()


    if 'MSE' in Arduinos:
        ard_MSE.setup(M,Arduinos)
        threading.Thread(target=arduino_mse_thread).start()
    else:
        print("!!!!!!!!!! 'MSE' not in Arduinos[] !!!!!!!!!!!")
        stop_ros()


    threading.Thread(target=arduino_master_thread).start()

else:
    spd2s("rp.require_Arudinos_MSE = False\nMSE Ardunio not used.")


q = raw_input('')
while q not in ['q','Q']:
    q = raw_input('')

stop_ros()