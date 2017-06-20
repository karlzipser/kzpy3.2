import caffe
from kzpy3.vis import *
os.chdir(home_path) # this is for the sake of the train_val.prototxt

########################################################
#          SETUP SECTION
#
solver_file_path = opjh("kzpy3/caf6/z2_color_3_step/solver.prototxt")
#weights_file_path = opjD('z2_color/z2_color.caffemodel') #
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
weights_file_path = opjD('z2_color_3_step')
weights_file_path = most_recent_file_in_folder(weights_file_path,['z2_color_3_step','caffemodel'])
solver.net.copy_from(weights_file_path)
plt.ion()

for n in range(96):
	width = 11
	img = np.zeros((3*width+8,2*width+6,3))
	for c in range(3):
		img[2:2+width,2:width+2,c] = solver.net.params['conv1'][0].data[n,0+6*c,:,:]
		img[2:2+width,-(width+2):-2,c] = solver.net.params['conv1'][0].data[n,3+6*c,:,:]
		img[4+width:4+2*width,2:width+2,c] = solver.net.params['conv1'][0].data[n,1+6*c,:,:]
		img[4+width:4+2*width,-(width+2):-2,c] = solver.net.params['conv1'][0].data[n,4+6*c,:,:]
		img[6+2*width:6+3*width,2:width+2,c] = solver.net.params['conv1'][0].data[n,2+6*c,:,:]
		img[6+2*width:6+3*width,-(width+2):-2,c] = solver.net.params['conv1'][0].data[n,5+6*c,:,:]

	mi(z2o(img),'conv1',img_title=d2s('conv1 channel',n)) 
	imsave(opjD('temp',d2n(n,'.png')),img)
	if n == 0:
		print("wait 10s")
		pause(10)
	else:
		pause(1)
	"""
					solver.net.blobs['ZED_data_pool2'].data[0,0,:,:] = data['left'][0][:,:,0]
					solver.net.blobs['ZED_data_pool2'].data[0,1,:,:] = data['left'][1][:,:,0]
					solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = data['left'][2][:,:,0]
					solver.net.blobs['ZED_data_pool2'].data[0,3,:,:] = data['right'][0][:,:,0]
					solver.net.blobs['ZED_data_pool2'].data[0,4,:,:] = data['right'][1][:,:,0]
					solver.net.blobs['ZED_data_pool2'].data[0,5,:,:] = data['right'][2][:,:,0]
					solver.net.blobs['ZED_data_pool2'].data[0,6,:,:] = data['left'][0][:,:,1]
					solver.net.blobs['ZED_data_pool2'].data[0,7,:,:] = data['left'][1][:,:,1]
					solver.net.blobs['ZED_data_pool2'].data[0,8,:,:] = data['left'][2][:,:,1]
					solver.net.blobs['ZED_data_pool2'].data[0,9,:,:] = data['right'][0][:,:,1]
					solver.net.blobs['ZED_data_pool2'].data[0,10,:,:] = data['right'][1][:,:,1]
					solver.net.blobs['ZED_data_pool2'].data[0,11,:,:] = data['right'][2][:,:,1]
					solver.net.blobs['ZED_data_pool2'].data[0,12,:,:] = data['left'][0][:,:,2]
					solver.net.blobs['ZED_data_pool2'].data[0,13,:,:] = data['left'][1][:,:,2]
					solver.net.blobs['ZED_data_pool2'].data[0,14,:,:] = data['left'][2][:,:,2]
					solver.net.blobs['ZED_data_pool2'].data[0,15,:,:] = data['right'][0][:,:,2]
					solver.net.blobs['ZED_data_pool2'].data[0,16,:,:] = data['right'][1][:,:,2]
					solver.net.blobs['ZED_data_pool2'].data[0,17,:,:] = data['right'][2][:,:,2]
	"""