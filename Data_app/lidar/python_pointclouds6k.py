#!/usr/bin/env python

from kzpy3.vis3 import *
import sensor_msgs
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import rospy

Output = {}

Durations = {}
durations = ['points__callback','process_callback_data','pointcloud_thread',]
for d in durations:
    Durations[d] = {}
    Durations[d]['timer'] = Timer()
    Durations[d]['list'] = []


A = {}
A['use_images'] = 1
A['time'] = 10
for a in Arguments:
    A[a] = Arguments[a]

waiting = Timer(1)
freq_timer = Timer(5);
timer = Timer(A['time'])

calls = 0
calls_prev = 0

"""
reflectivity is h_angle
t is r
intensity is intensity
"""

field_names = ['t','reflectivity','intensity']

width = 256
height = 16
width_times_height = width * height

for f in field_names:
    A[f] = zeros((height,width))


######################################
#
Y = {}
mx = 2*np.pi*1000.0
extra = 500
for d in range(0,int(mx+extra)):
    v = int( width*d / (1.0*mx) )
    if v > (width-1):
        v = (width-1)
    Y[d] = v

j = 0
for i in range(sorted(Y.keys())[-1]):
    if i in Y:
        j = Y[i]
    Y[i] = j

Y[np.nan] = 0
#
######################################







def points__callback(msg):
    global calls
    dname = 'points__callback'
    Durations[dname]['timer'].reset()    

    ctr = 0
    ctr3 = 0
    
    ary0 = A[field_names[0]]
    ary1 = A[field_names[1]]
    ary2 = A[field_names[2]]

    for point in pc2.read_points(msg,skip_nans=False,field_names=field_names):

        if ctr >= width:
            if ctr3 >= height-1:
                break
            ctr = 0

        ary0[ctr3,ctr] = point[0]  
        ary1[ctr3,ctr] = point[1]
        ary2[ctr3,ctr] = point[2]

        if ctr3 >= height-1:
            ctr3 = 0
            ctr += 1
        else:
            ctr3 += 1

    calls += 1

    Durations[dname]['list'].append(1000.0*Durations[dname]['timer'].time())







rospy.init_node('receive_pointclouds')
rospy.Subscriber('/os1_node/points', PointCloud2, points__callback)

Resize = {}
Resize['a'] = (89,167)
Resize['b'] = (0,256)
Resize['c'] = (44,212)
#image_type_versions = ['t','intensity','t']
image_type_versions = ['t']
#resize_versions = ['a','b']
resize_versions = ['c']

Images = {}
for image_type in image_type_versions:
    Images[image_type] = None

def process_callback_data():

    dname = 'process_callback_data'
    Durations[dname]['timer'].reset()

    y = (A['reflectivity'][8,:]).astype(int)



    for image_type in image_type_versions:



        if type(Images[image_type]) == type(None):
            Images[image_type] = A[image_type] * 0

        indicies = [Y[v] for v in y]

        Images[image_type][:,indicies] = A[image_type]

        for i in range(1,len(Images[image_type])):

            if Images[image_type][0,i] == 0:
                try:
                    Images[image_type][:,i] = Images[image_type+'_prev'][:,i]
                except:
                    Images[image_type][:,i] = Images[image_type][:,i-1]





            
            d2 = Images[image_type]

            for resize in resize_versions:

                r=Resize[resize]

                Images[image_type+'_resized_'+resize] = cv2.resize(d2[:,r[0]:r[1]],(168,94))

                #Images[image_type+'_resized_'+resize] = cv2.resize(d2[:,128-(168/2):128+(168/2)],(168,94))

            Images[image_type+'_prev'] = Images[image_type].copy()


    Durations[dname]['list'].append(1000.0*Durations[dname]['timer'].time())





def pointcloud_thread():
    global calls_prev
    print_Arguments()

    while calls < 1:
        waiting.message('waiting for data...')
        time.sleep(0.01)

    timer.reset()

    dname = 'pointcloud_thread'
    while not timer.check():

        if True:#try:
            calls_ = calls


            if calls_ > calls_prev:

                freq_timer.freq('LIDAR ')
                Durations[dname]['timer'].reset()

                process_callback_data()

                Durations[dname]['list'].append(1000.0*Durations[dname]['timer'].time())

                if A['use_images']:
                    #figure('d');clf();plot(d);xlim(0,(width-1))
                    #figure('d2');clf();plot(d2);xlim(0,(width-1));spause()#;raw_enter()
                    #mi(Output['e'].transpose(1,0));spause()#;raw_enter()
                    for image_type in image_type_versions:
                        for resize in resize_versions:
                            mci(
                                (z2o(Images[image_type+'_resized_'+resize])*255).astype(np.uint8),
                                scale=2.0,
                                color_mode=cv2.COLOR_GRAY2BGR,
                                title=image_type+' '+resize
                            )

            calls_prev = calls_

        else:#except:
            cs('exception',calls)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
    CA();time.sleep(1)
    A['ABORT'] = True
    cg('\npointcloud_thread() exiting.\n\n')





if __name__ == '__main__':
    threading.Thread(target=pointcloud_thread,args=[]).start()
    show_durations = Timer(5)
    A['hist_durations'] = True
    A['ABORT'] = False
    if 'hist_durations' in A:
        if A['hist_durations']:
            while A['ABORT'] == False:
                if show_durations.check():
                    for d in durations:
                        #figure(d);clf()
                        #hist(Durations[d]['list'])
                        #spause()
                        cg(d,':',np.median(Durations[d]['list']),'ms')
                        #cg(d,':',dp(np.median(Durations[d]['list']),1),'ms')
                        show_durations.reset()





"""
nc exampe:

tegra-ubuntu> ~ $ nc 192.168.1.251 7501

get_config_txt

{"auto_start_flag": 1, "tcp_port": 7501, "udp_ip": "192.168.1.103", "udp_port_lidar": 7502, "udp_port_imu": 7503, "timestamp_mode": "TIME_FROM_INTERNAL_OSC", "pps_out_mode": "OUTPUT_PPS_OFF", "pps_out_polarity": "ACTIVE_HIGH", "pps_rate": 1, "pps_angle": 360, "pps_pulse_width": 10, "pps_in_polarity": "ACTIVE_HIGH", "lidar_mode": "1024x10", "motor_phase_lock_enable": 0, "motor_phase_offset": 0, "motor_enable": 0, "pulse_mode": "STANDARD", "window_rejection_enable": 0}

set_config_param lidar_mode 512x10
set_config_param

reinitialize

reinitialize

get_config_txt

{"auto_start_flag": 1, "tcp_port": 7501, "udp_ip": "192.168.1.103", "udp_port_lidar": 7502, "udp_port_imu": 7503, "timestamp_mode": "TIME_FROM_INTERNAL_OSC", "pps_out_mode": "OUTPUT_PPS_OFF", "pps_out_polarity": "ACTIVE_HIGH", "pps_rate": 1, "pps_angle": 360, "pps_pulse_width": 10, "pps_in_polarity": "ACTIVE_HIGH", "lidar_mode": "512x10", "motor_phase_lock_enable": 0, "motor_phase_offset": 0, "motor_enable": 0, "pulse_mode": "STANDARD", "window_rejection_enable": 0}

"""


#EOF
