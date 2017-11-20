from kzpy3.Grapher_app.Graph_Image_Module import *
from kzpy3.Localization_app.aruco_whole_room_markers import *


def get_car_position_heading_validity(h5py_data_folder,graphics=False):

	L = h5r(opj(h5py_data_folder,'left_timestamp_metadata.h5py'))
	O = h5r(opj(h5py_data_folder,'original_timestamp_data.h5py'))

	left_images = O[left_image][vals][:].copy()
	left_images = left_images.mean(axis=3)
	right_images = O[right_image][vals][:].copy()
	right_images = right_images.mean(axis=3)

	if False:
		for i in range(2280,shape(left_images)[0]):
			mi(np.abs(left_images[i]-left_images[i-1]),2)
			pause(0.01)

	CA()

	pts = []
	if graphics: figure('arena');clf();plt_square();#xylim(-0.1,0.6,-0.1,0.6)#xysqlim(1.)
	for k in Marker_xy_dic:
		if graphics: pts_plot(na([Marker_xy_dic[k]]))
		if is_number(k):
			txt = str(k)
			if graphics: plt.annotate(txt,Marker_xy_dic[k])
			pts.append(Marker_xy_dic[k])
			left_pt = Marker_xy_dic[(k,LEFT2)]
			right_pt = Marker_xy_dic[(k,RIGHT2)]
			if graphics: plot([left_pt[0],right_pt[0]],[left_pt[1],right_pt[1]],'b')
			left_pt = Marker_xy_dic[(k,LEFT)]
			right_pt = Marker_xy_dic[(k,RIGHT)]
			pts.append(left_pt)
			pts.append(right_pt)
			if graphics: plot([left_pt[0],right_pt[0]],[left_pt[1],right_pt[1]],'g')
		elif graphics:
			txt = str(k[1])
			if '2' not in txt:
				plt.annotate(txt,Marker_xy_dic[k])

	pts = np.array(pts)


 
	n = [0]
	for i in range(1,shape(left_images)[0]):
		if i < len(right_images):
			ml = np.abs(left_images[i]-left_images[i-1]).mean()
			mr = np.abs(right_images[i]-right_images[i-1]).mean()
			n.append((ml+mr)/2.0)
		else:
			ml = np.abs(left_images[i]-left_images[i-1]).mean()
			n.append(ml)			


	t = O[left_image][ts][:]
	if graphics: figure('motion calculation');plot(t-t[0],n)


	hp = L[heading_pause][:]
	hp[hp<1]=0
	hp2 = 1-hp
	hp2[L[state][:]!=6] = 0

	mo_mask = L[motor][:]
	mo_mask[mo_mask<53]=0
	mo_mask[mo_mask>=53]=1.0
	o = mo_mask*hp2*n


	p=[]
	for q in o:
		if q > 0:
			p.append(q)
	if graphics: figure('motion calculation histogram');hist(p)

	o[o>(np.mean(p)+1.5*np.std(p))] = 0
	o[o<(np.mean(p)-1.5*np.std(p))] = 0
	
	if graphics: figure('motion calculation');plot(t-t[0],o)
	o_meo = na(meo(o,45))
	if graphics: plot(t-t[0],o_meo)
	#left_images=O[left_image][vals][:]
	#ctr=0
	pause_flag = False
	#dot_ctr = Timer(0.01)
	ax = na(meo(na(L[aruco_position_x][:]),45))
	ay = na(meo(na(L[aruco_position_y][:]),45))
	hx = na(meo(na(L[aruco_heading_x][:]),45))
	hy = na(meo(na(L[aruco_heading_y][:]),45))

	if graphics:
		x_min = -4.0#-(6.03/2.0)#-6.03+hw
		x_max = 4.0#(6.03/2.0)#hw
		y_min = -4.0#-(6.03/2.0)#-hw#
		y_max = 4.0#6.03/2.0#hw#
		time_counter = Timer(1/3.0)
		spause()
		raw_enter()
		cv2.destroyAllWindows()
		Gi = Graph_Image(xmin,x_min,ymin,y_min,xmax,x_max,ymax,y_max,xsize,350,ysize,350)
		for i in range(len(left_images)):
			time_counter.message(d2s(dp(t[i]-t[0])),'white')
			j=i+20
			if o_meo[i] >1:
				mci(O[left_image][vals][i],scale=4,title='left_image')#;spause();
				Gi[img]*=0
				Gi[ptsplot](x,pts[:,0],y,pts[:,1],color,(0,0,255))
				Gi[ptsplot](x,na([ax[j]]),y,na([ay[j]]),color,(255,255,255))
				Gi[ptsplot](x,na([hx[j]+ax[j]]),y,na([hy[j]+ay[j]]),color,(255,0,0))
				mci(Gi[img],scale=2,title='map');
				pause_flag = False
			else:
				if not pause_flag:
					mci(128+0*Gi[img],scale=2,title='map');
					pause(0.5)
					pause_flag = True

	return ax,ay,hx,hy,o_meo


