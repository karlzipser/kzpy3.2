from Parameters_Module import *
from kzpy3.utils2 import *
import roslib
import std_msgs.msg
import geometry_msgs.msg
import rospy
import cv2
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
exec(identify_file_str)

bridge = CvBridge()



_ = dictionary_access



def Ros_Subscriber(*args):
	Args = args_to_dictionary(args)
	D = {}
	True




	return D


#for topics_ in [steer, motor, state, encode, acc, gyro, gyro_heading,]

R = {}

R[steer] = {}
R[steer][ts] = []
R[steer][vals] = []

R[acc_x] = {}
R[acc_x][ts] = []
R[acc_x][vals] = []

R[left_image] = {}
R[left_image][ts] = []
R[left_image][vals] = []

R[right_image] = {}
R[right_image][ts] = []
R[right_image][vals] = []

def steer__callback(msg):
	R[steer][ts].append(time.time())
	R[steer][vals].append(msg.data)







def acc__callback(msg):
	R[acc_x][ts].append(time.time())
	R[acc_x][vals].append(msg.x)










def left_image__callback(data):
	R[left_image][ts].append(time.time())
	R[left_image][vals].append( bridge.imgmsg_to_cv2(data,"bgr8") )

def right_image__callback(data):
	R[right_image][ts].append(time.time())
	R[right_image][vals].append( bridge.imgmsg_to_cv2(data,"bgr8") )













rospy.init_node('listener',anonymous=True)

rospy.Subscriber('/bair_car/steer', std_msgs.msg.Int32, callback=steer__callback)
rospy.Subscriber('/bair_car/acc', geometry_msgs.msg.Vector3, callback=acc__callback)
rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_image__callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_image__callback,queue_size = 1)






D = Display_Graph_Module.Display_Graph(topics,R)
timer=Timer(0)
while True:
	timer.reset()
	D[show]()
	print timer.time()

















#EOF
