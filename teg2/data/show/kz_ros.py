from kzpy3.vis import *
#import roslib
import std_msgs.msg
import rospy
rivl='rosrun image_view image_view image:=/bair_car/zed/left/image_rect_color'

print("**** Make sure to do: "+rivl)

bags = sorted(gg(opj(sys.argv[1],'*.bag')))
for b in bags[int(sys.argv[2]):int(sys.argv[3])]:
	unix('rosbag play ' + b + ' --rate 1')

