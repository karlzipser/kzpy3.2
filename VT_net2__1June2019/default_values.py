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

# walking pace ~= 1.4 m/s
P['distance'] = 0.
P['graphics 1'] = False
P['graphics 2'] = True
P['graphics 3'] = False
P['vel-encoding coeficient'] = (1.0/2.3)
P['graphics_timer time'] = 1/4.
P['save metadata'] = False
P['step_size'] = 1
P['cmd/clear_screen'] = False
P['cv2 delay'] = 1
P['3d image scale'] = 1.0
P['metadata_3D_img scale'] = 8.3
P['Prediction2D_plot scale'] = 8.3
P['num timesteps'] = 9
P['load_timer_time'] = 2
P['U_heading_gain'] = 2.0
P['initial index'] = 4800
P['backup parameter'] = 1.0
P['use center line'] = True
P['cmd/an impulse (click)'] = False
P['show timer time'] = 0
P['add_mode'] = True
P['skip_3D'] = False
P['d_heading_multiplier'] = 8.5
P['plot xylims'] = [-2.5,2.55,-3.,0.1]
P['pts sym'] = '.'
P['To Expose']['VT menu'] = sorted(P.keys())
to_hide = ['To Expose','customers']
for h in to_hide:
	P['To Expose']['VT menu'].remove(h)
for k in P.keys():
	if '!' in k:
		P['To Expose']['VT menu'].remove(k)
P['dst path'] = opjD('Data/Network_Predictions_projected_gain_2')
P['timer'] = Timer(5)
P['vec sample frequency'] = 3.33
P['start menu automatically'] = False
P['show timer'] = Timer(P['show timer time'])
P['wait for start signal'] = False
P['index'] = P['initial index']
P['topic_suffix'] = ''
P['behavioral_mode_list'] = ['left','direct','right']
P['pixels_per_unit'] = 10.
P['num Array pts'] = 300

#EOF
