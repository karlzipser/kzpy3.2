from Paths_Module import *
exec(identify_file_str)

for _name in [
	'reject_run',
	'left',
	'out1_in2',
	'dic',
	'name',
	'test',
	'dic_type',
	'purpose',
	'batch_size',
	'net',
	'camera_data',
	'metadata',
	'target_data',
	'names',
	'states',
	'loss_dic',
	'train',
	'val',
	'ctr',
	'all_steer',
	'epoch_counter',
	'get_data',
	'next',
	'run_code',
	'seg_num',
	'offset',
	'all_data_moment_id_codes',
	'left',
	'right',
	'fill',
	'clear',
	'forward',
	'backward',
	'display',
	'GPU',
	'BATCH_SIZE',
	'DISPLAY',
	'VERBOSE',
	'LOAD_ARUCO',
	'BAIR_CAR_DATA_PATH',
	'RESUME',
	'IGNORE',
	'REQUIRE_ONE',
	'USE_STATES',
	'N_FRAMES',
	'N_STEPS',
	'STRIDE',
	'save_net_timer',
	'print_timer',
	'epoch_timer',
	'WEIGHTS_FILE_PATH',
	'SAVE_FILE_NAME',
	'mode',
	'criterion',
	'optimizer',
	'data_ids',
	'data_moment',
	'racing',
	'caffe',
	'follow',
	'direct',
	'play',
	'furtive',
	'labels',
	'LCR',
	'trial_loss_record',
	'loss',
	'outputs',
	'print_now',
	'network',
	'metadata',
	'steer',
	'motor',
	'data'
	]:exec(d2n(_name,'=',"'",_name,"'"))

#

#EOF