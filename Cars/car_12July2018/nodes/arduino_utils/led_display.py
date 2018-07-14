from kzpy3.utils2 import *
import threading

def LED_Display(arduino,P):
    D = {}
    D['arduino'] = arduino
    threading.Thread(target=_LED_Display_run_loop,args=[D,P]).start()
    return D
    
def _LED_Display_run_loop(D,P):
    print('_LED_Display_run_loop')
    time.sleep(0.1)
    D['arduino'].flushInput()
    time.sleep(0.1)
    D['arduino'].flushOutput()
    flush_seconds = 0.25
    flush_timer = Timer(flush_seconds)
    print_timer = Timer(1)
    write_timer = Timer(0.1)
    while P['ABORT'] == False:
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.0001)
        try:
            if 'Read serial and translate to list...':
                #read_str = D['arduino'].readline()
                if flush_timer.check():
                    D['arduino'].flushInput()
                    D['arduino'].flushOutput()
                    flush_timer.reset()
            if write_timer.check():
                #if P['LED_number']['write'] == False:
                D['arduino'].write(d2n('(',P['LED_number']['current'],')'))
                #P['LED_number']['write'] == True
                write_timer.reset()
            if print_timer.check():
                pass
                print_timer.reset()
            time.sleep(0.001)
        except Exception as e:
            print e
            pass            
    print 'end _LED_Display_run_loop.'

