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

cg("To start menu:\n\tpython kzpy3/Menu_app/menu2.py path",project_path,"dic P")



minute = 60
minutes = minute
hour = 60*minute
hours = hour



P = {}
P['Data_moment list temp'] =[]
P['ABORT'] = False
P['customers'] = ['train menu']
P['To Expose'] = {}

P['verbose'] = False
verbose = P['verbose']

P['loss_timer_time'] = 10*minute
P['print_timer_time'] = 1*minute
P['menu_load_timer_time'] = 10
P['spause_timer_time'] = 10

P['cmd/clear_screen'] = False

#P['parameter_file_menu_load_timer_time'] = minute
P['percent_of_loss_list_avg_to_show'] = 10.0


P['reload_image_file_timer_time'] = 30*minutes

P['DISPLAY_EACH'] = False
	#raw_enter(d2n("P['prediction_range'] = ",P['prediction_range'],', len = ',len(P['prediction_range']),', okay? '))
	# array([ 1, 10, 20, 30, 40, 50, 59, 69, 79, 89])
	# len(a) = 10
#P['gray_out_random_value'] = 0.0
P['start menu automatically'] = False
P['To Expose']['train menu'] = sorted(P.keys())
to_hide = ['To Expose','customers']
for h in to_hide:
	P['To Expose']['train menu'].remove(h)
for k in P.keys():
	if '!' in k:
		P['To Expose']['train menu'].remove(k)
###############################################################
###############################################################
###############################################################
###############################################################
P['lacking runs'] = {}



P['updated'] = []


P['BATCH_SIZE'] = 64
P['REQUIRE_ONE'] = []
P['save_net_timer'] = Timer(30*minute)
P['SAVE_FILE_NAME'] = 'net'
P['proportion of experiements to use'] = 1.0
P['proportion of runs to use'] = 1.0 #1/8. #(np.random.random()**2) 
P['start time'] = time_str()
P['start time numeric'] = time.time()
P['max_num_runs_to_open'] = 900
P['min_num_runs_to_open'] = 1
P['run time before quitting'] = 0.5*hour
P['experiments_folders'] = []
P['trigger print timer?'] = False
P['trigger loss_timer?'] = True
###############################################################
#
P['use_LIDAR'] = False
P['lidar_only'] = False
if P['lidar_only']:
	P['GPU'] = 0
elif P['use_LIDAR'] == False:
	P['GPU'] = 0
else:
	P['GPU'] = 1
P['GPU'] = 0
#
###############################################################
if P['lidar_only']:
	P['NETWORK_OUTPUT_FOLDER'] = opjD('Networks','net_15Sept2018_1Nov_with_reverse_14Nov_with_only_LIDAR') #
elif P['use_LIDAR']:
	P['NETWORK_OUTPUT_FOLDER'] = opjD('Networks','net_15Sept2018_1Nov_with_reverse_14Nov_with_LIDAR') #
else:
	#P['NETWORK_OUTPUT_FOLDER'] = opjD('Networks','net_15Sept2018_1Nov_with_reverse_') #
	#P['NETWORK_OUTPUT_FOLDER'] = opjD('Networks','net_15Sept2018_1Nov_with_reverse_with_12imgs') #
    P['NETWORK_OUTPUT_FOLDER'] = opjD('Networks','net_24Dec2018_12imgs_projections')
    
P['LIDAR_path'] = opjm('1_TB_Samsung_n1','_.Depth_images.log.resize.flip.left_ts')
P['LIDAR_extension'] = ".Depth_image.log.resize.flip.with_left_ts.h5py"

P['frequency_timer'] = Timer(0.5*minute)
P['duration timer'] = Timer()
P['TRAIN_TIME'] = 60*5.0
P['VAL_TIME'] = 60*1.0
P['RESUME'] = True
if P['RESUME']:
    P['INITIAL_WEIGHTS_FOLDER'] = opj(P['NETWORK_OUTPUT_FOLDER'],'weights')
    P['WEIGHTS_FILE_PATH'] = most_recent_file_in_folder(P['INITIAL_WEIGHTS_FOLDER'],['net'],[])
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
if False: # the standard before 15Sept2018
	P['prediction_range'] = range(1,60,6)
elif False:
	P['prediction_range'] = range(1,70,7)
	raw_enter(d2n("P['prediction_range'] = ",P['prediction_range'],', len = ',len(P['prediction_range']),', okay? '))
elif True:
	P['prediction_range'] = arange(1,90,9.8).astype(int)












####################### MENU ################################
#
if P['start menu automatically'] and using_linux():
    dic_name = "P"
    sys_str = d2n("gnome-terminal  --geometry 40x30+100+200 -x python kzpy3/Menu_app/menu2.py path ",project_path," dic ",dic_name)
    cr(sys_str)
    os.system(sys_str)


P['updated']

def load_parameters(P,customer='train menu'):
    if P['menu_load_timer'].check():
        Topics = menu2.load_Topics(project_path,first_load=False,customer=customer)
        if type(Topics) == dict:
            P['updated this load'] = []
            for t in Topics['To Expose']['train menu']:
                if t in Arguments:
                    topic_warning(t)
                if '!' in t:
                    pass
                else:
                    if P[t] == Topics[t]:
                        pass
                    else:
                        P[t] = Topics[t]
                        P['updated this load'].append(t)
                        P['updated'].append(t)
            if len(P['updated this load']) > 0:
                P['updated this load'] = list(set(P['updated this load']))
                P['updated'] = list(set(P['updated']))
                cg("Updated parameter this load:\n\t",P['updated this load'])
                cb("Updated parameter:\n\t",P['updated'])
        P['menu_load_timer'].reset()

# 
##############################################################










#EOF