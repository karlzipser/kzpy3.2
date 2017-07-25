
from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg10'])
from vis2 import *
from misc.progress import ProgressBar



doc_string = """
Interactive data viewer and labeler for model car project.
 

Change path with SP(), i.e., function_set_paths()

e.g., in ipython type:

from kzpy3.teg7.interactive import *

or from command line type:

python kzpy3/teg7/interactive.py

Then type:

VR()

This will visualize run data.

Type:

AR(600,610)

This will animate 10s of data. Note, frames that are not considered data are in grayscale.

Type:

LR()

to list runs. The first number is simply a count (starting with 0), the second number
is the number of bag files in the run. A bag file is 1GB of raw data (much less here)
and take up about 30s, although this varies with image complexity.

To choose a new run (say, run 53), type:

SR(53)
VR()

Note that the prompt on the command line lists the current run. Note that run 0 is selected by default.

Now try:

AR(900,920)

This will show going from non-data to data.

Note, sometimes there is a gap in the frames, as in this example.
The program will report this and pause during this time.
Using the TX1 dev. board cleans this up dramatically.


These runs need to be processed correctly:
22[18] direct_rewrite_test_24Apr17_13h09m31s_Mr_Blue  22	X:True 
25[24] direct_rewrite_test_24Apr17_13h31m59s_Mr_Black  25	X:True 
30[60] direct_rewrite_test_24Apr17_14h39m17s_Mr_Orange  30	X:True 


"""


Names = ['name','dic','argument_dictionary','translation_dic','accepted_states','bair_car_data_path']
for l in Names:
	exec(d2n(l,'=',"'",l,"'"))
Values = {}
V = Values

V[translation_dic] = {'src':bair_car_data_path}
if __name__ == "__main__" and '__file__' in vars():
    V[argument_dictionary] = args_to_dic({'pargs':sys.argv[1:]})
else:
    print('Running this within interactive python.')
    V[argument_dictionary] = args_to_dic({
    	'pargs':"-src /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR"})
V[argument_dictionary] = translate_args(
    {argument_dictionary:V[argument_dictionary],
    translation_dic:V[translation_dic]})
if len(V[argument_dictionary]) == 0:
	pd2s(doc_string)
	nice_print_dic({dic:V[translation_dic],name:'arguments'})
	exit()


nice_print_dic( dic,V[argument_dictionary],  name,argument_dictionary )


#V['bair_car_data_path'] = opjD('bair_car_data_new')
#V['bair_car_data_path'] = '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'
#V['bair_car_data_path'] = opjD('bair_car_data_Main_Dataset')
#V['bair_car_data_path'] = '/Volumes/SSD_2TB/bair_car_data_new_28April2017'
V[bair_car_data_path] = V[argument_dictionary][bair_car_data_path]
assert_disk_locations(V[bair_car_data_path])










i_variables = ['state','steer','motor','run_','runs','run_labels','meta_path','rgb_1to4_path',
	'B_','left_images','right_images','unsaved_labels']

i_labels = ['LCR','mostly_caffe','mostly_human','aruco_ring','out1_in2','direct','home','furtive',
	'play','racing','multicar','campus','night','Smyth','left','notes','local','Tilden','reject_run','reject_intervals','snow','follow','only_states_1_and_6_good']
not_direct_modes = ['out1_in2','left','furtive','play','racing','follow']

i_functions = ['function_close_all_windows','function_set_plot_time_range','function_set_label',
	'function_current_run','function_help','function_set_paths','function_list_runs','function_set_run',
	'function_visualize_run','function_animate','function_run_loop']

for q in i_variables + i_functions + i_labels:
	exec(d2n(q,' = ',"\'",q,"\'"))

i_label_abbreviations = {LCR:'LCR',aruco_ring:'ar_r',mostly_human:'mH',mostly_caffe:'mC',out1_in2:'o1i2', direct:'D',
	home:'H',furtive:'Fu',play:'P',racing:'R',multicar:'M',campus:'C',night:'Ni',Smyth:'Smy',
	left:'Lf',notes:'N',local:'L',Tilden:'T',reject_run:'X',reject_intervals:'Xi',snow:'S',follow:'F',
	only_states_1_and_6_good:'1_6'}

