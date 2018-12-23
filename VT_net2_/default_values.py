#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)



###############################################3
#
_ = {}
_['ABORT'] = False
_['customers'] = ['VT menu']
_['To Expose'] = {}
#
###############################################3

# walking pace = 1.4 m/s

_['plot_range'] = 5.0
_['step_size'] = 1
_['cmd/clear_screen'] = False
_['show 2D'] = True
_['show 3D'] = True
_['cv2 delay'] = 1
_['cv2 scale'] = 4
_['num timesteps'] = 30
_['step_skip'] = 4
_['load_timer_time'] = 2
_['metadata_version'] = False
_['index'] = 7000
_['backup parameter'] = 1.0
_['behavioral_mode_list'] = ['left','direct','right']
_['use center line'] = True
#_['To Expose']['VT menu'] = ['ABORT','fig','plot_range','good_starts','start_index_choice',
#	'past_steps','future_steps','cmd/clear_screen','offset','step_size']
_['To Expose']['VT menu'] = sorted(_.keys())
to_hide = ['To Expose','customers']
for h in to_hide:
	_['To Expose']['VT menu'].remove(h)
for k in _.keys():
	if '!' in k:
		_['To Expose']['VT menu'].remove(k)


_['timer'] = Timer(5)
_['fig'] = 1
#_['run_folder'] =  opjm('preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_19h55m13s')
#_['run_folder'] =  '/media/karlzipser/rosbags1/h5py/tegra-ubuntu_20Nov18_10h59m22s'
#_['run_folder'] = '/home/karlzipser/Desktop/h5py/Mr_Purple_24Nov18_11h48m54s'

_['vec sample frequency'] = 3.33
_['start menu automatically'] = True
_['vel-encoding coeficient'] = (1.0/2.3)

#EOF
