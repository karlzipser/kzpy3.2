#! /usr/bin/python
#//anaconda/bin/python

import caffe
from kzpy3.utils import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files3 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt


########################################################
#          SETUP SECTION
#
solver_file_path = opjh("kzpy3/caf5/z2_color_multiscale/solver.prototxt")
weights_file_path = None #opjD('z2/z2.caffemodel') #
#
########################################################




def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)

	print("")
	
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)

	print("")
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		if 'split' not in l[0]:
			print(l)

	return solver

solver = setup_solver()


"""

('steer_motor_target_data', (1, 20))
('metadata', (1, 6, 14, 26))
('ZED_data', (1, 4, 376, 672))
('ZED_data_ZED_data_0_split_0', (1, 4, 376, 672))
('ZED_data_ZED_data_0_split_1', (1, 4, 376, 672))
('ZED_data_pool1', (1, 4, 188, 336))
('ZED_data_pool1_ZED_data_pool1_0_split_0', (1, 4, 188, 336))
('ZED_data_pool1_ZED_data_pool1_0_split_1', (1, 4, 188, 336))
('ZED_data_pool1_ZED_data_pool1_0_split_2', (1, 4, 188, 336))
('ZED_data_pool2', (1, 4, 94, 168))

('conv1a', 		(1, 96, 122, 221))
('conv1a_pool', (1, 96, 61, 110))
('conv1b1', 	(1, 96, 61, 110))

('conv1b', (1, 96, 60, 109))



('conv1c', (1, 96, 28, 53))



('conv1a_pool1', (1, 96, 62, 111))

('conv1b_pool', (1, 96, 30, 54))

('conv1c_pool', (1, 96, 14, 26))

('conv1a', (96, 4, 11, 11))
('conv1b', (96, 4, 11, 11))
('conv1b1', (96, 4, 11, 11))
('conv1c', (96, 4, 11, 11))

"""
