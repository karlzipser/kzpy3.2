import threading
import rospy
from kzpy3.utils2 import *
import geometry_msgs.msg
import runtime_parameters as rp

imu_dic = {}
imu_dic['gyro'] = 'gyro_pub'
imu_dic['acc'] = 'acc_pub'
imu_dic['head'] = 'gyro_heading_pub'

lock = threading.Lock()

def setup(M,Arduinos):
    for m in ['gyro','acc','head']:
        for d in ['_x_lst','_y_lst','_z_lst']:
            M[m+d] = []
    M['acc_lst'] = []
    M['n_avg_IMU'] = rp.n_avg_IMU





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
                if m == 'acc':
                    #print("if m == 'acc':")
                    M['acc_lst'].append(M['acc'])
                    if len(M['acc_lst']) > 1.5*M['n_avg_IMU']:
                        M['acc_lst'] = M['acc_lst'][-M['n_avg_IMU']:]
                #print m,M[m]
                M[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*M[m]))

            except Exception as e:
                pass #print e
        stop_ros()
    except Exception as e:
        print("********** Exception ***********************")
        print(e.message, e.args)
        os.environ['STOP'] = 'True'
        LED_signal = d2n('(10000)')
        M['Stop_Arduinos'] = True
        if 'SIG' in Arduinos.keys():
            Arduinos['SIG'].write(LED_signal)
        rospy.signal_shutdown(d2s(e.message,e.args))
        stop_ros()






