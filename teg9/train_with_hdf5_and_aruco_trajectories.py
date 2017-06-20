from kzpy3.vis2 import *
from kzpy3.vis import mi_or_cv2_animate
import kzpy3.teg9.data.utils.get_data_with_hdf5 as get_data_with_hdf5
import caffe

REPO = 'kzpy3'
TEG = 'teg9'
CAF = 'caf8'
DISPLAY = True

ignore = ['reject_run','left','out1_in2','Smyth','racing','local','Tilden','campus'] # runs with these labels are ignored
require_one = ['aruco_ring'] # at least one of this type of run lable is required
use_states = [1,3,5,6,7]
rate_timer_interval = 5.
print_timer = Timer(5)

if False:
	MODEL = 'z2_color'
	print(MODEL)
	bair_car_data_path = opjD('bair_car_data_new_28April2017') #opjD('bair_car_data_Main_Dataset') # opjD('bair_car_data_new')
	weights_file_path =  most_recent_file_in_folder(opjD(MODEL),['caffemodel'])
	#weights_file_path = opjh('caffe_models/z2_color.caffemodel')
	N_FRAMES = 2 # how many timesteps with images.
	N_STEPS = 10 # how many timestamps with non-image data
	gpu = 1

if True:
	MODEL = 'z2_color_aruco'
	print(MODEL)
	bair_car_data_path = opjD('bair_car_data_new_28April2017') #opjD('bair_car_data_Main_Dataset') # opjD('bair_car_data_new')
	weights_file_path =  most_recent_file_in_folder(opjD(MODEL),['caffemodel'])
	#weights_file_path = opjh('caffe_models/z2_color/z2_color.caffemodel')
	N_FRAMES = 2 # how many timesteps with images.
	N_STEPS = 10 # how many timestamps with non-image data
	gpu = 1


if False:
	MODEL = 'z2_color_small_ip1'
	print(MODEL)
	bair_car_data_path = opjD('bair_car_data_Main_Dataset') # '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'#opjD('bair_car_data_new')
	weights_file_path =  most_recent_file_in_folder(opjD(fname(opjh(REPO,CAF,MODEL))),['caffemodel'])
	N_FRAMES = 2 # how many timesteps with images.
	N_STEPS = 10 # how many timestamps with non-image data
	gpu = 1


if False:
	MODEL = 'z3_color'
	print(MODEL)
	bair_car_data_path = opjD('bair_car_data_Main_Dataset') # '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'#opjD('bair_car_data_new')
	weights_file_path = most_recent_file_in_folder(opjD(fname(opjh(REPO,CAF,MODEL))),['caffemodel'])
	#weights_file_path = opj('caffe_models/z3_color_iter_14600000.caffemodel')
	N_FRAMES = 3 # how many timesteps with images.
	N_STEPS = 30 # how many timestamps with non-image data
	gpu = 1


if False:
	MODEL = 'z1_color'
	print(MODEL)
	bair_car_data_path = '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'
	weights_file_path = most_recent_file_in_folder(opjD(fname(opjh(REPO,CAF,MODEL))),['caffemodel'])
	N_FRAMES = 1 # how many timesteps with images.
	N_STEPS = 10 # how many timestamps with non-image data
	gpu = 1



