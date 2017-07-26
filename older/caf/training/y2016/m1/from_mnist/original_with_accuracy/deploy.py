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



solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m1/from_mnist/original_with_accuracy/solver_deploy.prototxt"))

solver.net.copy_from(opjh('scratch/2016/1/26/caffe/models/from_mnist/original_with_accuracy/model_iter_350000.caffemodel'))

solver.net.forward();print solver.net.blobs['ip2'].data


