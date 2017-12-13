from Paths_Module import *
from All_Names_Module import *
exec(identify_file_str)

_ = dictionary_access

#from aruco_home_4x4_markers import Marker_xy_dic
#from aruco_whole_room_markers import Marker_xy_dic
#from aruco_whole_room_markers_11circle_full_raised import Marker_xy_dic
#Marker_xy_dic = lo(opjD('aruco_raised11_5Nov2017_Marker_xy_dic.pkl'))
#Marker_xy_dic = lo(opjD('whole_room_19Nov2017_Marker_xy_dic.pkl'))
#Marker_xy_dic = lo(opjD('aruco_12circle_20Nov2017_Marker_xy_dic.pkl'))
#spd2s(Marker_xy_dic.keys())

P = {}
P['CAR_LIST'] = ['Mr_Purple','Mr_Black','Mr_Blue','Mr_Lt_Blue','Mr_Orange','Mr_Yellow','Mr_Silver_Orange','Mr_Silver_Orange_TX2_back','Mr_Silver']
P[VERBOSE] = True
P[GRAPHICS] = False
P[ROS_LIVE] = True
P[past_to_present_proportion] = 0.0#0.75#0.99 # 0.5
"""
P[MARKERS_TO_IGNORE] = [#58, #duplicated on post
	0,11,102,100, # post markers
	190, # often has False positives
	]
"""
P[MARKERS_TO_IGNORE] = [190] # often has False positives

P[DEGREE_STEP_FOR_ROTATION_FIT] = 5#15  # 10 to 30 range, bigger is faster
P[ANGLE_DIST_PARAM] = 0.3





#EOF