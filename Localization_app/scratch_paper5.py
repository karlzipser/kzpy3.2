###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Localization_app'])
#
###############################
from kzpy3.vis2 import *
#from Main import *
Aruco_data = lo(opjD('A'))





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









def Camera_view_field(*args):
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







P[GRAPHICS] = True
if P[GRAPHICS]:
	CA()
	figure(1)



car_pts_ = [];head_pts_ = [];thetas_=[]

timer_ = Timer(0)

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

hxl_ = []
hyl_ = []
xl_ = []
yl_ = []


hx_ = False
hy_ = False
x_ = False
y_ = False

ctr_ = 0
a_ = 0.975

while True:

	Data_left,Data_right = Data_access[get_data]()

	if Data_left == False:
		break

	if P[GRAPHICS]:
		clf();
		there_ = False
	try:
		for Q in [Data_left,Data_right]:
			D=Camera_view_field(aruco_data,Q)
			timer = Timer(0)
			results = []
			min_error_ = 9999
			t_ctr_ = 0
			for theta_ in range(0,360,30):
				error_ = D[rotate_around](theta,theta_)
				if error_ < min_error_:
					min_error_ = error_
					min_theta_ = theta_
				t_ctr_+=1
			D[rotate_around](theta,min_theta_)
			car_pts_.append(D[pts_centered][0]);head_pts_.append(D[pts_centered][1]);thetas_.append(min_theta_)

			if P[GRAPHICS]:
				there_ = True
				plt_square();xysqlim(3);
				pts_plot(D[pts_centered][:1],'r');
				for i_ in range(1):
					plot_line(D[pts_centered][i_],D[pts_centered][i_+1],'r')
				for i_ in range(0,len(D[actual_pts]),2):
					plot_line(D[actual_pts][i_],D[actual_pts][i_+1],'g')
				pts_plot(D[actual_pts],'y');
				pts_plot(D[pts_centered][2:],'k');
				for i_ in range(2,len(D[pts_centered]),2):
					plot_line(D[pts_centered][i_],D[pts_centered][i_+1],'k')	

			if False:
				if hx_ == False:
					hx_ = head_pts_[-1][0]
					hy_ = head_pts_[-1][1]
				hx_ =  a_*hx_+(1-a_)*head_pts_[-1][0]  
				hy_ = a_*hy_+(1-a_)*head_pts_[-1][1] 
				if x_ == False:
					x_ = car_pts_[-1][0]
					y_ = car_pts_[-1][1]
				x_ =  a_*x_+(1-a_)*car_pts_[-1][0]  
				y_ = a_*y_+(1-a_)*car_pts_[-1][1]
			
			if True:
				if hx_ == False:
					hx_ = head_pts_[-1][0]
					hy_ = head_pts_[-1][1]
				hx_ =  a_*hx_+(1-a_)*head_pts_[-10][0]  
				hy_ = a_*hy_+(1-a_)*head_pts_[-10][1] 
				if x_ == False:
					x_ = car_pts_[-1][0]
					y_ = car_pts_[-1][1]
				x_ =  a_*x_+(1-a_)*car_pts_[-1][0]  
				y_ = a_*y_+(1-a_)*car_pts_[-1][1]
				x__ = (x_+hx_)/2.0
				y__ = (y_+hy_)/2.0


			if True:
				hxl_.append(hx_)
				hyl_.append(hy_)
				xl_.append(x__)
				yl_.append(y__)

			"""
			if hx_ == False:
				hx_ = [head_pts_[-1][0]]
				hy_ = [head_pts_[-1][1]]
			hx_.append(  a_*hx_[-1]+(1-a_)*na(head_pts_)[-1:,0]  )
			hy_.append(  a_*hy_[-1]+(1-a_)*na(head_pts_)[-1:,1]  )
			if x_ == False:
				x_ = [car_pts_[-1][0]]
				y_ = [car_pts_[-1][1]]
			x_.append(  a_*x_[-1]+(1-a_)*na(car_pts_)[-1:,0]  )
			y_.append(  a_*y_[-1]+(1-a_)*na(car_pts_)[-1:,1]  )
			"""
			
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
	
	try:
		if P[GRAPHICS] and there_:
			plot(hxl_,hyl_,'b.')
			plot(xl_,yl_,'y.')
			pause(0.0001)
		ctr_ += 1
		if np.mod(ctr_,1) == 0:
			spd2s(ctr_/timer_.time(),'hz')
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)






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


#EOF
