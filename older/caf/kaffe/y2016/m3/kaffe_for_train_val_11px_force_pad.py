from kzpy3.vis import *
import caffe

# show_py_image_data(bb,fig=1,img_title='',dst=opjD('temp_conv2'),start_num=0,blanks=5,repeats=3)
def show_py_image_data(data,fig=1,img_title='',dst='',start_num=0,blanks=0,repeats=1):
	d = data[0].copy()
	d = z2o(d)
	print shape(d)
	if len(dst) > 0:
		unix(d2s('mkdir -p',dst),False)
	img = np.zeros((shape(d)[1],shape(d)[2],3))
	img = 0*img + 0.5#d[0,0,0]
	ctr = 0
	for j in range(repeats):
		for i in range(-blanks,9):
			
			if i >= 0:
				for l in range(3):
					img[:,:,l] = d[i,:,:]
			img[0,0] = 0
			img[0,1] = 1

			mi(img,fig,img_title=img_title)
			plt.pause(0.1)
			if len(dst) > 0:
				imsave(opj(dst,d2n(start_num+ctr,'.png')),imresize(img,400,'nearest'))
				ctr += 1

def img_from_caffe_data(data):
	img = np.zeros((shape(data)[2],shape(data)[3],3))
	img[:,:,2] = data[0,0,:,:]
	img[:,:,1] = data[0,1,:,:]
	img[:,:,0] = data[0,2,:,:]
	return z2o(img)



#solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m3/RPi3/solver_kaffe_11px.prototxt"))
#f=opjD('train_val_kaffe_11px_iter_2600000.caffemodel')
#solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m3/RPi3/solver_kaffe_11px.prototxt"))
#f=opjh('Google_Drive/2016-1/deep_dream_directions/BW/train_val_kaffe_11px_iter_3900000.caffemodel')
#solver.net.copy_from(f)








for i in range(9):
	solver.net.blobs['ddata'].data[0][i,:,:] = np.random.random(np.shape(solver.net.blobs['ddata'].data[0][1,:,:]))-0.5
#solver.net.blobs['py_image_data'].data[0] = 0*solver.net.blobs['py_image_data'].data[0]
#solver.net.blobs['ddata'].data[0] = 0*solver.net.blobs['ddata'].data[0]


jitter = 3
for j in range(100):
	ox, oy = np.random.randint(-jitter, jitter+1, 2)
	solver.net.blobs['ddata'].data[0] = np.roll(np.roll(solver.net.blobs['ddata'].data[0], ox, -1), oy, -2) # apply jitter shift
	
	solver.net.forward()#start='ddata')
	p = solver.net.blobs['ip2'].data[0,:]; p = (p*100).astype(int)/100.0; print p
#	print  solver.net.blobs['ip2'].data[:]
	solver.net.blobs['ip2'].diff[0] *= 0
	solver.net.blobs['ip2'].diff[0,3]=1
#	solver.net.blobs['conv1'].diff[0] *= 0
#	solver.net.blobs['conv1'].diff[0,30,8,15] = 1
#	solver.net.blobs['conv2'].diff[0,2,15,15] = 1
	solver.net.backward(start='ip2')
#	solver.net.backward(start='conv2')
	g = solver.net.blobs['ddata'].diff[0]
	solver.net.blobs['ddata'].data[:] += 0.005/np.abs(g).mean() * g
	
	solver.net.blobs['ddata'].data[:] = z2o(solver.net.blobs['ddata'].data[:]) - 0.5
	solver.net.blobs['ddata'].data[:] *= 0.95
	#solver.net.blobs['ddata'].data[0][i,:,:] += 0.001*(np.random.random(np.shape(solver.net.blobs['ddata'].data[0][1,:,:]))-0.5)
	solver.net.blobs['ddata'].data[0] = np.roll(np.roll(solver.net.blobs['ddata'].data[0], -ox, -1), -oy, -2) # unshift image

# use this for ~/Desktop/deep_dream_directions





sample_sequence = np.load(opjD('pid.npy'))

