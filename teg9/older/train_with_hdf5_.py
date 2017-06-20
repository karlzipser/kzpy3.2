
from kzpy3.utils import *
import kzpy3.teg9.get_data_with_hdf5 as get_data_with_hdf5
import threading

import caffe

gpu = 1
if gpu >= 0:
	caffe.set_device(gpu)
	caffe.set_mode_gpu()

import kzpy3.caf8.zn_color.solver as Solver

model_path = Solver.model_path

weights_file_path =  most_recent_file_in_folder(opjD(fname(model_path)))
weights_file_path = None

if weights_file_path:
	print(d2s("Copying weights from",weights_file_path,"to",Solver.solver))
	Solver.solver.net.copy_from(weights_file_path)
else:
	print(d2s("No weights loaded to",Solver.solver))




bair_car_data_path = opjD('bair_car_data_new') # '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'#opjD('bair_car_data_new')
hdf5_runs_path = opj(bair_car_data_path,'hdf5/runs')
hdf5_segment_metadata_path = opj(bair_car_data_path,'hdf5/segment_metadata')

N_FRAMES = 10 # how many timesteps with images.
N_STEPS = 40 # how many timestamps with non-image data
ignore = ['reject_run','left','out1_in2'] # runs with these labels are ignored
require_one = ['direct'] # at least one of this type of run lable is required
use_states = [1,5,6,7]

print_timer = Timer(5)
loss10000 = []
loss = []
rate_timer_interval = 10.
rate_timer = Timer(rate_timer_interval)
rate_ctr = 0
figure('steer',figsize=(3,2))
figure('loss',figsize=(3,2))



get_data_with_hdf5.load_Segment_Data(hdf5_segment_metadata_path,hdf5_runs_path)



print('\nloading low_steer... (takes awhile)')
low_steer = load_obj(opj(bair_car_data_path,'hdf5/segment_metadata/low_steer'))
print('\nloading high_steer... (takes awhile)')
high_steer = load_obj(opj(bair_car_data_path,'hdf5/segment_metadata/high_steer'))
len_high_steer = len(high_steer)
len_low_steer = len(low_steer)
figure('high low steer histograms',figsize=(2,1))
clf()
plt.hist(array(low_steer)[:,2],bins=range(0,100))
plt.hist(array(high_steer)[:,2],bins=range(0,100))
figure(1)
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
		
	if random.random() < len_high_steer/(len_low_steer+len_high_steer+0.0): # with some probability choose a low_steer element
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



def array_to_int_list(a):
	l = []
	for d in a:
		l.append(int(d*100))
	return l




data_lst = []

os.environ['DATA_TO_LIST'] = 'TRUE'

def data_thread(data_lst):
	#lock = threading.Lock()
	start_t = time.time()
	remind_timer = Timer(10)
	print(d2s("Starting data_thread start_t =",start_t)) 
	while os.environ['DATA_TO_LIST'] == 'TRUE':
		if remind_timer.check():
			print(d2s("Continuing data_thread start_t =",start_t))
			remind_timer.reset()
		batch = []
		t0 = time.time()
		for b in range(Solver.batch_size):
			data = None
			while data == None:
				data = get_data_considering_high_low_steer()
			batch.append(data)
		t1 = time.time()
		#print(d2s("rate =",Solver.batch_size/(t1-t0),"Hz, len(data_lst) =",len(data_lst)," for data_thread start_t =",start_t))
		#lock.acquire()
		data_lst.append([time.time(),batch])
		#lock.release()
	print(d2s("Exiting data_thread start_t =",start_t))

threading.Thread(target=data_thread,args=[data_lst]).start()

"""
#lock = threading.Lock()
ctr = 0
while len(data_lst) < 100000:
	#print(d2s("len(data_lst) =",)
	if len(data_lst) > 2:
		#lock.acquire()
		if ctr < len(data_lst):
			print(len(data_lst),ctr,len(data_lst)*Solver.batch_size/(data_lst[-1][0]-data_lst[0][0]))
			data = data_lst[ctr][1]
			data_lst[ctr][1] = time.time()
			ctr += 1
			time.sleep(0.5)

		#lock.release()
		#time.sleep(5)
"""

def stop():
	os.environ['DATA_TO_LIST'] = 'FALSE'

#stop()

#while False:
ctr = 0
while True: #len(data_lst) < 100000:
	print 1
	#print(d2s("len(data_lst) =",)
	if len(data_lst) > 2:
		print 2
		#lock.acquire()
		if ctr < len(data_lst):
			print 3
			print(len(data_lst),ctr,len(data_lst)*Solver.batch_size/(data_lst[-1][0]-data_lst[0][0]))
			batch = data_lst[ctr][1]
			data_lst[ctr][1] = time.time()
			ctr += 1
			print 4
			for b in range(Solver.batch_size):
				print b
				print 5
				"""
				data = None
				while data == None:
					data = get_data_considering_high_low_steer()
				"""
				mcia(batch[b]['left'])
				Solver.put_data_into_model(batch[b],Solver.solver,b)
			print 6
			Solver.solver.step(1)
			print("Solver.solver.step(1)")
			# The training step. Everything below is for display.
			rate_ctr += 1
			if rate_timer.check():
				print(d2s('rate =',dp(rate_ctr/rate_timer_interval,2),'Hz'))
				rate_timer.reset()
				rate_ctr = 0
			a = Solver.solver.net.blobs['steer_motor_target_data'].data[0,:] - Solver.solver.net.blobs['ip2'].data[0,:]
			loss.append(np.sqrt(a * a).mean())
			if len(loss) >= 10000/Solver.batch_size:
				loss10000.append(array(loss[-10000:]).mean())
				loss = []
				figure('loss');clf()
				lm = min(len(loss10000),100)
				plot(loss10000[-lm:])
				print(d2s('loss10000 =',loss10000[-1]))
			if print_timer.check():
				print(Solver.solver.net.blobs['metadata'].data[0,:,5,5])
				cprint(array_to_int_list(Solver.solver.net.blobs['steer_motor_target_data'].data[0,:][:]),'green','on_red')
				cprint(array_to_int_list(Solver.solver.net.blobs['ip2'].data[0,:][:]),'red','on_green')
				figure('steer')
				clf()
				ylim(-1.05,1.05);xlim(0,10)
				t = Solver.solver.net.blobs['steer_motor_target_data'].data[0,:]
				print(shape(Solver.solver.net.blobs['steer_motor_target_data'].data))
				print Solver.solver.net.blobs['steer_motor_target_data'].data[-1,:]
				print Solver.solver.net.blobs['ip2'].data[-1,:]
				o = Solver.solver.net.blobs['ip2'].data[-1,:]
				steer_ip2 = o[0:10]-o[10:20]
				steer_tar = t[0:10]-t[10:20]
				#plot(zeros(xlen+1)+49,'k');
				plot(steer_ip2,'g'); plot(steer_tar,'r'); plt.title(data['name']);pause(0.001)
				mi_or_cv2_animate(data['left'],delay=33)
				print_timer.reset()





