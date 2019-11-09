from kzpy3.utils3 import *
exec(identify_file_str)
cr(__file__)
cr(pname(__file__))
project_path = pname(__file__).replace(opjh(),'')
if project_path[0] == '/':
    project_path = project_path[1:]
sys_str = d2s('mkdir -p',opj(project_path,'__local__'))
cg(sys_str)
os.system(sys_str)


"""
These need to be updated on bdd4:
# tegra-ubuntu_15Nov18_20h52m26s has to have +32 to motor values.
# cp '/home/karlzipser/Desktop/Data/2_TB_Samsung_n3/rosbags__preprocessed_data/tu_15to16Nov2018/locations/local/left_direct_stop/h5py/tegra-ubuntu_15Nov18_20h52m26s/left_timestamp_metadata_right_ts.h5py' '/home/karlzipser/Desktop/Data/2_TB_Samsung_n3/rosbags__preprocessed_data/tu_15to16Nov2018/locations/local/left_direct_stop/h5py/tegra-ubuntu_15Nov18_20h52m26s/bkp.left_timestamp_metadata_right_ts.h5py'
# copy over fixed left_timestamp_metadata_right_ts file
# python kzpy3/Data_app/make_data_moments_dics.py --locations_path '/home/karlzipser/Desktop/Data/2_TB_Samsung_n3/rosbags__preprocessed_data/tu_15to16Nov2018/locations'
# and copy over fixed data_moments_dic.pkl
"""

P = {}
_ = P
_['project_path'] = project_path
minute = 60
minutes = minute
hour = 60*minute
hours = hour

_['display'] = False
_['num loss_list_avg steps to show'] = None
_['ABORT'] = False
_['customers'] = ['train menu']
_['To Expose'] = {}
_['verbose'] = False
_['loss figure size'] = (3,16)
_['figure size'] = (5,5)
_['loss_timer_time'] = 10*minute
_['print_timer_time'] = 5*minute
_['menu_load_timer_time'] = 10
_['spause_timer_time'] = 10
_['percent_of_loss_list_avg_to_show'] = 100.0
_['cmd/clear_screen'] = False


#_['parameter_file_menu_load_timer_time'] = minute


	#raw_enter(d2n("_['prediction_range'] = ",_['prediction_range'],', len = ',len(_['prediction_range']),', okay? '))
	# array([ 1, 10, 20, 30, 40, 50, 59, 69, 79, 89])
	# len(a) = 10
#_['gray_out_random_value'] = 0.0

_['To Expose']['train menu'] = sorted(_.keys())
to_hide = ['To Expose','customers']
for h in to_hide:
	_['To Expose']['train menu'].remove(h)
for k in _.keys():
	if '!' in k:
		_['To Expose']['train menu'].remove(k)
###############################################################
###############################################################
###############################################################
###############################################################
_['DOING_VALIDATION'] = False
_['full'] = True
#_['VALIDATION_WEIGHTS_FILE_PATH'] = '/home/karlzipser/Desktop/Network_Weights_from_bdd4/Sq120_ldr_output_4April2019/net_01Apr19_00h35m00s.infer'
_['start menu automatically'] = False

_['lacking runs'] = {}
_['freeze premetadata weights'] = False
if _['freeze premetadata weights']:
	cr("\n\n******* _['freeze premetadata weights'] == True *******\n")
	_['update premetadata weights from other model'] = most_recent_file_in_folder(opjD('Networks/net_24Dec2018_12imgs_projections/weights'),['.infer'],[])



_['updated'] = []
_['DISPLAY_EACH'] = False
_['RESUME'] = True
_['BATCH_SIZE'] = 64
_['REQUIRE_ONE'] = []
_['save_net_timer'] = Timer(1000*hours) #i.e., not used now
_['SAVE_FILE_NAME'] = 'net'
_['proportion of experiements to use'] = 1.0
_['proportion of runs to use'] = 1.0 #1/8. #(np.random.random()**2) 
_['start time'] = time_str()
_['start time numeric'] = time.time()
_['max_num_runs_to_open'] = 900
_['min_num_runs_to_open'] = 1
if not _['DOING_VALIDATION']:
	_['run time before quitting'] = 1.5*hours
else:
	_['run time before quitting'] = 5*minutes
_['reload_image_file_timer_time'] =  30*minutes
_['experiments_folders'] = []
_['trigger print timer?'] = True
_['trigger loss_timer?'] = True
###############################################################
#

_['use_LIDAR'] = False
_['lidar_only'] = False
"""
if _['lidar_only']:
	_['GPU'] = 0
elif _['use_LIDAR'] == False:
	_['GPU'] = 0
else:
	_['GPU'] = 1
_['GPU'] = 0
"""

#
###############################################################


                                                        
_['LIDAR_path'] = opjm('1_TB_Samsung_n1','_.Depth_images.log.resize.flip.left_ts')
_['LIDAR_extension'] = ".Depth_image.log.resize.flip.with_left_ts.h5py"
try:
	_['comparison losses'] = [lo(most_recent_file_in_folder(opjD('Networks/Sq40_initial_full_zeroing_and_projections_from_scratch/loss'),['.loss_avg.pkl'],[]))]
	_['comparison losses'] += [lo(most_recent_file_in_folder(opjD('Networks/net_24Dec2018_12imgs_projections/loss'),['.loss_avg.pkl'],[]))]
	_['comparison losses'] += [lo(most_recent_file_in_folder(opjD('Networks/Sq40_rb_zero_from_scratch/loss'),['.loss_avg.pkl'],[]))]
except:
	_['comparison losses'] = []
_['frequency_timer'] = Timer(0.5*minute)
_['duration timer'] = Timer()
_['TRAIN_TIME'] = 60*5.0
_['VAL_TIME'] = 60*1.0
_['LOSS_LIST_N'] = 30
_['run_name_to_run_path'] = {}
_['data_moments_indexed'] = []
_['heading_pause_data_moments_indexed'] = []
_['Loaded_image_files'] = {}
_['data_moments_indexed_loaded'] = []
_['behavioral_modes_no_heading_pause'] = ['direct','follow','furtive','play','left','right']
# note, 'center' is not included in _['behavioral_modes_no_heading_pause'] because 'center' is converted to 'direct' below.
_['behavioral_modes'] = _['behavioral_modes_no_heading_pause']+['heading_pause']
_['current_batch'] = []
if False: # the standard before 15Sept2018
	_['prediction_range'] = range(1,60,6)
elif False:
	_['prediction_range'] = range(1,70,7)
	raw_enter(d2n("_['prediction_range'] = ",_['prediction_range'],', len = ',len(_['prediction_range']),', okay? '))
elif True:
	_['prediction_range'] = arange(1,90,9.8).astype(int)






















#EOF