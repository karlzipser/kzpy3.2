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
h5py_folder = '/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py'#aruco_Smyth_Fern_experiment/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_ready/bdd_car_data_14Sept2017_whole_room/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_14Sept2017_whole_room/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_14Sept2017_circle/h5py'
runs = sggo(h5py_folder,'*')
for r in runs:
	if True:#try:
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

		#mask,cmd_mask = get_data_mask(state=state_,motor=motor_,cmd_motor=cmd_motor_,cmd_use_states=[3,5,6,7],human_use_states=[1],min_motor=51,min_cmd_motor=0,original_cmd_motor_ts=O['motor'][ts][:],ts=L[ts][:])

		if 'cmd_motor' in O:
			cmd_motor_ts = O['cmd_motor'][ts][:]
		else:
			cmd_motor_ts = L[ts][:]
		mask,cmd_mask = get_data_mask(state=state_,motor=motor_,cmd_motor=cmd_motor_,cmd_use_states=[3,5,6,7],human_use_states=[],min_motor=51,min_cmd_motor=0,original_cmd_motor_ts=cmd_motor_ts,ts=L[ts][:])
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
		L.close()#
		raw_enter()
	else:#except Exception as e:
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



runs = {}
datasets = sggo(opjD('all_aruco_ready','*'))
ctr = 0
for d in datasets:
	the_runs = sggo(d,'h5py','*')
	for r in the_runs:
		if fname(r) in runs:
			ctr += 1
			spd2s(r,'already in runs',ctr)
			#time.sleep(0.5)
		runs[fname(r)] = r









# 12/19
#aruco_data = lo('/home/karlzipser/Desktop/all_aruco_reprocessed/need_to_not_used_reprocessed_for_these/bdd_car_data_Sept2017_aruco_demo/h5py/Mr_Black_2017-09-02-13-42-50/aruco_data.pkl' )
#aruco_data = lo('/home/karlzipser/Desktop/all_aruco_reprocessed/need_to_not_used_reprocessed_for_these/bdd_car_data_Sept2017_aruco_demo_3/h5py/Mr_Yellow_2017-09-13-17-23-12/aruco_data.pkl')
#aruco_data = lo('/home/karlzipser/Desktop/all_aruco_reprocessed/need_to_not_used_reprocessed_for_these/bdd_car_data_Sept2017_aruco_demo_3/h5py/Mr_Purple_2017-09-13-17-46-21/aruco_data.pkl')
aruco_data = lo('/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py/direct_rewrite_test_24Apr17_13h09m31s_Mr_Blue/aruco_data.pkl')


















markers_clockwise_Smyth_Fern_arena = [56,62,55,61,
	134,133,139,138,
	199,200,202,203,
	204,205,208,206,
	174,175,176,177,
	57,58,67,59,
	173,172,171,170,
	5,53,54,60,
	153,152,151,150,
	169,168,167,165,
	207,209,210,211,
	154,155,156,157,
	215,212,213,214,
	227,226,228,225,
	216,217,218,219,
	223,222,221,220,
	66,70,64,65,
	132,137,136,135,
	198,196,197,194,
	140,141,143,142,
	68,69,74,6,
	162,163,164,166,
	229,131,144,145,
	190,188,193,195,
	48,46,49,47,
	161,160,159,158]

p1=[199,200,202,203]
p2=[204,205,208,206]
p3=[174,175,176,177]
p4=[57,58,67,59]
p5=[173,172,171,170]

p6=[227,226,228,225]
p7=[153,152,151,150]
p8=[134,133,139,138]
p9=[216,217,218,219] 

p10=[223,222,221,220]
p11=[169,168,167,165]
p12=[207,209,210,211]
p13=[132,137,136,135]
p14=[161]
p15=[55,61]
p16=[160,159,158]
p17=[182,183,184,201]
p18=[51,50,4,63]
p19=[146,147,148,149]
p20=[52,189,192,191]
markers_clockwise_whole_room = p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12+p13+p14+p15+p16+p17+p18+p19+p20

p1=[199,200,202,203]
p2=[204,205,208,206]
p3=[174,175,176,177]
p4=[57,58,67,59]
p5=[173,172,171,170]
p6=[227,226,228,225]
p7=[153,152,151,150]
p8=[134,133,139,138]
p9=[216,217,218,219] 
p10=[223,222,221,220]
p11=[169,168,167,165]
p12=[207,209,210,211]
markers_clockwise_12circle = p4+p5+p6+p7+p8+p9+p10+p11+p12+p1+p2+p3

