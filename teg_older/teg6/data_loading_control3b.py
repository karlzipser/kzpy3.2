from kzpy3.utils import *
import kzpy3.teg4.data.access.Bag_File as Bag_File
import cv2
import threading
from Queue import *

meta_dir = opjD('bair_car_data','meta')
rgb_1to4_dir = opjD('bair_car_data','rgb_1to4')







def get_bag_names_dic(meta_dir,rgb_1to4_dir,to_ignore = ['caffe','home','racing']):

	_,all_run_names = dir_as_dic_and_list(meta_dir)


	run_names_dic = {}
	
	bag_names_dic = {}


	for r in all_run_names:
		if str_contains_one(r,to_ignore):
			cprint("Ignoring "+r,'yellow','on_blue')
		else:
			run_names_dic[r] = None

	for r in run_names_dic:
		p = opj(rgb_1to4_dir,r)
		if len(gg(p)) > 0:
			_,b = dir_as_dic_and_list(p)
			run_names_dic[r] = b
			for f in run_names_dic[r]:
				bag_names_dic[opj(r,f)] = False
		else:
			cprint("Warning: "+p+" does not exist",'red','on_cyan')

	num_bag_files_to_load = 0
	for r in sorted(run_names_dic):
		n = len(run_names_dic[r])
		cprint(d2n('\t',r,': ',n))
		num_bag_files_to_load += n
	cprint(d2s('All runs:',len(all_run_names),'Using runs:',len(run_names_dic)))
	cprint(d2n('Number of bags:',num_bag_files_to_load,', estimated hours = ',dp(num_bag_files_to_load/120.,1)))

	return bag_names_dic







def load_bag_file(bag_names_dic,BagFolder_dic,bag_img_dic,skip_bag_dic,meta_dir,rgb_1to4_dir):
	timer = Timer(10)
	print "load_bag_file !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	while True:
		bn = a_key(bag_names_dic)
		if bn in skip_bag_dic:
			print(d2n('\t',bn,' in skip_bag_dic'))
			continue
		bf = fname(bn)
		if bag_names_dic[bn] == False:
			run_name = bn.split('/')[0]
			if run_name not in BagFolder_dic:
				cprint('Loading '+opj(run_name,'Bag_Folder.pkl'),'yellow','on_red')
				BagFolder_dic[run_name] = load_obj(opj(meta_dir,run_name,'Bag_Folder.pkl'))
			print "load_obj(opj(meta_dir,run_name end"
			bag_img_dic[bn] = Bag_File.load_images(opj(rgb_1to4_dir,bn),color_mode="rgb8",include_flip=True)
			bag_names_dic[bn] == True

			good_bag_timestamps = list(set(BagFolder_dic[run_name]['data']['good_start_timestamps']) & set(bag_img_dic[bn]['left'].keys()))
			if len(good_bag_timestamps) < 100:
				print(d2n('\t',bn,' len(good_bag_timestamps) < 100'))
				skip_bag_dic[bn] = True
				del bag_img_dic[bn]
				del bag_names_dic[bn]
				del BagFolder_dic[run_name]
				continue
			binned_timestamps = [[],[]]
			binned_steers = [[],[]]

			for t in good_bag_timestamps:
				steer = BagFolder_dic[run_name]['left_image_bound_to_data'][t]['steer']
				if steer < 43 or steer > 55:
					binned_timestamps[0].append(t)
					binned_steers[0].append(steer)
				else:
					binned_timestamps[1].append(t)
					binned_steers[1].append(steer)
			dic_keys = ['bag_file_image_data','good_bag_timestamps','binned_timestamps','binned_steers','bid_timestamps']
			for dk in dic_keys:
				if dk not in BagFolder_dic[run_name]:
					BagFolder_dic[run_name][dk] = {}
			BagFolder_dic[run_name]['good_bag_timestamps'][bf] = good_bag_timestamps
			BagFolder_dic[run_name]['binned_timestamps'][bf] = binned_timestamps
			BagFolder_dic[run_name]['binned_steers'][bf] = binned_steers
			BagFolder_dic[run_name]['bid_timestamps'][bf] = sorted(bag_img_dic[bn]['left'].keys())			
			
			#print bn
			
			return

		if timer:
			assert(False)










