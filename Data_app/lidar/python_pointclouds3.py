#!/usr/bin/env python
from kzpy3.vis3 import *
from sensor_msgs.msg import PointCloud2, PointField
import sensor_msgs.point_cloud2 as pc2
import sensor_msgs
import numpy as np
import struct





P = []
calls = 0
ABORT = False

def points__callback(msg):
    if ABORT:
        return
    global P
    global calls
    calls += 1
    valv_temp = list(sensor_msgs.point_cloud2.read_points(msg,skip_nans=False,field_names=("x","y","z")))
    valv_temp = na(valv_temp)
    valv_temp[np.isnan(valv_temp)] = 0
    P.append(valv_temp)


def cloud_cb(msg):
    if ABORT:
        return
    global P
    #P = pointcloud2_to_array(msg)
    for p in pc2.read_points(msg,skip_nans=True,field_names=("x","y","z")):
          if np.abs(p[0]) > 0:
              P.append(na(p))
          #print p[0],p[1],p[

if __name__ == '__main__':
    import rospy

    rospy.init_node('test_pointclouds')

    rospy.Subscriber('/os1_node/points', PointCloud2, points__callback)
    #figure(1);plt_square();xylim(-5,5,-5,5)
    timer = Timer(2)
    CA()
    while not timer.check():
        try:
            if False:
                p=P[-2]
                print shape(p)
                p[p>10] = 0
                p[p<-10] = 0
                p = (10*p).astype(int)
                p += 100
                clf()
                plot(p[:,0],p[:,1],'k,')
                #xylim(-20,20,-20,20)
                plt_square()
                spause()
            if True:
                p=P[-1]
                a=np.resize(p,(1024,64,3))
                b=np.sqrt(a[:,:,0]**2+a[:,:,1]**2+a[:,:,2]**2)
                clf()
                plot(b,',')
                ylim(0,8)
                spause()
                #clf();plot(P[-2][:,0],P[-2][:,1],'.')
            
            #print calls
        except:
            cs('exception',calls)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

        #raw_enter()
