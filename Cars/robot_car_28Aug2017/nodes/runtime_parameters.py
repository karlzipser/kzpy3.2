# This is used to specifiy caffe mode and data file name information


from kzpy3.utils2 import time_str
from kzpy3.utils2 import opjh
from kzpy3.utils2 import print_stars0
from kzpy3.utils2 import print_stars1
from kzpy3.utils2 import opjD

import os
import numpy as np
print_stars0();print(__file__);print_stars1()
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
	'Mr_Purple':'192.168.1.106'}
####################### general car settings ################
#
for i in range(1):
	print('*************' + computer_name + '***********')
Direct = 1.
Follow = 0.
Play = 0.
Furtive = 0.
Caf = 0.0
Racing = 0.0
Location =  'generic' #Smyth_tape'

weight_file_path = opjh('pytorch_models','epoch6goodnet')
require_Arudinos_MSE = True #!!!!!!!!!!!!!!!
verbose = False
#use_caffe = True
n_avg_IMU = 10
NETWORK = 111
I_ROBOT = 222
who_is_in_charge = I_ROBOT
robot_steer = 49
robot_motor = 58#49#60
robot_steer_gain = 0.6
potential_field_png = opjD('markers.crop.35x35.png')
past_to_present_proportion = 0.0
steer_momentum = 0.5
heading_pause_threshold_angle = 7
heading_float_pause_threshold = 0.995
X_PARAM = 1.0
Y_PARAM = 1.0
HEADING_DELTA_PARAM = 0.1
STEER_FROM_XY = False
radius = 0.5
#potential_graph_blur = 4
print_marker_ids = False
print_steer = False
img_width = 35

steer_gain = 1.0
motor_gain = 1.0
#acc2rd_threshold = 150

PID_min_max = [1.5,2.5]
motor_freeze_threshold = 55
robot_acc2rd_threshold = 40#20
robot_acc_y_exit_threshold = 3
potential_acc2rd_collision = 10
potential_motor_freeze_collision = 20
acc_y_tilt_event = 1000
#
###################################################################

####################### specific car settings ################
#

#
###################################################################
# 

non_user_section = True
if non_user_section:
	if Direct == 1:
		task = 'direct'
	elif Play == 1:
		task = 'play'
	elif Follow == 1:
		task = 'follow'
	elif Furtive == 1:
		task = 'furtive'
	elif Racing == 1:
		task = 'racing'
	else:
		assert(False)
	foldername = ''
	if Follow == 1:
		foldername = 'follow_'
	model_name = weight_file_path.split('/')[-1]
	if Caf == 1:
		foldername = foldername + 'caffe2_' + model_name +'_'
	foldername = foldername + task + '_'
	foldername = foldername + Location + '_'
	foldername = foldername + time_str() + '_'
	foldername = foldername + computer_name

     


