from kzpy3.utils2 import *
exec(identify_file_str)
import rospy

def LED_Display(P):
    threading.Thread(target=_LED_Display_run_loop,args=[P]).start()
    
def _LED_Display_run_loop(P):
    run_timer = Timer()
    print('_LED_Display_run_loop')
    time.sleep(0.1)
    P['Arduinos']['SIG'].flushInput()
    time.sleep(0.1)
    P['Arduinos']['SIG'].flushOutput()
    flush_seconds = 0.25
    flush_timer = Timer(flush_seconds)
    print_timer = Timer(1)
    write_timer = Timer(0.1)
    bag_timer = Timer(0.25)
    frequency_timer = Timer(1)
    while (not P['ABORT']) and (not rospy.is_shutdown()):
        frequency_timer.freq(name='_LED_Display_run_loop',do_print=P['print_led_freq'])
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.03)
        try:
            read_str = P['Arduinos']['SIG'].readline()
            if flush_timer.check():
                P['Arduinos']['SIG'].flushInput()
                P['Arduinos']['SIG'].flushOutput()
                flush_timer.reset()
            exec('gps_input = list({0})'.format(read_str))       
                assert(gps_input[0]=='GPS3')
            P['GPS_latitudeDegrees'] = gps_input[1]
            P['GPS_longitudeDegrees'] = gps_input[2]
            P['GPS_speed'] = gps_input[3]
            P['GPS_angle'] = gps_input[4]
            P['GPS_altitude'] = gps_input[5]
            P['GPS_fixquality'] = gps_input[6]
            P['GPS_satellites'] = gps_input[7]           
            if P['USE_ROS']:
                P['publish_GPS_data'](P,m)
            if write_timer.check():
                P['Arduinos']['SIG'].write(d2n('(',P['LED_number']['current'],')'))
                write_timer.reset()
            elif bag_timer.check():
                 num_bagfiles = len(sggo(most_recent_file_in_folder(opjm('new'),'*.bag')))
                P['Arduinos']['SIG'].write(d2n('(',-num_bagfiles,')'))
                bag_timer.reset()

            if print_timer.check():
                pass
                print_timer.reset()
            time.sleep(0.001)
        except Exception as e:
            print e
            pass
    P['Arduinos']['SIG'].write('(11119)')         
    print d2s('end _LED_Display_run_loop, ran for',dp(run_timer.time(),1),'seconds')

