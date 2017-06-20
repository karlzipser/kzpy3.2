from kzpy3.utils import *
import kzpy3.teg4.data.preprocess.preprocess_Bag_Folders as preprocess_Bag_Folders
import kzpy3.teg4.data.access.Bag_File as Bag_File



def load_Bag_Folders(data_path='/home/karlzipser/Desktop/bair_car_data',ignore=['caffe','play','follow','furtive','local','racing']):

	BagFolder_dic = {}

	BagFolders_weighted = []

	bag_folder_path_list_meta = sorted(gg(opj(data_path,'meta','*')),key=natural_keys)
	bag_folder_path_list_rgb = sorted(gg(opj(data_path,'rgb_1to4','*')),key=natural_keys)

	metas = []
	rgbs = []
	for b in bag_folder_path_list_meta:
		metas.append(fname(b))
	for b in bag_folder_path_list_rgb:
		rgbs.append(fname(b))

	for run_name in metas[:30]:
		print run_name
		if str_contains_one(run_name,ignore):
			continue
		num_bag_files = len(gg(opj(data_path,'rgb_1to4',run_name,'*.bag.pkl')))
		left_image_bound_to_data_name = preprocess_Bag_Folders.get_preprocess_dir_name_info(run_name)
		if len(gg(opj(data_path,'meta',run_name,'Bag_Folder.pkl'))) == 1:
			print('')
			cprint(opj(run_name,'Bag_Folder.pkl')+' exists, loading it.','yellow','on_red')
			BagFolder = load_obj(opj(data_path,'meta',run_name,'Bag_Folder.pkl'))
			for i in range(int(num_bag_files/10)):
				BagFolders_weighted.append(run_name)
		else:
			cprint('Warning, '+opj(run_name,'Bag_Folder.pkl')+' does not exist!','yellow','on_blue')
			continue
		if run_name in BagFolder_dic:
			cprint('Error, '+run_name+' already in BagFolder!','yellow','on_blue')
			assert(False)
		BagFolder_dic[run_name] = BagFolder

	return BagFolder_dic,BagFolders_weighted



def bag_file_loader_thread(thread_id,command_dic,data_path,BagFolder_dic,BagFolders_weighted,delay_before_delete): 
	loaded_bag_files_names = {}
	while True:
		state = command_dic[thread_id]
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
		total_num_bag_files = 0
		for bf in BagFolder_dic.keys():
			cprint(d2s(bf+':',len(BagFolder_dic[bf]['bag_files'])))
			total_num_bag_files += len(BagFolder_dic[bf]['bag_files'])
		cprint(d2s('total_num_bag_files =',total_num_bag_files))
		#print((len(loaded_bag_files_names),total_num_bag_files))
		if len(loaded_bag_files_names) >= 0.9*total_num_bag_files:
			cprint("90% of bag files loaded.")
			time.sleep(10)
		if len(loaded_bag_files_names) > 1000:
			cprint('\n\nTHREAD:: pause before deleting '+bf+'\n\n,,','blue','on_red')
			time.sleep(delay_before_delete)

			played_bagfile_dic_keys = []
			played_bagfile_dic_values = []
			for b in played_bagfile_dic.keys():
				played_bagfile_dic_keys.append(b)
				played_bagfile_dic_values.append(played_bagfile_dic[b])
			indicies = [i[0] for i in sorted(enumerate(played_bagfile_dic_values),key=lambda x:x[1])]
			indicies.reverse()
			ctr = 0
			for i in indicies:
				if ctr >= 25: #ctr >= 0.25*len(indicies): # if ctr >= 25:
					break
				bf = played_bagfile_dic_keys[i]
				if bf in loaded_bag_files_names:
					cprint('THREAD:: deleting '+bf,'blue','on_red')
					r = loaded_bag_files_names[bf]
					loaded_bag_files_names.pop(bf)
					BagFolder = BagFolder_dic[r]
					BagFolder['bag_file_image_data'].pop(bf)
					ctr += 1
		if True: #try:
			run = random.choice(BagFolders_weighted)
			BagFolder = BagFolder_dic[run]
			if type(BagFolder) != dict:
				continue
			dic_keys = ['bag_file_image_data','good_bag_timestamps','binned_timestamps','binned_steers','bid_timestamps']
			for dk in dic_keys:
				if dk not in BagFolder:
					BagFolder[dk] = {}
			if len(BagFolder['bag_file_num_dic']) > 0:
				try:
					bf = fname(random.choice(BagFolder['bag_file_num_dic']))
				except:
					continue
				if bf in BagFolder['bag_file_image_data']:
					continue
				#cprint('bf = ' + bf,'red','on_white')
				bag_file_path = opj(data_path,'rgb_1to4',run,bf)
				#print bag_file_path
				BagFolder['bag_file_image_data'][bf] = Bag_File.load_images(bag_file_path,color_mode="rgb8",include_flip=True)
				loaded_bag_files_names[bf] = run

				bid = BagFolder['bag_file_image_data'][bf]

				bag_left_timestamps = sorted(bid['left'].keys())

				good_bag_timestamps = list(set(BagFolder['data']['good_start_timestamps']) & set(bag_left_timestamps))
				
				binned_timestamps = [[],[]]
				binned_steers = [[],[]]

				for t in good_bag_timestamps:
					steer = BagFolder['left_image_bound_to_data'][t]['steer']
					if steer < 43 or steer > 55:
						binned_timestamps[0].append(t)
						binned_steers[0].append(steer)
					else:
						binned_timestamps[1].append(t)
						binned_steers[1].append(steer)

				BagFolder['good_bag_timestamps'][bf] = good_bag_timestamps
				BagFolder['binned_timestamps'][bf] = binned_timestamps
				BagFolder['binned_steers'][bf] = binned_steers
				BagFolder['bid_timestamps'][bf] = sorted(bid['left'].keys())

		else: #except Exception as e:
			cprint("THREAD:: ********** Exception ***********************",'red')
			print(e.message, e.args)




