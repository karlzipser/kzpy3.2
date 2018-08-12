from kzpy3.utils2 import *
exec(identify_file_str)

from default_values import flex_names



def IMU_Arduino(P):
    for f in flex_names:
        P[f] = {}
    threading.Thread(target=_FLEX_run_loop,args=[P]).start()

def _FLEX_run_loop(P):
    print '_FLEX_run_loop'
    flush_seconds = 0.1
    flush_timer = Timer(flush_seconds)
    time.sleep(0.1)
    P['Arduinos']['FLEX'].flushInput()
    time.sleep(0.1)
    P['Arduinos']['FLEX'].flushOutput()
    ctr_timer = Timer()
    frequency_timers = {}
    for f in flex_names:
        frequency_timers[f] = Timer(1)
    #acc_smoothed = [0,0,0]
    print_timer = Timer(0.1)
    P['Hz']['flex'] = 0
    #s = P['IMU_SMOOTHING_PARAMETER']
    while P['ABORT'] == False:
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.001)
        try:
            read_str = P['Arduinos']['FLEX'].readline()
            if flush_timer.check():
                P['Arduinos']['FLEX'].flushInput();P['Arduinos']['FLEX'].flushOutput()
                flush_timer.reset()            
            exec('flex_input = list({0})'.format(read_str))       
            m = imu_input[0]
            assert(m in flex_names)
            Hz = frequency_timers[m].freq(name=m,do_print=False)
            if False:#m == 'acc':
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
            P[m] = imu_input[1]
            if P['USE_ROS']:
                P['publish_FLEX_data'](P,m)
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
    print 'end _FLEX_run_loop.'





