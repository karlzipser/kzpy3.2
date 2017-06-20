
from kzpy3.vis import *

#  rdd = get_run_data('/Users/karlzipser/Desktop/RPi3_data/10Feb16_13h31m38s')

fig = plt.figure(figsize=(15,3))
#ax = fig.add_axes([0, 0, 1, 1], frameon=False)

# 0_1455048664.8_str=0_spd=0_rps=0_lrn=36_rrn=100_rnd=0_


def get_run_data(run_path):
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
    return run_data_dic

def get_all_runs_dic(RPi3_data_path):
    all_runs_dic,_ = dir_as_dic_and_list(RPi3_data_path)
    for k in all_runs_dic:
        all_runs_dic[k] = get_run_data(opj(RPi3_data_path,k))
    return all_runs_dic

def plot_run(run_data_dic):
    plt.ion()
    plt.clf()
    ts = run_data_dic['timestamp']
    fps = len(ts)/ts[-1]
    indx = 0
    ctr = 1
    while indx < len(ts):
        indx = fps*60*ctr
        plt.plot([indx,indx],[-1,3],'lightgray')
        ctr += 1
    plt.xlim([0,len(ts)])
    plot_run_timestamp_deltas(run_data_dic,max_thresh=3)
    plt.plot(run_data_dic['steer'],'k',label='steer')
    plt.plot(run_data_dic['rand_control']/4.0,'r',label='rand_control')
    plt.plot(run_data_dic['speed'],'b',label='speed')
    plt.plot(run_data_dic['rps']/3.0,'g',label='rps/3')
    plt.title(run_data_dic['run_path'].split('/')[-1])
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()

def test_run_timing(run_data_dic):
    index_errors = 0
    time_stamp_errors = 0
    for i in range(1,len(run_data_dic['index'])):
        if not run_data_dic['index'][i]>run_data_dic['index'][i-1]:
            index_errors += 1
            print i
        if not run_data_dic['timestamp'][i]>run_data_dic['timestamp'][i-1]:
            time_stamp_errors += 1
            print i
            plot(i,0,'o')
    print(index_errors,time_stamp_errors)

def plot_run_timestamp_deltas(run_data_dic,max_thresh=1):
    deltas = [0]
    for i in range(1,len(run_data_dic['timestamp'])):
        d = run_data_dic['timestamp'][i]-run_data_dic['timestamp'][i-1]
        d = min(max_thresh,d)
        deltas.append(d)
    plot(deltas,'o')
    return deltas


def button_press_event(event):
    for x in range(np.int(np.floor(event.xdata))+play_range[0],np.int(np.floor(event.xdata))+play_range[1]):
        run_data_dic = all_runs_dic[current_key]
        f = run_data_dic['img_lst'][x]
        r = run_data_dic['rand_control'][x]
        print f
        img = imread(opj(run_data_dic['run_path'],f))
        if r > 0:
            img[:,:,1:] *= 0.5
        plt.figure(10)
        plt.clf()
        plt.ion()
        mi(img,10,img_title=d2s(x))
        plt.pause(0.01)
    plt.figure(1)
    
"""
5884
5888
5916
5955
5967
6001
6010
6018
6029
6059
6094
6157
6164
6198
6204
6240
6242
6425
6433
6450
6461
6475
6605
6626

play_range = (0,5*30)
fig.canvas.mpl_connect('button_press_event', button_press_event)

all_runs_dic = get_all_runs_dic(opjD('RPi3_data/runs'))
current_key=k[-1];plot_run(all_runs_dic[current_key])
k = sorted(all_runs_dic.keys())
current_key = k[0]
plot_run(all_runs_dic[k[0]])

for r in k:
    print r
    try:
        test_run_timing(all_runs_dic[r])
    except Exception,e:
        print e
"""
)

