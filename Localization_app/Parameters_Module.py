from Paths_Module import *
from All_Names_Module import *
exec(identify_file_str)

_ = dictionary_access

#from aruco_home_4x4_markers import Marker_xy_dic
#from aruco_whole_room_markers import Marker_xy_dic
from aruco_whole_room_markers_11circle_half_raised import Marker_xy_dic
P = {}
P[VERBOSE] = True
P[GRAPHICS] = False
P[ROS_LIVE] = True
P[past_to_present_proportion] = 0.99 # 0.5
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