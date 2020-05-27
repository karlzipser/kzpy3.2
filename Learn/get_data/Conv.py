from kzpy3.vis3 import *
exec(identify_file_str)

# python kzpy3/drafts/Sq7/main.py --RESUME 1 --NET_TYPE ConDecon_test2 --NET_TYPE_SUFFIX 84x47
#WIDTH,HEIGHT = 168/2,94/2

#from kzpy3.Learn.get_data.runs import All_runs

from runs import All_runs

def setup(P):



    Runs = {}

    activation_folders = sggo(opjD('Data', 'Activations_folders','*'))
    
    for a in activation_folders:
        files = sggo(a,'indicies','*.h5py')
        E = h5r(files[0])
        if P['type'][1] in ' '.join(E.keys()):
            aruns = sggo(a,'indicies','*.h5py')
        E.close()

    _Runs = {}
    for r in aruns:
        run = fname(r).split('.')[0]
        if run in All_runs[P['runs']]:
            if os.path.getsize(r) > 0:
                if time.time() - os.path.getmtime(r) > 60:
                    _Runs[run] = opjh(r)

    Run_coder = {}

    run_ctr = 0

    good_list = []


    for r in _Runs.keys():

        Run_coder[run_ctr] = r

        H = find_files_recursively(opjD('Data'),r,DIRS_ONLY=True)

        if len(H['paths']) == 0:
            cr(r,'not found.')
            continue
        else:
            cg(r,'found.')

        Runs[r] = {
            'original_timestamp_data':{},
            'flip_images':{},
            'left_timestamp_metadata_right_ts':{},
        }
        
        Runs[r]['original_timestamp_data'] = \
            {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'original_timestamp_data.h5py'),'data':None}

        Runs[r]['flip_images'] = \
            {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'flip_images.h5py'),'data':None}

        Runs[r]['left_timestamp_metadata_right_ts'] = \
            {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'left_timestamp_metadata_right_ts.h5py'),'data':None}

        Runs[r]['button_number'] = None
        Runs[r]['encoder'] = None

        for k in Runs[r].keys():
            if k not in ['button_number','encoder']:
                if Runs[r][k]['data'] == None:
                    Runs[r][k]['data'] = h5r(Runs[r][k]['path'])
        for kk in ['button_number','encoder']:
            if Runs[r][kk] == None:
                Runs[r][kk] = Runs[r]['left_timestamp_metadata_right_ts']['data'][kk][:]

        length = len(Runs[r]['original_timestamp_data']['data']['left_image']['vals'])
        for i in range(length):
            if Runs[r]['button_number'][i] != 4 and Runs[r]['encoder'][i] > 0.1:
                good_list.append((run_ctr,i))

        run_ctr += 1
        

    P['Runs'] = Runs
    P['good_list'] = good_list
    P['Run_coder'] = Run_coder

###############

input_data_plus = None
target_data_plus = None


Toggle = Toggler()
global_ctr = 0


def _selector(P):
    global global_ctr
    R = P['runtime_parameters']
    Runs = P['Runs']
    good = P['good_list'][rndint(len(P['good_list']))]
    r, ctr = P['Run_coder'][good[0]], good[1]
    flip = rndint(2)

    if R['data_from_run'] != 'no':
        assert(type(R['data_from_run']) == str)
        r = R['data_from_run']

    if R['data_from_ctr'] > -1:
        if Toggle['test'](R['ctr_reset']):
            ctr = R['data_from_ctr']
            global_ctr = ctr
        else:
            global_ctr += R['step']
            if global_ctr >= len(Runs[r]['original_timestamp_data']['data']['left_image']['vals']):
                global_ctr = R['data_from_ctr']
            ctr = global_ctr

    if ctr > len(Runs[r]['original_timestamp_data']['data']['left_image']['vals']) - 300:
        r,ctr,flip = _selector(P)

    if R['data_from_flip'] > -1:
        assert(type(R['data_from_flip']) == int)
        assert(R['data_from_flip'] in [0,1])
        flip = R['data_from_flip']

    return r,ctr,flip



def get_data_function(P):

    global input_data_plus, target_data_plus

    Runs = P['Runs']

    


    while True:
        
        if True:#try:
            r,ctr,flip = _selector(P)



            flip = 0
            

            Lists = {'input':[],'target':[]}

            if not flip:
                B = Runs[r]['original_timestamp_data']['data']['left_image']['vals']
            else:
                assert(False)
                B = Runs[r]['flip_images']['data']['left_image_flip']['vals']
            if ctr >= len(B):
                continue



            for k in ['input']:

                if 'rgb' in P[k]:
                    noise =0
                    if P['noise'] > 0:
                        noise = P['noise']*rnd(shape(B[ctr]))-P['noise']/2.
                    Lists[k].append(B[ctr+P[k+'_offset']]+noise)
                    if rnd() < P['drop'] and k == 'input':
                        Lists[k][-1] *= 0
                    if k == 'input' and 'rgb.noise' in P:
                        if P['rgb.noise'] > 0:
                            noise = P['rgb.noise'] * rnd(shape(C[ctr])) - P['rgb.noise']/2.
                            noise = cv2.resize(noise,(168,94))
                            Lists[k][-1] = Lists[k][-1]*1.0 + noise
                    if 'drop.rgb' in P and rnd() < P['drop.rgb'] and k == 'input':
                        Lists[k][-1] *= 0




                if 'button' in P[k]:
                    img = zeros((P['width'],P['height'],3))
                    bn = int(Runs[r]['button_number'][ctr+P[k+'_offset']])
                    if 'blue_center_button' in P:
                        if bn == 1:
                            bn = 1
                        elif bn == 2:
                            bn = 3
                        elif bn == 3:
                            bn = 2
                    if 'original_Fire3_scaling' not in P:
                        if bn in (1,2,3):
                            img[:,:,bn-1] = 255        
                        img[0,0,:] = 255
                    else:
                        if bn in (1,2,3):
                            img[:,:,bn-1] = 1
                    Lists[k].append(img)
                    if rnd() < P['drop'] and k == 'input':
                        Lists[k][-1] *= 0


            img = B[ctr+P[k+'_offset']]
            line = img[94/2,:,0]
            temp = img.copy()
            for a in range(94):
                for b in range(3):
                    temp[a,:,b] = line
            Lists['target'].append(temp.transpose(2,1,0))
            #Lists['target'].append(line)


                    
            break
        

        

    P['ctr'] = ctr

    for k in ['input']:#sorted(Lists.keys()):
        lst = Lists[k]
        for l in rlen(lst):
            e = lst[l]
            e = e.astype(float)
            if P['width'] and P['height']:
                e = cv2.resize( e,(P['width'],P['height']))
            e = e.transpose(2,1,0)
            lst[l] = e

    Concats = {}
    for k in ['input','target']:#sorted(Lists.keys()):
        lst = Lists[k]
        for l in rlen(lst):
            if k not in Concats:
                Concats[k] = lst[l]
            else:
                Concats[k] = np.concatenate((Concats[k],lst[l]))


    Data = {
        'input':Concats['input'],
        'target':line,#Concats['target'],
        'ctr':ctr,
    }
    #print(shape(Data['input']))
    #print(shape(Data['target']))

    return Data




#EOF
