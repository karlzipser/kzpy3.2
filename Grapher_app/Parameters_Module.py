from Paths_Module import *
from All_Names_Module import *
exec(identify_file_str)

_ = dictionary_access

P = {}

_(P,VERBOSE,equals,True)
P[DATASET_PATHS] = [opjD('bdd_car_data_July2017_LCR')]
#P[DATASET_PATHS] = [opjm('ExtraDrive2/bdd_car_data_July2017_LCR')]
#P[DATASET_PATHS] = [opjm('ExtraDrive2/bair_car_data_Main_Dataset')]
#P[DATASET_PATHS] = [opjm('ExtraDrive2/bdd_car_data_July2017_regular')]
P[TOPICS] = {
	steer:{maxval:80,		minval:20,		baseline:49.0,	color:(255,0,0)},
	motor:{maxval:80,		minval:49,		baseline:49.0,	color:(0,255-32,32)},
	state:{maxval:6,		minval:-10,		baseline:0,		color:(128,128,128)},
	encoder:{maxval:4,		minval:-4,		baseline:0,		color:(0,128,128)},
	acc_x:{maxval:10,		minval:-10,		baseline:0,		color:(128,128,0)},
	acc_y:{maxval:10,		minval:-10,		baseline:0,		color:(128-32,128+32,0)},
	acc_z:{maxval:10-9.80,	minval:-10,		baseline:0,		color:(128-64,128+64,0)},
	gyro_x:{maxval:180,		minval:-180,	baseline:0,		color:(128,128,0)},
	gyro_y:{maxval:180,		minval:-180,	baseline:0,		color:(128-32,128+32,0)},
	gyro_z:{maxval:180,		minval:-180,	baseline:0,		color:(128-64,128+64,0)},
	gyro_heading_x:{maxval:360,minval:-180,	baseline:0,		color:(255,200,200)},
	left_ts_deltas:{maxval:0.1,minval:0,	baseline:0,		color:(0,0,255)},
	}
#P[VERTICAL_LINE_PROPORTION] = 0.5
P[X_PIXEL_SIZE] = 800
P[Y_PIXEL_SIZE] = 800
P[SCREEN_X] = 20
P[SCREEN_Y] = 40
P[CAMERA_SCALE] = 1
P[SHOW_MARKER_ID] = False
"""
P[MOUSE_MOVE_TIME] = 0
P[MOUSE_X] = 0
P[MOUSE_Y] = 0
P[REAL_TIME_DTV] = -2/30.

P[Y_MOUSE_RANGE_PROPORTION] = 0.5
P[ICONS] = []
P[MAX_ICONS_PER_ROW] = 14
"""

P[TOPIC_STEPS_LIMIT] = 5000




#EOF