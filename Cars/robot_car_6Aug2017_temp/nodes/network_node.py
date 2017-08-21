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

from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
bridge = CvBridge()
rospy.init_node('listener',anonymous=True)

left_list = []
right_list = []
state = 0
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
network_ignore_potential_collision = Timer(2) # starting driving triggers the collision IMU detector
folder_display_timer = Timer(30)
git_pull_timer = Timer(60)
reload_timer = Timer(10)
torch_steer_previous = 49
torch_motor_previous = 49


def state__callback(data):
	global state, previous_state, state_enter_timer
	# data.data = 6
	if state != data.data:
		state_enter_timer = Timer(0)
		if state in [3,5,6,7] and previous_state in [3,5,6,7]:
			pass
		else:
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
rospy.Subscriber('/bair_car/potential_collision', std_msgs.msg.Int32,potential_collision__callback)
steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=10)
motor_cmd_pub = rospy.Publisher('cmd/motor', std_msgs.msg.Int32, queue_size=10)
frozen_cmd_pub = rospy.Publisher('cmd/frozen', std_msgs.msg.Int32, queue_size=10)



###################################################################
# aruco markers
aruco_heading_x_pub = rospy.Publisher('/bair_car/aruco_heading_x', std_msgs.msg.Float32, queue_size=10)
aruco_heading_y_pub = rospy.Publisher('/bair_car/aruco_heading_y', std_msgs.msg.Float32, queue_size=10)
aruco_position_x_pub = rospy.Publisher('/bair_car/aruco_position_x', std_msgs.msg.Float32, queue_size=10)
aruco_position_y_pub = rospy.Publisher('/bair_car/aruco_position_y', std_msgs.msg.Float32, queue_size=10)
#
import threading
#
#heading_steering_coordinates = lo(opjD('heading_steering_coordinates'))
wall_length = 4*107.0/100.0
#
from kzpy3.vis2 import angle_clockwise
#
#
################################################################################3
#
from kzpy3.Grapher_app.Graph_Image_Module import *
wall_length = 4*107.0/100.0
half_wall_length = wall_length/2.0
hw = half_wall_length
tmp = Graph_Image(xmin,-hw, xmax,6.03-hw, ymin,-hw, ymax,hw, xsize,35, ysize,25)
#tmp[img] = cv2.blur(lo(opjD('Potential_graph_img')),(rp.potential_graph_blur,rp.potential_graph_blur))
tmp[img] = lo(opjD('Potential_graph_img'))
#tmp[img][18:21,10:15] = 1.0
#tmp[img] = cv2.blur(tmp[img],(rp.potential_graph_blur,rp.potential_graph_blur))

Potential_graph = Graph_Image(xmin,-hw, xmax,hw, ymin,-hw, ymax,hw, xsize,35, ysize,25, Img,tmp)
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

	x1,y1 = Potential_graph[floats_to_pixels](
		x,radius*heading_floats[:,1]+x_pos, y,radius*heading_floats[:,0]+y_pos, NO_REVERSE,False)

	min_potential = 9999
	min_potential_index = -9999
	for i in rlen(x1):
		if in_square(x1[i],y1[i],0,35,25,0):
			p = Potential_graph[img][x1[i],y1[i]]
			#print i,dp(p),dp(headings[i])
		else:
			p = 1
		if p < min_potential:
			min_potential = p
			min_potential_index = i

	return headings[min_potential_index],heading_floats,x1,y1
#
###################################################################
#
def get_steer(*args):
	Args = args_to_dictionary(args);_=da
	x = _(Args,X)
	y = _(Args,Y)
	dx = _(Args,DX)
	dy = _(Args,DY)
	True
	a = angle_clockwise((0,1),(dx,dy))

	if a >= 345 or a < 15:
		binned_angle = 0;
	elif a >= 15 and a < 45:
		binned_angle = 30;
	elif a >= 45 and a < 75:
		binned_angle = 60
	elif a >= 75 and a < 105:
		binned_angle = 90
	elif a >= 105 and a < 135:
		binned_angle = 120
	elif a >= 135 and a < 165:
		binned_angle = 150
	elif a >= 165 and a < 195:
		binned_angle = 180
	elif a >= 195 and a < 225:
		binned_angle = 210
	elif a >= 225 and a < 255:
		binned_angle = 240
	elif a >= 255 and a < 285:
		binned_angle = 270
	elif a >= 285 and a < 315:
		binned_angle = 300
	elif a >= 315 and a < 345:
		binned_angle = 330;

	px = int(x*7.0/wall_length + 4.0)
	py = int(y*7.0/wall_length + 4.0)
	#steer = int(heading_steering_coordinates[binned_angle][px,py])

	#return steer
