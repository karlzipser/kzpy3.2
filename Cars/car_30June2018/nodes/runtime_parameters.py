# This is used to specifiy  mode and data file name information


from kzpy3.utils2 import time_str
from kzpy3.utils2 import opjh
from kzpy3.utils2 import print_stars0
from kzpy3.utils2 import print_stars1
from kzpy3.utils2 import opjD
from kzpy3.utils2 import opjm

import os
import numpy as np

#print_stars0();print(__file__);print_stars1()
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
#weight_file_path = opjm('rosbags','net.infer')
weight_file_path = opjh('pytorch_models','net.infer')
require_Arudinos_MSE = True #!!!!!!!!!!!!!!!


Direct = 1.
Follow = 0.
Play = 0.
Furtive = 0.
Caf = 0.0
Racing = 0.0

steer_gain = 1.0
motor_gain = 1.0
motor_offset = 5

gyro_freeze_threshold = 150
acc_freeze_threshold_x = 14
acc_freeze_threshold_y_max = 30
acc_freeze_threshold_y_min = 0
acc_freeze_threshold_z = 14
motor_freeze_threshold = 55
n_avg_IMU = 10


