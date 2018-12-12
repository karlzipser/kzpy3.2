from kzpy3.utils3 import *
from default_values import *
#from kzpy3.Train_app.Train_SqueezeNet_15Sept2018_1Nov_14Nov.default_values import *
CODE_PATH__ = opjh('kzpy3/Train_app')
VERSION_PATH = 'Train_SqueezeNet_15Sept2018_1Nov_14Nov'

#spd2s('Using',VERSION_PATH,'(make sure this is correct)')
time.sleep(3)

pythonpaths([opjh('kzpy3'),opj(CODE_PATH__,VERSION_PATH),opj(CODE_PATH__,'nets')])

#from Paths_Module import *
exec(identify_file_str)

"""
spd2s('REMEMBER ulimit -Sn 65000')

import resource
soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
print 'Soft limit is ', soft
assert(soft>=65000)
"""



P['experiments_folders'] = []
if True:
	import kzpy3.Data_app.classify_data as classify_data
	
	
	if True:
		locations_to_classify = [opjm("1_TB_Samsung_n1"),opjm('2_TB_Samsung_n3/rosbags__preprocessed_data')]
	else:
		locations_to_classify = [opjm('2_TB_Samsung_n3/rosbags__preprocessed_data')]
	
	for l in locations_to_classify:
		cb("classify_data.find_locations('",l,"'),P['experiments_folders'])...")
		classify_data.find_locations(l,P['experiments_folders'],False)
		cb("...done.")
	if verbose: print len(P['experiments_folders'])
	if verbose: print P['experiments_folders']
	#raw_enter()
################################################################
if True:
################################################################
	older = [
		#opjm('2_TB_Samsung_n3/bdd_car_data_July2017_LCR/locations'),
		opjm('2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/bdd_model_car_data_early_8Oct2018_lrc_LIDAR/locations'),
		opjm('2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/bdd_model_car_data_late_Sept_early_Oct2018_lrc/locations'),
		opjm('2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/bdd_car_data_late_Sept2018_lrc/locations'),
		opjm('2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/bdd_car_data_18July_to_18Sept2018_lrc/locations'),
		opjm('2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations'),
		#opjm('2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/model_car_data_June2018_LCR/locations'),
	]

	P['experiments_folders'] += older

if False:
	P['experiments_folders'] = [
		'/media/karlzipser/1_TB_Samsung_n1/left_direct_stop__29to30Oct2018/locations',
		'/media/karlzipser/1_TB_Samsung_n1/left_direct_stop__31Oct_to_1Nov2018/locations',
	] # around 4:45pm

P['experiments_folders'] = list(set(P['experiments_folders']))
if P['proportion of experiements to use'] < 1.0:
	random.shuffle(P['experiments_folders'])
	P['experiments_folders'] = \
		P['experiments_folders'][:int(P['proportion of experiements to use']*len(P['experiments_folders']))]
#pprint(P['experiments_folders'])

def equalize_to_max_len(M):
	cg("equalize_to_max_len()")
	cg("\tinitial lengths:")
	for k in M.keys():
		cg("\t\t",k,len(M[k]))
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
	cg("\tfinal lengths:")
	for k in M.keys():
		cg("\t\t",k,len(M[k]))

