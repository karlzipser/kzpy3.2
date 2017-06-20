from kzpy3.caf2.utils.protos import *
from kzpy3.caf2.utils.data import *

"""
from kzpy3.caf2.models.m4d1_deconv_first_attempt.define import *
python kzpy3/caf2/models/m4d1_deconv_first_attempt/define.py

"""
#############################################################
#  
model_name = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
purpose = """
A first attempt at making a conv-deconv network
"""
CAFFE_TRAIN_DATA = opjD('RPi3_data/all_runs_dics/runs_scale_50_BW')
CAFFE_TEST_DATA = opjD('RPi3_data/all_runs_dics/runs_scale_50_BW_test')
CAFFE_FRAME_RANGE = (-9,1)
USE_REVERSE_CONTRAST = False
USE_BOTTOM_HALF = True
USE_NOISE = False
USE_JITTER = True
jitter = 12
input_size = (1,1,56-jitter,150-jitter)
#
#############################################################
#
"""
#
#############################################################
p = '# ' + model_name + '\n'
p = p + '# ' + time_str()
p = p + '\n# '.join(purpose.split('\n'))
p = p + dummy('py_image_data',input_size)
p = p + dummy('py_target_data',input_size)
p = p + conv(top='conv1',bottom='py_image_data',num_output=96,group=1,kernel_size=5,stride=3,pad=(2,0),
    weight_filler_type='gaussian',std=0.1)
p = p + conv(top='conv2',bottom='conv1',num_output=256,group=2,kernel_size=5,stride=3,pad=(1,1),
    weight_filler_type='gaussian',std=0.1)
p = p + deconv('deconv1','conv2',96,1,5,3,(1,1),'gaussian',0.1)
p = p + deconv('deconv2','deconv1',1,1,6,3,(2,0),'gaussian',0.1)

#
#############################################################
#
s = solver_proto(model_name)
#
#############################################################

#############################################################
#
tmp_path = opjh('kzpy3/caf2/models',model_name,'tmp')
s_path = opj(tmp_path,'solver.prototxt')
p_path = opj(tmp_path,'train_val.prototxt')
list_of_strings_to_txt_file(p_path,p.split('\n'))
print('Saved '+p_path)
list_of_strings_to_txt_file(s_path,s.split('\n'))
print('Saved '+s_path)
del s,p,s_path,p_path
#
#############################################################
#
"""
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

all_runs_dic = load_obj(opjD('RPi3_data/all_runs_dics/runs_scale_50_BW'))
steer_bins = get_steer_bins(all_runs_dic)
frame_range = CAFFE_FRAME_RANGE

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
    img_lst = process_frames(frame_names)
    return img_lst[:-1],[img_lst[-1]]


def step_train(solver=solver,steer_bins=steer_bins,all_runs_dic=all_runs_dic):
	img_lst,target_lst = get_caffe_input_target(steer_bins,all_runs_dic,frame_range)
	for i in range(len(img_lst)):
		solver.net.blobs['py_image_data'].data[0,i,:,:] = img_lst[i]
	for i in range(len(target_lst)):
		solver.net.blobs['py_target_data'].data[0,i] = target_lst[i]
	solver.step(1)#solver.net.forward()#


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