"""
#relative_heading:
clock_potential_values:
potential_values:
desired_direction:

marker_inverse_distances:
near_t:
other_car_inverse_distances:
steer:
velocity:

"""
if False:
	CS_('load aruco trajectory data')
	Aruco_Steering_Trajectories = {}
	aruco_data_location = opjD('output_data')
	paths = sggo(aruco_data_location,'*.pkl')
	for i in range(len(paths)):
		o = paths[i]
		ast = lo(o)
		for run_name in ast.keys():	
			print(d2n(run_name,' (',i+1,' of ',len(paths),')'))
			if run_name not in Aruco_Steering_Trajectories:
				Aruco_Steering_Trajectories[run_name] = {}
			if len(ast[run_name].keys()) > 4:
				print_stars()
				continue
			for mode in ast[run_name].keys():
				print('\t'+mode)
				if mode not in Aruco_Steering_Trajectories[run_name]:
					Aruco_Steering_Trajectories[run_name][mode] = {}
				timestamps = ast[run_name][mode]['near_t']
				dd = ast[run_name][mode]['desired_direction'][0]
				print('\t\t'+str(dd))
				Aruco_Steering_Trajectories[run_name][mode][dd] = {}
				for i in range(len(timestamps)):
					t = timestamps[i]
					Aruco_Steering_Trajectories[run_name][mode][dd][t] = {}
					for topic in ast[run_name][mode].keys():
						if topic not in ['near_t','desired_direction']:
							q = ast[run_name][mode][topic][i]
							if not(is_number(q)):
								q = array(q)
								q = q.astype(np.float16)
							else:
								q = np.float16(q)
							Aruco_Steering_Trajectories[run_name][mode][dd][t][topic] = q
	
	ctr = 0
	for run_name in Aruco_Steering_Trajectories.keys():
		if 'flip_' in run_name:
			del Aruco_Steering_Trajectories[run_name]
			continue
		flip = 'flip_'+run_name
		print(d2n(flip,' (',ctr+1,' of ',len(paths),')'))
		ctr += 1
		Aruco_Steering_Trajectories[flip]= {}
		for mode in Aruco_Steering_Trajectories[run_name]:
			Aruco_Steering_Trajectories[flip][mode] = {}
			for dd in [0,1]:
				Aruco_Steering_Trajectories[flip][mode][dd] = {}
				for t in Aruco_Steering_Trajectories[run_name][mode][dd].keys():
					Aruco_Steering_Trajectories[flip][mode][dd][t] = {}
					Aruco_Steering_Trajectories[flip][mode][dd][t]['steer'] = np.float16(99-Aruco_Steering_Trajectories[run_name][mode][dd][t]['steer'])
					Aruco_Steering_Trajectories[flip][mode][dd][t]['velocity'] = np.float16(Aruco_Steering_Trajectories[run_name][mode][dd][t]['velocity'])
					l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['other_car_inverse_distances'])
					l.reverse(); l = array(l); l = l.astype(np.float16)
					Aruco_Steering_Trajectories[flip][mode][dd][t]['other_car_inverse_distances'] = l
					l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['marker_inverse_distances'])
					l.reverse(); l = array(l); l = l.astype(np.float16)
					Aruco_Steering_Trajectories[flip][mode][dd][t]['marker_inverse_distances'] = l
					l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['potential_values'])
					l.reverse(); l = array(l); l = l.astype(np.float16)
					Aruco_Steering_Trajectories[flip][mode][dd][t]['potential_values'] = l

					l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['clock_potential_values'])
					l.reverse(); l = array(l); l = l.astype(np.float16)
					Aruco_Steering_Trajectories[flip][mode][dd][t]['clock_potential_values'] = l

					if dd == 0:
						Aruco_Steering_Trajectories[flip][mode][dd][t]['desired_direction'] = 1
					else:
						Aruco_Steering_Trajectories[flip][mode][dd][t]['desired_direction'] = 0
					Aruco_Steering_Trajectories[flip][mode][dd][t]['relative_heading'] =  np.float16(360 - Aruco_Steering_Trajectories[run_name][mode][dd][t]['relative_heading'])

	unix('mkdir -p '+opjD('Aruco_Steering_Trajectories'))
	ctr = 0
	for run_name in sorted(Aruco_Steering_Trajectories.keys()):
		print(d2n(run_name,' (',ctr+1,' of ',len(paths),')'))
		so(Aruco_Steering_Trajectories[run_name],opjD('Aruco_Steering_Trajectories',run_name))
		ctr += 1
	raw_input('enter')

#wait_for_enter()
if True:
	print("Loading Aruco_Steering_Trajectories . . .")
	paths = sggo(opjD('Aruco_Steering_Trajectories','*.pkl'))
	Aruco_Steering_Trajectories = {}
	ctr = 0
	for p in paths:
		o = lo(p)
		run_name = fname(p).replace('.pkl','')
		print(d2n(run_name,' (',ctr+1,' of ',len(paths),')'))
		Aruco_Steering_Trajectories[run_name] = o
		ctr += 1





#while True:
#	try:
if gpu >= 0:
	caffe.set_device(gpu)
	caffe.set_mode_gpu()

import_str = "import REPO.CAF.MODEL.solver as Solver"
import_str = import_str.replace("REPO",REPO)
import_str = import_str.replace("CAF",CAF)
import_str = import_str.replace("MODEL",MODEL)
exec(import_str)

time.sleep(0)

hdf5_runs_path = opj(bair_car_data_path,'hdf5/runs')
hdf5_segment_metadata_path = opj(bair_car_data_path,'hdf5/segment_metadata')


loss10000 = []
loss = []

rate_timer = Timer(rate_timer_interval)
rate_ctr = 0

get_data_with_hdf5.load_Segment_Data(hdf5_segment_metadata_path,hdf5_runs_path)



print('\nloading low_steer... (takes awhile)')
low_steer = load_obj(opj(hdf5_segment_metadata_path,'low_steer'))
random.shuffle(low_steer)
print('\nloading high_steer... (takes awhile)')
high_steer = load_obj(opj(hdf5_segment_metadata_path,'high_steer'))
random.shuffle(high_steer)
print('done')
len_high_steer = len(high_steer)
len_low_steer = len(low_steer)

ctr_low = -1 # These counter keep track of position in segment lists, and when to reshuffle.
ctr_high = -1






