#!/usr/bin/env python

# This is used to specifiy  mode and data file name information

#from kzpy3.utils2 import *
"""
*allow steer gain
*paramterize which part of motor and steer vector is chosen
*battery pods
*encoder adjustment
attach body
improve body connector
frequency min/max (longer than 1s period)
save steer and motor min and maxes
publish frequencies for all topics, figure out why acceleration is slowing down with network mode.
"""

"""
from kzpy3.utils2 import time_str
"""
from kzpy3.utils2 import opjh
"""
from kzpy3.utils2 import print_stars0
from kzpy3.utils2 import print_stars1
from kzpy3.utils2 import opjD
from kzpy3.utils2 import opjm

import os
import numpy as np
"""

if False:
	computer_name = "MR_Unknown"
	try:  
	   computer_name = os.environ["COMPUTER_NAME"]
	except KeyError: 
	   print """********** Please set the environment variable computer_name ***********
	   e.g.,
	   export COMPUTER_NAME="Mr_Orange"
	   """

#spd2s('reloading runtime_parameters.py')
print 'reloading runtime_parameters.py'
####################### general car settings ################
#
weight_file_path = opjh('pytorch_models','net.infer')

foldername_prefix = 'run_'

output_sample = 4 # >=0, <=9
steer_gain = 4.0
motor_gain = 1.0
motor_offset = -2
network_smoothing_parameter = 0.0


#EOF
