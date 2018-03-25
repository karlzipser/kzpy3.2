from Paths_Module import *
exec(identify_file_str)

spd2s('REMEMBER ulimit -Sn 65000')

import resource
soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
print 'Soft limit is ', soft
assert(soft>=65000)


P = {}
P['max_num_runs_to_open'] = 300
P['experiments_folder'] = '/home/karlzipser/Desktop/all_aruco_reprocessed'

P['GPU'] = 1
P['BATCH_SIZE'] = 512
P['REQUIRE_ONE'] = []
P['USE_STATES'] = [1,3,5,6,7]
P['N_FRAMES'] = 2
P['N_STEPS'] = 10
P['STRIDE'] = 9#3 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
P['NETWORK_OUTPUT_FOLDER'] = opjD('net_indoors')
P['SAVE_FILE_NAME'] = 'net'
P['save_net_timer'] = Timer(60*20)
P['print_timer'] = Timer(10)
P['frequency_timer'] = Timer(10.0)
P['TRAIN_TIME'] = 60*10.0
P['VAL_TIME'] = 60*1.0
P['RESUME'] = True
if P['RESUME']:
    P['INITIAL_WEIGHTS_FOLDER'] = opj(P['NETWORK_OUTPUT_FOLDER'],'weights')
    P['WEIGHTS_FILE_PATH'] = most_recent_file_in_folder(P['INITIAL_WEIGHTS_FOLDER'],['net'],[])	
P['reload_image_file_timer'] = Timer(1*60)
P['loss_timer'] = Timer(60*1/10)
P['LOSS_LIST_N'] = 3000
P['run_name_to_run_path'] = {}
P['data_moments_indexed'] = []
P['heading_pause_data_moments_indexed'] = []
P['Loaded_image_files'] = {}
P['data_moments_indexed_loaded'] = []
P['behavioral_modes'] = ['follow','direct']


if True:
	for e in sggo(P['experiments_folder'],'*'): #________________________________!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		e = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_15Sept2017_circle'
		print e
		if fname(e)[0] == '_':
			spd2s('Ignoring',e)
			continue #________________________________!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		_data_moments_indexed = lo(opj(e,'data_moments_indexed.pkl'))
		for _dm in _data_moments_indexed:
			if _dm['other_car_in_view'] == True:
				P['data_moments_indexed'].append(_dm)
		d = lo(opj(e,'heading_pause_data_moments_indexed.pkl'))
		P['heading_pause_data_moments_indexed'] += d
		for r in sggo(e,'h5py','*'):
			assert(fname(r) not in P['run_name_to_run_path'])
			P['run_name_to_run_path'][fname(r)] = r
		break
	spd2s("len(P['data_moments_indexed']) =",len(P['data_moments_indexed']))
	spd2s("len(P['heading_pause_data_moments_indexed']) =",len(P['heading_pause_data_moments_indexed']))


from kzpy3.vis2 import *
def get_Data_moment(dm=None,FLIP=None):
	Data_moment = {}
	left_index = dm['left_ts_index'][1]
	Data_moment['steer'] = zeros(90) + dm['steer']#P['Loaded_image_files'][dm['run_name']]['left_timestamp_metadata']['steer'][left_index:left_index+90] #zeros(90) + dm['steer']
	#clf();plot(Data_moment['steer']);spause()
	#raw_enter()
	if FLIP:
		Data_moment['steer'] = 99 - Data_moment['steer']
	new_motor = dm['motor']
	new_motor -= 49
	new_motor = max(0,new_motor)
	new_motor *= 7.0
	Data_moment['motor'] = zeros(90) + new_motor
	Data_moment['labels'] = {}
	for l in ['direct','follow']:
		Data_moment['labels'][l] = 0
	Data_moment['name'] = dm['run_name']
	#print dm['run_name'],P['Loaded_image_files'][dm['run_name']]['left_timestamp_metadata']['steer'][5000]
	behavioral_mode = dm['behavioral_mode']
	if behavioral_mode == 'Direct_Arena_Potential_Field':
		Data_moment['labels']['direct'] = 1
	elif behavioral_mode == 'Follow_Arena_Potential_Field':
		Data_moment['labels']['follow'] = 1



	tl0 = dm['left_ts_index'][0]; il0 = dm['left_ts_index'][1]
	tr0 = dm['right_ts_index'][0]; ir0 = dm['right_ts_index'][1]


	if FLIP:
		F = P['Loaded_image_files'][Data_moment['name']]['flip']
	else:
		F = P['Loaded_image_files'][Data_moment['name']]['normal']

	Data_moment['left'] = {}
	Data_moment['right'] = {}

	if not FLIP:
		if il0+1 < len(F['left_image']['vals']) and ir0+1 < len(F['right_image']['vals']):
			Data_moment['left'][0] = F['left_image']['vals'][il0]
			Data_moment['right'][0] = F['right_image']['vals'][ir0]
			Data_moment['left'][1] = F['left_image']['vals'][il0+1] # note, ONE frame
			Data_moment['right'][1] = F['right_image']['vals'][ir0+1]
		else:
			spd2s('if il0+1 < len(F[left_image][vals]) and ir0+1 < len(F[right_image][vals]): NOT TRUE!')
			return False
	else:
		if il0+1 < len(F['left_image_flip']['vals']) and ir0+1 < len(F['right_image_flip']['vals']):
			Data_moment['right'][0] = F['left_image_flip']['vals'][il0]
			Data_moment['left'][0] = F['right_image_flip']['vals'][ir0]
			Data_moment['right'][1] = F['left_image_flip']['vals'][il0+1]
			Data_moment['left'][1] = F['right_image_flip']['vals'][ir0+1]
		else:
			spd2s('if il0+1 < len(F[left_image_flip][vals]) and ir0+1 < len(F[right_image_flip][vals]): NOT TRUE!')
			return False
	return Data_moment










#EOF