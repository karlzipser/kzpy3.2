from Paths_Module import *
exec(identify_file_str)

spd2s('REMEMBER ulimit -Sn 65000')

import resource
soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
print 'Soft limit is ', soft
assert(soft>=65000)


P = {}
P['ABORT'] = False

################################################################
#
P['use_LIDAR'] = True
P['lidar_only'] = True
P['GPU'] = 1
#
################################################################

#P['LIDAR_path'] =                     opjD('Depth_images.log.resize.flip.left_ts')
P['LIDAR_path'] = opjm('1_TB_Samsung_n1','_.Depth_images.log.resize.flip.left_ts')
P['LIDAR_extension'] = ".Depth_image.log.resize.flip.with_left_ts.h5py"

P['start time'] = time_str()
P['start time numeric'] = time.time()

P['max_num_runs_to_open'] = 300
"""
P['experiments_folders'] = [
	opjm('rosbags/first_lidar_runs_SeptOct2018_lrc/locations'),
	opjm('preprocessed_5Oct2018_500GB/bdd_car_data_18July_to_18Sept2018_lrc/locations'),
	opjm('preprocessed_5Oct2018_500GB/bdd_car_data_late_Sept2018_lrc/locations'),
	opjm('2_TB_Samsung_n2_/bair_car_data_Main_Dataset_part1/locations'),#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	opjD('bdd_car_data_July2017_LCR/locations'),
	opjm('preprocessed_5Oct2018_500GB/model_car_data_June2018_LCR/locations'),
	opjm('preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations'),
	opjm('preprocessed_5Oct2018_500GB/bdd_model_car_data_late_Sept_early_Oct2018_lrc/locations'),
]
"""
"""
P['experiments_folders'] = [
	opjD('bdd_car_data_July2017_LCR/locations'),
	opjm('preprocessed_5Oct2018_500GB/bdd_model_car_data_early_8Oct2018_lrc_LIDAR/locations'),
	opjm('preprocessed_5Oct2018_500GB/bdd_model_car_data_late_Sept_early_Oct2018_lrc/locations'),
	opjm('preprocessed_5Oct2018_500GB/bdd_car_data_late_Sept2018_lrc/locations'),
	opjm('preprocessed_5Oct2018_500GB/bdd_car_data_18July_to_18Sept2018_lrc/locations'),
	opjm('preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations'),
	opjm('preprocessed_5Oct2018_500GB/model_car_data_June2018_LCR/locations'),
	opjD('bdd_car_data_July2017_LCR/locations'),
]
"""



if True:
	import kzpy3.Data_app.classify_data as classify_data
	P['experiments_folders'] = []
	classify_data.find_locations(opjm("1_TB_Samsung_n1"),P['experiments_folders'])
	#print len(P['experiments_folders'])
	#print P['experiments_folders']
	#raw_enter()
	classify_data.find_locations(opjm("rosbags"),P['experiments_folders'])
	print len(P['experiments_folders'])
	print P['experiments_folders']
	#raw_enter()
################################################################
if False:
################################################################
	older = [
		opjD('bdd_car_data_July2017_LCR/locations'),
		opjm('preprocessed_5Oct2018_500GB/bdd_model_car_data_early_8Oct2018_lrc_LIDAR/locations'),
		opjm('preprocessed_5Oct2018_500GB/bdd_model_car_data_late_Sept_early_Oct2018_lrc/locations'),
		opjm('preprocessed_5Oct2018_500GB/bdd_car_data_late_Sept2018_lrc/locations'),
		opjm('preprocessed_5Oct2018_500GB/bdd_car_data_18July_to_18Sept2018_lrc/locations'),
		opjm('preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations'),
		opjm('preprocessed_5Oct2018_500GB/model_car_data_June2018_LCR/locations'),
		opjD('bdd_car_data_July2017_LCR/locations'),
	]

	P['experiments_folders'] += older

