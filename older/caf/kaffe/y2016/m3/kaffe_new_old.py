from kzpy3.vis import *
import caffe

def mi_diffs(solver):
	print 'py_image_data'
	mi(np.abs(solver.net.blobs['py_image_data'].diff[0,:,:,:]).mean(axis=0),'py_image_data diff')
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
		if len(l[1]) > 2:
			mi(np.abs(solver.net.blobs[l[0]].diff[0,:,:,:]).mean(axis=0),l[0]+' diff')

def show_py_image_data(data):
	d = data[0].copy()
	d = z2o(d)
	d[:,0,0] = 1
	d[:,0,1] = 0
	for j in range(1):
	    for i in range(9):

	        mi(d[i,:,:])
	        plt.pause(0.1)


solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m3/RPi3/solver_kaffe_11px.prototxt"))
f=opjD('train_val_kaffe_11px_iter_700000.caffemodel')
solver.net.copy_from(f)


for i in range(9):
	solver.net.blobs['ddata'].data[0][i,:,:] = np.random.random(np.shape(solver.net.blobs['ddata'].data[0][1,:,:]))-0.5


step_size = 0.333
jitter = 5

def steer_show_gradient(solver,s):
	for i in range(9):
		solver.net.blobs['ddata'].data[0][i,:,:] = np.random.random(np.shape(solver.net.blobs['ddata'].data[0][1,:,:]))-0.5

	src = solver.net.blobs['py_image_data']
	solver.net.forward()
	solver.net.blobs['ip2'].diff[0] *= 0
	solver.net.blobs['ip2'].diff[0,s]=1
	solver.net.backward(start='ip2')
	show_py_image_data(solver.net)



mask = np.zeros(shape(solver.net.blobs['ip2'].diff))

src_lst = []
for s in range(1):
	for i in range(9):
		solver.net.blobs['ddata'].data[0][i,:,:] = np.random.random(np.shape(solver.net.blobs['ddata'].data[0][1,:,:]))-0.5

	step_size = 1.5#0.333
	jitter = 1
	src = solver.net.blobs['py_image_data']
	for j in range(100):

		ox, oy = np.random.randint(-jitter, jitter+1, 2)
		src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift

		solver.net.forward()
		mask *= 0
		mask[0,3]=1
		mask[0,2]=0.2
		mask[0,4]=0.2
		solver.net.blobs['ip2'].diff[0] = solver.net.blobs['ip2'].data * mask

		solver.net.blobs['conv2'].diff[0] *= 0
		solver.net.blobs['conv2'].diff[0,s,15,8] = 1

	#	solver.net.backward(start='ip2')
		solver.net.backward(start='conv2')

		g = src.diff[0]
		
		src.data[:] += step_size/np.abs(g).mean() * g

		src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image
	src_lst.append(src.data.copy())



