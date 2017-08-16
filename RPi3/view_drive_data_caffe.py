from kzpy3.RPi3.view_drive_data_essentials import *

CAFFE_TRAINING_MODE = 'CAFFE_TRAINING_MODE'
CAFFE_BVLC_REF_CAT_TRAINING_MODE = 'CAFFE_BVLC_REF_CAT_TRAINING_MODE'
CAFFE_BVLC_REF_TRAINING_MODE = 'CAFFE_BVLC_REF_TRAINING_MODE'
CAFFE_CAT_TRAINING_MODE = 'CAFFE_CAT_TRAINING_MODE'
MC_CAFFE_TRAINING_MODE = 'MC_CAFFE_TRAINING_MODE'
MC_CAFFE_CAT_TRAINING_MODE = 'MC_CAFFE_CAT_TRAINING_MODE'
CAFFE_DEPLOY_MODE = 'CAFFE_DEPLOY_MODE'
MC_CAFFE_DEPLOY_MODE = 'MC_CAFFE_DEPLOY_MODE'
USE_GRAPHICS = 'USE_GRAPHICS'
SAVE_ALL_RUN_DIC = 'SAVE_ALL_RUN_DIC'
CAFFE_TRAJECTORY_TRAINING_MODE = 'CAFFE_TRAJECTORY_TRAINING_MODE'
CAFFE_PATCH_TRAINING_MODE = 'CAFFE_PATCH_TRAINING_MODE'
run_mode = CAFFE_DEPLOY_MODE
#CAFFE_DATA = opjD('RPi3_data/all_runs_dics/runs_scl_25_BW')
#CAFFE_DATA = opjh('Desktop/RPi3_data/all_runs_dics/runs_scale_50_BW_test')
#CAFFE_DATA = opjh('Desktop/RPi3_data/runs_scale_50_BW_test')
CAFFE_FRAME_RANGE = (-7,-6)# (-15,-6) # 
CAFFE_DATA = opjh('Desktop/RPi3_data/all_runs_dics/runs_scl_100_RGB')
#CAFFE_DATA = opjh('Desktop/RPi3_data/runs_scale_25_BW_test')
#CAFFE_FRAME_RANGE = (-7,-6)# 

# all_runs_dic = load_objh('Desktop/RPi3_data/all_runs_dics/runs_scale_50_BW')

print(d2s('*** run_mode =',run_mode))

def get_steer_bins(all_runs_dic):
    steer_bins = {}
    steer_bins['left_max'] = []
    steer_bins['left'] = []
    steer_bins['left_min'] = []
    steer_bins['center'] = []
    steer_bins['right_min'] = []
    steer_bins['right'] = []
    steer_bins['right_max'] = []
    for k in all_runs_dic:
        print k
        run_data_dic = all_runs_dic[k]
        for i in range(len(run_data_dic['train_frames'])):
            t = run_data_dic['train_frames'][i]
            if t:
                #f = run_data_dic['img_lst'][i]
                if run_data_dic['steer'][i] < -0.6:
                    steer_bins['left_max'].append((k,i))
                elif run_data_dic['steer'][i] < -0.3:
                    steer_bins['left'].append((k,i))
                elif run_data_dic['steer'][i] < -0.05:
                    steer_bins['left_min'].append((k,i))
                elif run_data_dic['steer'][i] <= 0.05:
                    steer_bins['center'].append((k,i))
                elif run_data_dic['steer'][i] <= 0.3:
                    steer_bins['right_min'].append((k,i))
                elif run_data_dic['steer'][i] <= 0.6:
                    steer_bins['right'].append((k,i))
                elif run_data_dic['steer'][i] <= 1:
                    steer_bins['right_max'].append((k,i))
                else:
                    raise Exception('get_steer_bins error!')
    return steer_bins
def steer_bin_medians(steer_bins,all_runs_dic):
    m = []
    for b in steer_bins:
        lst = []
        for q in steer_bins[b]:
            lst.append(all_runs_dic[q[0]]['steer'][q[1]])
        m.append((b,np.median(lst),len(steer_bins[b])))
    return m
