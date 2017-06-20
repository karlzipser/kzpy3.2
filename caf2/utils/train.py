"""
ipy
import kzpy3.caf2.models.y2016m3.zeroth_model.define
from kzpy3.caf2.utils.train import *
solver = setup_solver('y2016m3.zeroth_model')
"""

from kzpy3.utils import *
import caffe

def setup_solver(model_name,training_path='default',solver_name='solver.prototxt'):
	if training_path == 'default':
		training_path=opjh('kzpy3/caf2/models',model_name,'tmp')
	exec('import '+'kzpy3.caf2.models.'+model_name)
	solver = caffe.SGDSolver(opj(training_path,solver_name))
	show_solver(solver)
	if host_name == 'redwood2':
		caffe.set_device(0)
		caffe.set_mode_gpu()
		print("************** using GPU *************")
	return solver

def step_train(solver):
	solver.step(1)
	return solver.net.blobs['py_target_data'].data[0,:],solver.net.blobs['ip2'].data[0,:]

def step_test(solver):
	solver.net.forward()
	return solver.net.blobs['py_target_data'].data[0,:],solver.net.blobs['ip2'].data[0,:]

def test_solver(solver,n,nt=10):
	t0 = time.time()
	t_lst = []
	o_lst = []
	for i in range(n/nt):
		t = time.time()
		for j in range(nt):
			t,o = step_test(solver)
			t_lst.append(t[0])
			o_lst.append(o[0])
		print nt/(time.time()-t)
	print(dp(n/(time.time()-t0)))
	#my_scatter(t_lst,o_lst,0,1,5,'test_solver test data normal contrast only')

def train_solver(solver,n,nt=10):
	for i in range(n/nt):
		t = time.time()
		for j in range(nt):
			step_train(solver)
		print nt/(time.time()-t)

def show_solver(solver):
	print('###############################')
	print('blobs')
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	print('###############################')
	print('params')
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	print('###############################')

def safe_solver_step(solver):
	while True:
		try:
			solver.step(10000)
			for k in solver.net.blobs.keys():
				print (k, solver.net.blobs[k].data.max())
		except Exception, e:
			print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
			print e
			print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

def my_vis_square(data,padsize=5,padval=0,fig_num='my_vis_square'):
	data = data.copy()
	data = z2o(data)
	n = int(np.ceil(np.sqrt(data.shape[0])))
	fx = np.shape(data)[2]
	fz = np.shape(data)[1]
	img = np.zeros((padsize+(padsize+fx)*n,padsize+(padsize+fx)*n))+0.5
	for x in range(n):
		for y in range(n):
			if y+x*n < data.shape[0]:
				img[(padsize*(1+x)+(x*(fx))):(padsize*(1+x)+((x+1)*fx)),(padsize*(1+y)+(y*fx)):(padsize*(1+y)+((y+1)*fx))] = data[y+x*n,0,:,:]
	mi(img,fig_num)

def scp_weights_from_redwood2(model_path):
	unix(d2s("""scp kzipser@redwood2.dyn.berkeley.edu:'""" + model_path + """' ~/Desktop""" ))

def test_solver_old(solver,n,fig=100):
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

def my_vis_square(solver,layer_name, padsize=5, padval=0.5):
	data = solver.net.params[layer_name][0].data.copy()
	data = z2o(data)
	n = int(np.ceil(np.sqrt(data.shape[0])))
	fx = np.shape(data)[2]
	fz = np.shape(data)[1]
	img = np.zeros((padsize+(padsize+fx)*n,padsize+(padsize+fx)*n))+padval
	for x in range(n):
		for y in range(n):
			if y+x*n < data.shape[0]:
				img[(padsize*(1+x)+(x*(fx))):(padsize*(1+x)+((x+1)*fx)),(padsize*(1+y)+(y*fx)):(padsize*(1+y)+((y+1)*fx))] = data[y+x*n,0,:,:]
	mi(img,layer_name)

def look_at_frames(solver,layer='py_image_data'):
	for i in range(shape(solver.net.blobs[layer].data)[1]):
		mi(solver.net.blobs[layer].data[0,i,:,:],1,img_title=d2s(i))
		plt.pause(0.2)

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

def load_latest(solver,model_name,model_path=opjh('scratch/caf2_models'),data_type='.caffemodel'):
	_,l_ = dir_as_dic_and_list(opj(model_path,model_name))
	l = []
	for m in l_:
		if data_type in m:
			l.append(m)
	m = opj(model_path,model_name,l[-1])
	print('Reading from:\n'+opj(model_path,model_name,l[-1]))
	solver.net.copy_from(m)
	return solver

def scp_latest(model_name,model_path=opj('scratch/caf2_models'),user_host='kzipser@redwood2.dyn.berkeley.edu'):
	l = unix('ssh '+user_host+' ls '+model_path+'/'+model_name+'/*.caffemodel')
	f = sorted(l,key=natural_keys)[-1]
	unix('mkdir -p '+opj(model_path,model_name))
	unix("""scp """+user_host+""":'"""+f+"""' """+opjh(model_path,model_name))


"""
#####################
solver.prototxt file
train_val.prototxt file
model name: this will determine all file names
layer module
trained model files, appropriate directories 
I find that deep directory structures are hard to deal with, better to have just model name folders
#####################

"""


