"""
Top priority items:

second car
second RPi
desktop linux machine
K40 GPU
budget (materials vs salary)

Jetson GPU


review of runs
09Feb16_12h10m58s_scl=25_mir=1 bad for training
09Feb16_13h37m22s_scl=25_mir=0 good to 1500

09Feb16_13h40m42s_scl=25_mir=0 good to 2600
10Feb16_08h25m38s_scl=25_mir=0 delete
10Feb16_08h31m21s_scl=25_mir=0 good to 2400
10Feb16_08h56m14s_scl=25_mir=0 good to 3500
10Feb16_09h03m26s_scl=25_mir=0 problem with very high rps with wheels of ground around delete 4829 to 4876
10Feb16_09h15m53s_scl=25_mir=0 problem with very high rps with wheels of ground around delete 8185 to 8215

13Feb16_08h29m40s_scl=25_mir=0 delete
13Feb16_18h09m00s_scl=25_mir=0 too dark
13Feb16_18h17m34s_scl=25_mir=0 too dark
14Feb16_11h34m14s_scl=25_mir=0 delete
14Feb16_12h43m16s_scl=25_mir=0 delete
14Feb16_15h00m14s_scl=25_mir=0 delete

09Feb16_14h19m10s_scl=25_mir=0 good to 6400

14Feb16_17h33m13s_scl=25_mir=0 delete 23179 to 23227

"""
from kzpy3.utils import *

<<<<<<< HEAD
USE_GRAPHICS = False
CAFFE_TRAINING_MODE = True
#CAFFE_FRAME_RANGE = (-15,-6)
CAFFE_FRAME_RANGE = (-7,-6)
#CAFFE_DATA = opjD('RPi3_data/runs_scale_50_BW')
CAFFE_DATA = opjD('RPi3_data/runs_scl_100_RGB')

=======
USE_GRAPHICS = True

CAFFE_TRAINING_MODE = False#

from kzpy3.utils import *
>>>>>>> 91f27f09d48b6d80e461f48b1636f7ae2a077f65

if USE_GRAPHICS:
    from kzpy3.vis import *

def get_run_data(run_path):
    print('get_run_data')
    _,l=dir_as_dic_and_list(run_path)
    index = []
    timestamp = []
    steer = []
    speed = []
    rps = []
    left_range = []
    right_range = []
    rand_control = []
    for m in l:
        n = m.split('_')
        p = n[0]
        index.append(int(p))
        p = n[1]
        timestamp.append(float(p))
        p = n[2].split('=')[1]
        steer.append(float(p)/100.0)
        p = n[3].split('=')[1]
        speed.append(float(p)/100.0)
        p = n[4].split('=')[1]
        rps.append(float(p)/10.0)
        p = n[5].split('=')[1]
        left_range.append(int(p))
        p = n[6].split('=')[1]
        right_range.append(int(p))
        p = n[7].split('=')[1]
        rand_control.append(int(p))
    run_data_dic = {}
    run_data_dic['run_path'] = run_path
    run_data_dic['img_lst'] = l
    run_data_dic['index'] = np.array(index)
    run_data_dic['timestamp'] = np.array(timestamp) - timestamp[0]
    run_data_dic['steer'] = np.array(steer)
    run_data_dic['speed'] = np.array(speed)
    run_data_dic['rps'] = np.array(rps)
    run_data_dic['left_range'] = np.array(left_range)
    run_data_dic['right_range'] = np.array(right_range)
    run_data_dic['rand_control'] = np.array(rand_control)
    deltas = [0]
    max_thresh = 3.0
    for i in range(1,len(run_data_dic['timestamp'])):
        d = run_data_dic['timestamp'][i]-run_data_dic['timestamp'][i-1]
        d = min(max_thresh,d)
        deltas.append(d)
    run_data_dic['timestamp_deltas'] = np.array(deltas)
    run_data_dic['frames_to_next_turn'] = frames_to_next_turn(run_data_dic,steer_thresh=0.1,max_thresh=100)
    lockout = []
    for i in range(len(run_data_dic['timestamp'])):
        d = 1
        if run_data_dic['timestamp_deltas'][i] > 0.14:
            d = 0
        if run_data_dic['rps'][i] < 0.1:
            d = 0
        lockout.append(d)
    run_data_dic['data_lockout'] = np.array(lockout)
    back_frame_range = (-5+-9,10)
    good = 0 * run_data_dic['data_lockout']
    print np.shape(run_data_dic['data_lockout'])
    for i in range(-back_frame_range[0],len(run_data_dic['timestamp'])+back_frame_range[0]):
        if run_data_dic['rand_control'][i] == 0:
            g = 1
            #print((-back_frame_range[0],len(run_data_dic['timestamp'])+back_frame_range[0]),(i+back_frame_range[0],i+back_frame_range[1]))
            for j in range(i+back_frame_range[0],i+back_frame_range[1]-1):
                if run_data_dic['data_lockout'][j] == 0:
                    g = 0
            good[i] = g
    run_data_dic['train_frames'] = good
    dsteer = 0.0 * run_data_dic['steer']
    for i in range(1,len(run_data_dic['steer'])):
        dsteer[i] = run_data_dic['steer'][i] - run_data_dic['steer'][i-1]
    run_data_dic['dsteer'] = dsteer
    return run_data_dic



