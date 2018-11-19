from kzpy3.utils3 import *
exec(identify_file_str)

P = {}
P['ABORT'] = False
P['verbose'] = False
verbose = P['verbose']
################################################################
#
P['use_LIDAR'] = True
P['lidar_only'] = True
if P['lidar_only']:
	P['GPU'] = 0
elif P['use_LIDAR'] == False:
	P['GPU'] = 0
else:
	P['GPU'] = 1
#
################################################################

P['LIDAR_path'] = opjm('1_TB_Samsung_n1','_.Depth_images.log.resize.flip.left_ts')
P['LIDAR_extension'] = ".Depth_image.log.resize.flip.with_left_ts.h5py"

P['start time'] = time_str()
P['start time numeric'] = time.time()

P['max_num_runs_to_open'] = 300

P['experiments_folders'] = []

P['To Expose'] = {}
P['To Expose']['Train'] = ['print_timer_time','parameter_file_load_timer_time','percent_of_loss_list_avg_to_show']

P['BATCH_SIZE'] = 64
P['REQUIRE_ONE'] = []

if P['lidar_only']:
	P['NETWORK_OUTPUT_FOLDER'] = opjD('net_15Sept2018_1Nov_with_reverse_14Nov_with_only_LIDAR') #
elif P['use_LIDAR']:
	P['NETWORK_OUTPUT_FOLDER'] = opjD('net_15Sept2018_1Nov_with_reverse_14Nov_with_LIDAR') #
else:
	P['NETWORK_OUTPUT_FOLDER'] = opjD('net_15Sept2018_1Nov_with_reverse_') #
P['save_net_timer'] = Timer(60*30)
P['SAVE_FILE_NAME'] = 'net'
P['print_timer_time'] = 60
P['parameter_file_load_timer_time'] = 5
P['percent_of_loss_list_avg_to_show'] = 10.0
P['frequency_timer'] = Timer(30.0)
P['TRAIN_TIME'] = 60*5.0
P['VAL_TIME'] = 60*1.0
P['RESUME'] = True
if P['RESUME']:
    P['INITIAL_WEIGHTS_FOLDER'] = opj(P['NETWORK_OUTPUT_FOLDER'],'weights')
    P['WEIGHTS_FILE_PATH'] = most_recent_file_in_folder(P['INITIAL_WEIGHTS_FOLDER'],['net'],[])

P['reload_image_file_timer_time'] = 5*60
P['loss_timer'] = Timer(60*10/10)
P['LOSS_LIST_N'] = 30
P['run_name_to_run_path'] = {}
P['data_moments_indexed'] = []
P['heading_pause_data_moments_indexed'] = []
P['Loaded_image_files'] = {}
P['data_moments_indexed_loaded'] = []
P['behavioral_modes_no_heading_pause'] = ['direct','follow','furtive','play','left','right']
# note, 'center' is not included in P['behavioral_modes_no_heading_pause'] because 'center' is converted to 'direct' below.
P['behavioral_modes'] = P['behavioral_modes_no_heading_pause']+['heading_pause']
P['current_batch'] = []
P['DISPLAY_EACH'] = False
if False: # the standard before 15Sept2018
	P['prediction_range'] = range(1,60,6)
elif False:
	P['prediction_range'] = range(1,70,7)
	raw_enter(d2n("P['prediction_range'] = ",P['prediction_range'],', len = ',len(P['prediction_range']),', okay? '))
elif True:
	P['prediction_range'] = arange(1,90,9.8).astype(int)
	#raw_enter(d2n("P['prediction_range'] = ",P['prediction_range'],', len = ',len(P['prediction_range']),', okay? '))
	# array([ 1, 10, 20, 30, 40, 50, 59, 69, 79, 89])
	# len(a) = 10
#P['gray_out_random_value'] = 0.0

P['lacking runs'] = {}






#EOF