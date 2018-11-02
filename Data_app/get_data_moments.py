from kzpy3.vis3 import *

"""
Extracted from 'get_data_moments_plus_other_task_2017.py', originally named 'ideas.py'
"""

def get_data_moments(dataset_path,location,behavioral_mode,run_name,num_steps):
	if behavioral_mode == 'LCR':
		return get_data_moments__LCR_dataset_version(dataset_path,location,behavioral_mode,run_name,num_steps)
	elif behavioral_mode == 'left_right_center':
		return get_data_moments__left_right_center_dataset_version(dataset_path,location,behavioral_mode,run_name,num_steps)
	elif behavioral_mode == 'left_direct_stop':
		return get_data_moments__left_direct_stop_dataset_version(dataset_path,location,behavioral_mode,run_name,num_steps)
	elif behavioral_mode in ['direct','follow','furtive','play']:
		return get_data_moments__more_generic_version(dataset_path,location,behavioral_mode,run_name,num_steps)
	else:
		spd2s('???')
		assert False

def get_data_moments__LCR_dataset_version(dataset_path,location,behavioral_mode,run_name,num_steps):
	# LCR dataset version
	assert(behavioral_mode == 'LCR')
	F_path = opj(dataset_path,location,behavioral_mode,'h5py',run_name,'original_timestamp_data.h5py')
	print F_path
	F=h5r(F_path)
	try:
		L=h5r(opj(dataset_path,location,behavioral_mode,'h5py',run_name,'left_timestamp_metadata.h5py'))
	except:
		L=h5r(opj(dataset_path,location,behavioral_mode,'h5py',run_name,'left_timestamp_metadata_right_ts.h5py'))
	timer = Timer(5)
	results = []
	state = L['state'][:]
	
	data_moments = []
	ts = L['ts'][:]
	r_indicies,r_timestamps = right_indicies_timestamps(F,n=60)
	assert(behavioral_mode == 'LCR')
	if behavioral_mode == 'LCR':
		accepted_states = [1,2,3]
	else:
		accepted_states = [1]

	for i in range(len(ts)-num_steps):
		timer.percent_message(i,len(ts)-num_steps)
		r = is_this_a_good_data_moment(L=L,index=i,steps=num_steps,time_proportion_tolerance=0.2,state_proportion_tolerance=0.4,min_initial_steps=15,accepted_states=accepted_states,motor_threshold=52)
		results.append(r)
		
		if r:
			#print behavioral_mode
			try:
				if True:#behavioral_mode == 'LCR':
					#print int(np.round(L['state'][i])),L['state'][i]
					s = int(np.round(L['state'][i]))
					if s == 1:
						behavioral_mode = 'center'
					elif s == 2:
						behavioral_mode = 'left'
						#print 'left'
					elif s == 3:
						behavioral_mode = 'right'
						#print 'right'
					else:
						print int(np.round(L['state'][i])),L['state'][i]
						assert(False)
				
				data_moments.append(
					{'behavioral_mode': behavioral_mode,
					 'left_ts_index': (ts[i], i),
					 'motor': np.int(np.round(L['motor'][i])),
					 'right_ts_index': (F['right_image']['ts'][r_indicies[i]],r_indicies[i]),#(right_tsv[i], i),
					 'run_name': run_name,
					 'steer': np.int(np.round(L['steer'][i]))})
				#if data_moments[-1]['behavioral_mode'] != 'center':
				#	print data_moments[-1]['behavioral_mode']
			except:
				pd2s('failed data_moments')
	figure('data moments');clf();ylim(-0.5,5.0)
	plot(state+0.02) 
	plot(L['left_ts_deltas'][:]*10)
	plot(results)
	plt.title(run_name)
	spause()

	dm_test = []
	for d in data_moments:
		dm_test.append(d['left_ts_index'][0]-d['right_ts_index'][0])
	figure(3);clf();hist(dm_test);spause()
	try:
		F.close()
		L.close()
	except:
		pass
	return data_moments



