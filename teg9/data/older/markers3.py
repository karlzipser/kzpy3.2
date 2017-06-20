from kzpy3.vis import *
from kzpy3.teg9.data.markers_clockwise import markers_clockwise
import operator
import kzpy3.teg9.data.utils.multi_preprocess_pkl_files_1 as multi_preprocess_pkl_files_1
import kzpy3.teg9.data.utils.data.get_new_A as get_new_A

O = 300
M = 50
E = 10

out_img = zeros((O*2,O*2,3),np.uint8)


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
for i in range(len(markers_clockwise)):
	m = markers_clockwise[i]
	xy = marker_xys[i]
	markers_xy_dic[m] = xy
	cv2.circle(out_img,(int(100*xy[0])+500,int(100*xy[1])+500),4,(255,0,0),-1)



def init_car_path(marker_data_pkl,side,name):
	A = {}
	A['marker_data_pkl'] = marker_data_pkl[side]
	A['x_avgs'] = []
	A['y_avgs'] = []
	A['pts'] = []
	A['ts'] = sorted(A['marker_data_pkl'].keys())
	A['timestamp_index'] = 0
	A['name'] = name
	return A


def plot_it2(angle1,distance1,angle2,distance2,xy):

	xd = distance1 * np.sin(angle2)
	yd = distance1 * np.cos(angle2)

	plot([xy[0],xd+xy[0]],[xy[1],yd+xy[1]])

	pause(0.001)

bag_folders_dst_rgb1to4_path = '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017/rgb_1to4'
bag_folders_dst_meta_path = '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017/meta'


run_name = 'direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue'
Mr_Blue_marker_data_pkl = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/'+run_name+'/marker_data.pkl')
Bul = init_car_path(Mr_Blue_marker_data_pkl,'left','Mr_Blue')
Bul['data'] = get_new_A.get_new_A()
Bur = init_car_path(Mr_Blue_marker_data_pkl,'right','Mr_Blue_right')
multi_preprocess_pkl_files_1.multi_preprocess_pkl_files(Bul['data'],opj(bag_folders_dst_meta_path,run_name),opj(bag_folders_dst_rgb1to4_path,run_name))



run_name = 'direct_rewrite_test_28Apr17_17h23m15s_Mr_Black'
Mr_Black_marker_data_pkl = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/'+run_name+'/marker_data.pkl')
Bkl = init_car_path(Mr_Black_marker_data_pkl,'left','Mr_Black')
Bkl['data'] = get_new_A.get_new_A()
Bkr = init_car_path(Mr_Black_marker_data_pkl,'right','Mr_Black_right')
multi_preprocess_pkl_files_1.multi_preprocess_pkl_files(Bkl['data'],opj(bag_folders_dst_meta_path,run_name),opj(bag_folders_dst_rgb1to4_path,run_name))



run_name = 'direct_rewrite_test_29Apr17_00h23m07s_Mr_Yellow'
Mr_Yellow_marker_data_pkl = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/'+run_name+'/marker_data.pkl')
Yl = init_car_path(Mr_Yellow_marker_data_pkl,'left','Mr_Yellow')
Yl['data'] = get_new_A.get_new_A()
Yr = init_car_path(Mr_Yellow_marker_data_pkl,'right','Mr_Yellow_right')
multi_preprocess_pkl_files_1.multi_preprocess_pkl_files(Yl['data'],opj(bag_folders_dst_meta_path,run_name),opj(bag_folders_dst_rgb1to4_path,run_name))



run_name = 'direct_rewrite_test_28Apr17_17h27m30s_Mr_Silver'
Mr_Silver_marker_data_pkl = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/'+run_name+'/marker_data.pkl')
Sl = init_car_path(Mr_Silver_marker_data_pkl,'left','Mr_Silver')
Sl['data'] = get_new_A.get_new_A()
Sr = init_car_path(Mr_Silver_marker_data_pkl,'right','Mr_Silver_right')
multi_preprocess_pkl_files_1.multi_preprocess_pkl_files(Sl['data'],opj(bag_folders_dst_meta_path,run_name),opj(bag_folders_dst_rgb1to4_path,run_name))



