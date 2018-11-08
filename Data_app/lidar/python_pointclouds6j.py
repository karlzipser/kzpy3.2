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



net_input_width = 168
net_input_height = 94

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
                for i in [0,1,2]:
                    half_width = half_widths[i]
                    f = cv2.resize(
                            d2[width/2 - half_width:width/2 + half_width, :],
                            (net_input_height,net_input_width)
                        ).transpose(1,0)
                    f = (255*z2o(f)).astype(int)
                    e.append(f)

                Output['e'] = e








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


if __name__ == '__main__':
    rospy.init_node('receive_pointclouds')
    rospy.Subscriber('/os1_node/points', PointCloud2, points__callback)
    threading.Thread(target=pointcloud_thread,args=[]).start()





#EOF
