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
import runtime_parameters as rp
bridge = CvBridge()

reload_timer = Timer(10)

R = {}
for topic_ in [steer, motor, state, encoder,
	acc_x,acc_y,acc_z,
	gyro_x,gyro_y,gyro_z,
	gyro_heading_x,gyro_heading_y,gyro_heading_z,
	left_image,right_image
	]:
	R[topic_] = {ts:[],vals:[]}

n_ = 20
def steer__callback(msg):
	R[steer][ts].append(time.time())
	R[steer][vals].append(msg.data)
	if len(R[steer][ts]) > 1.5*n_:
		R[steer][ts] = 		R[steer][ts][-n_:]
		R[steer][vals] = 	R[steer][vals][-n_:]

def motor__callback(msg):
	R[motor][ts].append(time.time())
	R[motor][vals].append(msg.data)
	if len(R[motor][ts]) > 1.5*n_:
		R[motor][ts] = 		R[motor][ts][-n_:]
		R[motor][vals] = 	R[motor][vals][-n_:]

def state__callback(msg):
	R[state][ts].append(time.time())
	R[state][vals].append(msg.data)
	if len(R[state][ts]) > 1.5*n_:
		R[state][ts] = 		R[state][ts][-n_:]
		R[state][vals] = 	R[state][vals][-n_:]

def encoder__callback(msg):
	R[encoder][ts].append(time.time())
	R[encoder][vals].append(msg.data)
	if len(R[encoder][ts]) > 1.5*n_:
		R[encoder][ts] = 		R[encoder][ts][-n_:]
		R[encoder][vals] = 		R[encoder][vals][-n_:]

def acc__callback(msg):
	t_ = time.time()
	R[acc_x][ts].append(t_)
	R[acc_x][vals].append(msg.x)
	R[acc_y][ts].append(t_)
	R[acc_y][vals].append(msg.y)
	R[acc_z][ts].append(t_)
	R[acc_z][vals].append(msg.z)
	if len(R[acc_x][ts]) > 1.5*n_:
		R[acc_x][ts] = 		R[acc_x][ts][-n_:]
		R[acc_x][vals] = 	R[acc_x][vals][-n_:]
		R[acc_y][ts] = 		R[acc_y][ts][-n_:]
		R[acc_y][vals] = 	R[acc_y][vals][-n_:]
		R[acc_z][ts] = 		R[acc_z][ts][-n_:]
		R[acc_z][vals] = 	R[acc_z][vals][-n_:]

def gyro__callback(msg):
	t_ = time.time()
	R[gyro_x][ts].append(t_)
	R[gyro_x][vals].append(msg.x)
	R[gyro_y][ts].append(t_)
	R[gyro_y][vals].append(msg.y)
	R[gyro_z][ts].append(t_)
	R[gyro_z][vals].append(msg.z)
	if len(R[gyro_x][ts]) > 1.5*n_:
		R[gyro_x][ts] = 	R[gyro_x][ts][-n_:]
		R[gyro_x][vals] = 	R[gyro_x][vals][-n_:]
		R[gyro_y][ts] = 	R[gyro_y][ts][-n_:]
		R[gyro_y][vals] = 	R[gyro_y][vals][-n_:]
		R[gyro_z][ts] = 	R[gyro_z][ts][-n_:]
		R[gyro_z][vals] = 	R[gyro_z][vals][-n_:]

def gyro_heading__callback(msg):
	t_ = time.time()
	R[gyro_heading_x][ts].append(t_)
	R[gyro_heading_x][vals].append(msg.x)
	R[gyro_heading_y][ts].append(t_)
	R[gyro_heading_y][vals].append(msg.y)
	R[gyro_heading_z][ts].append(t_)
	R[gyro_heading_z][vals].append(msg.z)
	if len(R[gyro_heading_x][ts]) > 1.5*n_:
		R[gyro_heading_x][ts] = 	R[gyro_heading_x][ts][-n_:]
		R[gyro_heading_x][vals] = 	R[gyro_heading_x][vals][-n_:]
		R[gyro_heading_y][ts] = 	R[gyro_heading_y][ts][-n_:]
		R[gyro_heading_y][vals] = 	R[gyro_heading_y][vals][-n_:]
		R[gyro_heading_z][ts] = 	R[gyro_heading_z][ts][-n_:]
		R[gyro_heading_z][vals] = 	R[gyro_heading_z][vals][-n_:]

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

rospy.Subscriber('/bair_car/steer', std_msgs.msg.Int32, callback=steer__callback)
rospy.Subscriber('/bair_car/motor', std_msgs.msg.Int32, callback=motor__callback)
rospy.Subscriber('/bair_car/state', std_msgs.msg.Int32, callback=state__callback)
rospy.Subscriber('/bair_car/encoder', std_msgs.msg.Float32, callback=encoder__callback)
rospy.Subscriber('/bair_car/acc', geometry_msgs.msg.Vector3, callback=acc__callback)
rospy.Subscriber('/bair_car/gyro', geometry_msgs.msg.Vector3, callback=gyro__callback)
rospy.Subscriber('/bair_car/gyro_heading', geometry_msgs.msg.Vector3, callback=gyro_heading__callback)
rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_image__callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_image__callback,queue_size = 1)

robot_in_charge_pub_ = rospy.Publisher('cmd/robot_in_charge', std_msgs.msg.Int32, queue_size=100)

GRAPHICS = True


robot_in_charge_ = 0
robot_in_charge_exit_timer_ = Timer(2) # gives time to get to normal acc values after car turn signal

while not rospy.is_shutdown():
	try:
		camera_img_ = R[left_image][vals][-1].copy()
		angles_to_center, angles_surfaces, distances_marker, markers = Angle_Dict_Creator.get_angles_and_distance(camera_img_)
		if GRAPHICS:
			key_ = mci(camera_img_,color_mode=cv2.COLOR_RGB2BGR,delay=33,title='topics')
	except Exception as e:
		print("********** robot_node.py Exception ***********************")
		print(e.message, e.args)	


stop_ros()
