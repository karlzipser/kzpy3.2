from kzpy3.vis3 import *
#from kzpy3.Data_app.lidar.reprocess_lidar_points.runs_with_points import runs_with_points
exec(identify_file_str)








depth_images_path = opjD('Data/Depth_images')

runs_with_depth_Images = fnamenes(sggo(depth_images_path,'*'))

#depth_images_path = opjD('Depth_images__to_be_introducted')
#paths_with_depth_Images = sggo(depth_images_path,'*')
#runs_with_depth_Images = []
#for r in paths_with_depth_Images:
#	runs_with_depth_Images.append(fnamene(r))
#runs_with_depth_Images = fnamenes(paths_with_depth_Images)
#cb(runs_with_depth_Images,ra=0)
#runs_with_depth_Images = runs_with_depth_Images[:4];cr('runs_with_depth_Images = runs_with_depth_Images[:4]',ra=1)
#cy('len(runs_with_depth_Images) =',len(runs_with_depth_Images))

#pprint(runs_with_depth_Images)

kprint(runs_with_depth_Images,'runs_with_depth_Images')

def prepare_data_for_training(_):
	full = True
	#########################################################################################

	_['experiments_folders'] = []

	import kzpy3.Data_app.classify_data as classify_data
	
	
	if full:
		locations_to_classify = [
			opjD("Data/1_TB_Samsung_n1"),
			opjD("Data/2_TB_Samsung_n3/rosbags__preprocessed_data"),
		]
	else:
		locations_to_classify = [opjD("Data/2_TB_Samsung_n3/rosbags__preprocessed_data")]
	
	for l in locations_to_classify:
		cb("classify_data.find_locations('",l,"'),_['experiments_folders'])...")
		classify_data.find_locations(l,_['experiments_folders'],False)
	

	################################################################
	if full:
		older = [
			opjD("Data/2_TB_Samsung_n3/bdd_car_data_July2017_LCR/locations"),
			opjD("Data/2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/bdd_model_car_data_early_8Oct2018_lrc_LIDAR/locations"),
			opjD("Data/2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/bdd_model_car_data_late_Sept_early_Oct2018_lrc/locations"),
			opjD("Data/2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/bdd_car_data_late_Sept2018_lrc/locations"),
			opjD("Data/2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/bdd_car_data_18July_to_18Sept2018_lrc/locations"),
			opjD("Data/2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations"),
			opjD("Data/2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/model_car_data_June2018_LCR/locations"),
		]
		
		newer = [
			opjD("Data/2_TB_Samsung_n3/mid_Dec2018_with_lidar_image/locations"),
			opjD("Data/h5py_data_reprocessed_from_other_drives/locations"),
		]

		_['experiments_folders'] += older
		_['experiments_folders'] += newer

	##############################################################################################



	_['experiments_folders'] = list(set(_['experiments_folders']))



	experiments_folders = []


	#cm(0,len(_['experiments_folders']),ra=1)

	for e in _['experiments_folders']:
		R = {}
		classify_data.classify_data(e,R)
		runs = R.keys()
		some_run_with_Depth_images = False
		for r in runs:
			if r in runs_with_depth_Images:
				some_run_with_Depth_images = True
				cg(e,'has some_run_with_Depth_images',ra=0)
				break
		if some_run_with_Depth_images:
			experiments_folders.append(e)
	_['experiments_folders'] = experiments_folders
	#cm(1,len(_['experiments_folders']),ra=1)



	if _['proportion of experiements to use'] < 1.0:
		random.shuffle(_['experiments_folders'])
		_['experiments_folders'] = \
			_['experiments_folders'][:int(_['proportion of experiements to use']*len(_['experiments_folders']))]


	def equalize_to_max_len(M):
		#cg("equalize_to_max_len()")
		#cg("\tinitial lengths:")
		for k in M.keys():
			pass#cg("\t\t",k,len(M[k]))
		lens = []
		steer_types = M.keys()

		for k in steer_types:
			lens.append(len(M[k]))
		max_len = max(lens)

		for k in steer_types:
			if len(M[k]) == 0:
				continue
			while len(M[k]) < max_len:
				random.shuffle(M[k])
				M[k] += M[k]
				if len(M[k]) > max_len:
					M[k] = M[k][:max_len]

		for k in steer_types:
			assert (len(M[k]) == max_len) or (len(M[k]) == 0)
		#cg("\tfinal lengths:")
		for k in M.keys():
			pass#cg("\t\t",k,len(M[k]))

	B = {}
	B['left'] = []
	B['right'] = []
	B['direct'] = []
	setup_timer = Timer(10)
	setup_timer.trigger()
	if True:
		#cm(2,len(_['experiments_folders']),ra=1)
		for experiments_folder in _['experiments_folders']:
			setup_timer.message('setting up')
			if fname(experiments_folder)[0] == '_':
				continue
			#cg("experiments_folder =",experiments_folder)
			locations = sggo(experiments_folder,'*')
			for location in locations:
				if fname(location)[0] == '_':
					#spd2s('ignoring',location,"because of '_'" )
					continue
				#if _['verbose']: cg("\t",location)
				b_modes = sggo(location,'*')
				#if _['verbose']: cg("\t\tbehavioral modes at this location:", b_modes)
				#cg(b_modes)
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
					#cb("\t",fname(e))

					_data_moments_indexed = lo(opj(e,'data_moments_dic.pkl'))
					#########################################################################
					# Validation to be done with separate runs, so combine all data here.
					#########################################################################
					M = {}
					

					steer_types = _data_moments_indexed['train'].keys() # i.e., high_steer, low_steer, reverse
					for k in steer_types:
						M[k] = _data_moments_indexed['train'][k] + _data_moments_indexed['val'][k]


					equalize_to_max_len(M)

					for k in steer_types:
						for _dm in M[k]:
							if _dm['behavioral_mode'] == 'center':
								_dm['behavioral_mode'] = 'direct'
							if _dm['motor'] > 53 or (_dm['behavioral_mode'] == 'direct' and fname(e) == 'left_direct_stop'):

								if _dm['behavioral_mode'] in B:
									B[_dm['behavioral_mode']].append(_dm)
								else:
									pass #cr("behavioral_mode not in B: ",_dm['behavioral_mode'])

					if _['lidar_only']:
						for r in sggo(e,'h5py','*'):
							skip = False
							for q in ['08Oct','11Oct','12Oct','15Oct','16Oct','17Oct','18Oct']:
								if q in r:
									cr(q,'in',r)
									skip = True
									break
							if not skip:
								#print fname(r)
								assert(fname(r) not in _['run_name_to_run_path'])
								_['run_name_to_run_path'][fname(r)] = r
					else:
						for r in sggo(e,'h5py','*'):
							#print fname(r)
							if fname(r) not in runs_with_depth_Images:
								continue
							assert(fname(r) not in _['run_name_to_run_path'])
							_['run_name_to_run_path'][fname(r)] = r

		#cy("_['run_name_to_run_path'].keys()",len(_['run_name_to_run_path'].keys()))
		#pprint(_['run_name_to_run_path'].keys())
		kprint(_['run_name_to_run_path'].keys(),title="_['run_name_to_run_path'].keys()")
		okay = True
		for r in _['run_name_to_run_path'].keys():
			if r not in runs_with_depth_Images:
				okay = False
				cprint(d2s(r,"not in runs_with_depth_Images"),'white','on_red')
		if okay:
			cg('runs_with_depth_Images accounted for.')
		okay = True
		for r in runs_with_depth_Images:
			if r not in _['run_name_to_run_path'].keys():
				okay = False
				cprint(d2s(r,"not in _['run_name_to_run_path'].keys()"),'red','on_white')
		if okay:
			cg("not in _['run_name_to_run_path'].keys() accounted for.")
		#cg("***********************************")
		equalize_to_max_len(B)

		for b in B.keys():
			_['data_moments_indexed'] += B[b]
		random.shuffle(_['data_moments_indexed'])

		runs_weighted = []
		for d in _['data_moments_indexed']:
			if d['run_name'] not in runs_weighted:
				runs_weighted.append(d['run_name'])
			if len(runs_weighted) == len(_['run_name_to_run_path']):
				break
		num_runs_to_use = max(_['min_num_runs_to_open'],int(_['proportion of runs to use']*len(runs_weighted)))
		runs_to_use = runs_weighted[:num_runs_to_use]
		#cr(runs_weighted)
		#cg(runs_to_use)
		data_moments_indexed = []
		for d in _['data_moments_indexed']:
			if d['run_name'] in runs_to_use:
				data_moments_indexed.append(d)
		_['data_moments_indexed'] = data_moments_indexed