def get_data_thread(data_package_dic):
	while len(data_package_dic) == 0:
		print "get_data_thread(data_package_dic) waiting to start . . ."
		time.sleep(15)

	timer = Timer(60)	
	while True:
		BagFolder_dic = data_package_dic['BagFolder_dic']
		bag_img_dic = data_package_dic['bag_img_dic']
		data_queue = data_package_dic['data_queue']
		skip_bag_dic = data_package_dic['skip_bag_dic']

		group_binned_timestamps = data_package_dic['group_binned_timestamps']
		NUM_STATE_ONE_STEPS = data_package_dic['NUM_STATE_ONE_STEPS']

		if timer.check():
			timer.reset()
			print(d2s("get_data_thread() is running. data_queue.qsize() =",data_queue.qsize()))
		if data_queue.qsize() < 5 and len(bag_img_dic) > 3:
			data = get_data(BagFolder_dic,bag_img_dic,group_binned_timestamps,skip_bag_dic,NUM_STATE_ONE_STEPS)
			if data != None:
				data_queue.put(data)
		else:
			#time.sleep(0.1)
			pass











def get_data(BagFolder_dic,bag_img_dic,group_binned_timestamps,skip_bag_dic,NUM_STATE_ONE_STEPS):
	#print "get_data"
	try:
		data = {}

		c = random.choice([0,1])
		rt = a_key(group_binned_timestamps[c])
		run_name,bf = group_binned_timestamps[c][rt]
		bn = opj(run_name,bf)

		BF = BagFolder_dic[run_name]

		if type(BF) != dict:
			skip_bag_dic[bn] = True; return None

		if fname(bn) not in BF['good_bag_timestamps']:
			cprint(bf + """ not in BF['good_bag_timestamps']""")
			skip_bag_dic[bn] = True; return None
		if len(BF['good_bag_timestamps'][fname(bn)]) < 100:
			if verbose:
				print(d2s('MAIN:: skipping',bf.split('/')[-1],"len(good_bag_timestamps) < 100"))
			skip_bag_dic[bn] = True; return None

		bid = bag_img_dic[bn]

		if len(BF['binned_timestamps'][bf][0]) > 0 and len(BF['binned_timestamps'][bf][1]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][np.random.randint(2)])
		elif len(BF['binned_timestamps'][bf][0]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][0])
		elif len(BF['binned_timestamps'][bf][1]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][1])
		else:
			skip_bag_dic[bn] = True; return None

		topics = ['left','right','left_flip','right_flip','steer','motor','state','gyro_x','gyro_y','gyro_z','gyro_yz_mag']
		for tp in topics:
			data[tp] = []

		ts = BF['bid_timestamps'][bf]
		for i in range(len(ts)):
			if ts[i] == rt:
				if len(ts) > i+NUM_STATE_ONE_STEPS:

					for j in range(i,i+NUM_STATE_ONE_STEPS):
						t = ts[j]

						steer = BF['left_image_bound_to_data'][t]['steer']
						motor = BF['left_image_bound_to_data'][t]['motor']
						#state = BF['left_image_bound_to_data'][t]['state']
						gyro_x = BF['left_image_bound_to_data'][t]['gyro'][0]
						gyro_y = BF['left_image_bound_to_data'][t]['gyro'][1]
						gyro_z = BF['left_image_bound_to_data'][t]['gyro'][2]
						gyro_yz_mag = np.sqrt(gyro_y**2+gyro_z**2)
						img_left = bid['left'][t]
						right_timestamp = BF['left_image_bound_to_data'][t]['right_image']
						img_right = bid['right'][right_timestamp]

						img_left_flip = bid['left_flip'][t]
						img_right_flip = bid['right_flip'][right_timestamp]


						data['path'] = bn
						data['steer'].append(steer)
						data['motor'].append(motor)
						data['gyro_x'].append(gyro_x)
						data['gyro_y'].append(gyro_y)
						data['gyro_z'].append(gyro_z)
						data['gyro_yz_mag'].append(gyro_yz_mag)
						data['left'].append(img_left)
						data['right'].append(img_right)
						data['left_flip'].append(img_left_flip)
						data['right_flip'].append(img_right_flip)


					break
				else:
					if verbose:
						cprint("MAIN:: ERROR!!!!!!!!! if len(ts) > i+10: failed")

		try:
			if type(data['path']) != str:
				skip_bag_dic[bn] = True; return None
			for topic in ['steer','motor','gyro_x','gyro_y','gyro_z','gyro_yz_mag','left','right','left_flip','right_flip']:
				if type(data[topic]) != list:
					skip_bag_dic[bn] = True; return None
				if len(data[topic]) != NUM_STATE_ONE_STEPS:
					skip_bag_dic[bn] = True; return None
			
			for topic in ['steer','motor','gyro_x','gyro_y','gyro_z','gyro_yz_mag']:
				for v in data[topic]:
					if not isinstance(v,(int,long,float)):
						skip_bag_dic[bn] = True; return None

			for topic in ['left','right','left_flip','right_flip']:
				for v in data[topic]:
					if not isinstance(v,np.ndarray):
						skip_bag_dic[bn] = True; return None
			
		except:
			skip_bag_dic[bn] = True; return None
 	except Exception as e:
		cprint("********** Exception ***********************",'red')
		print(e.message, e.args)
		skip_bag_dic[bn] = True; return None
		
	return data












