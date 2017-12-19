

def get_data_mask(state=None,motor=None,cmd_motor=None,human_use_states=[],cmd_use_states=[],min_motor=None,min_cmd_motor=None,original_cmd_motor_ts=None,ts=None):
	mask = 0 * state
	cmd_mask = 0 * state
	n = len(state)
	
	original_cmd_deltas = 0*original_cmd_motor_ts
	for i in range(1,len(original_cmd_deltas)-1):
		a = original_cmd_motor_ts[i]
		b = original_cmd_motor_ts[i-1]
		c = original_cmd_motor_ts[i+1]
		original_cmd_deltas[i] = (a-b+c-a)/2.0
	cmd_deltas_interp = np.interp(ts,original_cmd_motor_ts,original_cmd_deltas)
	#figure(10);plot(cmd_deltas_interp)
	cmd_deltas_mask = 1.0*cmd_deltas_interp
	cmd_deltas_mask[cmd_deltas_mask>0.25] = 0.0 #100*np.median(original_cmd_deltas)] = 0.0
	cmd_deltas_mask[cmd_deltas_mask>0] = 1.0

	for i in range(1,n-1):
		if state[i] != state[i-1]:
			if state[i] != state[i+1]:
				state[i] = state[i-1]
	for i in range(n):
		if state[i] in human_use_states:
			mask[i] = 1
		elif state[i] in cmd_use_states:
			cmd_mask[i] = cmd_deltas_mask[i]
		if state[i] in human_use_states:
			if min_motor != None:
				if motor[i] < min_motor:
					mask[i] = 0
		elif state[i] in cmd_use_states:
			if min_cmd_motor != None:
				if cmd_motor[i] < min_cmd_motor:
					cmd_mask[i] = 0
	return mask,cmd_mask



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
#h5py_folder = '/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py'#aruco_Smyth_Fern_experiment/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_ready/bdd_car_data_14Sept2017_whole_room/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_14Sept2017_whole_room/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_14Sept2017_circle/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/aruco_post_demo_circle11/h5py'
h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_12Sept2017_whole_room/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_ready/bdd_car_data_15Sept2017_circle/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_15Sept2017_circle/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_ready/bdd_car_data_Sept2017_aruco_demo/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/aruco_post_demo_circle11/h5py'

figure(1);
clf();
runs = sggo(h5py_folder,'*')
for r in runs:
	try:
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
		mask,cmd_mask = get_data_mask(state=state_,motor=motor_,cmd_motor=cmd_motor_,cmd_use_states=[6],human_use_states=[],min_motor=99,min_cmd_motor=53,original_cmd_motor_ts=cmd_motor_ts,ts=L[ts][:])
		m = mask + cmd_mask
		m = m[:len(P['aruco_heading_x'][:])]
		plot((m)*P['aruco_heading_x'][:],(m)*P['aruco_heading_y'][:],'k,')
		title(fname(r))
		figure(2);clf()
		plot(L[ts][:],L[state][:]+0.1,'g-')
		plot(L[ts][:],mask,'r-')
		plot(L[ts][:],cmd_mask,'b-')
		#plot(L[ts][:],P['o_meo'][:len(L[ts][:])])
		title(fname(r))
		figure(3);clf()
		plot(L[ts][:],L[motor][:]+0.1,'g-')
		plot(L[ts][:],L['cmd_motor'][:],'r-')

		#plot(L[ts][:],P['o_meo'][:len(L[ts][:])])
		title(fname(r))
		spause()
		P.close()
		L.close()#
		raw_enter()
	except Exception as e:
		print("********** Exception ***********************")####
		print(e.message, e.args)
		print r
		problem_runs.append(r)	




the_problem_runs = ['/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py/direct_rewrite_test_21Apr17_16h50m20s_Mr_Silver',
	 '/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py/direct_rewrite_test_25Apr17_16h09m24s_Mr_Black',
	 '/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py/direct_rewrite_test_25Apr17_16h09m29s_Mr_Orange',
	 '/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py/direct_rewrite_test_30Apr17_22h21m02s_Mr_Yellow']











L.close()
O.close()
L = h5r('/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py/caffe2_z2_color_direct_local_31Dec12_16h01m08s_Mr_Blue/left_timestamp_metadata_right_ts.h5py')
O = h5r('/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py/caffe2_z2_color_direct_local_31Dec12_16h01m08s_Mr_Blue/original_timestamp_data.h5py')

if False:
	original_cmd_deltas = 0*O['cmd_motor'][ts][:]
	for i in range(1,len(original_cmd_deltas)):
		original_cmd_deltas[i] = O['cmd_motor'][ts][i] - O['cmd_motor'][ts][i-1]
else:
	original_cmd_deltas = 0*O['cmd_motor'][ts][:]
	for i in range(1,len(original_cmd_deltas)-1):
		a = O['cmd_motor'][ts][i]
		b = O['cmd_motor'][ts][i-1]
		c = O['cmd_motor'][ts][i+1]
		original_cmd_deltas[i] = (a-b+c-a)/2.0



cmd_deltas_interp = np.interp(L[ts][:],O['cmd_motor'][ts],original_cmd_deltas)

cmd_deltas_mask = 1.0*cmd_deltas_interp
cmd_deltas_mask[cmd_deltas_mask>3*np.median(original_cmd_deltas)] = 0.0
cmd_deltas_mask[cmd_deltas_mask>0] = 1.0

plot(cmd_deltas_interp)
plot(cmd_deltas_mask)


