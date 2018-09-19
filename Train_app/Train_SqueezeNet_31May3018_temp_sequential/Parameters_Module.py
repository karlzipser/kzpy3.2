from Paths_Module import *
exec(identify_file_str)

if using_linux():
	spd2s('REMEMBER ulimit -Sn 65000')
	import resource
	soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
	print 'Soft limit is ', soft
	assert(soft>=65000)


P = {}

P['start time'] = time_str()

P['max_num_runs_to_open'] = 300

P['experiments_folders'] = [
	#opjm('2_TB_Samsung_n2_/bair_car_data_Main_Dataset_part1/locations'),#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	#opjD('bdd_car_data_July2017_LCR/locations'),
	#opjm('preprocessed_1b/model_car_data_June2018_LCR/locations'),
	#opjm('preprocessed_1b/model_car_data_July2018_lrc/locations'),
	opjm("transfer/model_car_data_July2018_lrc/locations"),
]

P['aruco_experiments_folders'] = []#[opjD('all_aruco_reprocessed')]#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


P['GPU'] = 0 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
P['BATCH_SIZE'] = 64
P['REQUIRE_ONE'] = []
P['NETWORK_OUTPUT_FOLDER'] = opjk('Train_app','Train_SqueezeNet_31May3018_temp_sequential','__local__') #  'net_7Sept2018')#opjD('net_16Aug2018')#opjD('net_16Aug2018')# #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
P['SAVE_FILE_NAME'] = 'net'
P['save_net_timer'] = Timer(60*30)
P['print_timer'] = Timer(30)
P['frequency_timer'] = Timer(10.0)
P['TRAIN_TIME'] = 60*5.0
P['VAL_TIME'] = 60*1.0
P['RESUME'] = True
if P['RESUME']:
    P['INITIAL_WEIGHTS_FOLDER'] = opj(P['NETWORK_OUTPUT_FOLDER'],'weights')
    P['WEIGHTS_FILE_PATH'] = most_recent_file_in_folder(P['INITIAL_WEIGHTS_FOLDER'],['net'],[])	
P['reload_image_file_timer'] = Timer(5*60)
P['loss_timer'] = Timer(60*10/10)
P['LOSS_LIST_N'] = 3
P['run_name_to_run_path'] = {}
P['data_moments_indexed'] = []
P['heading_pause_data_moments_indexed'] = []
P['Loaded_image_files'] = {}
P['data_moments_indexed_loaded'] = []
P['behavioral_modes_no_heading_pause'] = ['direct','follow','furtive','play','left','right']
# note, 'center' is not included in P['behavioral_modes_no_heading_pause'] because 'center' is converted to 'direct' below.
P['behavioral_modes'] = P['behavioral_modes_no_heading_pause']+['heading_pause']
P['current_batch'] = []
P['DISPLAY_EACH'] = False
P['prediction_range'] = range(1,60,6)
P['gray_out_random_value'] = 0.0
if True:
	for experiments_folder in P['experiments_folders']:
		if fname(experiments_folder)[0] == '_':
			continue
		print experiments_folder
		locations = sggo(experiments_folder,'*')
		for location in locations:
			if fname(location)[0] == '_':
				spd2s('ignoring',location)
				continue
			print location
			b_modes = sggo(location,'*')
			print b_modes
			for e in b_modes:
				if fname(e)[0] == '_':
					continue
				if fname(e) == 'racing':
					continue
				"""
				if fname(e) == 'play':
					continue
				if fname(e) == 'follow':
					continue
				if fname(e) == 'furtive':
					continue
				"""
				spd2s(fname(e))
				_data_moments_indexed = lo(opj(e,'data_moments_dic.pkl'))
				random.shuffle(_data_moments_indexed['train']['low_steer'])
				high_len = len(_data_moments_indexed['train']['high_steer'])
				_data_moments_indexed['train']['low_steer'] = _data_moments_indexed['train']['low_steer'][:high_len]
				for h_l in ['high_steer','low_steer']:
					for _dm in _data_moments_indexed['train'][h_l]:
						_dm['aruco'] = False
						if _dm['behavioral_mode'] == 'center':
							_dm['behavioral_mode'] = 'direct'
						if _dm['motor'] > 53:
							P['data_moments_indexed'].append(_dm)

				for r in sggo(e,'h5py','*'):
					print fname(r)
					assert(fname(r) not in P['run_name_to_run_path'])
					P['run_name_to_run_path'][fname(r)] = r
			#break
		#break
				

	spd2s("len(P['data_moments_indexed']) =",len(P['data_moments_indexed']))
	spd2s("len(P['heading_pause_data_moments_indexed']) =",len(P['heading_pause_data_moments_indexed']))
	#raw_enter()