def get_data_considering_high_low_steer():
	global ctr_low
	global ctr_high
	global low_steer
	global high_steer

	if ctr_low >= len_low_steer:
		ctr_low = -1
	if ctr_high >= len_high_steer:
		ctr_high = -1
	if ctr_low == -1:
		random.shuffle(low_steer) # shuffle data before using (again)
		ctr_low = 0
	if ctr_high == -1:
		random.shuffle(high_steer)
		ctr_high = 0
		
	if random.random() < 0.5: # len_high_steer/(len_low_steer+len_high_steer+0.0): # with some probability choose a low_steer element
		choice = low_steer[ctr_low]
		ctr_low += 1
	else:
		choice = high_steer[ctr_high]
		ctr_high += 1
	run_code = choice[3]
	seg_num = choice[0]
	offset = choice[1]

	data = get_data_with_hdf5.get_data(run_code,seg_num,offset,N_STEPS,offset+0,N_FRAMES,ignore=ignore,require_one=require_one,use_states=use_states)

	return data



loss_dic = {}
counter_dic = {}
counts = 0
high_loss_dic = {}
high_loss_keys = []
high_loss_key_ctr = 200000




############################################
#
if weights_file_path:
	print(d2s("Copying weights from",weights_file_path,"to",Solver.solver))
	Solver.solver.net.copy_from(weights_file_path)
else:
	print(d2s("No weights loaded to",Solver.solver))
#
###########################


def get_data_considering_high_low_steer_and_valid_trajectory_timestamp():
	#print "get_data_considering_high_low_steer_and_valid_trajectory_timestamp"
	global ctr_low
	global ctr_high
	global low_steer
	global high_steer
	global counts
	global high_loss_key_ctr
	global high_loss_keys

	if ctr_low >= len_low_steer:
		ctr_low = -1
	if ctr_high >= len_high_steer:
		ctr_high = -1
	if ctr_low == -1:
		random.shuffle(low_steer) # shuffle data before using (again)
		ctr_low = 0
	if ctr_high == -1:
		random.shuffle(high_steer)
		ctr_high = 0
		
	if random.random() < 0.5: # len_high_steer/(len_low_steer+len_high_steer+0.0): # with some probability choose a low_steer element
		choice = low_steer[ctr_low]
		ctr_low += 1
	else:
		choice = high_steer[ctr_high]
		ctr_high += 1
	run_code = choice[3]
	seg_num = choice[0]
	offset = choice[1]


	run_name = get_data_with_hdf5.Segment_Data['run_codes'][run_code]
	#print run_name
	if run_name not in Aruco_Steering_Trajectories.keys():
		#print('Run name '+run_name+' not in Aruco_Steering_Trajectories')
		return None
	if len(Aruco_Steering_Trajectories[run_name].keys()) < 2:
		#print('len(Aruco_Steering_Trajectories[run_name].keys()) <= 2')
		return None

	#print 'here!'
	seg_num_str = str(seg_num)
	aruco_matches = []
	#print(run_code,seg_num,offset,N_STEPS,offset+0,N_FRAMES)
	for i in [0]:#range(N_FRAMES):
		timestamp = get_data_with_hdf5.Segment_Data['runs'][run_name]['segments'][seg_num_str]['left_timestamp'][offset+i]
		behavioral_mode = np.random.choice(
			['Direct_Arena_Potential_Field',
 			#'Furtive_Arena_Potential_Field',
 			'Follow_Arena_Potential_Field'])
 			#'Play_Arena_Potential_Field'])
		desired_direction = np.random.choice([0,1])

		if timestamp in Aruco_Steering_Trajectories[run_name][behavioral_mode][desired_direction].keys():
			aruco_matches.append(timestamp)
		if len(aruco_matches) < 1:
			return None
	data = get_data_with_hdf5.get_data(run_code,seg_num,offset,N_STEPS,offset+0,N_FRAMES,ignore=ignore,require_one=require_one)
	if data != None:
		data['behavioral_mode'] = behavioral_mode
		data['desired_direction'] = desired_direction
 		for topic in Aruco_Steering_Trajectories[run_name][behavioral_mode][desired_direction][timestamp]:
 			data[topic] = Aruco_Steering_Trajectories[run_name][behavioral_mode][desired_direction][timestamp][topic]
 		data['id'] = (run_name,behavioral_mode,desired_direction,timestamp,run_code,seg_num,offset)


	return data

def array_to_int_list(a):
	l = []
	for d in a:
		l.append(int(d*100))
	return l



if DISPLAY:
	#figure('steer',figsize=(3,2))
	figure('loss',figsize=(3,2))
	figure('high low steer histograms',figsize=(2,1))
	histogram_plot_there = True
	clf()
	plt.hist(array(low_steer)[:,2],bins=range(0,100))
	plt.hist(array(high_steer)[:,2],bins=range(0,100))
	figure(1)