"""
h5py_data_folder = '/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo/h5py/Mr_Blue_2017-09-04-14-49-54'
ax,ay,hx,hy,o_meo = get_car_position_heading_validity(h5py_data_folder,graphics=False)
"""






# 25 Sept. 2017
from kzpy3.Localization_app.Project_Aruco_Markers_Module import * 
from kzpy3.Localization_app.aruco_whole_room_markers_11circle_no_pillar import *
import kzpy3.data_analysis.Angle_Dict_Creator as Angle_Dict_Creator

dont_know_why = True
if dont_know_why:
	P = {}
	P[VERBOSE] = True
	P[GRAPHICS] = False
	P[ROS_LIVE] = True
	P[past_to_present_proportion] = 0.99 # 0.5
	P[MARKERS_TO_IGNORE] = [190] # often has False positives
	P[DEGREE_STEP_FOR_ROTATION_FIT] = 5#15  # 10 to 30 range, bigger is faster
	P[ANGLE_DIST_PARAM] = 0.3

if False:
	D = bagfile_to_dic(BAG_PATH='/media/karlzipser/rosbags/processed_23Sep17_17h48m38s/Mr_Purple_2017-09-23-17-10-53/bair_car_2017-09-23-17-18-23_12.bag' )
	so(D,opjD('one_bag_dic'))
if True:
	D = lo(opjD('one_bag_dic'))

n = len(D[left_image][vals])

graphics = False

if graphics: CA();figure(1);plt_square();xysqlim(3)

timer = Timer(1)

mmm = {}
#mmm_lens = []
for h in range(1):
	for i in range(n):
		try:
			mm = {}
			angles_to_center, angles_surfaces, distances_marker, markers = Angle_Dict_Creator.get_angles_and_distance(D[left_image][vals][i],borderColor=(h*20,255-h*20,0))#None)
			Q = {'angles_to_center':angles_to_center,'angles_surfaces':angles_surfaces,'distances_marker':distances_marker}
			d = Camera_View_Field(aruco_data,Q,'p',P)
			if graphics: clf(); plt_square(); xysqlim(3);pts_plot(d['pts']);spause();mci(D[left_image][vals][i],delay=1)
			for m in d['markers'].keys():
				mm[d2n(m,'_left')] = d['markers'][m]['left']
				mm[d2n(m,'_right')] = d['markers'][m]['right']
			if len(mm) > 0:
				mmm[i] = mm
				#mmm_lens.append(len(mm))
		except Exception as e:
			print("********** Exception 123 ***********************")
			print(e.message, e.args)
		timer.message(d2s(i,int(100*i/(1.0*n)),'%'),color='white')



print('making mmm_overlap_dic')
mmm_overlap_dic = {}
for i in mmm.keys():
	for j in mmm.keys():
		if i != j:
			if len(set(mmm[i].keys()) & set(mmm[j].keys())) > 0:
				if i not in mmm_overlap_dic:
					mmm_overlap_dic[i] = []
				mmm_overlap_dic[i].append(j)
	#print len(mmm_overlap_dic[i])

max_num_markers_index = -1
max_num_markers_val = 0
for i in mmm.keys():
	if len(mmm[i]) > max_num_markers_val:
		max_num_markers_val = len(mmm[i])
		max_num_markers_index = i



www = {}


timer_total = Timer(0)
timer = Timer(0.1)
visited_dic = {}
j = max_num_markers_index #np.random.choice(mmm.keys()) #   max_overlap_index
for marker_id in mmm[j].keys():
	if marker_id not in www:
		www[marker_id] = {}
	www[marker_id][j] = mmm[j][marker_id]
graphics = False
for i in range(100000):
	if graphics: mci(D[left_image][vals][j],delay=500);clf(); plt_square(); xysqlim(3);pts_plot(na(mmm[j].values()));plt.title(len(mmm[j].values()));spause();raw_enter()
	if len(visited_dic) == len(mmm_overlap_dic):
		break
	timer.message(d2s('\t',int(100*len(visited_dic)/(1.0*len(mmm))),'%'),color='white')
	if j not in visited_dic:
		visited_dic[j] = 1
	else:
		visited_dic[j] += 1
	j = np.random.choice(mmm_overlap_dic[j])
	j_keys = sorted(mmm[j].keys())
	stationary = []
	moving = []
	for marker_id in j_keys:
		if marker_id in www.keys():
			stationary.append(list(na(www[marker_id].values()).mean(axis=0))+[0.0])
			moving.append(list(mmm[j][marker_id])+[0.0])
	print stationary
	print moving
	raw_enter()




