'''
20 Sept. 2015
Do this:
from kzpy3.caf.training.y2015.m9.from_mnist.original_with_isolayers.train import *


from kzpy3.vis import *
%matplotlib osx

t=1
d = solver.net.blobs['pydata'].data
i1 = solver.net.blobs['ic1_out2'].data
i2 = solver.net.blobs['ic2_out2'].data
i3 = solver.net.blobs['ic3_out2'].data
i4 = solver.net.blobs['ic11_out2'].data
i5 = solver.net.blobs['ic12_out1'].data
for m in range(10):
n = m +10
ii1 = i1[n,:].transpose(1,2,0)
ii2 = i2[n,:].transpose(1,2,0)
ii3 = i3[n,:].transpose(1,2,0)
ii4 = i4[n,:].transpose(1,2,0)
ii5 = i5[n,-3:].transpose(1,2,0)
dd=dd = d[n,0,:,:]
mi(dd,t,[6,10,m+1],img_title=d2s(int(solver.net.blobs['label'].data[n])))
mi(ii1,t,[6,10,m+11])
mi(ii2,t,[6,10,m+21],img_title=d2s(solver.net.blobs['ip1'].data[n,:].argmax()))
mi(ii3,t,[6,10,m+31],img_title=d2s(solver.net.blobs['ip1'].data[n,:].argmax()))
mi(ii4,t,[6,10,m+41],img_title=d2s(solver.net.blobs['ip2'].data[n,:].argmax()))
mi(ii5,t,[6,10,m+51],img_title=d2s(solver.net.blobs['ip2'].data[n,:].argmax()))



'''

from kzpy3.utils import *
import caffe

if home_path == '/global/home/users/karlz':
	caffe.set_device(0)
	caffe.set_mode_gpu()

os.chdir(home_path) # this is for the sake of the train_val.prototxt

global solver
global net

def all():
	global solver
	solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2015/m9/from_mnist/original_with_isolayers/solver.prototxt"))
	solver.step(100000)


def setup_solver():
	global solver
	solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2015/m9/from_mnist/original_with_isolayers/solver.prototxt"))
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
	solver.restore(opjh('scratch/2015/9/20/caffe/models/from_mnist/original_with_isolayers/model_iter_5000.solverstate'))


def deploy(img_name = opjh('caffe/examples/images/7.jpg')):
	global net
	net = caffe.Net(opjh('kzpy3/caf/training/y2015/m9/from_mnist/original_with_isolayers/deploy.prototxt'),opjh('scratch/2015/9/20/caffe/models/from_mnist/original_with_isolayers/model_iter_5000.caffemodel'),caffe.TEST)
	net.blobs['data'].reshape(1,1,28,28)
	img = scipy.misc.imread(img_name)
	img = img[:,:,0] # this network wants grayscale images, no color channel.
	net.blobs['data'].data[...] = img
	out = net.forward()
	print("Predicted class is #{}.".format(out['prob'].argmax()))
	mi(img,img_name)

if __name__ == '__main__':
	all()