def load_Network_Predictions(_):
	Network_Predictions = {}
	files = sggo(opjD('Data/Network_Predictions/*.pkl'))
	#cy(files)
	timer = Timer(60)
	ctr = 0
	for f in files:
		k = fnamene(f)
		
		if k not in runs_with_depth_Images:
			#cy(k)#,runs_with_depth_Images)
			cy('not loading Network_Predictions for',f)
			continue
		#pprint(_['run_name_to_run_path'].keys())
		#raw_enter()
		if k not in _['run_name_to_run_path'].keys():
			#cr(fname(f))
			cr('not loading Network_Predictions for',f)
			continue
		if False:#timer.check():
			cm('done')
			return
		if fname(f) != 'runs.pkl':
			ctr += 1
			cb('loading',k,'(',ctr,')')
			Network_Predictions[k] = lo(f)
		else:
			cr(f)
	return Network_Predictions




blank_meta = np.zeros((23,41,3),np.uint8)
blank_camera = np.zeros((94,168,3),np.uint8)







depth_image_files = sggo(depth_images_path,'*.Depth_image.with_left_ts.rgb_v1.h5py')
Depth_runs = {}
for f in depth_image_files:
	run_name = fname(f).split('.')[0]
	Depth_runs[run_name] = h5r(f)




