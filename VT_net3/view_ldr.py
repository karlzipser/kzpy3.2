from kzpy3.vis3 import *
exec(identify_file_str)

import roslib
import std_msgs.msg
from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
bridge = CvBridge()

rospy.init_node('listener',anonymous=True)
    
img = False

def ldr_callback(data):
    global img
    img = bridge.imgmsg_to_cv2(data,"rgb8")

rospy.Subscriber("/ldr_img",Image,ldr_callback,queue_size = 1)

while type(img) == bool:
    time.sleep(1)
while True:
    k = mci(img,color_mode=cv2.COLOR_RGB2BGR,delay=33,title='ldr',scale=8)
    if ord('q') == k:
        break

print 'goodbye!'



#EOF

    

