#!/usr/bin/env python

from kzpy3.vis3 import *


import sensor_msgs
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import rospy

TX1 = False
if username == 'nvidia':
    TX1 = True
if 'TX1' in Arguments:
    if not Arguments['TX1']:
        TX1 = False

Output = {}


Durations = {}
durations = ['points__callback','process_callback_data','pointcloud_thread',]
for d in durations:
    Durations[d] = {}
    Durations[d]['timer'] = Timer()
    Durations[d]['list'] = []



A = {}
A['ABORT'] = False
A['use_images'] = 0
#A['time'] = 10
A['calls_skip'] = 0
for a in Arguments:
    A[a] = Arguments[a]

waiting = Timer(1)
freq_timer = Timer(5);


calls = 0
calls_prev = 0
calls_skip = 0

if TX1:
    #field_names = ['t','reflectivity']
    field_names = ['reflectivity','intensity']
    width = 1024/2
else:
    field_names = ['y','intensity']#,'reflectivity']
    width = 1024

height = 16
width_times_height = width * height

for f in field_names:
    A[f] = zeros((width,height))
######################################
#
Y = {}
mx = 2*np.pi*1000.0 #6290
extra = 40
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
    #calls += 1
    dname = 'points__callback'
    Durations[dname]['timer'].reset()

    ctr = 0
    ctr2 = 0
    ctr3 = 0
    
    ary0 = A[field_names[0]]
    ary1 = A[field_names[1]]
    #ary2 = A[field_names[2]]

    for point in pc2.read_points(msg,skip_nans=False,field_names=field_names):

        if ctr2 == 1:
            if ctr3 >= height-1:
                ctr3 = 0
                ctr += 1
            else:
                ctr3 += 1

            if ctr >= width:
                if ctr3 >= height-1:
                    break
                ctr = 0
            ary0[ctr,ctr3] = point[0]  
            ary1[ctr,ctr3] = point[1]
            #ary1[ctr,ctr3] = point[2]
        ctr2 += 1
        if ctr2 >= 4:
            ctr2 = 0

        if ctr >= 511:
            break

    calls += 1

    Durations[dname]['list'].append(1000.0*Durations[dname]['timer'].time())





d2_prev = None




def process_callback_data():

    global d2_prev
    dname = 'process_callback_data'
    Durations[dname]['timer'].reset()

    if TX1:
        b = A['reflectivity']
        y = (b[:,8]).astype(int)
        b2 = A['intensity']
    else:
        b = A['y']
        y = (b[:,8]*1000).astype(int)
        b2 = A['intensity']


    indicies = [Y[v] for v in y]


    d2 = b2*0
    d2[indicies,:] = b2

    for i in range(1,len(d2)):


        if d2[i,0] == 0:
            try:
                d2[i,:] = d2_prev[i,:]#d2[i-1,:]
            except:
                d2[i,:] = d2[i-1,:]
    """
    if TX1:
        e = cv2.resize(d2[68:448,:],(94,168))
    else:
        e = cv2.resize(d2,(64,1024))
    """
    d2_prev = d2.copy()

    Durations[dname]['list'].append(1000.0*Durations[dname]['timer'].time())

#    return e
    return d2


net_input_width = 168
net_input_height = 94






"""
w/[0,1,2]
points__callback = 66.91 ms
process_callback_data = 4.02 ms
pointcloud_thread = 46.43 ms

w/[0]
points__callback : 60.5 ms
process_callback_data : 3.6 ms
pointcloud_thread : 8.5 ms

w/skipping processing of data from point cloud in callback
points__callback : 47.6 ms


w/[1]
points__callback : 61.3 ms
process_callback_data : 3.4 ms
pointcloud_thread : 8.0 ms

with three pointcloud fields instead of two as above
points__callback : 71.4 ms

"""


def pointcloud_thread():
    global calls_prev, calls_skip
    dname = 'pointcloud_thread'
    cg("\nStarting pointcloud_thread()\n")
    print_Arguments()

    while calls < 1:
        waiting.message('waiting for LIDAR data...')
        time.sleep(0.01)

    if 'time' in A:
        timer = Timer(A['time'])


    while A['ABORT'] == False:#not timer.check():

        try:
            calls_ = calls

            if calls_ > calls_prev:

                freq_timer.freq("LIDAR")
        
                Durations[dname]['timer'].reset()

                #Output['e'] = process_callback_data()
                Output['d2'] = process_callback_data()






                d2 = Output['d2']
                shape_ = shape(d2)# == (16,1024)
                #print 'shape_',shape_
                width,height = shape_[0],shape_[1]
                #print 'width',width
                #print 'height',height
                assert width in [512,1024]
                assert height == 16

                half_widths = [int(100*width/360./2),int(180*width/360./2),int(270*width/360./2)]
                # can be moved up if width known

                e = []
                for i in [1]:#,1,2]:
                    half_width = half_widths[i]
                    f = cv2.resize(
                            d2[width/2 - half_width:width/2 + half_width, :],
                            (net_input_height,net_input_width)
                        ).transpose(1,0)
                    f = (255*z2o(f)).astype(int)
                    e.append(f)

                Output['e'] = e





                Durations[dname]['list'].append(1000.0*Durations[dname]['timer'].time())


                if A['use_images']:
                    if A['calls_skip'] == calls_skip:
                        calls_skip = 0
                        print type(Output['e'])
                        print shape(Output['e'])
                        for i in [1]:
                            mci(
                                (z2o(Output['e'][i])*255).astype(np.uint8),
                                scale=2.0,
                                color_mode=cv2.COLOR_GRAY2BGR,
                                title=d2n("Output['e'][",i,"]")
                            )
                    else:
                        calls_skip += 1

                calls_prev = calls_
                
                

            if 'time' in A:
                if timer.check():
                    cr("timer.check()")
                    A['ABORT'] = True

        except:
            cs('exception',calls)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
    CA();time.sleep(1)
    A['ABORT'] = True
    cg('\npointcloud_thread() exiting.\n\n')


if __name__ == '__main__':
    rospy.init_node('receive_pointclouds')
    rospy.Subscriber('/os1_node/points', PointCloud2, points__callback)
    threading.Thread(target=pointcloud_thread,args=[]).start()
    show_durations = Timer(5)
    A['ABORT'] = False
    while A['ABORT'] == False:
        if show_durations.check():
            for d in durations:
                #figure(d);clf()
                #hist(Durations[d]['list'])
                #spause()
                cg(d,':',dp(np.median(Durations[d]['list']),1),'ms')
            show_durations.reset()




#EOF