Bur['pts'] = []
Bul['pts'] = []




#Mr_Black_marker_data_pkl = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/direct_rewrite_test_28Apr17_17h23m15s_Mr_Black/marker_data.pkl')

#Mr_Silver_marker_data_pkl = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/direct_rewrite_test_28Apr17_18h12m54s_Mr_Silver/marker_data.pkl' )

#Mr_Orange_marker_data_pkl = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/direct_rewrite_test_25Apr17_14h32m22s_Mr_Orange/marker_data.pkl' )
#A = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/direct_rewrite_test_25Apr17_13h09m04s_Mr_Black/marker_data.pkl')
#A = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/direct_rewrite_test_25Apr17_13h09m04s_Mr_Black/marker_data.pkl')
#A = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/direct_rewrite_test_25Apr17_21h31m25s_Mr_Yellow/marker_data.pkl')
#marker_data_pkl = Marker_Raw_Data['Mr_Yellow']['direct_rewrite_test_25Apr17_21h31m25s_Mr_Yellow']
#Mr_Yellow_marker_data_pkl = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/direct_rewrite_test_25Apr17_21h31m25s_Mr_Yellow/marker_data.pkl')








def get_position_and_heading(angles_to_center,angles_surfaces,distances_marker):
	marker_ids = angles_to_center.keys()
	x_avg = 0.0
	y_avg = 0.0
	d_sum = 0.0
	xs = []
	ys = []
	ds = []
	headings = []

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
				h = marker_angles_dic[m]+angles_surfaces[m]-np.pi/2.0+angles_to_center[m]
				#print h
				headings.append(h)

	d = 0
	for i in range(len(xs)):
		d += 1/ds[i]
		x_avg += d*xs[i]
		y_avg += d*ys[i]
		heading_avg = d*headings[i]
		d_sum += d

	median_d = np.median(array(ds))
	if d_sum == 0:
		return None,None,None,None
	x_avg /= d_sum
	y_avg /= d_sum
	heading_avg /= d_sum
	index,value = min(enumerate(ds),key=operator.itemgetter(1))
	heading_avg = headings[index]+np.pi/2.0
	median_d = max(median_d,1)
	median_d = median_d**2+3



	return marker_ids,x_avg,y_avg,median_d,heading_avg













