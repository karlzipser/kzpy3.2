#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)
###############################################3
#
P = {}
P['ABORT'] = False
P['customers'] = ['VT menu']
P['To Expose'] = {}
#
###############################################3

# walking pace = 1.4 m/s

P['plot_range'] = 5.0
P['step_size'] = 1
P['cmd/clear_screen'] = False
P['show 2D'] = True
P['show 3D'] = True
P['cv2 delay'] = 1
P['cv2 scale'] = 4
P['num timesteps'] = 30
P['step_skip'] = 4
P['load_timer_time'] = 2
P['metadata_version'] = True
P['index'] = 5000
P['backup parameter'] = 1.0
#P['To Expose']['VT menu'] = ['ABORT','fig','plot_range','good_starts','start_index_choice',
#	'past_steps','future_steps','cmd/clear_screen','offset','step_size']
P['To Expose']['VT menu'] = sorted(P.keys())
to_hide = ['To Expose','customers']
for h in to_hide:
	P['To Expose']['VT menu'].remove(h)
for k in P.keys():
	if '!' in k:
		P['To Expose']['VT menu'].remove(k)


P['timer'] = Timer(5)
P['fig'] = 1
#P['run_folder'] =  opjm('preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_19h55m13s')
#P['run_folder'] =  '/media/karlzipser/rosbags1/h5py/tegra-ubuntu_20Nov18_10h59m22s'
#P['run_folder'] = '/home/karlzipser/Desktop/h5py/Mr_Purple_24Nov18_11h48m54s'

P['vec sample frequency'] = 3.33
P['start menu automatically'] = True
P['vel-encoding coeficient'] = (1.0/2.3)

#EOF