if False:
	P['experiments_folders'] = [
		'/media/karlzipser/1_TB_Samsung_n1/left_direct_stop__29to30Oct2018/locations',
		'/media/karlzipser/1_TB_Samsung_n1/left_direct_stop__31Oct_to_1Nov2018/locations',
	] # around 4:45pm

P['experiments_folders'] = list(set(P['experiments_folders']))

"""
cb(P['experiments_folders'])
if P['use_LIDAR']:
	experiments_with_depth = []
	P['depth_run_files'] = sggo(P['LIDAR_path'],'*.Depth_images.log.resize.flip.left_ts')
	for r in sggo(P['depth_run_files'],'*'):
		run_name = fname(r).split('.')[0]
		for e in P['experiments_folders']:
			if fname(e) in P['depth_run_files']:
				experiments_with_depth.append(e)
	P['experiments_folders'] = experiments_with_depth
cg(P['experiments_folders'])
raw_enter()
"""
P['To Expose'] = {}
P['To Expose']['Train'] = ['print_timer_time','parameter_file_load_timer_time','percent_of_loss_list_avg_to_show']

P['BATCH_SIZE'] = 64
P['REQUIRE_ONE'] = []

if P['lidar_only']:
	P['NETWORK_OUTPUT_FOLDER'] = opjD('net_15Sept2018_1Nov_with_reverse_14Nov_with_only_LIDAR') #
elif P['use_LIDAR']:
	P['NETWORK_OUTPUT_FOLDER'] = opjD('net_15Sept2018_1Nov_with_reverse_14Nov_with_LIDAR') #
else:
	P['NETWORK_OUTPUT_FOLDER'] = opjD('net_15Sept2018_1Nov_with_reverse_') #
P['save_net_timer'] = Timer(60*30)
P['SAVE_FILE_NAME'] = 'net'
P['print_timer_time'] = 60
P['parameter_file_load_timer_time'] = 5
P['percent_of_loss_list_avg_to_show'] = 10.0
P['frequency_timer'] = Timer(30.0)
P['TRAIN_TIME'] = 60*5.0
P['VAL_TIME'] = 60*1.0
P['RESUME'] = True
if P['RESUME']:
    P['INITIAL_WEIGHTS_FOLDER'] = opj(P['NETWORK_OUTPUT_FOLDER'],'weights')
    P['WEIGHTS_FILE_PATH'] = most_recent_file_in_folder(P['INITIAL_WEIGHTS_FOLDER'],['net'],[])












P['reload_image_file_timer_time'] = 5*60
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
if False: # the standard before 15Sept2018
	P['prediction_range'] = range(1,60,6)
elif False:
	P['prediction_range'] = range(1,70,7)
	raw_enter(d2n("P['prediction_range'] = ",P['prediction_range'],', len = ',len(P['prediction_range']),', okay? '))
elif True:
	P['prediction_range'] = arange(1,90,9.8).astype(int)
	#raw_enter(d2n("P['prediction_range'] = ",P['prediction_range'],', len = ',len(P['prediction_range']),', okay? '))
	# array([ 1, 10, 20, 30, 40, 50, 59, 69, 79, 89])
	# len(a) = 10
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
				#########################################################################
				# Validation to be done with separate runs, so combine all data here.
				#########################################################################
				M = {}
				steer_types = _data_moments_indexed['train'].keys() # i.e., high_steer, low_steer, reverse
				for k in steer_types:
					M[k] = _data_moments_indexed['train'][k] + _data_moments_indexed['val'][k]

				lens = []
				for k in steer_types:
					lens.append(len(M[k]))
				max_len = max(lens)

				for k in steer_types:
					while len(M[k]) < max_len:
						random.shuffle(M[k])
						M[k] += M[k]
						if len(M[k]) > max_len:
							M[k] = M[k][:max_len]

				for k in steer_types:
					assert len(M[k]) == max_len


				for k in steer_types:
					for _dm in M[k]:
						#_dm['aruco'] = False
						if _dm['behavioral_mode'] == 'center':
							_dm['behavioral_mode'] = 'direct'
						if _dm['motor'] > 53 or (_dm['behavioral_mode'] == 'direct' and fname(e) == 'left_direct_stop'):
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







