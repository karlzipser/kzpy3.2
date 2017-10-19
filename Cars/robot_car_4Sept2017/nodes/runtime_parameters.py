# This is used to specifiy caffe mode and data file name information


from kzpy3.utils2 import time_str
from kzpy3.utils2 import opjh
from kzpy3.utils2 import print_stars0
from kzpy3.utils2 import print_stars1
from kzpy3.utils2 import opjD

import os
import numpy as np

computer_name = "MR_Unknown"
try:  
   computer_name = os.environ["COMPUTER_NAME"]
except KeyError: 
   print """********** Please set the environment variable computer_name ***********
   e.g.,
   export COMPUTER_NAME="Mr_Orange"
   """


Car_IP_dic = {'Mr_Blue':'192.168.1.101',
	'Mr_Black':'192.168.1.102',
	'Mr_Orange':'192.168.1.103',
	'Mr_Yellow':'192.168.1.104',
	'Mr_Lt_Blue':'192.168.1.105',
	'Mr_Purple':'192.168.1.106',
	'Mr_TX2':'192.168.1.201'}
Car_termcolor_dic = {'Mr_Blue':('blue','on_white'),
	'Mr_Black':('grey','on_white'),
	'Mr_Orange':('red','on_yellow'),
	'Mr_Yellow':('yellow','on_grey'),
	'Mr_Lt_Blue':('blue','on_cyan'),
	'Mr_Purple':('magenta','on_white'),
	'Mr_TX2':(255,200,150)}
Car_num_dic = {'Mr_Blue':1.0,
	'Mr_Black':2.0,
	'Mr_Orange':3.0,
	'Mr_Yellow':4.0,
	'Mr_Lt_Blue':5.0,
	'Mr_Purple':6.0,
	'Mr_TX2':7.0}
####################### general car settings ################
#
Direct = 1.
Follow = 0.
Play = 0.
Furtive = 0.
Caf = 0.0
Racing = 0.0


weight_file_path = opjh('pytorch_models','epoch6goodnet')
require_Arudinos_MSE = True #!!!!!!!!!!!!!!!
verbose = False
n_avg_IMU = 10
NETWORK = 111
I_ROBOT = 222
who_is_in_charge = I_ROBOT
robot_steer = 49
robot_motor = 58
robot_steer_gain = 0.75
other_car_distance_threshold = 1.0
car_detect_angle = 75
potential_field_png = opjD('markers.35x35.circle.png')
past_to_present_proportion = 0.75
aruco_error_time = 0.35
steer_momentum = 0.5
heading_pause_threshold_angle = 7
heading_float_pause_threshold = 10.95
X_PARAM = 1.0
Y_PARAM = 1.0
HEADING_DELTA_PARAM = 0.1
STEER_FROM_XY = False
radius = 0.5
print_marker_ids = False
print_steer = False
img_width = 35

steer_gain = 1.0
motor_gain = 1.0

#
###################################################################

####################### specific car settings ################
#

#
###################################################################
# 

     


