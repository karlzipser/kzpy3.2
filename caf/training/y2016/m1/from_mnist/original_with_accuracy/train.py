'''
20 Sept. 2015
Do this:
from kzpy3.caf.training.y2015.m9.from_mnist.original_with_accuracy.train import *

This module allows for training and deploy-testing of mnist network.

Next steps:
1) change to work with RGB images of look_at_numbers, using python layer for data layer.


26 Jan 2016
from kzpy3.caf.training.y2016.m1.from_mnist.original_with_accuracy.train import *;solver = setup_solver()
solver.restore('/Users/karlzipser/scratch/2016/1/26/caffe/models/from_mnist/original_with_accuracy/model_iter_2250000.solverstate')

solver.step(1000)

solver.net.copy_from('/Users/karlzipser/scratch/2016/1/26/caffe/models/from_mnist/original_with_accuracy/model_iter_40000.caffemodel')

'''

from kzpy3.vis import *
import caffe
plt.ion()
plt.show()
os.chdir(home_path) # this is for the sake of the train_val.prototxt


def setup_solver():
	solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m1/from_mnist/original_with_accuracy/solver.prototxt"))
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver


solver = setup_solver()

def show_solver_step(solver):
	solver.net.forward()
	img = np.zeros((224,298,3))
	img[:,:,0] = solver.net.blobs['py_image_data'].data[0,6,:,:]+0.5
	img[:,:,1] = solver.net.blobs['py_image_data'].data[0,7,:,:]+0.5
	img[:,:,2] = solver.net.blobs['py_image_data'].data[0,8,:,:]+0.5
	#plt.figure(1)
	#plt.clf()
	#mi(img,1)
	print( solver.net.blobs['py_target_data'].data[0])
	print( solver.net.blobs['ip2'].data)
	print( solver.net.blobs['identity'].data)
	plt.figure(2)
	#plt.clf()
	plt.plot([0,1],[0,1],'k')
	plt.plot(solver.net.blobs['py_target_data'].data[0][9:].mean(),solver.net.blobs['ip2'].data[0][9:].mean(),'ro')
	plt.plot(solver.net.blobs['py_target_data'].data[0][:9].mean(),solver.net.blobs['ip2'].data[0][:9].mean(),'bo')
	plt.xlim((0,1))
	plt.ylim((0,1))

show_solver_step(solver)


def safe_solver_step(solver):
    while True:
        try:
            solver.step(10000)
        except Exception, e: 
            print e


def look_at_numbers(solver):
	solver.step(1)
	mi(solver.net.blobs['data'].data[:1, 0].transpose(1, 0, 2).reshape(28, 1*28),'train')
	mi(solver.net.blobs['pydata'].data[:1, 0].transpose(1, 0, 2).reshape(28, 1*28),'train2')
	plt.ion()
	plt.show()
	print solver.net.blobs['label'].data[:1]
	mi(solver.test_nets[0].blobs['data'].data[:1, 0].transpose(1, 0, 2).reshape(28, 1*28), 'test')
	print solver.test_nets[0].blobs['label'].data[:1]


def restore(solver):
	solver.restore(opjh('scratch/2015/11/23/caffe/models/from_mnist/original_with_accuracy/model_iter_1000.solverstate'))


def deploy(img_name = opjh('caffe/examples/images/7.jpg')):
	net = caffe.Net(opjh('kzpy3/caf/training/y2015/m9/from_mnist/original_with_accuracy/deploy.prototxt'),opjh('scratch/2015/9/20/caffe/models/from_mnist/original_with_accuracy/model_iter_5000.caffemodel'),caffe.TEST)
	net.blobs['data'].reshape(1,1,28,28)
	img = scipy.misc.imread(img_name)
	img = img[:,:,0] # this network wants grayscale images, no color channel.
	net.blobs['data'].data[...] = img
	out = net.forward()
	print("Predicted class is #{}.".format(out['prob'].argmax()))
	mi(img,img_name)
	return net