def get_data_moments__more_generic_version(dataset_path,location,behavioral_mode,run_name,num_steps):
	# from LCR dataset version
	F_path = opj(dataset_path,location,behavioral_mode,'h5py',run_name,'original_timestamp_data.h5py')
	print F_path
	F=h5r(F_path)
	try:
		L=h5r(opj(dataset_path,location,behavioral_mode,'h5py',run_name,'left_timestamp_metadata.h5py'))
	except:
		L=h5r(opj(dataset_path,location,behavioral_mode,'h5py',run_name,'left_timestamp_metadata_right_ts.h5py'))
	timer = Timer(5)
	results = []
	state = L['state'][:]
	
	data_moments = []
	ts = L['ts'][:]
	r_indicies,r_timestamps = right_indicies_timestamps(F,n=60)
	accepted_states = [1]

	for i in range(len(ts)-num_steps):
		timer.percent_message(i,len(ts)-num_steps)
		r = is_this_a_good_data_moment(L=L,index=i,steps=num_steps,time_proportion_tolerance=0.2,state_proportion_tolerance=0.4,min_initial_steps=15,accepted_states=accepted_states,motor_threshold=52)
		results.append(r)
		
		if r:
			#print behavioral_mode
			try:
				"""
				if True:#behavioral_mode == 'LCR':
					#print int(np.round(L['state'][i])),L['state'][i]
					s = int(np.round(L['state'][i]))
					if s == 1:
						behavioral_mode = 'center'
					elif s == 2:
						behavioral_mode = 'left'
						#print 'left'
					elif s == 3:
						behavioral_mode = 'right'
						#print 'right'
					else:
						print int(np.round(L['state'][i])),L['state'][i]
						assert(False)
				"""
				
				data_moments.append(
					{'behavioral_mode': behavioral_mode,
					 'left_ts_index': (ts[i], i),
					 'motor': np.int(np.round(L['motor'][i])),
					 'right_ts_index': (F['right_image']['ts'][r_indicies[i]],r_indicies[i]),#(right_tsv[i], i),
					 'run_name': run_name,
					 'steer': np.int(np.round(L['steer'][i]))})
				#if data_moments[-1]['behavioral_mode'] != 'center':
				#	print data_moments[-1]['behavioral_mode']
			except:
				pd2s('failed data_moments')
	figure('data moments');clf();ylim(-0.5,5.0)
	plot(state+0.02) 
	plot(L['left_ts_deltas'][:]*10)
	plot(results)
	plt.title(run_name)
	spause()

	dm_test = []
	for d in data_moments:
		dm_test.append(d['left_ts_index'][0]-d['right_ts_index'][0])
	figure(3);clf();hist(dm_test);spause()
	try:
		F.close()
		L.close()
	except:
		pass
	return data_moments