I = {}











def function_close_all_windows():
	plt.close('all')
CA = function_close_all_windows




def function_help():
	"""
	function_help(q=None)
			HE
			get help.
	"""
	cprint(doc_string,'yellow')
	cprint('INTERACTIVE FUNCTIONS:')
	for f in i_functions:
		exec('print('+f+'.__doc__)')
	cprint('INTERACTIVE VARIABLES:')
	tab_list_print(i_variables)
	cprint('\nINTERACTIVE LABELS:')
	tab_list_print(i_labels)
HE = function_help
HE() # do this here so that we are reminded of this feature






def function_set_paths(p=opj(V[bair_car_data_path])):
	"""
	function_set_paths(p=opj(V['bair_car_data_path']))
		SP
	"""
	V[bair_car_data_path] = p
	global I
	I[meta_path] = opj(p,'meta')
	I[rgb_1to4_path] = opj(p,'rgb_1to4')
	I[runs] = sgg(opj(I[meta_path],'*'))
	for j in range(len(I[runs])):
		I[runs][j] = fname(I[runs][j])
	I[run_] = I[runs][0]
	cprint('meta_path = '+I[meta_path])
SP = function_set_paths
SP()





def function_current_run():
	"""
	function_current_run()
		CR
	"""
	r=I[run_]
	n = len(gg(opj(I[rgb_1to4_path],r,'*.bag.pkl')))
	cprint(d2n('[',n,'] ',r))
	state_hist = np.zeros(10)
	L=I[B_]['left_image_bound_to_data']
	for l in L:
		s = L[l]['state']
		if type(s) == str:
			s = 0
		else:
			s = int(s)
		state_hist[s]+=1
	state_hist /= state_hist.sum()
	state_percent = []
	for i in range(0,8):
		s = state_hist[i]
		state_percent.append(int(100*s))
	print(d2s('State percentages:',state_percent[1:8]))
	print(I[run_labels][r])
CR = function_current_run






def blank_labels():
	l = {}
	l[local] = False
	l[Tilden] = False
	l[reject_run] = False
	l[reject_intervals] = False
	l[snow] = False
	l[follow] = False
	l[only_states_1_and_6_good] = False
	return l



def function_list_runs(rng=None,auto_direct_labelling=False):
	"""
	function_list_runs()
		LR
	"""
	cprint(I[meta_path])
	try:
		run_labels_path = most_recent_file_in_folder(opj(V[bair_car_data_path],'run_labels'),['run_labels'])
		cprint(run_labels_path,'green')
		I[run_labels] = load_obj(run_labels_path)
	except:
		cprint('Unable to load run_labels!!!!! Initalizing to empty dict')
		I[run_labels] = {}
	if rng == None:
		rng = range(len(I[runs]))
	for j in rng:
		r = I[runs][j]
		if r not in I[run_labels]:
			I[run_labels][r] = blank_labels()
		n = len(gg(opj(I[rgb_1to4_path],r,'*.bag.pkl')))
		labels_str = ""
		ks = sorted(I[run_labels][r])
		labeled = False

		
		if auto_direct_labelling:
			direct_flag = True
			for k in not_direct_modes:
				if k in I[run_labels][r]:

					if I[run_labels][r][k] != False:
						direct_flag = False
			if direct_flag:
				I[run_labels][r][direct] = True

		for k in ks:
			if I[run_labels][r][k] != False:
				if k != only_states_1_and_6_good:
					labeled = True
				labels_str += d2n(i_label_abbreviations[k],':',I[run_labels][r][k],' ')
		if labeled:
			c = 'yellow'
		else:
			c = 'blue'
		cprint(d2n(j,'[',n,'] ',r,'  ',j,'\t',labels_str),c)
		#print I[run_labels][r][direct]
	
