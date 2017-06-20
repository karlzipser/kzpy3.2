'''
16 Feb 2016

from kzpy3.caf.training.y2016.m2.from_mnist.original_with_accuracy.train import *

solver.net.copy_from(opjh('scratch/2016/2/16/caffe/models/from_mnist/original_with_accuracy_11px_scl50_nin/original_with_accuracy_11px_scl50_nin_iter_300000.caffemodel'))

safe_solver_step(solver)

'''
import caffe
from kzpy3.utils import *

ON_CLUSTER = False
if home_path == '/global/home/users/karlz':
	ON_CLUSTER = True


if not ON_CLUSTER:
	from kzpy3.vis import *
	plt.ion()
	plt.show()
os.chdir(home_path) # this is for the sake of the train_val.prototxt

if host_name == 'redwood2':
	caffe.set_device(0)
	caffe.set_mode_gpu()

def setup_solver():
	solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m2/from_mnist/original_with_accuracy/solver_11px_scl50.prototxt"))
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver


solver = setup_solver()

#show_solver_step(solver)


def safe_solver_step(solver):
    while True:
        try:
            solver.step(10000)
        except Exception, e: 
            print e

"""
solver.step(1)
for i in range(9):
    plt.figure(9)
    plt.clf()
    mi(solver.net.blobs['py_image_data'].data[0,i,:,:],9,img_title=d2s(solver.net.blobs['py_target_data'].data[0][:],solver.net.blobs['ip2'].data))
    plt.pause(0.0001)

"""

def show_solver_step(solver):
	solver.net.forward()
	img = np.zeros((224,298,3))
	img[:,:,0] = solver.net.blobs['py_image_data'].data[0,6,:,:]+0.5
	img[:,:,1] = solver.net.blobs['py_image_data'].data[0,7,:,:]+0.5
	img[:,:,2] = solver.net.blobs['py_image_data'].data[0,8,:,:]+0.5
	#plt.figure(1)
	#plt.clf()
	#mi(img,1)
	print( solver.net.blobs['py_target_data'].data[0])
	print( solver.net.blobs['ip2'].data)
	print( solver.net.blobs['identity'].data)
	plt.figure(2)
	#plt.clf()
	plt.plot([0,1],[0,1],'k')
	plt.plot(solver.net.blobs['py_target_data'].data[0][9:].mean(),solver.net.blobs['ip2'].data[0][9:].mean(),'ro')
	plt.plot(solver.net.blobs['py_target_data'].data[0][:9].mean(),solver.net.blobs['ip2'].data[0][:9].mean(),'bo')
	plt.xlim((0,1))
	plt.ylim((0,1))


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
	plt.figure(fig,(5,7))
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
	plt.title((cS,cF,cR))
	#plt.legend()
	plt.ion()
	plt.show()
	plt.figure(100+fig,(5,7))
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
	return (St_list,So_list,Ft_list,Fo_list,Rt_list,Ro_list)

"""
solver.net.copy_from(opjh('/Users/karlzipser/scratch/2016/2/16/caffe/models/from_mnist/original_with_accuracy/model_iter_3200000.caffemodel'))
solver.net.copy_from(opjh('/Users/karlzipser/scratch/2016/2/16/caffe/models/from_mnist/original_with_accuracy_11px_iter_4800000.caffemodel'))
"""
o_list = [0,0,0,0,0]
def test_solver2(solver):
	global o_list
	solver.net.forward()
	o = solver.net.blobs['ip2'].data[0][0]
	advance(o_list,o)
	o = np.array(o_list).mean()
	img = solver.net.blobs['py_image_data'].data[0,8,:,:]
	img[0:2,:] = 0.5
	o -= 0.5
	if o >= 0:
		img[0:1,int(75/2.0):int(75/2.0+37*o)] = -0.5
	else:
		img[0:1,int(75/2.0+37*o):int(75/2.0)] = -0.5
	img[1,75/2] = -0.5
	plt.figure(7)
	plt.clf()
	mi(img,7)#,img_title=d2s(o))
	plt.pause(0.00001)
	

def view_filters(solver,fig=1):
	filters = solver.net.params['conv1'][0].data
	blnk = np.zeros((27,27*10))
	blnk[0,0] = -0.333/2.0
	blnk[0,1] = 0.333/2.0
	#plt.figure(fig)
	for j in range(100):
		for i in range(0,9): #(8,-1,-1):
			plt.clf()
			for f in range(10):#96):
				blnk[7:18,(f*14+7):(f*14+18)] = filters[f,i,:,:]
			mi(blnk,figure_num=fig,img_title=d2s(f))
			plt.pause(0.05)
		blnk *= 0
		blnk[0,0] = -0.333/2.0
		blnk[0,1] = 0.333/2.0
		#mi(blnk,figure_num=fig,img_title=d2s(f))
		plt.pause(0.5)


def view_filters2(solver,fig=1):
	filters = solver.net.params['conv1'][0].data
	blnk = np.zeros((27,27*10))
	blnk[0,0] = -0.333/2.0
	blnk[0,1] = 0.333/2.0

	for f in range(96):
		for i in range(0,9): #(8,-1,-1):
			plt.clf()
			blnk[7:18,(1*14+7):(1*14+18)] = filters[f,i,:,:]
			mi(blnk,figure_num=fig,img_title=d2s(f))
			plt.pause(0.05)
		blnk *= 0
		blnk[0,0] = -0.333/4.0
		blnk[0,1] = 0.333/4.0
		#mi(blnk,figure_num=fig,img_title=d2s(f))
		plt.pause(0.5)


"""
filters = solver.net.params['conv1'][0].data
for i in range(96):
	a=filters[i,:,:,:]
	a=np.transpose(a,(1,2,0))
	a -= a.min()
	a /= a.max()
	plt.clf()
	mi(a,img_title=d2s(i))
	plt.pause(0.5)


"""


