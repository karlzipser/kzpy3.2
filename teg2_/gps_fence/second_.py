# This must be done in the same terminal.
# export ROS_MASTER_URI=http://192.168.43.113:11311


from kzpy3.vis import *
import roslib
import std_msgs.msg
import rospy

GPS2_lat = -999.9
GPS2_long = 0
GPS2_speed = 0
GPS2_angle = 0

def GPS2_lat_callback(msg):
	global GPS2_lat
	GPS2_lat = msg.data


rospy.init_node('listener',anonymous=True)
rospy.Subscriber('/bair_car/GPS2_lat', std_msgs.msg.Float32, callback=GPS2_lat_callback)


while not rospy.is_shutdown():
	try:
		print GPS2_lat
		time.sleep(0.5)
	except Exception as e:
		print e.message, e.args