LR = function_list_runs
LR() # If this is not done first, other things don't work properly.




def function_set_label(k,v=True):
	"""
	function_set_label(k,v)
		SL
	"""
	unix('mkdir -p '+opj(V[bair_car_data_path],'run_labels'))
	if not I[run_] in I[run_labels]:
		I[run_labels][I[run_]] = {}
	if type(k) != list:
		k = [k]
	for m in k:
		I[run_labels][I[run_]][m] = v
	save_obj(I[run_labels],opj(V[bair_car_data_path],'run_labels','run_labels_'+time_str()+'.pkl'))
SL = function_set_label




def function_set_run(j):
	"""
	function_set_run()
		SR
	"""
	global I
	I[run_] = I[runs][j]
	#cprint(run_ + ' = ' + I[run_])
	Bag_Folder_filename = gg(opj(I[meta_path],I[run_],'Bag_Folder*'))[0]
	B = load_obj(Bag_Folder_filename)
	I[B_] = B
	CR()
SR = function_set_run
#SR(0)



def function_set_plot_time_range(t0=-999,t1=-999):
	"""
	function_set_plot_time_range
		ST
	"""
	r = I[run_]
	B = I[B_]
	ts = np.array(B['data']['raw_timestamps'])
	tsZero = ts - ts[0]
	if t0 < 0:
		t0 = tsZero[0]
		t1 = tsZero[-1]
	#figure(r+' stats')
	figure('stats')
	#clf()
	plt.subplot(5,1,1)
	plt.xlim(t0,t1)
	plt.xlim(t0,t1)
	plt.subplot(5,1,2)
	plt.xlim(t0,t1)
	plt.subplot(5,1,3)
	plt.xlim(t0,t1)
	plt.subplot(5,1,4)
	plt.xlim(t0,t1)
ST = function_set_plot_time_range




if False: # trying to fix problem
	for mode in ['state','motor','steer']:
		for i in range(len(I[B_]['data'][mode])):
			if type(I[B_]['data'][mode][i]) == str:#'no data':
				print 'no data'
				if mode == 'state':
					I[B_]['data'][mode][i] = 0
				else:
					I[B_]['data'][mode][i] = 49


def function_adjust_offset(t_start,t_end,motor_offset,steer_offset):
	"""
	In some runs state 4 is reached unintentionally, leading to calibration faults.
	This function allows estimated correction of this. Saving results and putting them
	into correct location must be done manually:

		B=I[B_]
		B['data']['steer'] = B['data']['steer_corrected']
		B['data']['motor'] = B['data']['motor_corrected']
		so(B,opjD('Bag_Folder'))
	
	Then, rename original Bag_Folder.pkl as "B_ag_Folder.pkl" and put new one in meta folder.
	Then, rerun this program to insure that corrections were saved properly.
	"""
	B = I[B_]
	if I[B_] == None:
		cprint('ERROR, first neet to set run (SR)')
		return
	ts = np.array(B['data']['raw_timestamps'])
	tsZero = ts - ts[0]
	if 'steer_corrected' not in B['data']:
		B['data']['steer_corrected'] = B['data']['steer'].copy()
	if 'motor_corrected' not in B['data']:
		B['data']['motor_corrected'] = B['data']['motor'].copy()
	L = I[B_]['left_image_bound_to_data']
	for i in range(len(ts)):
		if ts[i]-ts[0] >= t_start and ts[i]-ts[0] < t_end:
			if not is_number(L[ts[i]]['motor']):
				print(L[ts[i]]['motor'])
				L[ts[i]]['motor'] = 49
			if not is_number(L[ts[i]]['steer']):
				print(L[ts[i]]['steer'])
				L[ts[i]]['steer'] = 49
			if not is_number(L[ts[i]]['state']):
				print(L[ts[i]]['state'])
				L[ts[i]]['state'] = 4		
			L[ts[i]]['motor'] += motor_offset
			L[ts[i]]['steer'] += steer_offset
			if is_number(steer_offset):
				B['data']['steer_corrected'][i] += steer_offset
			if is_number(motor_offset):
				B['data']['motor_corrected'][i] += motor_offset
	plt.subplot(5,1,2)
	plot(tsZero,B['data']['steer_corrected'],'r:')
	plot(tsZero,B['data']['motor_corrected'],'b:')	




