###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Localization_app'])
#
###############################
from Parameters_Module import *
from kzpy3.vis2 import *
import operator
import scipy.interpolate
CubicSpline = scipy.interpolate.CubicSpline
import importlib
exec(identify_file_str)


_ = dictionary_access

for a in Args.keys():
	_(P,a,equals,_(Args,a))



#marker_module_ = importlib.import_module(P[MARKER_SETUP],package=None)
#markers_xy_dic = marker_module_.markers_xy_dic
#marker_angles_dic_ = marker_module_.marker_angles_dic_
#get_camera_position = marker_module_.get_camera_position




def car_name_from_run_name(rn):
	a = rn.split('Mr_')
	car_name_ = 'Mr_'+a[-1]
	return car_name_







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
	pause(0.001)
	return cs




def process_run_data(*args):
	Args = args_to_dictionary(args)
	marker_data_path_ = Args[marker_data_path]
	True
	run_name_ = fname(pname(marker_data_path_))
	car_name_ = car_name_from_run_name(run_name_)
	M = {}
	if car_name_ not in M:
		M[car_name_] = {}
	if run_name_ not in M[car_name_]:
		M[car_name_][run_name_] = run_name_
		marker_data_pkl = lo(marker_data_path_)
		print('processing marker data.')
		M[car_name_][run_name_] = {}
		for side in ['left','right']:
			M[car_name_][run_name_][side] = init_car_path(marker_data_pkl,side)
			for t in M[car_name_][run_name_][side]['raw_time_stamps']:
				angles_to_center = M[car_name_][run_name_][side]['raw_marker_data'][t]['angles_to_center']
				angles_surfaces = M[car_name_][run_name_][side]['raw_marker_data'][t]['angles_surfaces']
				distances_marker = M[car_name_][run_name_][side]['raw_marker_data'][t]['distances_marker']
				_,x_avg,y_avg,median_distance_to_markers = get_camera_position(angles_to_center,angles_surfaces,distances_marker)
				if is_number(x_avg) and is_number(y_avg) and is_number(median_distance_to_markers):
					M[car_name_][run_name_][side]['time_stamps'].append(t)
					M[car_name_][run_name_][side]['x_avg'].append(x_avg)
					M[car_name_][run_name_][side]['y_avg'].append(y_avg)
					M[car_name_][run_name_][side]['median_distance_to_markers'].append(median_distance_to_markers)
			M[car_name_][run_name_][side]['x_smooth'] = mean_exclude_outliers(M[car_name_][run_name_][side]['x_avg'],60,0.33,0.66)
			M[car_name_][run_name_][side]['y_smooth'] = mean_exclude_outliers(M[car_name_][run_name_][side]['y_avg'],60,0.33,0.66)
			CA()
			M[car_name_][run_name_][side]['cs_x'] = get_cubic_spline(M[car_name_][run_name_][side]['time_stamps'],M[car_name_][run_name_][side]['x_smooth'])
			M[car_name_][run_name_][side]['cs_y'] = get_cubic_spline(M[car_name_][run_name_][side]['time_stamps'],M[car_name_][run_name_][side]['y_smooth'])
			del M[car_name_][run_name_][side]['raw_marker_data']
	return M




#M = {}
#init_run_data('direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue',M)





def multi_preprocess_bagfiles(*args):
	Args = args_to_dictionary(args)
	bag_folder_path_ = Args[bag_folder_path]
	dst_path_ = Args[dst_path]
	visualize_ = Args[visualize]
	print bag_folder_path_
	bag_files_ = sgg(opj(bag_folder_path_,'*.bag'))
	assert(len(bag_files_) > 0)
	run_name = fname(pname(bag_files[0]))
	if len(gg(opj(dst_path_,run_name_))) == 0:
		print("Making "+opj(dst_path_,run_name_))
		unix('mkdir -p '+opj(dst_path_,run_name_))
	if len(gg(opj(dst_path_,run_name_,'marker_data.pkl'))) == 1:
		print(opj(dst_path_,run_name_,'marker_data.pkl')+' exists, doing nothing.')
		return
	A = {}
	A[bag_folder_path_] = bag_folder_path_
	for s in ['left','right']:
		A[s] = {}
	for path_ in bag_files_:
		print('############## '+path_+' #############')
		try:
		   preprocess_bagfile(dic,A, path,path_, visualize,visualize_)
		except Exception as e:
			print("********** Exception ***********************")
			print(e.message, e.args)
	save_obj(A,opj(dst_path_,run_name_,'marker_data.pkl'))





def preprocess_bagfile(*args):
	Args = args_to_dictionary(args)
	path_ = Args[path]
	visualize_ = Args[visualize]
	
	A={}
	A[left] = {}
	A[right] = {}
	import kzpy3.data_analysis.Angle_Dict_Creator as Angle_Dict_Creator
	
	import rospy
	import rosbag
	import cv2
	from cv_bridge import CvBridge,CvBridgeError
	bridge = CvBridge()
	ctr = 0
	timer = Timer(0)

	cprint('Loading bagfile '+path_,'yellow')

	assert_disk_locations(path_)
	bag = rosbag.Bag(path_)

	color_mode = "rgb8"
	for s in ['left','right']:
		for m in bag.read_messages(topics=['/bair_car/zed/'+s+'/image_rect_color']):
			t = round(m.timestamp.to_time(),3)
			A[s][t] = {}
			img = bridge.imgmsg_to_cv2(m[1],color_mode)

			angles_to_center, angles_surfaces, distances_marker, markers = Angle_Dict_Creator.get_angles_and_distance(img)
			A[s][t]['angles_to_center'] = angles_to_center
			A[s][t]['angles_surfaces'] = angles_surfaces
			A[s][t]['distances_marker'] = distances_marker
			A[s][t]['markers'] = markers
			for i_ in rlen(markers):
				marker_id_ = markers[i_].marker_id
				corners_xy_ = markers[i_].corners_xy.astype(np.int)
				xy_ = corners_xy_.mean(axis=1)
				#print(shape(xy_))
				#print (marker_id_,corners_xy_,'mean:',xy_,xy_[0][1])
				x_ = int(xy_[0][0])
				y_ = int(xy_[0][1])
				try:
					cv2.putText(
						img,
						str(marker_id_),
						(x_,y_),
						cv2.FONT_HERSHEY_SIMPLEX,
						0.35,(255,0,0),1)
				except:
					print "put text failed"
			if visualize_ > 0:
				if np.mod(ctr,visualize_) == 0:
					#print(d2c(fname(path),s,t,A[s][t]['distances_marker']))
					k = mci(img,delay=300,scale=4)
					if k == ord('q'):
						break
				ctr += 1
	print(d2s('Done in',timer.time(),'seconds'))
	return A


A=preprocess_bagfile(path,'/media/karlzipser/ExtraDrive4/Mr_Yellow_23_24July2017/processed2/direct_home_LCR_Aruco1_23Jul17_20h51m31s_Mr_Yellow/bair_car_2017-07-23-20-52-11_1.bag', visualize,0)
L = A['left']
ts_ = sorted(L.keys())
















#EOF