figure(5);clf();plt_square();xysqlim(2.1*107.0/100.0);
rpts_ = []
for k_ in Marker_xy_dic.keys():
	if not is_number(k_):
		if k_[1] == right:
			rpts_.append(Marker_xy_dic[k_])
rpts_ = na(rpts_)
pts_plot(rpts_,'r')

lpts_ = []
for k_ in Marker_xy_dic.keys():
	if not is_number(k_):
		if k_[1] == left:
			lpts_.append(Marker_xy_dic[k_])
lpts_ = na(lpts_)
pts_plot(lpts_,'b')




current_position_ = na((0.0,0.0))
#d_current_position_ = na((0,-0.01))
d_theta_ = 0.01
theta_ = 0.1

for i_ in range(200):
	clf();plt_square();xysqlim(2.1*107.0/100.0);
	current_position_ += d_current_position_
	theta_ += d_theta_
	rpts2_ = rpts_ - current_position_
	rpts2_ = na(rotatePolygon(rpts2_,theta_)) + current_position_ + d_current_position_
	
	pts_plot(lpts2_,'b')
	plot([0,0],[0,0.1],'k')
	print(theta_,current_position_)
	pause(0.0001)



pts = rpts_.copy()

xy_ = na((0.0,0.0))
theta_ = 0
for i_ in range(200):
	if i_ < 100:
		theta_ += 0.5
	else:
		theta_ -= 0.5
	xy_ += na(rotatePoint((0,0),(0,0.01),theta_))
	pts_pov_ = na(rotatePolygon(pts_-xy_,-theta_))
	clf();plt_square();xysqlim(2.1*107.0/100.0);pts_plot(pts_pov_,'b');plot(0,0,'ok');pause(0.001)
	#cf();plt_square();xysqlim(2.1*107.0/100.0);pts_plot(pts_,'b');plot(xy_[0],xy_[1],'ok');pause(0.001)
	print dp(theta_)


d = []
b = []
for a in arange(-45,45):
	b.append(a)
	d.append(1.0+(np.abs(a/45.0)**2)/10.0)
clf();plot(b,d,'o')











n = []
for i in rlen(hmx):
	n.append(angle_clockwise((0,1),(hmx[i]-Aruco_trajectories[left][x][i],hmy[i]-Aruco_trajectories[left][y][i])))
"""	
for i in range(0,len(hmx),5):
	clf();plt_square();xysqlim(3);
	plot(Aruco_trajectories[left][x][i],Aruco_trajectories[left][y][i],'.');pause(0.001)
	print n[i]
"""
figure(6);
for an in range(15,180+15,30):
	ox=[];oy=[]
	clf();plt_square();xysqlim(2*107.0/100.0)
	for i in range(0,len(hmx),5):
		if n[i] >an-15 and n[i]<an+15:
			ox.append(Aruco_trajectories[left][x][i])
			oy.append(Aruco_trajectories[left][y][i])
			plot(ox[-1],oy[-1],'r.');spause()



ox0=ox;oy0=oy






def A():
	D = {}
	B = {1:2,3:4}
	def _get_b(k):
		return B[k]
	D['get'] = _get_b
	return D

C = A()


a = d[LEFT][MIDDLE][RIGHT]



runs = sggo('/home/karlzipser/Desktop/all_aruco_ready/bdd_car_data_Sept2017_aruco_demo/h5py/*')
run_names = {}
for r in runs:
	run_names[fname(r)] = True

other_runs = {}
new_o = []
for p in o:
	if p[0] not in run_names:
		other_runs[p[0]] = True
	else:
		new_o.append(p)

new_q = []
other_runs2 = {}
for r in q:
	if r[0] not in run_names:
		other_runs2[r[0]] = True
	else:
		new_q.append(r)


















try:
	L.close()
	print 'closed L'
except:
	print 'L not open'
filename = '/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py/direct_rewrite_test_14May17_02h49m07s_Mr_Yellow/left_timestamp_metadata_right_ts.h5py'
L=h5r(filename)
figure(1);clf()
plot(L['motor'][:],'r.')#,',')
plot(L['steer'][:],'k.')#,',')
try:
	plot(L['cmd_motor'][:],'b.')#,',')
except:
	'no cmd_motor'
plot(10*L['state'][:],'g.')
#L.close()
















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
	cmd_deltas_mask = 1.0*cmd_deltas_interp
	cmd_deltas_mask[cmd_deltas_mask>3*np.median(original_cmd_deltas)] = 0.0
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
h5py_folder = '/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py'#aruco_Smyth_Fern_experiment/h5py'
runs = sggo(h5py_folder,'*')
for r in runs:
	try:
		P = h5r(opj(r,'position_data.h5py'))
		L = h5r(opj(r,'left_timestamp_metadata_right_ts.h5py'))
		O = h5r(opj(r,'original_timestamp_data.h5py'))
		figure(1);clf();plt_square();xysqlim(4.5)
		state_ = L[state][:]
		if motor in L.keys():
			motor_ = L[motor][:]
		else:
			motor_ = 0*state_+49
		if 'cmd_motor' in L.keys():
			cmd_motor_ = L['cmd_motor'][:]
		else:
			cmd_motor_ = 0*state_+49

		mask,cmd_mask = get_data_mask(state=state_,motor=motor_,cmd_motor=cmd_motor_,cmd_use_states=[3,5,6,7],human_use_states=[1],min_motor=51,min_cmd_motor=0,original_cmd_motor_ts=O['cmd_motor'][ts][:],ts=L[ts][:])
		m = mask + cmd_mask
		m = m[:len(P['ax'][:])]
		plot(m*P['ax'][:],m*P['ay'][:],'k,')
		title(fname(r))
		figure(2);clf()
		plot(L[ts][:],L[state][:]+0.1,'g-')
		plot(L[ts][:],mask,'r-')
		plot(L[ts][:],cmd_mask,'b-')
		
		title(fname(r))
		spause()
		P.close()
		L.close()
		raw_enter()
	except Exception as e:
		print("********** Exception ***********************")
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


