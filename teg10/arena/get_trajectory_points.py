from kzpy3.vis import *
from kzpy3.teg9.data.markers_clockwise import markers_clockwise
import operator
#import kzpy3.teg9.data.utils.multi_preprocess_pkl_files_1 as multi_preprocess_pkl_files_1
import scipy.interpolate
CubicSpline = scipy.interpolate.CubicSpline


def car_name_from_run_name(rn):
	a = rn.split('Mr_')
	car_name = 'Mr_'+a[-1]
	car_name = car_name.replace('Mr_Yellow_A','Mr_Yellow')
	car_name = car_name.replace('Mr_Yellow_B','Mr_Yellow')
	return car_name



def get_cubic_spline(time_points,data,n=100):
	n = 10
	D = []
	T = []
	for i in range(n/2,len(time_points),n):
		D.append(data[i])#-n/2:i+n/2].mean())
		T.append(time_points[i])#-n/2:i+n/2].mean())
	D,T = array(D),array(T)
	cs = CubicSpline(T,D)
	if False:
		plot(time_points,data,'o')
		plot(T,D,'o', label='smoothed data')
		plot(time_points,cs(time_points),label="S")
		plt.legend(loc='lower left', ncol=2)
		pause(0.001)
	return cs



def timestamp_spline(M,run_name,side):
	dts = {}
	car_name = car_name_from_run_name(run_name)
	for t in M[car_name][run_name][side]['raw_time_stamps']:
		dts[t] = 1
	T = M[car_name][run_name][side]['time_stamps']
	for i in range(1,len(T)):
		dts[T[i]] = T[i]-T[i-1]
	_,dts_els = get_key_sorted_elements_of_dic(dts)
	return get_cubic_spline(M[car_name][run_name][side]['raw_time_stamps'],dts_els,20)


def get_xp_pts(M,run_name,timestamps,Mult,Origin,dt):
	car_name = car_name_from_run_name(run_name)
	pts = {}
	pts['ts'] = timestamps
	for side in ['left','right']:
		pts[side] = {}
		for xy in ['x','y']:
			pts[side][xy] = M[car_name][run_name][side]['cs_'+xy](pts['ts'])
		pts[side]['timestamp_gap'] = timestamp_spline(M,run_name,side)(pts['ts'])
		pts[side]['x_pix'] = (-Mult*array(pts[side]['x'])+Origin).astype(int)
		pts[side]['y_pix'] = (Mult*array(pts[side]['y'])+Origin).astype(int)
		plot(pts[side]['x'],pts[side]['y'],'o');xylim(-5,5,-5,5)
		A=pts[side]['x'].copy()
		B=pts[side]['y'].copy()
		C=A*0.0
		print(d2s('A',type(A),shape(A)))
		print(d2s('B',type(B),shape(B)))
		print(d2s('C',type(C),shape(C)))
		C[1:] = np.sqrt((A[1:]-A[:-1])**2+(B[1:]-B[:-1])**2)
		pts[side]['t_vel'] = C / dt
	pts['camera_separation'] = np.sqrt((pts['left']['x']-pts['right']['x'])**2 + (pts['left']['y']-pts['right']['y'])**2)
	pts['run_name'] = run_name
	return pts
	



