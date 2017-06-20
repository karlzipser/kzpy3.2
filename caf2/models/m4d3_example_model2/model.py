"""
from kzpy3.caf2.models.m4d3_example_model2.define import *
python kzpy3/caf2/models/m4d3_example_model2/model.py
"""
from kzpy3.caf2.utils.protos import *
from kzpy3.caf2.utils.train import *
from kzpy3.caf2.utils.data import *
from kzpy3.caf2.utils.data import *
dis = {}
#
#############################################################
# 
dis['model_name'] = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
dis['purpose'] = """
This should be a basic model structure to solidify caf2 format and include:
    --define
    --train
    --test
    --deploy
Each should be set up to be run from the command line. This is a bit tricky, but important.
"""
#
#############################################################
#
def define():
	unix('mkdir -p scratch/caf2_models/'+dis['model_name'])
	dis['input_size'] = (1,1,90,160)
	dis['n_targets'] = 1
	dis['CAFFE_TRAIN_DATA'] = 'random'
	dis['CAFFE_TEST_DATA'] = 'random'
	dis['CAFFE_FRAME_RANGE'] = (0,1)
	p = '# ' + dis['model_name'] + '\n'
	p = p + '# ' + time_str()
	p = p + '\n# '.join(dis['purpose'].split('\n'))

	p = p + dummy('py_image_data',dis['input_size'])
	p = p + dummy('py_target_data',(1,dis['n_targets']))
	p = p + conv_layer_set(
		c_top='conv1',c_bottom='py_image_data',c_num_output=96,c_group=1,c_kernel_size=11,c_stride=3,c_pad=0,
		p_type='MAX',p_kernel_size=3,p_stride=2,p_pad=0,
		weight_filler_type='gaussian',std=0.1)
	p = p + conv_layer_set(
		c_top='conv2',c_bottom='conv1_pool',c_num_output=256,c_group=2,c_kernel_size=3,c_stride=2,c_pad=0,
		p_type='MAX',p_kernel_size=3,p_stride=2,p_pad=0,
		weight_filler_type='gaussian',std=0.1)
	p = p + ip_layer_set('ip1','conv2_pool',512,'xavier')
	p = p + ip_layer_set('ip2','ip1',dis['n_targets'],'xavier')
	p = p + euclidean('euclidean','ip2','py_target_data')

	s = solver_proto(dis['model_name'])

	tmp_path = opjh('kzpy3/caf2/models',dis['model_name'],'tmp')
	unix('mkdir -p '+tmp_path)
	s_path = opj(tmp_path,'solver.prototxt')
	p_path = opj(tmp_path,'train_val.prototxt')
	list_of_strings_to_txt_file(p_path,p.split('\n'))
	print('Saved '+p_path)
	list_of_strings_to_txt_file(s_path,s.split('\n'))
	print('Saved '+s_path)
	unix('mkdir -p scratch/caf2_models/'+dis['model_name'])
	del s,p,s_path,p_path
#
#############################################################
#
def collect_train_data(data_path=""):
	dis['all_runs_dic'] = []#load_obj(opjD('RPi3_data/all_runs_dics/runs_scale_50_BW_test'))
	dis['steer_bins'] = []#get_steer_bins(all_runs_dic)

def collect_test_data(data_path=""):
	dis['all_runs_dic'] = []#load_obj(opjD('RPi3_data/all_runs_dics/runs_scale_50_BW_test'))
	dis['steer_bins'] = []#get_steer_bins(all_runs_dic)

def process_frames(frame_names):
	pass

def get_caffe_input_target(steer_bins,all_runs_dic,frame_range):
    pass
#
#
#############################################################