if True:
	for experiments_folder in P['aruco_experiments_folders']:
		experiments = sggo(experiments_folder,'*')
		ctr = 0
		for experiment in experiments:
			print experiment

			#if 'Smyth' in experiment:
			#	continue
			if fname(experiment)[0] == '_':
				continue
			spd2s(fname(experiment))
			if ctr > 0:
				pd2s(ctr,'ctr>0')
				#break
			ctr += 1
			_data_moments_indexed = lo(opj(experiment,'data_moments_dic.pkl'))

			for behavioral_mode in _data_moments_indexed['train'].keys():
				if behavioral_mode != 'heading_pause':
					car_in_view_ctr = 0
					for _dm in _data_moments_indexed['train'][behavioral_mode]['car_in_view']:
						_dm['behavioral_mode'] = behavioral_mode
						_dm['aruco'] = True
						if _dm['behavioral_mode'] == 'direct':
							if random.random() > 0.5:
								_dm['behavioral_mode'] = 'furtive'
						if _dm['motor'] > 50:
							P['data_moments_indexed'].append(_dm)
							car_in_view_ctr += 1

					car_not_in_view_ctr = 0
					random.shuffle(_data_moments_indexed['train'][behavioral_mode]['car_not_in_view'])
					for _dm in _data_moments_indexed['train'][behavioral_mode]['car_not_in_view']:
						if car_not_in_view_ctr > car_in_view_ctr: #len(_data_moments_indexed['train'][behavioral_mode]['car_in_view']):
							print('ctr2 > car_in_view_ctr>')
							break
						_dm['behavioral_mode'] = behavioral_mode
						_dm['aruco'] = True
						if _dm['behavioral_mode'] == 'direct':
							if random.random() > 0.5:
								_dm['behavioral_mode'] = 'furtive'
						if _dm['motor'] > 50:
							P['data_moments_indexed'].append(_dm)
							car_not_in_view_ctr += 1
					print(car_in_view_ctr,car_not_in_view_ctr)				
				else:
					if _dm['motor'] < 52:
						for _dm in _data_moments_indexed['train'][behavioral_mode]:
							_dm['behavioral_mode'] = random.choice(['direct','follow']) #behavioral_mode
							_dm['aruco'] = True
							_dm['motor'] = 49
							P['data_moments_indexed'].append(_dm)
					else:
						print _dm['motor']

			for r in sggo(experiment,'h5py','*'):
				print fname(r)
				assert(fname(r) not in P['run_name_to_run_path'])
				P['run_name_to_run_path'][fname(r)] = r
			#break
		
				

	spd2s("len(P['data_moments_indexed']) =",len(P['data_moments_indexed']))
	spd2s("len(P['heading_pause_data_moments_indexed']) =",len(P['heading_pause_data_moments_indexed']))








def get_Data_moment(dm=None,FLIP=None):
	try:
		Data_moment = {}
		left_index = dm['left_ts_index'][1]
		steer_len = len(P['Loaded_image_files'][dm['run_name']]['left_timestamp_metadata']['steer'])
		data_len = min(steer_len - left_index,90)
		behavioral_mode = dm['behavioral_mode']
		if True:
			if steer_len - left_index < 90:
				print steer_len - left_index

		for q in ['steer','motor']:	
			Data_moment[q] = zeros(90) + 49
			if behavioral_mode != 'heading_pause':
				Data_moment[q][:data_len] = P['Loaded_image_files'][dm['run_name']]['left_timestamp_metadata'][q][left_index:left_index+data_len]

		if False:
			past_data_len = 3*23 # constrained by metadate image size
			past = '_past'
			for q in ['steer','motor','acc_x','acc_y','acc_z','gyro_x','gyro_y','gyro_z','encoder']:	
				Data_moment[q+past] = zeros(past_data_len)
				if behavioral_mode != 'heading_pause':
					if left_index-past_data_len < 0:
						#CS("left_index-past_data_len < 0:")
						return False
					else:
						pass#print "left_index-past_data_len >= 0:"
					
					Data_moment[q+past][:past_data_len] = P['Loaded_image_files'][dm['run_name']]['left_timestamp_metadata'][q][(left_index-past_data_len):left_index]
					if FLIP:
						if q == 'steer':
							Data_moment[q+past][:past_data_len] = 99-Data_moment[q+past][:past_data_len]
						elif q == 'acc_x' or q == 'gyro_x' or q == 'gyro_y':
							Data_moment[q+past][:past_data_len] = -1*Data_moment[q+past][:past_data_len]
					

		if FLIP:
			Data_moment['steer'] = 99 - Data_moment['steer']


		Data_moment['motor'][Data_moment['motor']<0] = 0
		Data_moment['motor'][Data_moment['motor']>99] = 99
		Data_moment['steer'][Data_moment['steer']<0] = 0
		Data_moment['steer'][Data_moment['steer']>99] = 99


		Data_moment['labels'] = {}
		Data_moment['name'] = dm['run_name']
		
		
		if FLIP:
			if behavioral_mode == 'left':
				behavioral_mode = 'right'
			elif behavioral_mode == 'right':
				behavioral_mode = 'left'

		for b in P['behavioral_modes']:
			Data_moment['labels'][b] = 0
		if behavioral_mode == 'heading_pause':
			behavioral_mode = random.choice(P['behavioral_modes_no_heading_pause'])
		Data_moment['labels'][behavioral_mode] = 1



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
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		CS_('Exception!',exception=True,newline=False)
		CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
		return False









#EOF