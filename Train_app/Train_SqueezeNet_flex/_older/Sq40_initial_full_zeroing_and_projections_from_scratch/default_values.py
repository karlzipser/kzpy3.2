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

minute = 60
minutes = minute
hour = 60*minute
hours = hour

P = {}
_ = P
_['display'] = False
_['project_path'] = project_path
_['num loss_list_avg steps to show'] = None
_['ABORT'] = False
_['customers'] = ['train menu']
_['To Expose'] = {}
_['verbose'] = False
_['loss figure size'] = (3,16)
_['figure size'] = (5,5)
_['loss_timer_time'] = 10*minute
_['print_timer_time'] = 10*minute
_['menu_load_timer_time'] = 10
_['spause_timer_time'] = 10
_['cmd/clear_screen'] = False
_['percent_of_loss_list_avg_to_show'] = 99.0
_['To Expose']['train menu'] = sorted(_.keys())
to_hide = ['To Expose','customers']
for h in to_hide:
	_['To Expose']['train menu'].remove(h)
for k in _.keys():
	if '!' in k:
		_['To Expose']['train menu'].remove(k)
###
###############################################################
###############################################################
###
_['reload_image_file_timer_time'] = 35*minutes
_['start menu automatically'] = False
_['lacking runs'] = {}
_['freeze premetadata weights'] = False
if ['freeze premetadata weights']:
	_['update premetadata weights from other model'] = \
	most_recent_file_in_folder( \
		opjD('Networks/net_24Dec2018_12imgs_projections/weights'),['.infer'],[])
_['updated'] = []
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
_['run time before quitting'] = 0.5*hour
_['experiments_folders'] = []
_['trigger print timer?'] = True
_['trigger loss_timer?'] = True
_['GPU'] = 0
_['LIDAR_path'] = opjm('1_TB_Samsung_n1','_.Depth_images.log.resize.flip.left_ts')
_['LIDAR_extension'] = ".Depth_image.log.resize.flip.with_left_ts.h5py"
_['comparison losses'] = [lo(most_recent_file_in_folder(opjD('Networks/Sq40_initial_full_zeroing_and_projections/loss'),['.loss_avg.pkl'],[]))]
_['comparison losses'] += [lo(most_recent_file_in_folder(opjD('Networks/net_24Dec2018_12imgs_projections/loss'),['.loss_avg.pkl'],[]))]
_['frequency_timer'] = Timer(0.5*minute)
_['duration timer'] = Timer()
_['TRAIN_TIME'] = 60*5.0
_['VAL_TIME'] = 60*1.0
_['DISPLAY_EACH'] = False
_['LOSS_LIST_N'] = 30
_['run_name_to_run_path'] = {}
_['data_moments_indexed'] = []
_['heading_pause_data_moments_indexed'] = []
_['Loaded_image_files'] = {}
_['data_moments_indexed_loaded'] = []
_['behavioral_modes_no_heading_pause'] = ['direct','follow','furtive','play','left','right']
_['behavioral_modes'] = _['behavioral_modes_no_heading_pause']+['heading_pause']
_['current_batch'] = []
_['use_LIDAR'] = False
_['lidar_only'] = False
if False: # the standard before 15Sept2018
	_['prediction_range'] = range(1,60,6)
elif False:
	_['prediction_range'] = range(1,70,7)
	raw_enter(d2n("_['prediction_range'] = ",_['prediction_range'],', len = ',len(_['prediction_range']),', okay? '))
elif True:
	_['prediction_range'] = arange(1,90,9.8).astype(int)






















#EOF