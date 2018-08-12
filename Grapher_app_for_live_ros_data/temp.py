
from kzpy3.vis2 import *


import roslib
import std_msgs.msg
import geometry_msgs.msg
import rospy
import cv2
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
exec(identify_file_str)
bridge = CvBridge()





R = {}
for topic_ in ['cmd_steer'
	]:
	R[topic_] = {'ts':[0],'vals':[49]}


def steer__callback(msg):
	R['cmd_steer']['ts'].append(time.time())
	R['cmd_steer']['vals'].append(msg.data)


rospy.init_node('listener',anonymous=True)

rospy.Subscriber('/bair_car/cmd/steer', std_msgs.msg.Int32, callback=steer__callback)




while True:
	print R['cmd_steer']['vals'][-1]
	time.sleep(0.2)















#EOF

#EOF