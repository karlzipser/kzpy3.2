from kzpy3.utils2 import *
CODE_PATH__ = opjh('kzpy3/Localization_app')
pythonpaths([opjh('kzpy3'),opjh(CODE_PATH__)])
from Parameters_Module import *
from vis2 import *
from aruco_home_4x4_markers import Marker_xy_dic
exec(identify_file_str)

na = np.array




def Camera_View_Field(*args):
	Args = args_to_dictionary(args)
	Aruco_data = Args[aruco_data]
	True
	D = {}
	D[markers] = {}
	nearest_marker_ = [None,999]
	for m_ in Aruco_data['angles_to_center'].keys():
		if m_ == 58:
			continue # a duplicate
		D[markers][m_] = {}
		D[markers][m_][alpha] = np.degrees(Aruco_data['angles_to_center'][m_])/2.0
		D[markers][m_][beta] = np.degrees(Aruco_data['angles_surfaces'][m_])
		D[markers][m_][dist] = Aruco_data['distances_marker'][m_]
		if D[markers][m_][dist] < nearest_marker_[1]:
			nearest_marker_ = [m_,D[markers][m_][dist]]
		a_ = [0,1]
		h_ = [0.333,0]
		a_rotated_ = na(rotatePoint([0,0],a_,-90-D[markers][m_][alpha]))
		D[markers][m_][marker_point] = D[markers][m_][dist]*a_rotated_
		marker_face_ = na(rotatePoint([0,0],-D[markers][m_][marker_point],D[markers][m_][beta]))/length(D[markers][m_][marker_point])/10.0
		gamma_ = angle_clockwise([0,-1],marker_face_)
		D[markers][m_][left] = 	D[markers][m_][marker_point]-marker_face_
		D[markers][m_][right] = D[markers][m_][marker_point]+marker_face_
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
		if m_ == 58:
			continue # a duplicate
		for side_ in [left,right]:
			D[pts].append(D[markers][m_][side_])
		D[actual_pts].append(Marker_xy_dic[(m_,left)])
		D[actual_pts].append(Marker_xy_dic[(m_,right)])

	D[pts] = na(D[pts])
	D[actual_pts] = na(D[actual_pts])

	def function_rotate_around(*args):
		Args = args_to_dictionary(args)
		theta_ = Args[theta]
		True
		#D[pts_centered] = D[pts]
		#return np.random.randn(1)[0]
		D[pts_translated] = D[pts] - D[markers][D[nearest_marker]][marker_point]
		D[pts_rotated] = na(rotatePolygon(D[pts_translated],theta_))
		D[pts_centered] = D[pts_rotated] + Marker_xy_dic[D[nearest_marker]]
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
	assert(58 not in D[markers].keys())
	return D




def Aruco_Trajectory():
	D = {}
	D[hx] = False
	D[hy] = False
	D[x] = False
	D[y] = False
	D[car_pts] = []
	D[head_pts] = []
	D[past_to_present_proportion] = 0.975
	D[max_list_length] = 12
	def _function_step(*args):
		Args = args_to_dictionary(args)
		one_frame_aruco_data_ = Args[one_frame_aruco_data]
		True
		CVF = Camera_View_Field(aruco_data,one_frame_aruco_data_)
		min_error_ = 9999
		car_pts_ = D[car_pts]
		head_pts_ = D[head_pts]
		a_ = P[past_to_present_proportion]
		t_ctr_ = 0
		for theta_ in range(0,360,30):
			error_ = CVF[rotate_around](theta,theta_)
			if error_ < min_error_:
				min_error_ = error_
				min_theta_ = theta_
			t_ctr_+=1
		CVF[rotate_around](theta,min_theta_)
		car_pts_.append(CVF[pts_centered][0])
		head_pts_.append(CVF[pts_centered][1])
		if len(car_pts_) > 1.5*D[max_list_length]:
			D[car_pts] = D[car_pts][-D[max_list_length]:]
		if len(head_pts_) > 1.5*D[max_list_length]:
			D[head_pts] = D[head_pts][-D[max_list_length]:]
		if D[hx] == False:
			D[hx] = head_pts_[-1][0]
			D[hy] = head_pts_[-1][1]
		D[hx] =  a_*D[hx]+(1-a_)*head_pts_[-1][0]  
		D[hy] = a_*D[hy]+(1-a_)*head_pts_[-1][1] 
		if D[x] == False:
			D[x] = car_pts_[-1][0]
			D[y] = car_pts_[-1][1]
		D[x] =  a_*D[x]+(1-a_)*car_pts_[-1][0]  
		D[y] = a_*D[y]+(1-a_)*car_pts_[-1][1]
		#x__ = (D[x]+D[hx])/2.0
		#y__ = (D[y]+D[hy])/2.0
		return D[hx],D[hy],D[x],D[y]#x__,y__
	D[step] = _function_step
	return D







#EOF


