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



# high steer low steer



# making data moment lists like aruco data for older data

"""
{'behavioral_mode': 'racing',
 'left_ts_index': (1506212011.0179999, 4605),
 'motor': 51,
 'right_ts_index': (1506212011.0409999, 4605),
 'run_name': 'Mr_Lt_Blue_2017-09-23-17-10-51',
 'steer': 11}


good data moment:
	select time interval: value should be within 20 percent
	80 percent of timepoint should be in state 1

Do I want non-linear time sampling? No.

input: num. sample points, time tolerance, state 1 tolerance

when in state 4, use previous motor and steer values because state 4 gives wild numbers

When not in state 1, maintain previous state 1 target values.

First sample must be in state 1.

"""


def get_good_data_moment_indicies(L=None,steps=0,time_tolerance=0,state_tolerance=0):
	for i in range(0,len(L['ts'])-steps):

		print L['state'][i]

def is_this_a_good_data_moment(L=None,index=0,steps=0,time_percent_tolerance=0,state_percent_tolerance=0):
	start_time = L['ts'][index]
	end_time = L['ts'][index+steps-1]
	d_time = end_time - start_time
	expected_time = steps * 1/30.0
	if abs(expected_time - d_time) > time_proportion_tolerance * expected_time:
		return False

	state_1s = 0
	for i in range(index,index + steps):
		if abs(L['state'] - 1.0) < 0.1:
			state_1s += 1




