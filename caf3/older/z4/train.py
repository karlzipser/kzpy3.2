#! /usr/bin/python
#//anaconda/bin/python

import caffe
from kzpy3.utils import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files4 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt

USE_GPU = False

########################################################
#          SETUP SECTION
#
solver_file_path = opjh("kzpy3/caf3/z4/solver.prototxt")
weights_file_path1 = None
if weights_file_path1 == "None":
	weights_file_path1 = None
#
########################################################

def setup_solver(solver_file_path):
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		if 'split' not in l[0]:
			print(l)
	#for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
	#	print(l)
	return solver


img = zeros((94,168,3))#,'uint8')


unix('mkdir -p '+opjD('z4'))


solver = setup_solver(solver_file_path)
