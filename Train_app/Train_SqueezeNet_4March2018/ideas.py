"""
{'behavioral_mode': 'Direct_Arena_Potential_Field',
 'counter_clockwise': 0,
 'left_ts_index': (1506212011.0179999, 4605),
 'motor': 51,
 'other_car_in_view': False,
 'right_ts_index': (1506212011.0409999, 4605),
 'run_name': 'Mr_Lt_Blue_2017-09-23-17-10-51',
 'steer': 11}


experiment_folders
data_moment_files
proportion


break up data_moments_index.pkl into

train_data_moments_index_car_in_view.pkl
val_data_moments_index_car_in_view.pkl

train_data_moments_index_car_not_in_view.pkl
val_data_moments_index_car_not_in_view.pkl

data_moments
	train_car_in_view.pkl
	val_car_in_view.pkl
	train_car_not_in_view.pkl
	val_car_not_in_view.pkl
"""


#############################################################################
#
experiments = sggo('/home/karlzipser/Desktop/all_aruco_reprocessed/*')
for e in experiments:
	if fname(e)[0] == '_':
		spd2s('ignoring',e)
		continue
	spd2s(e)

	data_moments_folder = opj(e,'data_moments')
	unix('mkdir -p '+data_moments_folder)
	data_moments_indexed_file = opj(e,'data_moments_indexed.pkl')

	data_moments = lo(data_moments_indexed_file)

	random.shuffle(data_moments)

	num_val = 0.1*len(data_moments)

	val__direct__car_in_view = []
	train__direct_car_in_view = []
	val__direct__car_not_in_view = []
	train__direct__car_not_in_view = []
	val__follow__car_in_view = []
	train__follow__car_in_view = []
	val__follow__car_not_in_view = []
	train__follow_car__not_in_view = []
	ctr = 0

	for d in data_moments:
		if d['behavioral_mode'] == 'Direct_Arena_Potential_Field':
			if d['other_car_in_view']:
				if ctr < num_val:
					val__direct__car_in_view.append(d)
				else:
					train__direct_car_in_view.append(d)
			else:
				if ctr < num_val:
					val__direct__car_not_in_view.append(d)
				else:
					train__direct__car_not_in_view.append(d)
		elif d['behavioral_mode'] == 'Follow_Arena_Potential_Field':
			if d['other_car_in_view']:
				if ctr < num_val:
					val__follow__car_in_view.append(d)
				else:
					train__follow__car_in_view.append(d)
			else:
				if ctr < num_val:
					val__follow__car_not_in_view.append(d)
				else:
					train__follow_car__not_in_view.append(d)
		else:
			assert(False)
		ctr += 1

	so(opj(data_moments_folder,'val__direct__car_in_view'),val__direct__car_in_view)
	so(opj(data_moments_folder,'train__direct_car_in_view'),train__direct_car_in_view)
	so(opj(data_moments_folder,'val__direct__car_not_in_view'),val__direct__car_not_in_view)
	so(opj(data_moments_folder,'train__direct__car_not_in_view'),train__direct__car_not_in_view)
	so(opj(data_moments_folder,'val__follow__car_in_view'),val__follow__car_in_view)
	so(opj(data_moments_folder,'train__follow__car_in_view'),train__follow__car_in_view)
	so(opj(data_moments_folder,'val__follow__car_not_in_view'),val__follow__car_not_in_view)
	so(opj(data_moments_folder,'train__follow_car__not_in_view'),train__follow_car__not_in_view)





# 9 March 2018, putting runs into location folders
# part 1
data_folder = '/media/karlzipser/2_TB_Samsung/bair_car_data_Main_Dataset_part1'
run_labels = lo(opj(data_folder,'run_labels/run_labels_23Apr17_10h04m46s.pkl' ))
runs = sggo(data_folder,'h5py/*')

locations = ['snow','campus','Tilden','home','local','Smyth']
for location in locations:
	unix(d2s('mkdir -p',opj(data_folder,location,'h5py')))
	for r in run_labels.keys():
		if location in run_labels[r]:
			if run_labels[r][location] == True:
				unix_str = d2s('mv',opj(data_folder,'h5py',r),opj(data_folder,location,'h5py'))
				print unix_str
				unix(unix_str,'False')


# part 2
behaviors = ['play','follow','racing','furtive','direct']
locations = ['snow','campus','Tilden','home','local','Smyth']
for location in locations:
	runs = sggo(data_folder,location,'h5py/*')
	#unix(d2s('mkdir -p',opj(data_folder,location,'h5py')))
	for r in runs: #run_labels.keys():
		run_name = fname(r)
		if run_name in run_labels.keys():
			if location in run_labels[run_name]:
				if run_labels[run_name][location] == True:
					for behavior in behaviors:
						if behavior in run_labels[run_name]:
							if run_labels[run_name][behavior] == True:
								dst = opj(data_folder,location,behavior,'h5py')
								unix_str = d2s('mkdir -p',dst)
								print unix_str
								unix(unix_str)
								unix_str = d2s('mv',r,dst)
								print unix_str
								unix(unix_str)
					#unix_str = d2s('mv',opj(data_folder,'h5py',r),opj(data_folder,location,'h5py'))
					#print unix_str
					#unix(unix_str,'False')

