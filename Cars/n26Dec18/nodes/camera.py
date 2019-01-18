#!/usr/bin/env python
from kzpy3.vis3 import *
exec(identify_file_str)

import rospy
import torch
import roslib
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
bridge = CvBridge()
import cv2

ga = getattr
sa = setattr

class C:
    def __init__(self):
        pass


class CameraShot:
    def __init__(self,data):
        self.ts = time.time()
        if False:
            self.img = data
        else:
            self.img = bridge.imgmsg_to_cv2(data,'rgb8')

Zed = C()
Zed.left = []
Zed.right = []
L = {}
L['left_ready'] = False

def zed_lst_lim(zed,side,max_len,min_len):
    l = ga(zed,side)
    if len(l) > max_len:
        sa(zed,side,l[-min_len:])

def left_callback(data):
    #global left_ready
    Zed.left.append(CameraShot(data))
    zed_lst_lim(Zed,'left',4,2)
    L['left_ready'] = True

def right_callback(data):
    Zed.right.append(CameraShot(data))
    zed_lst_lim(Zed,'right',4,2)

bcs = '/bair_car'
rospy.init_node('camera',anonymous=True,disable_signals=True)
rospy.Subscriber(bcs+"/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber(bcs+"/zed/left/image_rect_color",Image,left_callback,queue_size = 1)

hz = Timer(3)

while True:
    
    #if L['left_ready']:
    #    cr(1)
    for side in ['left']:

        if len(Zed.left) > 0 and L['left_ready']:
            L['left_ready'] = False
            #cr(0)
            hz.freq()
            mci(Zed.left[-1].img,delay=1)
            




#EOF

    