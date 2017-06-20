from kzpy3.caf2.utils.protos import *
"""
from kzpy3.caf2.models.m4d1_lower_field.define import *
"""
#############################################################
#  
model_name = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
purpose = """
A model that looks at lower half of scale 50 BW image sequences,
frame range (-15,-6) to predict steer at frame 0.
tested with jitter, reverse contrast, and noise.
###############################
blobs
('ddata', (1, 9, 50, 144))
('ddata2', (1, 3))
('py_image_data', (1, 9, 50, 144))
('py_target_data', (1, 3))
('conv1', (1, 96, 14, 45))
('conv1_pool', (1, 96, 7, 22))
('conv2', (1, 256, 3, 10))
('conv2_pool', (1, 256, 1, 5))
('ip1', (1, 512))
('ip2', (1, 3))
('euclidian', ())
###############################
params
('conv1', (96, 9, 11, 11))
('conv2', (256, 48, 3, 3))
('ip1', (512, 1280))
('ip2', (3, 512))
###############################
"""

c = """
CAFFE_MODE = 'train'
CAFFE_TRAIN_DATA = opjD('RPi3_data/all_runs_dics/runs_scale_50_BW')
CAFFE_TEST_DATA = opjD('RPi3_data/all_runs_dics/runs_scale_50_BW_test')
CAFFE_FRAME_RANGE = (-15,-6)
USE_REVERSE_CONTRAST = False
USE_BOTTOM_HALF = True
USE_NOISE = True
USE_JITTER = True
jitter = 6
input_size = (1,9,56-jitter,150-jitter)
"""
#copy_from = 'latest'
#
#############################################################
#

exec(c)

n_targets = 3
p = '# ' + model_name + '\n'
p = p + '# ' + time_str()
p = p + '\n# '.join(purpose.split('\n'))
p = p + dummy('py_image_data',input_size)
p = p + dummy('py_target_data',(1,n_targets))
p = p + conv_layer_set(
	c_top='conv1',c_bottom='py_image_data',c_num_output=96,c_group=1,c_kernel_size=11,c_stride=3,c_pad=0,
	p_type='MAX',p_kernel_size=3,p_stride=2,p_pad=0,
	weight_filler_type='gaussian',std=0.1)
p = p + conv_layer_set(
	c_top='conv2',c_bottom='conv1_pool',c_num_output=256,c_group=2,c_kernel_size=3,c_stride=2,c_pad=0,
	p_type='MAX',p_kernel_size=3,p_stride=2,p_pad=0,
	weight_filler_type='gaussian',std=0.1)
p = p + ip_layer_set('ip1','conv2_pool',512,'xavier')
p = p + ip_layer_set('ip2','ip1',n_targets,'xavier')
p = p + euclidean('euclidean','ip2','py_target_data')
#
#############################################################
#
s = solver_proto(model_name)
#
#############################################################

#############################################################
#
tmp_path = opjh('kzpy3/caf2/models',model_name,'tmp')
#list_of_strings_to_txt_file(opj(tmp_path,'__info__.py'),c.split('\n'))
s_path = opj(tmp_path,'solver.prototxt')
p_path = opj(tmp_path,'train_val.prototxt')
list_of_strings_to_txt_file(p_path,p.split('\n'))
print('Saved '+p_path)
list_of_strings_to_txt_file(s_path,s.split('\n'))
print('Saved '+s_path)
del s,c,p,s_path,p_path
#
#############################################################
#
if True:
	from kzpy3.caf2.utils.train import *
	solver = setup_solver(model_name)
#
#############################################################

blobs = solver.net.blobs
#blobs['py_image_data'].data[:] = np.random.random((1, 9, 50, 144))
# for i in range(9):mi(solver.net.blobs['py_image_data'].data[0,i,:,:]);plt.pause(0.2)
# my_vis_square(solver.net.params['conv1'][0].data)
# solver.net.copy_from('/Users/karlzipser/scratch/caf2_models/m3d31_example_model_iter_2500000.caffemodel')






from kzpy3.caf2.utils.data import *

