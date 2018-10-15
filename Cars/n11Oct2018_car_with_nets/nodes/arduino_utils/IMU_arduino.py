from kzpy3.utils3 import *
exec(identify_file_str)
import rospy

def IMU_Arduino(P):
    threading.Thread(target=_IMU_run_loop,args=[P]).start()

def _IMU_run_loop(P):
    print '_IMU_run_loop'
    flush_seconds = 0.1
    flush_timer = Timer(flush_seconds)
    time.sleep(0.1)
    P['Arduinos']['IMU'].flushInput()
    time.sleep(0.1)
    P['Arduinos']['IMU'].flushOutput()
    ctr_timer = Timer()
    frequency_timers = {'acc':Timer(1),'gyro':Timer(1),'head':Timer(1)}
    acc_smoothed = [0,0,0]
    print_timer = Timer(0.1)
    P['Hz']['acc'] = 0
    s = P['IMU_SMOOTHING_PARAMETER']
    while (not P['ABORT']) and (not rospy.is_shutdown()):
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.001)
        try:
            read_str = P['Arduinos']['IMU'].readline()
            if flush_timer.check():
                P['Arduinos']['IMU'].flushInput();P['Arduinos']['IMU'].flushOutput()
                flush_timer.reset()            
            exec('imu_input = list({0})'.format(read_str))       
            m = imu_input[0]
            assert(m in ['acc','gyro','head'])
            Hz = frequency_timers[m].freq(name=m,do_print=False)
            if m == 'acc':
                for i in range(3):
                    acc_smoothed[i] = (1.0-s)*imu_input[i+1] + s*acc_smoothed[i]
                #if acc_smoothed[1] < -9.0:
                #    spd2s('acc_smoothed[1] < -9.0, ABORTING, SHUTTING DOWN!!!!!')
                #    P['ABORT'] = True
                #    default_values.EXIT(restart=False,shutdown=True,kill_ros=True,_file_=__file__)
                if is_number(Hz):
                    P['Hz'][m] = Hz
                    if Hz < 30 or Hz > 90:
                        if ctr_timer.time() > 5:
                            spd2s(m,'Hz =',Hz,'...aborting...')
                        else:
                            pass
            P[m]['xyz'] = imu_input[1:4]
            if P['USE_ROS']:
                P['publish_IMU_data'](P,m)
            if P['IMU/print_timer'].check():
                #pd2s('IMU:',read_str)
                P['IMU/print_timer'] = Timer(P['print_timer time'])

        except Exception as e:
            pass
    print 'end _IMU_run_loop.'
    CS_("doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))")
    time.sleep(0.01)
    unix(opjh('kzpy3/scripts/kill_ros.sh'))





