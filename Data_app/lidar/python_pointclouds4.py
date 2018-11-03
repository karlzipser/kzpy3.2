#!/usr/bin/env python

from kzpy3.vis3 import *
import sensor_msgs
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import rospy





P = []
calls = 0
calls_prev = 0
ABORT = False

def points__callback(msg):
    if ABORT:
        return
    global P
    global calls
    calls += 1
    valv_temp = list(pc2.read_points(msg,skip_nans=False,field_names=("intensity","reflectivity","ring")))
    valv_temp = na(valv_temp)
    valv_temp[np.isnan(valv_temp)] = 0
    P.append(valv_temp)


if __name__ == '__main__':
    

    rospy.init_node('test_pointclouds')

    rospy.Subscriber('/os1_node/points', PointCloud2, points__callback)

    timer = Timer(30)

    CA()

    ctr = 0

    images = []

    while not timer.check():

        try:
            k=-1
            calls_ = calls
            if calls_ > calls_prev:
                p = P[k]
                a = np.resize(p,(1024,64,3))
                r = range(1,64,4)
                b = a[:,r,:]
                c = b[:,:,0]
                d = cv2.resize(c.astype(float),(64,1024))
                e = d.transpose(1,0)
                images.append(e)
                #mi(np.log(e),'reflectivity')
                spause()
                calls_prev = calls_

        except:
            cs('exception',calls)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
    if True:
        for k in rlen(images):
            mi(np.log(images[k]),'reflectivity')
            spause()
            #raw_enter()

if False:
    P=lo(opjD('P'))
    for k in rlen(P):
        #k=0
        p = P[k]
        a = np.resize(p,(1024,64,3))
        r=range(1,64,4)
        b=a[:,r,:]
        c = b[:,:,0]
        d=cv2.resize(c.astype(float),(64,1024))
        e = d.transpose(1,0)
        mi(np.log(e),'d')
        spause()