def visualize_data(data,dt=33,image_only=False):
	if not image_only:
		figure('steer motor gyro_yz_mag')
		clf()
		#plt.subplot(1,3,3)
		plot((array(data['steer'])-49)/100.,'r')
		plot((array(data['motor'])-49)/100,'g')
		plot((array(data['gyro_yz_mag'])/200.),'b')
		ylim(-0.5,0.5)
		pause(0.00001)
	for i in range(len(data['right'])):
		#mi(d['right'][i],'right')
		#pause(0.00000001)
		cv2.imshow('right',cv2.cvtColor(data['left'][i],cv2.COLOR_RGB2BGR))
		if cv2.waitKey(dt) & 0xFF == ord('q'):
			pass






		









def load_data_into_model_thread(data_package_dic):
	while len(data_package_dic) == 0:
		print "load_data_into_model_thread(data_package_dic) waiting to start . . ."
		time.sleep(15)

	timer = Timer(60)
	while True:
		#print(d2n("load_data_into_model_thread() is running.)"))
		version = data_package_dic['version']
		data_queue = data_package_dic['data_queue']
		solver_ready_queue = data_package_dic['solver_ready_queue']
		solver_waiting_queue = data_package_dic['solver_waiting_queue']
		#print "HERE!"
		try:
			if timer.check():
				timer.reset()
				print(d2n("load_data_into_model_thread() is running. solver_ready_queue.qsize() = ",
					solver_ready_queue.qsize(),", solver_waiting_queue.qsize() = ",solver_waiting_queue.qsize()))

			if solver_ready_queue.qsize() < 5 and data_queue.qsize() > 0 and solver_waiting_queue.qsize() > 0:
				#print "load_data_into_model_thread"
				if np.random.random() > 0.5:
					flip = False
				else:
					flip = True
				data = data_queue.get()
				solver = solver_waiting_queue.get()
				result = False
				while result == False:
					#print 'while result == False:'
					result = load_data_into_model(solver,version,data,flip,False,True)
				solver_ready_queue.put(solver)
				#print(d2s('data_queue size =',data_queue.qsize() ))
				#print(d2s('solver_ready_queue size =',solver_ready_queue.qsize() ))
				#print(d2s('solver_waiting_queue size =',solver_waiting_queue.qsize() ))
			else:
				#time.sleep(0.1)
				pass
	 	except Exception as e:
			cprint("********** Exception ***********************",'red')
			print(e.message, e.args)















import caffe
USE_GPU = True
gpu = 1
if USE_GPU:
	caffe.set_device(gpu)
	caffe.set_mode_gpu()
from kzpy3.caf6.Caffe_Net import *
solver_file_path = opjh("kzpy3/caf6/z2_color/solver_"+str(gpu)+"_a.prototxt")
version = 'version 1b'
weights_file_mode = None #'most recent' #'this one'  #None #'most recent'
#weights_file_path = '/home/karlzipser/Desktop/z2_color_continue_training_of_12_19_2016/z2_color_iter_11700000.caffemodel' # None #opjD('z2_color')
weights_file_path = None #'/home/karlzipser/Desktop/z2_color' # None #opjD('z2_color')

caffe_net = Caffe_Net(solver_file_path,version,weights_file_mode,weights_file_path,False)














def load_data_package_thread(num_bag_files_to_load,bag_names_dic,data_package_dic_queue):
	timer = Timer(1)
	while True:
		if timer.check():
			print "HERE!!!!!!!!!!!!!!!!!!!!"
		try:
			if timer.check():
				timer.reset()
				print(d2n("load_data_package_thread() is running. data_package_dic_queue.qsize() = ",
					data_package_dic_queue.qsize()))

			if True: #data_package_dic_queue.qsize() < 1000/num_bag_files_to_load:
				p = load_data_package(num_bag_files_to_load,bag_names_dic)
				data_package_dic_queue.put(p)
			else:
				time.sleep(0.1)
				pass
		except Exception as e:
			cprint("********** Exception ***********************",'red')
			print(e.message, e.args)











