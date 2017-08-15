###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Localization_app'])
#
###############################
import Parameters_Module
from Parameters_Module import *
from vis2 import *
from Project_Aruco_Markers_Module import Aruco_Trajectory
#from Main import *
exec(identify_file_str)
na = np.array

for a_ in Args.keys():
	P[a_] = Args[a_]


Aruco_trajectory = Aruco_Trajectory()
if P[GRAPHICS]:
	CA()


def get_cubic_spline(time_points,data,n=100):
	import scipy.interpolate
	CubicSpline = scipy.interpolate.CubicSpline
	n = 10
	D = []
	T = []
	for i in range(n/2,len(time_points),n):
		D.append(data[i])#-n/2:i+n/2].mean())
		T.append(time_points[i])#-n/2:i+n/2].mean())
	D,T = array(D),array(T)
	cs = CubicSpline(T,D)
	plot(time_points,data,'o')
	plot(T,D,'o', label='smoothed data')
	plot(time_points,cs(time_points),label="S")
	plt.legend(loc='lower left', ncol=2)
	pause(0.001)
	return cs


Markers = lo('/home/karlzipser/Desktop/meta/direct_home_LCR_Aruco1_23Jul17_20h51m31s_Mr_Yellow/marker_data.pkl')




graphics_timer = Timer(1.0)
Aruco_trajectories = {}
exception_count_ = 0
try_count_ = 0
for side_ in [left,right]:
	Aruco_trajectories[side_] = {}
	for q_ in [x,y,hx,hy]:

		Aruco_trajectories[side_][ts] = []
		Aruco_trajectories[side_][q_] = []

	ts_ = sorted(Markers[side_].keys())
	
	for t_ in ts_:
		try_count_ += 1
		try:
			Data_ = Markers[side_][t_]
			hx_,hy_,x_,y_ =	Aruco_trajectory[step](one_frame_aruco_data,Data_, p,P)
			Aruco_trajectories[side_][ts].append(t_)
			for q_ in [x,y,hx,hy]:
				
				exec(d2s('Aruco_trajectories[side_][',q_,'].append(',q_ + '_ )'))
			if graphics_timer.check():
				figure(5);clf();plt_square();xysqlim(2*107.0/100.0);
				plot(Aruco_trajectories[side_][x],Aruco_trajectories[side_][y],'.');pause(0.001)
				graphics_timer.reset()
		except Exception as e:
			print("********** Exception ***********************")
			print(e.message, e.args)
			exception_count_ += 1
			print(exception_count_,dp(exception_count_/(1.0*try_count_)*100),try_count_,len(ts_))

	for q_ in [x,y,hx,hy,ts]:
		Aruco_trajectories[side_][q_] = na(Aruco_trajectories[side_][q_])
		if q_ != ts:
			Aruco_trajectories[side_][q_+'_meo'] = meo( na(Aruco_trajectories[side_][q_]), 30)



	
F = h5w(opjD('temp.h5py'))
for side_ in Aruco_trajectories.keys():
	F.create_group(side_)
	for q_ in Aruco_trajectories[side_].keys():
		F[side_].create_dataset(q_,data=Aruco_trajectories[side_][q_])
F.close()


Cubic_splines = {}
for side_ in Aruco_trajectories.keys():
	Cubic_splines[side_] = {}
	for q_ in Aruco_trajectories[side_].keys():
		if q_ == ts:
			pass
		else:
			figure('splines');clf()
			Cubic_splines[side_][q_] = get_cubic_spline(Aruco_trajectories[side_][ts],Aruco_trajectories[side_][q_])
so(opjD('Cubic_splines'),Cubic_splines)





"""
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
"""

#EOF
