from kzpy3.utils3 import *
exec(identify_file_str)

P = {}
P['ABORT'] = False # this way in Menu_app
P['LIVE'] = False
P['TRAIN'] = not P['LIVE']
P['autostart menu'] = False # this way in Menu_app
P['autostart menu thread'] = False # this way in Menu_app
P['cmd/resume from saved state.'] = True
P['cmd/num epochs.'] = 50
P['cmd/initalize net.'] = False
P['cmd/start training,'] = False
P['cmd/pause training,'] = False
P['cmd/loss_timer,'] = Timer(10)
P['cmd/epoch timer,'] = Timer(15*60)
P['cmd/target output timer,'] = Timer(1)

P['path/processed data location.'] = opjk(pname(__file__),'__local__')
P['path/the menu path.'] = None
if using_linux():
	P['path/dataset path.'] = '/media/karlzipser/rosbags/flex_sensors_Aug2018'
else:
	P['path/dataset path.'] = '/Volumes/transfer/flex_sensors_Aug2018/'
P['path/weight out path'] = None

P['net/net!'] = None
P['net/criterion!'] = None
P['net/optimizer!'] = None
P['net/loss!'] = None
P['net/outputs!'] = None
P['net/loss list!'] = []
P['net/num input timesteps.'] = 60
P['net/hidden_size.'] = 250
P['net/batch size.'] = 100
P['net/initial learning rate.'] = 0.1
P['net/input lst.'] = [
	'xfc0',
	'xfl0',
	'xfl1',
	'xfr0',
	'xfr1',
]
P['net/input size.'] = P['net/num input timesteps.']*len(P['net/input lst.'])

P['net/target lst.'] = [
	'steer',
	'motor',
]
P['net/input indicies.'] = na(range(-P['net/num input timesteps.'],0))
P['net/target index range.'] = na(range(0,30,3))
P['net/output size.'] = len(P['net/target index range.'])*len(P['net/target lst.'])



P['plt/plot individual run data,'] = False
P['plt/plot concatenated run data,'] = False




P['dat/timeindex offset.'] = 0
P['dat/good timestep proportion.'] = 0.8
P['dat/sig sorted value,'] = 264000/4
P['dat/topics.'] = [
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



P['values in filename.'] = [
'net/hidden_size',
'net/batch_size',
'net/num_input_timesteps',

	'hidden_size',
	'batch_size',
	'num_input_timesteps',
	'target_index_range',
	'input_lst',
	'target_lst',
	'net/input_lst',
	'net/target_lst',
]

P['sys/GPU.'] = 0
if username == 'nvidia':
	P['sys/GPU.'] = 0
P['sys/GPU.'] = 0

P['to_expose'] = []  # this way in Menu_app
P['to_hide'] = ['to_expose','to_hide']  # this way in Menu_app
for t in P:
	if type(P[t]) == list:
		P['to_hide'].append(t)
	elif  type(P[t]) == dict:
		P['to_hide'].append(t)
	elif  type(P[t]) == np.ndarray:
		P['to_hide'].append(t)
	elif 'timer' in t:
		P['to_hide'].append(t)
	elif '!' in t:
		P['to_hide'].append(t)
for t in P:
	if t not in P['to_hide']:
		P['to_expose'].append(t)



for t in P:
	print d2n("P['",t,"']")
"""
P`cmd/num epochs. = 50
P['cmd/num epochs.'] = 50
num_epochs = 50
"""