loss_threshold = 0.08
velocity_data = []
velocity_data_timer = Timer(60)
even_ctr = 0



data_log = {}

while True:

	for b in range(Solver.batch_size):
		_data = None
		while _data == None:
			_data = get_data_considering_high_low_steer_and_valid_trajectory_timestamp()
		data = _data

		if data['id'] not in data_log:
			data_log[data['id']] = 0
		data_log[data['id']] += 1

		Solver.put_data_into_model(data,Solver.solver,b)
	if len(data['other_car_inverse_distances']) == 0:
		if np.random.random()<0.:
			continue

	Solver.solver.step(1) # The training step. Everything below is for display.

	rate_ctr += 1
	if rate_timer.check():
		print(d2s('rate =',dp(rate_ctr/rate_timer_interval,2),'Hz'))
		rate_timer.reset()
		rate_ctr = 0
	#the_loss = Solver.solver.net.blobs['steer_motor_target_data'].data[0,:] - Solver.solver.net.blobs['ip2'].data[0,:]
	#the_loss = np.sqrt(the_loss * the_loss).mean()
	#loss.append(the_loss)
	"""
	if the_loss >= loss_threshold:
		high_loss_dic[data['id']] = the_loss
	else:
		if data['id'] in high_loss_dic:
			del high_loss_dic[data['id']]
			#print(d2s('removed',data['id'],'from high_loss_dic'))
	"""
	#loss_dic[data['id']] = the_loss
	"""
	if len(loss) >= 10000/Solver.batch_size:
		loss10000.append(array(loss[-10000:]).mean())
		loss = []
		if DISPLAY:
			figure('loss');clf()
			lm = min(len(loss10000),300)
			plot(loss10000[-lm:])
			if histogram_plot_there:
				plt.close('high low steer histograms')
				histogram_plot_there = False
		print(d2s('loss10000 =',loss10000[-1]))
	"""
	velocity_data.append([Solver.solver.net.blobs['velocity'].data[-1,0], Solver.solver.net.blobs['ip_velocity'].data[-1,0]])


	if print_timer.check():#Solver.solver.net.blobs['metadata'].data[0,3,0,0] > 0 and the_loss > 0.1:#loss_threshold:
		print(d2s('len of data_log ='),len(data_log.keys()))
		print(data['name'])
		print(Solver.solver.net.blobs['metadata'].data[-1,:,5,5])

		if Solver.solver.net.blobs['metadata'].data[0,2,0,0] > 0:
			print 'follow'
		if Solver.solver.net.blobs['metadata'].data[0,3,0,0] > 0:
			print 'direct'
		if Solver.solver.net.blobs['metadata'].data[0,4,0,0] > 0:
			print 'play'
		if Solver.solver.net.blobs['metadata'].data[0,5,0,0] > 0:
			print 'furtive'
		print(d2s('len(counter_dic),counts',(len(counter_dic),counts)))
		print(array_to_int_list(Solver.solver.net.blobs['steer'].data[-1,:][:]),array_to_int_list(Solver.solver.net.blobs['motor'].data[-1,:][:]))
		print(array_to_int_list(Solver.solver.net.blobs['ip3_steer'].data[-1,:][:]),array_to_int_list(Solver.solver.net.blobs['ip3_motor'].data[-1,:][:]))
		velocity_data.append([Solver.solver.net.blobs['velocity'].data[-1,0], Solver.solver.net.blobs['ip_velocity'].data[-1,0]])
		if DISPLAY:
			fctr = 0
			for plot_data in [['potential_values','ip_potential_values'],['marker_inverse_distances','ip_marker_inverse_distances'],
				['other_car_inverse_distances','ip_other_car_inverse_distances'],['clock_potential_values','ip_clock_potential_values'],]:
				figure(d2s(fctr,plot_data[0]),figsize=(3,3));clf()
				t = Solver.solver.net.blobs[plot_data[0]].data[-1,:]
				o = Solver.solver.net.blobs[plot_data[1]].data[-1,:]
				ylim(-0.05,2.05);xlim(-0.5,len(t)-0.5)
				plot([-1,60],[0.49,0.49],'k');plot(o,'og'); plot(t,'or'); plt.title(data['name'])
				fctr += 1
			mi_or_cv2_animate(data['left'],delay=33);pause(0.001)

		print_timer.reset()
	
	if velocity_data_timer.check():
		velocity_data_timer.reset()
		figure('velocity data')
		clf()
		xylim(0,2,0,2)
		v = array(velocity_data)
		pts_plot(array(v))
		plt.title(d2s('r =',dp(np.corrcoef(v[:,0],v[:,1])[0,1],3)))

		if len(velocity_data) > 5000:
			velocity_data = velocity_data[-2500:]
			
"""
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
"""
