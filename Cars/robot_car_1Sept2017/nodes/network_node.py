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
network_ignore_potential_collision = Timer(2) # starting driving triggers the collision IMU detector
folder_display_timer = Timer(30)
git_pull_timer = Timer(60)
reload_timer = Timer(30)
torch_steer_previous = 49
torch_motor_previous = 49


def state__callback(data):
	global state, previous_state, state_enter_timer
	if state != data.data:
		state_enter_timer = Timer(0)
		if state in [3,5,7]:
			srpd2s('if state in [3,5,7]:')
			#unix('ssd')
			#stop_ros()

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
import paramiko
#
##################



Other_car_coordinates = {}
for k in rp.Car_IP_dic:
	if k != rp.computer_name:
		Other_car_coordinates[k] = {}

one_over_sixty = 1.0/60.0
one_over_fifteen = 1.0#/15.0

#TIME = 'TIME'
#POSE = 'POSE'

def get_other_car_coordinates_thread():
	while True:
		if state in [3,5,6,7]:
			try:
				#print 'get_other_car_coordinates_thread'
				timer = Timer(0)
				for car in sgg(opjD('*.car.txt')):
					#car_ctime = os.path.getctime(car)
					if True:#time.time() - car_ctime < 2.0:
						car_name = fname(car).split('.')[0]
						new_car = car.replace('.car','')
						unix('cp '+car+' '+new_car,False)
						l = txt_file_to_list_of_strings(new_car)
						for ll in l:
							exec(ll)
						if len(pose) == 4:
							Other_car_coordinates[car_name][POSE] = pose
							Other_car_coordinates[car_name][TIME] = time.time()
						#spd2s(Other_car_coordinates)
				t = timer.time()
				if t < one_over_fifteen:
					time.sleep(one_over_fifteen - t)
			except Exception as e:
				print("********** def get_other_car_coordinates_thread(): Exception ***********************")
				print(e.message, e.args)
		else:
			time.sleep(0.1)
threading.Thread(target=get_other_car_coordinates_thread).start()




###################################################################
# aruco markers
aruco_heading_x_pub = rospy.Publisher('/bair_car/aruco_heading_x', std_msgs.msg.Float32, queue_size=10)
aruco_heading_y_pub = rospy.Publisher('/bair_car/aruco_heading_y', std_msgs.msg.Float32, queue_size=10)
aruco_position_x_pub = rospy.Publisher('/bair_car/aruco_position_x', std_msgs.msg.Float32, queue_size=10)
aruco_position_y_pub = rospy.Publisher('/bair_car/aruco_position_y', std_msgs.msg.Float32, queue_size=10)
#other_car_position_pub = rospy.Publisher('/bair_car/other_car_position', geometry_msgs.msg.Vector3, queue_size=10)
#

#
#heading_steering_coordinates = lo(opjD('heading_steering_coordinates'))
wall_length = 4*107.0/100.0
#

#
#
################################################################################3
#

wall_length = 4*107.0/100.0
half_wall_length = wall_length/2.0
hw = half_wall_length

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
def check_for_other_car(x_avg,y_avg,dx_avg,dy_avg):
	for k in Other_car_coordinates:
		try:
			if TIME in Other_car_coordinates[k]:
				if time.time() - Other_car_coordinates[k][TIME] < 1.0:
					ox = Other_car_coordinates[k][POSE][0]
					oy = Other_car_coordinates[k][POSE][1]
					#other_car_position_pub.publish(geometry_msgs.msg.Vector3(ox,oy,rp.Car_num_dic[k]))
					#print k,Other_car_coordinates[k]
					#return False
					ac = angle_clockwise((dx_avg,dy_avg),(ox-x_avg,oy-y_avg))
					#print ac
					if np.abs(ac) < rp.car_detect_angle or np.abs(ac) > (360-rp.car_detect_angle):
						di = np.sqrt((x_avg-ox)**2+(y_avg-oy)**2)
						#print di
						if di < rp.other_car_distance_threshold:
							#car_print(d2s(k,' distance =',dp(di)),name=k)
							return k
		except Exception as e:
			print("***** def check_for_other_car(x_avg,y_avg,dx_avg,dy_avg): ***** Exception ***********************")
			print(e.message, e.args)
	return False


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

