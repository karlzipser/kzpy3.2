from kzpy3.vis3 import *
exec(identify_file_str)

# python kzpy3/drafts/Sq7/main.py --RESUME 1 --NET_TYPE ConDecon_test2 --NET_TYPE_SUFFIX 84x47


WIDTH,HEIGHT = 168/2,94/2



from runs import All_runs

def setup(P):
    
    """
    from runs import *
    if P['runs'] == 'train':
        runs = train_runs
    elif P['runs'] == 'validate':
        runs = val_runs
    """
    runs = All_runs[P['runs']]
    
    Runs = {}

    Run_coder = {}

    run_ctr = 0

    good_list = []

    for r in runs:

        Run_coder[run_ctr] = r

        H = find_files_recursively(opjD('Data'),r,DIRS_ONLY=True)

        Runs[r] = {
            'original_timestamp_data':{},
            'flip_images':{},
            'left_timestamp_metadata_right_ts':{},
            'net_projections':{},
        }


        Runs[r]['original_timestamp_data'] = \
            {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'original_timestamp_data.h5py'),'data':None}

        Runs[r]['flip_images'] = \
            {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'flip_images.h5py'),'data':None}

        Runs[r]['left_timestamp_metadata_right_ts'] = \
            {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'left_timestamp_metadata_right_ts.h5py'),'data':None}

        Runs[r]['net_projections'] = \
            {'path':opj(opjD('Data'),'Network_Predictions_projected',r+'.net_projections.h5py'),'data':None}

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

    #P['X'] = X
    P['Runs'] = Runs
    P['good_list'] = good_list
    P['Run_coder'] = Run_coder


###############
n = 5
input_data_plus = zeros((3,2*n+WIDTH,2*n+HEIGHT))#+0.5
target_data_plus = zeros((3,2*n+WIDTH,2*n+HEIGHT))+0.5

WWWW = Toggler()
global_ctr = 0

def _selector(P):
    global global_ctr
    R = P['runtime_parameters']
    Runs = P['Runs']
    #X = P['X']
    #kprint(R,'R')
    good = P['good_list'][rndint(len(P['good_list']))]
    r, ctr = P['Run_coder'][good[0]], good[1]
    flip = rndint(2)

    if R['data_from_run'] != 'no':
        assert(type(R['data_from_run']) == str)
        r = R['data_from_run']

    if R['data_from_ctr'] > -1:
        if WWWW['test'](R['ctr_reset']):
            ctr = R['data_from_ctr']
            global_ctr = ctr
        else:
            global_ctr += R['step']
            if global_ctr >= len(Runs[r]['original_timestamp_data']['data']['left_image']['vals']):
                global_ctr = R['data_from_ctr']
            ctr = global_ctr

    if R['data_from_flip'] > -1:
        assert(type(R['data_from_flip']) == int)
        assert(R['data_from_flip'] in [0,1])
        flip = R['data_from_flip']
    else:
        flip = 0

    #print ctr
    return r,ctr,flip




def get_data_function(P):
    #global global_ctr
    #R = P['runtime_parameters']
    Runs = P['Runs']
    #X = P['X']
    #kprint(R,'R')
    r,ctr,flip = _selector(P)
    if False:
        good = P['good_list'][rndint(len(P['good_list']))]
        r, ctr = P['Run_coder'][good[0]], good[1]
        good = P['good_list'][rndint(len(P['good_list']))]
        r, ctr = P['Run_coder'][good[0]], good[1]
        flip = rndint(2)

    if not flip:
        A = Runs[r]['net_projections']['data']['normal']
        B = Runs[r]['original_timestamp_data']['data']['left_image']['vals']
    else:
        A = Runs[r]['net_projections']['data']['flip']
        B = Runs[r]['flip_images']['data']['left_image_flip']['vals']

    ###############
    input_data =  A[ctr]
    temp = A[ctr]
    if flip:
        input_data[:,:,0] = temp[:,:,1]
        input_data[:,:,1] = temp[:,:,0]
    target_data = B[ctr]

    if False:
        if WIDTH == 41:
            target_data = cv2.resize(target_data ,(WIDTH,HEIGHT)).transpose(2,1,0)
            input_data =  input_data.transpose(2,1,0)
        else:
            input_data = cv2.resize(input_data ,(WIDTH,HEIGHT)).transpose(2,1,0)
            target_data =  target_data.transpose(2,1,0)

    input_data = cv2.resize(input_data ,(WIDTH,HEIGHT)).transpose(2,1,0)
    target_data = cv2.resize(target_data ,(WIDTH,HEIGHT)).transpose(2,1,0)


    input_data = 1/255.0*input_data
    input_data = input_data - 0.5
    target_data = 1/255.0*target_data

    if False:
        if r not in X['data_tracker']:
            X['data_tracker'][r] = {}
        if ctr not in X['data_tracker'][r]:
            X['data_tracker'][r][ctr] = 0
        X['data_tracker'][r][ctr] += 1

    ###############
    target_data_plus[:,n:n+WIDTH,n:n+HEIGHT] = target_data
    input_data_plus[:,n:n+WIDTH,n:n+HEIGHT] = input_data

    return {
        'input':input_data_plus,
        'target':target_data_plus,
        'ctr':ctr,
    }




#EOF
