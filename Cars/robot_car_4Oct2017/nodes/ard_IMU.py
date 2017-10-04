import threading
import rospy
from kzpy3.utils2 import *
import geometry_msgs.msg

imu_dic = {}
imu_dic['gyro'] = 'gyro_pub'
imu_dic['acc'] = 'acc_pub'
imu_dic['head'] = 'gyro_heading_pub'

lock = threading.Lock()

def setup(M,Arduinos):
    pass

def run_loop(Arduinos,M):

    try:
        if os.environ['STOP'] == 'True':
            stop_ros()
            assert(False)
        while M['Stop_Arduinos'] == False or not rospy.is_shutdown():

            try:        
                read_str = Arduinos['IMU'].readline()
                #print read_str
                exec('imu_input = list({0})'.format(read_str))
                #print imu_input
                m = imu_input[0]
                M[m] = imu_input[1:4]
                M[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*M[m]))


            except Exception as e:
                    print("********** def run_loop(Arduinos,M): 1 Exception ***********************")
                    print(e.message, e.args)
        stop_ros()
    except Exception as e:
        print("********** def run_loop(Arduinos,M): 2 Exception ***********************")
        print(e.message, e.args)
        os.environ['STOP'] = 'True'
        LED_signal = d2n('(10000)')
        M['Stop_Arduinos'] = True
        if 'SIG' in Arduinos.keys():
            Arduinos['SIG'].write(LED_signal)
        rospy.signal_shutdown(d2s(e.message,e.args))
        stop_ros()






