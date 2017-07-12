from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])

from vis import *
from data.markers_clockwise import markers_clockwise
import data.utils.general
from data.utils.general import car_name_from_run_name
from data.utils.general import car_colors as colors

import data.arena
DISPLAY_LEFT = False
if DISPLAY_LEFT:
	import data.utils.multi_preprocess_pkl_files_1





bair_car_data_location = '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'
bag_folders_dst_rgb1to4_path = opj(bair_car_data_location,'rgb_1to4')
bag_folders_dst_meta = opj(bair_car_data_location,'meta')





markers = data.arena.Markers(range(96),4*107/100.)
Origin = 300
Mult = 50
out_img = Image([Origin*2,Origin*2,3],Origin,Mult)
markers['cv2_draw'](markers,out_img)





if 'N' not in locals():
	N = lo(opjD('N.pkl'))







def plot_trajectory_point(traj,side,i,t,out_img,c):
	assert(traj['ts'][i] <= t)
	if traj['ts'][i] == t:
		if traj[side]['t_vel'][i] > 2: # 1.788: # Above 4 mph
			c = (0,30,0)
		elif traj['camera_separation'][i] > 0.25: # almost larger than length of car
			c = (0,20,0)
		elif traj[side]['timestamp_gap'][i] > 0.1: # missed data points
			c = (0,10,0,0)
		cv2.circle(out_img['img'],(traj[side]['x_pix'][i],traj[side]['y_pix'][i]),1,c,-1)







Done = False

while not Done:
	if True:#try:
		traj_lst = []
		CAR_NAME = random.choice(N.keys())
		RUN_NAME = random.choice(N[CAR_NAME].keys())
		if len(N[CAR_NAME][RUN_NAME]['other_trajectories']) < 2:
			continue
		for ot in [N[CAR_NAME][RUN_NAME]['self_trajectory']]+N[CAR_NAME][RUN_NAME]['other_trajectories']:
			run_name = ot['run_name']
			car_name = car_name_from_run_name(run_name)
			traj_lst.append( N[car_name][run_name]['self_trajectory'] )
			print(car_name,run_name)

		for i in range(4):
			traj_lst[i]['data'] = data.utils.general.get_new_Data_dic()
			if DISPLAY_LEFT:
				data.utils.multi_preprocess_pkl_files_1.multi_preprocess_pkl_files(
					traj_lst[i]['data'],
						opj(bag_folders_dst_meta_path,traj_lst[i]['run_name']),
						opj(bag_folders_dst_rgb1to4_path,traj_lst[i]['run_name']))

		T0 = traj_lst[0]['ts'][0]
		t = T0
		Tn = traj_lst[0]['ts'][-1]
		DT = 1/30.
		dt = DT
		timer = Timer(10)
		PAUSE = False
		out_img['img'] *= 0
		markers['cv2_draw'](markers,out_img)
		cv2.putText(out_img['img'],RUN_NAME,(50,2*Origin-50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255));



		while t < traj_lst[0]['ts'][-1]:

			if not PAUSE:
				if timer.check():
					out_img['img'] *= 0
					markers['cv2_draw'](markers,out_img)
					cv2.putText(out_img['img'],RUN_NAME,(50,2*Origin-50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255));
					timer.reset()

			ctr = 0
			for traj in traj_lst:
				car_name = car_name_from_run_name(traj['run_name'])
				if t>traj['ts'][0] and t<traj['ts'][-1]:
					near_t = -1
					for i in range(1,len(traj['ts'])):
						if traj['ts'][i-1]<t and traj['ts'][i]>t:
							near_t = traj['ts'][i]
							near_i = i
							break
					if near_t > 0:
						for side in ['left','right']:
							plot_trajectory_point(traj,side,near_i,near_t,out_img,colors[car_name])
						if ctr < 4 and DISPLAY_LEFT:
							quadrant = ctr
							index = traj['data']['t_to_indx'][near_t]
							img = traj['data']['left'][index]
							if quadrant == 0:
								out_img['img'][:shape(img)[0]+E,:E+shape(img)[1],:] = colors[car_name]
								out_img['img'][:shape(img)[0],:shape(img)[1]] = img
							elif quadrant == 1:
								out_img['img'][-E-shape(img)[0]:,:E+shape(img)[1],:] = colors[car_name]
								out_img['img'][-shape(img)[0]:,:shape(img)[1]] = img
							elif quadrant == 2:
								out_img['img'][:shape(img)[0]+E,-E-shape(img)[1]:,:] = colors[car_name]
								out_img['img'][:shape(img)[0]:,-shape(img)[1]:] = img
							elif quadrant == 3:
								out_img['img'][-E-shape(img)[0]:,-E-shape(img)[1]:,:] = colors[car_name]
								out_img['img'][-shape(img)[0]:,-shape(img)[1]:] = img

				ctr += 1

			k = mci(out_img['img'],delay=33)


			if not PAUSE:
				dt = DT
			if k == ord('q'):
				print('q')
				break
			if k == ord('d'):
				print('done')
				DONE = True
				cv2.destroyAllWindows()
				sys.exit()
			elif k == ord('k'):
				dt = -2
			elif k == ord('l'):
				dt = 2
			elif k == ord(' '):
				if PAUSE:
					PAUSE = False
					print("<<end pause>>")
				else:
					PAUSE = True
					dt = 0
					print("<<pause>>")


			if abs(dt) > DT:
				timer.trigger()

			t += dt

			if t < T0:
				t = T0
			elif t >= Tn:
				print('At end')
				t = Tn-1


	"""

	except Exception as e:
		print("********** Exception ***********************")
		print(time_str('Pretty'))
		print(e.message, e.args)

	"""





