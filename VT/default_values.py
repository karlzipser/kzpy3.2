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

################### POTENTIALLY EXPOSED ############################3
#
P['start menu automatically'] = True
P['fig'] = 1
P['l'] = 5.0
P['start_index_choice'] = 0
P['past_steps'] = 30
P['future_steps'] = 90
P['offset'] = 15
P['step_size'] = 1
P['cmd/clear_screen'] = False
P['load_timer_time'] = 2
P['vel-encoding coeficient'] = (1.0/2.3)
P['show 2D'] = False
P['show 3D'] = True
P['cv2 delay'] = 1#33
P['cv2 scale'] = 2
P['backup parameter'] = 1.0
P['step_skip'] = 4

##################### expose/hide ###########################
#
P['To Expose']['customer0'] = sorted(P.keys())
to_hide = ['To Expose']
for h in to_hide:
	P['To Expose']['customer0'].remove(h)
for k in P.keys():
	if '!' in k:
		P['To Expose']['customer0'].remove(k)
#
####################################################

################### NOT EXPOSED ############################
#
P['index_timer!'] = Timer(5)
P['angs'] = []
P['timer'] = Timer(5)
if using_linux():
	#P['run_folder'] =  opjm('preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_19h55m13s')
	#P['run_folder'] =  '/media/karlzipser/rosbags1/h5py/tegra-ubuntu_20Nov18_10h59m22s'
	#P['run_folder'] =  opjm('2_TB_Samsung_n3/rosbags__preprocessed_data/tu_15to16Nov2018/locations/local/left_direct_stop/h5py/tegra-ubuntu_15Nov18_20h55m02s')
	P['run_folder'] =  opjD('Data/16Nov2018_held_out_data/h5py/tegra-ubuntu_16Nov18_17h59m10s')
else:
	P['run_folder'] =  opjD('model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_14h29m56s_local_lrc')
#P['good_starts'] = [['cool_run_by_metal_bridge',30000],] #[['cool_run_by_metal_bridge',22000],]
P['good_starts'] = [['generic',12000],]
#
####################################################

#EOF
