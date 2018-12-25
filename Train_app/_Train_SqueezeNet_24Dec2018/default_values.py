from kzpy3.utils3 import *
import kzpy3.Menu_app.menu2 as menu2
exec(identify_file_str)
cr(__file__)
cr(pname(__file__))
project_path = pname(__file__).replace(opjh(),'')
if project_path[0] == '/':
    project_path = project_path[1:]
sys_str = d2s('mkdir -p',opj(project_path,'__local__'))
cg(sys_str)
os.system(sys_str)

cg("To start menu:\n\tpython kzpy3/Menu_app/menu2.py path",project_path,"dic _")



minute = 60
minutes = minute
hour = 60*minute
hours = hour


P = {}
_=P
_['Data_moment list temp'] =[]
_['ABORT'] = False
_['customers'] = ['train menu']
_['To Expose'] = {}

_['verbose'] = False
verbose = _['verbose']

_['loss_timer_time'] = 10*minute
_['print_timer_time'] = hour
_['menu_load_timer_time'] = 10
_['spause_timer_time'] = 10

_['cmd/clear_screen'] = False

#_['parameter_file_menu_load_timer_time'] = minute
_['percent_of_loss_list_avg_to_show'] = 10.0


_['reload_image_file_timer_time'] = 30*minutes

_['DISPLAY_EACH'] = False
	#raw_enter(d2n("_['prediction_range'] = ",_['prediction_range'],', len = ',len(_['prediction_range']),', okay? '))
	# array([ 1, 10, 20, 30, 40, 50, 59, 69, 79, 89])
	# len(a) = 10
#_['gray_out_random_value'] = 0.0
_['start menu automatically'] = False
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
_['lacking runs'] = {}



_['updated'] = []


_['BATCH_SIZE'] = 64
_['REQUIRE_ONE'] = []
_['save_net_timer'] = Timer(30*minute)
_['SAVE_FILE_NAME'] = 'net'
_['proportion of experiements to use'] = 1.0
_['proportion of runs to use'] = 1.0 #1/8. #(np.random.random()**2) 
_['start time'] = time_str()
_['start time numeric'] = time.time()
_['max_num_runs_to_open'] = 900
_['min_num_runs_to_open'] = 1
_['run time before quitting'] = 0.5*hour
_['experiments_folders'] = []
_['trigger print timer?'] = False
_['trigger loss_timer?'] = True
###############################################################
#
_['use_LIDAR'] = False
_['lidar_only'] = False
if _['lidar_only']:
	_['GPU'] = 0
elif _['use_LIDAR'] == False:
	_['GPU'] = 0
else:
	_['GPU'] = 1
_['GPU'] = 0
#
###############################################################
if _['lidar_only']:
	_['NETWORK_OUTPUT_FOLDER'] = opjD('Networks','net_15Sept2018_1Nov_with_reverse_14Nov_with_only_LIDAR') #
elif _['use_LIDAR']:
	_['NETWORK_OUTPUT_FOLDER'] = opjD('Networks','net_15Sept2018_1Nov_with_reverse_14Nov_with_LIDAR') #
else:
	_['NETWORK_OUTPUT_FOLDER'] = opjD('Networks','net_15Sept2018_1Nov_with_reverse_') #
	_['NETWORK_OUTPUT_FOLDER'] = opjD('Networks','net_15Sept2018_1Nov_with_reverse_with_12imgs') #
_['LIDAR_path'] = opjm('1_TB_Samsung_n1','_.Depth_images.log.resize.flip.left_ts')
_['LIDAR_extension'] = ".Depth_image.log.resize.flip.with_left_ts.h5py"

_['frequency_timer'] = Timer(0.5*minute)
_['duration timer'] = Timer()
_['TRAIN_TIME'] = 60*5.0
_['VAL_TIME'] = 60*1.0
_['RESUME'] = True
if _['RESUME']:
    _['INITIAL_WEIGHTS_FOLDER'] = opj(_['NETWORK_OUTPUT_FOLDER'],'weights')
    _['WEIGHTS_FILE_PATH'] = most_recent_file_in_folder(_['INITIAL_WEIGHTS_FOLDER'],['net'],[])
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












####################### MENU ################################
#
if _['start menu automatically'] and using_linux():
    dic_name = "_"
    sys_str = d2n("gnome-terminal  --geometry 40x30+100+200 -x python kzpy3/Menu_app/menu2.py path ",project_path," dic ",dic_name)
    cr(sys_str)
    os.system(sys_str)


_['updated']

def load_parameters(_,customer='train menu'):
    if _['menu_load_timer'].check():
        Topics = menu2.load_Topics(project_path,first_load=False,customer=customer)
        if type(Topics) == dict:
            _['updated this load'] = []
            for t in Topics['To Expose']['train menu']:
                if t in Arguments:
                    topic_warning(t)
                if '!' in t:
                    pass
                else:
                    if _[t] == Topics[t]:
                        pass
                    else:
                        _[t] = Topics[t]
                        _['updated this load'].append(t)
                        _['updated'].append(t)
            if len(_['updated this load']) > 0:
                _['updated this load'] = list(set(_['updated this load']))
                _['updated'] = list(set(_['updated']))
                cg("Updated parameter this load:\n\t",_['updated this load'])
                cb("Updated parameter:\n\t",_['updated'])
        _['menu_load_timer'].reset()

# 
##############################################################










#EOF