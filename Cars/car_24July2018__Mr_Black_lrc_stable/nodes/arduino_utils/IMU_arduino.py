from kzpy3.utils2 import *
import threading

def IMU_Arduino(P):
    P['acc'] = {}
    P['gyro'] = {}
    P['head'] = {}
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
    while P['ABORT'] == False:
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
                if acc_smoothed[1] < -9.0:
                    spd2s('acc_smoothed[1] < -9.0, ABORTING, SHUTTING DOWN!!!!!')
                    P['ABORT'] = True
                    time.sleep(0.01)
                    unix('sudo shutdown -h now')
                if is_number(Hz):
                    P['Hz'][m] = Hz
                    if Hz < 30 or Hz > 90:
                        if ctr_timer.time() > 5:
                            spd2s(m,'Hz =',Hz,'...aborting...')
                            #P['ABORT'] = True
                        else:
                            pass#print 'ignoring IMU freq. error.'
            P[m]['xyz'] = imu_input[1:4]
            if P['USE_ROS']:
                P['publish_IMU_data'](P,m)
            if print_timer.check():
                #pd2s(dp(acc_smoothed[0],1),dp(acc_smoothed[1],1),dp(acc_smoothed[2],1))
                #print P['acc']['xyz'],P['gyro']['xyz'],P['head']['xyz'],P['acc']['Hz']
                #if P['print_imu_freq']:
                #    print P['gyro']['xyz'],P['acc']['Hz']
                print_timer.reset()
        except Exception as e:
            #print("********** IMU_run_loop(Arduinos,P) Exception ***********************")
            #print(e.message, e.args)
            pass
    print 'end IMU_run_loop.'