P['lacking runs'] = {}

def get_Data_moment(dm=None,FLIP=None):

	try:
		if dm['run_name'] in P['lacking runs']:
			return False
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





		################################## TEMP ################################
		#if min(Data_moment['motor'][:10]) > 50:
		#	return False
		#########################################################################

		if FLIP:
			Data_moment['steer'] = 99 - Data_moment['steer']
			Data_moment['gyro_heading_x'] = -1.0*Data_moment['gyro_heading_x']


		Data_moment['motor'][Data_moment['motor']<0] = 0
		Data_moment['motor'][Data_moment['motor']>99] = 99
		Data_moment['steer'][Data_moment['steer']<0] = 0
		Data_moment['steer'][Data_moment['steer']>99] = 99


		Data_moment['labels'] = {}
		Data_moment['name'] = dm['run_name']
		
		if P['use_LIDAR']:
			#cy("P['Loaded_image_files'].keys() =",P['Loaded_image_files'].keys())
			if 'depth' not in P['Loaded_image_files'][Data_moment['name']]:
				pass
				#cr("depth not in P['Loaded_image_files'][",Data_moment['name'],"]")
				return False
				
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


		if not P['use_LIDAR']:
			
			return Data_moment

		###############################################################
		###############################################################
		###############################################################
		####
		if P['use_LIDAR']:
			if P['lidar_only']:
				camera_lidar_1___camera_2___lidar_3 = 3
			else:
				camera_lidar_1___camera_2___lidar_3 = 1 #np.random.choice( [1,1,1,2,3,3,3,3])

		####
		###############################################################
		###############################################################
		###############################################################

		if P['use_LIDAR']:
			if camera_lidar_1___camera_2___lidar_3 == 3:
				for side in ['left','right']:
					for time_step in [0,1]:
						Data_moment[side][time_step] *= 0

			"""
			# This is temporary
			TEMP = [0,1,2]
			for side in ['left','right']:
				for position in [0,1,2]:
					Data_moment[side][1][:,:,position] *= 0
			"""


		if P['use_LIDAR']:
			#cy("P['Loaded_image_files'].keys() =",P['Loaded_image_files'].keys())
			if 'depth' not in P['Loaded_image_files'][Data_moment['name']]:
				pass
				cb("depth not in P['Loaded_image_files'][",Data_moment['name'],"]")
			else:
				#print P['Loaded_image_files'][Data_moment['name']].keys()
				#print P['Loaded_image_files'][Data_moment['name']]['depth'].keys()
				if 'depth' in P['Loaded_image_files'][Data_moment['name']]:
					pass#print 'A'
				if 'left_to_lidar_index' in P['Loaded_image_files'][Data_moment['name']]['depth'].keys():
					pass#print 'B'
					
				lidar_index = P['Loaded_image_files'][Data_moment['name']]['depth']['left_to_lidar_index'][il0]
				if FLIP:
					R = P['Loaded_image_files'][Data_moment['name']]['depth']['resized_flipped']
				else:
					R = P['Loaded_image_files'][Data_moment['name']]['depth']['resized']
				lidar_images = []
				for i in [0,-1,-2,-3]:
					lidar_images.append(R[lidar_index+i,:,:])
				Data_moment['left'][1][:,:,1] = lidar_images[0]
				Data_moment['left'][1][:,:,2] = lidar_images[1]
				Data_moment['right'][1][:,:,1] = lidar_images[2]
				Data_moment['right'][1][:,:,2] = lidar_images[3]




				if camera_lidar_1___camera_2___lidar_3 == 2:
					for side in ['left','right']:
						for position in [1,2]:
							Data_moment[side][1][:,:,position] *= 0

				#cg("success")
				return Data_moment

		return False
		#return Data_moment

	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		CS_('Exception!',exception=True,newline=False)
		CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
		return False









#EOF