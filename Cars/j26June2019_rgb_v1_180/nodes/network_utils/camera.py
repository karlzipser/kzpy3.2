#!/usr/bin/env python
########################## 70 ########################################
from kzpy3.vis3 import *
import default_values
import rospy
import torch
import torch.autograd
import cv_bridge
from sensor_msgs.msg import Image
import kzpy3.VT_net2__1June2019.rectangles as rectangles

exec(identify_file_str)

full_width,full_height = 690/2,64


bridge = cv_bridge.CvBridge()

num_rectangle_patterns = 4
Rectangles = rectangles.Random_black_white_rectangle_collection(
    num_rectangle_patterns=num_rectangle_patterns
)


rgb_v1_list = []
def rgb_v1_callback(data):
    global rgb_v1_list
    img = bridge.imgmsg_to_cv2(data,'rgb8')
    img[:,:,2] = 0
    img = img[:,full_width/2:-full_width/2,:]
    rgb_v1_list.append(img)
    if len(rgb_v1_list) > 4:
        rgb_v1_list = rgb_v1_list[-4:]


rospy.Subscriber(
    "/os1_node/rgb_v1",
    Image,
    rgb_v1_callback,
    queue_size = 1)






        

#EOF