from kzpy3.utils2 import *
exec(identify_file_str)

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

P = {}
P[GPU] = 1
P[BATCH_SIZE] = 100
P[DISPLAY] = True
P[VERBOSE] = True
P[LOAD_ARUCO] = False
P[BAIR_CAR_DATA_PATH] = opjD('bdd_car_data_July2017_LCR')
P[RESUME] = False
if RESUME:
    P[weights_file_path] = most_recent_file_in_folder(opjD(),['save_file'],['infer'])
P[IGNORE] = ['reject_run','left','out1_in2']#,'Smyth','racing','local','Tilden','campus']
P[REQUIRE_ONE] = []
P[USE_STATES] = [1,3,5,6,7]
P[N_FRAMES] = 2
P[N_STEPS] = 10
P[STRIDE] = 3 # multiply by N Steps in order to have fixed number of steps reach further in time.
# STRIDE is not fully controlled here, there must be changes in _data_into_batch().
P[save_net_timer] = Timer(60*30)
P[print_timer] = Timer(15)
P[epoch_timer] = Timer(15)
P[save_file_name] = 'save_file_LCR_'




#EOF