#!/usr/bin/env python

from kzpy3.vis3 import *
import sensor_msgs
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import rospy

timer = Timer(15)

calls = 0
calls_prev = 0

field_names = ['y','reflectivity']

A = {}

width = 1024
height = 64
width_times_height = width * height
height2 = 16

for f in field_names:
    A[f] = zeros(height*width)



def points__callback(msg):
    global calls
    calls += 1
    ctr = 0
    even_odd = 0
    ary0 = A[field_names[0]]
    ary1 = A[field_names[1]]
    for point in pc2.read_points(msg,skip_nans=False,field_names=field_names):
        #if even_odd == 0:
        ary0[ctr]=point[0]	
        ary1[ctr]=point[1]
        ctr+=1
        #even_odd = 0
        if ctr >= width_times_height:
            break
        #else:
        #even_odd = 0


rospy.init_node('receive_pointclouds')

rospy.Subscriber('/os1_node/points', PointCloud2, points__callback)

waiting = Timer(1)

while calls < 1:
    waiting.message('waiting for data...')
    time.sleep(0.01)

freq_timer = Timer(1);





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





while not timer.check():

    try:

        calls_ = calls

        if calls_ > calls_prev:

            freq_timer.freq()

            b = A['y'].reshape(width,height).copy()

            #figure('b');plot(b);xlim(0,width)

            c = b[:,1:height:4] 

            y = (c[:,8]*1000).astype(int)

            #figure('y');plot(y,'.')

            indicies = [Y[v] for v in y]


            b2 = A['reflectivity'].reshape(width,height).copy()

            #figure('b2');plot(b2);xlim(0,width)

            c2 = b2[:,1:height:4] 




            d = 0*c
            d[indicies,:] = c


            d2 = c2*0
            d2[indicies,:] = c2



            for i in range(1,len(d)):

                if d[i,0] == 0:
                    d[i,:] = d[i-1,:]

                if d2[i,0] == 0:
                    d2[i,:] = d2[i-1,:]


            #figure('d');plot(d);xlim(0,(width-1))
            #figure('d2');plot(d2);xlim(0,(width-1));spause()#;raw_enter()
            #mi(d.transpose(1,0));spause();raw_enter()
        calls_prev = calls_
            
    except:
        cs('exception',calls)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)






#EOF