def load_images(bag_file_path,color_mode="rgb8",include_flip=True):
    bag_img_dic = {}
    sides=['left','right']
    if bag_file_path.split('.')[-1] == 'bag':
        PKL = False
    elif bag_file_path.split('.')[-1] == 'pkl':
        PKL = True
    else:
        assert(False)
    if not PKL:
        for s in sides:
            bag_img_dic[s] = {}
        bag = rosbag.Bag(bag_file_path)
        for s in sides:
            for m in bag.read_messages(topics=['/bair_car/zed/'+s+'/image_rect_color']):
                t = round(m.timestamp.to_time(),3)
                img = bridge.imgmsg_to_cv2(m[1],color_mode)
                bag_img_dic[s][t] = img
    else:
        bag_img_dic = load_obj(bag_file_path)

    if include_flip:
        for s in sides:
            bag_img_dic[s+'_flip'] = {}
            for t in bag_img_dic[s]:
                img = bag_img_dic[s][t]
                bag_img_dic[s+'_flip'][t] = scipy.fliplr(img)
    return bag_img_dic




def function_visualize_run(j=None,img_load=False,do_CA=False):
	"""
	function_visualize_run()
		VR
	"""
	if do_CA:
		CA()
	if j != None:
		SR(j)
	else:
		CR()
	global I
	r = I[run_]
	#Bag_Folder_filename = gg(opj(I[meta_path],r,'Bag_Folder*'))[0]
	#B = load_obj(Bag_Folder_filename)
	#I[B_] = B
	B = I[B_]
	L = B['left_image_bound_to_data']
	if I[B_] == None:
		cprint('ERROR, first neet to set run (SR)')
		return
	
	ts = np.array(B['data']['raw_timestamps'])
	tsZero = ts - ts[0]
	dts = B['data']['raw_timestamp_deltas']
	dts_hist = []
	gZero = np.array(B['data']['good_start_timestamps'])
	gZero -= ts[0]

	for j in range(len(dts)):
		dt = dts[j]
		if dt > 0.3:
			dt = 0.3
		dts_hist.append(dt)

	#figure(r+' stats',figsize=(7,8))
	figure('stats',figsize=(7,8))
	clf()
	plt.subplot(5,1,1)
	plt.ylim(-1,8)
	plt.xlim(tsZero[0],tsZero[-1])
	plt.ylabel('state')
	plot(gZero,0.0*array(B['data']['good_start_timestamps']),'gx')
	#plot(tsZero,B['data']['encoder'],'r')
	plot(tsZero,B['data']['state'],'k')
	
	plt.subplot(5,1,2)
	plt.ylim(-5,104)
	plt.xlim(tsZero[0],tsZero[-1])
	plt.ylabel('steer(r) and motor(b)')
	plot(gZero,49+0.0*array(B['data']['good_start_timestamps']),'gx')
	plot(tsZero,B['data']['steer'],'r')
	plot(tsZero,B['data']['motor'],'b')

	plt.subplot(5,1,3)
	plt.xlim(tsZero[0],tsZero[-1])
	plt.ylabel('frame intervals')
	plot(gZero,0.0*array(B['data']['good_start_timestamps']),'gx')
	plot(tsZero,dts)
	plt.ylim(0,0.3)

	plt.subplot(5,1,4)
	plt.xlim(tsZero[0],tsZero[-1])
	plot(gZero,0.0*array(B['data']['good_start_timestamps']),'gx')
	plt.ylabel('state one steps')
	plot(tsZero,array(B['data']['state_one_steps']),'k-')
	#plt.ylim(0,500)

	plt.subplot(5,2,9)
	plt.ylabel('frame intervals')
	bins=plt.hist(dts_hist,bins=100)
	plt.xlim(0,0.3)
	plt.ylim(0,0.001*bins[0].max())
	plt.pause(0.01)

	if img_load:
		left_images_ = {}
		right_images_ = {}
		steer_ = {}
		motor_ = {}
		state_ = {}
		bag_paths = sgg(opj(I[rgb_1to4_path],r,'*.bag.pkl'))
		n = len(bag_paths)
		pb = ProgressBar(n)
		j =  0
		cprint('Loading images...')
		for b in bag_paths:
			pb.animate(j); j+=1
			bag_img_dic = load_images(b,color_mode="rgb8",include_flip=False)
			for t in bag_img_dic['left'].keys():
				#print t
				if t in L:
					steer_[t] = L[t]['steer']
					motor_[t] = L[t]['motor']
					state_[t] = L[t]['state']
					rt = L[t]['right_image']
					if rt in bag_img_dic['right']:
						left_images_[t] = bag_img_dic['left'][t]
						right_images_[t] = bag_img_dic['right'][rt]
					else:
						pass
						#print "rt not in right"
				else:
					pass
					#print "t not in left"

		pb.animate(n); print('')
		I[left_images] = left_images_
		I[right_images] = right_images_
		I[steer] = steer_
		I[motor] = motor_
		I[state] = state_
		#preview_fig = r+' previews'
		preview_fig = 'previews'

		figure(preview_fig)
		clf()

		N = 7
		T0 = B['data']['raw_timestamps'][0]
		Tn1 = B['data']['raw_timestamps'][-1]
		dT = (Tn1-T0)/N**2
		img_title = d2s('total time =',dp((Tn1-T0)/60.0,1),'minutes')
		ctr = 0
		for t in B['data']['raw_timestamps']:
			if t > T0 + ctr * dT:
				if t in left_images_:
					ctr += 1
					mi(left_images_[t],preview_fig,[N,N,ctr],do_clf=False);pause(0.01)
					if ctr == N/2:
						plt.title(img_title)
		pause(0.01)
