# 





def rigid_transform_3D(A, B):
	"""
	http://nghiaho.com/uploads/code/rigid_transform_3D.py_
	Input: expects Nx3 matrix of points
	Returns R,t
	R = 3x3 rotation matrix
	t = 3x1 column vector
	"""
	#from numpy import *
	from math import sqrt
	assert len(A) == len(B)
	A = np.matrix(A); B = np.matrix(B)
	N = A.shape[0]; # total points
	centroid_A = np.mean(A, axis=0)
	centroid_B = np.mean(B, axis=0)
	# centre the points
	AA = A - np.tile(centroid_A, (N, 1))
	BB = B - np.tile(centroid_B, (N, 1))
	# dot is matrix multiplication for array
	H = np.transpose(AA) * BB
	U, S, Vt = np.linalg.svd(H)
	R = Vt.T * U.T
	# special reflection case
	if np.linalg.det(R) < 0:
	   #print "Reflection detected"
	   Vt[2,:] *= -1
	   R = Vt.T * U.T
	t = -R*centroid_A.T + centroid_B.T
	#print t
	return R, t






# 25 Sept. 2017
#import kzpy3.Localization_app.Project_Aruco_Markers_Module as Project_Aruco_Markers_Module



from kzpy3.Localization_app.Project_Aruco_Markers_Module import * 
from kzpy3.Localization_app.aruco_whole_room_markers_11circle_no_pillar import *
import kzpy3.data_analysis.Angle_Dict_Creator as Angle_Dict_Creator
import kzpy3.Car_Data_app.Data_Module as Data_Module
dont_know_why = True
if dont_know_why:
	P = {}
	P[VERBOSE] = True
	P[GRAPHICS] = False
	P[ROS_LIVE] = True
	P[past_to_present_proportion] = 0.99 # 0.5
	P[MARKERS_TO_IGNORE] = [190] # often has False positives
	P[DEGREE_STEP_FOR_ROTATION_FIT] = 5#15  # 10 to 30 range, bigger is faster
	P[ANGLE_DIST_PARAM] = 0.3



#def load


if True:
	#D = Project_Aruco_Markers_Module.bagfile_to_dic(BAG_PATH='/media/karlzipser/rosbags/processed_23Sep17_17h48m38s/Mr_Purple_2017-09-23-17-10-53/bair_car_2017-09-23-17-18-23_12.bag' )
	D = Data_Module.bagfile_to_dic(BAG_PATH_LIST=sgg(opjD('Mr_Purple_2017-09-23-17-10-53/*.bag')) ) #'Mr_Black_2017-09-12-13-48-11/a/*.bag')) )
	#so(D,opjD('one_bag_dic2'))
if False:
	D = lo(opjD('one_bag_dic2'))


def get_mmm(img_lst):
	print('get_mmm(img_lst)')
	n = len(img_lst)

	graphics = False
	if graphics: CA();figure(1);plt_square();xysqlim(3)
	timer = Timer(1)

	mmm = {}
	for h in range(1):
		for i in range(n):
			#print i
			try:
				mm = {}
				angles_to_center_more = {}
				angles_surfaces_more = {}
				distances_marker_more = {}
				for r in range(1):
					angles_to_center, angles_surfaces, distances_marker, markers = Angle_Dict_Creator.get_angles_and_distance(img_lst[i],borderColor=None)
					for k in angles_to_center.keys():
						if k not in angles_to_center_more.keys():
							angles_to_center_more[k] = []
							angles_surfaces_more[k] = []
							distances_marker_more[k] = []
						angles_to_center_more[k].append(angles_to_center[k])
						angles_surfaces_more[k].append(angles_surfaces[k])
						distances_marker_more[k].append(distances_marker[k])
				for k in angles_to_center_more.keys():
					#print angles_to_center_more[k]
					angles_to_center[k] = na(angles_to_center_more[k]).mean()
					angles_surfaces_more[k] = na(angles_surfaces_more[k]).mean()
					distances_marker_more[k] = na(distances_marker_more[k]).mean()
				Q = {'angles_to_center':angles_to_center,'angles_surfaces':angles_surfaces,'distances_marker':distances_marker}
				d = Camera_View_Field(aruco_data,Q,'p',P)
				if graphics: clf(); plt_square(); xysqlim(3);pts_plot(d['pts']);spause();mci(img_lst[i],delay=1)
				for m in d['markers'].keys():
					mm[d2n(m,'_left')] = d['markers'][m]['left']
					mm[d2n(m,'_right')] = d['markers'][m]['right']
				if len(mm) > 3:
					mmm[i] = mm
					#mmm_lens.append(len(mm))
			except Exception as e:
				print("********** Exception 123 ***********************")
				print(e.message, e.args)
			timer.message(d2s(i,int(100*i/(1.0*n)),'%'),color='white')
	return mmm

