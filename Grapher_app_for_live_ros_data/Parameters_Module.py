from Paths_Module import *
from misc.All_Names_Module import *
exec(identify_file_str)

_ = dictionary_access

P = {}
P['USE_ARUCO'] = False
P['USE_IMAGES'] = True
bair_car_str = '/bair_car'

flex_names = []
for fb in ['F']:
    for lr in ['L','C','R']:
        for i in [0,1,2,3]:
            flex_names.append(d2n(fb,lr,i))
#flex_names.append('xan0')
            
R = {}
for topic_ in ['cmd/steer','cmd/motor','steer', 'motor', 'encoder',
	'acc_x','acc_y','acc_z',
	'gyro_x','gyro_y','gyro_z','button_number',
	gyro_heading_x,gyro_heading_y,gyro_heading_z,
	left_image,right_image
	]+flex_names:
	R[topic_] = {'ts':[],'vals':[]}

acc_color = (255,255,0)
gyro_color = (255,0,255)
P[TOPICS] = {
	steer:{maxval:80,		minval:20,		baseline:49.0,	color:(255,0,0)},
	'cmd/steer':{maxval:80,		minval:20,		baseline:49.0,	color:(255,255,0)},
	'cmd/motor':{maxval:80,		minval:20,		baseline:49.0,	color:(0,255,255)},
	motor:{maxval:80,		minval:49,		baseline:49.0,	color:(0,0,255)},
	'button_number':{maxval:4,		minval:0,		baseline:0,		color:(0,255,0)},
	encoder:{maxval:4,		minval:0,		baseline:0,		color:(255,255,255)},
	acc_x:{maxval:3,		minval:-3,		baseline:0,		color:acc_color},
	acc_y:{maxval:3,		minval:-3,		baseline:0,		color:acc_color},
	acc_z:{maxval:3-9.80,	minval:-3,		baseline:0,		color:acc_color},
	gyro_x:{maxval:30,		minval:-30,	baseline:0,		color:gyro_color},
	gyro_y:{maxval:30,		minval:-30,	baseline:0,		color:gyro_color},
	gyro_z:{maxval:30,		minval:-30,	baseline:0,		color:gyro_color},
	gyro_heading_x:{maxval:45,minval:-45,	baseline:0,		color:(255,200,200)},
	left_ts_deltas:{maxval:0.1,minval:0,	baseline:0,		color:(0,0,255)},
}
ctr = 0
for f in flex_names:
	if 'C' in f:
		b = 0
	elif 'R' in f:
		b = 128
	elif 'L' in f:
		b = 255
	c = bound_value(20.0*ctr,0,255)
	#col = (255*z2o(na([c,255-c,127]))).astype(int)
	col = [c,255-c,b]
	P[TOPICS][f] = {maxval:3000,		minval:-100,	baseline:0,		color:col}
	ctr += 1
##}
P['topic_keys_sorted'] = [
	steer,
	motor,
	'cmd/motor',
	'cmd/steer',
	acc_x,
	acc_y,
	acc_z,
	gyro_x,
	gyro_y,
	gyro_z,
	gyro_heading_x,
	left_ts_deltas,
	encoder,
	'button_number',
	]
P['topic_keys_sorted'] += flex_names

P[X_PIXEL_SIZE] = 400
P[Y_PIXEL_SIZE] = 400
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