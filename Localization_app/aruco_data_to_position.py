import Parameters_Module
from Parameters_Module import *
from vis2 import *
from Project_Aruco_Markers_Module import Aruco_Trajectory
#from Main import *
exec(identify_file_str)

data_path = Args['SRC']
folder_paths = sggo(data_path,'h5py','*')
#file_path = '/home/karlzipser/Desktop/full_raised/h5py/Mr_Lt_Blue_2017-10-23-12-28-27'

for file_path in folder_paths:
	if len(sggo(file_path,'aruco_position.h5py')) > 0:
		pd2s(opj(file_path,'aruco_position.h5py'),'exists')
		continue
	try:
		spd2s(file_path)
		O = h5r(opj(file_path,'original_timestamp_data.h5py'))
		o = lo(opj(file_path,'aruco_data.pkl'))

		AT= Aruco_Trajectory()

		Traj = build_dic_list_leaves([['left','right','avg'],['xy','hxy','no_data'],['vals','ts','indx']])
		for s in ['left','right']:
			Traj[s]['xy']['indx'] = {}

		percent_timer = Timer(1)
		Ctr = {'left':0,'right':0}
		for i in range(0,min(len(o['left_image_aruco']['vals']),len(o['right_image_aruco']['vals'])),1):
			percent_timer.percent_message(i,len(o['left_image_aruco']['vals']),flush=True)
			for s in ['left','right']:
				try:
					a,b,c,d=AT[step](one_frame_aruco_data,o[s+'_image_aruco']['vals'][i],p,P)
					Traj[s]['xy']['indx'][i] = Ctr[s]; Ctr[s] += 1
					Traj[s]['hxy']['vals'].append([a,b])
					Traj[s]['xy']['vals'].append([c,d])
					Traj[s]['hxy']['ts'].append(o[s+'_image_aruco']['ts'][i])
					Traj[s]['xy']['ts'].append(o[s+'_image_aruco']['ts'][i])
					Traj[s]['no_data']['vals'].append(0)
					Traj[s]['no_data']['ts'].append(o[s+'_image_aruco']['ts'][i])
					#print 'success'
				except KeyboardInterrupt:
					break			
				except:
					Traj[s]['no_data']['vals'].append(1)
					Traj[s]['no_data']['ts'].append(o[s+'_image_aruco']['ts'][i])
					#print 'exception'
					pass
				
		Traj['right']['no_data']['vals'] = np.interp(Traj['left']['no_data']['ts'],Traj['right']['no_data']['ts'],Traj['right']['no_data']['vals'])
		Traj['right']['no_data']['ts'] = Traj['left']['no_data']['ts']
		x=Traj['right']['no_data']['vals']
		x[x>0]=1.0
		mult = Traj['right']['no_data']['vals']*Traj['left']['no_data']['vals']
		count = []
		ctr = 0
		for i in range(len(mult)):
			if mult[i] > 0:
				ctr += 1
			else:
				ctr = 0
			count.append(ctr)
		heading_pause = na(count)
		
		heading_pause[heading_pause<11] = 0.0
		heading_pause[heading_pause>=11] = 1.0

		for d in ['xy','hxy']:
			for s in ['left','right']:
				m = []
				for n in [0,1]:
					v = na(Traj[s][d]['vals'])[:,n]
					m.append(np.interp(Traj['left']['no_data']['ts'],Traj[s][d]['ts'],v))
				Traj[s][d]['interp'] = na(m).transpose()

			for s in ['left','right']:
				m = []
				for n in [0,1]:
					v = na(Traj[s][d]['interp'])[:,n]
					m.append(meo(v,30))
				Traj[s][d]['meo'] = na(m).transpose()
			Traj['avg'][d]['meo'] = (Traj['left'][d]['meo']+Traj['right'][d]['meo'])/2.0


		G = h5w(opj(file_path,'aruco_position.h5py'))
		G.create_dataset('ts',data=o['left_image_aruco']['ts'])
		G.create_dataset('aruco_position_x',data=Traj['avg']['xy']['meo'][:,0])
		G.create_dataset('aruco_position_y',data=Traj['avg']['xy']['meo'][:,1])
		G.create_dataset('aruco_heading_x',data=Traj['avg']['hxy']['meo'][:,0])
		G.create_dataset('aruco_heading_y',data=Traj['avg']['hxy']['meo'][:,1])
		G.create_dataset('heading_pause',data=heading_pause)
		for s in ['left','right']:
			G.create_dataset(s+'_no_data',data=Traj[s]['no_data']['vals'])
			for d in ['xy','hxy']:
				G.create_dataset(s+'_'+d,data=Traj[s][d]['meo'])
		G.close()
	except Exception as e:
		print("********** this Exception ***********************")
		print(e.message, e.args)




	if False:
		timer = Timer(1)
		spause_timer = Timer(0.2)
		timer.trigger()

		for i in range(2000,len(Traj['left']['no_data']['vals']),1):

			if timer.check():
				timer.reset()
				figure(1);clf();plt_square();xysqlim(2.5)
			if True:#Traj[s]['no_data']['vals'][i] == 0:
				"""
				for s in ['left','right']:
					if s == 'left':
						c = 'b'
					else:
						c = 'r'
					xy = Traj[s]['xy']['meo'][i]
					pts_plot(na([xy]),c)
					hxy = Traj[s]['hxy']['meo'][i]
					pts_plot(na([hxy]),'k')
				"""
				xy = Traj['avg']['xy']['meo'][i]
				pts_plot(na([xy]),'g')
				hxy = Traj['avg']['hxy']['meo'][i]
				pts_plot(na([hxy]),'k')

			img = cv2.resize(O[left_image][vals][i][:], (0,0), fx=2.0, fy=2.0)
			mci(img,delay=1)
			if spause_timer:
				spause()
				spause_timer.reset()
			print i


























#EOF


