from kzpy3.teg8.train_with_hdf5_utils import *

"""
*** kzpy3/teg8/train_with_hdf5.py ***

This script trains a model on hdf5 model car data. It expects to find the hdf5 folder here:

	~/Desktop/bair_car_data/hdf5

It also needs:

	~/kzpy3/caf7/z2_color/solver.prototxt
	~/kzpy3/caf7/z2_color/train_val.prototxt

and expects to find a folder:

	~/Desktop/z2_color

for saving weights.

Can run from python or command line:

	$ python ~/kzpy3/teg8/train_with_hdf5.py

The script regularly displays left camera data, steer data (red) and
network steer output (green) [49=straight, 0=right, 99=left], and loss
averaged over 10000 iterations.

"""


USE_GPU = True
if USE_GPU:
	caffe.set_device(1)
	caffe.set_mode_gpu()

if True:
	load_run_codes()

if True:
	pb = ProgressBar(len(Segment_Data['run_codes']))
	ctr = 0
	print("doing run_into_Segment_Data...")
	for n in Segment_Data['run_codes'].keys():
		ctr+=1
		pb.animate(ctr)
		run_into_Segment_Data(n)
	pb.animate(len(Segment_Data['run_codes']))

if True:
	print('\nloading low_steer... (takes awhile)')
	low_steer = load_obj(opjD('bair_car_data/hdf5/segment_metadata/low_steer'))
	print('\nloading high_steer... (takes awhile)')
	high_steer = load_obj(opjD('bair_car_data/hdf5/segment_metadata/high_steer'))

	len_high_steer = len(high_steer)
	len_low_steer = len(low_steer)
	ctr_low = -1 # These counter keep track of position in segment lists, and when to reshuffle.
	ctr_high = -1

if True:
	solver_name = opjh('kzpy3/caf7/z2_color/solver_loss.prototxt')
	solver = setup_solver(solver_name)
	weights_file_path = opjh('kzpy3/caf5/z2_color/z2_color.caffemodel')
	#solver.net.copy_from(weights_file_path)
	#cprint('Loaded weights from '+weights_file_path)
	N_FRAMES = 2 # how many timesteps with images.
	N_STEPS = 10 # how many timestamps with non-image data

	if 'solver_loss' in solver_name:
		ignore = [reject_run,left,out1_in2,Smyth,racing] # runs with these labels are ignored
		require_one = [] # at least one of this type of run lable is required
		use_states = [1,5,6,7]
	if 'solver_state_1_no_Smyth_or_racing' in solver_name:
		ignore = [reject_run,left,out1_in2,Smyth,racing] # runs with these labels are ignored
		require_one = [] # at least one of this type of run lable is required
		use_states = [1]
	if 'solver_state_6_no_Smyth_or_racing' in solver_name:
		ignore = [reject_run,left,out1_in2,Smyth,racing] # runs with these labels are ignored
		require_one = [] # at least one of this type of run lable is required
		use_states = [6]
	if 'solver_state_1_5_6_7_no_Smyth_or_racing' in solver_name:
		ignore = [reject_run,left,out1_in2,Smyth,racing] # runs with these labels are ignored
		require_one = [] # at least one of this type of run lable is required
		use_states = [1,5,6,7]
	if 'solver_state_1_5_6_7.' in solver_name:
		ignore = [reject_run,left,out1_in2] # runs with these labels are ignored
		require_one = [] # at least one of this type of run lable is required
		use_states = [1,5,6,7]
	if 'solver_state_1_5_6_7_plus_extra_Smyth_racing' in solver_name:
		ignore = [reject_run,left,out1_in2] # runs with these labels are ignored
		require_one = [Smyth,racing] # at least one of this type of run lable is required
		use_states = [1,5,6,7]
	print_timer = Timer(5)
	save_timer = Timer(60*10)
	loss10000 = []
	loss = []
	rate_timer_interval = 10.
	rate_timer = Timer(rate_timer_interval)
	rate_ctr = 0


	print "Loading z2_color_loss_dict . . ."
	loss_dict = load_obj(opjD('z2_color_loss_dict'))
	choice_list = []
	for run_code in loss_dict.keys():
		for seg_num in loss_dict[run_code].keys():
			for offset in loss_dict[run_code][seg_num].keys():
				choice_list.append( [run_code,seg_num,offset] )
	print(d2s('len(choice_list) =',len(choice_list)))
	len_choice_list = len(choice_list)
	choice_ctr = -1
	lctr = 0
	while True:
		if choice_ctr == -1 or choice_ctr >= len_choice_list:
			random.shuffle(choice_list)
			choice_ctr = 0
		choice = choice_list[choice_ctr]
		run_code = choice[0]
		seg_num = choice[1]
		offset = choice[2]
		choice_ctr += 1
		data = get_data(run_code,seg_num,offset,N_STEPS,offset+0,N_FRAMES,ignore=ignore,require_one=require_one,use_states=use_states)
		if data == None:
			continue
		############## load data into solver #####################
		#
		ctr = 0
		for c in range(3):
			for camera in ('left','right'):
				for t in range(N_FRAMES):
					solver.net.blobs['ZED_data_pool2'].data[0,ctr,:,:] = data[camera][t][:,:,c]
					ctr += 1
		Racing = 0
		Caf = 0
		Follow = 0
		Direct = 0
		Play = 0
		Furtive = 0
		if data['labels']['racing']:
			Racing = 1.0
		if data['states'][0] == 6:
			Caf = 1.0
		if data['labels']['follow']:
			Follow = 1.0
		if data['labels']['direct']:
			Direct = 1.0
		if data['labels']['play']:
			Play = 1.0
		if data['labels']['furtive']:
			Furtive = 1.0
		solver.net.blobs['metadata'].data[0,0,:,:] = Racing
		solver.net.blobs['metadata'].data[0,1,:,:] = Caf
		solver.net.blobs['metadata'].data[0,2,:,:] = Follow
		solver.net.blobs['metadata'].data[0,3,:,:] = Direct
		solver.net.blobs['metadata'].data[0,4,:,:] = Play
		solver.net.blobs['metadata'].data[0,5,:,:] = Furtive
		solver.net.blobs['steer_motor_target_data'].data[0,0] = loss_dict[run_code][seg_num][offset]
		#
		##########################################################
		solver.step(1) # The training step. Everything below is for display.
		rate_ctr += 1
		lctr += 1
		if rate_timer.check():
			print(d2s('rate =',dp(rate_ctr/rate_timer_interval,2),'Hz'))
			rate_timer.reset()
			rate_ctr = 0
		a = solver.net.blobs['steer_motor_target_data'].data[0,:] - solver.net.blobs['ip2'].data[0,:]
		loss = np.sqrt(a * a).mean()
		loss_dict[run_code][seg_num][offset] = loss
		if print_timer.check():
			print(d2s("lctr =",lctr))
			print(solver.net.blobs['metadata'].data[0,:,5,5])
#			cprint(array_to_int_list(solver.net.blobs['steer_motor_target_data'].data[0,:][:]),'green','on_red')
#			cprint(array_to_int_list(solver.net.blobs['ip2'].data[0,:][:]),'red','on_green')
			cprint(solver.net.blobs['steer_motor_target_data'].data[0,:][:],'green','on_red')
			cprint(solver.net.blobs['ip2'].data[0,:][:],'red','on_green')
			print_timer.reset()
		#if save_timer.check():
		#	save_obj(loss_dict,opjD('z2_color_loss_dict'))
		#	save_timer.reset()
	#save_obj(loss_dict,opjD('z2_color_loss_dict'))
