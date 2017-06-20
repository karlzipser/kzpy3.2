'''
21 Sept. 2015, Haarlem

Take the MNIST number, randomly reverse contrast and present this to net [SimpleLayer1] or
with distractor letters [SimpleLayer2].
Output is classification and identity mapping of original number without any
contrast reversal or distractors.

This net thus illustrates:
	- python layer manipulation of data layer
	- identity mapping with Euclidean loss layer

To train:

from kzpy3.caf.training.y2015.m9.from_mnist.python_identity_mapping.train import *
setup_solver()
train()

or

from kzpy3.caf.training.y2015.m9.from_mnist.python_identity_mapping.train import *;setup_solver();train(1000)


To look at sample outputs:

%matplotlib osx 
deploy(17000)
test(img_name = opjh('caffe/examples/images/0.png'))
test(img_name = opjh('caffe/examples/images/2.png'))
test(img_name = opjh('caffe/examples/images/7.png'))


To look at training outputs:

%matplotlib osx
from kzpy3.caf.training.y2015.m9.from_mnist.python_identity_mapping.train import *
d = solver.net.blobs['data'].data
p = solver.net.blobs['pydata'].data
o = solver.net.blobs['ip3'].data
#o2 = solver.net.blobs['ip3_2'].data
for n in range(10):
oo = np.reshape(o[n,:],(28,28))
#oo2 = np.reshape(o2[n,:],(28,28))
dd=dd = d[n,0,:,:]
pp=pp = p[n,0,:,:]
mi(dd,10,[4,10,n+1])
mi(pp,10,[4,10,n+11],img_title=d2s(int(solver.net.blobs['label'].data[n])))
mi(oo,10,[4,10,n+21],img_title=d2s(solver.net.blobs['ip2'].data[n,:].argmax()))
#mi(oo2,10,[4,10,n+31],img_title=d2s(solver.net.blobs['ip2_2'].data[n,:].argmax()))


'''

from kzpy3.vis import *
import caffe

os.chdir(home_path) # this is for the sake of the train_val.prototxt

global solver
global net

def setup_solver():
	global solver
	solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2015/m9/from_mnist/python_identity_mapping/solver.prototxt"))
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)

def train(n=5000):
	solver.step(n)


def look_at_numbers():
	solver.step(1)
	mi(solver.net.blobs['data'].data[:8, 0].transpose(1, 0, 2).reshape(28, 8*28),'train')
	print solver.net.blobs['label'].data[:8]
	mi(solver.test_nets[0].blobs['data'].data[:8, 0].transpose(1, 0, 2).reshape(28, 8*28), 'test')
	print solver.test_nets[0].blobs['label'].data[:8]


def restore(itr):
	solver.restore(opjh(d2n('scratch/2015/9/20/caffe/models/from_mnist/python_identity_mapping/model_iter_',itr,'.solverstate')))


def deploy(itr):
	global net
	net = caffe.Net(opjh('kzpy3/caf/training/y2015/m9/from_mnist/python_identity_mapping/deploy.prototxt'),opjh(d2n('scratch/2015/9/20/caffe/models/from_mnist/python_identity_mapping/model_iter_',itr,'.caffemodel')),caffe.TEST)
	net.blobs['data'].reshape(1,1,28,28)

def test(img_name = opjh('caffe/examples/images/7.jpg')):
	global net
	img = scipy.misc.imread(img_name)
	img = img[:,:,0] # this network wants grayscale images, no color channel.
	net.blobs['data'].data[...] = img
	out = net.forward()
	print("Predicted class is #{}.".format(out['prob'].argmax()))
	plt.figure('check activations')
	plt.clf()
	mi(img,'check activations',[1,4,1])
	mi(np.reshape(net.blobs['data'].data,(28,28)),'check activations',[1,4,2])
	mi(np.reshape(net.blobs['pydata'].data,(28,28)),'check activations',[1,4,3])
	mi(np.reshape(net.blobs['ip3'].data,(28,28)),'check activations',[1,4,4])

def filters():
	net.blobs['data'].reshape(1,1,28,28)
	f = net.params['conv1'][0].data
	for i in range(shape(f)[0]):
		mi(f[i,0,:,:],1,[5,5,i+1],'conv1')

def vis_square(data, fig_name='vis_square',subplot_array=[1,1,1], padsize=1, padval=0):
    data -= data.min()
    data /= data.max()   
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    mi(data,fig_name,subplot_array)
