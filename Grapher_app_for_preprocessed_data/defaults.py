from Paths_Module import *
from misc.All_Names_Module import *
exec(identify_file_str)



Q = {
	'VERBOSE':	True,
	'TOPICS': {
		steer:{maxval:80,		minval:20,		baseline:49.0,	color:(255,0,0)},
		motor:{maxval:80,		minval:49,		baseline:49.0,	color:(0,255-32,32)},
		'cmd_steer':{maxval:80,		minval:20,		baseline:49.0,	color:(255,0,0)},
		'cmd_motor':{maxval:80,		minval:49,		baseline:49.0,	color:(0,255,0)},
		'drive_mode':{maxval:1,		minval:-10,		baseline:0,	color:(255,255,255)},
		'human_agent':{maxval:1,		minval:-10,		baseline:0,	color:(0,255,255)},
		'button_number':{maxval:6,		minval:-10,		baseline:0,		color:(255,255,255)},
		encoder:{maxval:4,		minval:-4,		baseline:0,		color:(0,128,128)},
		acc_x:{maxval:10,		minval:-10,		baseline:0,		color:(128,128,0)},
		acc_y:{maxval:10,		minval:-10,		baseline:0,		color:(128-32,128+32,0)},
		acc_z:{maxval:10-9.80,	minval:-10,		baseline:0,		color:(128-64,128+64,0)},
		gyro_x:{maxval:180,		minval:-180,	baseline:0,		color:(128,128,0)},
		gyro_y:{maxval:180,		minval:-180,	baseline:0,		color:(128-32,128+32,0)},
		gyro_z:{maxval:180,		minval:-180,	baseline:0,		color:(128-64,128+64,0)},
		gyro_heading_x:{maxval:(2*360),minval:-360,	baseline:0,		color:(255,200,200)},
		left_ts_deltas:{maxval:0.5,minval:0,	baseline:0,		color:(255,255,255)},
		#heading_pause:{maxval:1,minval:0,	baseline:0,		color:(255,255,19)},
		#car_in_range:{maxval:1,minval:0,	baseline:0,		color:(255,0,0)},
		#aruco_position_x:{maxval:-4,minval:4,	baseline:0,		color:(0,0,255)},
		#aruco_position_y:{maxval:-4,minval:4,	baseline:0,		color:(0,100,155)},
		#other_car_position_x:{maxval:-4,minval:4,	baseline:0,		color:(0,255,100)},
		#other_car_position_y:{maxval:-4,minval:4,	baseline:0,		color:(0,255,100)},
	},
	'VERTICAL_LINE_PROPORTION' : 0.5,
	'X_PIXEL_SIZE' : 800,#1500
	'Y_PIXEL_SIZE' : 800,#1100#2000#1100
	'SCREEN_X' : 20,
	'SCREEN_Y' : 40,
	'MOUSE_MOVE_TIME' : 0,
	'MOUSE_X' : 0,
	'MOUSE_Y' : 0,
	'REAL_TIME_DTV' : -2/30.,
	'CAMERA_SCALE' : 4,
	'Y_MOUSE_RANGE_PROPORTION' : 0.5,
	'ICONS' : [],
	'MAX_ICONS_PER_ROW' : 14,
	'CV2_KEY_COMMANDS' : {
		'p':("START_TIME -= REAL_TIME_DTV; END_TIME -= REAL_TIME_DTV",
			"Time step forward,real time"),
		'm':("START_TIME -= REAL_TIME_DTV/2.0; END_TIME -= REAL_TIME_DTV/2.0",
			"Time step forward,real time"),
		'l':("START_TIME -= dt_; END_TIME -= dt_",
			"Time step forward"),
		'h':("START_TIME += dt_; END_TIME += dt_",
			"Time step back"),
		'u':("START_TIME += 'REAL_TIME_DTV'; END_TIME += REAL_TIME_DTV",
			"Time step back, real time"),
		'v':("START_TIME += 'REAL_TIME_DTV'/2.0; END_TIME += REAL_TIME_DTV/2.0",
			"Time step back, real time"),
		'j':("START_TIME += 100.0*dt_; END_TIME -= 100.0*dt_",
			"Time scale out"),
		'k':("START_TIME -= 100.0*dt_; END_TIME += 100.0*dt_",
			"Time scale in"),
		' ':("""
	'VERTICAL_LINE_PROPORTION'=0.5
	'START_TIME','END_TIME' = 'START_TIME_INIT','END_TIME_INIT'
	ymin_,ymax_ = ymin_init_,ymax_init_
	show_menuv = True""",
			"Reset"),
		'a':("show_menuv = True","Menu"),
		'q':("sys.exit()","Quit"),
	}
}





#EOF