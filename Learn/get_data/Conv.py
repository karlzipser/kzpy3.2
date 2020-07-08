from kzpy3.vis3 import *
exec(identify_file_str)

# python kzpy3/drafts/Sq7/main.py --RESUME 1 --NET_TYPE ConDecon_test2 --NET_TYPE_SUFFIX 84x47
#WIDTH,HEIGHT = 168/2,94/2

#from kzpy3.Learn.get_data.runs import All_runs

from runs import All_runs

def setup(P):

    Runs = {}

    for path in sggo(opjD('Data/outer_contours/rotated2','*.h5py')):
        r = fname(path).split('.')[0]
        if r in All_runs[P['runs']]:
            if os.path.getsize(path) > 0:
                if time.time() - os.path.getmtime(path) > 60:
                    Runs[r] = {}
                    for k in [
                        'rotated',
                        'original_timestamp_data',
                        'flip_images',
                        'left_timestamp_metadata_right_ts',
                        'button_number',
                        'encoder',
                    ]:
                        Runs[r][k] = None
                    Runs[r]['rotated'] = h5r(path)

    P['good_indicies'] = []

    if 'save_output_2' in P and P['save_output_2']:
        P['output_2_data'] = {}

    for r in Runs.keys():

        H = find_files_recursively(opjD('Data'),r,DIRS_ONLY=True)

        if len(H['paths']) == 0:
            cr(r,'not found.')
            continue
        else:
            cg(r,'found.')

        for k in ['original_timestamp_data','flip_images','left_timestamp_metadata_right_ts']:
            Runs[r][k] = h5r(opj(opjD('Data'),H['paths'].keys()[0],r,k+'.h5py'))


        good_indicies_file = opjD('Data/outer_contours','good_indicies.'+P['runs']+'.pkl')
        if len(sggo(good_indicies_file)) == 0:
            for i in rlen(Runs[r]['rotated']['valid']):
                if Runs[r]['rotated']['valid'][i]:
                    P['good_indicies'].append( (r,i) )


    if len(sggo(good_indicies_file)) == 1:
        P['good_indicies'] = lo(good_indicies_file)
    else:
        so(good_indicies_file,P['good_indicies'])

    P['Runs'] = Runs
    
    g = len(P['good_indicies'])
    T = {
        'n good_indicies':g,
        'hours of good_indicies':dp(g/30. /60. /60.),
        'data type':P['runs']
    }
    print ''
    kprint(T,title='good_indicies',p=3)
    print ''


meta_blank = zeros((1,41,22))

meta_gradient1 = meta_blank.copy()
meta_gradient2 = meta_blank.copy()
meta_gradient3 = meta_blank.copy()
meta_gradient4 = meta_blank.copy()

for x in range(22):
    meta_gradient1[0,:,x] = x/21.0
    meta_gradient2[0,:,x] = 1-x/21.0

for x in range(41):
    meta_gradient3[0,x,:] = x/40.0
    meta_gradient4[0,x,:] = 1-x/40.0


from scipy.ndimage import interpolation

gctr = 0 #10000
#cm('gctr = 10000',ra=1)


# python kzpy3/Learn/main_conv.py --main 6 --net_str conv1  --save_output_2 True --batch_size 1 --save_timer_time 999999 --LR 0 --runs validate --single_run tegra-ubuntu_25Oct18_15h43m36s --manual_input0 True

