"""
run "kzpy3/caf/training/y2016/m3/RPi3/train.py"
#f=opjh('scratch/2016/3/RPi3/11px_MC_train_on_first_set/11px_MC_iter_4700000.caffemodel')
#f=opjD('train_val_kaffe_11px_iter_900000.caffemodel')
#f=opjh('caffe/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel')
#f=opjh('scratch/2016/3/RPi3/bvlc_ref_mod_iter_2600000.caffemodel')
#f=opjD('bvlc_ref_mod_str_iter_100000.caffemodel')
f=opjD('bvlc_ref_mod_str_iter_100000.caffemodel')
solver.net.copy_from(f)
blobs = solver.net.blobs
params = solver.net.params
# safe_solver_step(solver)
# scp kzipser@redwood2.dyn.berkeley.edu:'scratch/2016/3/RPi3/bvlc_ref_mod_str_iter_100000.caffemodel' ~/Desktop
test_solver(solver,1000,100000)

"""

import caffe
from kzpy3.vis import *


os.chdir(home_path) # this is for the sake of the train_val.prototxt

#training_path = opjh('kzpy3/caf/training/y2016/m2/from_mnist/original_with_accuracy')
training_path = opjh('kzpy3/caf/training/y2016/m3/RPi3/scl25')
#solver_name = 'solver_11px_scl50.prototxt'
#solver_name = 'solver_11px_scl100_RGB.prototxt'
#solver_name = 'solver_kaffe_11px.prototxt'
#solver_name = 'solver_kaffe_11px.prototxt'
#solver_name = 'solver_kaffe_11px_RGB.prototxt'
#solver_name = 'solver_11px_MC_slim.prototxt'
#solver_name = 'solver_scl50_nin0.prototxt'
#solver_name = 'bvlc_solver_str.prototxt'
solver_name = 'solver_11px.prototxt'
#solver_name = 'solver_11px_scl25.prototxt'

def show_solver(solver):
	print('blobs')
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	print('\nparams')
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)

def setup_solver():
	solver = caffe.SGDSolver(opj(training_path,solver_name))
	show_solver(solver)
	if host_name == 'redwood2':
		caffe.set_device(0)
		caffe.set_mode_gpu()
		print("************** using GPU *************")
	return solver

solver = setup_solver()



"""
m = solver.net.blobs['M_py_image_data'].data
c = solver.net.blobs['C_py_image_data'].data
C = c[0,:,:,:]
C = C.transpose(1,2,0)
 C-=C.min();C/=C.max()
mi(m[0,8,:,:])
mi(c[0,1,:,:],2)
mi(C,3)

"""

    


def safe_solver_step(solver):
	while True:
		try:
			solver.step(10000)
			for k in solver.net.blobs.keys():
				print (k, solver.net.blobs[k].data.max())
		except Exception, e: 
			print e


def test_solver(solver,n,fig=100):
	St_list = []
	Ft_list = []
	Rt_list = []
	So_list = []
	Fo_list = []
	Ro_list = []
	start_t = time.time()
	for i in range(n):
		try:
			solver.net.forward()
			t = solver.net.blobs['py_target_data'].data[0]
			o = solver.net.blobs['ip2'].data[0]
			St_list.append(t[0])
			So_list.append(o[0])
			Ft_list.append(t[1])
			Fo_list.append(o[1])
			Rt_list.append(t[2])
			Ro_list.append(o[2])
		except Exception,e:
			print e
	print(d2s('Speed =',n/(time.time()-start_t),'trials per second.'))
	plt.figure(fig,(5,5))
	plt.clf()
	plt.plot(Ft_list,Fo_list,'gx',label='frames to turn')
	plt.plot(Rt_list,Ro_list,'rx',label='rot')
	plt.plot(St_list,So_list,'bo',label='steer')
	plt.xlim((0,1))
	plt.ylim((0,1))
	cS,cF,cR = 0,0,0
	try:
		cS = int(1000.0*np.corrcoef(St_list,So_list)[0,1])/1000.0
	except: pass
	try:
		cF = int(1000.0*np.corrcoef(Ft_list,Fo_list)[0,1])/1000.0
	except: pass
	try:
		cR = int(1000.0*np.corrcoef(Rt_list,Ro_list)[0,1])/1000.0
	except: pass
	#plt.title(cS)
	plt.title((cS,cF,cR))
	#plt.legend()
	plt.ion()
	plt.show()
	plt.figure(100+fig,(5,5))
	plt.clf()
	a=[]
	b=[]
	for tt,oo in zip(St_list,So_list):
		if tt <0.1:
			a.append(oo)
	for tt,oo in zip(St_list,So_list):
		if tt >0.9:
			b.append(oo)
	plt.hist(a,bins=25,alpha=0.5);
	plt.hist(b,bins=25,alpha=0.5);
	plt.xlim((0,1))
	plt.title((np.median(a),np.median(b),np.median(b)-np.median(a)))
	#return (St_list,So_list,Ft_list,Fo_list,Rt_list,Ro_list)





