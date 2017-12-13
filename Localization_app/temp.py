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





def get_data_mask(state=None,motor=None,cmd_motor=None,human_use_states=[],cmd_use_states=[],min_motor=None,min_cmd_motor=None):
	mask = 0 * state
	cmd_mask = 0 * state
	n = len(state)
	for i in range(n):
		if state[i] in human_use_states:
			mask[i] = 1
		elif state[i] in cmd_use_states:
			cmd_mask[i] = 1
		if state[i] in human_use_states:
			if min_motor != None:
				if motor[i] < min_motor:
					mask[i] = 0
		elif state[i] in cmd_use_states:
			if min_cmd_motor != None:
				if cmd_motor[i] < min_cmd_motor:
					cmd_mask[i] = 0
	return mask,cmd_mask


mask,cmd_mask = get_data_mask(state=L[state][:],motor=L[motor][:],cmd_motor=L['cmd_motor'][:],cmd_use_states=[3,5,6,7],human_use_states=[1],min_motor=53,min_cmd_motor=53)
t = L[ts][:]
figure(1);clf()
plot(t,mask*L['motor'][:],'r.')#,',')
plot(t,mask*L['steer'][:],'k.')#,',')
try:
	plot(t,cmd_mask*L['cmd_steer'][:],'c.')#,',')
	plot(t,cmd_mask*L['cmd_motor'][:],'b.')#,',')
except:
	'no cmd_motor'
#plot(10*L['state'][:],'g.')



P = h5r('/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py/direct_rewrite_test_14May17_02h49m07s_Mr_Yellow/aruco_position.h5py')




try:
	P.close()
except:
	pass
try:
	L.close()
except:
	pass
h5py_folder = '/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py'#aruco_Smyth_Fern_experiment/h5py'
runs = sggo(h5py_folder,'*')
for r in runs:
	P = h5r(opj(r,'position_data.h5py'))
	L = h5r(opj(r,'left_timestamp_metadata_right_ts.h5py'))
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

	mask,cmd_mask = get_data_mask(state=state_,motor=motor_,cmd_motor=cmd_motor_,cmd_use_states=[3,5,6,7],human_use_states=[1],min_motor=53,min_cmd_motor=53)
	m = mask + cmd_mask
	m = m[:len(P['ax'][:])]
	plot(m*P['ax'][:],m*P['ay'][:],'k,')
	title(fname(r))
	P.close()
	L.close()
	raw_enter()



