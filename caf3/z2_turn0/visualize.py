import caffe
from kzpy3.vis import *
os.chdir(home_path) # this is for the sake of the train_val.prototxt

########################################################
#          SETUP SECTION
#
solver_file_path = opjh("kzpy3/caf3/z2/solver.prototxt")
weights_file_path = opjD('z2/z2.caffemodel') #
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

plt.ion()
for n in range(96):
	width = 11
	img = np.zeros((2*width+7,2*width+7))
	img[2:width+2,2:width+2] = solver.net.params['conv1'][0].data[n,0,:,:]
	img[2:width+2,-(width+2):-2] = solver.net.params['conv1'][0].data[n,2,:,:]
	img[-(width+2):-2,2:width+2] = solver.net.params['conv1'][0].data[n,1,:,:]
	img[-(width+2):-2,-(width+2):-2] = solver.net.params['conv1'][0].data[n,3,:,:]

	mi(img,'conv1',img_title=d2s('conv1 channel',n)) 

	plt.pause(1)

