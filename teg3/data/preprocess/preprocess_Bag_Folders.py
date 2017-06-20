from kzpy3.vis import *
import kzpy3.teg3.data.access.Bag_Folder as Bag_Folder




def preprocess_Bag_Folder(bag_folders_path = opjD('runs'),NUM_STATE_ONE_STEPS=30,graphics=True):
	
	bag_folders_paths_list = sorted(gg(opj(bag_folders_path,'*')),key=natural_keys)

	try:
		for bfp in bag_folders_paths_list:

			run_name = bfp.split('/')[-1]

			preprocessed_dir,left_image_bound_to_data_name = get_preprocess_dir_name_info(bfp)

			if len(gg(opj(bfp,preprocessed_dir,'Bag_Folder.pkl'))) == 1:
				print('')
				cprint(opj(run_name,preprocessed_dir,'Bag_Folder.pkl')+' exists, loading it.','yellow','on_red')
				BF = load_obj(opj(bfp,preprocessed_dir,'Bag_Folder.pkl'))
			else:
				BF = Bag_Folder.init(bfp,
					preprocessed_dir=preprocessed_dir,
					left_image_bound_to_data_name=left_image_bound_to_data_name,
					NUM_STATE_ONE_STEPS=NUM_STATE_ONE_STEPS)
				save_obj(BF,opj(bfp,preprocessed_dir,'Bag_Folder.pkl'))

			if graphics:
				figure(run_name+' timecourses')
				plot(BF['data']['raw_timestamps'],100*BF['data']['encoder'],'y')
				plot(BF['data']['raw_timestamps'],BF['data']['state_one_steps'],'bo-')
				plot(BF['data']['good_start_timestamps'],zeros(len(BF['data']['good_start_timestamps']))+100,'go')
				plot(BF['data']['raw_timestamps'],2000*BF['data']['raw_timestamp_deltas'],'r')
				ylim(0,1000)

				figure(run_name+' raw_timestamp_deltas')
				rtd = BF['data']['raw_timestamp_deltas'].copy()
				rtd[rtd>0.08] = 0.08
				hist(rtd)
				#plot(BF['data']['raw_timestamps'],100*BF['data']['state'],'r')
				#plot(BF['data']['raw_timestamps'],100*BF['data']['acc_z'],'r')

				figure(run_name+' scatter')
				plot(BF['data']['steer'][BF['data']['good_start_indicies']],BF['data']['gyro_x'][BF['data']['good_start_indicies']],'o')

				plt.pause(0.001)

	except Exception as e:
		cprint("********** Exception ***********************",'red')
		print(e.message, e.args)			



def get_preprocess_dir_name_info(bfp):
	# Some tiresome checking for which preprocessed data version to use.
	if len(gg(opj(bfp,'.preprocessed2'))) == 1:
		if len(gg(opj(bfp,'.preprocessed2','left_image_bound_to_data.pkl'))) == 1:
			preprocessed_dir = '.preprocessed2'
			left_image_bound_to_data_name = 'left_image_bound_to_data.pkl'		
		else:
			assert(False)
	elif len(gg(opj(bfp,'.preprocessed'))) == 1:
		if len(gg(opj(bfp,'.preprocessed','left_image_bound_to_data.pkl'))) == 1:
			preprocessed_dir = '.preprocessed'
			left_image_bound_to_data_name = 'left_image_bound_to_data.pkl'		
		elif len(gg(opj(bfp,'.preprocessed','left_image_bound_to_data2.pkl'))) == 1:
			preprocessed_dir = '.preprocessed'
			left_image_bound_to_data_name = 'left_image_bound_to_data2.pkl'
		else:
			assert(False)
	else:
		assert(False)
	return preprocessed_dir,left_image_bound_to_data_name