solver.net.blobs['ddata'].data[:] = sample_sequence.copy()
jitter = 0
for j in range(1000):
	solver.net.blobs['ddata'].data[0,0,:,:] = sample_sequence[0,0,:,:].copy()
	ox, oy = np.random.randint(-jitter, jitter+1, 2)
	solver.net.blobs['ddata'].data[0] = np.roll(np.roll(solver.net.blobs['ddata'].data[0], ox, -1), oy, -2) # apply jitter shift
	
	solver.net.forward()#start='ddata')
	p = solver.net.blobs['ip2'].data[0,:]; p = (p*100).astype(int)/100.0; print p
#	print  solver.net.blobs['ip2'].data[:]
#	solver.net.blobs['ip2'].diff[0] *= 0
#	solver.net.blobs['ip2'].diff[0,6]=1
	solver.net.blobs['conv1'].diff[0] *= 0
	solver.net.blobs['conv1'].diff[0,30,8,15] = 1
#	solver.net.blobs['conv2'].diff[0,2,15,15] = 1
#	solver.net.backward(start='ip2')
	solver.net.backward(start='conv1')
	g = solver.net.blobs['ddata'].diff[0]
	solver.net.blobs['ddata'].data[:] += 0.005/np.abs(g).mean() * g
	
	#solver.net.blobs['ddata'].data[:] = z2o(solver.net.blobs['ddata'].data[:]) - 0.5
	#solver.net.blobs['ddata'].data[:] *= 0.95
	#solver.net.blobs['ddata'].data[0][i,:,:] += 0.001*(np.random.random(np.shape(solver.net.blobs['ddata'].data[0][1,:,:]))-0.5)
	solver.net.blobs['ddata'].data[0] = np.roll(np.roll(solver.net.blobs['ddata'].data[0], -ox, -1), -oy, -2) # unshift image








show_py_image_data(solver.net.blobs['py_image_data'].data,'py_image_data')

show_py_image_data(solver.net.blobs['conv1'].data,'conv1')



"""
scp kzipser@redwood2.dyn.berkeley.edu:'scratch/2016/2/16/caffe/models/from_mnist/original_with_accuracy_11px/train_val_kaffe_11px_iter_2600000.caffemodel' ~/Desktop
train_val_kaffe_11px_iter_2600000.caffemodel

for 100000, percent correct = 45.3%
for 900000, percent correct = 48.1%
for 2600000, percent correct = 51.4%
chance = 14.2%
"""
n = 500
n_correct = 0
for i in range(n):
	print i
	solver.net.forward()
	if solver.net.blobs['MC_cat_ip2'].data[0].argmax(axis=0) == solver.net.blobs['MC_cat_py_target_data'].data[0].argmax(axis=0):
		n_correct += 1

print(d2s('percent correct =',n_correct,'/',n,'chance =',int(1/7.0*n),'/',n))
print(d2s('percent correct =',n_correct/(1.0*n)))



n = 1000
n_correct = 0
for i in range(n):
	print i
	solver.net.forward()
	if solver.net.blobs['ip3'].data[0].argmax(axis=0) == solver.net.blobs['py_target_data'].data[0].argmax(axis=0):
		n_correct += 1

print(d2s('percent correct =',n_correct,'/',n,'chance =',int(1/7.0*n),'/',n))
print(d2s('percent correct =',n_correct/(1.0*n)))


n=1000
results = np.zeros((7,7))
ctrs = np.zeros(7)
for i in range(n):
	solver.net.forward()
	j = solver.net.blobs['py_target_data'].data[0].argmax(axis=0)
	results[j,:] += solver.net.blobs['ip3'].data[0]
	ctrs[j] += 1.0
for i in range(7):
	results[i,:] /= ctrs[i]

print results




results = {}
ctr = 0

img = imread('/Users/karlzipser/Desktop/RPi3_data/runs_scl_100_RGB/09Feb16_14h03m20s_scl=100_mir=0/3091_1455055614.01_str=0_spd=48_rps=28_lrn=0_rrn=0_rnd=0_scl=100_mir=0_.jpg')

