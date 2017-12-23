from kzpy3.vis2 import *
import kzpy3.Localization_app.classify_arena as classify_arena
import kzpy3.Localization_app.get_data_mask as get_data_mask


def display_trajectory(h5py_path=None,marker_pts=None,results=None):
	r = h5py_path
	pts = marker_pts
	if True:#try:
		P = h5r(opj(r,'aruco_position.h5py'))
		try:
			L = h5r(opj(r,'left_timestamp_metadata_right_ts.h5py'))
		except:
			L = h5r(opj(r,'left_timestamp_metadata.h5py'))
		O = h5r(opj(r,'original_timestamp_data.h5py'))
		figure(1);
		clf();
		plt_square();xysqlim(4.5)
		state_ = L[state][:]
		if motor in L.keys():
			motor_ = L[motor][:]
		else:
			motor_ = 0*state_+49
		if 'cmd_motor' in L.keys():
			cmd_motor_ = L['cmd_motor'][:]
		else:
			cmd_motor_ = 0*state_+49

		#mask,cmd_mask = get_data_mask(state=state_,motor=motor_,cmd_motor=cmd_motor_,cmd_use_states=[3,5,6,7],human_use_states=[1],min_motor=51,min_cmd_motor=0,original_cmd_motor_ts=O['motor'][ts][:],ts=L[ts][:])

		if 'cmd_motor' in O:
			cmd_motor_ts = O['cmd_motor'][ts][:]
		else:
			cmd_motor_ts = L[ts][:]

		if False:
			mask,cmd_mask = get_data_mask.get_data_mask(state=state_,motor=motor_,cmd_motor=cmd_motor_,cmd_use_states=[6],human_use_states=[],min_motor=99,min_cmd_motor=53,original_cmd_motor_ts=cmd_motor_ts,ts=L[ts][:])
		else:
			mask,cmd_mask = get_data_mask.get_data_mask(state=state_,motor=motor_,cmd_motor=cmd_motor_,cmd_use_states=[3,5,6,7],human_use_states=[1],min_motor=53,min_cmd_motor=53,original_cmd_motor_ts=cmd_motor_ts,ts=L[ts][:])

		m = mask + cmd_mask
		m = m[:len(P['aruco_position_x'][:])]
		plot(P['aruco_position_x'][:],P['aruco_position_y'][:],'g,')
		plot((m)*P['aruco_position_x'][:],(m)*P['aruco_position_y'][:],'k,')
		pts_plot(pts)
		minutes = (L[ts][-1]-L[ts][0])/60.0
		title(d2s(fname(r),'   ',dp(minutes,1),'minutes'))
		if results != None:
			plt.xlabel(d2s(results))
		figure(2);clf()
		min_len = min(len(P[ts][:]),len(P['heading_pause'][:]))
		plot(P[ts][:min_len],P['heading_pause'][:min_len]+0.1,'k-')
		plot(L[ts][:],L[state][:]+0.1,'g-')
		plot(L[ts][:],mask,'r-')
		#plot(L[ts][:],P[])
		if 'cmd_motor' in L.keys():
			plot(L[ts][:],cmd_mask,'b-')
		#plot(L[ts][:],P['o_meo'][:len(L[ts][:])])
		title(fname(r))
		figure(3);clf()
		plot(L[ts][:],L[motor][:]+0.1,'g-')
		plot(L[ts][:],L['cmd_motor'][:],'r-')
		figure(4);clf()
		mm = min(len(L[ts][:]),len(P['aruco_position_x'][:]))
		plot(L[ts][:mm],P['aruco_position_x'][:mm],'g-')
		plot(L[ts][:mm],P['aruco_position_y'][:mm],'r-')


		#plot(L[ts][:],P['o_meo'][:len(L[ts][:])])
		title(fname(r))
		spause()
		P.close()
		L.close()
		O.close()
		
	else:#except Exception as e:
		print("********** Exception ***********************")####
		print(e.message, e.args)
		print r
		problem_runs.append(r)	
		try:
			P.close()
		except:
			pass
		try:
			L.close()
		except:
			pass
		try:
			O.close()
		except:
			pass



def get_marker_pts(h5py_folder):
	Marker_xy_dic = False
	pkl_files = sggo(h5py_folder.replace('/h5py',''),'*.pkl')
	print pkl_files
	for p in pkl_files:
		if 'Marker_xy_dic' in p:
			Marker_xy_dic = lo(p)
			break
	assert(Marker_xy_dic != False)
	pts = []
	for k in Marker_xy_dic.keys():
		if not is_number(k):
			pts.append(Marker_xy_dic[k])
	pts = na(pts)
	return pts	


if 'H5PY' in Args:

	problem_runs = []

	try:
		P.close()
	except:
		pass
	try:
		L.close()
	except:
		pass
	try:
		O.close()
	except:
		pass
	#h5py_folder = '/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py'
	#h5py_folder = '/home/karlzipser/Desktop/all_aruco_ready/bdd_car_data_14Sept2017_whole_room/h5py'
	#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_14Sept2017_whole_room/h5py'
	#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_14Sept2017_circle/h5py'
	#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/aruco_post_demo_circle11/h5py'
	#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_12Sept2017_whole_room/h5py'
	#h5py_folder = '/home/karlzipser/Desktop/all_aruco_ready/bdd_car_data_15Sept2017_circle/h5py'
	#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_14Sept2017_circle/h5py'
	#h5py_folder = '/home/karlzipser/Desktop/all_aruco_ready/bdd_car_data_Sept2017_aruco_demo/h5py'
	#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/full_raised/h5py'
	#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_Sept2017_aruco_demo/h5py'

	h5py_folder = Args['H5PY']
	pts = get_marker_pts(h5py_folder)
	runs = sggo(h5py_folder,'*')
	for r in runs:
		print r
		results = classify_arena.classify_arena(lo(opj(r,'aruco_data.pkl'),noisy=False))
		pd2s(fname(r),'\t\t',results)
		display_trajectory(r,pts,results)
		display_trajectory(h5py_path=r,marker_pts=pts,results=results)
		raw_enter()



if False:
	the_problem_runs = ['/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py/direct_rewrite_test_21Apr17_16h50m20s_Mr_Silver',
		 '/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py/direct_rewrite_test_25Apr17_16h09m24s_Mr_Black',
		 '/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py/direct_rewrite_test_25Apr17_16h09m29s_Mr_Orange',
		 '/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py/direct_rewrite_test_30Apr17_22h21m02s_Mr_Yellow']












