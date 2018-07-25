from kzpy3.Localization_app.Project_Aruco_Markers_Module import *

P[past_to_present_proportion] = 0.0

from kzpy3.Image_app.Image_Module import Img
base_graph = Img(
	xmin=-2.5,
	xmax=2.5,
	ymin=-2.5,
	ymax=2.5,
	xsize=300,
	ysize=300)






























if True:
	if True:
		O = h5r('/media/karlzipser/2_TB_Samsung/h5py/Mr_Lt_Blue_2017-10-23-18-09-39/original_timestamp_data.h5py')
		o=lo('/media/karlzipser/2_TB_Samsung/h5py/Mr_Lt_Blue_2017-10-23-18-09-39/aruco_data.pkl' )
	if False:
		O = h5r('/media/karlzipser/2_TB_Samsung/h5py/Mr_Yellow_2017-10-16-11-14-16/original_timestamp_data.h5py')
		o=lo('/media/karlzipser/2_TB_Samsung/h5py/Mr_Yellow_2017-10-16-11-14-16/aruco_data.pkl')
	lv=o['left_image_aruco']['vals']
	rv=o['right_image_aruco']['vals']
	AT= Aruco_Trajectory()
	traj = {}
	traj['left'] = {}
	traj['right'] = {}
	traj['left']['xy'] = []
	traj['right']['xy'] = []
	traj['left']['hxy'] = []
	traj['right']['hxy'] = []

if True:
	percent_timer = Timer(1)
	a_prev,b_prev,c_prev,d_prev,e_prev,f_prev,g_prev,h_prev = 0,0,0,0,0,0,0,0
	for i in range(0,len(lv),1):
		percent_timer.percent_message(i,len(lv),flush=True)
		try:                                                         
			a,b,c,d=AT[step](one_frame_aruco_data,lv[i],p,P)
			e,f,g,h=AT[step](one_frame_aruco_data,rv[i],p,P)
			traj['left']['hxy'].append([a,b])
			traj['right']['hxy'].append([e,f])
			traj['left']['xy'].append([c,d])
			traj['right']['xy'].append([g,h])
			a_prev,b_prev,c_prev,d_prev,e_prev,f_prev,g_prev,h_prev = a,b,c,d,e,f,g,h
		except KeyboardInterrupt:
			break
		except:
			print('fail')
			a,b,c,d,e,f,g,h = a_prev,b_prev,c_prev,d_prev,e_prev,f_prev,g_prev,h_prev
			traj['left']['hxy'].append([a,b])
			traj['right']['hxy'].append([e,f])
			traj['left']['xy'].append([c,d])
			traj['right']['xy'].append([g,h])			
	for s in ['left','right']:
		for t in ['hxy','xy']:
			traj[s][t] = na(traj[s][t])
	assert(len(traj['left']['xy'])==len(lv))

n = 30
if True:
	traj['left']['x_meo'] = meo(traj['left']['xy'][:,0],n)
	traj['right']['x_meo'] = meo(traj['right']['xy'][:,0],n)
	traj['left']['y_meo'] = meo(traj['left']['xy'][:,1],n)
	traj['right']['y_meo'] = meo(traj['right']['xy'][:,1],n)
	traj['left']['hx_meo'] = meo(traj['left']['hxy'][:,0],n)
	traj['right']['hx_meo'] = meo(traj['right']['hxy'][:,0],n)
	traj['left']['hy_meo'] = meo(traj['left']['hxy'][:,1],n)
	traj['right']['hy_meo'] = meo(traj['right']['hxy'][:,1],n)
	traj['left']['x_meo_hx_meo'] = traj['left']['hx_meo']
	traj['left']['y_meo_hy_meo'] = traj['left']['hy_meo']
	traj['right']['x_meo_hx_meo'] = traj['right']['hx_meo']
	traj['right']['y_meo_hy_meo'] = traj['right']['hy_meo']


M=lo('/home/karlzipser/Desktop/aruco_raised11_5Nov2017_Marker_xy_dic.pkl')
xs = []
ys = []
for k in M.keys():
	if not is_number(k):
		xy = M[k]
		xs.append(xy[0])
		ys.append(xy[1])
if True:
	q=1
	start = 21000#14562#4000#

	plot_data = [{'X_REF':['left','x_meo'],'Y_REF':['left','y_meo'],'BACK_TIME':-30,'COLOR':(255,0,0)}]
	plot_data += [{'X_REF':['right','x_meo'],'Y_REF':['right','y_meo'],'BACK_TIME':-30,'COLOR':(0,255,0)}]
	plot_data += [{'X_REF':['right','x_meo_hx_meo'],'Y_REF':['right','y_meo_hy_meo'],'BACK_TIME':-1,'COLOR':(255,255,0)}]
	plot_data += [{'X_REF':['left','x_meo_hx_meo'],'Y_REF':['left','y_meo_hy_meo'],'BACK_TIME':-1,'COLOR':(255,255,0)}]
	
	for i in range(start,len(traj['left']['x_meo']),1):
		base_graph[IMG] *= 0
		base_graph[PTS_PLOT](x_=na(xs),y_=na(ys), color_=(255,255,255))
		for p in plot_data:
			s = p['X_REF'][0]
			x = p['X_REF'][1]
			y = p['Y_REF'][1]
			#print s,x,y
			back_time = p['BACK_TIME']
			color = p['COLOR']
			base_graph[PTS_PLOT](x_=na([traj[s][x][i+back_time:i]]),y_=na([traj[s][y][i+back_time:i]]), color_=color)

		mci(base_graph[IMG],title='trajectory',scale=2.0)
		#plt.title(i)
		#plot(traj['left']['x_meo'][i:i+30*q],traj['left']['y_meo'][i:i+30*q],'b.')
		#plot(traj['right']['x_meo'][i:i+30*q],traj['right']['y_meo'][i:i+30*q],'r.')
		img = O[left_image][vals][i][:].copy()
		img[:(50),:,:] = 128
		mci(img,title='left',scale=4.0)
		#plt.title(i)
		#spause()





#EOF