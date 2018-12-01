from kzpy3.vis3 import *
exec(identify_file_str)

import roslib
import std_msgs.msg
import geometry_msgs.msg
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



rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)




main_timer = Timer(60*60*24)
frequency_timer = Timer(1.0)
print_timer = Timer(5)






low_frequency_pub_timer = Timer(0.5)
low_frequency_pub_timer2 = Timer(0.5)

#net_utils.init_model(N) 

while not main_timer.check():
    if len(left_list) > 2:
        time.sleep(0/60.)
        key_ = mci(left_list[-1],color_mode=cv2.COLOR_RGB2BGR,delay=1,title='topics')


print 'goodbye!'
print "unix(opjh('kzpy3/kill_ros.sh'))"
unix(opjh('kzpy3/kill_ros.sh'))


#EOF

    

