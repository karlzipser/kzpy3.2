from kzpy3.Train_app.Train_SqueezeNet_lidar0.Paths_Module import *
exec(identify_file_str)

spd2s('REMEMBER ulimit -Sn 65000')

import resource
soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
print 'Soft limit is ', soft
#assert(soft>=65000)


P = {}

P['start time'] = time_str()

P['max_num_runs_to_open'] = 300
"""
opjm('rosbags/bdd_car_data_18July_to_18Sept2018_lrc/locations'),
opjm('rosbags1/bdd_car_data_late_Sept2018_lrc/locations'),
#opjm('2_TB_Samsung_n2_/bair_car_data_Main_Dataset_part1/locations'),#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
opjD('bdd_car_data_July2017_LCR/locations'),
opjm('preprocessed_1b/model_car_data_June2018_LCR/locations'),
opjm('preprocessed_1b/model_car_data_July2018_lrc/locations'),

P['experiments_folders'] = [
#	opjm('preprocessed_5Oct2018_500GB/bdd_model_car_data_early_8Oct2018_lrc_LIDAR/locations'),#
#	opjm('preprocessed_5Oct2018_500GB/bdd_model_car_data_late_Sept_early_Oct2018_lrc/locations'),
#	opjm('preprocessed_5Oct2018_500GB/bdd_car_data_late_Sept2018_lrc/locations'),
#	opjm('preprocessed_5Oct2018_500GB/bdd_car_data_18July_to_18Sept2018_lrc/locations'),
#	opjm('preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations'),
#	opjm('preprocessed_5Oct2018_500GB/model_car_data_June2018_LCR/locations'),
#	opjD('bdd_car_data_July2017_LCR/locations'),
	opjD('temp_data/locations')
]

	opjm('preprocessed_5Oct2018_500GB/bdd_car_data_18July_to_18Sept2018_lrc/locations'),
	opjm('preprocessed_5Oct2018_500GB/bdd_car_data_late_Sept2018_lrc/locations'),
	#opjm('2_TB_Samsung_n2_/bair_car_data_Main_Dataset_part1/locations'),#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	
	opjm('preprocessed_5Oct2018_500GB/model_car_data_June2018_LCR/locations'),
	opjm('preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations'),
	opjm('preprocessed_5Oct2018_500GB/bdd_model_car_data_late_Sept_early_Oct2018_lrc/locations'),
]
"""





import kzpy3.Data_app.classify_data as classify_data
P['experiments_folders'] = []
classify_data.find_locations(opjm("1_TB_Samsung_n1"),P['experiments_folders'])
if False: # this is only for preparing data, not for training.
	import kzpy3.Data_app.make_data_moments_dics as make_data_moments_dics
	for locations_path in P['experiments_folders']:
		make_data_moments_dics.make_data_moments_dics(locations_path)
P['experiments_folders'] = list(set(P['experiments_folders']))



P['GPU'] = 0 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
P['BATCH_SIZE'] = 64
P['REQUIRE_ONE'] = []
P['NETWORK_OUTPUT_FOLDER'] = opjD('net_lidar0')#opjD('net_16Aug2018')#opjD('net_16Aug2018')# #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
P['SAVE_FILE_NAME'] = 'net'
P['save_net_timer'] = Timer(60*30)
P['print_timer'] = Timer(10)
P['frequency_timer'] = Timer(10.0)
P['TRAIN_TIME'] = 60*5.0
P['VAL_TIME'] = 60*1.0
P['RESUME'] = False
if P['RESUME']:
    P['INITIAL_WEIGHTS_FOLDER'] = opj(P['NETWORK_OUTPUT_FOLDER'],'weights')
    P['WEIGHTS_FILE_PATH'] = most_recent_file_in_folder(P['INITIAL_WEIGHTS_FOLDER'],['net'],[])	