def view_M_filters(solver,fig=1):
	filters = solver.net.params['conv1'][0].data
	blnk = np.zeros((27,27))
	blnk[0,0] = -0.333/2.0
	blnk[0,1] = 0.333/2.0

	for f in range(shape(filters)[0]):
		for i in range(0,9): #(8,-1,-1):
			plt.clf()
			blnk[7:18,7:18] = filters[f,i,:,:]
			mi(blnk,figure_num=fig,img_title=d2s(f))
			plt.pause(0.1)
		blnk *= 0
		blnk[0,0] = -0.333/1.0
		blnk[0,1] = 0.333/1.0
		#mi(blnk,figure_num=fig,img_title=d2s(f))
		plt.pause(0.5)

def view_C_filters(solver,fig=2):
	filters = solver.net.params['C_conv1'][0].data
	for i in range(96):
		a=filters[i,:,:,:]
		a=np.transpose(a,(1,2,0))
		a -= a.min()
		a /= a.max()
		plt.clf()
		mi(a,img_title=d2s(i))
		plt.pause(0.5)




"""

caffe_root = opjh('caffe')  # this file is expected to be in {caffe_root}/examples
transformer = caffe.io.Transformer({'data': solver.net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.load(opj(caffe_root,'python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

f = opjD('RPi3_data/runs_scl_100_RGB/09Feb16_13h33m51s_scl=100_mir=0/310_1455053662.01_str=0_spd=66_rps=29_lrn=55_rrn=67_rnd=0_scl=100_mir=0_.jpg')


solver.net.blobs['data'].data[...] = transformer.preprocess('data', caffe.io.load_image(f)) 
out = solver.net.forward()

feat = net.blobs['ip3'].data[0]
plt.subplot(2, 1, 1)
plt.plot(feat.flat)
plt.subplot(2, 1, 2)
_ = plt.hist(feat.flat[feat.flat > 0], bins=100)


for j in range(100):
	solver.step(1)
	print solver.net.blobs['py_target_data'].data[:][0]
	mi(solver.net.blobs['py_target_data'].data[0,0,:,:],2)
	for i in range(8):
		mi(solver.net.blobs['py_image_data'].data[0,i,:,:])
		plt.pause(0.2)

n=5000
t=[]
o=[]
for i in range(n):
	solver.net.forward()
	t.append(solver.net.blobs['py_target_data'].data.copy())
	o.append(solver.net.blobs['ip2'].data.copy())
plt.clf()
t=np.array(t)
o=np.array(o)
plt.plot(t[:,0,0],o[:,0,0],'o')
plt.plot(t[:,0,1],o[:,0,1],'o')
plt.xlim(0,1)
plt.ylim(0,1)
print np.corrcoef(t[:,0,0],o[:,0,0])
print np.corrcoef(t[:,0,1],o[:,0,1])


"""








