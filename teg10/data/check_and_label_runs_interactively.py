
from kzpy3.misc.progress import *
from kzpy3.vis2 import *


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
    	'pargs':"-src /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_path_dataset"})
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
		run_labels_path = most_recent_file_in_folder(opj(V['bair_car_data_path'],'run_labels'),['run_labels'])
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
	if not I[run_] in I[run_labels]:
		I[run_labels][I[run_]] = {}
	if type(k) != list:
		k = [k]
	for m in k:
		I[run_labels][I[run_]][m] = v
	save_obj(I[run_labels],opj(V['bair_car_data_path'],'run_labels','run_labels_'+time_str()+'.pkl'))
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
	clf()
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
	for i in range(len(I[B_]['data']['state'])):
		if I[B_]['data']['state'][i] == 'no data':
			I[B_]['data']['state'][i] = 0



def function_adjust_offset(t_start,t_end,motor_offset,steer_offset):
	"""
	In some runs state 4 is reached unintentionally, leading to calibration faults.
	This function allows estimated correction of this. Saving results and putting them
	into correct location must be done manually.
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
				if state_one_g_t_zero_dict[t] < 1:#t not in B['good_timestamps_to_raw_timestamps_indicies__dic']:
					#img[:,:,0] = img[:,:,1]
					#img[:,:,2] = img[:,:,1]
					img[-10:,:,0] = 255
					img[-10:,:,1:2] = 0
				cv2.imshow('video',cv2.cvtColor(img,cv2.COLOR_RGB2BGR))
				if cv2.waitKey(30) & 0xFF == ord('q'):
					pass
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







#EOF