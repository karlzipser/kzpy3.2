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
image_list = []

nframes = 2 #figure out how to get this from network
    
def right_callback(data):
    global right_list, solver
    cimg = bridge.imgmsg_to_cv2(data,"rgb8")
    if len(right_list) > nframes + 3:
        right_list = right_list[-(nframes + 3):]
    right_list.append(cimg)
def left_callback(data):
    global left_list
    cimg = bridge.imgmsg_to_cv2(data,"rgb8")
    if len(left_list) > nframes + 3:
        left_list = left_list[-(nframes + 3):]
    left_list.append(cimg)
def image_callback(data):
    global image_list
    cimg = bridge.imgmsg_to_cv2(data,"rgb8")
    if len(image_list) > nframes + 3:
        image_list = image_list[-(nframes + 3):]
    image_list.append(cimg)



rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)
rospy.Subscriber("/os1_node/image",Image,image_callback,queue_size = 1)




main_timer = Timer(60*60*24)






while not main_timer.check():
    if len(left_list) > 2:
        time.sleep(0/60.)
        for l,n in zip([left_list,right_list,image_list],['left','right','image']):
            img = l[-1]
            #img.transpose(0, 2)
            #img.transpose(1, 2)
            key_ = mci(img,delay=1,title=n,scale=4)
            #mi(img,n);spause()
            if key_ == ord('q'): sys.exit()



print 'goodbye!'
print "unix(opjh('kzpy3/kill_ros.sh'))"
unix(opjh('kzpy3/kill_ros.sh'))


#EOF

    