def show_timepoint(A,timestamp,out_img,dot_color,max_dt=60/1000.,start_index=0,hour_correction=0,quadrant=0,TEMPORAL_SMOOTHING=False,SHOW_GRAPHICS=True):
	if 'heading_prev' not in A:
		A['heading_prev'] = 0
	try:
		A['timestamp_index'] = start_index
		while A['ts'][A['timestamp_index']] < timestamp:	
			A['timestamp_index'] += 1
		if A['ts'][A['timestamp_index']]-timestamp > max_dt:
			print A['ts'][A['timestamp_index']]-timestamp
			return

		i = A['timestamp_index']
		ts = A['ts']


		

		if quadrant == None:
			pass
		else:
			img = A['data'] ['left'] [i] #[A['data']['t_to_indx']] [ts[i]]
			if quadrant == 0:
				out_img[:shape(img)[0]+E,:E+shape(img)[1],:] = [0,0,255]
				out_img[:shape(img)[0],:shape(img)[1]] = img
			elif quadrant == 1:
				out_img[-E-shape(img)[0]:,:E+shape(img)[1],:] = [100,100,100]
				out_img[-shape(img)[0]:,:shape(img)[1]] = img
			elif quadrant == 2:
				out_img[:shape(img)[0]+E,-E-shape(img)[1]:,:] = [255,255,0]
				out_img[:shape(img)[0]:,-shape(img)[1]:] = img
			elif quadrant == 3:
				out_img[-E-shape(img)[0]:,-E-shape(img)[1]:,:] = [255,255,255]
				out_img[-shape(img)[0]:,-shape(img)[1]:] = img

		angles_to_center = A['marker_data_pkl'][ts[i]]['angles_to_center']
		angles_surfaces = A['marker_data_pkl'][ts[i]]['angles_surfaces']
		distances_marker = A['marker_data_pkl'][ts[i]]['distances_marker']

		marker_ids,x_avg,y_avg,median_d,heading = get_position_and_heading(angles_to_center,angles_surfaces,distances_marker)
		#print np.degrees(heading - A['heading_prev'])
		if marker_ids == None:
			return
		A['x_avgs'].append(x_avg)
		A['y_avgs'].append(y_avg)
		if len(A['x_avgs'])>10:
			if TEMPORAL_SMOOTHING != False:
				e = TEMPORAL_SMOOTHING # 5
				x = array(A['x_avgs'][-int(e*median_d):]).mean()
				y = array(A['y_avgs'][-int(e*median_d):]).mean()
			else:
				x,y = x_avg,y_avg

			A['pts'].append([x,y,ts[i]])
			#if len(A['pts']) > 100:
			#	A['pts'] = A['pts'][-100:]
			if len(A['pts'])>11:
				"""
				for qq in range(10,0,-1):
					x,y = A['pts'][-qq][0],A['pts'][-qq][1]
					new_dot_color = array(dot_color)/(np.sqrt(qq))
					x2,y2 = x+0.4*np.sin(heading),y+0.4*np.cos(heading)
					if np.mod(i,10) == 0:
						cv2.line(out_img,(int(-100*x)+500,int(100*y)+500),(int(-100*x2)+500,int(100*y2)+500),(255,255,255))
					cv2.circle(out_img,(int(-100*x)+500,int(100*y)+500),4,new_dot_color,-1)
				"""

				x,y = A['pts'][-1][0],A['pts'][-1][1]
				xp,yp = A['pts'][-2][0],A['pts'][-2][1]


				dx,dy = (x-xp),(y-yp)
				sq = np.sqrt(dx**2+dy**2)
				x2,y2 = x+0.1*dx/sq,y+0.1*dy/sq
				new_dot_color = dot_color
				#new_dot_color = array(dot_color)/(np.sqrt(qq))
				#x2,y2 = x+0.4*np.sin(heading),y+0.4*np.cos(heading)
				#cv2.circle(out_img,(int(-100*x)+500,int(100*y)+500),4,new_dot_color,-1)
				if SHOW_GRAPHICS:
					if np.mod(i,1) == 0:
						cv2.line(out_img,(int(-M*x)+O,int(M*y)+O),(int(-M*x2)+O,int(M*y2)+O),new_dot_color)


			if SHOW_GRAPHICS:
				for j in range(len(markers_clockwise)):
					m = markers_clockwise[j]
					xy = marker_xys[j]
					markers_xy_dic[m] = xy
					c = (255,0,0)
					if m in marker_ids:
						c = (0,255,0)
						cv2.circle(out_img,(int(-M*xy[0])+O,int(M*xy[1])+O),4,c,-1)

		if SHOW_GRAPHICS:
			if True: #quadrant == 0:
				k = mci(out_img,delay=1,title='out_img')
				if k == ord('q'):
					return;	
		if len(A['x_avgs']) > 100:
			A['x_avgs'] = A['x_avgs'][-100:]
			A['y_avgs'] = A['y_avgs'][-100:]
		A['heading_prev'] = heading

	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
		time.sleep(0.01)



SAVE_GRAPHICS = True
frame_ctr = 0
out_img *= 0
iprev = 0
tprev = 0
for i in range(7750,20000): #len(Bul['ts'])): #range(len(Bul['ts'])): #
	if np.mod(i,10*30) == 0:
		out_img *= 0
	print i