VR = function_visualize_run

def VRi(j=None,img_load=True,do_CA=False):
	VR(j,img_load,do_CA)


def function_animate(t0,t1):
	"""
	function_animate(t0,t1)
		AR
	"""
	CR()
	dT = t1 - t0
	assert(dT>0)
	B = I[B_]
	T0 = t0 + B['data']['raw_timestamps'][0]
	ctr = 0
	s_timer = Timer(1)

	state_one_g_t_zero_dict = {}
	for i in range(len(B['data']['raw_timestamps'])):
		rt = B['data']['raw_timestamps'][i]
		state_one_g_t_zero_dict[rt] = B['data']['state_one_steps'][i]
		#print d2s(rt,state_one_g_t_zero_dict[rt])


	for t in B['data']['raw_timestamps']:
		if t >= T0:
			if s_timer.check():
				print(dp(t-T0+t0,0))
				s_timer.reset()
			if t < T0 + dT:
				rdt = B['data']['raw_timestamp_deltas'][ctr]
				if rdt > 0.1:
					cprint(d2s('Delay between frames =',rdt),'yellow','on_red')
					plt.pause(rdt)
				#mi(left_images[t],preview_fig,[N,N,5],do_clf=False)
				#pause(0.0001)
				try:
					img = I[left_images][t]
				except Exception as e:
					cprint("********** Exception ***********************",'red')
					print(e.message, e.args)
				#print state_one_g_t_zero_dict[t]
				if False:#state_one_g_t_zero_dict[t] < 1:#t not in B['good_timestamps_to_raw_timestamps_indicies__dic']:
					#img[:,:,0] = img[:,:,1]
					#img[:,:,2] = img[:,:,1]
					img[-10:,:,0] = 255
					img[-10:,:,1:2] = 0
				L = B['left_image_bound_to_data'][t]
				state = L['state']
				motor = L['motor']
				steer = L['steer']
				img = cv2.resize(img, (0,0), fx=3.0, fy=3.0)
				cv2.putText(img,d2s(int(state),int(steer),int(motor)),(10,30),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,0,0),4)
				cv2.imshow('function_animate',cv2.cvtColor(img,cv2.COLOR_RGB2BGR))
				if cv2.waitKey(30) & 0xFF == ord('q'):
					return
		ctr += 1
