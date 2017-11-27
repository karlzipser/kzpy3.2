from Names_Module import *
from kzpy3.utils2 import *
exec(identify_file_str)

P = {}

P['EXPERIMENT_FOLDERS'] = sggo('/home/karlzipser/Desktop/all_aruco_ready','*')
P['data_moments_indexed'] = []
P['all_image_file_paths'] = []
P['all_flip_image_file_paths'] = []

for p in P['EXPERIMENT_FOLDERS']:
	P['data_moments_indexed'] += lo(opj(p,'data_moments_indexed.pkl'))
	for r in sggo(p,'h5py','*'):
		P['all_image_file_paths'].append(opj(r,'original_timestamp_data.h5py'))
		P['all_flip_image_file_paths'].append(opj(r,'flip_images.h5py'))



P[GPU] = 0
P[BATCH_SIZE] = 512
P[DISPLAY] = True
P[VERBOSE] = True
P[LOAD_ARUCO] = False
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

#if 'Aruco_Steering_Trajectories' not in P:
#	P['Aruco_Steering_Trajectories'] = lo(opj(P[BAIR_CAR_DATA_PATH],'Aruco_Steering_Trajectories'))


#EOF