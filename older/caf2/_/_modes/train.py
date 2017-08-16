from kzpy3.caf2.utils.data import *

info_file = 'kzpy3/caf2/tmp/__info__.py'
c = txt_file_to_list_of_strings(opjh(info_file))
for e in c: exec(e)
#unix('rm '+info_file)

to_do_str = """
if 'all_runs_dics' in CAFFE_PHASE_DATA:
    all_runs_dic_PHASE = load_obj(CAFFE_PHASE_DATA)
else: 
    all_runs_dic_PHASE = get_all_runs_dic(CAFFE_PHASE_DATA)
steer_bins_PHASE = get_steer_bins(all_runs_dic_PHASE)
"""
for phase in ['TRAIN','TEST']:
    lsr = to_do_str.replace('PHASE',phase)
    exec(lsr)

def process_frames(frame_names):
    img_lst = []
    reverse_contrast = False
    if USE_JITTER:
        jitx = np.floor(np.random.random()*jitter)
        jity = np.floor(np.random.random()*jitter)
    if USE_REVERSE_CONTRAST:
        if np.random.random() < 0.5:
            reverse_contrast = True
    for f in frame_names:
        img = imread(f)/255.0-0.5
        if reverse_contrast:
            img = -img
        if USE_BOTTOM_HALF:
            img = img[np.floor(shape(img)[0]/2):,:]
        if USE_JITTER:
            img = img[jity:(jity+input_size[2]),jitx:(jitx+input_size[3])]
        img_lst.append(img)
    if len(img_lst) == 1 and len(np.shape(img_lst[0])) == 3:
        img = img_lst[0]
        img_lst = [img[:,:,0],img[:,:,1],img[:,:,2]]
    return img_lst

def get_caffe_input_target(steer_bins,all_runs_dic,frame_range):
    b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
    b_,r_,n_,steer_,frames_to_next_turn_,rps_,noise_frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
    img_lst = process_frames(frame_names)
    noise_img_lst = process_frames(noise_frame_names)
    noise_p1 = 0.33333
    noise_p2 = np.random.random()*noise_p1
    for i in range(len(img_lst)):
        img_lst[i] = (1.0-noise_p2)*img_lst[i] + noise_p2*noise_img_lst[i]
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
    return img_lst,[S,0,0]