def get_rand_frame_data(steer_bins,all_runs_dic,frame_range=(-15,-6),Graphics=False):
    sbks = steer_bins.keys() + ['center'] # This + ['center'] has the effect of doubling the chance of center position result.
    b = sbks[np.random.randint(len(sbks))]
    ardks = all_runs_dic.keys()
    l = len(steer_bins[b])
    e = steer_bins[b][np.random.randint(l)]
    r = e[0]
    n = e[1]
    steer = int(100.0*all_runs_dic[r]['steer'][n])
    frames_to_next_turn = int(all_runs_dic[r]['frames_to_next_turn'][n])
    rps = int(10.0*all_runs_dic[r]['rps'][n])
    frame_names = []
    for i in range(frame_range[0]+n,frame_range[1]+n):
        frame_names.append(opj(all_runs_dic[r]['run_path'],all_runs_dic[r]['img_lst'][i]))
    return (b,r,n,steer,frames_to_next_turn,rps,frame_names)
def get_rand_frame_trajectory_data(steer_bins,all_runs_dic,frame_range=(-15,-6),trajectory_range=(-15,15)):
    sbks = steer_bins.keys()
    b = sbks[np.random.randint(len(sbks))]
    l = len(steer_bins[b])
    e = steer_bins[b][np.random.randint(l)]
    r = e[0]
    n = e[1]
    steer_lst = []
    rps_lst = []
    for i in range(trajectory_range[0],trajectory_range[1]):
        steer_lst.append(int(100.0*all_runs_dic[r]['steer'][n+i]))
        rps_lst.append(int(10.0*all_runs_dic[r]['rps'][n+i]))
    frame_names = []
    for i in range(frame_range[0]+n,frame_range[1]+n):
        frame_names.append(opj(all_runs_dic[r]['run_path'],all_runs_dic[r]['img_lst'][i]))
    return (steer_lst,rps_lst,frame_names)
def categorize_steer(s):
    bs = s * 7 * 0.9999
    return np.int(np.floor(bs))
def blurred_steer(c):
    if c == 0:
        s = [5,2,1,0,0,0,0]
    elif c == 1:
        s = [2,5,2,1,0,0,0]
    elif c == 2:
        s = [1,2,5,2,1,0,0]
    elif c == 3:
        s = [0,1,2,5,2,1,0]
    elif c == 4:
        s = [0,0,1,2,5,2,1]
    elif c == 5:
        s = [0,0,0,1,2,5,2]
    elif c == 6:
        s = [0,0,0,0,1,2,5]
    else:
        assert(False)
    assert len(s) == 7
    return list(z2o(np.array(s)))
  
def package_caffe_data_for_single_run(run_data_dic,net,layer_name_list,frame_range):
    """
    run "kzpy3/caf/training/y2016/m3/RPi3/train.py"
    all_runs_dic = load_obj('/Users/karlzipser/Desktop/RPi3_data/all_runs_dics/runs_scl_25_BW')
    solver.net.copy_from('/Users/karlzipser/Google_Drive/2016-3/original_with_accuracy_11px_iter_11100000.caffemodel')
    k = all_runs_dic.keys()
    net = solver.net
    run_data_dic = all_runs_dic[k[1]]
    img_dic={}
    from kzpy3.RPi3.view_drive_data_essentials import *
    frame_range=(-15,-6)
    layer_name_list = ['conv2','ip1','ip2']
    ('ddata', (1, 9, 56, 75))
    ('ddata2', (1, 3))
    ('py_image_data', (1, 9, 56, 75))
    ('py_target_data', (1, 3))
    ('conv1', (1, 96, 16, 22))
    ('pool1', (1, 96, 8, 11))
    ('conv2', (1, 256, 4, 7))
    ('pool2', (1, 256, 2, 3))
    ('ip1', (1, 512))
    ('ip2', (1, 3))
    ('identity', ())
    ('conv1', (96, 9, 11, 11))
    ('conv2', (256, 48, 5, 5))
    ('ip1', (512, 1536))
    ('ip2', (3, 512))

    """
    
    caffe_data_dic = {}
    len_train_frames = len(run_data_dic['train_frames'])

    for l in layer_name_list:
        shp = list(shape(net.blobs[l]))
        shp[0] = len_train_frames
        print shp
        caffe_data_dic[l] = zeros(shp)

    for i in range(len_train_frames):
        img_lst = []
        print i
        t = run_data_dic['train_frames'][i]
        for j in range(frame_range[0]+i,frame_range[1]+i):
            f = run_data_dic['img_lst'][j]
            img_lst.append(imread_from_img_dic(img_dic,run_data_dic['run_path'],f,True))
        for j in range(len(img_lst)):
            net.blobs['ddata'].data[0,j,:,:] = img_lst[j]/255.0-0.5
        net.forward()

        if np.mod(i,10) == 0:
            plt.figure('ip1')
            plt.clf()
            plot(net.blobs['ip1'].data.T)
            mi(net.blobs['conv1'].data[0,15,:,:],100)
            mi(net.blobs['conv2'].data[0,16,:,:],101)
            mi(net.blobs['py_image_data'].data[0,3,:,:],99)
            plt.pause(0.01)
        for l in layer_name_list:
            #mi(net.blobs[l].data[0,13,:,:],88)
            caffe_data_dic[l][i,:] = net.blobs[l].data

    return caffe_data_dic

