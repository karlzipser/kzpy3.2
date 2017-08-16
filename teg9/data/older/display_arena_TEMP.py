from kzpy3.vis import *
from kzpy3.teg9.data.markers_clockwise import markers_clockwise
import operator
import kzpy3.teg9.data.utils.multi_preprocess_pkl_files_1 as multi_preprocess_pkl_files_1
import scipy.interpolate
CubicSpline = scipy.interpolate.CubicSpline



Origin = 300
Mult = 50
E = 10

out_img = zeros((Origin*2,Origin*2,3),np.uint8)

marker_ids_all = []
marker_angles_dic = {}
marker_angles = 2*np.pi*np.arange(len(markers_clockwise))/(1.0*len(markers_clockwise))
marker_xys = []
for i in range(len(markers_clockwise)):
	a = marker_angles[i]
	marker_angles_dic[markers_clockwise[i]] = a
	x = 4*107/100.*np.sin(a)
	y = 4*107/100.*np.cos(a)
	marker_xys.append([x,y])

markers_xy_dic = {}
assert(len(markers_clockwise) == len(marker_xys))

def meters_to_pixels(x,y):
	return (int(-Mult*x)+Origin),(int(Mult*y)+Origin)

def draw_markers(out_img):
	for j in range(len(markers_clockwise)):
		m = markers_clockwise[j]
		xy = marker_xys[j]
		markers_xy_dic[m] = xy
		c = (255,0,0)
		xp,yp = meters_to_pixels(xy[0],xy[1])
		cv2.circle(out_img,(xp,yp),4,c,-1)



def car_name_from_run_name(rn):
	a = rn.split('Mr_')
	car_name = 'Mr_'+a[-1]
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
	for t in M[car_name][run_name][side]['raw_time_stamps']:
		dts[t] = 1
	T = M[car_name][run_name][side]['time_stamps']
	for i in range(1,len(T)):
		dts[T[i]] = T[i]-T[i-1]
	_,dts_els = get_key_sorted_elements_of_dic(dts)
	return get_cubic_spline(M[car_name][run_name][side]['raw_time_stamps'],dts_els,20)


def get_xp_pts(M,run_name,):
	pts = {}
	pts['ts'] = 
	for side in ['left','right']:
		pts[side] = {}
		for xy in ['x','y']:
			pts[side][xy] = M[car_name][run_name][side]['cs_'+xy](pts['ts'])
		pts[side]['timestamp_gap'] = timestamp_spline(M,run_name,side)(pts['ts'])
		pts[side]['x_pix'] = (-Mult*array(pts[side]['x'])+Origin).astype(int)
		pts[side]['y_pix'] = (Mult*array(pts[side]['y'])+Origin).astype(int)
		A=pts[side]['x'].copy()
		B=pts[side]['y'].copy()
		C=A*0
		C[1:] = sqrt((A[1:]-A[:-1])**2+(B[1:]-B[:-1])**2)
		pts[side]['t_vel'] = C / dt
	pts['camera_separation'] = sqrt((pts['left']['x']-pts['right']['x'])**2 + (pts['left']['y']-pts['right']['y'])**2)
	return pts
	



if False:

bag_folders_path = opjD('bair_car_data_new')
bag_folders_meta_path = opj(bag_folders_path,'meta')




M = {}
c=(255,0,0)
delay = 1#int(1000/30.0)
run_name = 'direct_rewrite_test_25Apr17_15h57m04s_Mr_Black'
run_name = 'direct_caffe_Fern_aruco_15Apr17_14h02m46s_Mr_Blue'
run_name = 'direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue'
run_name = 'direct_rewrite_test_30Apr17_11h50m02s_Mr_Blue'

car_name = car_name_from_run_name(run_name)
if car_name not in M:
	M[car_name] = {}
M[car_name][run_name] = lo(opj(bag_folders_meta_path,run_name,'trajectory.pkl'))




t0 = max(M[car_name][run_name]['left']['time_stamps'][0],M[car_name][run_name]['right']['time_stamps'][0])
tn = max(M[car_name][run_name]['left']['time_stamps'][-1],M[car_name][run_name]['right']['time_stamps'][-1])
dt = 1/30.0
ts = arange(t0,tn,dt)

pts = get_xp_pts(M,run_name,ts)




for i in range(len(pts['left']['y_pix'])):
	if np.mod(i,30*30*60) == 0:
		out_img *= 0
	for side in ['left','right']:
		xp,yp = pts[side]['x_pix'][i],pts[side]['y_pix'][i]
		#print pts['camera_separation'][i]
		if pts[side]['t_vel'][i] > 1.788: # Above 4 mph
			c = (255,255,255)
		elif pts['camera_separation'][i] > 0.25: # almost larger than length of car
			c = (0,255,0)
		elif pts[side]['timestamp_gap'][i] > 0.1: # missed data points
			c = (255,0,0)
		else:
			c = (0,0,255)
		cv2.circle(out_img,(xp,yp),1,c,-1)
		k = mci(out_img,delay=1)
		if k == ord('q'):
			break


