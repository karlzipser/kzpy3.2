#!/usr/bin/env python
"""
reed to run roslaunch first, e.g.,

roslaunch bair_car bair_car.launch use_zed:=true record:=false
"""

from kzpy3.utils2 import *
import runtime_parameters as rp
import net_utils
########################################################
#          ROSPY SETUP SECTION
import roslib
import std_msgs.msg
import geometry_msgs.msg
#import cv2
from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
bridge = CvBridge()
rospy.init_node('listener',anonymous=True)

left_list = []
right_list = []
nframes = 2 #figure out how to get this from network

def right_callback(data):
    global left_list, right_list, solver
    cimg = bridge.imgmsg_to_cv2(data,"bgr8")
    if len(right_list) > nframes + 3:
        right_list = right_list[-(nframes + 3):]
    right_list.append(cimg)
def left_callback(data):
    global left_list, right_list
    cimg = bridge.imgmsg_to_cv2(data,"bgr8")
    if len(left_list) > nframes + 3:
        left_list = left_list[-(nframes + 3):]
    left_list.append(cimg)

steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=100)
motor_cmd_pub = rospy.Publisher('cmd/motor', std_msgs.msg.Int32, queue_size=100)
rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)




q = '_'
while q not in ['q','Q']:
    print "In main loop (q-enter to quit)"
    time.sleep(0.1)
    q = raw_input('')

    if len(left_list) > nframes + 2:
        camera_data = net_utils.format_camera_data(left_list, right_list)
        metadata = net_utils.format_metadata((rp.Follow, rp.Direct))
        torch_motor, torch_steer = net_utils.run_model(camera_data, metadata)
      
        #steer_cmd_pub.publish(std_msgs.msg.Int32(torch_steer))
        #motor_cmd_pub.publish(std_msgs.msg.Int32(torch_motor))
        print torch_steer,torch_motor
print 'goodbye!'
unix('kzpy3/kill_ros.sh')


    