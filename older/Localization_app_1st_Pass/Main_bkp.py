###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Localization_app'])
#
###############################
from Parameters_Module import *
from vis2 import *
from Project_Aruco_Markers_Module import Aruco_Trajectory
#from Main import *
exec(identify_file_str)
na = np.array

for a_ in Args.keys():
	P[a_] = Args[a_]


if P[ROS_LIVE]:
	import roslib
	import std_msgs.msg
	import geometry_msgs.msg
	import rospy
	import cv2
	from cv_bridge import CvBridge,CvBridgeError
	from sensor_msgs.msg import Image
	import kzpy3.data_analysis.Angle_Dict_Creator as Angle_Dict_Creator
	bridge = CvBridge()
	R = {}
	def left_image__callback(data):
		R[left_image] = bridge.imgmsg_to_cv2(data,"rgb8")
	def right_image__callback(data):
		R[right_image] = bridge.imgmsg_to_cv2(data,"rgb8") 

	rospy.init_node('listener',anonymous=True)
	rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_image__callback,queue_size = 1)
	rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_image__callback,queue_size = 1)
	aruco_heading_x_pub = rospy.Publisher('/bair_car/aruco_heading_x', std_msgs.msg.Float32, queue_size=100)
	aruco_heading_y_pub = rospy.Publisher('/bair_car/aruco_heading_y', std_msgs.msg.Float32, queue_size=100)
	aruco_position_x_pub = rospy.Publisher('/bair_car/aruco_position_x', std_msgs.msg.Float32, queue_size=100)
	aruco_position_y_pub = rospy.Publisher('/bair_car/aruco_position_y', std_msgs.msg.Float32, queue_size=100)

	def Data_Access():
		D = {}
		def _function_get_data():
			camera_img_ = R[left_image]
			angles_to_center, angles_surfaces, distances_marker, markers = Angle_Dict_Creator.get_angles_and_distance(camera_img_,borderColor=None)#borderColor=(255,0,0))
			Left = {'angles_to_center':angles_to_center,'angles_surfaces':angles_surfaces,'distances_marker':distances_marker}
			if P[GRAPHICS]:
				mci(camera_img_,color_mode=cv2.COLOR_RGB2BGR,delay=33,title='left_image')
			camera_img_ = R[right_image]
			angles_to_center, angles_surfaces, distances_marker, markers = Angle_Dict_Creator.get_angles_and_distance(camera_img_,borderColor=None)#borderColor=(0,0,255))
			Right = {'angles_to_center':angles_to_center,'angles_surfaces':angles_surfaces,'distances_marker':distances_marker}
			if P[GRAPHICS]:
				mci(camera_img_,color_mode=cv2.COLOR_RGB2BGR,delay=33,title='right_image')
			return Left,Right
		D[get_data] = _function_get_data
		return D
else:
	Aruco_data = lo(opjD('A'))
	def Data_Access():
		D = {}
		D[ts] = {}
		for side_ in [left,right]:
			D[ts][side_] = sorted(Aruco_data[side_].keys())
		D[index] = 0
		def _function_get_data():
			if D[index] >= len(D[ts][right]) or D[index] >= len(D[ts][left]):
				return False,False
			data_ = Aruco_data[left][D[ts][left][D[index]]],Aruco_data[right][D[ts][right][D[index]]]
			D[index] += 1
			return data_
		D[get_data] = _function_get_data
		return D



Data_access = Data_Access()
Aruco_trajectory = Aruco_Trajectory()
if P[GRAPHICS]:
	CA()
ctr_ = 0
timer_ = Timer(0)
while True:

	try:
		Data_left,Data_right = Data_access[get_data]()

		if Data_left == False:
			break

		if P[GRAPHICS]:
			clf();
			there_ = False



		for Q in [Data_left,Data_right]:
			
				hx_,hy_,x_,y_ =	Aruco_trajectory[step](one_frame_aruco_data,Q)

				aruco_position_x_pub.publish(std_msgs.msg.Float32(x_))
				aruco_position_y_pub.publish(std_msgs.msg.Float32(y_))
				aruco_heading_x_pub.publish(std_msgs.msg.Float32(hx_-x_))
				aruco_heading_y_pub.publish(std_msgs.msg.Float32(hy_-y_))



	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
	
	try:
		if P[GRAPHICS]:
			figure(5);clf();plt_square();xysqlim(2*107.0/100.0);
			plot(hx_,hy_,'b.')
			plot(x_,y_,'y.')
			pause(0.0001)
			pass
		ctr_ += 1
		if np.mod(ctr_,100) == 0:
			spd2s(ctr_/timer_.time(),'hz')
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)





"""
if True:#P[GRAPHICS]:
	figure(2);clf();plt_square();xysqlim(3);
	pts_plot(na(car_pts_),'b')
	pts_plot(na(head_pts_),'b')
	figure(3)
	plot(na(car_pts_)[:,1],'r.')
	plot(na(car_pts_)[:,0],'.')
	figure(4)
	plot(thetas_,'.')
	figure(5);clf();plt_square();xysqlim(3);
	plot(na(hxl_)[range(0,len(hxl_),1)],na(hyl_)[range(0,len(hyl_),1)],'b.')
	plot(na(xl_)[range(0,len(xl_),1)],na(yl_)[range(0,len(yl_),1)],'y.')
	raw_enter()
"""

#EOF