P['reload_image_file_timer'] = Timer(5*60)
P['loss_timer'] = Timer(60*10/10)
P['LOSS_LIST_N'] = 30
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
P['Depth_images_path'] = opjD('Depth_images')
P['run_name_to_run_depth_images_path'] = {}

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
				#e='/media/karlzipser/1_TB_Samsung_n1/tu_15to16Oct2018/locations/local/left_right_center'
				for r in sggo(e,'h5py','*'):
					run_name = fname(r)
					run_depth_images_path = opj(P['Depth_images_path'],d2p(run_name,'Depth_images','with_flip','with_left_ts','h5py'))
					if len(sggo(run_depth_images_path)) == 1:
						if True:#run_name not in P['run_name_to_run_path']:
							P['run_name_to_run_path'][run_name] = r
							P['run_name_to_run_depth_images_path'][run_name] = run_depth_images_path
							cg("Using",run_name)
					else:
						cb("Not using",run_name,"because",fname(run_depth_images_path),"not found.")
			#break
		#break
				

	spd2s("len(P['data_moments_indexed']) =",len(P['data_moments_indexed']))
	spd2s("len(P['heading_pause_data_moments_indexed']) =",len(P['heading_pause_data_moments_indexed']))
	#raw_enter()








def get_Data_moment(dm=None,FLIP=None):
	try:
		#if dm['run_name'] in P['lacking runs']:
		#	return False
		Data_moment = {}
		left_index = dm['left_ts_index'][1]
		steer_len = len(P['Loaded_image_files'][dm['run_name']]['left_timestamp_metadata']['steer'])
		data_len = min(steer_len - left_index,90)
		behavioral_mode = dm['behavioral_mode']
		if True:
			if steer_len - left_index < 90:
				print steer_len - left_index

		for q in ['steer','motor','gyro_heading_x','encoder_meo']:	
			Data_moment[q] = zeros(90) + 49
			if q not in P['Loaded_image_files'][dm['run_name']]['left_timestamp_metadata']:
				pd2s(dm['run_name'],'lacks',q)
				P['lacking runs'][dm['run_name']] = q
				return False
			if behavioral_mode != 'heading_pause':
				Data_moment[q][:data_len] = P['Loaded_image_files'][dm['run_name']]['left_timestamp_metadata'][q][left_index:left_index+data_len]

		if True:
			past_data_len = 3*23 # constrained by metadate image size
			past = '_past'
			for q in ['encoder']:#'steer','motor','acc_x','acc_y','acc_z','gyro_x','gyro_y','gyro_z','encoder']:	
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


		"""
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
			for q in ['steer','motor','gyro_heading_x','encoder_meo']:	
				#Data_moment[q+past] = zeros(past_data_len)
				Data_moment[q] = zeros(90) + 49
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
		"""			

		if FLIP:
			Data_moment['steer'] = 99 - Data_moment['steer']
			Data_moment['gyro_heading_x'] = -1.0*Data_moment['gyro_heading_x']


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



		#tl0 = dm['left_ts_index'][0]

		#il0 = dm['left_ts_index'][1]

		run_name


		if FLIP:
			F = P['Loaded_image_files'][Data_moment['name']]['depth']['log_flip']
		else:
			F = P['Loaded_image_files'][Data_moment['name']]['depth']['log']

		il0 = P['Loaded_image_files'][Data_moment['name']]['depth']['left_to_lidar_index'][left_index]

		Data_moment['lidar'] = []

		Data_moment['left_index'] = left_index

		Data_moment['flip'] = FLIP

		if il0+3 < len(F):
			#cr('il0+3 < len(F),',il0+3,'<',len(F),' if True')
			img = []
			for i in [-2,-1,0]:
				img.append(F[il0+i][:])
			img = na(img)
			Data_moment['lidar'] = img
		else:
			cr('il0+3 < len(F),',il0+3,'<',len(F),' NOT TRUE!')
			return False


		return Data_moment
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		CS_('Exception!',exception=True,newline=False)
		CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
		return False









#EOF