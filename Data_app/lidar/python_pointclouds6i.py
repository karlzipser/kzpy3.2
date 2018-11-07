#!/usr/bin/env python

from kzpy3.vis3 import *

cr(time.time())

import sensor_msgs
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import rospy

TX1 = False
if username == 'nvidia':
    TX1 = True
    cs("Using TX1")

Output = {}

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
    field_names = ['y','intensity']
    width = 1024

height = 16
width_times_height = width * height

for f in field_names:
    A[f] = zeros((width,height))
cr(time.time())
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
cr(time.time())
def points__callback(msg):
    global calls
    #calls += 1
    
    ctr = 0
    ctr2 = 0
    ctr3 = 0
    
    ary0 = A[field_names[0]]
    ary1 = A[field_names[1]]
    
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
        ctr2 += 1
        if ctr2 >= 4:
            ctr2 = 0

    calls += 1
cr(time.time())



d2_prev = None

def process_callback_data():

    global d2_prev

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

#    return e
    return d2

cr(time.time())

def pointcloud_thread():
    global calls_prev, calls_skip

    cg("\nStarting pointcloud_thread()\n")
    print_Arguments()

    while calls < 1:
        waiting.message('waiting for LIDAR data...')
        time.sleep(0.01)

    if 'time' in A:
        cr("timer = Timer(A['time'])")
        timer = Timer(A['time'])


    while A['ABORT'] == False:#not timer.check():

        try:
            calls_ = calls

            if calls_ > calls_prev:

                freq_timer.freq("LIDAR")
        
                #Output['e'] = process_callback_data()
                Output['d2'] = process_callback_data()

                if A['use_images']:
                    if A['calls_skip'] == calls_skip:
                        calls_skip = 0
                        mci(
                            (z2o(Output['e'].transpose(1,0))*255).astype(np.uint8),
                            scale=2.0,
                            color_mode=cv2.COLOR_GRAY2BGR,
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
    cg('\npointcloud_thread() exiting.\n\n')

cr(time.time())

if __name__ == '__main__':
    rospy.init_node('receive_pointclouds')
    rospy.Subscriber('/os1_node/points', PointCloud2, points__callback)
    threading.Thread(target=pointcloud_thread,args=[]).start()





#EOF
