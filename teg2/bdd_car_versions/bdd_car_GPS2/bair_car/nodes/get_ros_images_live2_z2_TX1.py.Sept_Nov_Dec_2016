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
state_transition_time_s = 0

def state_callback(data):
	global state
	state = data.data
def right_callback(data):
	global A,B, left_list, right_list, solver
	A += 1
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(right_list) > 5:
		right_list = right_list[-5:]
	right_list.append(cimg)
def left_callback(data):
	global A,B, left_list, right_list
	B += 1
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(left_list) > 5:
		left_list = left_list[-5:]
	left_list.append(cimg)
def state_transition_time_s_callback(data):
	global state_transition_time_s
	state_transition_time_s = data.data


GPS2_lat = -999.99
GPS2_long = -999.99
GPS2_lat_orig = -999.99
GPS2_long_orig = -999.99
def GPS2_lat_callback(msg):
	global GPS2_lat
	GPS2_lat = msg.data
def GPS2_long_callback(msg):
	global GPS2_long
	GPS2_long = msg.data

camera_heading = 49.0
def camera_heading_callback(msg):
	global camera_heading
	c = msg.data
	#print camera_heading
	if c > 90:
		c = 90
	if c < -90:
		c = -90
	c += 90
	c /= 180.
	
	c *= 99

	if c < 0:
		c = 0
	if c > 99:
		c = 99
	c = 99-c
	camera_heading = int(c)
"""
def GPS2_lat_orig_callback(msg):
	global GPS2_lat_orig
	GPS2_lat_orig = msg.data
def GPS2_long_orig_callback(msg):
	global GPS2_long_orig
	GPS2_long_orig = msg.data
"""
##
########################################################

import thread
import time


rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)
rospy.Subscriber('/bair_car/state', std_msgs.msg.Int32,state_callback)
rospy.Subscriber('/bair_car/state_transition_time_s', std_msgs.msg.Int32, state_transition_time_s_callback)
steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=100)
motor_cmd_pub = rospy.Publisher('cmd/motor', std_msgs.msg.Int32, queue_size=100)

rospy.Subscriber('/bair_car/GPS2_lat', std_msgs.msg.Float32, callback=GPS2_lat_callback)
rospy.Subscriber('/bair_car/GPS2_long', std_msgs.msg.Float32, callback=GPS2_long_callback)
#rospy.Subscriber('/bair_car/GPS2_lat_orig', std_msgs.msg.Float32, callback=GPS2_lat_callback)
#rospy.Subscriber('/bair_car/GPS2_long_orig', std_msgs.msg.Float32, callback=GPS2_long_callback)
rospy.Subscriber('/bair_car/camera_heading', std_msgs.msg.Float32, callback=camera_heading_callback)


ctr = 0

from computer_name import *
from kzpy3.teg2.global_run_params import *

t0 = time.time()
time_step = True
while not rospy.is_shutdown():
	if True: #state in [3,5,6,7]:
		
		#if np.mod(ctr,1000)==0:
		#	print d2s("state =",state)
		#ctr+=1
		#if ctr > 65000:
		#	ctr = 0
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
			#print solver.net.blobs['ip2'].data[0,:]S

			caf_steer = 100*solver.net.blobs['ip2'].data[0,9]
			caf_motor = 100*solver.net.blobs['ip2'].data[0,19]
			if state == 4 and state_transition_time_s > 60:
				print("Shutting down because in state 4 for 60+ s")
				unix('sudo shutdown -h now')
			if True:
				if np.abs(GPS2_lat) > 0 and np.abs(GPS2_lat) > 0:
					if GPS2_lat_orig > -999 and GPS2_long_orig > -999:
						if time_step:
							print(GPS2_lat_orig,GPS2_lat,GPS2_long_orig,GPS2_long)
						if state == 4 and state_transition_time_s > 20:

							GPS2_lat_orig = GPS2_lat; GPS2_long_orig = GPS2_long;
							print("Set GPS2 origin to current coordiates because in state 4 for 20+ s")
						dist = lat_lon_to_dist_meters(GPS2_lat_orig,GPS2_long_orig,GPS2_lat,GPS2_long)
						if dist > GPS2_radius_meters:
							caf_steer = 49
							caf_motor = 49
							if np.mod(int(10*time.time()),10):
								if time_step: #np.mod(ctr,1000) == 0:
									print(d2s("GPS2 stopping car because dist",dist,"> GPS2_radius_meters",GPS2_radius_meters,time_str()))
									ctr += 1
						else:
							if time_step:
								print(d2s("dist =",dist))
				else:
					if time_step:
						print("No GPS fix. "+time_str())

			
			steer_cmd_pub.publish(std_msgs.msg.Int32(caf_steer))
			motor_cmd_pub.publish(std_msgs.msg.Int32(caf_motor))

			if time_step:
				print(d2s("In state",state,"for",state_transition_time_s,"seconds"))

		time_step = False
		if time.time() - t0 > 1.0:
			t0 = time.time()
			time_step = True
	else:
		pass
			



