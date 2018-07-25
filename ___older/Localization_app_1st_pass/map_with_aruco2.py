SETUP = 1
RELOAD = 0
RUN_LOOP = 1


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




if SETUP:
	# 
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











	if True:
		#D = Project_Aruco_Markers_Module.bagfile_to_dic(BAG_PATH='/media/karlzipser/rosbags/processed_23Sep17_17h48m38s/Mr_Purple_2017-09-23-17-10-53/bair_car_2017-09-23-17-18-23_12.bag' )
		D = Data_Module.bagfile_to_dic(BAG_PATH=opjD('Mr_Purple_2017-09-23-17-10-53/bair_car_2017-09-23-17-18-23_12.bag'))
		#D = Data_Module.bagfile_to_dic(BAG_PATH_LIST=sgg(opjD('Mr_Purple_2017-09-23-17-10-53/*.bag')) ) #'Mr_Black_2017-09-12-13-48-11/a/*.bag')) )
		#so(D,opjD('one_bag_dic2'))
	if False:
		D = lo(opjD('one_bag_dic2'))


	def get_Frame_data(img_lst):
		print('get_Frame_data(img_lst)')
		n = len(img_lst)
		graphics = False
		if graphics:figure(2);clf();plt_square();xysqlim(20)
		timer = Timer(1)
		F = {}
		for h in range(1):
			for i in range(n):
				#print i
				try:
					mm = {}
					angles_to_center_more = {}
					angles_surfaces_more = {}
					distances_marker_more = {}
					for r in range(10):
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
						F[i] = mm
				except Exception as e:
					print("********** Exception 123 ***********************")
					print(e.message, e.args)
				timer.message(d2s(i,int(100*i/(1.0*n)),'%'),color='white')
		Frame_data = F
		return Frame_data

	F = get_Frame_data(D[left_image][vals]+list(D[right_image][vals]))


	if False:
		print('making F_overlap_dic')
		F_overlap_dic = {}
		len_F = len(F.keys())
		timer = Timer(5)
		ctr = 0
		for i in F.keys():
			timer.percent_message(i,len_F)
			for f in F.keys():
				if i != f:
					if len(set(F[i].keys()) & set(F[f].keys())) > 0:
						if i not in F_overlap_dic:
							F_overlap_dic[i] = []
						F_overlap_dic[i].append(f)
			ctr += 1

	max_num_markers_index = -1
	max_num_markers_val = 0
	for i in F.keys():
		if len(F[i]) > max_num_markers_val:
			max_num_markers_val = len(F[i])
			max_num_markers_index = i




if RELOAD:
	F = lo(opjD('F.pkl'))
	W = lo(opjD('W.pkl'))
	max_num_markers_index = -1
	max_num_markers_val = 0
	for i in F.keys():
		if len(F[i]) > max_num_markers_val:
			max_num_markers_val = len(F[i])
			max_num_markers_index = i


