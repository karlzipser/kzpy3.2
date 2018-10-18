from Paths_Module import *
#from All_Names_Module import *
exec(identify_file_str)

"""
Zed output = (376, 672, 3)
network input = (94, 168, 3)
"""

P = {}

P['SINGLE_VALUE_TOPICS'] = [
	'button_number',
	'drive_mode', 
	'human_agent',
	'steer',
	'state',
	'motor',
	'potential_collision',
	'encoder',
	'aruco_heading_x',
	'aruco_heading_y',
	'aruco_position_x',
	'aruco_position_y',
	'cmd/heading_pause',
	'cmd/car_in_range',
	'cmd/steer',
	'cmd/motor',
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
	'GPS_latitudeDegrees',
	'GPS_longitudeDegrees',
	'GPS_speed',
	'GPS_angle',
	'GPS_altitude',
	'GPS_fixquality',
	'GPS_satellites',
]

P['VECTOR3_TOPICS'] = ['acc','gyro','gps','gyro_heading','other_car_position','os1_node/points']

P['STRING_TOPICS'] = ['behavioral_mode','place_choice',]

P['string_to_num_dic'] = {'behavioral_mode':{'False':0,'direct':2,'follow':4,'furtive':5,'play':6,'left':3,'right':1},'place_choice':{'False':0,'local':1,'home':2,'Tilden':3,'campus':4,'arena':5,'other':6,}}

P['MEO_PARAMS'] = {'acc_x':50,'acc_y':50,'acc_z':50,'gyro_x':50,'gyro_y':50,'gyro_z':50,'gyro_heading_x':50,'gyro_heading_y':50,'gyro_heading_z':50,'encoder':200,}

P['USE_ARUCO'] = False


#EOF