def get_data_moments__left_right_center_dataset_version(dataset_path,location,behavioral_mode,run_name,num_steps):
	# left_right_center dataset version
	assert(behavioral_mode == 'left_right_center')
	F_path = opj(dataset_path,location,behavioral_mode,'h5py',run_name,'original_timestamp_data.h5py')
	print F_path
	F=h5r(F_path)
	try:
		L=h5r(opj(dataset_path,location,behavioral_mode,'h5py',run_name,'left_timestamp_metadata.h5py'))
	except:
		L=h5r(opj(dataset_path,location,behavioral_mode,'h5py',run_name,'left_timestamp_metadata_right_ts.h5py'))
	timer = Timer(5)
	results = []
	drive_state = L['drive_mode'][:] * L['human_agent'][:]
	
	data_moments = []
	ts = L['ts'][:]
	r_indicies,r_timestamps = right_indicies_timestamps(F,n=60)
	
	accepted_states = [1]

	for i in range(len(ts)-num_steps):
		timer.percent_message(i,len(ts)-num_steps)
		r = is_this_a_good_data_moment__left_right_center_version(drive_state=drive_state,L=L,index=i,steps=num_steps,time_proportion_tolerance=0.2,state_proportion_tolerance=0.4,min_initial_steps=15,accepted_states=accepted_states,motor_threshold=52)
		results.append(r)
		
		if r:
			#print behavioral_mode
			try:
				if True:#behavioral_mode == 'LCR':
					if intr(drive_state[i]) == 1:
						L_behavioral_mode = intr(L['behavioral_mode'][i])
						#'direct':2,'left':3,'right':1
						if L_behavioral_mode == 1:
							behavioral_mode = 'right'
						elif L_behavioral_mode == 2:
							behavioral_mode = 'center'
						elif L_behavioral_mode == 3:
							behavioral_mode = 'left'							
						else:
							spd2s(L['behavioral_mode'][i])
							continue
				
				data_moments.append(
					{'behavioral_mode': behavioral_mode,
					 'left_ts_index': (ts[i], i),
					 'motor': np.int(np.round(L['motor'][i])),
					 'right_ts_index': (F['right_image']['ts'][r_indicies[i]],r_indicies[i]),#(right_tsv[i], i),
					 'run_name': run_name,
					 'steer': np.int(np.round(L['steer'][i]))})
				#if data_moments[-1]['behavioral_mode'] != 'center':
				#	print data_moments[-1]['behavioral_mode']
			except:
				pd2s('failed data_moments')
	figure('data moments');clf();ylim(-0.5,5.0)
	plot(drive_state+0.02) 
	plot(L['left_ts_deltas'][:]*10)
	plot(results)
	plt.title(run_name)
	spause()

	dm_test = []
	for d in data_moments:
		dm_test.append(d['left_ts_index'][0]-d['right_ts_index'][0])
	figure(3);clf();hist(dm_test);spause()
	try:
		F.close()
		L.close()
	except:
		pass
	return data_moments





def get_data_moments__left_direct_stop_dataset_version(dataset_path,location,behavioral_mode,run_name,num_steps):

	assert(behavioral_mode == 'left_direct_stop')

	F_path = opj(dataset_path,location,behavioral_mode,'h5py',run_name,'original_timestamp_data.h5py')
	print F_path
	F=h5r(F_path)
	try:
		L=h5r(opj(dataset_path,location,behavioral_mode,'h5py',run_name,'left_timestamp_metadata.h5py'))
	except:
		L=h5r(opj(dataset_path,location,behavioral_mode,'h5py',run_name,'left_timestamp_metadata_right_ts.h5py'))
	timer = Timer(5)
	results = []

	b = L['button_number'][:]
	button_lt_3 = b.copy().astype(int)
	button_lt_3[ button_lt_3 > 2] = 0
	button_lt_3[ button_lt_3 > 0 ] = 1

	drive_state = L['drive_mode'][:] * L['human_agent'][:] * button_lt_3
	
	data_moments = []
	ts = L['ts'][:]
	r_indicies,r_timestamps = right_indicies_timestamps(F,n=60)
	
	accepted_states = [1]

	for i in range(len(ts)-num_steps):

		timer.percent_message(i,len(ts)-num_steps)

		r = is_this_a_good_data_moment__left_right_center_version(
			drive_state=drive_state,
			L=L,index=i,
			steps=num_steps,
			time_proportion_tolerance=0.2,
			state_proportion_tolerance=0.4,
			min_initial_steps=15,
			accepted_states=accepted_states,
			motor_threshold=0)  ### NOTE THAT REVERSE IS PERMITTED IN THIS BEHAVIORAL MODE

		results.append(r)
		
		if r:
			#print behavioral_mode
			try:
				if True:
					if intr(drive_state[i]) == 1:
						L_behavioral_mode = intr(L['behavioral_mode'][i])
						#'direct':2,'left':3,'right':1
						if L_behavioral_mode == 1:
							behavioral_mode = 'stop'
						elif L_behavioral_mode == 2:
							behavioral_mode = 'center'
						elif L_behavioral_mode == 3:  ### IT IS CONFUSING THAT L_behavioral_mode numbers
								# are different from button numbers.
							behavioral_mode = 'left'							
						else:
							spd2s(L['behavioral_mode'][i])
							continue
				
				data_moments.append(
					{'behavioral_mode': behavioral_mode,
					 'left_ts_index': (ts[i], i),
					 'motor': np.int(np.round(L['motor'][i])),
					 'right_ts_index': (F['right_image']['ts'][r_indicies[i]],r_indicies[i]),#(right_tsv[i], i),
					 'run_name': run_name,
					 'steer': np.int(np.round(L['steer'][i]))})
				#if data_moments[-1]['behavioral_mode'] != 'center':
				#	print data_moments[-1]['behavioral_mode']
			except:
				pd2s('failed data_moments')
	figure('data moments');clf();ylim(-0.5,5.0)
	plot(drive_state+0.02) 
	plot(L['left_ts_deltas'][:]*10)
	plot(results)
	plt.title(run_name)
	spause()

	dm_test = []
	for d in data_moments:
		dm_test.append(d['left_ts_index'][0]-d['right_ts_index'][0])
	figure(3);clf();hist(dm_test);spause()
	try:
		F.close()
		L.close()
	except:
		pass
	return data_moments