Ssh = {}
Connected_car_names = {}
for k in rp.Car_IP_dic:
	if k != rp.computer_name:
		Connected_car_names[k] = False
		Ssh[k] = paramiko.SSHClient()
		Ssh[k].set_missing_host_key_policy(paramiko.AutoAddPolicy())

def paramiko_connection_thread():
	timer = Timer(0)
	while timer.time() < 120:
		for k in rp.Car_IP_dic:
			if k != rp.computer_name:
				if Connected_car_names[k] == False:
					try:
						#print 'paramiko_connection_thread: '+k
						#if error_timer.check():
						#	print Connected_car_names
						Ssh[k].connect(rp.Car_IP_dic[k], username='nvidia')
						Connected_car_names[k] = True
						spd2s('ssh connection to',k,'established')
					except:
						pd2s('ssh connection to',k,'failed')
						pass
		time.sleep(5)
threading.Thread(target=paramiko_connection_thread).start()

ssh_command_str = ''


def paramiko_command_thread():
	timer = Timer(0)
	while True:
		if state in [3,5,6,7]:
			timer.reset()
			for k in rp.Car_IP_dic:
				
				if k != rp.computer_name:
					if Connected_car_names[k]:
						#print 'paramiko_command_thread +'+k
						try:
							Ssh[k].exec_command(ssh_command_str)
							#spd2s('ssh.exec_command  to',k)
						except:
							if error_timer.check():
								srpd2s('ssh.exec_command failed to',k)
								error_timer.reset()
			t = timer.time()
			if t < one_over_sixty:
				time.sleep(one_over_sixty - t)
		else:
			time.sleep(0.1)
threading.Thread(target=paramiko_command_thread).start()
#
###################################################################

car_print_timer = Timer(0.5)
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
		if state in [6]:
			try:
				if aruco_error_timer.check():
					heading_pause = 1
					if False:#aruco_error_print_timer.check():
						srpd2s('aruco_error_timer.check()',aruco_error_timer.time())
						aruco_error_print_timer.reset()
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
				
				#print(heading_new,heading_floats,x1,y1,heading_pause)
				car_in_range = 0
				car_question_mark = check_for_other_car(x_avg,y_avg,dx_avg,dy_avg)
				if car_question_mark != False:
					car_print('!!!!!!!!!!!!!!!!!!!!!!!!!\n!',rp.computer_name)
					car_print(d2s('\t',car_question_mark,' is too close!!!!'),car_question_mark)
					car_print('!\n!!!!!!!!!!!!!!!!!!!!!!!!!',rp.computer_name)
					car_print_timer.reset()
					heading_pause = 1
					car_in_range = 1


				heading_delta = (heading_new - heading)

				pose_str = d2n("(",dp(x_avg),',',dp(y_avg),',',dp(dx_avg),',',dp(dy_avg),")")

				heading_floats_str = "["
				for h in heading_floats:
					heading_floats_str += d2n('[',dp(rp.radius*h[0]+x_avg),',',dp(rp.radius*h[1]+y_avg),'],')
				heading_floats_str += ']'

				xy_str = "["
				for xy in zip(x1,y1):
					xy_str += d2n('[',xy[0],',',xy[1],'],')
				xy_str += ']'

				temp = d2n("echo 'pose = ",pose_str,"\nxy = ",xy_str,"\nheading_floats = ",heading_floats_str,"' > ~/Desktop/",rp.computer_name,".car.txt ")
				ssh_command_str = temp


				
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
					car_in_range_pub.publish(std_msgs.msg.Int32(car_in_range))
					
					if heading_pause:
						if not car_in_range:
							message_timer.message('heading_pause')
						else:
							message_timer.message('car in range')

				aruco_freq.freq()
				error_ctr_ = 0
				aruco_error_timer.reset()

			except Exception as e:
				aruco_position_x_pub.publish(std_msgs.msg.Float32(x_avg_prev))
				aruco_position_y_pub.publish(std_msgs.msg.Float32(y_avg_prev))
				aruco_heading_x_pub.publish(std_msgs.msg.Float32(dx_avg_prev))
				aruco_heading_y_pub.publish(std_msgs.msg.Float32(dy_avg_prev))
				heading_pause_pub.publish(std_msgs.msg.Int32(heading_pause))
				car_in_range_pub.publish(std_msgs.msg.Int32(car_in_range))
				if False: #aruco_thread_exception_print_timer.check():
					print("********** def aruco_thread(): Exception ***********************")
					print(e.message, e.args)
					error_ctr_ += 1
					print(d2s("aruco_thread error #",error_ctr_," (may be transient)"))
					aruco_thread_exception_print_timer.reset()
		else:
			time.sleep(0.1)
