

from Names_Module import *
from utils2 import *
exec(identify_file_str)


P = {}
P['data_moments_indexed'] =  lo('/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo/data_moments_indexed_1.pkl')
P['data_moments_indexed'] += lo('/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo/data_moments_indexed_2.pkl')
P['data_moments_indexed'] += lo('/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo/heading_pause_data_moments_indexed.pkl')

P['data_moments_indexed'] += lo('/home/karlzipser/Desktop/bdd_car_data_14Sept2017_whole_room/data_moments_indexed.pkl')
P['data_moments_indexed'] += lo('/home/karlzipser/Desktop/bdd_car_data_14Sept2017_whole_room/heading_pause_data_moments_indexed.pkl')

P['data_moments_indexed'] += lo('/home/karlzipser/Desktop/bdd_car_data_14Sept2017_circle/data_moments_indexed.pkl')
P['data_moments_indexed'] += lo('/home/karlzipser/Desktop/bdd_car_data_14Sept2017_circle/heading_pause_data_moments_indexed.pkl')

P['data_moments_indexed'] += lo('/home/karlzipser/Desktop/bdd_car_data_15Sept2017_circle/data_moments_indexed.pkl')
P['data_moments_indexed'] += lo('/home/karlzipser/Desktop/bdd_car_data_15Sept2017_circle/heading_pause_data_moments_indexed.pkl')

P['data_moments_indexed'] += lo('/home/karlzipser/Desktop/bdd_car_data_23Sept2017_circle11/data_moments_indexed.pkl')
P['data_moments_indexed'] += lo('/home/karlzipser/Desktop/bdd_car_data_23Sept2017_circle11/heading_pause_data_moments_indexed.pkl')




P[GPU] = 1
P[BATCH_SIZE] = 512
P[DISPLAY] = True
P[VERBOSE] = True
P[LOAD_ARUCO] = False
P[BAIR_CAR_DATA_PATH] = opjD('bdd_car_data_Sept2017_aruco_demo')
P[CODE_PATH] = CODE_PATH__
P[IGNORE] = [reject_run,left,out1_in2]#,'Smyth','racing','local','Tilden','campus']
P[REQUIRE_ONE] = []
P[USE_STATES] = [1,3,5,6,7]
P[N_FRAMES] = 2
P[N_STEPS] = 10
P[STRIDE] = 9#3 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
P[NETWORK_OUTPUT_FOLDER] = opjD('net_indoors')
P[SAVE_FILE_NAME] = 'net'
P[save_net_timer] = Timer(60*5)
P[print_timer] = Timer(4)
P[TRAIN_TIME] = 60*10.0
P[VAL_TIME] = 60*1.0
P[RESUME] = True
if RESUME:
    P[INITIAL_WEIGHTS_FOLDER] = opj(P[NETWORK_OUTPUT_FOLDER],'weights')
    P[WEIGHTS_FILE_PATH] = most_recent_file_in_folder(P[INITIAL_WEIGHTS_FOLDER],['net'],[])

All_image_files = {}
folders5 = sgg('/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo/h5py/*')
random.shuffle(folders5)
open_runs_ctr = 0
for f in folders5:
	if open_runs_ctr > 350:
		break
	print fname(f)
	All_image_files[fname(f)] = {}
	if True:
		try:
			O = h5r(opj(f,'original_timestamp_data.h5py'))
			F = h5r(opj(f,'flip_images.h5py'))
			All_image_files[fname(f)]['normal'] = O
			All_image_files[fname(f)]['flip'] = F
			open_runs_ctr += 1
		except Exception as e:
			print("********** Exception ***********************")
			print(e.message, e.args)	
P['All_image_files'] = All_image_files

#EOF