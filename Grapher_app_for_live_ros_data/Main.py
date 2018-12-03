###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils3 import *
	pythonpaths(['kzpy3','kzpy3/Grapher_app'])
#
###############################
from Parameters_Module import *
from kzpy3.vis3 import *

import Display_Graph_Module
#from Car_Data_app.Names_Module import *
exec(identify_file_str)
"""
	* Have playback at fix rate, not machine capacity
	* Parameterize all those little display constants
	* Write out total time
	* Print out all topic values at current time
	* Show left and right images
	* Allow programatic display, exactly corresponding to network training needs
	* Need to display data from hdf5 files or from data extracted from neural network inputs/outputs
	* Need to display from ros
"""
_ = dictionary_access

for a in Args.keys():
	ar = Args[a]
	if str_is_int(ar):
		P[a] = int(ar)
	else:
		P[a] = ar

P[X_PIXEL_SIZE_INIT],P[Y_PIXEL_SIZE_INIT] = P[X_PIXEL_SIZE],P[Y_PIXEL_SIZE]

import roslib
import std_msgs.msg
import geometry_msgs.msg
import rospy
import cv2
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
exec(identify_file_str)
bridge = CvBridge()

rospy.init_node('listener',anonymous=True)




def steer__callback(msg):
	R['steer']['ts'].append(time.time())
	R['steer']['vals'].append(msg.data)

def cmd_steer__callback(msg):
	R['cmd/steer']['ts'].append(time.time())
	R['cmd/steer']['vals'].append(msg.data)

def cmd_motor__callback(msg):
	R['cmd/motor']['ts'].append(time.time())
	R['cmd/motor']['vals'].append(msg.data)

def motor__callback(msg):
	R['motor']['ts'].append(time.time())
	R['motor']['vals'].append(msg.data)

def state__callback(msg):
	R['state']['ts'].append(time.time())
	R['state']['vals'].append(msg.data)

def encoder__callback(msg):
	R['encoder']['ts'].append(time.time())
	R['encoder']['vals'].append(msg.data)

def acc__callback(msg):
	t_ = time.time()
	R['acc_x']['ts'].append(t_)
	R['acc_x']['vals'].append(msg.x)
	R['acc_y']['ts'].append(t_)
	R['acc_y']['vals'].append(msg.y)
	R['acc_z']['ts'].append(t_)
	R['acc_z']['vals'].append(msg.z)

def gyro__callback(msg):
	t_ = time.time()
	R['gyro_x']['ts'].append(t_)
	R['gyro_x']['vals'].append(msg.x)
	R['gyro_y']['ts'].append(t_)
	R['gyro_y']['vals'].append(msg.y)
	R['gyro_z']['ts'].append(t_)
	R['gyro_z']['vals'].append(msg.z)


def gyro_heading__callback(msg):
	t_ = time.time()
	R[gyro_heading_x]['ts'].append(t_)
	R[gyro_heading_x]['vals'].append(msg.x)
	R[gyro_heading_y]['ts'].append(t_)
	R[gyro_heading_y]['vals'].append(msg.y)
	R[gyro_heading_z]['ts'].append(t_)
	R[gyro_heading_z]['vals'].append(msg.z)

def left_image__callback(data):
	R[left_image]['ts'].append(time.time())
	R[left_image]['vals'].append( bridge.imgmsg_to_cv2(data,"rgb8") )


def right_image__callback(data):
	R[right_image]['ts'].append(time.time())
	R[right_image]['vals'].append( bridge.imgmsg_to_cv2(data,"rgb8") )

for f in flex_names:
	s = """
def FLEX__callback(msg):
	R['FLEX']['ts'].append(time.time())
	R['FLEX']['vals'].append(msg.data)
rospy.Subscriber('/bair_car/FLEX', std_msgs.msg.Int32, callback=FLEX__callback)
	"""
	exec_str = s.replace('FLEX',f)
	exec(exec_str)

rospy.Subscriber('/bair_car/steer', std_msgs.msg.Int32, callback=steer__callback)
rospy.Subscriber('/bair_car/cmd/steer', std_msgs.msg.Int32, callback=cmd_steer__callback)
rospy.Subscriber('/bair_car/cmd/motor', std_msgs.msg.Int32, callback=cmd_motor__callback)
rospy.Subscriber('/bair_car/motor', std_msgs.msg.Int32, callback=motor__callback)
rospy.Subscriber('/bair_car/state', std_msgs.msg.Int32, callback=state__callback)
rospy.Subscriber('/bair_car/encoder', std_msgs.msg.Float32, callback=encoder__callback)
rospy.Subscriber('/bair_car/acc', geometry_msgs.msg.Vector3, callback=acc__callback)
rospy.Subscriber('/bair_car/gyro', geometry_msgs.msg.Vector3, callback=gyro__callback)
rospy.Subscriber('/bair_car/gyro_heading', geometry_msgs.msg.Vector3, callback=gyro_heading__callback)
if P['USE_IMAGES']:
	if True:
		rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_image__callback,queue_size = 1)
	if True:	
		rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_image__callback,queue_size = 1)


print('Make sure this has been done if necessary, e.g.:\n\texport ROS_MASTER_URI=http://nvidia@192.168.1.11:11311')
timer=Timer(0)
while len(R['steer']['ts']) < 100:# and len(R['left_image']['ts']) < 1:
	print('waiting for ROS data . . .')
	pause(0.5)
while True:
	
	timer.reset()
	if P['USE_IMAGES']:
		for m_ in ['ts','vals']:
			if left_image in R:
				R[left_image][m_] = R[left_image][m_][-1:]
				R[right_image][m_] = R[left_image][m_][-1:]
	for topic_ in R.keys():
		if len(R[topic_]['ts']) > P[TOPIC_STEPS_LIMIT]:
			for m_ in ['ts','vals']:
				R[topic_][m_] = R[topic_][m_][-P[TOPIC_STEPS_LIMIT]:]
	try:
		D = Display_Graph_Module.Display_Graph(topics,R)
		D[show]()
	except Exception as e:
	    exc_type, exc_obj, exc_tb = sys.exc_info()
	    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	    CS_('Exception!',emphasis=True)
	    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)


#EOF