"""
reed to run roslaunch first, e.g.,

roslaunch bair_car bair_car.launch use_zed:=true record:=false
"""

import roslib
import cv2
from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
import scipy
import numpy as np

bridge = CvBridge()


rospy.init_node('listener',anonymous=True)

A = 0

def callback(data):
	global A
	A += 1
	print A
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	cv2.imshow("Image Window",np.flipud(cimg))
	cv2.waitKey(1)


rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,callback)

rospy.spin()
