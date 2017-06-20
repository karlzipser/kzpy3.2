#! /usr/bin/python
#//anaconda/bin/python
#
import caffe
caffe.set_device(0)
caffe.set_mode_gpu()
from kzpy3.utils import *
from kzpy3.teg2.data.access.get_data_from_bag_files9 import *
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
			target_data = list(data['steer'])
			target_data += list(data['motor'])
			target_data[0] = data['steer'][0]
			target_data[10] = data['motor'][0]

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
				for i in range(len(target_data)/2):
					t = target_data[i]
					t = t - 49
					t = -t
					t = t + 49
					target_data[i] = t

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


			for i in range(len(target_data)):
				solver.net.blobs['steer_motor_target_data'].data[0,i] = target_data[i]/99.

		else:
			print """not if type(data['left']) == np.ndarray: """+str(time.time())
	else:
		pass #print """not if 'left' in data: """+str(time.time())
		return 'no data'
	if show:
		show_solver_data(solver,data,flip,49.,1.)
	return True


def show_solver_data(solver,data,flip,steer_offset,steer_mult):
	caffe_steer_color_color = [1.,0,0]
	human_steer_color_color = [0,0,1.]

	data_img_shape = np.shape(solver.net.blobs['ZED_data_pool2'].data)
	num_frames = (data_img_shape[1])/2
	print num_frames		
	img = np.zeros((data_img_shape[2],data_img_shape[3],3))+0.5
	img[0,0,:]=1
	img[0,1,:]=0
	mi(img)
	plt.pause(0.5)
	for i in range(num_frames):
		#print i
		#if i > 0:
		#    img_prev = img.copy()

		if not flip:
			d = data['left'][i][:,:]/255.0-.5
		else:
			d = scipy.fliplr(data['left'][i][:,:]/255.0-.5)
		d = z2o(d)
		if i < 2:
			img[:,:,0] = z2o(solver.net.blobs['ZED_data_pool2'].data[0,i,:,:])
		else:
			img[:,:,0] = d #z2o(solver.net.blobs['ZED_data_pool2'].data[0,i+2,:,:])
		img[:,:,1] = img[:,:,0].copy()
		img[:,:,2] = img[:,:,0].copy()

		if solver.net.blobs['metadata'].data[0,1,0,0] == 1.0: #caffe is steering
		    steer_rect_color = caffe_steer_color_color
		else:
			steer_rect_color = human_steer_color_color

		steer = 99*solver.net.blobs['steer_motor_target_data'].data[0,0] * steer_mult + steer_offset
		apply_rect_to_img(img,steer,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=True)

		mi(img,img_title=d2s(flip,i))#,img_title=(d2s('dt = ', int(1000*dt),'ms')))
		#print solver.net.blobs['steer_motor_target_data'].data
		plt.pause(0.25)




good_start_timestamp_indicies_test_results = {}

def main(good_start_timestamp_indicies_test_results):
	weights_file_path = most_recent_file_in_folder(opjD('z2'),['z2','caffemodel']) 
	if weights_file_path == "None":
		weights_file_path = None
	if weights_file_path != None:
		print "loading " + weights_file_path
		solver.net.copy_from(weights_file_path)

	path = opjD('bair_car_data_min')
	bag_folder_paths = sorted(glob.glob(opj(path,'*')))

	ctr = 0
	for bf in bag_folder_paths:
		if bf in good_start_timestamp_indicies_test_results.keys():
			continue
		good_start_timestamp_indicies_test_results[bf] = {}
		good_start_timestamp_indicies_test_results[bf]['loss'] = []
		good_start_timestamp_indicies_test_results[bf]['steer'] = []
		cprint(bf,'red','on_green')
		if False: #bf in bair_car_data.bag_folders_dic:
			#BF = bair_car_data.bag_folders_dic[bf]
			pass
		else:
			BF = load_obj(opjD('train_preprocessed_bag_folder_path',bf.split('/')[-1]+'.pkl'))
		for indx in range(len(BF.data['good_start_timestamps'])):
			#print indx
			try:
				data = BF.get_data(num_image_steps=2,good_start_index=indx)
				result = load_data_into_model(solver, data, flip=False)
				solver.net.forward()
				a = solver.net.blobs['steer_motor_target_data'].data[0,:10] - solver.net.blobs['ip2'].data[0,:10] # only do loss on steering
				loss = np.sqrt(a * a).mean()
			except:
				loss = -1 # an error code
			good_start_timestamp_indicies_test_results[bf]['loss'].append(loss)
			good_start_timestamp_indicies_test_results[bf]['steer'].append(int(100*solver.net.blobs['ip2'].data[0,9]))
			if np.mod(ctr,5000) == 0:
				print loss
				#plt.figure(1)
				#plt.clf()
				#plt.plot(good_start_timestamp_indicies_test_results[bf])
				#plt.title(bf)
			ctr += 1


if True:
	solver_file_path = opjh("kzpy3/caf3/z2_test/solver.prototxt")
	solver = setup_solver()
	main(good_start_timestamp_indicies_test_results)

