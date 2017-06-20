from kzpy3.caf2.utils.protos import *
"""
from kzpy3.caf2.models.<MODEL_NAME>.define import *
"""
#############################################################
#  
model_name = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
purpose = """
Test the ability of my new wrapper system to generate and train models.
I've been working on getting everything directed from a single file.
###############################
blobs
('ddata', (1, 9, 56, 150))
('ddata2', (1, 3))
('py_image_data', (1, 9, 56, 150))
('py_target_data', (1, 3))
('conv1', (1, 96, 16, 47))
('conv1_pool', (1, 96, 8, 23))
('conv2', (1, 256, 2, 7))
('conv2_pool', (1, 256, 1, 3))
('ip1', (1, 512))
('ip2', (1, 3))
('euclidian', ())
###############################
params
('conv1', (96, 9, 11, 11))
('conv2', (256, 48, 5, 5))
('ip1', (512, 768))
('ip2', (3, 512))
###############################
"""

c = """
CAFFE_MODE = 'train'
CAFFE_TRAIN_DATA = opjD('RPi3_data/all_runs_dics/runs_scale_50_BW')
CAFFE_TEST_DATA = opjD('RPi3_data/all_runs_dics/runs_scale_50_BW_test')
CAFFE_FRAME_RANGE = (-15,-6)
USE_REVERSE_CONTRAST = True
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
p = p + dummy('ddata',input_size)
p = p + dummy('ddata2',(1,n_targets))
for phase in ['TRAIN','TEST']:
	p = p + python('py_image_data','ddata','caf2_layers','SimpleLayer4_'+phase,phase)
	p = p + python('py_target_data','ddata2','caf2_layers','SimpleLayer5_'+phase,phase)
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
p = p + euclidian('euclidian','ip2','py_target_data')
#
#############################################################
#
s = solver_proto(model_name)
#
#############################################################

#############################################################
#
list_of_strings_to_txt_file(opjh('kzpy3/caf2/tmp/__info__.py'),c.split('\n'))
s_path = opjh('kzpy3/caf2/tmp/solver.prototxt')
p_path = opjh('kzpy3/caf2/tmp/train_val.prototxt')
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

# for i in range(9):mi(solver.net.blobs['py_image_data'].data[0,i,:,:]);plt.pause(0.2)
# my_vis_square(solver.net.params['conv1'][0].data)
