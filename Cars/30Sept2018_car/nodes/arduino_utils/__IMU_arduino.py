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
    P['Arduinos']['MSE'].flushInput()
    time.sleep(0.1)
    P['Arduinos']['MSE'].flushOutput()
    ctr_timer = Timer()
    frequency_timers = {'acc':Timer(1),'gyro':Timer(1),'head':Timer(1)}
    
    print_timer = Timer(0.1)
    P['Hz']['acc'] = 0
    
    while (not P['ABORT']) and (not rospy.is_shutdown()):
        time.sleep(1)
            if False:
            if 'Brief sleep to allow other threads to process...':
                time.sleep(0.001)
            try:
                read_str = P['Arduinos']['MSE'].readline()
                #if flush_timer.check():
                #    P['Arduinos']['MSE'].flushInput();P['Arduinos']['MSE'].flushOutput()
                #    flush_timer.reset()            
                exec('imu_input = list({0})'.format(read_str))       
                m = imu_input[0]




                if print_timer.check():
                    print_timer.reset()
            except Exception as e:
                pass
    print 'end _IMU_run_loop.'





