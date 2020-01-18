from kzpy3.vis3 import *
exec(identify_file_str)

# python kzpy3/drafts/Sq7/main.py --RESUME 1 --NET_TYPE ConDecon_test2 --NET_TYPE_SUFFIX 84x47
#WIDTH,HEIGHT = 168/2,94/2
WIDTH,HEIGHT = 168,94


from runs import All_runs

def setup(P):

    Runs = {}

    #activation_folders = sggo(opjm('2_TB_Samsung','Activations_folders','*'))
    activation_folders = sggo(opjD('Activations_folders','*'))
    
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
            {'path':opj(pname(pname(_Runs[r])),'data',r+'.h5py'),'data':None}

        Runs[r]['activations/indicies'] = \
            {'path':opj(pname(pname(_Runs[r])),'indicies',r+'.h5py'),'data':None}

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
            Runs[r]['activations/indicies']['data'][P['type'][1]+'.squeeze_activation']

        u = Runs[r]['activations/indicies']['data'][:]
        v = Runs[r]['activations/reverse-indicies']['data']

        for i in rlen(u):
            ii = u[i].astype(int)

            if ii < len(v) and ii > -1:
                v[ii] = i

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

    if R['data_from_flip'] > -1:
        assert(type(R['data_from_flip']) == int)
        assert(R['data_from_flip'] in [0,1])
        flip = R['data_from_flip']

    return r,ctr,flip


def get_data_function(P):

    global input_data_plus, target_data_plus

    Runs = P['Runs']

    drop = 0.05

    while True:
        if True:#try:
            r,ctr,flip = _selector(P)

            flip = 0
            #input_list = []
            #target_list = []

            Lists = {'input':[],'target':[]}

            if not flip:
                A = Runs[r]['activations/data']['data'][P['type'][1]+'.squeeze_activation']
                B = Runs[r]['original_timestamp_data']['data']['left_image']['vals']
                #print Runs[r]['button_number'][ctr]
                C = Runs[r]['net_projections']['data']['normal']
            else:
                assert(False)
                A = Runs[r]['net_projections']['data']['flip']
                B = Runs[r]['flip_images']['data']['left_image_flip']['vals']
                C = Runs[r]['net_projections']['data']['flip']
            if ctr >= len(A):
                print 'ctr >= len(A)'
                continue

            for k in Lists.keys():

                if 'rgb' in P[k]:
                    #print k,'rgb'
                    noise =0
                    if P['noise'] > 0:
                        noise = P['noise']*rnd(shape(B[ctr]))-P['noise']/2.
                    Lists[k].append(B[ctr+P[k+'_offset']]+noise)
                    if rnd() < drop and k == 'input':
                        Lists[k][-1] *= 0
                    #print 'rgb', dp(Lists[k][-1].min()), dp(Lists[k][-1].max())

                if 'projections' in P[k]:
                    #print k,'projections'
                    #s0,s1,s2,s3 = shape(C[ctr])[0],shape(C[ctr])[1],shape(C[ctr])[2],shape(C[ctr])[3]
                    #print shape(C[ctr])
                    #if False:#'+noise=' in P[k]:
                    #    mag = int(P[k].split('+noise=')[-1])
                    #    noise = mag*rnd(shape(C[ctr]))
                    #else:
                    #    noise = 0
                    noise =0
                    if P['noise'] > 0:
                        noise = P['noise']*rnd(shape(C[ctr]))-P['noise']/2.
                    #noise = 25*rnd(shape(C[ctr]))-15.5
                    Lists[k].append(C[ctr+P[k+'_offset']]+noise )
                    if rnd() < drop and k == 'input':
                        Lists[k][-1] *= 0
                    #print 'projections', dp(Lists[k][-1].min()), dp(Lists[k][-1].max())

                if 'button' in P[k]:
                    #print k,'button'
                    img = 0*B[ctr]
                    bn = int(Runs[r]['button_number'][ctr+P[k+'_offset']])
                    #print bn
                    #print bn
                    if bn in (1,2,3):
                        img[:,:,bn-1] = 255
                    img[0,0,:] = 255# + 24*rnd(shape(img))-12,
                    Lists[k].append(img)
                    if rnd() < drop and k == 'input':
                        Lists[k][-1] *= 0
                    #print 'button', dp(Lists[k][-1].min()), dp(Lists[k][-1].max())

                if 'Fire3' in P[k]:
                    #print k,'Fire3'
                    i = A[Runs[r]['activations/reverse-indicies']['data'][ctr+P[k+'_offset']]]
                    i = i.transpose(1,2,0) * 255/15.
                    Lists[k].append(i)
                    if rnd() < drop and k == 'input':
                        Lists[k][-1] *= 0
                    #print 'Fire3', dp(Lists[k][-1].min()), dp(Lists[k][-1].max())
                    

            break
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

    P['ctr'] = ctr

    for k in sorted(Lists.keys()):
        lst = Lists[k]
        for l in rlen(lst):
            e = lst[l]
            e = e.astype(float)
            e = cv2.resize( e,(WIDTH,HEIGHT))
            e = e.transpose(2,1,0)
            lst[l] = e

    Concats = {}
    for k in sorted(Lists.keys()):
        lst = Lists[k]
        for l in rlen(lst):
            if k not in Concats:
                Concats[k] = lst[l]
            else:
                Concats[k] = np.concatenate((Concats[k],lst[l]))


    Data = {
        'input':Concats['input'],
        'target':Concats['target'],
        'ctr':ctr,
    }

    return Data




#EOF