#
steer_prev = 49
robot_steer = 49
error_timer = Timer(3)
#
from kzpy3.Localization_app.Parameters_Module import *
#figure(5);clf();plt_square();xysqlim(2*107.0/100.0);
x_avg = 0.0
y_avg = 0.0
steer = 0.0

import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
def paramiko_thread():
	connected = False
	while connected == False:
		try:
			ssh.connect('192.168.1.10', username='nvidia',password='nvidia')
			connected = True
			spd2s('ssh connection established.')
		except:
			spd2s('ssh connection failed . . . [will retry]')
			time.sleep(0.5)

threading.Thread(target=paramiko_thread).start()

def aruco_thread():
	import kzpy3.data_analysis.Angle_Dict_Creator as Angle_Dict_Creator
	
	from kzpy3.Localization_app.Project_Aruco_Markers_Module import Aruco_Trajectory
	Aruco_trajectory = Aruco_Trajectory()
	P[past_to_present_proportion] = rp.past_to_present_proportion
	global robot_steer,x_avg,y_avg,steer,steer_prev

	print('starting aruco_thread . . .')

	error_ctr_ = 0

	while not rospy.is_shutdown():
		try:
			x_avg,y_avg = 0.0,0.0
			dx_avg,dy_avg = 0.0,0.0
			for camera_list_ in [left_list,right_list]:

				camera_img_ = camera_list_[-1]

				angles_to_center, angles_surfaces, distances_marker, markers = Angle_Dict_Creator.get_angles_and_distance(camera_img_,borderColor=None)
				
				if rp.print_marker_ids:
					print angles_to_center.keys()

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


			heading = angle_clockwise((0,1),(dx_avg,dy_avg))

			heading_new,heading_floats,x1,y1 = get_best_heading(rp.X_PARAM*x_avg,rp.Y_PARAM*y_avg,heading,rp.radius)
			
			heading_delta = (heading_new - heading)

			pose_str = d2n("(",dp(x_avg),',',dp(y_avg),',',dp(dx_avg),',',dp(dy_avg),")")

			heading_floats_str = "["
			for h in heading_floats:
				heading_floats_str += d2n('[',rp.radius*h[0]+x_avg,',',rp.radius*h[1]+y_avg,'],')
			heading_floats_str += ']'

			xy_str = "["
			for xy in zip(x1,y1):
				xy_str += d2n('[',xy[0],',',xy[1],'],')
			xy_str += ']'

			ssh_command_str = d2n("echo 'pose = ",pose_str,"\nxy = ",xy_str,"\nheading_floats = ",heading_floats_str,"' > ~/Desktop/",rp.computer_name,".car.txt ")
			#print ssh_command_str
			try:
				ssh.exec_command(ssh_command_str)
			except:
				#print('ssh.exec_command failed')
				pass

			"""
			if rp.STEER_FROM_XY:
				steer = get_steer(X,x_avg, Y,y_avg, DX,dx_avg, DY,dy_avg)

			steer += rp.HEADING_DELTA_PARAM * heading_delta
			"""
			steer = heading_delta*(-99.0/45)

			steer =int((steer-49.0)*rp.robot_steer_gain+49.0)
			steer = min(99,steer)
			steer = max(0,steer)
			steer = int((1.0-rp.steer_momentum)*steer+rp.steer_momentum*steer_prev)
			steer_prev = steer
			#print dp(x_avg,1), dp(y_avg,1)
			#print steer
			#print int(heading_new),int(heading),int(heading_delta),int(steer)

			robot_steer = steer

			if True:
				aruco_position_x_pub.publish(std_msgs.msg.Float32(x_avg))
				aruco_position_y_pub.publish(std_msgs.msg.Float32(y_avg))
				aruco_heading_x_pub.publish(std_msgs.msg.Float32(dx_avg))
				aruco_heading_y_pub.publish(std_msgs.msg.Float32(dy_avg))

			aruco_freq.freq()
			#print robot_steer,dp(x_avg,1),dp(y_avg,1)
			error_ctr_ = 0

		except Exception as e:
			pass
			"""
			print("********** Exception ***********************")
			print(e.message, e.args)
			error_ctr_ += 1
			#print(d2s("aruco_thread error #",error_ctr_," (may be transient)"))
			"""