def get_all_runs_dic(RPi3_data_path):
    all_runs_dic,_ = dir_as_dic_and_list(RPi3_data_path)
    for k in all_runs_dic:
        print k
        all_runs_dic[k] = get_run_data(opj(RPi3_data_path,k))
    return all_runs_dic



def imread_from_img_dic(img_dic,path,fname):
    if fname not in img_dic:
        img_dic[fname] = imread(opj(path,fname))
    return img_dic[fname]


####################
def run_to_scaled_BW(img_dic,run_data_dic,scale_percent,mirror=False):
    mirror_str = '_mir=0'
    if mirror:
        mirror_str = '_mir=1'
    dst_path = d2n(run_data_dic['run_path'],'_scl=',scale_percent,mirror_str)
    unix(d2s('mkdir -p',dst_path))
    _,l=dir_as_dic_and_list(run_data_dic['run_path'])
    for m in l:
        n = m.split('_')
        p = int(n[2].split('=')[1])
        img = imread_from_img_dic(img_dic,run_data_dic['run_path'],m)
        img_scaled = imresize(img,scale_percent)
        img_scaled = img_scaled.mean(axis=2)
        if mirror:
            p = -p
            img_scaled = np.fliplr(img_scaled)
        n[2] = d2n('str=',p)
        f = '_'.join(n)
        f0 = f.split('_')
        f2 = f.replace('.jpg',d2n('scl=',scale_percent,mirror_str,'_.png'))
        #print(d2s(m,'to',f2))
        imsave(opj(dst_path,f2),img_scaled)

def scale_BW_mirror_all_runs(img_dic,all_runs_dic,scale_percent):
    for k in all_runs_dic:
        print k
        for mirror in [False,True]:
            print mirror
            run_to_scaled_BW(img_dic,all_runs_dic[k],scale_percent,mirror)




def run_to_scaled_color_mod(img_dic,run_data_dic,scale_percent,mirror=False,to_BW=False):
    mirror_str = '_mir=0'
    if mirror:
        mirror_str = '_mir=1'
    dst_path = d2n(run_data_dic['run_path'],'_scl=',scale_percent,mirror_str)
    unix(d2s('mkdir -p',dst_path))
    _,l=dir_as_dic_and_list(run_data_dic['run_path'])
    for m in l:
        n = m.split('_')
        p = int(n[2].split('=')[1])
        img = imread_from_img_dic(img_dic,run_data_dic['run_path'],m)
        if scale_percent < 100:
            img_scaled = imresize(img,scale_percent)
        else:
            img_scaled = img
        if to_BW:
            img_scaled = img_scaled.mean(axis=2)
        if mirror:
            p = -p
            img_scaled = np.fliplr(img_scaled)
        n[2] = d2n('str=',p)
        f = '_'.join(n)
        f0 = f.split('_')
        if scale_percent <= 50:
            extension = '_.png'
        else:
            extension = '_.jpg'            
        f2 = f.replace('.jpg',d2n('scl=',scale_percent,mirror_str,extension))
        #print(d2s(m,'to',f2))
        imsave(opj(dst_path,f2),img_scaled)

def scale_color_mod_mirror_all_runs(img_dic,all_runs_dic,scale_percent,to_BW=False):
    for k in all_runs_dic:
        print k
        for mirror in [False,True]:
            print mirror
            run_to_scaled_color_mod(img_dic,all_runs_dic[k],scale_percent,mirror,to_BW)

####################




def frames_to_next_turn(run_data_dic,steer_thresh=0.1,max_thresh=100):
    m = 0 * run_data_dic['steer']
    len_steer = len(run_data_dic['steer'])
    for i in range(len_steer):
        ctr = i
        for j in range(i,len_steer):
            if np.abs(run_data_dic['steer'][j]) > steer_thresh:
                break
            elif run_data_dic['rps'][j] > 0:
                ctr += 1
        m[i] = min(ctr-i,max_thresh)
    return m




