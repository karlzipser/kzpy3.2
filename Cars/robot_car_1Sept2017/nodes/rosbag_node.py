#!/usr/bin/env python
from kzpy3.utils2 import *
import os, sys, shutil, subprocess, time
import rospy
import std_msgs.msg

os.environ['STOP'] = 'False'

time.sleep(3)

if __name__ == '__main__':
    rospy.init_node('rosbag_node', anonymous=True)

    rate = rospy.Rate(0.5)

    while not rospy.is_shutdown():
        rate.sleep()

        except Exception as e:
            print("********** rospy.init_node('rosbag_node', anonymous=True) Exception ***********************")
            print(e.message, e.args)
            os.environ['STOP'] = 'True'
            rospy.signal_shutdown(d2s(e.message,e.args))
            stop_ros()
    stop_ros()