#
threading.Thread(target=aruco_thread).start()
#
###################################################################


frozen_ = 0
defrosted_timer = Timer(0)
while not rospy.is_shutdown():

	#clf();plt_square();xysqlim(2*107.0/100.0);plot(x_avg,y_avg,'ro');spause()

	if reload_timer.check(): # put in thread?
		reload(rp)
		reload_timer.reset()


	if state in [3,5,6,7]:
		potential_collision_ = potential_collision_from_callback_
		if potential_collision_ == 2:
			network_enter_timer.reset()

		if (previous_state not in [3,5,6,7]):
			previous_state = state
			network_enter_timer.reset()
			defrosted_timer.reset()
			frozen_ = 0
			
		if not network_enter_timer.check() or potential_collision_ == 2:
			defrosted_timer.reset()
			frozen_ = 0
			print "waiting before entering network mode..."
			steer_cmd_pub.publish(std_msgs.msg.Int32(49))
			motor_cmd_pub.publish(std_msgs.msg.Int32(49))
			time.sleep(0.1)
			continue
		else:
			if len(left_list) > nframes + 2:
				if False:
					camera_data = format_camera_data(left_list, right_list)
					metadata = format_metadata((rp.Racing, 0, rp.Follow, rp.Direct, rp.Play, rp.Furtive))
					torch_motor, torch_steer = run_model(camera_data, metadata)

				#print dp(defrosted_timer.time())
				if ((defrosted_timer.time()<2 and potential_collision_ < 2) or potential_collision_ == 0) and not frozen_:
				#if potential_collision_ == 0 and not frozen_:

					frozen_cmd_pub.publish(std_msgs.msg.Int32(frozen_))
					
					if state in [3,6]:
						steer_cmd_pub.publish(std_msgs.msg.Int32(robot_steer))
						if False:
							if rp.robot_steer < 0:   
								steer_cmd_pub.publish(std_msgs.msg.Int32(torch_steer))
							else:
								steer_cmd_pub.publish(std_msgs.msg.Int32(rp.robot_steer))
					if state in [6,7]:
						motor_cmd_pub.publish(std_msgs.msg.Int32(rp.robot_motor))
						if False:
							if rp.robot_motor < 0:
								motor_cmd_pub.publish(std_msgs.msg.Int32(torch_motor))
							else:
								motor_cmd_pub.publish(std_msgs.msg.Int32(rp.robot_motor))

				elif potential_collision_:

					#if not frozen_:
					#	if not network_ignore_potential_collision.check():
					#		continue
					if not frozen_:
						print('I_ROBOT',rp.who_is_in_charge,rp.robot_steer,rp.robot_motor)
					frozen_ = 1			

					frozen_cmd_pub.publish(std_msgs.msg.Int32(frozen_))

					if state in [3,6]:          
						steer_cmd_pub.publish(std_msgs.msg.Int32(49))
					if state in [6,7]:
						motor_cmd_pub.publish(std_msgs.msg.Int32(49))					


	else:
		network_enter_timer.reset()
	

	shutdown_time = 30
	if state == 4 and state_enter_timer.time() > shutdown_time-5:
		print('!!! about to reboot from state 4 !!! ' + str(steer))
	if state == 4 and state_enter_timer.time() > shutdown_time:
		print(d2s("Rebooting because in state 4 for",shutdown_time,"+ s"))
		unix('sudo reboot')


	if time_step.check():
		
		#print(torch_steer,torch_motor)
		print(d2s("In state",state,"for",dp(state_enter_timer.time()),"seconds, previous_state =",previous_state,'frozen_ =',frozen_))
		time_step.reset()

stop_ros()
