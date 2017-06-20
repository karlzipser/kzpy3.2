from kzpy3.utils import *

topics = [('steer','std_msgs.msg.Int32'),('gyro','geometry_msgs.msg.Vector3'),('GPS2_lat','std_msgs.msg.Float32')]
prefix = '/bair_car/'


ros_str = """# rospy meta code"""
ros_str += """
import rospy
import std_msgs.msg
import geometry_msgs.msg
import sensor_msgs.msg
"""

for tp in topics:
	tn = tp[0] + '_msg'
	ros_str += """
"""+tn+""" = None
def """+tn+"""_callback(msg):
	global """+tn+"""
	"""+tn+""" = msg
		"""
	

ros_str += """
rospy.init_node('listener',anonymous=True)

"""


for tp in topics:
	tn = tp[0]
	tt = tp[1]
	ros_str += """rospy.Subscriber('"""+prefix+tn+"""', """+tt+""", callback="""+tn+"""_msg_callback)\n"""

print ros_str