def package_caffe_data_for_multi_runs(all_runs_dic,net,layer_name_list,frame_range):
    for k in sorted(all_runs_dic.keys()):
        p = package_caffe_data_for_single_run(all_runs_dic[k],net,layer_name_list,frame_range)
        save_obj(p,opjD(k+'_caffe_data'))


"""
f = '09Feb16_14h19m10s_scl=25_mir=0'
d=load_obj('/Users/karlzipser/Desktop/'+f+'_caffe_data')
r = all_runs_dic[f]
i = d['ip2'][:,0]-0.5
s = r['steer']
plt.figure(1)
plot(i)
plot(s)
plt.title(np.corrcoef(s,i)[0,1])
t = r['train_frames']
s2 = t*s
i2 = t*i
plt.figure(2)
plot(i2)
plot(s2)
plt.title(np.corrcoef(s2,i2)[0,1])
plt.figure(3)
plt.scatter(s2,i2)
plt.title(np.corrcoef(s2,i2)[0,1])
"""



if run_mode == CAFFE_TRAINING_MODE:
    if 'all_runs_dics' in CAFFE_DATA:
        all_runs_dic = load_obj(CAFFE_DATA)
    else: 
        all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    steer_bins = get_steer_bins(all_runs_dic)
    def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-15,-6)):
        b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
        img_lst = []
        for f in frame_names:
            img = imread_from_img_dic(img_dic,'',f)/255.0-0.5
            #img = -img # temp
            img_lst.append(img)
        if len(img_lst) == 1 and len(np.shape(img_lst[0])) == 3:
            img = img_lst[0]
            img_lst = [img[:,:,0],img[:,:,1],img[:,:,2]]
        S = steer/200.0 + 0.5
        assert(S>=0)
        assert(S<=1)
        F = frames_to_next_turn/45.0
        F = min(F,1.0)
        assert(F>=0)
        assert(F<=1)
        R = rps/75.0
        R = min(R,1.0)
        assert(R>=0)
        assert(R<=1)
        #return img_lst,[S,0*F,0*R] #steer only, 17 Feb 2015 trianing
        return img_lst,[S,F,R]

elif run_mode == CAFFE_PATCH_TRAINING_MODE:
    if 'all_runs_dics' in CAFFE_DATA:
        all_runs_dic = load_obj(CAFFE_DATA)
    else: 
        all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    steer_bins = get_steer_bins(all_runs_dic)
    img_shape = (225, 300, 3)
    #img_shape = (112, 150)
    patch_width = 75#int(img_shape[1]/4.0)
    x1x2y1y2_lst = []
    for x1 in range(img_shape[1]-patch_width):
        for y1 in range(img_shape[0]-patch_width):
            x2 = x1+patch_width
            y2 = y1+patch_width
            assert(x1>=0 and x1<=img_shape[1]-patch_width)
            assert(y1>=0 and y1<=img_shape[0]-patch_width)
            assert(x2<=img_shape[1])
            assert(y2<=img_shape[0])
            #print(x1,x2,y1,y2)
            x1x2y1y2_lst.append((x1,x2,y1,y2))
    def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-15,-6)):
        j = np.random.randint(len(x1x2y1y2_lst))
        (x1,x2,y1,y2) = x1x2y1y2_lst[j]
        b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
        img_lst = []
        for f in frame_names:
            img = imread_from_img_dic(img_dic,'',f)/255.0-0.5
            img2 = img[y1:y2,x1:x2,:]
            img2 = img2.mean(axis=2)
            assert(len(shape(img2))==2)
            img_lst.append(img2)
        return img_lst,[(x1+x2)/2.0/(1.0*img_shape[1]),(y1+y2)/2.0/(1.0*img_shape[1])]