AR = function_animate



def function_run_loop():
	"""
	function_run_loop()
		RL
	"""
	print('')
	SR(0)
	while True:
		if True:#try:
			#
			#CR()
			command = raw_input(I[run_] + ' >> ')
			if command in ['q','quit','outta-here!']:
				break
			eval(command)
		else:#except Exception as e:
			cprint("********** Exception ***********************",'red')
			print(e.message, e.args)






if __name__ == '__main__' and '__file__' in locals():
	function_run_loop()











##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################







def function_save_hdf5(run_num=None,dst_path=opj(V[bair_car_data_path],'hdf5/runs'),flip=False):
	if run_num != None:
		CA()
		SR(run_num)
		VR()
	min_seg_len = 30
	seg_lens = []
	B = I[B_]
	L = B['left_image_bound_to_data']
	sos=B['data']['state_one_steps']

	segment_list = []

	in_segment = False

	for i in range(len(sos)):
		t = B['data']['raw_timestamps'][i]
		if sos[i] > 0 and t in I[left_images] and t in I[right_images]:
			if not in_segment:
				in_segment = True
				segment_list.append([])
			segment_list[-1].append(B['data']['raw_timestamps'][i])
		else:
			in_segment = False


	segment_list_with_min_len = []
	for s in segment_list:
		if len(s) >= min_seg_len:
			segment_list_with_min_len.append(s)

	for s in segment_list_with_min_len:
		seg_lens.append(len(s))

	
	if not flip:
		rn = opj(I[run_])
	else:
		rn = opj('flip_'+I[run_])

	unix('mkdir -p '+dst_path)

	F = h5py.File(opjD(dst_path,rn+'.hdf5'))

	glabels = F.create_group('labels')
	gsegments = F.create_group('segments')

	if flip:
		glabels['flip'] = np.array([1])
	else:
		glabels['flip'] = np.array([0])	
	for l in i_labels:
		if l in I[run_labels][I[run_]]:
			if I[run_labels][I[run_]][l]:
				glabels[l] = np.array([1])
			else:
				glabels[l] = np.array([0])
		else:
			glabels[l] = np.array([0])
	for i in range(len(segment_list_with_min_len)):
		segment = segment_list_with_min_len[i]
		left_image_list = []
		right_image_list = []
		steer_list = []
		motor_list = []
		state_list = []
		for j in range(len(segment)):
			t = segment[j]
			limg = I[left_images][t]
			rimg = I[right_images][t]
			st = I[steer][t]
			sta = I[state][t]
			if flip:
				st -= 49
				st *= -1.0
				st += 49
				left_image_list.append(scipy.fliplr(rimg))
				right_image_list.append(scipy.fliplr(limg))
				if glabels[LCR] > 0:
					if sta == 2: # reverse left-right direction indicated by state in LCR mode
						sta = 3
					elif sta == 3:
						sta = 2
			else:
				left_image_list.append(limg)
				right_image_list.append(rimg)
			steer_list.append(st)
			motor_list.append(I[motor][t])
			state_list.append(sta)#(I[state][t])
		gsegments[opj(str(i),'left_timestamp')] = segment
		gsegments[opj(str(i),'left')] = np.array(left_image_list)
		gsegments[opj(str(i),'right')] = np.array(right_image_list)
		gsegments[opj(str(i),'steer')] = np.array(steer_list)
		gsegments[opj(str(i),'motor')] = np.array(motor_list)
		gsegments[opj(str(i),'state')] = np.array(state_list)
	F.close()







def mi_or_cv2(img,cv=True,delay=30,title='animate'):
	if cv:
		cv2.imshow(title,cv2.cvtColor(img,cv2.COLOR_RGB2BGR))
		if cv2.waitKey(delay) & 0xFF == ord('q'):
			pass
	else:
		mi(img,title)
		pause(0.0001)





