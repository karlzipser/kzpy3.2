import rospy
import std_msgs.msg


def callback(data):
	print data.data

rospy.init_node('test',anonymous=True)

cmd_steer_sub = rospy.Subscriber('cmd/steer', std_msgs.msg.Int32, callback)

rospy.spin()