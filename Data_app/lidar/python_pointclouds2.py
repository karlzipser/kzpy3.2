#!/usr/bin/env python
from kzpy3.vis3 import *
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2import

P = []
ABORT = False

def cloud_callback(msg):
    global P
    if ABORT:
        return
    for p in pc2.read_points(msg,skip_nans=True,field_names=("x","y","z")):
          if np.abs(p[0]) > 0:
              P.append(p)

if __name__ == '__main__':
    import rospy
    from std_msgs.msg import Empty
    rospy.init_node('test_pointclouds')
    rospy.Subscriber('/os1_node/points', PointCloud2, cloud_callback)
    timer = Timer(0.2)
    while not timer.check():
	    pass
    print('ABORT')
    ABORT = True          
    so(opjD('P'),P)
 
