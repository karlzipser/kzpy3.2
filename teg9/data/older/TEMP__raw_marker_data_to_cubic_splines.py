from kzpy3.vis import *
from kzpy3.teg9.data.markers_clockwise import markers_clockwise
import operator
import kzpy3.teg9.data.utils.multi_preprocess_pkl_files_1 as multi_preprocess_pkl_files_1
import kzpy3.teg9.data.utils.get_new_A as get_new_A
import scipy.interpolate
CubicSpline = scipy.interpolate.CubicSpline




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
for i in range(len(markers_clockwise)):
	m = markers_clockwise[i]
	xy = marker_xys[i]
	markers_xy_dic[m] = xy
	



def car_name_from_run_name(rn):
	a = rn.split('_')
	car_name = 'Mr_'+a[-1]
	return car_name



def get_camera_position(angles_to_center,angles_surfaces,distances_marker):
	marker_ids = angles_to_center.keys()
	x_avg = 0.0
	y_avg = 0.0
	d_sum = 0.0
	xs = []
	ys = []
	ds = []
	for m in marker_ids:
		if m in [190]: # This one gives false positives on ground.
			continue
		if m in markers_xy_dic:
			xy = markers_xy_dic[m]
			angle1 = angles_to_center[m]
			distance1 = distances_marker[m]
			distance2 = 4*107/100.
			angle2 = (np.pi+marker_angles_dic[m]) - (np.pi/2.0-angles_surfaces[m])
			xd = distance1 * np.sin(angle2)
			yd = distance1 * np.cos(angle2)
			#print (dp(np.degrees(marker_angles_dic[m]+np.pi/2.0-angles_surfaces[m]+angles_to_center[m]),2))#,dp(np.degrees(marker_angles_dic[m]),2),dp(np.degrees(angles_surfaces[m]),2),dp(np.degrees(angles_to_center[m],2)))
			if distance1 < 2*distance2 and distance1 > 0.05:
			#if distance1 < 2 and distance1 > 0.05:
				xs.append(xd+xy[0])
				ys.append(yd+xy[1])
				ds.append(distance1)
	d = 0
	for i in range(len(xs)):
		d += 1/ds[i]
		x_avg += d*xs[i]
		y_avg += d*ys[i]
		d_sum += d
	if len(ds) > 2:
		median_distance_to_markers = np.median(array(ds))
	elif len(ds) > 0:
		median_distance_to_markers = array(ds).min()
	else:
		median_distance_to_markers = None
	if d_sum == 0:
		return None,None,None,None
	x_avg /= d_sum
	y_avg /= d_sum
	return marker_ids,x_avg,y_avg,median_distance_to_markers





def init_car_path(marker_data_pkl,side):
	A = {}
	A['raw_marker_data'] = marker_data_pkl[side]
	A['x_avg'] = []
	A['y_avg'] = []
	A['time_stamps'] = []
	A['median_distance_to_markers'] = []
	A['raw_time_stamps'] = sorted(A['raw_marker_data'].keys())
	return A



def get_cubic_spline(time_points,data,n=100):
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
	return cs




def process_run_data(run_name,bag_folders_dst_meta_path,M):
	car_name = car_name_from_run_name(run_name)
	if car_name not in M:
		M[car_name] = {}
		if run_name not in M[car_name]:
			M[car_name]['run_name'] = run_name
			mdp_path = opj(bag_folders_dst_meta_path,run_name,'marker_data.pkl')
			print('Loading ' + mdp_path)
			marker_data_pkl = lo(mdp_path)
			print('processing marker data.')
			for side in ['left','right']:
				M[car_name]['run_name'] = {}
				M[car_name]['run_name'][side] = init_car_path(marker_data_pkl,side)
				for t in M[car_name]['run_name'][side]['raw_time_stamps']:
					angles_to_center = M[car_name]['run_name'][side]['raw_marker_data'][t]['angles_to_center']
					angles_surfaces = M[car_name]['run_name'][side]['raw_marker_data'][t]['angles_surfaces']
					distances_marker = M[car_name]['run_name'][side]['raw_marker_data'][t]['distances_marker']
					_,x_avg,y_avg,median_distance_to_markers = get_camera_position(angles_to_center,angles_surfaces,distances_marker)
					if is_number(x_avg) and is_number(y_avg) and is_number(median_distance_to_markers):
						M[car_name]['run_name'][side]['time_stamps'].append(t)
						M[car_name]['run_name'][side]['x_avg'].append(x_avg)
						M[car_name]['run_name'][side]['y_avg'].append(y_avg)
						M[car_name]['run_name'][side]['median_distance_to_markers'].append(median_distance_to_markers)
				M[car_name]['run_name'][side]['x_smooth'] = mean_exclude_outliers(M[car_name]['run_name'][side]['x_avg'],60,0.33,0.66)
				M[car_name]['run_name'][side]['y_smooth'] = mean_exclude_outliers(M[car_name]['run_name'][side]['y_avg'],60,0.33,0.66)
				CA()
				M[car_name]['run_name'][side]['cs_x'] = get_cubic_spline(M[car_name]['run_name'][side]['time_stamps'],M[car_name]['run_name'][side]['x_smooth'])
				M[car_name]['run_name'][side]['cs_y'] = get_cubic_spline(M[car_name]['run_name'][side]['time_stamps'],M[car_name]['run_name'][side]['y_smooth'])
				return [M[car_name]['run_name'][side]['cs_x'],M[car_name]['run_name'][side]['cs_y']]
				#del M[car_name]['run_name'][side]['raw_marker_data']




#M = {}
#init_run_data('direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue',M)