p1=[199,200,202,203]	#
p2=[204,205,208,206]	# K
p3=[174,175,176,177]	# J
p4=[57,58,67,59]		# I
p5=[173,172,171,170]	# H
p6=[227,226,228,225]	# G
p7=[153,152,151,150]	# F
p8=[134,133,139,138]	# E
p9=[216,217,218,219]	# D
p10=[223,222,221,220]	# C
p11=[169,168,167,165]	# B
p12=[207,209,210,211]	# A
markers_clockwise_11circle = p4+p5+p6+p7+p8+p9+p10+p11+p12   +    p2+p3

p2=[201,184,183,182]	# +
p3=[174,175,176,177]	# J
p4=[214,213,212,215]	# +
p5=[173,172,171,170]	# H
p6=[135 ,136,137,132]	# +
p7=[153,152,151,150]	# F
p8=[134,133,139,138]	# E
p9=[157,156,155,154]	# +
p10=[223,222,221,220]	# C
p11=[65,64,70,66]		# +
p12=[207,209,210,211]	# A
markers_clockwise_11circle_half_raised = p4+p5+p6+p7+p8+p9+p10+p11+p12   +    p2+p3


p2=[182,183,184,201]	# + door
p3=[178,179,180,181]	# J
p4=[66,70,64,65]	# +
p5=[51,50,4,63]	# H
p6=[154,155,156,157]	# +
p7=[52,189,192,191]	# F
p8=[146,147,148,149]	# E fireplace
p9=[132,137,136,135]	# +
p10=[199,200,202,203]	# C
p11=[215,212,213,214]		# +
p12=[198,196,197,194]	# A windows
markers_clockwise_11circle_full_raised = p4+p5+p6+p7+p8+p9+p10+p11+p12+p2+p3

all_markers = {}
for m in markers_clockwise_Smyth_Fern_arena+markers_clockwise_whole_room+markers_clockwise_12circle+markers_clockwise_11circle+markers_clockwise_11circle_half_raised+markers_clockwise_11circle_full_raised:
	all_markers[m] = True
del(all_markers[190])
del(all_markers[131])




def classify_arena(aruco_data):
	results = []
	for markers_clockwise in [markers_clockwise_Smyth_Fern_arena,markers_clockwise_whole_room,markers_clockwise_12circle,markers_clockwise_11circle,markers_clockwise_11circle_half_raised,markers_clockwise_11circle_full_raised]:

		markers = {}
		for side in ['left','right']:
			for q in aruco_data[side+'_image_aruco'][vals]:
				for m in q['angles_to_center'].keys():
					if m in all_markers:
						markers[m] = True


		false_positives = {}

		ctr1 = 0
		#print 'markers not in markers_clockwise:'
		for m in markers_clockwise:
			if m not in markers:
				#print m
				ctr1 += 1
		#pd2s('len(markers) =',len(markers),'len(markers_clockwise) =',len(markers_clockwise))

		ctr2 = 0
		#print 'markers_clockwise not in markers:'
		for m in markers:
			if m not in markers_clockwise:
				#print m
				ctr2 += 1

		for m in markers:
			if m not in markers_clockwise:
				false_positives[m] = True

		#pd2s('false positives:',false_positives.keys())

		results += [(dp(ctr1/(1.0*len(markers)),1),dp(ctr2/(1.0*len(markers)),1))]
	return results





#
####################################
#


runs = sggo('/home/karlzipser/Desktop/all_aruco_reprocessed/full_raised/h5py','*')
for d in range(1,31):
	for r in runs:
		if d < 10:
			dd = d2n('0',d)
		else:
			dd = str(d)
		if d2n('2017-10-',dd,'-') in fname(r):
			results = classify_arena(lo(opj(r,'aruco_data.pkl'),noisy=False))
			pd2s(d,fname(r),'\t\t',results)


def check_run_dates(folder,month,day_range):
	runs = sggo(folder,'h5py','*')
	for r in runs:
		print r
		success = False
		for d in day_range:
			if d < 10:
				dd = d2n('0',d)
			else:
				dd = str(d)
			#print d2n('2017-',month,'-',dd,'-'),fname(r)
			if d2n('2017-',month,'-',dd,'-') in fname(r):
				success = True
				break
		assert(success)