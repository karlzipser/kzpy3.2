#! /usr/bin/python 
#//anaconda/bin/python

import caffe
from kzpy3.utils import *
os.chdir(home_path) # this is for the sake of the train_val.prototxt


########################################################
#          SETUP SECTION
#
#from kzpy3.teg1.get_bag_data import get_data
#from kzpy3.teg1.get_live_data import get_data
def get_data():
	data_dic = {}
	data_dic['img'] = np.zeros((10,10))
	return data_dic

solver_file_path = opjh("kzpy3/caf3/z1/solver.prototxt")
weights_file_path = opjD('z1/z1_iter_3000.caffemodel') #None #
#
########################################################




def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver


def load_data_into_model(data_dic):
	pass


if __name__ == '__main__':
	#caffe.set_device(0)
	#caffe.set_mode_gpu()
	solver = setup_solver()
	if weights_file_path != None:
		print "loading " + weights_file_path
		solver.net.copy_from(weights_file_path)
	for i in range(10000):
		load_data_into_model(get_data())
		solver.step(1)


