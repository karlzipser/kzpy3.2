#!/usr/bin/env python
"""
reed to run roslaunch first, e.g.,

roslaunch bair_car bair_car.launch use_zed:=true record:=false
"""

from kzpy3.utils2 import *
import torch
import torch.nn as nn
from torch.autograd import Variable
from nets.squeezenet import SqueezeNet
import runtime_parameters as rp








reload_timer = Timer(30)

last_time = 0

verbose = False

nframes = 2 # default superseded by net



def static_vars(**kwargs):
	def decorate(func):
		for k in kwargs:
			setattr(func, k, kwargs[k])
		return func
	return decorate


def init_model():
	global solver, scale, nframes
	# Load PyTorch model
	save_data = torch.load(rp.weight_file_path)
	print("Loaded "+rp.weight_file_path)
	# Initializes Solver
	solver = SqueezeNet().cuda()
	solver.load_state_dict(save_data['net'])
	solver.eval()
	nframes = solver.N_FRAMES
	# Create scaling layer
	scale = nn.AvgPool2d(kernel_size=3, stride=2, padding=1).cuda()

init_model()






def nonlinear_motor(m):
	bb = m * 7.0
	bb = max(0,10.0*np.log(bb+10))
	return bb

"""
def nonlinear_motor(m):
	bb = m * 7.0
	bb = max(0,25.0*np.log(bb+100))
	return bb
"""





@static_vars(torch_motor_previous=49, torch_steer_previous=49)
def run_model(input, metadata):
	"""
	Runs neural net to get motor and steer data. Scales output to 0 to 100 and applies an IIR filter to smooth the
	performance.

	:param input: Formatted input data from ZED depth camera
	:param metadata: Formatted metadata from user input
	:return: Motor and Steering values
	"""
	
	output = solver(input, Variable(metadata))  # Run the neural net

	if verbose:
		print(output)

	# Get latest prediction
	#torch_motor = 100 * output[0][19].data[0]
	#torch_steer = 100 * output[0][9].data[0]
	torch_motor = 100 * output[0][11].data[0] ########################!!!!!!!!!!!!!!!!!!!!!
	#print d2s('torch_motor =',torch_motor)
	torch_steer = 100 * output[0][2].data[0] ########################!!!!!!!!!!!!!!!!!!!!!
	
	if True:
		torch_motor /= 7.0
		torch_motor += 49
	
	#torch_motor = (torch_motor+nonlinear_motor(torch_motor))/2.0

	if verbose:
		print('Torch Prescale Motor: ' + str(torch_motor))
		print('Torch Prescale Steer: ' + str(torch_steer))
	
	# Scale Output
	torch_motor = int((torch_motor - 49.) * rp.motor_gain + 49.)
	torch_steer = int((torch_steer - 49.) * rp.steer_gain + 49.)

	# Bound the output
	torch_motor = max(0, torch_motor)
	torch_steer = max(0, torch_steer)
	torch_motor = min(99, torch_motor)
	torch_steer = min(99, torch_steer)

	# Apply an IIR Filter
	torch_motor = int((torch_motor + run_model.torch_motor_previous) / 2.0)
	run_model.torch_motor_previous = torch_motor
	torch_steer = int((torch_steer + run_model.torch_steer_previous) / 2.0)
	run_model.torch_steer_previous = torch_steer

	return torch_motor, torch_steer

def format_camera_data(left_list, right_list):
	"""
	Formats camera data from raw inputs from camera.

	:param l0: left camera data from time step 0
	:param l1: right camera data from time step 1
	:param r0: right camera dataa from time step 0
	:param r1: right camera data from time step 0
	:return: formatted camera data ready for input into pytorch z2color
	"""

	camera_start = time.clock()
	half_img_height = int(shape(left_list[-1])[0]/2)
	listoftensors = []
	for i in range(nframes):
		for side in (left_list, right_list):
			#print shape(side[-i - 1])
			side[-i - 1][:188,:,:] = 128  #*= 0 ####################!!!!!!!!!!!!!!!!!!!!!!!!!
			#side[-i - 1][:188,:,:] += 128
			listoftensors.append(torch.from_numpy(side[-i - 1]))
	camera_data = torch.cat(listoftensors, 2)

   # camera_data = torch.FloatTensor()
   # for c in range(3):
   #     for side in (left_list, right_list):
   #         for i in range(nframes): # [0,1,2,... nframes -1]
   #             camera_data = torch.cat((torch.from_numpy(side[-i - 1][:, :, c]).float().unsqueeze(2), camera_data), 2)

	
	camera_data = camera_data.cuda().float()/255. - 0.5
	camera_data = torch.transpose(camera_data, 0, 2)
	camera_data = torch.transpose(camera_data, 1, 2)
	camera_data = camera_data.unsqueeze(0)
	camera_data = scale(Variable(camera_data))
	camera_data = scale(camera_data)

	return camera_data


def format_metadata(raw_metadata):
	"""
	Formats meta data from raw inputs from camera.
	:return:
	"""
	metadata = torch.FloatTensor()
	for mode in raw_metadata:
		metadata = torch.cat((torch.FloatTensor(1, 23, 41).fill_(mode), metadata), 0)
	zero_matrix = torch.FloatTensor(1, 23, 41).zero_()
	for i in range(126):
		metadata = torch.cat((zero_matrix, metadata), 0) 
	return metadata.cuda().unsqueeze(0)

