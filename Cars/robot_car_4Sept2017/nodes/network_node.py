#!/usr/bin/env python
"""
https://answers.ros.org/question/90536/ros-remote-master-can-see-topics-but-no-data/

on roscore machine:
export ROS_IP=0.0.0.0 # Listen on any interface
"""
from kzpy3.utils2 import *
aruco_freq = Timer(5)
import cv2 # befor pytorch_code import on purpose, affects bdd2, maybe not TX1
from pytorch_code import *
import roslib
import std_msgs.msg
import geometry_msgs.msg
import threading
from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
bridge = CvBridge()
rospy.init_node('listener',anonymous=True)

left_list = []
right_list = []
state = '{Not Set}'
steer = 0
potential_collision_from_callback_ = 0
previous_state = 0
state_transition_time_s = 0
state_enter_timer = Timer(0)
freeze = False
torch_motor,torch_steer = None,None
ctr = 0
time_step = Timer(2)
network_enter_timer = Timer(2)
folder_display_timer = Timer(30)
git_pull_timer = Timer(60)
reload_timer = Timer(30)
torch_steer_previous = 49
torch_motor_previous = 49


def state__callback(data):
	global state, previous_state, state_enter_timer
	if state != data.data:
		state_enter_timer = Timer(0)
		previous_state = state
	state = data.data

def steer__callback(data):
	global steer
	steer = data.data

def potential_collision__callback(data):
	global potential_collision_from_callback_
	potential_collision_from_callback_ = data.data

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
steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=10)
motor_cmd_pub = rospy.Publisher('cmd/motor', std_msgs.msg.Int32, queue_size=10)
frozen_cmd_pub = rospy.Publisher('cmd/frozen', std_msgs.msg.Int32, queue_size=10)
heading_pause_pub = rospy.Publisher('cmd/heading_pause', std_msgs.msg.Int32, queue_size=10)
car_in_range_pub = rospy.Publisher('cmd/car_in_range', std_msgs.msg.Int32, queue_size=10)

state = '{Not Set}'

###################
# These imports should go after ros setup section
from kzpy3.Grapher_app.Graph_Image_Module import *
from kzpy3.vis2 import angle_clockwise
from kzpy3.Localization_app.Parameters_Module import *
import kzpy3.data_analysis.Angle_Dict_Creator as Angle_Dict_Creator
from kzpy3.Localization_app.Project_Aruco_Markers_Module import Aruco_Trajectory

#
##################






###################################################################
# aruco markers
aruco_heading_x_pub = rospy.Publisher('/bair_car/aruco_heading_x', std_msgs.msg.Float32, queue_size=10)
aruco_heading_y_pub = rospy.Publisher('/bair_car/aruco_heading_y', std_msgs.msg.Float32, queue_size=10)
aruco_position_x_pub = rospy.Publisher('/bair_car/aruco_position_x', std_msgs.msg.Float32, queue_size=10)
aruco_position_y_pub = rospy.Publisher('/bair_car/aruco_position_y', std_msgs.msg.Float32, queue_size=10)
#other_car_position_pub = rospy.Publisher('/bair_car/other_car_position', geometry_msgs.msg.Vector3, queue_size=10)
#

#

#

#
#
################################################################################3
#

x_min = -(6.03/2.0)#-6.03+hw
x_max = (6.03/2.0)#hw
y_min = -(6.03/2.0)#-hw#
y_max = 6.03/2.0#hw#

tmp = Graph_Image(xmin,x_min, xmax,x_max, ymin,y_min, ymax,y_max, xsize,rp.img_width, ysize,rp.img_width)
potential_image = imread(rp.potential_field_png)
potential_image = 1.0*potential_image[:,:,0]
potential_image = z2o(potential_image)
tmp[img] = potential_image#lo(opjD('Potential_graph_img'))

Potential_graph = Graph_Image(xmin,x_min, xmax,x_max, ymin,y_min, ymax,y_max, xsize,rp.img_width, ysize,rp.img_width, Img,tmp)
#
Polar_Cartesian_dictionary = {}
Pc = Polar_Cartesian_dictionary
for a in range(360):
	ay = np.sin(np.radians(a))
	ax = np.cos(np.radians(a))
	Pc[a]=[ax,ay]
