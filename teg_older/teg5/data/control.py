from kzpy3.vis import *
import kzpy3.teg5.data.access_bag_files as access_bag_files
import threading



loaded_bag_files_names = {}
played_bagfile_dic = {}
used_timestamps = {}

data_path = '/home/karlzipser/Desktop/bair_car_data'
NUM_STATE_ONE_STEPS = 30

ignore_most=['August','sidewalks','campus','caffe','play','follow','furtive','local']

BagFolder_dic,BagFolders_weighted = access_bag_files.load_Bag_Folders(data_path,ignore=['caffe','racing'])

thread_id = 'loader_thread'
command_dic = {}
command_dic[thread_id] = 'start' #  command_dic[thread_id] = 'pause' # command_dic[thread_id] = 'stop'
delay_before_delete = 5*60

threading.Thread(target=access_bag_files.bag_file_loader_thread,
	args=(thread_id,command_dic,data_path,BagFolder_dic,BagFolders_weighted,delay_before_delete,loaded_bag_files_names,played_bagfile_dic)).start()

data_list = []

thread_id = 'get data thread'
command_dic[thread_id] = 'start'
def get_data_thread(BagFolder_dic,played_bagfile_dic,used_timestamps,NUM_STATE_ONE_STEPS):
	global data_list
	timer = Timer(1./300.)
	while True:
		#time.sleep(1)
		state = command_dic[thread_id]
		command = command_dic[thread_id]
		if command == 'pause':
			if state == 'pause':
				pass
			else:
				state = 'pause'
				cprint(d2s('Pausing thread ',thread_id),'yellow','on_blue')
			#time.sleep(1)
			continue
		if command == 'start' and state == 'pause':
			state = 'running'
			cprint(d2s('Unpausing thread ',thread_id),'yellow','on_blue')			
		if command == 'stop':
			cprint(d2s('Stopping thread ',thread_id),'yellow','on_blue')
			return
		data = access_bag_files.get_data(BagFolder_dic,played_bagfile_dic,used_timestamps,NUM_STATE_ONE_STEPS)
		try:
			if data != None:
				#print type(data['right_flip'][-1])
				#time.sleep(1)
				data_list.append(data)
				#print((len(data_list),len(data_list[-1])))
				#print(d2s("motor",data_list[-1]['motor'][-1]))
		except:
			pass #print 'error'
		if len(data_list) > 5:
			data_list = data_list[-5:]
		while not timer.check():
			time.sleep(1./30000.)
		timer.reset()

wait_delay = 120
cprint(d2s('Waiting',wait_delay,'seconds to let data thread load a lot of data.'))
time.sleep(wait_delay)
threading.Thread(target=get_data_thread,args=(BagFolder_dic,played_bagfile_dic,used_timestamps,NUM_STATE_ONE_STEPS)).start()
time.sleep(5)



import caffe
USE_GPU = True
if USE_GPU:
	caffe.set_device(0)
	caffe.set_mode_gpu()
from kzpy3.caf5.Caffe_Net import *
solver_file_path = opjh("kzpy3/caf5/z2_color/solver.prototxt")
version = 'version 1b'
weights_file_mode = None #'most recent'
weights_file_path = None #opjD('z2_color')
caffe_net = Caffe_Net(solver_file_path,version,weights_file_mode,weights_file_path,False)



if True:

	#print 'here 1'
	while True:
		try:
			#print 'here 2'
			data = data_list[-1]
		except Exception as e:
			cprint("********** Exception ***********************",'red')
			print(e.message, e.args)
		if data != None:
			#print data['path']
			#time.sleep(1)
			#print 'here 3'
			caffe_net.train_step(data)
			#print 'here 4'
		else:
			print "data == None"


def plot_loss1000(paths='/home/karlzipser/Desktop/loss1000.pkl',max_num_points=100000):
	if type(paths) != list:
		paths = [paths]
	l = []
	for path in paths:
		l = l + list(load_obj(path))
	if len(l) > max_num_points:
		l = l[:max_num_points]
	plot(l,'.')
	x,d = sequential_means(l,100)
	plot(x,d,'ro-')

def plot_loss_comparison(max_num_points=2000):
	figure('loss')
	clf()
	plot_loss1000('/home/karlzipser/Desktop/z2_color_trained_12_15_2016/_loss1000.pkl',max_num_points)
	plot_loss1000('/home/karlzipser/Desktop/loss1000.pkl',max_num_points)

"""
from kzpy3.caf5.Caffe_Net import *

def caffe_net_thread(thread_id,solver_file_path,version,weights_file_mode,weights_file_path,command_dic,gpu_num):
	caffe.set_device(gpu_num)
	caffe.set_mode_gpu()
	caffe_net = Caffe_Net(solver_file_path,version,weights_file_mode,weights_file_path)
	cprint(d2s('Starting thread ',thread_id),'yellow','on_blue')
	state = command_dic[thread_id]
	while True:
		command = command_dic[thread_id]
		if command == 'pause':
			if state == 'pause':
				pass
			else:
				state = 'pause'
				cprint(d2s('Pausing thread ',thread_id),'yellow','on_blue')
			time.sleep(1)
			continue
		if command == 'start' and state == 'pause':
			state = 'running'
			cprint(d2s('Unpausing thread ',thread_id),'yellow','on_blue')			
		if command == 'stop':
			cprint(d2s('Stopping thread ',thread_id),'yellow','on_blue')
			return
		try:
			data = data_list[-(1+gpu_num)]
		except Exception as e:
			cprint("********** Exception ***********************",'red')
			print(e.message, e.args)			
		if data != None:
			caffe_net.train_step(data)


if False:
	for gpu_num in range(2):
		thread_id = d2s('caffe net',gpu_num)
		solver_file_path = opjh(d2n("kzpy3/caf5/z2_color/solver",gpu_num,".prototxt"))
		version = 'version 1'
		weights_file_mode = 'most recent'
		weights_file_path = opjD('z2_color')
		command_dic = {}
		command_dic[thread_id] = 'start' # command_dic[thread_id] = 'stop'
		threading.Thread(target=caffe_net_thread,args=(thread_id,solver_file_path,version,weights_file_mode,weights_file_path,command_dic,gpu_num)).start()


"""
pass

