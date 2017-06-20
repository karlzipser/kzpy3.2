'''
20 Sept. 2015
Do this:
from kzpy3.caf.training.y2015.m9.from_mnist.original_with_accuracy.train import *

This module allows for training and deploy-testing of mnist network.

Next steps:
1) change to work with RGB images of look_at_numbers, using python layer for data layer.
'''

from kzpy3.vis import *
import caffe

os.chdir(home_path) # this is for the sake of the train_val.prototxt

global solver
global net

def setup_solver():
	global solver
	solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2015/m9/from_mnist/original_with_accuracy/solver.prototxt"))
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)

def train():
	solver.step(5000)


def look_at_numbers():
	solver.step(1)
	mi(solver.net.blobs['data'].data[:8, 0].transpose(1, 0, 2).reshape(28, 8*28),'train')
	print solver.net.blobs['label'].data[:8]
	mi(solver.test_nets[0].blobs['data'].data[:8, 0].transpose(1, 0, 2).reshape(28, 8*28), 'test')
	print solver.test_nets[0].blobs['label'].data[:8]


def restore():
	solver.restore(opjh('scratch/2015/11/23/caffe/models/from_mnist/original_with_accuracy/model_iter_1000.solverstate'))


def deploy(img_name = opjh('caffe/examples/images/7.jpg')):
	global net
	net = caffe.Net(opjh('kzpy3/caf/training/y2015/m9/from_mnist/original_with_accuracy/deploy.prototxt'),opjh('scratch/2015/9/20/caffe/models/from_mnist/original_with_accuracy/model_iter_5000.caffemodel'),caffe.TEST)
	net.blobs['data'].reshape(1,1,28,28)
	img = scipy.misc.imread(img_name)
	img = img[:,:,0] # this network wants grayscale images, no color channel.
	net.blobs['data'].data[...] = img
	out = net.forward()
	print("Predicted class is #{}.".format(out['prob'].argmax()))
	mi(img,img_name)