#
def angle_360_correction(angle):
	if angle < 0:
		angle = 360 + angle
	elif angle >= 360:
		angle -= 360
	if angle >= 0 and angle < 360:
		return angle
	else:
		return angle_360_correction(angle)
#
def get_headings(x_pos_input,y_pos_input,heading):
	heading_floats = []
	headings = arange(heading-45,heading+45,22.5/4.0).astype(np.int)
	for a in headings:
		b = angle_360_correction(int(a))
		heading_floats.append(Pc[b])
	heading_floats = na(heading_floats)
	return headings,heading_floats
#

def in_square(x0,y0, x_left, x_right, y_top, y_bottom):
	if x0 >= x_left:
		if x0 < x_right:
			if y0 < y_top:
				if y0 >= y_bottom:
					return True
	return False
#



def get_best_heading(x_pos,y_pos,heading,radius):
	headings,heading_floats = get_headings(x_pos,y_pos,heading)
	middle_heading_index = int(len(headings)/2)
	x1,y1 = Potential_graph[floats_to_pixels](
		x,radius*heading_floats[:,1]+x_pos, y,radius*heading_floats[:,0]+y_pos, NO_REVERSE,False)
	heading_pause = 0
	min_potential = 9999
	min_potential_index = -9999
	for i in rlen(x1):
		if in_square(x1[i],y1[i],0,rp.img_width,rp.img_width,0):
			p = Potential_graph[img][x1[i],y1[i]]
		else:
			p = 1
		if p < min_potential:
			min_potential = p
			min_potential_index = i
		if not heading_pause:
			if np.abs(headings[i]-headings[middle_heading_index]) < rp.heading_pause_threshold_angle:
				p2 = Potential_graph[img][int((x1[i]+x_pos)/2.0),int((y1[i]+y_pos)/2.0)]
				if p2 > rp.heading_float_pause_threshold:
					print p2
					heading_pause = 1
	return headings[min_potential_index],heading_floats,x1,y1,heading_pause
#
###################################################################
#
#
steer_prev = 49
robot_steer = 49
heading_pause = 0
error_timer = Timer(3)
#

x_avg = 0.0
y_avg = 0.0
steer = 0.0
###################################################################
#

###################################################################