#
#############################################################################
# 13 March 2018, putting runs into location folders
# part 1
data_folder = '/media/karlzipser/2_TB_Samsung_n2_/bair_car_data_Main_Dataset_part1'
run_labels = lo(opj(data_folder,'run_labels/run_labels_23Apr17_10h04m46s.pkl' ))
runs = sggo(data_folder,'h5py/*')

locations = ['snow','campus','Tilden','home','local','Smyth']
for location in locations:
	unix(d2s('mkdir -p',opj(data_folder,location,'h5py')))
	for r in run_labels.keys():
		if location in run_labels[r]:
			if run_labels[r][location] == True:
				unix_str = d2s('mv',opj(data_folder,'h5py',r),opj(data_folder,location,'h5py'))
				print unix_str
				unix(unix_str,'False')

# part 2
behaviors = ['play','follow','racing','furtive','direct']
locations = ['snow','campus','Tilden','home','local','Smyth']
for location in locations:
	runs = sggo(data_folder,location,'h5py/*')
	#unix(d2s('mkdir -p',opj(data_folder,location,'h5py')))
	for r in runs: #run_labels.keys():
		run_name = fname(r)
		if run_name in run_labels.keys():
			if location in run_labels[run_name]:
				if run_labels[run_name][location] == True:
					for behavior in behaviors:
						if behavior in run_labels[run_name]:
							if run_labels[run_name][behavior] == True:
								dst = opj(data_folder,location,behavior,'h5py')
								unix_str = d2s('mkdir -p',dst)
								print unix_str
								unix(unix_str)
								unix_str = d2s('mv',r,dst)
								print unix_str
								unix(unix_str)
					#unix_str = d2s('mv',opj(data_folder,'h5py',r),opj(data_folder,location,'h5py'))
					#print unix_str
					#unix(unix_str,'False')

#
#############################################################################
# high steer low steer



# making data moment lists like aruco data for older data

"""
good data moment:
	select time interval: value should be within 20 percent
	80 percent of timepoint should be in state 1

Do I want non-linear time sampling? No.

input: num. sample points, time tolerance, state 1 tolerance

when in state 4, use previous motor and steer values because state 4 gives wild numbers

When not in state 1, maintain previous state 1 target values.

First sample must be in state 1.

"""






###################################################################
#

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


def is_this_a_good_data_moment(L=None,index=0,steps=0,time_proportion_tolerance=0,state_proportion_tolerance=0,min_initial_steps=0):
	start_time = L['ts'][index]
	end_time = L['ts'][index+steps-1]
	d_time = end_time - start_time
	expected_time = steps * 1/30.0
	if abs(expected_time - d_time) > time_proportion_tolerance * expected_time:
		return 0
	state_1s = 0
	for i in range(index,index + steps):
		if abs(L['state'][i] - 1.0) < 0.1:
			state_1s += 1
		else:
			if i-index < min_initial_steps:
				#pd2s('rejecting',i)
				return 0
	if state_1s / (1.0*steps) < state_proportion_tolerance:
		return 0
	return 1


def get_data_moments(dataset_path,location,behavioral_mode,run_name,num_steps):
	F=h5r(opj(dataset_path,location,behavioral_mode,'h5py',run_name,'original_timestamp_data.h5py'))
	L=h5r(opj(dataset_path,location,behavioral_mode,'h5py',run_name,'left_timestamp_metadata.h5py'))
	timer = Timer(5)
	results = []
	state = L['state'][:]
	
	data_moments = []
	ts = L['ts'][:]
	r_indicies,r_timestamps = right_indicies_timestamps(F,n=60)
	#right_tsv = _assign_right_image_timestamps2(F)
	for i in range(len(ts)-num_steps):
		timer.percent_message(i,len(ts)-num_steps)
		r = is_this_a_good_data_moment(L=L,index=i,steps=num_steps,time_proportion_tolerance=0.2,state_proportion_tolerance=0.4,min_initial_steps=15)
		results.append(r)
		if r:
			try:
				data_moments.append(
					{'behavioral_mode': behavioral_mode,
					 'left_ts_index': (ts[i], i),
					 'motor': L['motor'][i],
					 'right_ts_index': (F['right_image']['ts'][r_indicies[i]],r_indicies[i]),#(right_tsv[i], i),
					 'run_name': run_name,
					 'steer': L['steer'][i]})
			except:
				pd2s('failed data_moments')
	figure('data moments');clf();ylim(-0.5,3.0)
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


locations_path = '/media/karlzipser/2_TB_Samsung_n2_/bair_car_data_Main_Dataset_part1/locations'
#locations_path = '/media/karlzipser/2_TB_Samsung/bair_car_data_Main_Dataset_part1/locations'
locations = sggo(locations_path,'*')
num_steps = 90
for l in locations:
	location = fname(l)
	behavioral_modes = sggo(l,'*')
	for b in behavioral_modes:
		Data_Moments = []
		behavioral_mode = fname(b)
		print location,behavioral_mode
		runs = sggo(b,'h5py','*')
		for r in runs:
			run_name = fname(r)
			pd2s('\t',run_name)
			data_moments = get_data_moments(locations_path,location,behavioral_mode,run_name,num_steps)
			Data_Moments += data_moments
			pd2s('len data_moments =',len(data_moments))
			pd2s('len Data_Moments =',len(Data_Moments))
		so(Data_Moments,opj(b,'data_moments_right_ts'))
		#raw_enter()
		


#
#############################################################################





# LOW STEER HIGH STEER









