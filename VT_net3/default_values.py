#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)

###############################################3
#
P = {}
P = P
P['ABORT'] = False
P['customers'] = ['VT menu']
P['To Expose'] = {}
#
###############################################3

# walking pace ~= 1.4 m/s
P['save metadata'] = False
P['step_size'] = 1
P['cmd/clear_screen'] = False
P['cv2 delay'] = 1
P['3d image scale'] = 1.0
P['num timesteps'] = 900
P['load_timer_time'] = 2
P['U_heading_gain'] = 2.0
P['index'] = 9000
P['backup parameter'] = 1.0
P['behavioral_mode_list'] = ['left','direct','right']
P['use center line'] = True
P['cmd/an impulse (click)'] = False
P['show timer time'] = 0
P['To Expose']['VT menu'] = sorted(P.keys())
to_hide = ['To Expose','customers']
for h in to_hide:
	P['To Expose']['VT menu'].remove(h)
for k in P.keys():
	if '!' in k:
		P['To Expose']['VT menu'].remove(k)
P['dst path'] = opjD('Data/Network_Predictions_projected_gain_2')
P['timer'] = Timer(5)
P['net sample frequency'] = 3.33
P['start menu automatically'] = True
P['vel-encoding coeficient'] = (1.0/2.3)
P['show timer'] = Timer(P['show timer time'])
P['wait for start signal'] = False
P['USE_ROS'] = True

#EOF
