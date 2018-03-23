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
P['save_net_timer'] = Timer(60*2)
P['print_timer'] = Timer(10)
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



if True:
	for e in sggo(P['experiments_folder'],'*'): #________________________________!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		#if True:
		#e = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_15Sept2017_circle'
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

		#break


	spd2s("len(P['data_moments_indexed']) =",len(P['data_moments_indexed']))
	spd2s("len(P['heading_pause_data_moments_indexed']) =",len(P['heading_pause_data_moments_indexed']))














#EOF