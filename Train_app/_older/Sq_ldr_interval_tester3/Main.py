from kzpy3.utils3 import *
import default_values
import Batch_Module
import Network_Module
import kzpy3.Menu_app.menu2 as menu2

exec(identify_file_str)

_ = default_values.P

if 'run' in Arguments:
    _['the run name'] = Arguments['run']

####################### MENU ################################
#
def load_parameters(_,customer='train menu'):
    if _['menu_load_timer'].check():
        Topics = menu2.load_Topics(_['project_path'],first_load=False,customer=customer)
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

Timer_updates = {
    'print_timer_time':'print_timer',
    'loss_timer_time':'loss_timer',
    'spause_timer_time':'spause_timer',
    'reload_image_file_timer_time':'reload_image_file_timer',
    'menu_load_timer_time':'menu_load_timer',
}

startup_timer = Timer()

for a in Arguments.keys():
    _[a] = Arguments[a]
print_Arguments()

_['print_timer'] = Timer(_['print_timer_time'])
_['loss_timer'] = Timer(_['loss_timer_time'])
_['menu_load_timer'] = Timer(_['menu_load_timer_time'])
_['spause_timer'] = Timer(_['spause_timer_time'])
if _['trigger print timer?']:
    _['print_timer'].trigger()
_['reload_image_file_timer'] = Timer(_['reload_image_file_timer_time'])
if _['trigger loss_timer?']:
    _['loss_timer'].trigger()

_['NETWORK_OUTPUT_FOLDER'] = opjD('Networks',fname(_['project_path']))
if _['RESUME']:
    _['INITIAL_WEIGHTS_FOLDER'] = opj(_['NETWORK_OUTPUT_FOLDER'],'weights')
    _['WEIGHTS_FILE_PATH'] = most_recent_file_in_folder(_['INITIAL_WEIGHTS_FOLDER'],['.infer'],[])
else:
    cr("\n*********** STARTING FROM RANDOM WEIGHTS ***********\n")
    raw_enter()



#for r in Batch_Module.GOOD_LIST:

Network = Network_Module.Pytorch_Network(_)

Batch = Batch_Module.Batch(_,the_network=Network)

cr("\n\nTime needed for startup =",int(startup_timer.time()),"seconds.\n\n")
#del startup_timer


menu_reminder = Timer(10*60)
menu_reminder.trigger()
timer = Timer(_['run time before quitting'])

_['ABORT'] = False
#_['the run name'] = r
cb("*** using run",_['the run name'],'***',ra=0)

if True:#try:
    while _['ABORT'] == False:

        ##################################
        #
        load_parameters(_,customer='train menu')

        for u in Timer_updates.keys():
            if u in _['updated']:
                _[Timer_updates[u]] = Timer(_[u])
                _['updated'].remove(u)
        #
        ##################################

        if timer.check():
            cg("\n\nQuitting after runing for",timer.time(),"seconds.\n\n")
            _['save_net_timer'].trigger()
            Network['SAVE_NET']()
            break

        Batch['CLEAR']()

        Batch['FILL']()

        Batch['FORWARD']()

        #Batch['ACCUMULATE_RESULTS']()

        Batch['DISPLAY']()

        if False:
            ###############################
            #
            import kzpy3.Cars.n26Dec18.nodes.network_utils.camera as camera
            Q2 = camera.Quartet('camera from Quartet')
            Q2['from_torch'](Network['net'].A['camera_input'])
            Q2['display'](
                delay_blank=1000,
                delay_prev=1000,
                delay_now=1000)    
            #
            ###############################

        #Batch['BACKWARD']()
        """
        else:#except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)    
        """   

    # Start training with 12 mini metadata images at 9am 12Dec2018

        menu_reminder.message(d2s("\n\nTo start menu:\n\tpython kzpy3/Menu_app/menu2.py path",_['project_path'],"dic P\n\n"))

    #cg('here',ra=True)
    Q = {
        'LDR values':_['LDR values'],
        'the run name':_['the run name'],
        'LDR ref index':_['LDR ref index'],
        }

    so(opjD(_['the ref run name']+'__interval_tests__ref_index_'+str(_['LDR ref index'])+'__'+_['the run name']),Q)
    #cb('here',ra=True)
    



#EOF