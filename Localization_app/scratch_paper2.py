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


F = h5r('/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/h5py/direct_home_LCR_Aruco1_23Jul17_20h51m31s_Mr_Yellow/original_timestamp_data.h5py')



L = A['left']
ts_ = sorted(L.keys())
ctr_ = 0

M = {}

for t_ in ts_[50:]:

	Q = L[t_]

	marker_ids_ = sorted(Q['angles_surfaces'].keys())

	if P[GRAPHICS]: figure(22); clf(); plt_square(); N=4; xysqlim(N) ### P[GRAPHICS] ###
	left_pts_ = []
	right_pts_ = []
	for k_ in Marker_xy_dic.keys():
		if is_number(k_):
			plt.annotate(k_,Marker_xy_dic[k_])
		elif k_[1] == 'left':
			left_pts_.append(Marker_xy_dic[k_])
		elif k_[1] == 'right':
			right_pts_.append(Marker_xy_dic[k_])
	if P[GRAPHICS]: pts_plot(na(left_pts_),'y')  ### P[GRAPHICS] ###
	if P[GRAPHICS]: pts_plot(na(right_pts_),'g')  ### P[GRAPHICS] ###
		


	Nearest_marker = {}
	Nearest_marker[dist] = 9999
	for marker_ in marker_ids_:

		alpha_ = np.degrees(Q['angles_to_center'][marker_])/2.0
		beta_ = np.degrees(Q['angles_surfaces'][marker_])
		dist_ = Q['distances_marker'][marker_]
		if dist_ < Nearest_marker[dist]:
			Nearest_marker[dist] = dist_
			Nearest_marker[marker] = marker_
		a_ = [0,1]
		h_ = [0.333,0]
		a_rotated_ = na(rotatePoint([0,0],a_,-90-alpha_))
		marker_point_ = dist_*a_rotated_
		marker_face_ = na(rotatePoint([0,0],-marker_point_,beta_))/length(marker_point_)/10.0
		gamma_ = angle_clockwise([0,-1],marker_face_)

		M[marker_] = {}
		M[marker_][alpha] 		= alpha_
		M[marker_][beta] 		= beta_
		M[marker_][dist] 		= dist_
		M[marker_][a] 			= a_
		M[marker_][h] 			= h_
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