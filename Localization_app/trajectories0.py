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

if False:
	timer = Timer(30)
	O = h5r('/media/karlzipser/2_TB_Samsung/h5py/Mr_Lt_Blue_2017-10-23-18-09-39/original_timestamp_data.h5py')
	o=lo('/media/karlzipser/2_TB_Samsung/h5py/Mr_Lt_Blue_2017-10-23-18-09-39/aruco_data.pkl' )
	lv=o['left_image_aruco']['vals']
	rv=o['right_image_aruco']['vals']
	figure(1);clf();plt_square();xysqlim(4) 
	AT= Aruco_Trajectory()
	c_prev,d_prev = 0,0
	for i in range(0,len(lv),1):
		if timer.check():
			time.sleep(0.1)
			timer.reset()
			figure(1);clf();plt_square();xysqlim(4)
		try:                                                         
			a,b,c,d=AT[step](one_frame_aruco_data,lv[i],p,P)
			e,f,g,h=AT[step](one_frame_aruco_data,rv[i],p,P)
			if length([c-c_prev,d-d_prev]) > 0.01:
				figure(1)
				plot(c,d,'r.')
				plot(g,h,'b.');
				mi(O[left_image][vals][i][:],2)
				spause()
			c_prev = c
			d_prev = d
		except KeyboardInterrupt:
			break
		except:
			pass





if True:
	O = h5r('/media/karlzipser/2_TB_Samsung/h5py/Mr_Lt_Blue_2017-10-23-18-09-39/original_timestamp_data.h5py')
	o=lo('/media/karlzipser/2_TB_Samsung/h5py/Mr_Lt_Blue_2017-10-23-18-09-39/aruco_data.pkl' )
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
	for i in range(0,len(lv),1):
		percent_timer.percent_message(i,len(lv),flush=True)
		try:                                                         
			a,b,c,d=AT[step](one_frame_aruco_data,lv[i],p,P)
			e,f,g,h=AT[step](one_frame_aruco_data,rv[i],p,P)
			traj['left']['hxy'].append([a,b])
			traj['right']['hxy'].append([e,f])
			traj['left']['xy'].append([c,d])
			traj['right']['xy'].append([g,h])
		except KeyboardInterrupt:
			break
		except:
			print('fail')
			a,b,c,d,e,f,g,h=0,0,0,0,0,0,0,0
			traj['left']['hxy'].append([a,b])
			traj['right']['hxy'].append([e,f])
			traj['left']['xy'].append([c,d])
			traj['right']['xy'].append([g,h])			
	for s in ['left','right']:
		for t in ['hxy','xy']:
			traj[s][t] = na(traj[s][t])
	assert(len(traj['left']['xy'])==len(lv))
if True:
	figure(1);clf()
	traj['left']['x_meo'] = meo(traj['left']['xy'][:,0],30)
	traj['right']['x_meo'] = meo(traj['right']['xy'][:,0],30)
	traj['left']['y_meo'] = meo(traj['left']['xy'][:,1],30)
	traj['right']['y_meo'] = meo(traj['right']['xy'][:,1],30)
	plot(traj['left']['x_meo'],'r')
	plot(traj['right']['x_meo'],'b')
	plot(traj['left']['xy'][:,0],'b.'),
	plot(traj['right']['xy'][:,0],'r.')
	q=1
	start = 31000#14562#4000#

	
	for i in range(start,len(traj['left']['x_meo']),5):
		base_graph[IMG] *= 0
		#figure(2)#;clf();plt_square();xysqlim(2.5)
		#plot(traj['left']['xy'][i,0],traj['left']['xy'][i,1],'b.')
		base_graph[PTS_PLOT](x_=na([traj['left']['x_meo'][i-90:i]]),y_=na([traj['left']['y_meo'][i-90:i]]), color_=(255,0,0))
		base_graph[PTS_PLOT](x_=na([traj['right']['x_meo'][i-90:i]]),y_=na([traj['right']['y_meo'][i-90:i]]), color_=(0,255,0))
		mci(base_graph[IMG],title='trajectory',scale=2.0)
		#plt.title(i)
		#plot(traj['left']['x_meo'][i:i+30*q],traj['left']['y_meo'][i:i+30*q],'b.')
		#plot(traj['right']['x_meo'][i:i+30*q],traj['right']['y_meo'][i:i+30*q],'r.')
		mci(O[left_image][vals][i][:],title='left',scale=4.0)
		#plt.title(i)
		#spause()






#EOF