from Paths_Module import *
from All_Names_Module import *
exec(identify_file_str)

_ = dictionary_access

from aruco_home_4x4_markers import Marker_xy_dic
P = {}
P[VERBOSE] = True
P[GRAPHICS] = False
P[ROS_LIVE] = True
P[past_to_present_proportion] = 0.5
P[MARKERS_TO_IGNORE] = [58, #duplicated on post
	190, # often has False positives
	]
P[DEGREE_STEP_FOR_ROTATION_FIT] = 15  # 10 to 30 range, bigger is faster

#EOF