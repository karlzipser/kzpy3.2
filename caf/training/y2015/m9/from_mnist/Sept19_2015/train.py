from kzpy3.vis import *
import caffe

os.chdir(home_path)

solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2015/m9/from_mnist/Sept19_2015/solver.prototxt"))

for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
	print(l)

for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
	print(l)
	
def ook():
	solver.step(1)

	mi(solver.net.blobs['data'].data[:8, 0].transpose(1, 0, 2).reshape(28, 8*28),'train')
	print solver.net.blobs['label'].data[:8]

	mi(solver.test_nets[0].blobs['data'].data[:8, 0].transpose(1, 0, 2).reshape(28, 8*28), 'test')
	print solver.test_nets[0].blobs['label'].data[:8]