def load_data_package(num_bag_files_to_load,bag_names_dic):
	print "1  HERE!!!!!!!!!!!!!!!!!!!!"
	data_queue = Queue()
	solver_waiting_queue = Queue()
	solver_ready_queue = Queue()
	for i in range(10):
		solver_waiting_queue.put(setup_solver(solver_file_path))

	skip_bag_dic = {}
	timing_data = []
	BagFolder_dic = {}
	bag_img_dic = {}
	bag_viewed_counter_dic = {}


	t0=time.time()
	for i in range(num_bag_files_to_load):
		print i
		load_bag_file(bag_names_dic,BagFolder_dic,bag_img_dic,skip_bag_dic,meta_dir,rgb_1to4_dir)


	group_binned_timestamps = {}
	group_binned_timestamps[0] = {}
	group_binned_timestamps[1] = {}
	for r in BagFolder_dic.keys():
		if 'binned_timestamps' in BagFolder_dic[r]:
			for bf in BagFolder_dic[r]['binned_timestamps'].keys():
				#for bn in bag_img_dic.keys():
				bf = fname(bf)
				binned_timestamps = BagFolder_dic[r]['binned_timestamps'][bf]
				for i in range(2):
					for j in range(len(binned_timestamps[i])):
						group_binned_timestamps[i][binned_timestamps[i][j]] = (r,bf)
	t1=time.time()
	load_time = t1-t0
	print(d2s('load_time =',load_time))
	print "2  HERE!!!!!!!!!!!!!!!!!!!!"
	data_package_dic = {}
	data_package_dic['data_queue'] = data_queue
	data_package_dic['solver_waiting_queue'] = solver_waiting_queue
	data_package_dic['solver_ready_queue'] = solver_ready_queue
	data_package_dic['skip_bag_dic'] = skip_bag_dic
	data_package_dic['timing_data'] = timing_data
	data_package_dic['BagFolder_dic'] = BagFolder_dic
	data_package_dic['bag_img_dic'] = bag_img_dic
	data_package_dic['bag_viewed_counter_dic'] = bag_viewed_counter_dic
	data_package_dic['group_binned_timestamps'] = group_binned_timestamps
	data_package_dic['version'] = version
	data_package_dic['NUM_STATE_ONE_STEPS'] = NUM_STATE_ONE_STEPS
	print "3  HERE!!!!!!!!!!!!!!!!!!!!"
	return data_package_dic









bag_names_dic = get_bag_names_dic(meta_dir,rgb_1to4_dir)


verbose = False
num_bag_files_to_load = 100
NUM_STATE_ONE_STEPS = 30
global_timer = Timer(60*60*24*2)


#16.8 GiB







ctr = 0


data_package_dic_queue = Queue()

Data_Package_Dic = {}


threading.Thread(target=load_data_package_thread,args=(num_bag_files_to_load,bag_names_dic,data_package_dic_queue)).start()
threading.Thread(target=get_data_thread,args=(Data_Package_Dic,)).start()
threading.Thread(target=load_data_into_model_thread,args=(Data_Package_Dic,)).start()









t0 = time.time()
timer = Timer(5)
data_package_timer = Timer(120)
data_package_dic = None
while True:

	if data_package_dic_queue.qsize() > 0:
		if data_package_dic == None or data_package_timer.check():
			data_package_timer.reset()
			data_package_dic = data_package_dic_queue.get()
			for k in data_package_dic.keys():
				Data_Package_Dic[k] = data_package_dic[k]
			t0 = time.time()
			ctr = 0
		while data_package_timer.check() == False:
			if timer.check():
				timer.reset()
				dt = time.time()-t0
				cprint(d2s("ctr =",ctr,"dt =",dt,"Rate =",(ctr/(dt),"Hz")),'blue','on_yellow')
				print d2s("data_package_dic_queue.qsize() =", data_package_dic_queue.qsize())
			if 'solver_ready_queue' in Data_Package_Dic:
				if Data_Package_Dic['solver_ready_queue'].qsize() > 0:
					s = Data_Package_Dic['solver_ready_queue'].get()
					caffe_net.train_step(s)
					Data_Package_Dic['solver_waiting_queue'].put(s)
					ctr += 1
	else:
		time.sleep(0.1)
	



print "done."