def get_Data_moment(_,Network_Predictions,dm=None,FLIP=None):

	try:
		if dm['run_name'] in _['lacking runs']:
			return False
		Data_moment = {}
		Data_moment['FLIP'] = FLIP
		left_index = dm['left_ts_index'][1]
		steer_len = len(_['Loaded_image_files'][dm['run_name']]['left_timestamp_metadata']['steer'])
		data_len = min(steer_len - left_index,90)
		behavioral_mode = dm['behavioral_mode']
		#cg(dm['run_name'],left_index)




		if dm['run_name'] in Depth_runs:
			if left_index >= len(Depth_runs[dm['run_name']]['left_to_lidar_index']):
				return False
			index = Depth_runs[dm['run_name']]['left_to_lidar_index'][left_index]
			if index < 1:
				return False
			if FLIP:
				fp = 'rgb_v1_flip'
			else:
				fp = 'rgb_v1_normal'
			Data_moment['depth_image_0'] = Depth_runs[dm['run_name']][fp][index]
			Data_moment['depth_image_n1'] = Depth_runs[dm['run_name']][fp][index-1]
		else:
			return False





		Data_moment['predictions'] = {}
		for s in ['left','direct','right']:
			_index = Network_Predictions[dm['run_name']]['index'][left_index]
			if True:
				Data_moment['predictions'][s] = Network_Predictions[dm['run_name']][s][_index].copy()
			elif False:
				Data_moment['predictions'][s] = Network_Predictions[dm['run_name']][s][_index]
			#Data_moment['predictions'][s]['heading'] -= Data_moment['predictions'][s]['heading'][0]
			if FLIP:
				Data_moment['predictions'][s]['steer'] = 99 - Data_moment['predictions'][s]['steer']
				Data_moment['predictions'][s]['heading'] = -1 * Data_moment['predictions'][s]['heading']

		if True:
			if steer_len - left_index < 90:
				print steer_len - left_index

		for q in ['steer','motor','gyro_heading_x','encoder_meo']:	
			Data_moment[q] = zeros(90) + 49
			if q not in _['Loaded_image_files'][dm['run_name']]['left_timestamp_metadata']:
				pd2s(dm['run_name'],'lacks',q)
				_['lacking runs'][dm['run_name']] = q
				return False
			if behavioral_mode != 'heading_pause':
				Data_moment[q][:data_len] = _['Loaded_image_files'][dm['run_name']]['left_timestamp_metadata'][q][left_index:left_index+data_len]

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
					#cg(q,past,past_data_len,left_index,dm['run_name'])
					#cb(shape(_['Loaded_image_files'][dm['run_name']]['left_timestamp_metadata'][q][(left_index-past_data_len):left_index]))
					Data_moment[q+past][:past_data_len] = _['Loaded_image_files'][dm['run_name']]['left_timestamp_metadata'][q][(left_index-past_data_len):left_index]
					if FLIP:
						if q == 'steer':
							Data_moment[q+past][:past_data_len] = 99-Data_moment[q+past][:past_data_len]
						elif q == 'acc_x' or q == 'gyro_x' or q == 'gyro_y':
							Data_moment[q+past][:past_data_len] = -1*Data_moment[q+past][:past_data_len]

		if FLIP:
			Data_moment['steer'] = 99 - Data_moment['steer']
			Data_moment['gyro_heading_x'] = -1.0*Data_moment['gyro_heading_x']


		Data_moment['motor'][Data_moment['motor']<0] = 0
		Data_moment['motor'][Data_moment['motor']>99] = 99
		Data_moment['steer'][Data_moment['steer']<0] = 0
		Data_moment['steer'][Data_moment['steer']>99] = 99

		Data_moment['labels'] = {}
		Data_moment['name'] = dm['run_name']
		
		if _['use_LIDAR']:
			if 'depth' not in _['Loaded_image_files'][Data_moment['name']]:
				return False
				
		if FLIP:
			if behavioral_mode == 'left':
				behavioral_mode = 'right'
			elif behavioral_mode == 'right':
				behavioral_mode = 'left'

		for b in _['behavioral_modes']:
			Data_moment['labels'][b] = 0
		if behavioral_mode == 'heading_pause':
			behavioral_mode = random.choice(_['behavioral_modes_no_heading_pause'])
		Data_moment['labels'][behavioral_mode] = 1



		tl0 = dm['left_ts_index'][0]; il0 = dm['left_ts_index'][1]
		tr0 = dm['right_ts_index'][0]; ir0 = dm['right_ts_index'][1]

		if FLIP:
			F = _['Loaded_image_files'][Data_moment['name']]['flip']
			
		else:
			F = _['Loaded_image_files'][Data_moment['name']]['normal']
			
		

		
		Data_moment['left'] = {}
		Data_moment['right'] = {}


		if False: # for full zeroing of camera inputs
			Data_moment['left'][0] = blank_camera
			Data_moment['right'][0] = blank_camera
			Data_moment['left'][1] = blank_camera
			Data_moment['right'][1] = blank_camera
			return Data_moment

		else: # below is the normal case
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


			if False:
				mci(Data_moment['left'][0],title='left')
				mci(Data_moment['right'][0],title='right')
				mci(Data_moment['depth_image_0'],title='depth_image_0')
				mci(Data_moment['depth_image_n1'],title='depth_image_n1')
				clf()
				print shape(Data_moment['steer'])
				plot(Data_moment['steer'][:30],'r.-')
				plot(Data_moment['steer'][30:60],'g.-')
				plot(Data_moment['steer'][60:],'b.-')
				xylim(0,90,0,99);spause()
				raw_enter()




			return Data_moment

		return False

	except Exception as e:
	    exc_type, exc_obj, exc_tb = sys.exc_info()
	    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	    CS_('Exception!',emphasis=True)
	    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

	return False








#EOF