def plot_run(all_runs_dic,key_index):
    global some_data
    ky = sorted(all_runs_dic.keys())[key_index]
    print ky
    some_data['current_key'] = ky
    run_data_dic = all_runs_dic[ky]
    fig = plt.figure(1,figsize=(7,2))
    plt.clf()
    plt.ion()
    plt.show()
    fig.canvas.mpl_connect('button_press_event', button_press_event)
    ts = run_data_dic['timestamp']
    fps = len(ts)/ts[-1]
    indx = 0
    ctr = 1
    while indx < len(ts):
        indx = fps*60*ctr
        plt.plot([indx,indx],[-1,3],'lightgray')
        ctr += 1
    plt.xlim([0,len(ts)])
    plt.plot(run_data_dic['steer'],'b',label='steer')
    #plt.plot(run_data_dic['dsteer'],'r',label='dsteer')
    plt.plot(2.5+run_data_dic['rand_control']/4.0,'r',label='rand_control')
    #plt.plot(run_data_dic['left_range']/100.0,'go',label='left_range')
    #plt.plot(run_data_dic['right_range']/100.0,'ro',label='right_range')
    plt.plot(run_data_dic['speed'],'k',label='speed')
    plt.plot(run_data_dic['rps']/3.0,'g',label='rps/3')
    plt.plot(run_data_dic['timestamp_deltas']-0.9,'r',label='timestamp_deltas')
    plt.plot(run_data_dic['frames_to_next_turn']/100.0+2.0,'y',label='frames_to_next_turn')
    #plt.plot(run_data_dic['data_lockout']/4.0-0.5,'k',label='data_lockout')
    plt.plot(run_data_dic['train_frames']/4.0+1.5,'c',label='train_frames')
    plt.title(run_data_dic['run_path'].split('/')[-1])
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.ylim(-1.5,3.5)
    #plt.figure(3);plt.clf();
    #plt.hist(all_runs_dic[some_data['current_key']]['timestamp_deltas'],100);
    #plot_run_timestamp_deltas(run_data_dic,max_thresh=3)





def animate_frames(run_data_dic,start_frame,end_frame,fig,title=''):
    for x in range(start_frame,end_frame):
        f = run_data_dic['img_lst'][x]
        r = run_data_dic['rand_control'][x]
        dlo = run_data_dic['data_lockout'][x]
        img = imread(opj(run_data_dic['run_path'],f))
        if len(np.shape(img)) > 2:
            if r > 0:
                img[:,:,1:] *= 0.5
            if dlo == 0:
                img[:,:,[0,1]] *= 0.5
        plt.figure(fig)
        plt.clf()
        mi(img,fig,img_title=title)
        plt.pause(0.0001)


def button_press_event(event):
    current_key = some_data['current_key']
    all_runs_dic = some_data['all_runs_dic']
    play_range = some_data['play_range']
    plt.figure(1)
    plt.plot([event.xdata+play_range[0],event.xdata+play_range[1]],[2,2],'k')
    run_data_dic = all_runs_dic[current_key]
    animate_frames(run_data_dic,np.int(np.floor(event.xdata))+play_range[0],np.int(np.floor(event.xdata))+play_range[1],2)

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
    sbks = steer_bins.keys() + ['center']
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
    """
    if Graphics:
        for f in frame_names:
            img = imread(f)
            plt.figure(9)
            plt.clf()
            mi(img,9)
            plt.pause(0.0001)
    """
    return (b,r,n,steer,frames_to_next_turn,rps,frame_names)


if CAFFE_TRAINING_MODE:
    def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=CAFFE_FRAME_RANGE):
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
        F = frames_to_next_turn/45.0
        F = min(F,1.0)
        assert(F>=0)
        assert(F<=1)
        R = rps/75.0
        R = min(R,1.0)
        assert(R>=0)
        assert(R<=1)
        return img_lst,[S,0*F,0*R] #steer only, 17 Feb 2015 trianing
        #return img_lst,[S,F,R]
else:
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

"""    
current_key = '14Feb16_17h33m13s_scl=25_mir=0'
INDEX = 2000
def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-15,-6)):
    global INDEX
    run_data_dic = all_runs_dic[current_key]
    img_lst = []
    for i in range(INDEX,INDEX+9):
        img_lst.append(imread_from_img_dic(img_dic,run_data_dic['run_path'],run_data_dic['img_lst'][i])/255.0-0.5)
    INDEX += 1
    return img_lst,[0,0,0]
"""
"""
for j in range(100):
    il,tl=get_caffe_input_target_(img_dic,steer_bins,all_runs_dic,(-15,-6));
    for img in il:
        plt.figure(9)
        plt.clf()
        mi(img,9,img_title=d2s(INDEX))
        plt.pause(0.0001)
"""
"""
from kzpy3.caf.training.y2016.m2.from_mnist.original_with_accuracy.train import *
solver.net.copy_from(opjh('/Users/karlzipser/scratch/2016/2/16/caffe/models/from_mnist/steer_only/model_iter_3200000.caffemodel'))
for i in range(1000): test_solver2(solver)
"""

####################################################


img_dic = {}

if CAFFE_TRAINING_MODE:
    all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    steer_bins = get_steer_bins(all_runs_dic)
else:
    all_runs_dic = {}
    steer_bins = {}


if USE_GRAPHICS:
<<<<<<< HEAD
    all_runs_dic = get_all_runs_dic(opjD('RPi3_data/runs_new'))
=======
    all_runs_dic = get_all_runs_dic(opjD('/Users/karlzipser/Desktop/RPi_data/caffe'))
>>>>>>> 91f27f09d48b6d80e461f48b1636f7ae2a077f65
    k = sorted(all_runs_dic.keys())
    play_range = (0,15*15)
    some_data = {}
    some_data['current_key'] = k[0]
    some_data['all_runs_dic'] = all_runs_dic
    some_data['play_range'] = play_range