def get_data_function(P):

    global gctr

    Runs = P['Runs']

    
    while True:
        
        if True:#try:

            if not 'single_run' in P or not P['single_run']:
                g = len(P['good_indicies'])
                r,ctr = P['good_indicies'][rndint(g)]
                flip = rndint(2)
                assert flip in [0,1]

            elif k_in_D('manual_input0',P):
                r = P['single_run']
                while True:
                    try:
                        r = P['single_run']
                        
                        ctr,i_v = input('ctr, [[indx,val],...]: ')
                        print Runs[r]['rotated']['turns'][ctr][:]
                        assert type(ctr) == int
                        assert ctr < len(Runs[r]['original_timestamp_data']['left_image']['vals'])
                        if False:
                            for iv in i_v:
                                print iv
                                assert 0 <= iv[0] < 22
                                assert iv[1] in [1,2,3]
                        flip = 0
                        break

                    except KeyboardInterrupt:
                        cr('*** KeyboardInterrupt ***')
                        sys.exit()
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        CS_('Exception!',emphasis=True)
                        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
                        clp('Try again','`wrb')

            else:
                r = P['single_run']
                ctr = gctr
                flip = 0
                gctr += 1
                if gctr > len(Runs[r]['original_timestamp_data']['left_image']['vals']):
                    raw_enter()

            

            Lists = {'input':[],'target':[],'meta':[]}

            if not flip:
                B = Runs[r]['original_timestamp_data']['left_image']['vals']
            else:
                B = Runs[r]['flip_images']['left_image_flip']['vals']
            if ctr >= len(B):
                continue



            for k in ['input']:

                if 'rgb' in P[k]:
                    noise = 0
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



            if 'outer_contours' in P['target']:

                if not flip:
                    #cm('not flip')
                    Lists['target'].append(Runs[r]['rotated']['outer_countours_rotated_left'][ctr][:,0])
                    Lists['target'].append(Runs[r]['rotated']['outer_countours_rotated_right'][ctr][:,0])

                    Lists['target'].append(Runs[r]['rotated']['outer_countours_rotated_left'][ctr][:,1]/10.)
                    Lists['target'].append(Runs[r]['rotated']['outer_countours_rotated_right'][ctr][:,1]/10.)

                    Lists['target'].append(Runs[r]['rotated']['angles_left'][ctr][:]/10.)
                    Lists['target'].append(Runs[r]['rotated']['angles_right'][ctr][:]/10.)

                else:
                    #cy('flip')
                    Lists['target'].append(-Runs[r]['rotated']['outer_countours_rotated_right'][ctr][:,0])
                    Lists['target'].append(-Runs[r]['rotated']['outer_countours_rotated_left'][ctr][:,0])
                    
                    Lists['target'].append(Runs[r]['rotated']['outer_countours_rotated_right'][ctr][:,1]/10.)
                    Lists['target'].append(Runs[r]['rotated']['outer_countours_rotated_left'][ctr][:,1]/10.)
                    
                    Lists['target'].append(-Runs[r]['rotated']['angles_right'][ctr][:]/10.)
                    Lists['target'].append(-Runs[r]['rotated']['angles_left'][ctr][:]/10.)

            break
    


    meta_turns = meta_blank.copy()

    if k_in_D('manual_input0',P):
        meta_turns += 2
        for i in range(22):#i_v:
            meta_turns[0,:,i] = i_v
        #clp(meta_turns,r=1)

    elif not k_in_D('turns_zeroed',P):
        turns = Runs[r]['rotated']['turns'][ctr][:]
        if flip:
            turns -= 2
            turns *= -1
            turns += 2

        turns22 = interpolation.zoom(turns,22/(1.0*len(turns)))

        #cm(shape(turns22),ra=1)

        for i in range(shape(meta_turns)[1]):
            meta_turns[0,i,:] = turns22

    #mi(meta_turns[0,:,:])
    #spause()
    #raw_enter()

    Lists['meta'].append(meta_gradient1)
    Lists['meta'].append(meta_gradient2)
    Lists['meta'].append(meta_gradient3)
    Lists['meta'].append(meta_gradient4)
    Lists['meta'].append(meta_turns)

    for i in range(10-len(Lists['meta'])):
        Lists['meta'].append(meta_blank)
        
    #for i in rlen(Lists['meta']):
    #    mi(z55(Lists['meta'][i][0,:,:]),i)
    #spause()

    P['ctr'] = ctr
    #cy(ctr)
    P['run'] = r

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
    for k in ['input','target','meta']:#sorted(Lists.keys()):
        lst = Lists[k]
        for l in rlen(lst):
            if k not in Concats:
                Concats[k] = lst[l]
            else:
                Concats[k] = np.concatenate((Concats[k],lst[l]))

    #cm(shape(Concats['target']),ra=1)
    #print shape(Concats['meta'])
    Data = {
        'input':Concats['input'],
        'target':Concats['target'],
        'meta':Concats['meta'],
        'ctr':ctr,
    }
    #print(shape(Data['input']))
    #print(shape(Data['target']))

    return Data




#EOF
