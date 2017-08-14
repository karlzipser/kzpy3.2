###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Localization_app'])
#
###############################
from vis2 import *
from Main import *

P = {}
P[GRAPHICS] = True

def plot_line(a_,b,c):
	plot([a_[0],b[0]],[a_[1],b[1]],c)

na = np.array

Markers_clockwise = {
	################
	# East 1
	'East':[ 51,50,4,63,
		# East 2
		146,147,148,149,
		# East 3
		52,189,192,191,
		# East 4
		199,200,202,203],
		#
	################
	# South 1
	'South':[204,205,208,206,
		# South 2
		174,175,176,177,
		# South 3
		57,58,67,59,
		# South 4
		173,172,171,170],
	################
	# West 1
	'West':[227,226,228,225,
		# West 2
		153,152,151,150,
		# West 3
		134,133,139,138,
		# West 4
		216,217,218,219],
	#################
	# North 1
	'North':[223,222,221,220,
		# North 2
		132,137,136,135,
		# North 3
		198,196,197,194,
		# North 4
		178,179,180,181]
		###############
}
Marker_xy_dic = {}

marker_spacing_ = 107/4.0/100.0
marker_width = 21/100.0

ctr_ = 7.5
for k_ in Markers_clockwise['North']:
	Marker_xy_dic[k_] = na([ctr_*marker_spacing_,-8*marker_spacing_])
	Marker_xy_dic[(k_,left)] = Marker_xy_dic[k_] + na([marker_width/2.0,0])
	Marker_xy_dic[(k_,right)] = Marker_xy_dic[k_] - na([marker_width/2.0,0])
	ctr_ -= 1
ctr_ = -7.5
for k_ in Markers_clockwise['South']:
	Marker_xy_dic[k_] = na([ctr_*marker_spacing_,8*marker_spacing_])
	Marker_xy_dic[(k_,left)] = Marker_xy_dic[k_] - na([marker_width/2.0,0])
	Marker_xy_dic[(k_,right)] = Marker_xy_dic[k_] + na([marker_width/2.0,0])
	ctr_ += 1
ctr_ = -7.5
for k_ in Markers_clockwise['East']:
	Marker_xy_dic[k_] = na([-8*marker_spacing_,ctr_*marker_spacing_])
	Marker_xy_dic[(k_,left)] = Marker_xy_dic[k_] + na([0,-marker_width/2.0])
	Marker_xy_dic[(k_,right)] = Marker_xy_dic[k_] + na([0,marker_width/2.0])
	ctr_ += 1
ctr_ = 7.5
for k_ in Markers_clockwise['West']:
	Marker_xy_dic[k_] = na([8*marker_spacing_,ctr_*marker_spacing_])
	Marker_xy_dic[(k_,left)] = Marker_xy_dic[k_] + na([0,marker_width/2.0])
	Marker_xy_dic[(k_,right)] = Marker_xy_dic[k_] + na([0,-marker_width/2.0])
	ctr_ -= 1



CA()

def Camera_view_field(*args):
	Args = args_to_dictionary(args)
	Aruco_data = Args[aruco_data]
	True
	D = {}
	D[markers] = {}
	nearest_marker_ = [None,999]
	for m_ in Aruco_data['angles_to_center'].keys():
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
	for m_ in D[markers].keys():
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
		D[pts_translated] = D[pts] - D[markers][D[nearest_marker]][marker_point]
		D[pts_rotated] = na(rotatePolygon(D[pts_translated],theta_))
		D[pts_centered] = D[pts_rotated] + Marker_xy_dic[D[nearest_marker]]
		return ((D[actual_pts] - D[pts_centered][2:])**2).mean()
	D[rotate_around] = function_rotate_around
	return D

figure(1);clf();
for i_ in range(0,len(ts_)):
	print i_
	try:
		plt_square();xysqlim(3)
		Q = L[ts_[i_]]
		D=Camera_view_field(aruco_data,Q)

		timer = Timer(0)
		results = []
		min_error_ = 9999
		for theta_ in range(0,360,10):
			error_ = D[rotate_around](theta,theta_)
			if error_ < min_error_:
				min_error_ = error_
				min_theta_ = theta_
			results.append([theta_,error_])
		#print timer.time(),dp(min_theta_),dp(min_error_)

		D[rotate_around](theta,min_theta_)

		#pts_plot(D[pts_centered][2:],'k');
		#for i_ in range(2,len(D[pts_centered]),2):
		#	plot_line(D[pts_centered][i_],D[pts_centered][i_+1],'k')
		pts_plot(D[pts_centered][:1],'r');
		#for i_ in range(1):
		#	plot_line(D[pts_centered][i_],D[pts_centered][i_+1],'r')
		#for i_ in range(0,len(D[actual_pts]),2):
		#	plot_line(D[actual_pts][i_],D[actual_pts][i_+1],'g')
		#pts_plot(D[actual_pts],'y');
		
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
	if np.mod(i_,10)==0:
		pause(0.0001)



	#raw_input('enter')