solver.net.blobs['C_ip2'].data[:] *= 0
for k in [6]:#range(7):
	#for i in range(3):
	#	solver.net.blobs['C_ddata'].data[0][i,:,:] = np.random.random(np.shape(solver.net.blobs['C_ddata'].data[0][1,:,:]))-0.5
	#solver.net.blobs['py_image_data'].data[0] = 0*solver.net.blobs['py_image_data'].data[0]
	#solver.net.blobs['ddata'].data[0] = 0*solver.net.blobs['ddata'].data[0]

	solver.net.blobs['C_py_image_data'].diff[0] *= 0
	solver.net.blobs['C_ddata'].data[0,0,:,:] = img[:,:,0].copy()
	solver.net.blobs['C_ddata'].data[0,1,:,:] = img[:,:,1].copy()
	solver.net.blobs['C_ddata'].data[0,2,:,:] = img[:,:,2].copy()
	
	jitter = 3
	p_best = 0
	c_best = 0*solver.net.blobs['C_py_image_data'].data[:]
	for j in range(200):
		ox, oy = np.random.randint(-jitter, jitter+1, 2)
		solver.net.blobs['C_ddata'].data[0] = np.roll(np.roll(solver.net.blobs['C_ddata'].data[0], ox, -1), oy, -2) # apply jitter shift

		solver.net.forward()#start='ddata')
		print (100*solver.net.blobs['C_ip2'].data[:]).astype(int)/100.0
		#p = solver.net.blobs['C_ip2'].data[0,:].copy(); p = (p*100).astype(int)/100.0; print p
		if j > 0:
			if solver.net.blobs['C_ip2'].data[0,k] > p_best:
				p_best = solver.net.blobs['C_ip2'].data[0,k]
				c_best = solver.net.blobs['C_py_image_data'].data[:].copy()
			else:
				print(d2s(p_best,'>',solver.net.blobs['C_ip2'].data[0,k]))
				print('revert')
				solver.net.blobs['C_py_image_data'].data[:] = 1.0 * c_best
	#	print  solver.net.blobs['ip2'].data[:]
	#	solver.net.blobs['C_ip2'].diff[0] *= 0
	#	solver.net.blobs['C_ip2'].diff[0,3]=1
		solver.net.blobs['C_ip2'].diff[0] *= 0
		solver.net.blobs['C_ip2'].diff[0,k] = 1
		solver.net.backward(start='C_ip2')
	#	solver.net.backward(start='conv2')
		g = solver.net.blobs['C_py_image_data'].diff[0]
		solver.net.blobs['C_ddata'].data[:] += 0.001/np.abs(g).mean() * g
		
		solver.net.blobs['C_ddata'].data[:] = z2o(solver.net.blobs['C_ddata'].data[:]) - 0.5
		#solver.net.blobs['C_ddata'].data[:] *= 0.95
		#solver.net.blobs['ddata'].data[0][i,:,:] += 0.001*(np.random.random(np.shape(solver.net.blobs['ddata'].data[0][1,:,:]))-0.5)
		solver.net.blobs['C_ddata'].data[0] = np.roll(np.roll(solver.net.blobs['C_ddata'].data[0], -ox, -1), -oy, -2) # unshift image
	results[ctr] = img_from_caffe_data(solver.net.blobs['C_ddata'].data)
	mi(results[ctr],ctr,img_title=d2s(k))
	ctr += 1
	plt.pause(0.01)





results = {}

