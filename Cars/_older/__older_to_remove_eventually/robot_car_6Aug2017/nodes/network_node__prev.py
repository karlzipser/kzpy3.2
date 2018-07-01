#!/usr/bin/env python

import cv2 # befor pytorch_code import on purpose, affects bdd2, maybe not TX1
from pytorch_code import *
import roslib
import std_msgs.msg
import geometry_msgs.msg

from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
bridge = CvBridge()
rospy.init_node('listener',anonymous=True)

left_list = []
right_list = []
state = 0
steer = 0
previous_state = 0
state_transition_time_s = 0
state_enter_time = 0
freeze = False
torch_motor,torch_steer = None,None
ctr = 0
time_step = Timer(2)
network_enter_timer = Timer(0.3)
folder_display_timer = Timer(30)
git_pull_timer = Timer(60)
reload_timer = Timer(10)
torch_steer_previous = 49
torch_motor_previous = 49


def state__callback(data):
	global state, previous_state, state_enter_time
	# data.data = 6
	if state != data.data:
		state_enter_time = time.time()
		if state in [3,5,6,7] and previous_state in [3,5,6,7]:
			pass
		else:
			previous_state = state
	state = data.data

def steer__callback(data):
	global steer
	steer = data.data

def right_image__callback(data):
	global left_list, right_list, solver
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(right_list) > nframes + 3:
		right_list = right_list[-(nframes + 3):]
	right_list.append(cimg)

def left_image__callback(data):
	global left_list, right_list
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(left_list) > nframes + 3:
		left_list = left_list[-(nframes + 3):]
	left_list.append(cimg)

def state_transition_time_s__callback(data):
	global state_transition_time_s
	state_transition_time_s = data.data

rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_image__callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_image__callback,queue_size = 1)
rospy.Subscriber("/bair_car/steer", std_msgs.msg.Int32,steer__callback)
rospy.Subscriber('/bair_car/state', std_msgs.msg.Int32,state__callback)
steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=100)
motor_cmd_pub = rospy.Publisher('cmd/motor', std_msgs.msg.Int32, queue_size=100)
freeze_cmd_pub = rospy.Publisher('cmd/freeze', std_msgs.msg.Int32, queue_size=100)
model_name_pub = rospy.Publisher('/bair_car/model_name', std_msgs.msg.String, queue_size=10)




while not rospy.is_shutdown():
	if state in [3,5,6,7]:
		if (previous_state not in [3,5,6,7]):
			previous_state = state
			network_enter_timer.reset()
		if not network_enter_timer.check():
			print "waiting before entering network mode..."
			steer_cmd_pub.publish(std_msgs.msg.Int32(49))
			motor_cmd_pub.publish(std_msgs.msg.Int32(49))
			time.sleep(0.1)
			continue
		else:
			if len(left_list) > nframes + 2:
				camera_data = format_camera_data(left_list, right_list)
				metadata = format_metadata((rp.Racing, 0, rp.Follow, rp.Direct, rp.Play, rp.Furtive))

				torch_motor, torch_steer = run_model(camera_data, metadata)

				freeze_cmd_pub.publish(std_msgs.msg.Int32(freeze))
				
				if state in [3,6]:          
					steer_cmd_pub.publish(std_msgs.msg.Int32(torch_steer))
				if state in [6,7]:
					motor_cmd_pub.publish(std_msgs.msg.Int32(torch_motor))
	else:
		network_enter_timer.reset()
	

	shutdown_time = 30
	if state == 4 and time.time()-state_enter_time > shutdown_time-5:
		print('!!! about to reboot from state 4 !!! ' + str(steer))
	if state == 4 and time.time()-state_enter_time > shutdown_time:
		print(d2s("Rebooting because in state 4 for",shutdown_time,"+ s"))
		unix('sudo reboot')


	if time_step.check():
		print(torch_steer,torch_motor)
		print(d2s("In state",state,"for",dp(time.time()-state_enter_time),"seconds, previous_state =",previous_state))
		time_step.reset()

stop_ros()