def function_load_hdf5(path):
	F = h5py.File(path)
	Lb = F['labels']
	S = F['segments']
	return Lb,S




def start_at(t):
	while time.time() < t:
		time.sleep(0.1)
		print t-time.time()

def load_animate_hdf5(path,start_at_time=0):
	start_at(start_at_time)
	l,s=function_load_hdf5(path)
	img = False
	for h in range(len(s)):
		if type(img) != bool:
			img *= 0
			img += 128
			mi_or_cv2(img)
		pause(0.5)
		n = str(h)
		for i in range(len(s[n]['left'])):
			img = s[n]['left'][i]
			#print s[n][state][i]
			bar_color = [0,0,0]
			
			if s[n][state][i] == 1:
				bar_color = [0,0,255]
			elif s[n][state][i] == 6:
				bar_color = [255,0,0]
			elif s[n][state][i] == 5:
				bar_color = [255,255,0]
			elif s[n][state][i] == 7:
				bar_color = [255,0,255]
			else:
				bar_color = [0,0,0]
			if i < 2:
				smooth_steer = s[n][steer][i]
			else:
				smooth_steer = (s[n][steer][i] + 0.5*s[n][steer][i-1] + 0.25*s[n][steer][i-2])/1.75
			#print smooth_steer
			apply_rect_to_img(img,smooth_steer,0,99,bar_color,bar_color,0.9,0.1,center=True,reverse=True,horizontal=True)
			apply_rect_to_img(img,s[n][motor][i],0,99,bar_color,bar_color,0.9,0.1,center=True,reverse=True,horizontal=False)
			mi_or_cv2(img)
A5 = load_animate_hdf5






########################################################





def load_hdf5_steer_hist(path,dst_path):
	if len(gg(opj(dst_path,fname(path).replace('hdf5','state_hist_list.pkl')))) == 1:
		print(opj(dst_path,fname(path).replace('hdf5','state_hist_list.pkl'))+' exists')
		return
	try:
		print path
		unix('mkdir -p '+dst_path)
		low_steer = []
		high_steer = []
		l,s=function_load_hdf5(path)
		pb = ProgressBar(len(s))
		state_hist_list = []
		for h in range(len(s)):
			pb.animate(h)
			state_hist = np.zeros(8)
			n = str(h)
			for i in range(len(s[n][left])):
				state_hist[int(s[n][state][i])] += 1
				if i < 2:
					smooth_steer = s[n][steer][i]
				else:
					smooth_steer = (s[n][steer][i] + 0.5*s[n][steer][i-1] + 0.25*s[n][steer][i-2])/1.75
				if smooth_steer < 43 or smooth_steer > 55:
					high_steer.append([h,i,int(round(smooth_steer))])
				else:
					low_steer.append([h,i,int(round(smooth_steer))])
			state_hist_list.append(state_hist)
		pb.animate(h)
		assert(len(high_steer)>0)
		assert(len(low_steer)>0)
		save_obj(low_steer+high_steer,opj(dst_path,fname(path).replace('hdf5','all_valid_data_moments.pkl')))
		save_obj(high_steer,opj(dst_path,fname(path).replace('hdf5','high_steer_data_moments.pkl')))
		save_obj(low_steer,opj(dst_path,fname(path).replace('hdf5','low_steer_data_moments.pkl')))
		save_obj(state_hist_list,opj(dst_path,fname(path).replace('hdf5','state_hist_list.pkl')))
	except Exception as e:
		cprint("********** load_hdf5_steer_hist Exception ***********************",'red')
		print(e.message, e.args)






