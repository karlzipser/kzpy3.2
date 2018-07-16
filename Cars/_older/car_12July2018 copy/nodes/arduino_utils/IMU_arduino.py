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
    flush_seconds = 0.1
    flush_timer = Timer(flush_seconds)
    time.sleep(0.1)
    D['arduino'].flushInput()
    time.sleep(0.1)
    D['arduino'].flushOutput()
    ctr_timer = Timer()
    frequency_timers = {'acc':Timer(1),'gyro':Timer(1),'head':Timer(1)}
    print_timer = Timer(0.1)
    while P['ABORT'] == False:
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.001)
        try:
            read_str = D['arduino'].readline()
            if flush_timer.check():
                D['arduino'].flushInput();D['arduino'].flushOutput()
                flush_timer.reset()            
            exec('imu_input = list({0})'.format(read_str))       
            m = imu_input[0]
            assert(m in ['acc','gyro','head'])
            Hz = frequency_timers[m].freq(name=m,do_print=False)
            if is_number(Hz) and m == 'acc':
                P[m]['Hz'] = Hz
                if Hz < 60 or Hz > 90:
                    if ctr_timer.time() > 5:
                        spd2s(m,'Hz =',Hz,'...aborting...')
                        P['ABORT'] = True
            P[m]['xyz'] = imu_input[1:4]
            if P['USE_ROS']:
                P['publish_IMU_data'](P,m)
                #P[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*P[m]['xyz']))
            if print_timer.check():
                #print P['acc']['xyz'],P['gyro']['xyz'],P['head']['xyz'],P['acc']['Hz']
                if P['print_imu_freq']:
                    print P['gyro']['xyz'],P['acc']['Hz']
                print_timer.reset()
        except Exception as e:
            #print("********** IMU_run_loop(Arduinos,P) Exception ***********************")
            #print(e.message, e.args)
            pass
    print 'end IMU_run_loop.'





