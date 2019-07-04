#!/usr/bin/env python
from kzpy3.utils3 import *
import rospy
import std_msgs.msg
from std_msgs.msg import Int32MultiArray
exec(identify_file_str)

pub = rospy.Publisher(
	'array',
	std_msgs.msg.Float32MultiArray,
	queue_size = 1
)

rospy.init_node('network_node',anonymous=True,disable_signals=True)


timer = Timer(1000)
rate = Timer(1)

n = 64
data = rnd((23,41,n))
while not timer.check():
	pub.publish(data=data.reshape(23*41*n))
	rate.freq()

cg('done.')

#EOF
