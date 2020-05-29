from kzpy3.vis3 import *
exec(identify_file_str)

# python kzpy3/drafts/Sq7/main.py --RESUME 1 --NET_TYPE ConDecon_test2 --NET_TYPE_SUFFIX 84x47
#WIDTH,HEIGHT = 168/2,94/2

#from kzpy3.Learn.get_data.runs import All_runs

from runs import All_runs

def setup(P):

    Runs = {}

    for path in sggo(opjD('Data/outer_contours/rotated','*.h5py')):
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

    for r in Runs.keys():

        H = find_files_recursively(opjD('Data'),r,DIRS_ONLY=True)

        if len(H['paths']) == 0:
            cr(r,'not found.')
            continue
        else:
            cg(r,'found.')

        for k in ['original_timestamp_data','flip_images','left_timestamp_metadata_right_ts']:
            Runs[r][k] = h5r(opj(opjD('Data'),H['paths'].keys()[0],r,k+'.h5py'))

        if len(sggo(opjD('temp.pkl'))) == 0:
            for i in rlen(Runs[r]['rotated']['valid']):
                if Runs[r]['rotated']['valid'][i]:
                    P['good_indicies'].append( (r,i) )
    


    if len(sggo(opjD('temp.pkl'))) == 1:
        P['good_indicies'] = lo(opjD('temp.pkl'))
    else:
        so(opjD('temp.pkl'),P['good_indicies'])

    P['Runs'] = Runs
    








def get_data_function(P):

    #cm(P.keys(),ra=1)
    Runs = P['Runs']

    
    while True:
        
        if True:#try:

            g = len(P['good_indicies'])
            r,ctr = P['good_indicies'][rndint(g)]
            flip = 0

            

            Lists = {'input':[],'target':[],'meta':[]}

            if not flip:
                B = Runs[r]['original_timestamp_data']['left_image']['vals']
            else:
                assert(False)
                B = Runs[r]['flip_images']['left_image_flip']['vals']
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


            if 'outer_contours' in P['target']:
                Lists['target'].append(Runs[r]['rotated']['outer_countours_rotated_left'][ctr][:,0])
                Lists['target'].append(Runs[r]['rotated']['outer_countours_rotated_right'][ctr][:,0])
                Lists['target'].append(Runs[r]['rotated']['outer_countours_rotated_left'][ctr][:,1]/10.)
                Lists['target'].append(Runs[r]['rotated']['outer_countours_rotated_right'][ctr][:,1]/10.)
                Lists['target'].append(Runs[r]['rotated']['angles_left'][ctr][:]/10.)
                Lists['target'].append(Runs[r]['rotated']['angles_right'][ctr][:]/10.)

            if 'test22' in P['target']:
                img = B[ctr+P[k+'_offset']]
                line = img[:,:,1].mean(axis=1)
                Lists['target'].append(line)


            break
    

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


    for i in range(10-len(Lists['meta'])):
        Lists['meta'].append(meta_blank)
        
    for i in rlen(Lists['meta']):
        mi(z55(Lists['meta'][i][0,:,:]),i)

    spause()

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