elif run_mode == CAFFE_TRAJECTORY_TRAINING_MODE:
    if 'all_runs_dics' in CAFFE_DATA:
        all_runs_dic = load_obj(CAFFE_DATA)
    else: 
        all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    steer_bins = get_steer_bins(all_runs_dic)
    def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-15,-6)):
        steer_lst,rps_lst,frame_names = get_rand_frame_trajectory_data(steer_bins,all_runs_dic,frame_range=(-15,-6),trajectory_range=(-15,15))
        img_lst = []
        for f in frame_names:
            img = imread_from_img_dic(img_dic,'',f)/255.0-0.5
            #img = -img # temp
            img_lst.append(img)
        if len(img_lst) == 1 and len(np.shape(img_lst[0])) == 3:
            img = img_lst[0]
            img_lst = [img[:,:,0],img[:,:,1],img[:,:,2]]
        
        S_lst = np.array(steer_lst)/200.0 + 0.5
        assert(S_lst.min()>=0)
        assert(S_lst.max()<=1)

        R_lst = np.array(rps_lst)/75.0
        R_lst[R_lst>1.0] = 1.0
        assert(R_lst.min()>=0)
        assert(R_lst.max()<=1)
        return img_lst,list(S_lst)+list(R_lst)

elif run_mode == CAFFE_CAT_TRAINING_MODE:
    all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    steer_bins = get_steer_bins(all_runs_dic)
    def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-15,-6)):
        b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
        img_lst = []
        for f in frame_names:
            img_lst.append(imread_from_img_dic(img_dic,'',f)/255.0-0.5)
        if len(img_lst) == 1 and len(np.shape(img_lst[0])) == 3:
            img = img_lst[0]
            img_lst = [img[:,:,0],img[:,:,1],img[:,:,2]]
        S = steer/200.0 + 0.5
        assert(S>=0)
        assert(S<=1)
        steer_lst = [0,0,0,0,0,0,0]
        c = categorize_steer(S)
        assert(c<len(steer_lst))
        assert(c>=0)
        steer_lst[c] = 1.0
        return img_lst,steer_lst


elif run_mode == CAFFE_BVLC_REF_CAT_TRAINING_MODE or run_mode == CAFFE_BVLC_REF_TRAINING_MODE:
    #img_mask = np.zeros((3,227,227))+1.0
    #img_mask[:,:100,:] = 0.0
    import caffe
    # Here I use the image transformer code from the bvlc_reference net to get my images in the correct scaling and format
    # for the pretrained bvlc_reference net
    all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    #all_runs_dic = load_obj(opjD('RPi3_data/all_runs_dics/runs_scl_100_RGB'))
    steer_bins = get_steer_bins(all_runs_dic)
    caffe_root = opjh('caffe')  # this file is expected to be in {caffe_root}/examples
    transformer = caffe.io.Transformer({'data': (1, 3, 227, 227)})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', np.load(opj(caffe_root,'python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
    def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-7,-6)):
        assert frame_range == (-7,-6) # i.e., we will only work with a single RGB image.
        b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
        img_lst = []
        for f in frame_names:
            cimg = caffe.io.load_image(f)
            cimg = cimg[105:,:,:]
            img_lst.append(transformer.preprocess('data',cimg))
        try:
            assert len(img_lst) == 1
            assert len(np.shape(img_lst[0])) == 3
        except:
            print "BIG PROBLEM!"
        img = img_lst[0]
        img_lst = [img[0,:,:],img[1,:,:],img[2,:,:]]
        S = steer/200.0 + 0.5
        assert(S>=0)
        assert(S<=1)
        if run_mode == CAFFE_BVLC_REF_CAT_TRAINING_MODE:
            steer_lst = [0,0,0,0,0,0,0]
            c = categorize_steer(S)
            assert(c<len(steer_lst))
            assert(c>=0)
            steer_lst = blurred_steer(c)
            return img_lst,steer_lst
        else:
            F = frames_to_next_turn/90.0
            F = min(F,1.0)
            assert(F>=0)
            assert(F<=1)
            R = rps/75.0
            R = min(R,1.0)
            assert(R>=0)
            assert(R<=1)
            return img_lst,[S,F,0*R]
        
