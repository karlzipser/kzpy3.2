#!/usr/bin/env python
from kzpy3.utils2 import *
import os, sys, shutil, subprocess, time
import rospy
import std_msgs.msg
import runtime_parameters as rp

os.environ['STOP'] = 'False'

time.sleep(3)

try:
    existing_bag_files = sgg('/media/nvidia/rosbags/*.bag')
    folder_name = existing_bag_files[0].replace('bair_car',rp.computer_name)
    folder_name = '_'.join(folder_name.split('_')[:-1])
    print('mkdir '+folder_name)
    print('mv /media/nvidia/rosbags/*.bag '+folder_name)
except Exception as e:
    print("********** rosbag_node.py Exception ***********************")
    print(e.message, e.args)

if __name__ == '__main__':
    rospy.init_node('rosbag_node', anonymous=True)

    rate = rospy.Rate(0.5)

    while not rospy.is_shutdown():
        rate.sleep()

    stop_ros()