all_runs_dic = load_obj(opjD('RPi3_data/all_runs_dics/runs_scale_50_BW_test'))
steer_bins = get_steer_bins(all_runs_dic)
frame_range = (-15,-6)

def process_frames(frame_names):
    img_lst = []
    reverse_contrast = False
    if USE_JITTER:
        jitx = np.floor(np.random.random()*jitter)
        jity = np.floor(np.random.random()*jitter)
    if USE_REVERSE_CONTRAST:
        if np.random.random() < 0.5:
            reverse_contrast = True
    for f in frame_names:
        img = imread(f)/255.0-0.5
        if reverse_contrast:
            img = -img
        if USE_BOTTOM_HALF:
            img = img[np.floor(shape(img)[0]/2):,:]
        if USE_JITTER:
            img = img[jity:(jity+input_size[2]),jitx:(jitx+input_size[3])]
        img_lst.append(img)
    if len(img_lst) == 1 and len(np.shape(img_lst[0])) == 3:
        img = img_lst[0]
        img_lst = [img[:,:,0],img[:,:,1],img[:,:,2]]
    return img_lst

def get_caffe_input_target(steer_bins,all_runs_dic,frame_range):
    b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
    b_,r_,n_,steer_,frames_to_next_turn_,rps_,noise_frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
    img_lst = process_frames(frame_names)
    noise_img_lst = process_frames(noise_frame_names)
    noise_p1 = 0.33333
    noise_p2 = np.random.random()*noise_p1
    for i in range(len(img_lst)):
        img_lst[i] = (1.0-noise_p2)*img_lst[i] + noise_p2*noise_img_lst[i]
    S = steer/200.0 + 0.5
    assert(S>=0)
    assert(S<=1)
    F = frames_to_next_turn/45.0
    F = min(F,1.0)
    assert(F>=0)
    assert(F<=1)
    R = rps/75.0
    R = min(R,1.0)
    assert(R>=0)
    assert(R<=1)
    return img_lst,[S,0,0]

def get_caffe_input_target(steer_bins,all_runs_dic,frame_range):
    b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
    img_lst = process_frames(frame_names)
    S = steer/200.0 + 0.5
    assert(S>=0)
    assert(S<=1)
    F = frames_to_next_turn/45.0
    F = min(F,1.0)
    assert(F>=0)
    assert(F<=1)
    R = rps/75.0
    R = min(R,1.0)
    assert(R>=0)
    assert(R<=1)
    return img_lst,[S,0,0]


def step_train(solver=solver,steer_bins=steer_bins,all_runs_dic=all_runs_dic):
	img_lst,target_lst = get_caffe_input_target(steer_bins,all_runs_dic,frame_range)
	for i in range(len(img_lst)):
		solver.net.blobs['py_image_data'].data[0,i,:,:] = img_lst[i]
	for i in range(len(target_lst)):
		solver.net.blobs['py_target_data'].data[0,i] = target_lst[i]
	solver.step(1)#solver.net.forward()#
	return solver.net.blobs['py_target_data'].data[0,:],solver.net.blobs['ip2'].data[0,:]


def my_scatter(x,y,xmin,xmax,fig_wid,fig_name):
	plt.figure(fig_name,(fig_wid,fig_wid))
	plt.clf()
	plt.plot(x,y,'bo')
	plt.title(np.corrcoef(x,y)[0,1])
	plt.xlim(xmin,xmax)
	plt.ylim(xmin,xmax)

def test_solver(n=1000):
	t0 = time.time()
	t_lst = []
	o_lst = []
	for i in range(n):
		t,o = step_train()
		t_lst.append(t[0])
		o_lst.append(o[0])
	print(dp(n/(time.time()-t0)))
	my_scatter(t_lst,o_lst,0,1,5,'test_solver test data normal contrast only')

def train_solver(solver=solver):
	for i in range(1000000):
		t = time.time()
		for j in range(1000):
			step_train()
		print 1000.0/(time.time()-t)

def look_at_frames(solver):
	for i in range(shape(solver.net.blobs['py_image_data'].data)[1]):
		mi(solver.net.blobs['py_image_data'].data[0,i,:,:],1,img_title=d2s(i))
		plt.pause(0.2)


