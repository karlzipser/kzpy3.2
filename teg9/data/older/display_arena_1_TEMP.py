from kzpy3.vis import *
from kzpy3.teg9.data.markers_clockwise import markers_clockwise
import operator
import kzpy3.teg9.data.utils.multi_preprocess_pkl_files_1 as multi_preprocess_pkl_files_1
import kzpy3.teg9.data.utils.get_trajectory_points as get_trajectory_points
import kzpy3.teg9.data.utils.get_new_A as get_new_A

Origin = 300
Mult = 50

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


Origin = 300
Mult = 50
Extra = 10


bk = N['Mr_Black']['direct_rewrite_test_28Apr17_17h50m34s_Mr_Black']['self_trajectory']
yl = N['Mr_Yellow']['direct_rewrite_test_29Apr17_00h50m25s_Mr_Yellow']['self_trajectory']
si = N['Mr_Silver']['direct_rewrite_test_28Apr17_17h51m01s_Mr_Silver']['self_trajectory']
bu = N['Mr_Blue']['direct_rewrite_test_28Apr17_17h50m31s_Mr_Blue']['self_trajectory']
og = N['Mr_Orange']['direct_rewrite_test_28Apr17_17h59m53s_Mr_Orange']['self_trajectory']

traj_lst = [bk,yl,si,bu,og]

traj_lst[0]['data'] = get_new_A.get_new_A()
multi_preprocess_pkl_files_1.multi_preprocess_pkl_files(
	traj_lst[0]['data'],
		opj(bag_folders_dst_meta_path,traj_lst[0]['run_name']),
		opj(bag_folders_dst_rgb1to4_path,traj_lst[0]['run_name']))

t = traj_lst[0]['ts'][0]

dt = 1/30.
while t < traj_lst[0]['ts'][-1]:
	for traj in traj_lst:
		car_name = get_trajectory_points.car_name_from_run_name(traj['run_name'])
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
	t += dt
	index = traj_lst[0]['data']['t_to_indx'][traj_lst[0]['ts'][i]]
	img = traj_lst[0]['data']['left'][index]
	out_img[:shape(img)[0]+Extra,-Extra-shape(img)[1]:,:] = colors[get_trajectory_points.car_name_from_run_name(traj_lst[0]['run_name'])]
	out_img[:shape(img)[0]:,-shape(img)[1]:] = img

	k = mci(out_img,delay=3)


