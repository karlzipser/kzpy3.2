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
    timer = Timer(600)
    CA()
    ctr = 0
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
            if False:
                p=P[-1]
                a=np.resize(p,(1024,64,3))
                b=np.sqrt(a[:,:,0]**2+a[:,:,1]**2+a[:,:,2]**2)
                clf()
                plot(b,',')
                ylim(0,8)
                spause()
                #clf();plot(P[-2][:,0],P[-2][:,1],'.')
            if False:
                ctr += 1
                if ctr >= 30:
                    clf()
                    ctr = 0
                #for k in rlen(P):
                k=-1
                p=P[k]
                a=np.resize(p,(1024,64,3))
                r=range(1,64)
                b=a[:,r,:]
                d = b[:,1,:]
                e=np.sqrt(b[:,:,0]**2+b[:,:,1]**2+b[:,:,2]**2)
                c = zeros(1024);
                for i in range(1024):
                    x,y = d[i,0],d[i,1]
                    q = np.degrees(angle_between((1,0), (x,y)) )
                    if y > 0:
                        q*=-1
                    c[i] = q
                figure('c');plot(c,'.');spause()
            if True:#for k in rlen(P):#if True:
                k=-1
                p=P[k]
                a=np.resize(p,(1024,64,3))
                a=a[(512-120):(512+120),:,:]
                r=range(1,64,4)
                b=a[:,r,:]
                e=np.sqrt(b[:,:,0]**2+b[:,:,1]**2+b[:,:,2]**2)
                e[e>10]=10
                f=cv2.resize(e,(64,240))
                mi(z2o(f));spause()
            #print calls
        except:
            cs('exception',calls)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

        #raw_enter()
