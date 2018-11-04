#!/usr/bin/env python

from kzpy3.vis3 import *
import sensor_msgs
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import rospy
import kzpy3.Data_app.lidar.imagestack as imagestack
"""
Names = {
    "x":"x","angle":"y","depth":"z","t":"t",
    "reflectivity":"reflectivity",
    "intensity":"intensity",
    "ring":"ring",
}
"""
names = [
    "x","y","z","t",
    "reflectivity",
    "intensity",
    "ring",
]

########################################################
#
A = Arguments

if 'mode' not in A:
    A['mode'] = 'offline'

if 'time' not in A:
    A['time'] = 10
else:
    assert type(A['time']) == int

if '1' not in A:
    A['fields_to_show'] = ["y","z","reflectivity","intensity"]
else:
    A['fields_to_show'] = []
    for i in range(20):
        if str(i) in A:
            A['fields_to_show'].append(A[str(i)])
            del A[str(i)]
for f in A['fields_to_show']:
    if f not in names:
        cr(f,'not in',names)
        assert(False)

if 'save_Images' not in A:
    A['save_Images'] = False
elif A['save_Images'] in ['y','yes','True']:
    A['save_Images'] = True
else:
    A['save_Images'] = False

if 'show_live_Images' not in A:
    A['show_live_Images'] = False
elif A['show_live_Images'] in ['y','yes','True']:
    A['show_live_Images'] = True
else:
    A['show_live_Images'] = False

print_Arguments()
#
########################################################

###############################
#    
Image_stack = imagestack.Image_Stack(None,A['fields_to_show'])
#
###############################

if A['mode'] == 'live':
    P = []
    calls = 0
    calls_prev = 0
    ABORT = False

    field_names= A['fields_to_show']

    def points__callback(msg):
        if ABORT:
            return
        global P
        global calls
        calls += 1
        p = list(pc2.read_points(msg,skip_nans=False,field_names=field_names))
        p = na(p)
        p[np.isnan(p)] = 0
        P.append(p)

    rospy.init_node('receive_pointclouds')

    rospy.Subscriber('/os1_node/points', PointCloud2, points__callback)

    CA()

    ctr = 0

    Images = {}

    for q in A['fields_to_show']:
        Images[q] = []

    waiting = Timer(1)

    while calls < 1:
        waiting.message('waiting for data')
        time.sleep(0.01)

    timer = Timer(A['time'])

    cg("processing ROSbag data...")

    while not timer.check():

        waiting.message(d2s('Processing ROSbag data...',time_str()))

        try:
            calls_ = calls
            if calls_ > calls_prev:
                p = P[-1]
                a = np.resize(p,(1024,64,len(field_names)))
                r = range(1,64,4)
                b = a[:,r,:]
                for i in rlen(field_names):
                    c = b[:,:,i]
                    d = cv2.resize(c.astype(float),(64,1024))
                    e = d.transpose(1,0)
                    Images[field_names[i]].append(e)
                calls_prev = calls_
                if A['show_live_Images']:
                    Image = {}
                    for q in Images.keys():
                        Image[q] = Images[q][-1]
                    ###############################
                    #    
                    Image_stack['show'](Image)
                    #
                    ###############################                   

        except:
            cs('exception',calls)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

    cg("Done.")

    if A['save_Images']:
        so(opjD('Images_'+time_str()),Images)












elif A['mode'] == 'offline':

    

    

    if 'Images' not in locals():
        Images = lo('/home/karlzipser/Desktop/Images_03Nov18_12h32m24s.pkl' )
        #Images = lo("/home/karlzipser/Desktop/Images_04Nov18_00h04m14s.pkl")
        pass

    duration_timer = Timer(A['time'])

    CA()

    for k in range(2,len(an_element(Images))):

        if duration_timer.check():
            cb("Duration timer check, breaking.")
            break

        Image = {}
        for q in Images.keys():
            Image[q] = Images[q][k]

        ###############################
        #    
        Image_stack['show'](Image)
        #
        ###############################

else:
    cr(d2n("Error, unknown mode '",A['mode'],"'"))
    raw_enter()

#EOF