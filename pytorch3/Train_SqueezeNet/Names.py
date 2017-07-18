from Paths import *
exec(identify_file_str)

for _name in ['dic','name','test','dic_type','purpose',
	'batch_size','net','camera_data','metadata','target_data','names','states',
	'train_los_dic','train','val','ctr','all_steer','epoch_counter','get_data','next','run_code','seg_num','offset']:
	exec(d2n(_name,'=',"'",_name,"'"))

for _name in [
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
	'SAVE_FILE_NAME']:exec(d2n(_name,'=',"'",_name,"'"))



#EOF