from Paths_Module import *
from All_Names_Module import *
exec(identify_file_str)

_ = dictionary_access

P = {}

_(P,VERBOSE,equals,True)
P[GRAPHICS] = False
P[ROS_LIVE] = True
P[past_to_present_proportion] = 0.5
#P[MARKER_SETUP] = 'aruco_markers_clockwise_April_2017_Smyth_Fern_arena'
#P[MARKER_SETUP] = 'aruco_markers_4x4_1408_August_2017'

#EOF