B = {}
B['left'] = []
B['right'] = []
B['direct'] = []
if True:
	for experiments_folder in P['experiments_folders']:
		if fname(experiments_folder)[0] == '_':
			continue
		cg("experiments_folder =",experiments_folder)
		locations = sggo(experiments_folder,'*')
		for location in locations:
			if fname(location)[0] == '_':
				spd2s('ignoring',location,"because of '_'" )
				continue
			if verbose: cg("\t",location)
			b_modes = sggo(location,'*')
			if verbose: cg("\t\tbehavioral modes at this location:", b_modes)
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
				cb("\t",fname(e))

				_data_moments_indexed = lo(opj(e,'data_moments_dic.pkl'))
				#########################################################################
				# Validation to be done with separate runs, so combine all data here.
				#########################################################################
				M = {}
				

				steer_types = _data_moments_indexed['train'].keys() # i.e., high_steer, low_steer, reverse
				for k in steer_types:
					M[k] = _data_moments_indexed['train'][k] + _data_moments_indexed['val'][k]


				equalize_to_max_len(M)

				#for k in steer_types:
				#	assert len(M[k]) == max_len

				for k in steer_types:
					for _dm in M[k]:
						#_dm['aruco'] = False
						#if (_dm['behavioral_mode'] == 'direct' and fname(e) == 'left_direct_stop'):
						#	cr(_dm)
						if _dm['behavioral_mode'] == 'center':
							_dm['behavioral_mode'] = 'direct'
						if _dm['motor'] > 53 or (_dm['behavioral_mode'] == 'direct' and fname(e) == 'left_direct_stop'):
							#P['data_moments_indexed'].append(_dm)
							if _dm['behavioral_mode'] in B:
								B[_dm['behavioral_mode']].append(_dm)
							else:
								pass #cr("behavioral_mode not in B: ",_dm['behavioral_mode'])

				if P['lidar_only']:
					for r in sggo(e,'h5py','*'):
						skip = False
						for q in ['08Oct','11Oct','12Oct','15Oct','16Oct','17Oct','18Oct']:
							if q in r:
								cr(q,'in',r)
								skip = True
								break
						if not skip:
							print fname(r)
							assert(fname(r) not in P['run_name_to_run_path'])
							P['run_name_to_run_path'][fname(r)] = r
				else:
					for r in sggo(e,'h5py','*'):
						print fname(r)
						assert(fname(r) not in P['run_name_to_run_path'])
						P['run_name_to_run_path'][fname(r)] = r
			
	cg("***********************************")
	equalize_to_max_len(B)

	for b in B.keys():
		P['data_moments_indexed'] += B[b]
	random.shuffle(P['data_moments_indexed'])


	#cb("\tlen( P['data_moments_indexed'] ) =", len( P['data_moments_indexed']) )

	########## TEMP ##############
	#
	#P['data_moments_indexed'] = P['data_moments_indexed'][:int(0.01*len(P['data_moments_indexed']))]
	#
	###########################
	runs_weighted = []
	for d in P['data_moments_indexed']:
		if d['run_name'] not in runs_weighted:
			runs_weighted.append(d['run_name'])
		if len(runs_weighted) == len(P['run_name_to_run_path']):
			break
	num_runs_to_use = max(P['min_num_runs_to_open'],int(P['proportion of runs to use']*len(runs_weighted)))
	runs_to_use = runs_weighted[:num_runs_to_use]
	cr(runs_weighted)
	cg(runs_to_use)
	data_moments_indexed = []
	for d in P['data_moments_indexed']:
		if d['run_name'] in runs_to_use:
			data_moments_indexed.append(d)
	P['data_moments_indexed'] = data_moments_indexed





	cb("\tlen( P['data_moments_indexed'] ) =", len( P['data_moments_indexed']) )

	#pprint(P['run_name_to_run_path'])

			#raw_enter()
			#break
		#break
				

	cg("len(P['data_moments_indexed']) =",len(P['data_moments_indexed']))
	cg("len(P['heading_pause_data_moments_indexed']) =",len(P['heading_pause_data_moments_indexed']))
	#raw_enter()










def get_Data_moment(dm=None,FLIP=None):

	try:
		if dm['run_name'] in P['lacking runs']:
			return False
		Data_moment = {}
		Data_moment['FLIP'] = FLIP
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




				if camera_lidar_1___camera_2___lidar_3 == 2:#???????????????????????
					for side in ['left','right']:
						for position in [1,2]:
							Data_moment[side][1][:,:,position] *= 0

				#cg("success")
				return Data_moment

		return False
		#return Data_moment


	except Exception as e:
	    exc_type, exc_obj, exc_tb = sys.exc_info()
	    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	    CS_('Exception!',emphasis=True)
	    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

	return False









#EOF