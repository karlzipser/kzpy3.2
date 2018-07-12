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
human_agent = 1
behavoral_mode = 'direct'
button_number = 1

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
def human_agent_callback(msg):
    global human_agent
    human_agent = msg.data
def button_number_callback(msg):
    global button_number
    button_number = msg.data
def behavioral_mode_callback(msg):
    global behavoral_mode
    behavoral_mode = msg.data

steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=100)
motor_cmd_pub = rospy.Publisher('cmd/motor', std_msgs.msg.Int32, queue_size=100)
rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)
rospy.Subscriber('/bair_car/human_agent', std_msgs.msg.Int32, callback=human_agent_callback)
rospy.Subscriber('/bair_car/button_number', std_msgs.msg.Int32, callback=button_number_callback)
rospy.Subscriber('/bair_car/behavioral_mode', std_msgs.msg.String, callback=behavioral_mode_callback)



reload_timer = Timer(30)
current_steer = 49
current_motor = 49
s = 0.75

main_timer = Timer(60*60*24)
while main_timer.check() == False:
    if reload_timer.check(): # put in thread?
        reload(rp)
        reload_timer.reset()
    if not human_agent:
        if behavioral_mode == 'direct':
            direct = 1.0
            follow = 0.0
        elif behavioral_mode == 'follow':
            direct = 0.0
            follow = 1.0
        else:
            spd2s('unknown behavioral_mode')
        print behavioral_mode
        if len(left_list) > nframes + 2:
            camera_data = net_utils.format_camera_data(left_list, right_list)
            metadata = net_utils.format_metadata((follow, direct))
            torch_motor, torch_steer = net_utils.run_model(camera_data, metadata)

            if 'Do smoothing of percents...':
                current_steer = (1.0-s)*torch_steer + s*current_steer
                current_motor = (1.0-s)*torch_motor + s*current_motor

            adjusted_motor = rp.motor_gain*(current_motor-49) + rp.motor_offset + 49

            steer_cmd_pub.publish(std_msgs.msg.Int32(current_steer))
            motor_cmd_pub.publish(std_msgs.msg.Int32(adjusted_motor))
    else:
        time.sleep(0.1)

print 'goodbye!'
print "unix(opjh('kzpy3/kill_ros.sh'))"
unix(opjh('kzpy3/kill_ros.sh'))


#EOF

    