"""
TO RUN:
First, need to do this in two separate terminal windows:
$ roscore
$ rosbag play /home/YOU/BAG_FOLDER/*.bag
e.g.,
$ rosbag play /home/karlzipser/Desktop/bair_car_data_min_disks/bair_car_data_6_min/direct_local_sidewalk_test_data_01Nov16_14h59m31s_Mr_Orange/*.bag

Then, 
$ python kzpy3/caf3/z2_ttest/caf_ros_drydock.py

########################################################




"""

########################################################
#						Caffe
import caffe
caffe.set_device(0)
caffe.set_mode_gpu()
from kzpy3.vis import *
#from kzpy3.teg2.data.access.get_data_from_bag_files9 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt
import os, serial, threading, Queue
import threading

img = zeros((94,168,3))
DO_LOADING = False
QUIT = False

def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver

def load_data_into_model(solver,data,flip,show=False):
	global img
	if data == 'END' :
		print """data = 'END':"""
		return False
	if 'left' in data:
		if type(data['left'][0]) == np.ndarray:


			if not flip:
				solver.net.blobs['ZED_data_pool2'].data[0,0,:,:] = data['left'][0][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,1,:,:] = data['left'][1][:,:]/255.0-.5
				#solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = data['left'][2][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = data['right'][0][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,3,:,:] = data['right'][1][:,:]/255.0-.5
				#solver.net.blobs['ZED_data_pool2'].data[0,5,:,:] = data['right'][2][:,:]/255.0-.5

			else: # flip left-right
				solver.net.blobs['ZED_data_pool2'].data[0,0,:,:] = scipy.fliplr(data['left'][0][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,1,:,:] = scipy.fliplr(data['left'][1][:,:]/255.0-.5)
				#solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = scipy.fliplr(data['left'][2][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = scipy.fliplr(data['right'][0][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,3,:,:] = scipy.fliplr(data['right'][1][:,:]/255.0-.5)
				#solver.net.blobs['ZED_data_pool2'].data[0,5,:,:] = scipy.fliplr(data['right'][2][:,:]/255.0-.5)

			Direct = 0.
			Follow = 0.
			Play = 0.
			Furtive = 0.
			Caf = 0

			#print data['bag_filename']

			if 'follow' in data['path']:
				Follow = 1.0
			if 'direct' in data['path']:
				Direct = 1.0
			if 'play' in data['path']:
				Play = 1.0
			if 'furtive' in data['path']:
				Furtive = 1.0
			if 'caffe' in data['path']:
				Caf = 1.0

			solver.net.blobs['metadata'].data[0,0,:,:] = 0
			solver.net.blobs['metadata'].data[0,1,:,:] = Caf
			solver.net.blobs['metadata'].data[0,2,:,:] = Follow
			solver.net.blobs['metadata'].data[0,3,:,:] = Direct
			solver.net.blobs['metadata'].data[0,4,:,:] = Play
			solver.net.blobs['metadata'].data[0,5,:,:] = Furtive
			#solver.net.blobs['metadata'].data[0,6,:,:] = target_data[0] #current steer
			#solver.net.blobs['metadata'].data[0,7,:,:] = target_data[len(target_data)/2] #current motor
			#solver.net.blobs['metadata'].data[0,8,:,:] = 0
			#solver.net.blobs['metadata'].data[0,9,:,:] = 0

		else:
			print """not if type(data['left']) == np.ndarray: """+str(time.time())
	else:
		pass #print """not if 'left' in data: """+str(time.time())
		return 'no data'
	if show:
		show_solver_data(solver,data,flip,49.,1.)
	return True






########################################################
#          				ROSPY
import roslib
import std_msgs.msg
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge,CvBridgeError
bridge = CvBridge()
rospy.init_node('listener',anonymous=True)
left_list = []
right_list = []
state = 0
def state_callback(data):
	global state
	state = data.data
def right_callback(data):
	global left_list, right_list, solver
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(right_list) > 5:
		right_list = right_list[-5:]
	right_list.append(cimg)
def left_callback(data):
	global left_list, right_list
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(left_list) > 5:
		left_list = left_list[-5:]
	left_list.append(cimg)
rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)
rospy.Subscriber('/bair_car/state',std_msgs.msg.Int32,state_callback)



weights_file_path = most_recent_file_in_folder(opjD('z2'),['z2','caffemodel']) 
solver_file_path = opjh("kzpy3/caf3/z2/solver.prototxt")
solver = setup_solver()
solver.net.copy_from(weights_file_path)


while not rospy.is_shutdown():
	
	if len(left_list) > 4:
		l0 = left_list[-2]
		l1 = left_list[-1]
		r0 = right_list[-2]
		r1 = right_list[-1]

		data = {}
		data['left'] = []
		data['right'] = []
		data['left'].append(imresize(l0[:,:,1],0.25)) # on TX1, this is done in model (see tran_val_live.prototxt)
		data['left'].append(imresize(l1[:,:,1],0.25))
		data['right'].append(imresize(r0[:,:,1],0.25))
		data['right'].append(imresize(r1[:,:,1],0.25))
		data['path'] = "/...direct.../"  # can use 'furtive','play','follow'
				
		load_data_into_model(solver, data, flip=False)
		solver.net.forward()
		model_steer = 100*solver.net.blobs['ip2'].data[0,9]
		model_motor = 100*solver.net.blobs['ip2'].data[0,19]

		img = l1
		steer_rect_color = [0,0,255] # red in BGR
		apply_rect_to_img(img,model_steer,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=True)
		apply_rect_to_img(img,model_motor,49,99,steer_rect_color,steer_rect_color,0.8,0.05,center=False,reverse=True,horizontal=False)

		cv2.imshow("Left",img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break