def right_indicies_timestamps(F,n=5):
	l_ts = F['left_image']['ts'][:]
	r_ts = F['right_image']['ts'][:]
	r_indicies = []
	r_timestamps = []
	ln = min(len(l_ts),len(r_ts))
	test = []
	for i in range(ln):
		l = l_ts[i]
		smallest_delta = 10
		best_j = i
		for j in range(i-n,i+n):
			if j >= 0:
				if j < ln:
					delta = l_ts[i]-r_ts[j]
					if abs(delta)<smallest_delta and delta<0:
						smallest_delta = delta
						best_j = j
		test.append(best_j-i)
		r_indicies.append(best_j)
		r_timestamps.append(r_ts[best_j])
	figure('test');clf()
	hist(test);spause()
	return r_indicies,r_timestamps




def is_this_a_good_data_moment(L=None,index=0,steps=0,time_proportion_tolerance=0,state_proportion_tolerance=0,min_initial_steps=0,accepted_states=[],motor_threshold=0):
	start_time = L['ts'][index]
	end_time = L['ts'][index+steps-1]
	d_time = end_time - start_time
	expected_time = steps * 1/30.0
	if abs(expected_time - d_time) > time_proportion_tolerance * expected_time:
		return 0
	state_1s = 0
	for i in range(index,index + steps):
		if int(np.round(L['state'][i])) in accepted_states:
			state_1s += 1
		else:
			if i-index < min_initial_steps:
				return 0
		if L['motor'][i] < motor_threshold:
			return 0
	if state_1s / (1.0*steps) < state_proportion_tolerance:
		return 0
	return 1



def is_this_a_good_data_moment__left_right_center_version(drive_state=None,L=None,index=0,steps=0,time_proportion_tolerance=0,state_proportion_tolerance=0,min_initial_steps=0,accepted_states=[],motor_threshold=0):
	start_time = L['ts'][index]
	end_time = L['ts'][index+steps-1]
	d_time = end_time - start_time
	expected_time = steps * 1/30.0
	if abs(expected_time - d_time) > time_proportion_tolerance * expected_time:
		return 0
	state_1s = 0
	for i in range(index,index + steps):
		if intr(drive_state[i]) == 1: ########## This is the difference from the version above
			state_1s += 1
		else:
			if i-index < min_initial_steps:
				return 0
		if L['motor'][i] < motor_threshold:
			return 0
	if state_1s / (1.0*steps) < state_proportion_tolerance:
		return 0
	return 1






# EOF