from kzpy3.vis3 import *
exec(identify_file_str)

# python kzpy3/drafts/Sq7/main.py --RESUME 1 --NET_TYPE ConDecon_test2 --NET_TYPE_SUFFIX 84x47

X = {'data_tracker':{}}

WIDTH,HEIGHT = 168/2,94/2


Runs = {}


aruns = sggo(opjD('Activations','data','*.h5py'))
runs = []
for r in aruns:
    if os.path.getsize(r) > 0:
        if time.time() - os.path.getmtime(r) > 60:
            runs.append(fname(r).split('.')[0])
np.random.shuffle(runs)


Run_coder = {}

run_ctr = 0

good_list = []

for r in runs:
    """
    print opjD('Activations','data',r+'.h5py')

    print sggo(opjD('Activations','data',r+'.h5py'))
    if len(sggo(opjD('Activations','data',r+'.h5py'))) < 1:
        continue
    """
    Run_coder[run_ctr] = r

    H = find_files_recursively(opjD('Data'),r,DIRS_ONLY=True)

    
    Runs[r] = {
        'original_timestamp_data':{},
        'flip_images':{},
        'left_timestamp_metadata_right_ts':{},
        'net_projections':{},
        'activations/data':{},
        'activations/indicies':{},
    }
    


    Runs[r]['original_timestamp_data'] = \
        {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'original_timestamp_data.h5py'),'data':None}

    Runs[r]['flip_images'] = \
        {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'flip_images.h5py'),'data':None}

    Runs[r]['left_timestamp_metadata_right_ts'] = \
        {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'left_timestamp_metadata_right_ts.h5py'),'data':None}

    Runs[r]['net_projections'] = \
        {'path':opj(opjD('Data'),'Network_Predictions_projected',r+'.net_projections.h5py'),'data':None}

    Runs[r]['activations/data'] = \
        {'path':opj(opjD('Activations'),'data',r+'.h5py'),'data':None}

    Runs[r]['activations/indicies'] = \
        {'path':opj(opjD('Activations'),'indicies',r+'.h5py'),'data':None}



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

    Runs[r]['activations/reverse-indicies'] = \
        {'data':np.zeros(len(Runs[r]['left_timestamp_metadata_right_ts']['data']['motor']),int)-1}


    Runs[r]['activations/indicies']['data'] = \
        Runs[r]['activations/indicies']['data'][u'Fire6.squeeze_activation']





    u = Runs[r]['activations/indicies']['data'][:]
    v = Runs[r]['activations/reverse-indicies']['data']


    for i in rlen(u):
        ii = u[i].astype(int)

        if ii < len(v) and ii > -1:
            v[ii] = i




        run_ctr += 1
    """
    except KeyboardInterrupt:
        cr('*** KeyboardInterrupt ***')
        sys.exit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)   
    """

kprint(Runs)
###############

input_data_plus = None
target_data_plus = None


WWWW = Toggler()
global_ctr = 0

def _selector(P):
    global global_ctr
    R = P['runtime_parameters']
    #kprint(R,'R')
    good = good_list[rndint(len(good_list))]
    r, ctr = Run_coder[good[0]], good[1]
    flip = rndint(2)

    if R['data_from_run'] != 'no':
        assert(type(R['data_from_run']) == str)
        r = R['data_from_run']

    if R['data_from_ctr'] > -1:
        if WWWW['test'](R['ctr_reset']):
            ctr = R['data_from_ctr']
            global_ctr = ctr
        else:
            global_ctr += 1
            if global_ctr >= len(Runs[r]['original_timestamp_data']['data']['left_image']['vals']):
                global_ctr = R['data_from_ctr']
            ctr = global_ctr

    if R['data_from_flip'] > -1:
        assert(type(R['data_from_flip']) == int)
        assert(R['data_from_flip'] in [0,1])
        flip = R['data_from_flip']

    #print ctr
    return r,ctr,flip


def get_data_function(P):

    global input_data_plus, target_data_plus

    while True:
        if True:#try:
            r,ctr,flip = _selector(P)
            flip = 0
            if not flip:
                #A = Runs[r]['net_projections']['data']['normal']
                A = Runs[r]['activations/data']['data'][u'Fire6.squeeze_activation']
                B = Runs[r]['original_timestamp_data']['data']['left_image']['vals']
                #print 'not flip'
            else:
                assert(False)
                A = Runs[r]['net_projections']['data']['flip']
                B = Runs[r]['flip_images']['data']['left_image_flip']['vals']
                #print 'FLIP'

            input_data =  A[Runs[r]['activations/reverse-indicies']['data'][ctr]]
            if ctr >= len(A):
                print 'ctr >= len(A)'
                continue
            temp = A[ctr]
            break
        else:#except:
            print 'except'

    if flip:
        input_data[:,:,0] = temp[:,:,1]
        input_data[:,:,1] = temp[:,:,0]
    target_data = B[ctr]

    n = 5
    if input_data_plus == None:
        nc = shape(input_data)[0]
        n = 5
        input_data_plus = zeros((nc,2*n+WIDTH,2*n+HEIGHT))#+0.5
        target_data_plus = zeros((3,2*n+WIDTH,2*n+HEIGHT))+0.5


    input_data = input_data.astype(float).transpose(1,2,0)

    input_data = cv2.resize( input_data,(WIDTH,HEIGHT)).transpose(2,1,0)

    target_data = cv2.resize(target_data ,(WIDTH,HEIGHT)).transpose(2,1,0)


    target_data = 1/255.0*target_data


    if r not in X['data_tracker']:
        X['data_tracker'][r] = {}
    if ctr not in X['data_tracker'][r]:
        X['data_tracker'][r][ctr] = 0
    X['data_tracker'][r][ctr] += 1

    target_data_plus[:,n:n+WIDTH,n:n+HEIGHT] = target_data
    input_data_plus[:,n:n+WIDTH,n:n+HEIGHT] = input_data

    return {
        'input':input_data_plus,
        'target':target_data_plus,
        'ctr':ctr,
    }




#EOF
