#!/usr/bin/env python

from kzpy3.utils3 import *

###############################################3
#
P = {}
P['ABORT'] = False
P['customers'] = ['customer0']
P['To Expose'] = {}
#
###############################################3


P['start menu automatically'] = False
P['fig'] = 1
P['l'] = 5.0
P['good_starts'] = [['cool_run_by_metal_bridge',30000],] #[['cool_run_by_metal_bridge',22000],]
P['good_starts'] = [['generic',20000],]
P['start_index_choice'] = 0
P['past_steps'] = 30
P['future_steps'] = 90
P['offset'] = 15
P['step_size'] = 1
P['cmd/clear_screen'] = False
#P['run_folder'] =  opjm('preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_19h55m13s')
if using_linux():
	P['run_folder'] =  '/media/karlzipser/rosbags1/h5py/tegra-ubuntu_20Nov18_10h59m22s'
else:
	P['run_folder'] =  opjD('model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_14h29m56s_local_lrc')
P['load_timer_time'] = 2
P['hide this!'] = 'hide this!'
P['vel-encoding coeficient'] = (1.0/2.3)
P['timer'] = Timer(5)
P['show 2D'] = True
P['show 3D'] = True
P['cv2 delay'] = 33
P['cv2 scale'] = 2
P['backup parameter'] = 1.0
P['step_skip'] = 4
P['index_timer!'] = Timer(5)
#P['To Expose']['customer0'] = ['ABORT','fig','l','good_starts','start_index_choice',
#	'past_steps','future_steps','cmd/clear_screen','offset','step_size']
P['To Expose']['customer0'] = sorted(P.keys())
to_hide = ['To Expose']
for h in to_hide:
	P['To Expose']['customer0'].remove(h)
for k in P.keys():
	if '!' in k:
		P['To Expose']['customer0'].remove(k)

#EOF
