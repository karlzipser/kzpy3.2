
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
#h5py_folder = '/media/karlzipser/2_TB_Samsung_n3/aruco_Smyth_Fern_experiment/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_ready/bdd_car_data_14Sept2017_whole_room/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_14Sept2017_whole_room/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_14Sept2017_circle/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/aruco_post_demo_circle11/h5py'
h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_12Sept2017_whole_room/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_ready/bdd_car_data_15Sept2017_circle/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_14Sept2017_circle/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_ready/bdd_car_data_Sept2017_aruco_demo/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/full_raised/h5py'
#h5py_folder = '/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_Sept2017_aruco_demo/h5py'


Marker_xy_dic = False
pkl_files = sggo(h5py_folder.replace('/h5py',''),'*.pkl')
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

figure(1);
clf();
runs = sggo(h5py_folder,'*')
for r in runs:
	print r
	results = classify_arena(lo(opj(r,'aruco_data.pkl'),noisy=False))
	pd2s(fname(r),'\t\t',results)
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
			mask,cmd_mask = get_data_mask(state=state_,motor=motor_,cmd_motor=cmd_motor_,cmd_use_states=[6],human_use_states=[],min_motor=99,min_cmd_motor=53,original_cmd_motor_ts=cmd_motor_ts,ts=L[ts][:])
		else:
			mask,cmd_mask = get_data_mask(state=state_,motor=motor_,cmd_motor=cmd_motor_,cmd_use_states=[3,5,6,7],human_use_states=[1],min_motor=53,min_cmd_motor=53,original_cmd_motor_ts=cmd_motor_ts,ts=L[ts][:])


		m = mask + cmd_mask
		m = m[:len(P['aruco_position_x'][:])]
		plot(P['aruco_position_x'][:],P['aruco_position_y'][:],'g,')
		plot((m)*P['aruco_position_x'][:],(m)*P['aruco_position_y'][:],'k,')
		pts_plot(pts)
		minutes = (L[ts][-1]-L[ts][0])/60.0
		title(d2s(fname(r),'   ',dp(minutes,1),'minutes'))
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