#
########################################################


########################################################
#          ROSPY SETUP SECTION
import thread
import time
import roslib
import std_msgs.msg
import geometry_msgs.msg
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
steer = 49
back_steer = 49
back_motor = 49
previous_state = 0
state_transition_time_s = 0
state_enter_time = 0

if 'Back' not in rp.computer_name:
	def state_callback(data):
		global state, previous_state, state_enter_time
		# data.data = 6
		if state != data.data:
			state_enter_time = time.time()
			if state in [3,5,6,7] and previous_state in [3,5,6,7]:
				pass
			else:
				previous_state = state
		state = data.data
	def steer_callback(data):
		global steer
		steer = data.data
	def back_steer_callback(data):
		global back_steer
		back_steer = data.data
	def back_motor_callback(data):
		global back_motor
		back_motor = data.data
def right_callback(data):
	global A,B, left_list, right_list, solver
	A += 1
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(right_list) > nframes + 3:
		right_list = right_list[-(nframes + 3):]
	right_list.append(cimg)
def left_callback(data):
	global A,B, left_list, right_list
	B += 1
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(left_list) > nframes + 3:
		left_list = left_list[-(nframes + 3):]
	left_list.append(cimg)
def state_transition_time_s_callback(data):
	global state_transition_time_s
	state_transition_time_s = data.data

#########################################################

rospy.Subscriber(d2n("/",rp.computer_name,"/zed/right/image_rect_color"),Image,right_callback,queue_size = 1)
rospy.Subscriber(d2n("/",rp.computer_name,"/zed/left/image_rect_color"),Image,left_callback,queue_size = 1)
if 'Back' not in rp.computer_name:
	rospy.Subscriber(d2n("/",rp.computer_name,"/steer"), std_msgs.msg.Int32,steer_callback)
	rospy.Subscriber(d2n("/",rp.computer_name,"/state"), std_msgs.msg.Int32,state_callback)
	rospy.Subscriber("/Mr_Back/cmd/back_steer", std_msgs.msg.Int32,back_steer_callback)
	rospy.Subscriber('/Mr_Back/cmd/back_motor', std_msgs.msg.Int32,back_motor_callback)
	steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=10)
	motor_cmd_pub = rospy.Publisher('cmd/motor', std_msgs.msg.Int32, queue_size=10)
else:
	steer_cmd_pub = rospy.Publisher('cmd/back_steer', std_msgs.msg.Int32, queue_size=10)
	motor_cmd_pub = rospy.Publisher('cmd/back_motor', std_msgs.msg.Int32, queue_size=10)


ctr = 0

time_step = Timer(2)
caffe_enter_timer = Timer(1)
folder_display_timer = Timer(30)
git_pull_timer = Timer(60)
reload_timer = Timer(10)
#torch_steer_previous = 49
#torch_motor_previous = 49


if 'Back' in rp.computer_name or not rp.use_MSE:
	state = 6
backward_timer = None
torch_motor = 49
torch_steer = 49
while not rospy.is_shutdown():
	
	if reload_timer.check(): # put in thread?
		reload(rp)
		reload_timer.reset()
	if state in [3,5,6,7]:
		if (previous_state not in [3,5,6,7]):
			previous_state = state
			caffe_enter_timer.reset()
		if not caffe_enter_timer.check():
			print "waiting before entering caffe mode..."
			steer_cmd_pub.publish(std_msgs.msg.Int32(49))
			motor_cmd_pub.publish(std_msgs.msg.Int32(49))
			time.sleep(0.1)
			continue
		else:
			if len(left_list) > nframes + 2:
				camera_data = format_camera_data(left_list, right_list)
				metadata = format_metadata((rp.Follow, rp.Direct))

				#torch_motor, torch_steer = run_model(camera_data, metadata)


				forward_motor, forward_steer = run_model(camera_data, metadata)

				if 'Back' not in rp.computer_name:
					if backward_timer == None:
						if forward_motor < rp.forward_threshold:
							backward_timer = Timer(rp.backward_timer_time)
						else:
							torch_motor = forward_motor
							torch_steer = forward_steer
					else:
						torch_motor = 99 - int((back_motor - 49.) * rp.back_motor_gain + 49.)
						#torch_motor = 99 - back_motor
						torch_steer = back_steer
						if backward_timer.check():
							backward_timer = None
				else:
					torch_motor = forward_motor
					torch_steer = forward_steer

				cur_time = time.time()
				last_time = cur_time

				if state in [3,6]:          
					steer_cmd_pub.publish(std_msgs.msg.Int32(torch_steer))
				if state in [6,7]:
					motor_cmd_pub.publish(std_msgs.msg.Int32(torch_motor))

				print((back_steer,torch_steer),(back_motor,torch_motor))
	else:
		caffe_enter_timer.reset()
	
	shutdown_time = 30
	if state == 4 and time.time()-state_enter_time > shutdown_time-5:
		print('!!! about to reboot from state 4 !!! ' + str(steer))
	if state == 4 and time.time()-state_enter_time > shutdown_time:
		print(d2s("Rebooting because in state 4 for",shutdown_time,"+ s"))
		unix('sudo reboot')
	if time_step.check():
		print(d2s("In state",state,"for",dp(time.time()-state_enter_time),"seconds, previous_state =",previous_state))
		time_step.reset()

stop_ros()
	