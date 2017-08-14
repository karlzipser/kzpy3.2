###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Localization_app'])
#
###############################
from vis2 import *
from Parameter_Module import *
from aruco_home_4x4_markers.py import Marker_xy_dic
from Project_Aruco_Markers_Module import Camera_View_Field
#from Main import *
exec(identify_file_str)

for a in Args.keys():
	_(P,a,equals,_(Args,a))


Aruco_data = lo(opjD('A'))

na = np.array


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

			
			D = Camera_View_Field(aruco_data,Q)
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