for k in range(0,512):
	for i in range(9):
		solver.net.blobs['M_ddata'].data[0][i,:,:] = np.random.random(np.shape(solver.net.blobs['M_ddata'].data[0][1,:,:]))-0.5
	for i in range(3):
		solver.net.blobs['C_ddata'].data[0][i,:,:] = np.random.random(np.shape(solver.net.blobs['C_ddata'].data[0][1,:,:]))-0.5
	jitter = 3
	for j in range(60):
		ox, oy = np.random.randint(-jitter, jitter+1, 2)
		solver.net.blobs['M_ddata'].data[0] = np.roll(np.roll(solver.net.blobs['M_ddata'].data[0], ox, -1), oy, -2) # apply jitter shift
		
		solver.net.forward()#start='ddata')
	#	p = solver.net.blobs['M_cccp2'].data[0,:]; p = (p*100).astype(int)/100.0; print p
	#	print  solver.net.blobs['ip2'].data[:]
		solver.net.blobs['MC_cat_ip2'].diff[0] *= 0
		solver.net.blobs['MC_cat_ip2'].diff[0,k]=1
	#	solver.net.blobs['MC_conv3'].diff[0]*=0
	#	solver.net.blobs['MC_conv3'].diff[0,0,10,10]=1
	#	solver.net.blobs['conv1'].diff[0] *= 0
	#	solver.net.blobs['conv1'].diff[0,30,8,15] = 1
	#	solver.net.blobs['conv2'].diff[0,2,15,15] = 1
		solver.net.backward(start='MC_cat_ip2')
	#	solver.net.backward(start='conv2')
		for l in ['M_ddata','C_ddata']:
			g = solver.net.blobs[l].diff[0]
			solver.net.blobs[l].data[:] += 0.005/np.abs(g).mean() * g
			
			solver.net.blobs[l].data[:] = z2o(solver.net.blobs[l].data[:]) - 0.5
			solver.net.blobs[l].data[:] *= 0.95
			#solver.net.blobs['ddata'].data[0][i,:,:] += 0.001*(np.random.random(np.shape(solver.net.blobs['ddata'].data[0][1,:,:]))-0.5)
			solver.net.blobs[l].data[0] = np.roll(np.roll(solver.net.blobs[l].data[0], -ox, -1), -oy, -2) # unshift image
	print  solver.net.blobs['MC_cat_ip2'].data[:]
	# use this for ~/Desktop/deep_dream_directions
	results[k] = (solver.net.blobs['M_ddata'].data.copy(),solver.net.blobs['C_ddata'].data.copy())
	mi(img_from_caffe_data(results[k][1]),'C_ddata',img_title=d2s('C_ddata',k))
	show_py_image_data(results[k][0],'M_ddata')


	
for k in range(7):
	mi(img_from_caffe_data(results[k][1]),'C_ddata',img_title=d2s('C_ddata',k))
	show_py_image_data(results[k][0],'M_ddata')
	time.sleep(1)








img = img.mean(axis=2)
img = imresize(img,50)
img = z2o(img)

results = {}

for k in [0,3,6]:#range(0,7):
	for i in range(9):
		#solver.net.blobs['ddata'].data[0,i,:,:] = img[:,:].copy()-0.5
		solver.net.blobs['ddata'].data[0][i,:,:] = np.random.random(np.shape(solver.net.blobs['ddata'].data[0][1,:,:]))-0.5
	jitter = 0
	for j in range(100):
		ox, oy = np.random.randint(-jitter, jitter+1, 2)
		solver.net.blobs['ddata'].data[0] = np.roll(np.roll(solver.net.blobs['ddata'].data[0], ox, -1), oy, -2) # apply jitter shift
		
		solver.net.forward()#start='ddata')
	#	p = solver.net.blobs['M_cccp2'].data[0,:]; p = (p*100).astype(int)/100.0; print p
	#	print  solver.net.blobs['ip2'].data[:]
	#	solver.net.blobs['ip1'].diff[0] *= 0
	#	solver.net.blobs['ip1'].diff[0,k]=1
		solver.net.blobs['conv1'].diff[0]*=0
		solver.net.blobs['conv1'].diff[0,k,10,10]=1
	#	solver.net.blobs['conv1'].diff[0] *= 0
	#	solver.net.blobs['conv1'].diff[0,30,8,15] = 1
	#	solver.net.blobs['conv2'].diff[0,2,15,15] = 1
	#	solver.net.backward(start='ip1')
		solver.net.backward(start='conv1')
		for l in ['ddata']:
			g = solver.net.blobs[l].diff[0]
			solver.net.blobs[l].data[:] += 0.005/np.abs(g).mean() * g
			
			#solver.net.blobs[l].data[:] = z2o(solver.net.blobs[l].data[:]) - 0.5
			solver.net.blobs[l].data[:] *= 0.95
			#solver.net.blobs['ddata'].data[0][i,:,:] += 0.001*(np.random.random(np.shape(solver.net.blobs['ddata'].data[0][1,:,:]))-0.5)
			solver.net.blobs[l].data[0] = np.roll(np.roll(solver.net.blobs[l].data[0], -ox, -1), -oy, -2) # unshift image
		#solver.net.blobs['ddata'].data[0,1:,:,:] = z2o(solver.net.blobs['ddata'].data[0,1:,:,:])
		#solver.net.blobs['ddata'].data[0,0,:,:] = img.copy() - 0.5
	print  solver.net.blobs['ip2'].data[:]
	# use this for ~/Desktop/deep_dream_directions
	results[k] = (solver.net.blobs['ddata'].data.copy(),solver.net.blobs['ddata'].data.copy())
	show_py_image_data(results[k][0],'ddata')


