#!/usr/bin/env python
from kzpy3.vis3 import *
exec(identify_file_str)
import roslib
import std_msgs.msg
import geometry_msgs.msg
from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
bridge = CvBridge()


for k in [('s',3600),('scale',1),('topic',"/bair_car/zed/left/image_rect_color")]:
    if k[0] not in Arguments:
         Arguments[k[0]] = k[1]

rospy.init_node('listener',anonymous=True)

image_list = []

def image_callback(data):
    global image_list
    cimg = bridge.imgmsg_to_cv2(data,"rgb8")
    if len(image_list) > 2 + 3:
        image_list = image_list[-(2 + 3):]
    image_list.append(cimg)

rospy.Subscriber(Arguments['topic'],Image,image_callback,queue_size = 1)



main_timer = Timer(Arguments['s'])
waiting = Timer(1)

while not main_timer.check():
    if len(image_list) > 2:
        img = image_list[-1]
        key_ = mci(img,delay=33,title=Arguments['topic'],scale=Arguments['scale'])
        if key_ == ord('q'): sys.exit()
    else:
        waiting.message('waiting for data...')

cb('\nDone.\n')
#EOF

    

