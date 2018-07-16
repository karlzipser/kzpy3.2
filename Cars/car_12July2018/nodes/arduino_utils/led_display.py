from kzpy3.utils2 import *
import threading

def LED_Display(arduino,P):
    D = {}
    D['arduino'] = arduino
    threading.Thread(target=_LED_Display_run_loop,args=[D,P]).start()
    return D
    
def _LED_Display_run_loop(D,P):
    run_timer = Timer()
    print('_LED_Display_run_loop')
    time.sleep(0.1)
    D['arduino'].flushInput()
    time.sleep(0.1)
    D['arduino'].flushOutput()
    flush_seconds = 0.25
    flush_timer = Timer(flush_seconds)
    print_timer = Timer(1)
    write_timer = Timer(0.1)
    frequency_timer = Timer(1)
    while P['ABORT'] == False:
        frequency_timer.freq(name='_LED_Display_run_loop',do_print=P['print_led_freq'])
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.03)
        try:
            if 'Flush input and output...':
                if flush_timer.check():
                    D['arduino'].flushInput()
                    D['arduino'].flushOutput()
                    flush_timer.reset()
            if write_timer.check():
                D['arduino'].write(d2n('(',P['LED_number']['current'],')'))
                write_timer.reset()
            if print_timer.check():
                pass
                print_timer.reset()
            time.sleep(0.001)
        except Exception as e:
            print e
            pass            
    print d2s('end _LED_Display_run_loop, ran for',dp(run_timer.time(),1),'seconds')