#results = motion_ip1_j3.copy()
#results = motion_conv1_j0.copy()
#results = motion_ip1_j3.copy()

def show_results(results,img_title):
	for k in [0,3,6,]:
		for l in range(5):
			show_py_image_data(results[k][0],100,d2s(img_title,k))
			time.sleep(0.5)
		time.sleep(1.0)


























from kzpy3.vis import *
import caffe
# scp kzipser@redwood2.dyn.berkeley.edu:'scratch/2016/3/RPi3/bvlc_ref_mod_iter_400000.caffemodel' ~/Desktop
training_path = opjh('kzpy3/caf/training/y2016/m3/RPi3')
solver_name = 'bvlc_solver_0.prototxt'
solver = caffe.SGDSolver(opj(training_path,solver_name))
model = opjD('bvlc_ref_mod_iter_400000.caffemodel')
solver.net.copy_from(model)




results = {}
ctr = 0
f='/Users/karlzipser/Desktop/RPi3_data/runs_scl_100_RGB/09Feb16_14h03m20s_scl=100_mir=0/3091_1455055614.01_str=0_spd=48_rps=28_lrn=0_rrn=0_rnd=0_scl=100_mir=0_.jpg'
for k in [0,3,6]:
	caffe_root = opjh('caffe')  # this file is expected to be in {caffe_root}/examples
	transformer = caffe.io.Transformer({'data': (1, 3, 227, 227)})
	transformer.set_transpose('data', (2,0,1))
	transformer.set_mean('data', np.load(opj(caffe_root,'python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
	transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
	transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
	solver.net.blobs['data'].data[...] = transformer.preprocess('data', caffe.io.load_image(f))
	jitter = 3
	for j in range(150):
		ox, oy = np.random.randint(-jitter, jitter+1, 2)
		solver.net.blobs['data'].data[0] = np.roll(np.roll(solver.net.blobs['data'].data[0], ox, -1), oy, -2) # apply jitter shift
		solver.net.forward()
		solver.net.blobs['ip3'].diff[0] *= 0
		solver.net.blobs['ip3'].diff[0,k] = 1
		solver.net.backward(start='ip3')
		g = solver.net.blobs['py_image_data'].diff[0]
		solver.net.blobs['data'].data[:] += 0.1/np.abs(g).mean() * g
		#solver.net.blobs['data'].data[:] = z2o(solver.net.blobs['data'].data[:]) - 0.5
		solver.net.blobs['data'].data[0] = np.roll(np.roll(solver.net.blobs['data'].data[0], -ox, -1), -oy, -2) # unshift image
	results[ctr] = img_from_caffe_data(solver.net.blobs['data'].data)
	mi(results[ctr],ctr,img_title=d2s(k))
	ctr += 1
	plt.pause(0.01)



