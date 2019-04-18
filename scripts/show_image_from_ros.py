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



ROS_initalized = False



image_list = []




def image_callback(data):
    global image_list
    cimg = bridge.imgmsg_to_cv2(data,"rgb8")
    if len(image_list) > 2 + 3:
        image_list = image_list[-(2 + 3):]
    image_list.append(cimg)





def action(topic,scale=1,delay=33,s=3600):
    global ROS_initalized
    if not ROS_initalized:
        rospy.Subscriber(topic,Image,image_callback,queue_size = 1)
        rospy.init_node('show_image_from_ros_'+str(np.random.randint(1000000)),anonymous=True)
        ROS_initalized = True

    main_timer = Timer(s)

    waiting = Timer(1)

    while not main_timer.check():

        if len(image_list) > 2:
            img = image_list[-1]
            #mi(img);spause()
            q = mci(img,delay=33,title=topic,scale=scale)
            if q == ord('q'):
                sys.exit()
        else:
            waiting.message('waiting for data...')






if __name__ == '__main__':

    Defaults = {'s':3600,'scale':1,'delay':33,'topic':"/bair_car/zed/left/image_rect_color"}
    for k in Defaults:
        if k not in Arguments:
            Arguments[k] = Defaults[k]
    for k in Arguments:
        if type(Arguments[k]) == str:
            Argk = d2n("'",Arguments[k],"'")
        else:
            Argk = Arguments[k]
        exec_str = d2s(k,'=',Argk)
        cg(exec_str)
        exec(exec_str)

    action(topic,scale,delay,s)

    cb('\nDone.\n')
#EOF

    

