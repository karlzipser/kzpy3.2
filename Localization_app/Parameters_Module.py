from Paths_Module import *
from All_Names_Module import *
exec(identify_file_str)

_ = dictionary_access

#from aruco_home_4x4_markers import Marker_xy_dic
#from aruco_whole_room_markers import Marker_xy_dic
#from aruco_whole_room_markers_11circle_full_raised import Marker_xy_dic
Marker_xy_dic = lo(opjD('aruco_raised11_5Nov2017_Marker_xy_dic.pkl'))
spd2s(Marker_xy_dic.keys())
P = {}
P[VERBOSE] = True
P[GRAPHICS] = False
P[ROS_LIVE] = True
P[past_to_present_proportion] = 0.75#0.99 # 0.5
"""
P[MARKERS_TO_IGNORE] = [#58, #duplicated on post
	0,11,102,100, # post markers
	190, # often has False positives
	]
"""
P[MARKERS_TO_IGNORE] = [190] # often has False positives

P[DEGREE_STEP_FOR_ROTATION_FIT] = 5#15  # 10 to 30 range, bigger is faster
P[ANGLE_DIST_PARAM] = 0.3


if False:
	timer = Timer(30)
	O = h5r('/media/karlzipser/2_TB_Samsung/h5py/Mr_Lt_Blue_2017-10-23-18-09-39/original_timestamp_data.h5py')
	o=lo('/media/karlzipser/2_TB_Samsung/h5py/Mr_Lt_Blue_2017-10-23-18-09-39/aruco_data.pkl' )
	lv=o['left_image_aruco']['vals']
	rv=o['right_image_aruco']['vals']
	figure(1);clf();plt_square();xysqlim(4) 
	AT= Aruco_Trajectory()
	c_prev,d_prev = 0,0
	for i in range(0,len(lv),1):
		if timer.check():
			time.sleep(0.1)
			timer.reset()
			figure(1);clf();plt_square();xysqlim(4)
		try:                                                         
			a,b,c,d=AT[step](one_frame_aruco_data,lv[i],p,P)
			e,f,g,h=AT[step](one_frame_aruco_data,rv[i],p,P)
			if length([c-c_prev,d-d_prev]) > 0.01:
				figure(1)
				plot(c,d,'r.')
				plot(g,h,'b.');
				mi(O[left_image][vals][i][:],2)
				spause()
			c_prev = c
			d_prev = d
		except KeyboardInterrupt:
			break
		except:
			pass




#EOF