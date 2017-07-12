from kzpy3.vis import *
from kzpy3.teg9.data.markers_clockwise import markers_clockwise
import operator
import kzpy3.teg9.data.utils.multi_preprocess_pkl_files_1 as multi_preprocess_pkl_files_1
import kzpy3.teg9.data.utils.get_trajectory_points as get_trajectory_points
import kzpy3.teg9.data.utils.get_new_A as get_new_A

Origin = 300
Mult = 50
Extra = 10

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



colors = {'Mr_Yellow':(255,255,0), 'Mr_Silver':(255,255,255), 'Mr_Blue':(0,0,255), 'Mr_Orange':(255,0,0), 'Mr_Black':(100,100,100)}



def plot_trajectory_point(traj,side,i,t,out_img,c):
	assert(traj['ts'][i] <= t)
	if traj['ts'][i] == t:
		if traj[side]['t_vel'][i] > 2: # 1.788: # Above 4 mph
			c = (0,30,0)
		elif traj['camera_separation'][i] > 0.25: # almost larger than length of car
			c = (0,20,0)
		elif traj[side]['timestamp_gap'][i] > 0.1: # missed data points
			c = (0,10,0,0)		
		cv2.circle(out_img,(traj[side]['x_pix'][i],traj[side]['y_pix'][i]),1,c,-1)

DISPLAY_LEFT = True
#/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017/meta/direct_rewrite_test_30Apr17_12h29m10s_Mr_Black
if DISPLAY_LEFT:
	bag_folders_dst_rgb1to4_path = '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017/rgb_1to4'
	bag_folders_dst_meta_path = '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017/meta'# opjD('bair_car_data_new/meta')# '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017/meta'

N = lo(opjD('N.pkl'))


CAR_NAME = 'Mr_Blue'
RUN_NAME = 'direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue'

while True:
	try:
		CAR_NAME = random.choice(N.keys())
		RUN_NAME = random.choice(N[CAR_NAME].keys())
		if len(N[CAR_NAME][RUN_NAME]['other_trajectories']) < 2:
			continue
		print()
		print(RUN_NAME)
		print(CAR_NAME)
		for o in N[CAR_NAME][RUN_NAME]['other_trajectories']:
			print('\t'+get_trajectory_points.car_name_from_run_name(o['run_name']))

		traj1 = N[CAR_NAME][RUN_NAME]['self_trajectory']
		traj2 = N[CAR_NAME][RUN_NAME]['other_trajectories']

		if DISPLAY_LEFT:
			for traj in [traj1]:
				if True: #'data' not in traj.keys():
					traj['data'] = get_new_A.get_new_A()
					multi_preprocess_pkl_files_1.multi_preprocess_pkl_files(
						traj['data'],
						opj(bag_folders_dst_meta_path,traj['run_name']),
						opj(bag_folders_dst_rgb1to4_path,traj['run_name']))

		out_img *= 0
		draw_markers(out_img)
		cv2.putText(out_img,RUN_NAME,(50,2*Origin-50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255));

		timer = Timer(10)
		PAUSE = False
		i = 0
		while True: #i < len(traj1['ts']):
			if not PAUSE:
				if timer.check():
					out_img *= 0
					draw_markers(out_img)
					cv2.putText(out_img,RUN_NAME,(50,2*Origin-50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255));
					timer.reset()
			try:
				for traj in [traj1]+traj2:
					car_name = get_trajectory_points.car_name_from_run_name(traj['run_name'])
					if i < len(traj['ts']):
						t = traj['ts'][i]
						for side in ['left','right']:
							plot_trajectory_point(traj,side,i,t,out_img,colors[car_name])
			except Exception as e:
				print("********** Exception ***********************")
				print(time_str('Pretty'))
				print(e.message, e.args)
			if DISPLAY_LEFT:
				#print i #traj1['ts'][i]
				index = traj1['data']['t_to_indx'][traj1['ts'][i]]
				img = traj1['data']['left'][index]
				out_img[:shape(img)[0]+Extra,-Extra-shape(img)[1]:,:] = colors[get_trajectory_points.car_name_from_run_name(traj1['run_name'])]
				out_img[:shape(img)[0]:,-shape(img)[1]:] = img
				k = mci(out_img,delay=33)
				di = 0
				if k == ord('q'):
					print('q')
					break
				if k == ord('d'):
					print('done')
					exit()
				elif k == ord('k'):
					di = -30*2
				elif k == ord('l'):
					di = 30*2
				elif k == ord(' '):
					if PAUSE:
						PAUSE = False
					else:
						PAUSE = True
						print("<<pause>>")
				else:
					if not PAUSE:
						di = 1
				if abs(di) > 1:
					timer.trigger()
				i += di
				if i < 0:
					i = 0
				elif i >= len(traj1['ts']):
					print('At end')
					i = len(traj1['ts'])-1

		#raw_input('>>>>')
		
	except Exception as e:
		print("********** Exception ***********************")
		print(time_str('Pretty'))
		print(e.message, e.args)

	