verbose = False
save_get_data_timer = Timer(60)
def get_data(BF_dic,played_bagfile_dic,used_timestamps,NUM_STATE_ONE_STEPS):
	try:
		data = {}
		r = random.choice(BF_dic.keys())
		BF = BF_dic[r]
		if type(BF) != dict:
			return None
		if 'bag_file_image_data' not in BF:
			#print("""if 'bag_file_image_data' not in BF:""")
			#time.sleep(1)
			return None
		if len(BF['bag_file_image_data']) < 1:
			#print("""if len(BF['bag_file_image_data']) < 1:""")
			#time.sleep(1)
			return None
		bf = a_key(BF['bag_file_image_data'])
		if bf not in BF['good_bag_timestamps']:
			cprint(bf + """ not in BF['good_bag_timestamps']""")
			return None
		if len(BF['good_bag_timestamps'][bf]) < 100:
			if verbose:
				print(d2s('MAIN:: skipping',bf.split('/')[-1],"len(good_bag_timestamps) < 100"))
			return None
		bid = BF['bag_file_image_data'][bf]
		if bf not in played_bagfile_dic:
			played_bagfile_dic[bf] = 0
		played_bagfile_dic[bf] += 1

		if len(BF['binned_timestamps'][bf][0]) > 0 and len(BF['binned_timestamps'][bf][1]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][np.random.randint(2)])
		elif len(BF['binned_timestamps'][bf][0]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][0])
		elif len(BF['binned_timestamps'][bf][1]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][1])
		else:
			return None		

		topics = ['left','right','left_flip','right_flip','steer','motor','state','gyro_x','gyro_y','gyro_z','gyro_yz_mag']
		for tp in topics:
			data[tp] = []

		ts = BF['bid_timestamps'][bf]
		for i in range(len(ts)):
			if ts[i] == rt:
				if len(ts) > i+NUM_STATE_ONE_STEPS:
					if rt not in used_timestamps:
						used_timestamps[rt] = 0
					used_timestamps[rt] += 1
					if False: #save_get_data_timer.check():
						save_obj(played_bagfile_dic,opjD('played_bagfile_dic'))
						save_obj(used_timestamps,opjD('used_timestamps'))
						save_get_data_timer.reset()
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


						data['path'] = r #bf
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
				return None
			for topic in ['steer','motor','gyro_x','gyro_y','gyro_z','gyro_yz_mag','left','right','left_flip','right_flip']:
				if type(data[topic]) != list:
					return None
				if len(data[topic]) != NUM_STATE_ONE_STEPS:
					return None
			
			for topic in ['steer','motor','gyro_x','gyro_y','gyro_z','gyro_yz_mag']:
				for v in data[topic]:
					if not isinstance(v,(int,long,float)):
						return None

			for topic in ['left','right','left_flip','right_flip']:
				for v in data[topic]:
					if not isinstance(v,np.ndarray):
						return None
			
		except:
			return None
 	except Exception as e:
		cprint("********** Exception ***********************",'red')
		print(e.message, e.args)
		return None	
	return data