for t_ in ts_:
	Q = L[t_]
	figure(1);clf();plt_square()
	D=Camera_view_field(aruco_data,Q)



		a_ = [0,1]
		h_ = [0.333,0]
		a_rotated_ = na(rotatePoint([0,0],a_,-90-alpha_))
		marker_point_ = dist_*a_rotated_
		marker_face_ = na(rotatePoint([0,0],-marker_point_,beta_))/length(marker_point_)/10.0
		gamma_ = angle_clockwise([0,-1],marker_face_)


		M[marker_][a_rotated] 	= a_rotated_
		M[marker_][marker_point] = marker_point_
		M[marker_][marker_face] = marker_face_
		M[marker_][gamma] 		= gamma_
		M[marker_][left] = M[marker_][marker_point]-M[marker_][marker_face]
		M[marker_][right] = M[marker_][marker_point]+M[marker_][marker_face]

	origin_ = na(Marker_xy_dic[Nearest_marker[marker]]) - M[Nearest_marker[marker]][marker_point]

	if False:
		for marker_ in marker_ids_:
			if P[GRAPHICS]:
				plot_line(origin_,origin_+M[marker_][h],'r')
				plot_line(origin_,origin_+M[marker_][marker_point],'b')
				plt.annotate(marker_,origin_+M[marker_][marker_point])
				plot_line(origin_+M[marker_][marker_point],origin_+M[marker_][left],'y')
				plot_line(origin_+M[marker_][marker_point],origin_+M[marker_][right],'g')

	if True:
		origin_ = na([0,0])
		for marker_ in marker_ids_:
			if P[GRAPHICS]:
				plot_line(origin_,origin_+M[marker_][h],'r')
				plot_line(origin_,origin_+M[marker_][marker_point],'b')
				plt.annotate(marker_,origin_+M[marker_][marker_point])
				plot_line(origin_+M[marker_][marker_point],origin_+M[marker_][left],'y')
				plot_line(origin_+M[marker_][marker_point],origin_+M[marker_][right],'g')




	fixed_markers_ = Markers_clockwise['North']+Markers_clockwise['South']+Markers_clockwise['East']+Markers_clockwise['West']
	markers_ = []
	xy_markers = []
	for m_ in sorted(M.keys()):
		if m_ in fixed_markers_:
			markers_.append(m_)
	fixed_pts_ = []
	moving_pts_ = []
	for m_ in markers_:
		for side in [left,right]:
			fixed_pts_.append(Marker_xy_dic[(m_,side)])
			moving_pts_.append(M[m_][side])
	fixed_pts_ = na(fixed_pts_)
	moving_pts_ = na(moving_pts_)
	nearest_marker_ = Nearest_marker[marker]
	translation_vector_ = Marker_xy_dic[nearest_marker_]-M[nearest_marker_][marker_point]
	nearest_marker_point_ = M[nearest_marker_][marker_point]


	def fun(theta_,theta0_,moving_pts_,nearest_marker_point_,translation_vector_):
		#figure(22)
		rotating_pts_ = moving_pts_.copy()
		rotating_pts_ -= nearest_marker_point_
		rotating_pts_ = na(rotatePolygon(rotating_pts_,theta_))
		rotating_pts_ += nearest_marker_point_
		translated_pts_ = translation_vector_+rotating_pts_
		#pts_plot(translated_pts_,'b')
		return ((fixed_pts_ - translated_pts_)**2).mean()

	results = []
	timer = Timer(0)
	min_error_ = 9999
	for theta_ in range(0,360,10):
		error_ = fun(theta_,0,moving_pts_,nearest_marker_point_,translation_vector_)
		if error_ < min_error_:
			min_error_ = error_
			min_theta_ = theta_
		results.append([theta_,error_])
	print timer.time(),dp(min_theta_),dp(min_error_)



	theta_ = min_theta_
	rotating_pts_ = moving_pts_.copy()
	rotating_pts_ -= nearest_marker_point_
	rotating_pts_ = na(rotatePolygon(rotating_pts_,theta_))
	rotating_pts_ += nearest_marker_point_
	translated_pts_ = translation_vector_+rotating_pts_
	assert(len(translated_pts_) == len(fixed_pts_))
	pts_plot(translated_pts_,'r')

	r=na(results) 
	figure(2);pts_plot(r)
	"""
		fixed_moving_center_point_ = 
		
		theta_ = 
		error_ = 
	"""
	mi(F[left_image][vals][ctr_],0);pause(0.01)
	ctr_ += 1
	pause(.001)
	#raw_input('enter')