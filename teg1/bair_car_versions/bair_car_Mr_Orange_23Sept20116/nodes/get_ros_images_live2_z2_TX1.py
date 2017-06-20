#!/usr/bin/env python

"""
reed to run roslaunch first, e.g.,

roslaunch bair_car bair_car.launch use_zed:=true record:=false
"""

########################################################
#          CAFFE SETUP SECTION
import caffe
caffe.set_device(0)
caffe.set_mode_gpu()
from kzpy3.utils import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files2 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt

solver_file_path = opjh("kzpy3/caf3/z2/solver_live.prototxt")
weights_file_path = opjD('z2/z2.caffemodel') #
def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver
solver = setup_solver()
if weights_file_path != None:
	print "loading " + weights_file_path
	solver.net.copy_from(weights_file_path)
#
########################################################


########################################################
#          ROSPY SETUP SECTION
import roslib
import std_msgs.msg
import cv2
from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
bridge = CvBridge()
rospy.init_node('listener',anonymous=True)

left_list = []
right_list = []
A = 0
B = 0
state = 0

def state_callback(data):
	state = data

def right_callback(data):
	global A,B, left_list, right_list, solver
	A += 1
	
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(right_list) > 5:
		right_list = right_list[-5:]
	right_list.append(cimg)
	#cv2.imshow("Left",solver.net.blobs['ZED_data_pool2'].data[0,1,:,:]/255.0)
	#cv2.imshow("Right",solver.net.blobs['ZED_data_pool2'].data[0,3,:,:]/255.0)
	#cv2.waitKey(1)

def left_callback(data):
	global A,B, left_list, right_list
	B += 1
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(left_list) > 5:
		left_list = left_list[-5:]
	left_list.append(cimg)
	#cv2.imshow("Left",cimg)
	#cv2.waitKey(1)
##
########################################################

import thread
import time

# Define a function for the thread
#def print_time( threadName, delay):

rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)
rospy.Subscriber('/bair_car/state', std_msgs.msg.Int32,state_callback)
steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=100)
motor_cmd_pub = rospy.Publisher('cmd/motor', std_msgs.msg.Int32, queue_size=100)
#rospy.spin()

# Create two threads as follows
#try:
#   thread.start_new_thread( print_time, ("Thread-1", 2, ) )

#except:
#   print "Error: unable to start thread"




#rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback)
#rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback)

while not rospy.is_shutdown():
	#print (A,B,len(left_list),len(right_list))
	try:
		pass
		#cv2.imshow("Left",left_list[-1])
		#cv2.waitKey(1)
	except:
		pass
	if len(left_list) > 4:
		l0 = left_list[-2]
		l1 = left_list[-1]
		r0 = right_list[-2]
		r1 = right_list[-1]

		solver.net.blobs['ZED_data'].data[0,0,:,:] = l0[:,:,1]/255.0-.5
		solver.net.blobs['ZED_data'].data[0,1,:,:] = l1[:,:,1]/255.0-.5
		solver.net.blobs['ZED_data'].data[0,2,:,:] = r0[:,:,1]/255.0-.5
		solver.net.blobs['ZED_data'].data[0,3,:,:] = r1[:,:,1]/255.0-.5
		from computer_name import *	
		"""
		Direct = 1.
		Follow = 0.
		Play = 0.
		Furtive = 0.
		Caf = 1.0
		"""
		solver.net.blobs['metadata'].data[0,0,:,:] = 0#target_data[0]/99. #current steer
		solver.net.blobs['metadata'].data[0,1,:,:] = Caf#target_data[len(target_data)/2]/99. #current motor
		solver.net.blobs['metadata'].data[0,2,:,:] = Follow
		solver.net.blobs['metadata'].data[0,3,:,:] = Direct
		solver.net.blobs['metadata'].data[0,4,:,:] = Play
		solver.net.blobs['metadata'].data[0,5,:,:] = Furtive


		#solver.net.forward(start='ZED_data',end='ZED_data_pool1')
		#solver.net.forward(start='ZED_data_pool1',end='ZED_data_pool2')
		#solver.net.forward(start='ZED_data_pool2',end='conv1')
		
		solver.net.forward()
		#print solver.net.blobs['ip2'].data[0,:]
		steer_cmd_pub.publish(std_msgs.msg.Int32(100*solver.net.blobs['ip2'].data[0,9]))
		motor_cmd_pub.publish(std_msgs.msg.Int32(100*solver.net.blobs['ip2'].data[0,19]))
		#solver.step(100)
		
		#cv2.imshow("Right",solver.net.blobs['ZED_data_pool2'].data[0,3,:,:]/255.0)
		




#rospy.spin()