mmm = get_mmm(D[left_image][vals]) #+list(D[right_image][vals]))

"""
cARS
lEFT_IMAGE
aNGLES_SURFACES
rIGHT_IMAGE
"""

print('making mmm_overlap_dic')
mmm_overlap_dic = {}
len_mmm = len(mmm.keys())
timer = Timer(5)
ctr = 0
for i in mmm.keys():
	#timer.message(d2s(i,int(100*ctr/(1.0*len_mmm)),'%'),color='white')
	timer.percent_message(i,len_mmm)
	for j in mmm.keys():
		if i != j:
			if len(set(mmm[i].keys()) & set(mmm[j].keys())) > 0:
				if i not in mmm_overlap_dic:
					mmm_overlap_dic[i] = []
				mmm_overlap_dic[i].append(j)
	#print len(mmm_overlap_dic[i])
	ctr += 1

max_num_markers_index = -1
max_num_markers_val = 0
for i in mmm.keys():
	if len(mmm[i]) > max_num_markers_val:
		max_num_markers_val = len(mmm[i])
		max_num_markers_index = i

radius = 144/2.0*2.5/100.0
Constrained = {'210_left':na([0,radius]), '58_left':na([radius,0]), '218_left':na([-radius,0]), '228_left':na([0,-radius])}

while True:
	www = {}
	run_timer = Timer(60*10)
	CA()
	timer_total = Timer(0)
	timer = Timer(1)
	pts_timer = Timer(1)
	pts_timer2 = Timer(20)
	visited_dic = {}
	j = max_num_markers_index #np.random.choice(mmm.keys()) #   max_overlap_index
	for marker_id in mmm[j].keys():
		if marker_id not in www:
			www[marker_id] = {}
		www[marker_id][j] = mmm[j][marker_id]
	graphics = True
	first_time = True
	while True:#not run_timer.check():#for i in range(100000):
		if run_timer.time() > 2 and first_time:
			keep = raw_input('keep? ')
			if keep != 'y':
				break
			else:
				first_time = False
		alpha = max(0,(1*run_timer.time_s - run_timer.time()) / run_timer.time_s)

		if len(visited_dic) == len(mmm_overlap_dic):
			pass#break
		timer.message(d2s('\t',int(100*len(visited_dic)/(1.0*len(mmm))),'%'),color='white')
		if j not in visited_dic:
			visited_dic[j] = 1
		else:
			visited_dic[j] += 1
		if False:#len(visited_dic) < len(mmm_overlap_dic):
			j = np.random.choice(mmm_overlap_dic[j])
		else:
			j = np.random.choice(mmm.keys())
		if j == max_num_markers_index:
			continue
		j_keys = sorted(mmm[j].keys())
		stationary = []
		moving = []
		all_moving = []
		for marker_id in j_keys:
			all_moving.append(list(mmm[j][marker_id])+[0.0])
			if marker_id in www.keys():
				stationary.append(list(na(www[marker_id].values()).mean(axis=0))+[0.0]) #+alpha*np.random.randn(2)
				moving.append(list(mmm[j][marker_id])+[0.0])
		if shape(moving)[0] < 3:
			continue
		ret_R,ret_t = rigid_transform_3D(moving,stationary)
		all_moving = np.matrix(all_moving)
		fitted = (ret_R*all_moving.T) + np.tile(ret_t,(1,len(all_moving)))
		fitted = fitted.T
		fitted = na(fitted)[:,:2]
		ctr = 0
		for marker_id in j_keys:
			#mmm[j][marker_id] = fitted[ctr,:]
			if marker_id not in www:
				www[marker_id] = {}
			if False:#marker_id in Constrained:
				www[marker_id][j] = Constrained[marker_id]
			else:
				www[marker_id][j] = fitted[ctr,:]+1*alpha*np.random.randn(2)
			ctr += 1
		if graphics:
			if False: #pts_timer2.check():
				clf();
				pts_timer2.reset()
			#mci(D[left_image][vals][j],delay=1);
			if pts_timer.check():
				clf()
				left_fitted = []
				right_fitted = []
				for k in www.keys():
					if 'left' in k:
						left_fitted.append(na(www[k].values()).mean(axis=0))
						plt.annotate(k.split('_')[0],left_fitted[-1])
					else:
						right_fitted.append(na(www[k].values()).mean(axis=0))
				pts_plot(na(right_fitted),'r');pts_plot(na(left_fitted),'g')
				pd2s('alpha =',dp(alpha,3))
				plt_square(); xysqlim(8);plt.title( d2s(len(mmm[j].values()),dp(alpha) ) )  ;spause();#raw_enter()
				pts_timer.reset()






pd2s('Done in ',dp(timer_total.time()),'seconds')
#CA();
figure('hist');hist(visited_dic.values(),bins=500)










True



#EOF
