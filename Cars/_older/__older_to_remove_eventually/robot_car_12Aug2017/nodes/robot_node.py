#!/usr/bin/env python

from kzpy3.utils2 import *
from kzpy3.vis2 import *
import roslib
import std_msgs.msg
import geometry_msgs.msg
import rospy
import cv2
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
import kzpy3.data_analysis.Angle_Dict_Creator as Angle_Dict_Creator
bridge = CvBridge()


R = {}
for topic_ in [left_image,right_image]:
	R[topic_] = {ts:[],vals:[]}



def left_image__callback(data):
	R[left_image][ts].append(time.time())
	R[left_image][vals].append( bridge.imgmsg_to_cv2(data,"rgb8") )
	R[left_image][ts] = R[left_image][ts][-2:]
	R[left_image][vals] = R[left_image][vals][-2:]

def right_image__callback(data):
	R[right_image][ts].append(time.time())
	R[right_image][vals].append( bridge.imgmsg_to_cv2(data,"rgb8") )
	R[right_image][ts] = R[right_image][ts][-2:]
	R[right_image][vals] = R[right_image][vals][-2:]


rospy.init_node('listener',anonymous=True)


rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_image__callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_image__callback,queue_size = 1)


GRAPHICS = True


while not rospy.is_shutdown():
	try:
		camera_img_ = R[right_image][vals][-1].copy()
		angles_to_center, angles_surfaces, distances_marker, markers = Angle_Dict_Creator.get_angles_and_distance(camera_img_)
		if GRAPHICS:
			key_ = mci(camera_img_,color_mode=cv2.COLOR_RGB2BGR,delay=33,title='right_image')
		camera_img_ = R[left_image][vals][-1].copy()
		angles_to_center, angles_surfaces, distances_marker, markers = Angle_Dict_Creator.get_angles_and_distance(camera_img_)
		if GRAPHICS:
			key_ = mci(camera_img_,color_mode=cv2.COLOR_RGB2BGR,delay=33,title='left_image')


	except Exception as e:
		print("********** robot_node.py Exception ***********************")
		print(e.message, e.args)	


stop_ros()

#EOF