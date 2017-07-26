#! /usr/bin/python
#//anaconda/bin/python

import caffe
from kzpy3.utils import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files2 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt


########################################################
#          SETUP SECTION
#
solver_file_path = opjh("kzpy3/caf3/z1/solver.prototxt")
weights_file_path = opjD('z1/z1_iter_510000.caffemodel') #
#
########################################################




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



