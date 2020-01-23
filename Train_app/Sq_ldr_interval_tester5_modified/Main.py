from kzpy3.vis3 import *
import default_values
import Batch_Module
import Network_Module
import kzpy3.Menu_app.menu2 as menu2
exec(identify_file_str)

_ = default_values.P

# python kzpy3/Train_app/Sq_ldr_interval_tester5/Main.py cluster_list ~/Desktop/cluster_list_25_1st_pass.pkl threshold 0.25

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


def get_cleaned_cluster_list(c):
    #c=loD('cluster_list_25_1st_pass.pkl')
    C = {}
    for i in rlen(c):
        for j in rlen(c[i]):
            D = c[i][j]
            t = (D['name'],D['index'])
            if t not in C:
                C[t] = [i]
            else:
                C[t].append(i)
        #C[t] = list(set(C[t]))
        #cg(C[t],ra=0)

    cleaned = []
    for i in range(1024):
        cleaned.append([])

    
    for t in C.keys():
        indicies = C[t]
        choice = np.random.choice(indicies)
        cleaned[choice].append({'index':t[1],'name':t[0]})

    clens = []
    for d in cleaned:
        clens.append(len(d))
    figure('hist')
    hist(clens)
    cg(np.median(clens),ra=1)
    CA()
    return cleaned
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

Network = Network_Module.Pytorch_Network(_)

Batch = Batch_Module.Batch(_,the_network=Network)

cr("\n\nTime needed for startup =",int(startup_timer.time()),"seconds.\n\n")
del startup_timer


menu_reminder = Timer(10*60)
menu_reminder.trigger()
timer = Timer(_['run time before quitting'])
"""
files = sggo('/home/karlzipser/Desktop/Data/Network_Predictions_projected/*.net_projections.h5py')
Files = {}
for f in files:
    name = fname(f).split('.')[0]
    Files[name] = h5r(f)['normal']
"""
blank_meta = np.zeros((23,41,3),np.uint8)

"""
if 'threshold' not in Arguments:
    Arguments['threshold'] = 0.25


if 'cluster_list' not in Arguments:
    seed_name = a_key(Files)
    seed_index = np.random.randint(len(Files[seed_name]))
    C = {
        'name':seed_name,
        'index':seed_index,
    }
    cluster_list = [
        [C],
    ]
    Arguments['cluster_list'] = d2n(opjD('cluster_list_',Arguments['threshold'],'.pkl'))
else:
    cluster_list = lo(Arguments['cluster_list'])

#cluster_list = get_cleaned_cluster_list(cluster_list)

if 'prune' in Arguments:
    cl = []
    for c in cluster_list:
        if len(c) > Arguments['prune']:
            cl.append(c)
    cluster_list = cl

count_timer = Timer(60)
save_timer = Timer(60*5)
"""

def get_similarity(            
    ref_img,
    other_img,
    show=True,
): 

    #other_img = Files[other_name][other_index].copy()
    the_img = other_img
    blank_meta[:,:,0] = the_img[:,:,1]
    blank_meta[:,:,1] = the_img[:,:,0]
    blank_meta[:,:,2] = the_img[:,:,2]
    other_img = the_img.copy()

    #ref_img = Files[ref_name][ref_index].copy()
    the_img = ref_img
    blank_meta[:,:,0] = the_img[:,:,1]
    blank_meta[:,:,1] = the_img[:,:,0]
    blank_meta[:,:,2] = the_img[:,:,2]
    ref_img = the_img.copy()

    Batch['CLEAR']()

    Batch['FILL'](
        'ref_name',
        0,
        ref_img,
        'other_name',
        0,
        other_img,       
    )

    value = Batch['FORWARD']()
    if show:
        mi(ref_img,'ref_run')
        mi(other_img,'other_run')
        spause()
    return value

#EOF