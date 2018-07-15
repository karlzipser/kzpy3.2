
from kzpy3.utils2 import *
import threading


def IMU_setup(Arduinos,P):
    P['acc'] = {}
    P['gyro'] = {}
    P['head'] = {}
    for k in ['acc','gyro','head']:
        P[k]['ctr'] = 0
    print 'IMU_setup'
    pass
def IMU_run_loop(Arduinos,P):
    print 'IMU_run_loop'
    imu_dic = {}
    imu_dic['gyro'] = 'gyro_pub'
    imu_dic['acc'] = 'acc_pub'
    imu_dic['head'] = 'gyro_heading_pub'
    flush_seconds = 0.5
    flush_timer = Timer(flush_seconds)
    time.sleep(0.1)
    Arduinos['IMU'].flushInput()
    time.sleep(0.1)
    Arduinos['IMU'].flushOutput()
    ctr_timer = Timer()
    while P['ABORT'] == False:
        if P['PAUSE'] == True:
            time.sleep(0.1)
            continue
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.0001)
        try:
            read_str = Arduinos['IMU'].readline()
            if flush_timer.check():
                Arduinos['IMU'].flushInput()
                flush_timer.reset()            
            exec('imu_input = list({0})'.format(read_str))       
            m = imu_input[0]
            assert(m in ['acc','gyro','head'])
            if False:
                P[m]['x'] = imu_input[1]
                P[m]['y'] = imu_input[2]
                P[m]['z'] = imu_input[3]
            P[m]['xyz'] = imu_input[1:4]
            P[m]['ctr'] += 1
            P[m]['Hz'] = dp(P[m]['ctr']/ctr_timer.time(),1)
            if ctr_timer.time() > 5:
                if P[m]['Hz'] < 60 or P[m]['Hz'] > 100:
                    P['ABORT'] = True
                    spd2s("\nP[",m,"]['Hz'] =",P[m]['Hz'])
            if True:
                P[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*P[m]['xyz']))
        except Exception as e:
            #print("********** IMU_run_loop(Arduinos,P) Exception ***********************")
            #print(e.message, e.args)
            pass
    print 'end IMU_run_loop.'