#
threading.Thread(target=aruco_thread).start()
#
###################################################################

def car_print(stri,name=rp.computer_name):
	cprint(stri,rp.Car_termcolor_dic[name][0],rp.Car_termcolor_dic[name][1])

frozen_ = 0
defrosted_timer = Timer(0)
state_messenger = Timer(1)
while not rospy.is_shutdown():

	if reload_timer.check(): # put in thread?
		reload(rp)
		reload_timer.reset()


	if state in [6]:#[3,5,6,7]:
		if frozen_:
			message_timer.message('frozen_')

		potential_collision_ = potential_collision_from_callback_
		if False: # why is the below there?
			if potential_collision_ == rp.potential_motor_freeze_collision:
				network_enter_timer.reset()
		

		if (previous_state not in [3,5,6,7]):
			previous_state = state
			network_enter_timer.reset()
			defrosted_timer.reset()
			frozen_ = 0
			
		if not network_enter_timer.check() or potential_collision_ == rp.acc_y_tilt_event:
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

				if ((defrosted_timer.time()<2 and potential_collision_ < rp.potential_motor_freeze_collision) or potential_collision_ == 0) and not (heading_pause or frozen_):

					frozen_cmd_pub.publish(std_msgs.msg.Int32(frozen_))
					
					if state in [6]:# [3,6]:
						steer_cmd_pub.publish(std_msgs.msg.Int32(robot_steer))
						if False:
							if rp.robot_steer < 0:   
								steer_cmd_pub.publish(std_msgs.msg.Int32(torch_steer))
							else:
								steer_cmd_pub.publish(std_msgs.msg.Int32(rp.robot_steer))
					if state in [6]: #[6,7]:
						motor_cmd_pub.publish(std_msgs.msg.Int32(rp.robot_motor))
						if False:
							if rp.robot_motor < 0:
								motor_cmd_pub.publish(std_msgs.msg.Int32(torch_motor))
							else:
								motor_cmd_pub.publish(std_msgs.msg.Int32(rp.robot_motor))

				elif potential_collision_:

					if not frozen_:
						srpd2s('I_ROBOT',rp.who_is_in_charge,rp.robot_steer,rp.robot_motor)
					frozen_ = 1			

					frozen_cmd_pub.publish(std_msgs.msg.Int32(frozen_))

					if state in [3,6]:          
						steer_cmd_pub.publish(std_msgs.msg.Int32(49))
					if state in [6,7]:
						motor_cmd_pub.publish(std_msgs.msg.Int32(49))					

				elif heading_pause:
					if error_timer.check():
						srpd2s('heading_pause')
						error_timer.reset()
						
					if state in [3,6]:          
						steer_cmd_pub.publish(std_msgs.msg.Int32(49))
					if state in [6,7]:
						motor_cmd_pub.publish(std_msgs.msg.Int32(49))	
	else:
		if state in [3,5,7]:
			steer_cmd_pub.publish(std_msgs.msg.Int32(49))
			motor_cmd_pub.publish(std_msgs.msg.Int32(49))
			state_messenger('state in [3,5,7] so outputs set to 49','red')
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


