#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)

###############################################3
#
P = {}
_ = P
_['ABORT'] = False
_['customers'] = ['VT menu']
_['To Expose'] = {}
#
###############################################3

# walking pace ~= 1.4 m/s
_['graphics 1'] = True ####TEMP_CHANGE False
_['graphics 2'] = True
_['graphics 3'] = True ####TEMP_CHANGE False
_['save metadata'] = False
_['step_size'] = 1
_['cmd/clear_screen'] = False
_['cv2 delay'] = 1
_['3d image scale'] = 2.0#1.0
_['metadata_3D_img scale'] = 8.3
_['Prediction2D_plot scale'] = 8.3
_['num timesteps'] = 8
_['load_timer_time'] = 2
_['U_heading_gain'] = 2.0
_['initial index'] = 4800
_['backup parameter'] = 1.0
_['use center line'] = True
_['cmd/an impulse (click)'] = False
_['show timer time'] = 0
_['add_mode'] = True
_['skip_3D'] = False
_['d_heading_multiplier'] = 0.535
_['cmd_camera_to_camera_heading_cooeficient'] = 0.75
_['99 mov timer time'] = 1.0
_['To Expose']['VT menu'] = sorted(_.keys())
to_hide = ['To Expose','customers']
for h in to_hide:
	_['To Expose']['VT menu'].remove(h)
for k in _.keys():
	if '!' in k:
		_['To Expose']['VT menu'].remove(k)
_['dst path'] = opjD('Data/Network_Predictions_projected_gain_2')
_['timer'] = Timer(5)
_['vec sample frequency'] = 3.33
_['start menu automatically'] = False
_['vel-encoding coeficient'] = (1.0/2.3)
_['show timer'] = Timer(_['show timer time'])
_['wait for start signal'] = False
_['index'] = _['initial index']
_['topic_suffix'] = ''
_['behavioral_mode_list'] = ['left','direct','right']

#EOF
