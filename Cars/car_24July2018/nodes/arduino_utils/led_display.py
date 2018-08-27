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
    threading.Thread(target=internet_on_thread,args=[P,]).start()
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
            #pd2s("Start:",gps_input) 
            if type(gps_input) != list:
                continue
            if len(gps_input) != 8:
                continue
            if gps_input[0]!='GPS3':
                continue
            #print 'a'
            P['GPS_latitudeDegrees'] = gps_input[1]
            #print 'b'
            P['GPS_longitudeDegrees'] = gps_input[2]
            #print 'c'
            P['GPS_speed'] = gps_input[3]
            #print 'd'
            P['GPS_angle'] = gps_input[4]
            #print 'e'
            P['GPS_altitude'] = gps_input[5]
            #print 'f'
            P['GPS_fixquality'] = gps_input[6]
            #print 'g'
            P['GPS_satellites'] = gps_input[7]
            #print 'h'        
            if P['USE_ROS']:
                P['publish_GPS_data'](P)
            if write_timer.check():
                P['Arduinos']['SIG'].write(d2n('(',P['LED_number']['current'],')'))
                write_timer.reset()
            if bag_timer.check():
                num_bag_files = 0
                GPS_status = 1
                wifi_status = 0
                num_arduinos = 0
                for a in ['MSE','IMU','SIG','FLEX']:
                    if a in P['Arduinos']:
                        num_arduinos += 1
                num_bag_files = len(sggo(most_recent_file_in_folder(opjm('rosbags/new')),'*.bag'))
                if P['GPS_fixquality'] > 0:
                    GPS_status = 2
                if False:
                    if internet_on():
                        wifi_status = 1
                if P['internet_on']:
                    wifi_status = 1
                #print(GPS_status,num_arduinos,wifi_status,num_bag_files)
                write_num = 10000*GPS_status+num_arduinos*1000+num_bag_files
                if wifi_status:
                    write_num += 500
                P['Arduinos']['SIG'].write(d2n('(',-write_num,')'))
                #pd2s("P['Arduinos']['SIG'].write(d2n('(',-write_num,')')) =",-write_num)
                bag_timer.reset()

            if print_timer.check():
                pass
                print_timer.reset()
            time.sleep(0.001)
        except Exception as e:
            pd2s("led_display.py Exception:",e)
            pass
    P['Arduinos']['SIG'].write('(11119)')         
    print d2s('end _LED_Display_run_loop, ran for',dp(run_timer.time(),1),'seconds')

