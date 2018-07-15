from kzpy3.utils2 import *
import threading

def IMU_Arduino(arduino,P):
    D = {}
    P['acc'] = {}
    P['gyro'] = {}
    P['head'] = {}
    D['arduino'] = arduino
    threading.Thread(target=_IMU_run_loop,args=[D,P]).start()
    return D

def _IMU_run_loop(D,P):
    print '_IMU_run_loop'
    imu_dic = {}
    imu_dic['gyro'] = 'gyro_pub'
    imu_dic['acc'] = 'acc_pub'
    imu_dic['head'] = 'gyro_heading_pub'
    flush_seconds = 0.5
    flush_timer = Timer(flush_seconds)
    time.sleep(0.1)
    D['arduino'].flushInput()
    time.sleep(0.1)
    D['arduino'].flushOutput()
    ctr_timer = Timer()
    frequency_timer = Timer(1)
    print_timer = Timer(1)
    while P['ABORT'] == False:
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.0001)
        try:
            read_str = D['arduino'].readline()
            if flush_timer.check():
                D['arduino'].flushInput()
                flush_timer.reset()            
            exec('imu_input = list({0})'.format(read_str))       
            m = imu_input[0]
            assert(m in ['acc','gyro','head'])
            Hz = frequency_timer.freq(name='_IMU_run_loop')
            if is_number(Hz):
                P[m]['Hz'] = Hz
            P[m]['xyz'] = imu_input[1:4]
            #P[m]['ctr'] += 1
            #P[m]['Hz'] = dp(P[m]['ctr']/ctr_timer.time(),1)
            if ctr_timer.time() > 5:
                if P[m]['Hz'] < 60 or P[m]['Hz'] > 100:
                    P['ABORT'] = True
                    spd2s("\nP[",m,"]['Hz'] =",P[m]['Hz'])
            if False:
                P[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*P[m]['xyz']))
            if True:
                if print_timer.check():
                    print m,P[m]
                    print_timer.reset()
        except Exception as e:
            #print("********** IMU_run_loop(Arduinos,P) Exception ***********************")
            #print(e.message, e.args)
            pass
    print 'end IMU_run_loop.'