pd2s('Done in ',dp(timer_total.time()),'seconds')
CA();
hist(visited_dic.values(),bins=500)











#timer.message(d2s('\t',int(100*i/(1.0*len(mmm))),'%'),color='white')


"""
print('finding max_overlap_index')
mmm_lens_sorted_indicies = sorted(range(len(mmm_lens)), key=lambda k: mmm_lens[k])
mmm_lens_sorted_indicies.reverse()
mmm_overlap = {}
max_overlap_val = 0
max_overlap_index = None
ctr = 0
for i in mmm_lens_sorted_indicies:#rlen(mmm):
	timer.message(d2s('\t',int(100*ctr/(1.0*len(mmm))),'%'),color='white')
	for j in mmm_lens_sorted_indicies:#rlen(mmm):
		if j not in mmm_overlap.keys():
			if i != j:
				if i not in mmm_overlap:
					mmm_overlap[i] = (-1,0)
				o = len(set(mmm[i].keys()) & set(mmm[j].keys()))
				if o > mmm_overlap[i][1]:
					mmm_overlap[i] = (j,o)
					if o > max_overlap_val:
						max_overlap_val = o
						max_overlap_index = i
	if mmm_overlap[i] == (-1,0):
		del mmm_overlap[i]
	ctr += 1
pd2s('Done in ',dp(timer_total.time()),'seconds')
"""





True




isdir = os.path.isdir
top = '/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo'
D = {}
assert(isdir(top))

def folder_to_dic(D,top):
	try:
		D[fname(top)] = {}
		items = sggo(top,'*')

		for i in items:
			if isdir(i):
				
				D[fname(top)][fname(i)] = {}
				D[fname(top)][fname(i)] = folder_to_dic(D[fname(top)][fname(i)],i)
			else:
				D[fname(top)][fname(i)] = dp(os.path.getsize(i)/(10.0**6))
	except Exception as e:
		print("**********folder_to_dic Exception ***********************")
		print(e.message, e.args)
	return D[fname(top)]


E = folder_to_dic(D,top)


def ls_dic(D,tabs=0):
	tabstr = ''
	for i in range(tabs):
		tabstr += '\t'
	for k in D.keys():
		if type(D[k]) != dict:
			pd2s(tabstr,k,':',D[k])
		else:
			pd2s(tabstr,k,':')
			ls_dic(D[k],tabs=tabs+1)
				





set(raise_aruco_1).intersection(set(bdd_car_data_Sept2017_aruco_demo))



top = '/media/karlzipser/2_TB_Samsung/full_raised'#'/home/karlzipser/Desktop/raise_aruco_1'#'/home/karlzipser/Desktop/sorting_data'#'/media/karlzipser/2_TB_Samsung/sorting_data' #  
D={};E=folder_to_dic(D,top)
runs = []
#for i in D.keys():
for j in D.keys():
	if 'h5py' in D[j]:
		runs += D[j]['h5py'].keys()
runs_on_external = runs
#runs_on_computer = runs

len(set(runs_on_external).intersection(set(runs_on_computer)))






# 20 Nov. 2017

O = h5r('/home/karlzipser/Desktop/direct_local_arena_16_17_Sept_with_aruco/direct_local_16Sep17_14h35m25s_Mr_Lt_Blue/original_timestamp_data.h5py')
l = len(O['left_image']['vals'][:])
timer = Timer()
for i in range(1000):
	img = O['left_image']['vals'][np.random.randint(l)]
print timer.time() # = 0.295176029205


timer = Timer()
for i in range(1000):
	img = cv2.flip(O['left_image']['vals'][1500],1)
print timer.time() # = 0.260668992996




folder = '/home/karlzipser/Desktop/bdd_car_data_14Sept2017_whole_room'
Aruco_Steering_Trajectories = sggo(folder,'Aruco_Steering_Trajectories/*.pkl')

for a in Aruco_Steering_Trajectories:
	run_name = a.split('/')[-1].split('.')[0]
	unix_str = d2s('mv',opj('/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo/h5py',run_name),opj(folder,'h5py'))
	print unix_str
	unix(unix_str,False)



# 20 Nov. 2017

folder = '/home/karlzipser/Desktop/full_raised'
observer_folder = '/home/karlzipser/Desktop/full_raised_observer'
runs = sggo(folder,'h5py/*')

for a in runs:
	run_name = fname(a)
	F = h5r(opj(a,'left_timestamp_metadata_right_ts.h5py'))
	print run_name,'state' in F.keys()
	if 'state' in F.keys():
		observer = False
	else:
		observer = True
	F.close()
	if observer:
		unix_str = d2s('mv',a,opj(observer_folder,'h5py'))
		print unix_str
		unix(unix_str,False)










#EOF



