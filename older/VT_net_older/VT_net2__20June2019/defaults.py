#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)

Q = {
	'TO_EXPOSE': {
		'ABORT': False,
		'customers': ['VT menu'],
		'distance': 0.,
		'graphics 1': False,
		'graphics 2': True,
		'graphics 3': False,
		'slow_encoder_s': 0.5,
		'stop_timer_time': 0.5,
		'slow_encoder_wait': 0.5,
		'point_lifetime': 20,
		'circle_lifetime': 5,
		'vel-encoding coeficient': 0.5,
		'graphics_timer time': 1/4.,
		'save metadata': False,
		'step_size': 1,
		'cmd/clear_screen': False,
		'cv2 delay': 1,
		'3d image scale': 1.0,
		'metadata_3D_img scale': 8.3,
		'Prediction2D_plot scale': 8.3,
		'num timesteps': 9,
		'U_heading_gain': 2.0,
		'initial index': 0,
		'backup parameter': 0.5,
		'use center line': True,
		'show timer time': 0,
		'add_mode': True,
		'skip_3D': False,
		'd_heading_multiplier': 10.5,
		'plot xylims': [-2.5,2.55,-3.,0.1],
		'pts sym': '.',
	},
	'TO_HIDE': {
		'dst path': opjD('Data/Network_Predictions_projected_gain_2'),
		'timer': Timer(5),
		'vec sample frequency': 3.33,
		'start menu automatically': False,
		'wait for start signal': False,
		'index': 0,
		'topic_suffix': '',
		'behavioral_mode_list': ['left','direct','right'],
		'pixels_per_unit': 20.,
		'num Array pts': 300,
		'load_timer_time': 2,
	},
}


#EOF
