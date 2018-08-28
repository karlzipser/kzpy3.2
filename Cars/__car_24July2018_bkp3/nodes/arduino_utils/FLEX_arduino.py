from kzpy3.utils2 import *
exec(identify_file_str)
from default_values import flex_names
import rospy


def FLEX_Arduino(P):
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
    print_timer = Timer(0.1)
    P['Hz']['flex'] = 0
    while (not P['ABORT']) and (not rospy.is_shutdown()):
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.001)
        try:
            read_str = P['Arduinos']['FLEX'].readline()
            if flush_timer.check():
                P['Arduinos']['FLEX'].flushInput();P['Arduinos']['FLEX'].flushOutput()
                flush_timer.reset()            
            exec('flex_input = list({0})'.format(read_str))       
            m = flex_input[0]
            assert(m in flex_names)
            Hz = frequency_timers[m].freq(name=m,do_print=False)
            P[m] = flex_input[1]
            if P['USE_ROS']:
                P['publish_FLEX_data'](P,m)
            if print_timer.check():
                print_timer.reset()
        except Exception as e:
            pass
    print 'end _FLEX_run_loop.'





