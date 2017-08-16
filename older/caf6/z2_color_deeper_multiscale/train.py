import caffe
from kzpy3.utils import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files3 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt


########################################################
#          SETUP SECTION
#
solver_file_path = opjh("kzpy3/caf6/z2_color_deeper_multiscale/solver.prototxt")
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