# e.g.s for transforming filenames
# C_f='/Users/karlzipser/Desktop/RPi3_data/runs_scl_100_RGB/09Feb16_13h33m51s_scl=100_mir=0/0_1455053641.36_str=-6_spd=52_rps=0_lrn=125_rrn=105_rnd=0_scl=100_mir=0_.jpg'
# M_f='/Users/karlzipser/Desktop/RPi3_data/runs_scale_50_BW/09Feb16_13h33m51s_scl=50_mir=0/0_1455053641.36_str=-6_spd=52_rps=0_lrn=125_rrn=105_rnd=0_scl=50_mir=0_.png'
elif run_mode == MC_CAFFE_TRAINING_MODE:
    all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    steer_bins = get_steer_bins(all_runs_dic)
    def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-15,-6)):
        b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
        M_img_lst = []
        C_img_lst = []
        for M_f in frame_names:
            M_img_lst.append(imread_from_img_dic(img_dic,'',M_f)/255.0-0.5)
        c_f = M_f # last frame is most recent
        c_f = c_f.replace('scale_50_BW','scl_100_RGB')
        c_f = c_f.replace('scl=50','scl=100')
        C_f = c_f.replace('png','jpg')
        C_img = imread_from_img_dic(img_dic,'',C_f)/255.0-0.5
        C_img_lst = [C_img[:,:,0],C_img[:,:,1],C_img[:,:,2]]
        S = steer/200.0 + 0.5
        assert(S>=0)
        assert(S<=1)
        F = frames_to_next_turn/45.0
        F = min(F,1.0)
        assert(F>=0)
        assert(F<=1)
        R = rps/75.0
        R = min(R,1.0)
        assert(R>=0)
        assert(R<=1)
        return M_img_lst,C_img_lst,[S,0*F,0*R]

elif run_mode == MC_CAFFE_CAT_TRAINING_MODE:
    all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    steer_bins = get_steer_bins(all_runs_dic)
    def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-15,-6)):
        b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
        M_img_lst = []
        C_img_lst = []
        for M_f in frame_names:
            M_img_lst.append(imread_from_img_dic(img_dic,'',M_f)/255.0-0.5)
        c_f = M_f # last frame is most recent
        c_f = c_f.replace('scale_50_BW','scl_100_RGB')
        c_f = c_f.replace('scl=50','scl=100')
        C_f = c_f.replace('png','jpg')
        C_img = imread_from_img_dic(img_dic,'',C_f)/255.0-0.5
        C_img_lst = [C_img[:,:,0],C_img[:,:,1],C_img[:,:,2]]
        S = steer/200.0 + 0.5
        assert(S>=0)
        assert(S<=1)
        steer_lst = [0,0,0,0,0,0,0]
        c = categorize_steer(S)
        assert(c<len(steer_lst))
        assert(c>=0)
        steer_lst[c] = 1.0
        return M_img_lst,C_img_lst,steer_lst

