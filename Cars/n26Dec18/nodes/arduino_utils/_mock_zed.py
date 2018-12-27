from kzpy3.utils3 import *
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge,CvBridgeError

rospy.init_node('mock',anonymous=True)

pub = rospy.Publisher("/zed/left/image_rect_color",Image,queue_size=1)

def Mock_ZED():
    while True:
        print "mz"
        time.sleep(1/30.)
        img = np.random.randn(94,168,3)
        img = z2_255(img)
        pub.publish(CvBridge().cv2_to_imgmsg(img,'rgb8'))

Mock_ZED()
#EOF