if RUN_LOOP:
	radius = 144/2.0*2.5/100.0
	Constrained = {'210_left':na([0,radius]), '58_left':na([radius,0]), '218_left':na([-radius,0]), '228_left':na([0,-radius]),
		'220_left':na([-np.sqrt(2.0)/2.0*radius,np.sqrt(2.0)/2.0*radius]),
		'175_left':na([np.sqrt(2.0)/2.0*radius,np.sqrt(2.0)/2.0*radius]),
		'170_left':na([np.sqrt(2.0)/2.0*radius,-np.sqrt(2.0)/2.0*radius]),
		'133_left':na([-np.sqrt(2.0)/2.0*radius,-np.sqrt(2.0)/2.0*radius])
		}
	while True:
		
		run_timer = Timer(60*30)
		#CA()
		timer_total = Timer(0)
		timer = Timer(1)
		pts_timer = Timer(1)
		pts_timer2 = Timer(20)

		f = max_num_markers_index #np.random.choice(F.keys()) #   max_overlap_index
		W = {} # marker coordinates for different frame indicies
		for marker_id in F[f].keys():
			if marker_id not in W:
				W[marker_id] = {}
			W[marker_id][f] = F[f][marker_id]
		graphics = True
		first_time = True

		F_sorted_marker_keys = {}
		for f in F.keys():
			F_sorted_marker_keys[f] = sorted(F[f].keys())
		sorted_F_keys = sorted(F.keys())


		run_ctr = 0
		rotated = False
		while True:

			alpha = max(0,(0.5*run_timer.time_s - run_timer.time()) / run_timer.time_s)

			f = np.random.choice(F.keys())

			f_marker_keys = F_sorted_marker_keys[f]

			do_rotate = False
			if run_timer.time() > 20 and np.mod(run_ctr,5000) == 0:
				do_rotate = True
				a = 0.0
			else:
				a = alpha

			if True:#run_timer.time() < 2:
				stationary = []
				moving = []
				all_moving = []
				for marker_id in f_marker_keys:
					all_moving.append(list(F[f][marker_id])+[0.0])
					if marker_id in W.keys():
						stationary.append(list(na(W[marker_id].values()).mean(axis=0)+a*np.random.randn(2))+[0.0]   )
						moving.append(list(F[f][marker_id])+[0.0])
				if shape(moving)[0] < 3:
					continue

				ret_R,ret_t = rigid_transform_3D(moving,stationary)
				all_moving = np.matrix(all_moving)
				fitted = (ret_R*all_moving.T) + np.tile(ret_t,(1,len(all_moving)))
				fitted = fitted.T
				fitted = na(fitted)[:,:2]
				ctr = 0
				for marker_id in f_marker_keys:
					if marker_id not in W:
						W[marker_id] = {}
					W[marker_id][f] = fitted[ctr,:]
					ctr += 1

			if do_rotate:#run_timer.time() > 20 and np.mod(run_ctr,5000) == 0:# and rotated == False:# and run_ctr > 100:
				print('here')
				
				stationary = []
				moving = []
				all_moving = []
				all_moving_record = []
				lack_marker = False
				for marker_id in Constrained:
					if marker_id not in W.keys():
						lack_marker = True
						break

				if not lack_marker:
					lmax_mv = 0
					for marker_id in sorted(Constrained.keys()):
						stationary.append(list(Constrained[marker_id])+[0.0])
						moving.append(list(na(W[marker_id].values()).mean(axis=0))+[0.0])
						"""
						for f_ in W[marker_id].keys():
							if False:
								mv = (0.1 * (na(stationary[-1])-na(moving[-1])))[:2]
								lmv = length(mv)
								if lmv > lmax_mv:
									lmax_mv = lmv
								W[marker_id][f_] += mv
							if rotated:
								W[marker_id][f_] = na(stationary[-1])[:2]
						print lmax_mv
						"""

					print(na(stationary)-na(moving))

					if shape(moving)[0] > 3:
						rotated = True
						ret_R,ret_t = rigid_transform_3D(moving,stationary)

						for marker_id in sorted(W.keys()):
							moving2 = []
							for f_ in sorted(W[marker_id]):
								moving2.append(na(list(W[marker_id][f_])+[0]))
							#print marker_id,shape(moving2)

							moving2 = np.matrix(moving2)
							fitted = (ret_R*moving2.T) + np.tile(ret_t,(1,len(moving2)))
							fitted = fitted.T
							fitted = na(fitted)[:,:2]
							for f_ in sorted(W[marker_id]):
								W[marker_id][f_] = fitted[ctr,:]
								















			if True:
				if graphics:
					if pts_timer.check():
						clf()
						left_fitted = []
						right_fitted = []
						for k in W.keys():
							if 'left' in k:
								left_fitted.append(na(W[k].values()).mean(axis=0))
								plt.annotate(k.split('_')[0],left_fitted[-1])
							else:
								right_fitted.append(na(W[k].values()).mean(axis=0))
						#pts_plot(na(fitted),'c')
						pts_plot(na(right_fitted),'r');pts_plot(na(left_fitted),'g')
						#pd2s('alpha =',dp(alpha,3))
						plt_square(); xysqlim(3);plt.title( d2s(len(F[f].values())/2,dp(alpha) ) )  ;spause();
						pts_timer.reset()
				timer.message(d2s('\trun_ctr =',run_ctr,'alpha =',dp(alpha)),color='white',flush=True)
				if False:#run_timer.time() > 2 and first_time:
					keep = raw_input('keep? ')
					if keep != 'y':
						break
					else:
						first_time = False
			run_ctr += 1
			#time.sleep(0.1)

	#EOF
