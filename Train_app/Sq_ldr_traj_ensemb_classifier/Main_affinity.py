from kzpy3.vis3 import *
import default_values
import Batch_Module
import Network_Module
import kzpy3.Menu_app.menu2 as menu2

exec(identify_file_str)

_ = default_values.P

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

Network = Network_Module.Pytorch_Network(_)

Batch = Batch_Module.Batch(_,the_network=Network)

cr("\n\nTime needed for startup =",int(startup_timer.time()),"seconds.\n\n")
del startup_timer


menu_reminder = Timer(10*60)
menu_reminder.trigger()
timer = Timer(_['run time before quitting'])

files = sggo('/home/karlzipser/Desktop/Data/Network_Predictions_projected/*.net_projections.h5py')
Files = {}
for f in files:
    name = fname(f).split('.')[0]
    Files[name] = h5r(f)['normal']

blank_meta = np.zeros((23,41,3),np.uint8)





cluster_list = lo(Arguments['cluster_list'])


if 'prune' in Arguments:
    cl = []
    for c in cluster_list:
        if len(c) > Arguments['prune']:
            cl.append(c)
    cluster_list = cl

count_timer = Timer(30)
save_timer = Timer(60*1)



affinity = zeros((1024,1024))

i_time = Timer()
while _['ABORT'] == False:

    other_name = a_key(Files)
    other_index = np.random.randint(len(Files[other_name]))

    other_img = Files[other_name][other_index].copy()
    the_img = other_img

    other_img = the_img.copy()

    cluster_found = False

    

    for i in range(len(cluster_list)):

        cg(i,int(i_time.time()),'s')

        c = cluster_list[i]
        C = c[0]
        ref_name = C['name']
        ref_index = C['index']
        ref_img = Files[ref_name][ref_index].copy()
        the_img = ref_img

        ref_img = the_img.copy()

        for j in range(len(cluster_list)):
            #cb(i,j)
            #cr(A)
            #if j in A[i]:
            #    cm(0)
            #    continue
            #if j in A:
            #    if i in A[j]:
            #        cm(1)
            #        continue

            _c = cluster_list[j]
            _C = _c[0]
            _ref_name = _C['name']
            _ref_index = _C['index']
            _ref_img = Files[_ref_name][_ref_index].copy()
            _the_img = _ref_img
            _ref_img = _the_img.copy()
            Batch['CLEAR']()

            Batch['FILL'](
                ref_name,
                ref_index,
                ref_img,
                _ref_name,
                _ref_index,
                _ref_img,       
            )

            value = Batch['FORWARD']()

            affinity[i][j] = value
            #if i != j:
            #    affinity[j][i] = value

        if save_timer.check():
            save_timer.reset()
            so(opjD('affinity'),affinity)

    """
    if count_timer.check():
        count_timer.reset()
        counts = []
        total = 0
        for c in cluster_list:
            counts.append(len(c))
            total += len(c)-1
        cb(total/(1.0*len(cluster_list)),total)
        figure('counts');clf();plot(counts,'.');spause()
    """


# Start training with 12 mini metadata images at 9am 12Dec2018

 


#EOF