from kzpy3.vis import *
import roslib
import std_msgs.msg
import rospy
rivl='rosrun image_view image_view image:=/bair_car/zed/left/image_rect_color'

steer_list = []

def steer_callback(msg):
	global steer_list
	steer_list.append(msg.data)
	if len(steer_list) > 100:
		steer_list = steer_list[-100:]

rospy.init_node('listener',anonymous=True)

rospy.Subscriber('/bair_car/steer', std_msgs.msg.Int32, callback=steer_callback)


figure(1)

while True:
	plt.clf()
	plot([0,99],[49,49],'r')
	plt.xlim(0,99)
	plt.ylim(0,99)
	plot(steer_list,'b')
	plt.pause(0.02)