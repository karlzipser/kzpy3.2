from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/scratch/y2017/temp9'])
exec(identify_file_str)

for _name in ['first','second','fun2','dic','name','test','dic_type','purpose']:exec(d2n(_name,'=',"'",_name,"'"))


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
	'weights_file_path',
	'save_file_name']:exec(d2n(_name,'=',"'",_name,"'"))



#EOF