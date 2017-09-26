# http://nghiaho.com/uploads/code/rigid_transform_3D.py_

from numpy import *
from math import sqrt

# Input: expects Nx3 matrix of points
# Returns R,t
# R = 3x3 rotation matrix
# t = 3x1 column vector

def rigid_transform_3D(A, B):
    assert len(A) == len(B)
    A = matrix(A); B = matrix(B)
    N = A.shape[0]; # total points
    centroid_A = mean(A, axis=0)
    centroid_B = mean(B, axis=0)
    # centre the points
    AA = A - tile(centroid_A, (N, 1))
    BB = B - tile(centroid_B, (N, 1))
    # dot is matrix multiplication for array
    H = transpose(AA) * BB
    U, S, Vt = linalg.svd(H)
    R = Vt.T * U.T
    # special reflection case
    if linalg.det(R) < 0:
       #print "Reflection detected"
       Vt[2,:] *= -1
       R = Vt.T * U.T
    t = -R*centroid_A.T + centroid_B.T
    #print t
    return R, t






# 25 Sept. 2017
from kzpy3.Localization_app.Project_Aruco_Markers_Module import * 
from kzpy3.Localization_app.aruco_whole_room_markers_11circle_no_pillar import *
import kzpy3.data_analysis.Angle_Dict_Creator as Angle_Dict_Creator

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

if False:
	D = bagfile_to_dic(BAG_PATH='/media/karlzipser/rosbags/processed_23Sep17_17h48m38s/Mr_Purple_2017-09-23-17-10-53/bair_car_2017-09-23-17-18-23_12.bag' )
	so(D,opjD('one_bag_dic'))
if True:
	D = lo(opjD('one_bag_dic'))

n = len(D[left_image][vals])

graphics = False

if graphics: CA();figure(1);plt_square();xysqlim(3)

timer = Timer(1)

mmm = {}

for h in range(1):
	for i in range(n):
		try:
			mm = {}
			angles_to_center, angles_surfaces, distances_marker, markers = Angle_Dict_Creator.get_angles_and_distance(D[left_image][vals][i],borderColor=(h*20,255-h*20,0))#None)
			Q = {'angles_to_center':angles_to_center,'angles_surfaces':angles_surfaces,'distances_marker':distances_marker}
			d = Camera_View_Field(aruco_data,Q,'p',P)
			if graphics: clf(); plt_square(); xysqlim(3);pts_plot(d['pts']);spause();mci(D[left_image][vals][i],delay=1)
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



print('making mmm_overlap_dic')
mmm_overlap_dic = {}
for i in mmm.keys():
	for j in mmm.keys():
		if i != j:
			if len(set(mmm[i].keys()) & set(mmm[j].keys())) > 0:
				if i not in mmm_overlap_dic:
					mmm_overlap_dic[i] = []
				mmm_overlap_dic[i].append(j)
	#print len(mmm_overlap_dic[i])

max_num_markers_index = -1
max_num_markers_val = 0
for i in mmm.keys():
	if len(mmm[i]) > max_num_markers_val:
		max_num_markers_val = len(mmm[i])
		max_num_markers_index = i



www = {}

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



while True:#for i in range(100000):
	alpha = 0.3 # min(1.0,120/timer_total.time())
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
			stationary.append(list(na(www[marker_id].values()).mean(axis=0)+alpha*np.random.randn(2))+[0.0])
			moving.append(list(mmm[j][marker_id])+[0.0])
	if shape(moving)[0] < 3:
		continue
	ret_R,ret_t = rigid_transform_3D(moving,stationary)
	all_moving = matrix(all_moving)
	fitted = (ret_R*all_moving.T) + tile(ret_t,(1,len(all_moving)))
	fitted = fitted.T
	fitted = na(fitted)[:,:2]
	ctr = 0
	for marker_id in j_keys:
		mmm[j][marker_id] = fitted[ctr,:]
		if marker_id not in www:
			www[marker_id] = {}
		www[marker_id][j] = fitted[ctr,:]
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
				else:
					right_fitted.append(na(www[k].values()).mean(axis=0))
			pts_plot(na(right_fitted),'r');pts_plot(na(left_fitted),'g')
			pd2s('alpha =',dp(alpha,3))
			plt_square(); xysqlim(8);plt.title(len(mmm[j].values()));spause();#raw_enter()
			pts_timer.reset()
	#print all_moving
	#raw_enter()




pd2s('Done in ',dp(timer_total.time()),'seconds')
#CA();
figure('hist');hist(visited_dic.values(),bins=500)










True



#EOF