message_timer = Timer(0.1)
aruco_error_timer = Timer(rp.aruco_error_time)
aruco_error_print_timer = Timer(rp.aruco_error_time)
aruco_thread_exception_print_timer = Timer(0.3)
def aruco_thread():

	Aruco_trajectory = Aruco_Trajectory()
	P[past_to_present_proportion] = rp.past_to_present_proportion
	global robot_steer,x_avg,y_avg,steer,steer_prev,heading_pause,ssh_command_str

	spd2s('starting aruco_thread . . .')

	error_ctr_ = 0

	x_avg_prev,y_avg_prev = 0.0,0.0
	dx_avg_prev,dy_avg_prev = 0.0,0.0
	while not rospy.is_shutdown():
		if state in [1,6]: 
			try:
				if aruco_error_timer.check():
					heading_pause = 1

				x_avg,y_avg = 0.0,0.0
				dx_avg,dy_avg = 0.0,0.0
				for camera_list_ in [left_list,right_list]:

					camera_img_ = camera_list_[-1]

					angles_to_center, angles_surfaces, distances_marker, markers = Angle_Dict_Creator.get_angles_and_distance(camera_img_,borderColor=None)
					
					if rp.print_marker_ids:
						pd2s('angles_to_center.keys()',angles_to_center.keys())

					Q = {'angles_to_center':angles_to_center,'angles_surfaces':angles_surfaces,'distances_marker':distances_marker}

					hx_,hy_,x_,y_ =	Aruco_trajectory[step](one_frame_aruco_data,Q, p,P)
					x_avg += x_
					y_avg += y_
					dx_avg += hx_-x_
					dy_avg += hy_-y_

				x_avg /= 2.0
				dx_avg /= 2.0
				y_avg /= 2.0
				dy_avg /= 2.0

				x_avg_prev,y_avg_prev = x_avg,y_avg
				dx_avg_prev,dy_avg_prev = dx_avg,dy_avg

				heading = angle_clockwise((0,1),(dx_avg,dy_avg))

				###

				heading_new,heading_floats,x1,y1,heading_pause = get_best_heading(rp.X_PARAM*x_avg,rp.Y_PARAM*y_avg,heading,rp.radius)
			


				heading_delta = (heading_new - heading)
				
				steer = heading_delta*(-99.0/45)

				steer =int((steer-49.0)*rp.robot_steer_gain+49.0)
				steer = min(99,steer)
				steer = max(0,steer)
				steer = int((1.0-rp.steer_momentum)*steer+rp.steer_momentum*steer_prev)
				steer_prev = steer
				if rp.print_steer:
					pd2s('steer =',steer)
				robot_steer = steer

				if True:
					aruco_position_x_pub.publish(std_msgs.msg.Float32(x_avg))
					aruco_position_y_pub.publish(std_msgs.msg.Float32(y_avg))
					aruco_heading_x_pub.publish(std_msgs.msg.Float32(dx_avg))
					aruco_heading_y_pub.publish(std_msgs.msg.Float32(dy_avg))
					heading_pause_pub.publish(std_msgs.msg.Int32(heading_pause))

				aruco_freq.freq()
				error_ctr_ = 0
				aruco_error_timer.reset()

			except Exception as e:
				aruco_position_x_pub.publish(std_msgs.msg.Float32(x_avg_prev))
				aruco_position_y_pub.publish(std_msgs.msg.Float32(y_avg_prev))
				aruco_heading_x_pub.publish(std_msgs.msg.Float32(dx_avg_prev))
				aruco_heading_y_pub.publish(std_msgs.msg.Float32(dy_avg_prev))
				heading_pause_pub.publish(std_msgs.msg.Int32(heading_pause))

		else:
			time.sleep(0.1)
#
threading.Thread(target=aruco_thread).start()
#
###################################################################

def car_print(stri,name=rp.computer_name):
	print(stri)


state_messenger = Timer(1)
while not rospy.is_shutdown():

	if reload_timer.check(): # put in thread?
		reload(rp)
		reload_timer.reset()


	if state == 6:

		if len(left_list) > nframes + 2:
			if False:
				camera_data = format_camera_data(left_list, right_list)
				metadata = format_metadata((rp.Racing, 0, rp.Follow, rp.Direct, rp.Play, rp.Furtive))
				torch_motor, torch_steer = run_model(camera_data, metadata)

			if ((defrosted_timer.time()<2 and potential_collision_ < rp.potential_motor_freeze_collision) or potential_collision_ == 0) and not (heading_pause or frozen_):

				frozen_cmd_pub.publish(std_msgs.msg.Int32(frozen_))
				
				if state == 6:
					steer_cmd_pub.publish(std_msgs.msg.Int32(robot_steer))
					motor_cmd_pub.publish(std_msgs.msg.Int32(rp.robot_motor))


			elif heading_pause:
				if error_timer.check():
					srpd2s('heading_pause')
					error_timer.reset()
					
				if state == 6:          
					steer_cmd_pub.publish(std_msgs.msg.Int32(49))
					motor_cmd_pub.publish(std_msgs.msg.Int32(49))	
	else:
		potential_collision_ = 0
		network_enter_timer.reset()
	
	shutdown_time = 30
	if state == 4 and state_enter_timer.time() > shutdown_time-5:
		car_print('!!! about to reboot from state 4 !!! ' + str(steer))
	if state == 4 and state_enter_timer.time() > shutdown_time:
		car_print(d2s("Rebooting because in state 4 for",shutdown_time,"+ s"))
		unix('sudo reboot')

	if time_step.check():

		car_print(d2s(rp.computer_name,"in state <",state,"> for",dp(state_enter_timer.time()),"seconds, previous_state =",previous_state,'frozen_ =',frozen_,'heading_pause =', heading_pause))
		time_step.reset()

stop_ros()