def create_normal_and_flip_hdf5_segements():
	CS_("Goal: create normal and flip hdf5 segements. (Very time consuming)")
	hdf5_runs_path = opj(pname(I['meta_path']),'hdf5','runs')
	existing_hdf5_files = gg(opj(hdf5_runs_path,'*.hdf5'))
	for i in range(len(existing_hdf5_files)):
		existing_hdf5_files[i] = fname(existing_hdf5_files[i])
	for i in range(len(I[runs])):
		r = I[runs][i]
		if r+'.hdf5' in existing_hdf5_files:
			print(r+' is done')
			continue
		else:
			print(r+' is NOT done')
		if True:#try:
			VR(i,img_load=True)
			
			ks = sorted(I[run_labels][r])
			labeled = False
			for k in ks:
				if I[run_labels][r][k]:
					labeled = True
			if labeled and I[run_labels][I[runs][i]][reject_run] == False:
				cprint(d2s(i,') accept',r),'yellow')
				function_save_hdf5(i,flip=False)
				function_save_hdf5(flip=True)
			else:
				cprint(d2s(i,') reject',r),'red')

		else:#except Exception as e:
			print("********** Exception ***********************")
			print(e.message, e.args)
			cprint('Failure in for i in range(len(I[runs])): loop','blue')



def create_valid_hdf5_data_moments():
	CS_("Goal: create valid data moments. (Time Consuming)")
	hdf5s = sgg(opj(V[bair_car_data_path],'hdf5/runs/*.hdf5'))
	ctr = 0
	for h in hdf5s:
		ctr += 1
		print ctr
		load_hdf5_steer_hist(h,opj(V[bair_car_data_path],'hdf5','segment_metadata'))



def compile_run_codes_and_hdf5_data_moment_lists():
	if True:
		CS_("Goal: compile run codes. (Fast)")
		run_codes = {}
		steer_hists = sgg(opj(V[bair_car_data_path],'hdf5/segment_metadata/*.state_hist_list.pkl'))
		ctr = 0
		combined = []
		for s in steer_hists:
			o = load_obj(s)
			run_codes[ctr] = fname(s).replace('.state_hist_list.pkl','')
			print ctr,run_codes[ctr]
			#for j in range(len(o)):
			#	o[j][3] = ctr
			#	combined.append(o[j])
			ctr += 1
		#save_obj(combined,opjD('combined'))
		unix('mkdir -p '+opj(V[bair_car_data_path],'hdf5/segment_metadata'))
		save_obj(run_codes,opj(V[bair_car_data_path],'hdf5/segment_metadata/run_codes'))
	if True:
		CS_("Goal: compile low_steer and high_steer. (Fast)")
		low_steer = []
		high_steer = []
		low_steer_files = sgg(opj(V[bair_car_data_path],'hdf5/segment_metadata/*.low_steer_data_moments.pkl'))
		ctr = 0
		for s in low_steer_files:
			print (ctr,s)
			q = load_obj(s)
			for i in range(len(q)):
				q[i].append(ctr)
			low_steer += q
			q = load_obj(s.replace('.low_steer.','.high_steer_data_moments.'))
			for i in range(len(q)):
				q[i].append(ctr)
			high_steer += q
			ctr += 1
		save_obj(high_steer+low_steer,opj(V[bair_car_data_path],'hdf5/segment_metadata/all_valid_data_moments'))
		save_obj(low_steer,opj(V[bair_car_data_path],'hdf5/segment_metadata/low_steer_data_moments'))
		save_obj(high_steer,opj(V[bair_car_data_path],'hdf5/segment_metadata/high_steer_data_moments'))







if False:
	create_normal_and_flip_hdf5_segements()
	create_valid_hdf5_data_moments()
	compile_run_codes_and_hdf5_data_moment_lists()






if False:
	p = lo('/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/hdf5/segment_metadata/all_valid_data_moments.pkl' )
	q=random.shuffle(p)  
	val_all_steer = p[:int(len(p)*0.1)]
	train_all_steer = p[int(len(p)*0.1):]
	so(opj('/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/hdf5/segment_metadata','val_all_steer'),val_all_steer)
	so(opj('/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/hdf5/segment_metadata','train_all_steer'),train_all_steer)

# rsync -rav /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/hdf5 /home/karlzipser/Desktop/bdd_car_data_July2017_LCR/









#EOF