from kzpy3.vis import *


import caffe
USE_GPU = True
gpu = 0
if USE_GPU:
	caffe.set_device(gpu)
	caffe.set_mode_gpu()
from kzpy3.caf6.Caffe_Net import *
solver_file_path = opjh("kzpy3/caf6/z2_color/solver_"+str(gpu)+"_a.prototxt")
version = 'version 1b'
weights_file_mode = None #'this one' #None #'most recent' #'this one'  #None #'most recent'
weights_file_path = None #opjh('kzpy3/caf6/z2_color/z2_color.caffemodel') #None #'/home/karlzipser/Desktop/z2_color' # None #opjD('z2_color')

caffe_net = Caffe_Net(solver_file_path,version,weights_file_mode,weights_file_path,False)




import h5py
hdf5_filename = '/media/karlzipser/ExtraDrive1/runs/direct_1Sept2016_Mr_Orange_local_sidewalks.hdf5'
solver_inputs = h5py.File(hdf5_filename,'r')



def plot_performance(steer,motor,loss1000):
	figure('loss1000')
	clf()
	plot(loss1000)
	plt.title(time_str('Pretty'))
	figure('steer')
	clf()

	s1000 = steer[-(min(len(steer),10000)):]
	s = array(s1000)
	plot(s[:,0],s[:,1],'o')
	plt.xlim(0,1.0)
	plt.ylim(0,1.0)
	plot([-1,5,1.5],[-1,5,1.5],'r')
	plt_square()
	plt.title(time_str('Pretty'))


timer = Timer(6)

ks = solver_inputs.keys()
print len(ks)
ctr = 0

steer = []
motor = []

while True:
	random.shuffle(ks)
	for k in ks:
		caffe_net.solver.net.blobs['ZED_data_pool2'].data[:] = solver_inputs[k]['ZED_data_pool2'][:]/255.-0.5
		caffe_net.solver.net.blobs['metadata'].data[:] = solver_inputs[k]['metadata'][:]
		caffe_net.solver.net.blobs['steer_motor_target_data'].data[:] = solver_inputs[k]['steer_motor_target_data'][:]
		caffe_net.train_step()
		steer.append([caffe_net.solver.net.blobs['steer_motor_target_data'].data[0,9],caffe_net.solver.net.blobs['ip2'].data[0,9]])
		motor.append([caffe_net.solver.net.blobs['steer_motor_target_data'].data[0,19],caffe_net.solver.net.blobs['ip2'].data[0,19]])
		ctr += 1
		if timer.check():
			plot_performance(steer,motor,caffe_net.loss1000)
			timer.reset()
pass	