elif run_mode == CAFFE_DEPLOY_MODE:
    img_top_folder = opjh('Desktop/RPi_data')
    _,img_dirs = dir_as_dic_and_list(img_top_folder)
    ctimes = []
    for d in img_dirs:
        ctimes.append(os.path.getmtime(opj(img_top_folder,d)))
    sort_indicies = [i[0] for i in sorted(enumerate(ctimes), key=lambda x:x[1])]
    most_recent_img_dir = img_dirs[sort_indicies[-1]]
    print most_recent_img_dir
    unix(d2s('mkdir -p',opj(img_top_folder,most_recent_img_dir+'_caffe')),False)
    def get_caffe_input_target(img_dic,_ignore1_,_ignore2_,_ignore3_):
        _,img_files = dir_as_dic_and_list(opj(img_top_folder,most_recent_img_dir))
        if len(img_files) > 9:
            img_lst = []
            for i in range(-10,-1): # = [-10, -9, -8, -7, -6, -5, -4, -3, -2]
                # we avoid loading the most recent image to avoid 'race' conditions.
                f = img_files[i]
                #print f
                img = imread_from_img_dic(img_dic,opj(img_top_folder,most_recent_img_dir),f)
                img = img.mean(axis=2)
                img = imresize(img,25)/255.0-0.5
                img_lst.append(img)
            if len(img_files) > 10:
                for f in img_files[:-10]:
                    unix(d2s('mv',opj(img_top_folder,most_recent_img_dir,f),opj(img_top_folder,most_recent_img_dir+'_caffe')),False)
        else:
            dummy = np.random.random((56,75))
            for i in range(9):
                img_lst.append(dummy)
        return img_lst,[0,0,0]

elif run_mode == MC_CAFFE_DEPLOY_MODE:
    img_top_folder = opjh('Desktop/RPi_data')
    _,img_dirs = dir_as_dic_and_list(img_top_folder)
    ctimes = []
    for d in img_dirs:
        ctimes.append(os.path.getmtime(opj(img_top_folder,d)))
    sort_indicies = [i[0] for i in sorted(enumerate(ctimes), key=lambda x:x[1])]
    most_recent_img_dir = img_dirs[sort_indicies[-1]]
    print most_recent_img_dir
    unix(d2s('mkdir -p',opj(img_top_folder,most_recent_img_dir+'_caffe')),False)
    def get_caffe_input_target(img_dic,_ignore1_,_ignore2_,_ignore3_):
        _,img_files = dir_as_dic_and_list(opj(img_top_folder,most_recent_img_dir))
        if len(img_files) > 9:
            M_img_lst = []
            C_img_lst = []
            for i in range(-10,-1): # = [-10, -9, -8, -7, -6, -5, -4, -3, -2]
                # we avoid loading the most recent image to avoid 'race' conditions.
                f = img_files[i]
                #print f
                img = imread_from_img_dic(img_dic,opj(img_top_folder,most_recent_img_dir),f)
                if i == -1:
                    C_img = img.copy()
                    C_img_lst = [C_img[:,:,0],C_img[:,:,1],C_img[:,:,2]]
                img = img.mean(axis=2)
                img = imresize(img,50)/255.0-0.5
                M_img_lst.append(img)
            if len(img_files) > 10:
                for f in img_files[:-10]:
                    unix(d2s('mv',opj(img_top_folder,most_recent_img_dir,f),opj(img_top_folder,most_recent_img_dir+'_caffe')),False)
        else:
            dummy = np.random.random((56,75))
            for i in range(9):
                img_lst.append(dummy)
        return M_img_lst,C_img_lst,[0,0,0]


elif run_mode == USE_GRAPHICS:
    from kzpy3.vis import *
    all_runs_dic = get_all_runs_dic(opjD('/Users/karlzipser/Desktop/RPi3_data/runs_checked'))
    k = sorted(all_runs_dic.keys())
    play_range = (0,15*15)
    some_data = {}
    some_data['current_key'] = k[0]
    some_data['all_runs_dic'] = all_runs_dic
    some_data['play_range'] = play_range

elif run_mode == SAVE_ALL_RUN_DIC:
    from kzpy3.utils import *
    all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    save_obj(all_runs_dic,opjD('RPi3_data/all_runs_dics',CAFFE_DATA.split('/')[-1]))

else:
    print('Unknown mode')
    assert(False)









"""
Top priority items:

second car
second RPi
desktop linux machine
K40 GPU
budget (materials vs salary)
Jetson GPU -- ordered, 22 March 2016
install caffe on RPi: http://www.knight-of-pi.org/deepdreaming-on-a-raspberry-pi-2/
"""

    