#	out_img -= 1
	if np.mod(i,20*30000) == 0:
		out_img *= 0
	t =  i/30.
	#print t
	t += Bul['ts'][0]
	for j in range(len(markers_clockwise)):
		m = markers_clockwise[j]
		xy = marker_xys[j]
		markers_xy_dic[m] = xy
		c = (255,0,0)
		cv2.circle(out_img,(int(-M*xy[0])+O,int(M*xy[1])+O),4,c,-1)
	#img2 = Bul[]
	#show_timepoint(Bul,t,out_img,(  0,  0,255),100000.,0,0,0,10,True)
	#show_timepoint(Bkl,t,out_img,(100,100,100),100000.,0,0,1,10,True)
	show_timepoint(Yl,t,out_img,(255,255,0),100000.,   0,0,2,10,True)
	#show_timepoint(Sl,t,out_img,(255,255,255),100000. ,0,0,3,10,True)

	#show_timepoint(Bur,t,out_img,(0,100,255),100000.,0,0,None,10,True)
	#show_timepoint(Bkr,t,out_img,(80,80,80 ),100000.,0,0,None,10,True)
	show_timepoint(Yr,t,out_img,(150,150,0),100000.,0,0,None,10,True)
	#show_timepoint(Sr,t,out_img,(150,150,150),100000.,0,0,None,10,True)
		
	if SAVE_GRAPHICS:
		imsave(opjD('markers3',str(frame_ctr)+'.png'),out_img)
		frame_ctr += 1

	tprev = t
	iprev = i
	if t-tprev > 1:
		print tprev






import scipy.interpolate
CubicSpline = scipy.interpolate.CubicSpline

def get_cubic_spline(time_points,data):
	D,T = array(data),array(time_points)
	cs = CubicSpline(T,D)
	new_time_points = time_points #np.arange(time_points[0],time_points[-1],1)
	plot(time_points,data,'o')
	plot(T,D,'o', label='smoothed data')
	plot(time_points,cs(time_points),label="S")
	plt.legend(loc='lower left', ncol=2)
	figure(10)
	plot(T,D,'o')
	plot(time_points,data,'x')
	pause(0.1)
	return cs



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




figure('side')

time_points = array(Bul['pts'])[:,2]
Bul['cs_x'] = get_cubic_spline(time_points,array(Bul['pts'])[:,0])
Bul['cs_y'] = get_cubic_spline(time_points,array(Bul['pts'])[:,1])

time_points = array(Bur['pts'])[:,2]
Bur['cs_x'] = get_cubic_spline(time_points,array(Bur['pts'])[:,0])
Bur['cs_y'] = get_cubic_spline(time_points,array(Bur['pts'])[:,1])

time_points = array(Bkl['pts'])[:,2]
Bkl['cs_x'] = get_cubic_spline(time_points,array(Bkl['pts'])[:,0])
Bkl['cs_y'] = get_cubic_spline(time_points,array(Bkl['pts'])[:,1])

time_points = array(Bkr['pts'])[:,2]
Bkr['cs_x'] = get_cubic_spline(time_points,array(Bkr['pts'])[:,0])
Bkr['cs_y'] = get_cubic_spline(time_points,array(Bkr['pts'])[:,1])




figure('top')
t1 = 1493425694.71+5
t2 = 1493425899.676476 - 100
T = np.arange(t1,t2,1/30.)
plot(Bul['cs_x'](T),Bul['cs_y'](T),'o')
plot(Bur['cs_x'](T),Bur['cs_y'](T),'o')
plot(Bkl['cs_x'](T),Bkl['cs_y'](T),'o')
plot(Bkr['cs_x'](T),Bkr['cs_y'](T),'o')


if True:
	CS = {}
	CS['Mr_Blue'] = {}
	CS['Mr_Blue']['left'] = (Bul['cs_x'],Bul['cs_y'])
	CS['Mr_Blue']['right'] =(Bur['cs_x'],Bur['cs_y'])
	CS['Mr_Black'] = {}
	CS['Mr_Black']['left'] = (Bkl['cs_x'],Bkl['cs_y'])
	CS['Mr_Black']['right'] =(Bkr['cs_x'],Bkr['cs_y'])
	save_obj(CS,opjD('trajectories.pkl'))



bcx = Bul['cs_x'](T)
bcy = Bul['cs_y'](T)
brcx = Bur['cs_x'](T)
brcy = Bur['cs_y'](T)

for i in range(len(T)):
	x,y = bcx[i],bcy[i]
	xr,yr = brcx[i],brcy[i]
	cv2.circle(out_img,(int(-M*x)+O,int(M*y)+O),4,(90,100,110),-1)
	cv2.circle(out_img,(int(-M*xr)+O,int(M*yr)+O),4,(90,100,110),-1)




while True:
	k = mci(out_img,delay=100,title='out_img')
	if k == ord('q'):
		break;

