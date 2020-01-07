from kzpy3.utils3 import *
import default_values
import Batch_Module
import Network_Module
import kzpy3.Menu_app.menu2 as menu2

exec(identify_file_str)

_ = default_values.P

_['INDEX'] = 0
_['RUN'] = ''
_['LENGTHS'] = {}
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
kprint(Arguments,'Arguments')

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

Network = Network_Module.Pytorch_Network(_)

Batch = Batch_Module.Batch(_,the_network=Network)

cr("\n\nTime needed for startup =",int(startup_timer.time()),"seconds.\n\n")
del startup_timer


menu_reminder = Timer(10*60)
menu_reminder.trigger()
timer = Timer(_['run time before quitting'])
short_timer = Timer(_['short timer time'])

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

    if short_timer.check() or _['short timer time'] < short_timer.time():
        short_timer = Timer(_['short timer time'])
        Network['SAVE_NET'](temp=True)
        
    Batch['CLEAR']()

    Batch['FILL']()

    Batch['FORWARD']()

    Batch['DISPLAY']()

    #Batch['BACKWARD']()
    print _['INDEX'],_['LENGTHS'][_['RUN']]
    if _['INDEX'] >= _['LENGTHS'][_['RUN']]:
        break
    

# Start training with 12 mini metadata images at 9am 12Dec2018

    menu_reminder.message(d2s("\n\nTo start menu:\n\tpython kzpy3/Menu_app/menu2.py path",_['project_path'],"dic P\n\n"))




    



#EOF