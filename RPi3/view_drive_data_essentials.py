from kzpy3.utils import *
if host_name != 'redwood2':
    from kzpy3.vis import *

img_dic = {}
steer_bins = {}
all_runs_dic = {}
some_data = {}

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

def imread_from_img_dic(img_dic,path,fname,use_dic=False):
    if use_dic:
        if fname not in img_dic:
            img_dic[fname] = imread(opj(path,fname))
        else:
            print(fname)
        return img_dic[fname]
    else:
        return imread(opj(path,fname))

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

###### To process to 50% scale BW and 100% scale RGB #######################
# scale_color_mod_mirror_all_runs(img_dic,all_runs_dic,50,to_BW=True)
# scale_color_mod_mirror_all_runs(img_dic,all_runs_dic,100,to_BW=False)
###########################################################################
# all_runs_dic = get_all_runs_dic('/Users/karlzipser/Desktop/RPi3_data/runs_original')
# scale_color_mod_mirror_all_runs(img_dic,all_runs_dic,25,to_BW=True)
#  save_obj(all_runs_dic,'/Users/karlzipser/Desktop/RPi3_data/all_runs_dics/runs_scale_50_BW_test')

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
    plt.ylim(-1.3,3.5)
    #plt.figure(3);plt.clf();
    #plt.hist(all_runs_dic[some_data['current_key']]['timestamp_deltas'],100);
    #plot_run_timestamp_deltas(run_data_dic,max_thresh=3)

def animate_frames(run_data_dic,start_frame,end_frame,fig,title=''):
    for x in range(start_frame,end_frame):
        f = run_data_dic['img_lst'][x]
        r = run_data_dic['rand_control'][x]
        dlo = run_data_dic['data_lockout'][x]
        img = imread(opj(run_data_dic['run_path'],f))
        #print((img.max(),img.min()))
        if len(np.shape(img)) > 2:
            if r > 0:
                img[:,:,1:] *= 0.5
            if dlo == 0:
                img[:,:,[0,1]] *= 0.5
        #img = 255-img
        #img = img[-28:,:]
        plt.figure(fig)
        plt.clf()
        mi(img,fig,img_title=title)
        plt.pause(0.0001)

def animate_and_save_frames(run_data_dic,start_frame,end_frame,fig,title='',save_path=''):
    ctr = 0
    if len(save_path) > 0:
        unix(d2n('mkdir -p ',save_path))
    if end_frame < 0:
        end_frame = len(run_data_dic['img_lst'])
    img = zeros((250,300,3))
    for x in range(start_frame,end_frame):
        f = run_data_dic['img_lst'][x]
        r = run_data_dic['rand_control'][x]
        dlo = run_data_dic['data_lockout'][x]
        img_ = imread(opj(run_data_dic['run_path'],f))
        img *= 0
        s = (run_data_dic['steer'][x] + run_data_dic['steer'][x-1] ) /2.0
        #print s
        if s >= 0:
            a,b = 150,150+300*s
        else:
            a,b = 150+(300*s),150
        #print a,b
        img[224:,a:b,0] = 1
        img[224:,149:151,2] = 1
        img[0:225,:,:] = img_ / 255.0
        plt.figure(fig)
        plt.clf()
        mi(img,fig,img_title=title)
        if len(save_path) > 0:
            imsave(opj(save_path,d2n(ctr,'.png')),img)
        ctr += 1
        plt.pause(0.0001)


def button_press_event(event):
    current_key = some_data['current_key']
    all_runs_dic = some_data['all_runs_dic']
    play_range = some_data['play_range']
    plt.figure(1)
    plt.plot([event.xdata+play_range[0],event.xdata+play_range[1]],[2,2],'k')
    run_data_dic = all_runs_dic[current_key]
    animate_frames(run_data_dic,np.int(np.floor(event.xdata))+play_range[0],np.int(np.floor(event.xdata))+play_range[1],2)


def get_frame_pairs(all_runs_dic,key_index,dst):
    """
    all_runs_dic = get_all_runs_dic('/Users/karlzipser/Desktop/RPi3_data/runs_caffe')
    k = sorted(all_runs_dic.keys())
    indx = 0
    dst = opjD(all_runs_dic[k[indx]]['run_path'].split('/')[-1]+'_frames')
    get_frame_pairs(all_runs_dic,indx,dst)

    """
    global some_data
    unix(d2s('mkdir -p',dst))
    ky = sorted(all_runs_dic.keys())[key_index]
    print ky
    some_data['current_key'] = ky
    run_data_dic = all_runs_dic[ky]
    #frame_lst = []
    for i in range(len(run_data_dic['img_lst'])):
        print i
        r = imread(opj(run_data_dic['run_path'],run_data_dic['img_lst'][i]))
        r = z2o(r)
        bw = z2o(imresize(imresize(r.mean(axis=2),25),(225,300),'nearest'))
        c = np.zeros((225,620,3))
        c[:,:300,:] = r
        for j in [0,1,2]:
            c[:,320:,j]=bw
        c = c[:-1,:,:]
        imsave(opj(dst,d2n(i,'.png')),c)
    #return frame_lst

"""
elif run_mode == USE_GRAPHICS:
    from kzpy3.vis import *
    all_runs_dic = get_all_runs_dic(opjD('/Users/karlzipser/Desktop/RPi3_data/runs_checked'))
    k = sorted(all_runs_dic.keys())
    play_range = (0,15*1)
    
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






