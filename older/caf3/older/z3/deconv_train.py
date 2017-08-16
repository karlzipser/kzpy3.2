#! /usr/bin/python
#//anaconda/bin/python

import caffe
from kzpy3.utils import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files4 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt

USE_GPU = False


def setup_solver(solver_file_path):
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver



if USE_GPU:
	caffe.set_device(0)
	caffe.set_mode_gpu()






bair_car_data = Bair_Car_Data(opjD('bair_car_data_min'),1000,100)

solver = setup_solver(opjh('kzpy3/caf3/z3/deconv_solver.prototxt'))
ctr = 0
loss = []
img = zeros((94,168,3))

while True:
	data = bair_car_data.get_data(['steer','motor'],3,3)

	solver.net.blobs['image_data_past'].data[0,0,:,:] 	= data['left'][0][:,:]/255.0
	solver.net.blobs['image_data'].data[0,0,:,:] 		= data['left'][1][:,:]/255.0
	solver.net.blobs['image_data_future'].data[0,0,:,:] = data['left'][2][:,:]/255.0

	plt.ion()

	solver.step(1)
	ctr += 1

	print ctr
	print solver.net.blobs['deconv1_NIN'].data[0,0,:,:].max() - solver.net.blobs['deconv1_NIN'].data[0,0,:,:].min()

	mi(solver.net.blobs['deconv1_NIN'].data[0,0,:,:])
	plt.pause(0.001)
#cv2.imshow('left',img.astype('uint8'))
#if cv2.waitKey(1) & 0xFF == ord('q'):
#    pass
