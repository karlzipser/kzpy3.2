from kzpy3.utils3 import *
exec(identify_file_str)

P = {}
P['resume from saved state'] = True
P['to_expose'] = []
P['to_hide'] = ['to_expose','to_hide','The menu path.']

for k in P.keys():
	if k not in P['to_hide']:
		P['to_expose'].append(k)

P['GPU'] = 1
P['num_input_timesteps'] = 60
P['plot individual run data'] = False
P['plot concatenated run data'] = False
P['input_indicies'] = na(range(-P['num_input_timesteps'],0))
P['target_index_range'] = na(range(0,30,3))
P['timeindex_offset'] = 0
if using_linux():
	P['dataset path'] = '/media/karlzipser/rosbags/flex_sensors_Aug2018'
else:
	P['dataset path'] = '/Volumes/transfer/flex_sensors_Aug2018/'
P['good_timestep_proportion'] = 0.8
P['processed data location'] = opjk(pname(__file__),'__local__')

P['topics'] = [
	 'acc_x',
	 'acc_y',
	 'acc_z',
	 'encoder',
	 'gyro_x',
	 'gyro_y',
	 'gyro_z',
	 'cmd_steer',
	 'cmd_motor',
	 'gyro_heading_x',
	 'gyro_heading_y',
	 'gyro_heading_z',
	 'drive_mode',
	 'human_agent',
	 'motor',
	 'steer',
	 'xfc0',
	 'xfl0',
	 'xfl1',
	 'xfr0',
	 'xfr1',
	]


P['input_lst'] = [
	'IMU_mag',
	'encoder',
	#'cmd_steer',
	#'cmd_motor',
	#'motor',
	#'steer',
	'xfc0',
	'xfl0',
	'xfl1',
	'xfr0',
	'xfr1',
]
P['target_lst'] = [
	'steer',
	'motor',
]
