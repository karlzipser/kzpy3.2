###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Grapher_app'])
#
###############################
from Parameters_Module import *
from kzpy3.vis2 import *

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
	_(P,a,equals,_(Args,a))

P[X_PIXEL_SIZE_INIT],P[Y_PIXEL_SIZE_INIT] = P[X_PIXEL_SIZE],P[Y_PIXEL_SIZE]



"""
##########################################
#
h5py_run_path = '/home/karlzipser/Desktop/bdd_car_data_July2017_LCR/h5py/direct_Tilden_LCR_23Jul17_10h27m34s_Mr_Yellow'
l_ = opj(h5py_run_path,'left_timestamp_metadata.h5py')
o_  = opj(h5py_run_path,'original_timestamp_data.h5py')
#
##########################################
#   left-timestamp bound data
L = h5r(l_)
O = h5r(o_ )
OO = {}
for topic_ in P[TOPICS].keys():
	if topic_ in L.keys():
		OO[topic_] = {}
		OO[topic_][ts] = L[ts][:]
		OO[topic_][vals] = L[topic_][:]
OO[left_image] = {}
OO[left_image][ts] = L[ts][:]
OO[left_image][vals] = O[left_image][vals]
#
#########################################

"""






"""
if __name__ == '__main__':

	
	D = Display_Graph_Module.Display_Graph(topics,OO)
	timer=Timer(0)
	while True:
		timer.reset()
		D[show]()
		print timer.time()
"""






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
for topic_ in [steer, motor, state, encoder,
	acc_x,acc_y,acc_z,
	gyro_x,gyro_y,gyro_z,
	gyro_heading_x,gyro_heading_y,gyro_heading_z,
	#left_image,right_image
	]:
	R[topic_] = {ts:[],vals:[]}


def steer__callback(msg):
	R[steer][ts].append(time.time())
	R[steer][vals].append(msg.data)

def motor__callback(msg):
	R[motor][ts].append(time.time())
	R[motor][vals].append(msg.data)

def state__callback(msg):
	R[state][ts].append(time.time())
	R[state][vals].append(msg.data)

def encoder__callback(msg):
	R[encoder][ts].append(time.time())
	R[encoder][vals].append(msg.data)

def acc__callback(msg):
	t_ = time.time()
	R[acc_x][ts].append(t_)
	R[acc_x][vals].append(msg.x)
	R[acc_y][ts].append(t_)
	R[acc_y][vals].append(msg.y)
	R[acc_z][ts].append(t_)
	R[acc_z][vals].append(msg.z)

def gyro__callback(msg):
	t_ = time.time()
	R[gyro_x][ts].append(t_)
	R[gyro_x][vals].append(msg.x)
	R[gyro_y][ts].append(t_)
	R[gyro_y][vals].append(msg.y)
	R[gyro_z][ts].append(t_)
	R[gyro_z][vals].append(msg.z)


def gyro_heading__callback(msg):
	t_ = time.time()
	R[gyro_heading_x][ts].append(t_)
	R[gyro_heading_x][vals].append(msg.x)
	R[gyro_heading_y][ts].append(t_)
	R[gyro_heading_y][vals].append(msg.y)
	R[gyro_heading_z][ts].append(t_)
	R[gyro_heading_z][vals].append(msg.z)


def left_image__callback(data):
	R[left_image][ts].append(time.time())
	R[left_image][vals].append( bridge.imgmsg_to_cv2(data,"rgb8") )

def right_image__callback(data):
	R[right_image][ts].append(time.time())
	R[right_image][vals].append( bridge.imgmsg_to_cv2(data,"rgb8") )



rospy.init_node('listener',anonymous=True)

rospy.Subscriber('/bair_car/steer', std_msgs.msg.Int32, callback=steer__callback)
rospy.Subscriber('/bair_car/motor', std_msgs.msg.Int32, callback=motor__callback)
rospy.Subscriber('/bair_car/state', std_msgs.msg.Int32, callback=state__callback)
rospy.Subscriber('/bair_car/encoder', std_msgs.msg.Float32, callback=encoder__callback)
rospy.Subscriber('/bair_car/acc', geometry_msgs.msg.Vector3, callback=acc__callback)
rospy.Subscriber('/bair_car/gyro', geometry_msgs.msg.Vector3, callback=gyro__callback)
rospy.Subscriber('/bair_car/gyro_heading', geometry_msgs.msg.Vector3, callback=gyro_heading__callback)
#rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_image__callback,queue_size = 1)
#rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_image__callback,queue_size = 1)






print('Make sure this has been done if necessary:\n\texport ROS_MASTER_URI=http://nvidia@192.168.1.11:11311')
timer=Timer(0)
while len(R[steer][ts]) < 100:
	print('waiting for ROS data . . .')
	pause(0.5)
while True:
	timer.reset()
	for m_ in [ts,vals]:
		if left_image in R:
			R[left_image][m_] = R[left_image][m_][-1:]
			R[right_image][m_] = R[left_image][m_][-1:]
	for topic_ in R.keys():
		#print len(R[topic_][ts]),P[TOPIC_STEPS_LIMIT]
		if len(R[topic_][ts]) > P[TOPIC_STEPS_LIMIT]:
			for m_ in [ts,vals]:
				R[topic_][m_] = R[topic_][m_][-P[TOPIC_STEPS_LIMIT]:]
	D = Display_Graph_Module.Display_Graph(topics,R)
	D[show]()#start_time,D[end_time]-10)
	#print timer.time()

















#EOF

#EOF