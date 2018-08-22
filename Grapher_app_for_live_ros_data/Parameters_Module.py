from Paths_Module import *
from misc.All_Names_Module import *
exec(identify_file_str)

_ = dictionary_access

P = {}
P['USE_ARUCO'] = False
P['USE_IMAGES'] = False

flex_names = []
for fb in ['f','b']:
    for lr in ['l','r','c']:
        for i in [0,1]:
            flex_names.append(d2n('x',fb,lr,i))
flex_names.append('xan0')
            
R = {}
for topic_ in ['cmd_steer','steer', 'motor', 'state', 'encoder',
	'acc_x','acc_y','acc_z',
	'gyro_x','gyro_y','gyro_z',
	gyro_heading_x,gyro_heading_y,gyro_heading_z,
	left_image,right_image
	]+flex_names:
	R[topic_] = {'ts':[],'vals':[]}

P[TOPICS] = {
	steer:{maxval:80,		minval:20,		baseline:49.0,	color:(255,0,0)},
	'cmd_steer':{maxval:80,		minval:20,		baseline:49.0,	color:(0,255,0)},
	motor:{maxval:80,		minval:49,		baseline:49.0,	color:(0,0,255)},
	state:{maxval:6,		minval:-10,		baseline:0,		color:(128,128,128)},
	encoder:{maxval:4,		minval:0,		baseline:0,		color:(0,128,128)},
	acc_x:{maxval:10,		minval:-10,		baseline:0,		color:(128,128,0)},
	acc_y:{maxval:10,		minval:-10,		baseline:0,		color:(128-32,128+32,0)},
	acc_z:{maxval:10-9.80,	minval:-10,		baseline:0,		color:(128-64,128+64,0)},
	gyro_x:{maxval:180,		minval:-180,	baseline:0,		color:(128,128,0)},
	gyro_y:{maxval:180,		minval:-180,	baseline:0,		color:(128-32,128+32,0)},
	gyro_z:{maxval:180,		minval:-180,	baseline:0,		color:(128-64,128+64,0)},
	gyro_heading_x:{maxval:360,minval:-180,	baseline:0,		color:(255,200,200)},
	left_ts_deltas:{maxval:0.1,minval:0,	baseline:0,		color:(0,0,255)},
	'xfl0':{maxval:100,		minval:-50,	baseline:0,		color:(255,255,255)},
	'xfl1':{maxval:100,		minval:-50,	baseline:0,		color:(255,255,255)},
	'xfc0':{maxval:100,		minval:-50,	baseline:0,		color:(255,255,255)},
	'xan0':{maxval:100,		minval:-50,	baseline:0,		color:(255,255,0)},
	'xfr0':{maxval:100,		minval:-50,	baseline:0,		color:(255,255,255)},
	'xfr1':{maxval:100,		minval:-50,	baseline:0,		color:(255,255,255)},
	'xbl0':{maxval:100,		minval:-50,	baseline:0,		color:(255,255,255)},
	'xbl1':{maxval:100,		minval:-50,	baseline:0,		color:(255,255,255)},
	'xbr0':{maxval:100,		minval:-50,	baseline:0,		color:(255,255,255)},
	'xbr1':{maxval:100,		minval:-50,	baseline:0,		color:(255,255,255)},
}
P['topic_keys_sorted'] = [
	acc_x,
	acc_y,
	acc_z,
	gyro_x,
	gyro_y,
	gyro_z,
	'cmd_steer',
	steer,
	motor,

	gyro_heading_x,
	left_ts_deltas,
	encoder,
	'xfl0',
	'xfl1',
	'xfc0',
	'xan0',
	'xfr0',
	'xfr1',
	'xbl0',
	'xbl1',
	'xbr0',
	'xbr1',
]

P[X_PIXEL_SIZE] = 800
P[Y_PIXEL_SIZE] = 800
P[SCREEN_X] = 20
P[SCREEN_Y] = 40
P[CAMERA_SCALE] = 1
P[SHOW_MARKER_ID] = False
P[TOPIC_STEPS_LIMIT] = 5000
P['TIME_RANGE'] = 15




"""
use one terminal window with different tabs:

$ roscore
____
$ rosbag play /media/karlzipser/rosbags/Mr_Lt_Blue_16_50_29Aug2017/processed2/Mr_Lt_Blue_16_50_29Aug2017/*.bag
____
$ python kzpy3/Grapher_app/Main.py 


[press 'q' while mouse is in graphics window to quit]


next,
$ python kzpy3/Grapher_app_3rd_pass/Main.py

[this shows the h5py version of the data and gives access at any timepoint.]
"""



#EOF