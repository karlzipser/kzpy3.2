from kzpy3.vis2 import *
from kzpy3.vis import mi_or_cv2_animate
import kzpy3.teg9.data.utils.get_data_with_hdf5 as get_data_with_hdf5


REPO = 'kzpy3'
TEG = 'teg9'
CAF = 'caf8'
DISPLAY = True

#################################################
#
import caffe 
if True:
	MODEL = 'z2_color'
	print(MODEL)
	bair_car_data_path = opjD('bair_car_data_Main_Dataset')
	weights_file_path =  most_recent_file_in_folder(opjD(MODEL),['caffemodel'])
	#weights_file_path = opjh('caffe_models/z2_color.caffemodel')
	N_FRAMES = 2
	N_STEPS = 10
	gpu = 1
if gpu >= 0:
	caffe.set_device(gpu)
	caffe.set_mode_gpu()
import_str = "import REPO.CAF.MODEL.solver as Solver"
import_str = import_str.replace("REPO",REPO)
import_str = import_str.replace("CAF",CAF)
import_str = import_str.replace("MODEL",MODEL)
exec(import_str)

if weights_file_path:
	print(d2s("Copying weights from",weights_file_path,"to",Solver.solver))
	Solver.solver.net.copy_from(weights_file_path)
else:
	print(d2s("No weights loaded to",Solver.solver))

#
##################################################



ignore = ['reject_run','left','out1_in2']#,'Smyth','racing','local','Tilden','campus']
require_one = []
use_states = [1,3,5,6,7]
rate_timer_interval = 5.
print_timer = Timer(5)

hdf5_runs_path = opj(bair_car_data_path,'hdf5/runs')
hdf5_segment_metadata_path = opj(bair_car_data_path,'hdf5/segment_metadata')

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

ctr_low = -1
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












if DISPLAY:
	figure('high low steer histograms',figsize=(2,1))
	histogram_plot_there = True
	clf()
	plt.hist(array(low_steer)[:,2],bins=range(0,100))
	plt.hist(array(high_steer)[:,2],bins=range(0,100))
	figure(1)



while True:

	for b in range(Solver.batch_size): #######################
		_data = None
		while _data == None:
			_data = get_data_considering_high_low_steer()
		data = _data


	##################################################
	#
		Solver.put_data_into_model(data,Solver.solver,b)

	Solver.solver.step(1)
	#
	##################################################



	rate_ctr += 1
	if rate_timer.check():
		print(d2s('rate =',dp(rate_ctr/rate_timer_interval,2),'Hz'))
		rate_timer.reset()
		rate_ctr = 0





########################################################
#
	if print_timer.check():
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
		if DISPLAY:
			fctr = 0
			mi_or_cv2_animate(data['left'],delay=33);pause(0.001)

		print_timer.reset()
#
##########################################################
	

			
