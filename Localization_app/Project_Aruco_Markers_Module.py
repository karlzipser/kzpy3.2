from kzpy3.utils2 import *
CODE_PATH__ = opjh('kzpy3/Localization_app')
pythonpaths([opjh('kzpy3'),opjh(CODE_PATH__)])
from Parameters_Module import *
from vis2 import *
exec(identify_file_str)

na = np.array




def Camera_View_Field(*args):
	Args = args_to_dictionary(args)
	Aruco_data = Args[aruco_data]
	P = Args[p]
	True
	D = {}
	D[markers] = {}
	nearest_marker_ = [None,999]
	pts_ = []
	a_ = [0,1]
	#h_ = [0.53,0] # heading point
	h_ = [0.1,0] # heading point
	for m_ in Aruco_data['angles_to_center'].keys():
		if m_ in P[MARKERS_TO_IGNORE]:
			continue
		D[markers][m_] = {}
		D[markers][m_][alpha] = np.degrees(Aruco_data['angles_to_center'][m_])/2.0
		D[markers][m_][beta] = np.degrees(Aruco_data['angles_surfaces'][m_])
		D[markers][m_][dist] = Aruco_data['distances_marker'][m_] * (1.0+(np.abs(D[markers][m_][alpha]/45.0)**2)*P[ANGLE_DIST_PARAM])

		if D[markers][m_][dist] < nearest_marker_[1]:
			nearest_marker_ = [m_,D[markers][m_][dist]]
		#a_ = [0,1]
		#h_ = [0.333,0]
		a_rotated_ = na(rotatePoint([0,0],a_,-90-D[markers][m_][alpha]))
		D[markers][m_][marker_point] = D[markers][m_][dist]*a_rotated_
		marker_face_ = na(rotatePoint([0,0],-D[markers][m_][marker_point],D[markers][m_][beta]))/length(D[markers][m_][marker_point])/10.0
		gamma_ = angle_clockwise([0,-1],marker_face_)
		D[markers][m_][left] = 	D[markers][m_][marker_point]-marker_face_
		D[markers][m_][right] = D[markers][m_][marker_point]+marker_face_
		
	#D[center_of_mass] = na(pts_).mean(axis=0)

	D[nearest_marker] = nearest_marker_[0]
	def _function_plot_start_configuration():
		origin_ = na([0,0])
		for m_ in D[markers].keys():
			mp_ = D[markers][m_][marker_point]
			plot_line(origin_,origin_+na(h_),'r')
			plot_line(origin_,origin_+mp_,'b')
			plt.annotate(m_,origin_+mp_)
			plot_line(origin_+mp_,origin_+D[markers][m_][left],'y')
			plot_line(origin_+mp_,origin_+D[markers][m_][right],'g')
	D[plot_start_configuration] = _function_plot_start_configuration
	D[pts] = [[0,0],h_]
	D[actual_pts] = []
	for m_ in sorted(D[markers].keys()):
		if m_ in P[MARKERS_TO_IGNORE]:
			continue
		for side_ in [left,right]:
			D[pts].append(D[markers][m_][side_])
		D[actual_pts].append(Marker_xy_dic[(m_,left)])
		D[actual_pts].append(Marker_xy_dic[(m_,right)])
	D[pts] = na(D[pts])
	D[actual_pts] = na(D[actual_pts])
	D[center_of_mass] = D[pts].mean(axis=0)
	D[actual_center_of_mass] = D[actual_pts].mean(axis=0)
	def function_rotate_around(*args):
		Args = args_to_dictionary(args)
		theta_ = Args[theta]
		True
		D[pts_translated] = D[pts] - D[center_of_mass]#D[markers][D[nearest_marker]][marker_point]
		D[pts_rotated] = na(rotatePolygon(D[pts_translated],theta_))
		D[pts_centered] = D[pts_rotated] + D[actual_center_of_mass]#Marker_xy_dic[D[nearest_marker]]
		return ((D[actual_pts] - D[pts_centered][2:])**2).mean()
	D[rotate_around] = function_rotate_around

	def function_rotate_around_marker(*args):
		Args = args_to_dictionary(args)
		theta_ = Args[theta]
		marker_ = Args[marker]
		True
		D[pts_translated] = D[pts] - D[markers][marker_][marker_point]
		D[pts_rotated] = na(rotatePolygon(D[pts_translated],theta_))
		D[pts_centered] = D[pts_rotated] + Marker_xy_dic[marker_]
		return ((D[actual_pts] - D[pts_centered][2:])**2).mean()
	D[rotate_around_marker] = function_rotate_around_marker
	#assert(58 not in D[markers].keys())
	return D




def Aruco_Trajectory():
	D = {}
	D[hx] = False
	D[hy] = False
	D[x] = False
	D[y] = False
	#D[car_pts] = []
	#D[head_pts] = []
	#D[past_to_present_proportion] = 0.975
	D[max_list_length] = 12
	timer = Timer(10)
	def _function_step(*args):
		Args = args_to_dictionary(args)
		one_frame_aruco_data_ = Args[one_frame_aruco_data]
		P = Args[p]
		True
		CVF = Camera_View_Field(aruco_data,one_frame_aruco_data_, p,P)
		min_error0_ = 9999
		min_error1_ = 9999
		min_error2_ = 9999
		#car_pts_ = D[car_pts]
		#head_pts_ = D[head_pts]
		a_ = P[past_to_present_proportion]
		t_ctr_ = 0

		for theta0_ in range(0,360,60):
			error_ = CVF[rotate_around](theta,theta0_)
			if error_ < min_error0_:
				min_error0_ = error_
				min_theta0_ = theta0_
			t_ctr_+=1

		min_theta1_ = min_theta0_
		for theta1_ in range(min_theta0_-30,min_theta0_+31,20):#P[DEGREE_STEP_FOR_ROTATION_FIT]):
			error_ = CVF[rotate_around](theta,theta1_)
			if error_ < min_error1_:
				min_error1_ = error_
				min_theta1_ = theta1_

		min_theta2_ = min_theta1_
		for theta2_ in range(min_theta1_-10,min_theta1_+11,P[DEGREE_STEP_FOR_ROTATION_FIT]):
			error_ = CVF[rotate_around](theta,theta2_)
			if error_ < min_error2_:
				min_error2_ = error_
				min_theta2_ = theta2_
			t_ctr_+=1

		if timer.check():
			print(d2s('t_ctr_ =',t_ctr_))
			timer.reset()

		CVF[rotate_around](theta,min_theta2_)
		car_pts_=CVF[pts_centered][0]
		head_pts_=CVF[pts_centered][1]

		if D[hx] == False:
			D[hx] = head_pts_[0]
			D[hy] = head_pts_[1]
		D[hx] =  a_*D[hx]+(1-a_)*head_pts_[0]  
		D[hy] = a_*D[hy]+(1-a_)*head_pts_[1] 
		if D[x] == False:
			D[x] = car_pts_[0]
			D[y] = car_pts_[1]
		D[x] =  a_*D[x]+(1-a_)*car_pts_[0]  
		D[y] = a_*D[y]+(1-a_)*car_pts_[1]

		return D[hx],D[hy],D[x],D[y]
	D[step] = _function_step
	return D







#EOF


