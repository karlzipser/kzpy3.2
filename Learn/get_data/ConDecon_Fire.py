from kzpy3.vis3 import *
exec(identify_file_str)






assert(False)








# python kzpy3/drafts/Sq7/main.py --RESUME 1 --NET_TYPE ConDecon_test2 --NET_TYPE_SUFFIX 84x47
#WIDTH,HEIGHT = 168/2,94/2

#from kzpy3.Learn.get_data.runs import All_runs

from runs import All_runs

def setup(P):

    if 'pts2d' in P['target']:# or 'pts2d' in P['input']:
        P['pts2d_runs'] = []
        pruns = sggo(opjD('Data','pts2D_multi_step',P['pts2_h5py_type'],'*.h5py'))
        for p in pruns:
            if os.path.getsize(p) > 0:
                P['pts2d_runs'].append(fname(p).split('.')[0])

    Runs = {}

    #activation_folders = sggo(opjm('2_TB_Samsung','Activations_folders','*'))
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

    #kprint(_Runs)

    for r in _Runs.keys():


        if 'pts2d' in P['target']:# or 'pts2d' in P['input']:
            if r not in P['pts2d_runs']:
                cm('not using',r)
                continue

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

        if 'pts2d' in P['target'] or 'pts2d' in P['input']:
            path = opjD('Data','pts2D_multi_step',P['pts2_h5py_type'],r+'.h5py')
            if os.path.getsize(path) > 0:

                Runs[r]['pts2d'] = {'path':path}
                if os.path.exists(Runs[r]['pts2d']['path']):
                    Runs[r]['pts2d']['h5py'] = h5r(Runs[r]['pts2d']['path'])
                    Runs[r]['pts2d']['data'] = Runs[r]['pts2d']['h5py']['images']

                    Runs[r]['pts2d']['reverse-indicies'] = np.zeros(int(1.5*len(Runs[r]['pts2d']['data'])))#     len(Runs[r]['left_timestamp_metadata_right_ts']['data']['motor']),int)-1
                    u = Runs[r]['pts2d']['h5py']['index'][:]
                    v = Runs[r]['pts2d']['reverse-indicies']
                    for i in rlen(u):
                        ii = u[i].astype(int)
                        if ii < len(v) and ii > -1:
                            v[ii] = i
            else:
                clp('size of',path,'== 0','`ybb')
                
        else:
            clp('warning,','`y',Runs[r]['pts2d']['path'],'`y-r','not found','`y')

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
        #clp('_selector calss self, ctr=',ctr,'run =',r)
        r,ctr,flip = _selector(P)

    if R['data_from_flip'] > -1:
        assert(type(R['data_from_flip']) == int)
        assert(R['data_from_flip'] in [0,1])
        flip = R['data_from_flip']

    return r,ctr,flip

if False:
    ctr_lst = []
    ctr_timer = Timer(15)
#Button_translation = {1:0,2:2,3:1}

def get_data_function(P):

    global input_data_plus, target_data_plus

    Runs = P['Runs']

    #drop = 0.1


    while True:
        #print P['drop'],type(P['drop'])
        try:
            r,ctr,flip = _selector(P)

            #P[r].append(ctr)

            #if r_ctr_dic_timer.check():
            #    r_ctr_dic_timer.reset()
            #    soD(P)

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
                #print 'ctr >= len(A)'
                continue

            if False:
                ctr_lst.append(ctr)
                if ctr_timer.check():
                    ctr_timer.reset()
                    figure('ctr hist')
                    hist(ctr_lst)
                    spause()

            for k in Lists.keys():
                #P[k+'_offset'] = int(P[k+'_offset'])

                if 'rgb' in P[k]:
                    #print k,'rgb'
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
                    #print 'rgb', dp(Lists[k][-1].min()), dp(Lists[k][-1].max())



                if 'pts2d' in P[k]:

                    i = Runs[r]['pts2d']['reverse-indicies'][ctr]
                    p = Runs[r]['pts2d']['data'][i + P[k+'_offset']]
                    if k == 'input':
                        #p[:,18*2:,:] = 0
                        p *= 0
                        #p[:(47-18+6)*2,:,:] = 0
                    if 'pts2d2' in P['type'] or 'pts2d2_from_scratch' in P['type']:
                        p[:,:,2] /= 3
                    Lists[k].append(p)
                    



                if 'projections' in P[k]:

                    if type(P[k+'_offset']) == list:
                        offset_list = P[k+'_offset']
                    else:
                        offset_list = [P[k+'_offset']]
                    for off in offset_list:
                        off = int(off)
                        noise =0
                        if k == 'input':
                            if P['projection.noise'] > 0:
                                noise = P['projection.noise'] * rnd(shape(C[ctr])) - P['projection.noise']/2.
                        Lists[k].append(C[ctr+off]+noise )
                        if rnd() < P['drop'] and k == 'input':
                            Lists[k][-1] *= 0

                if 'button' in P[k]:
                    #print k,'button'
                    #print ctr,k,P[k+'_offset']
                    #img = 0*B[ctr]
                    img = zeros((P['width'],P['height'],3))
                    bn = int(Runs[r]['button_number'][ctr+P[k+'_offset']])
                    #print bn
                    #print bn
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
                        img[0,0,:] = 255# + 24*rnd(shape(img))-12,
                    else:
                        pass #print '********************* original_Fire3_scaling button'
                        if bn in (1,2,3):
                            img[:,:,bn-1] = 1
                    Lists[k].append(img)
                    if rnd() < P['drop'] and k == 'input':
                        Lists[k][-1] *= 0
                    #print 'button', dp(Lists[k][-1].min()), dp(Lists[k][-1].max())

                if 'Fire3' in P[k]:
                    #print k,'Fire3'
                    i = A[Runs[r]['activations/reverse-indicies']['data'][ctr+P[k+'_offset']]]
                    i = i.transpose(1,2,0)
                    if 'original_Fire3_scaling' not in P:
                        i = i * 255/15.
                    else:
                        pass#print '********************* original_Fire3_scaling Fire3'

                    Lists[k].append(i)
                    if rnd() < P['drop'] and k == 'input':
                        Lists[k][-1] *= 0
                    #print 'Fire3', dp(Lists[k][-1].min()), dp(Lists[k][-1].max())
                    


                    Lists[k].append(i)
                    if rnd() < P['drop'] and k == 'input':
                        Lists[k][-1] *= 0
                    
            break
        
        except KeyboardInterrupt:
            cr('*** KeyboardInterrupt ***')
            sys.exit()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
        

    P['ctr'] = ctr

    for k in sorted(Lists.keys()):
        lst = Lists[k]
        for l in rlen(lst):
            e = lst[l]
            e = e.astype(float)
            if P['width'] and P['height']:
                e = cv2.resize( e,(P['width'],P['height']))
            e = e.transpose(2,1,0)
            lst[l] = e

    Concats = {}
    for k in sorted(Lists.keys()):
        lst = Lists[k]
        for l in rlen(lst):
            #print shape(lst[l])
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
