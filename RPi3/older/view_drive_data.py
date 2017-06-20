
from kzpy3.vis import *

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
    deltas = [0]
    for i in range(1,len(run_data_dic['timestamp'])):
        d = run_data_dic['timestamp'][i]-run_data_dic['timestamp'][i-1]
        d = min(max_thresh,d)
        deltas.append(d)
    run_data_dic['timestamp_deltas'] = np.array(deltas)
    return run_data_dic


def get_all_runs_dic(RPi3_data_path):
    all_runs_dic,_ = dir_as_dic_and_list(RPi3_data_path)
    for k in all_runs_dic:
        all_runs_dic[k] = get_run_data(opj(RPi3_data_path,k))
    return all_runs_dic

def frames_to_next_turn(run_data_dic,steer_thresh=0.1):
    m = 0 * run_data_dic['steer']
    len_steer = len(run_data_dic['steer'])
    for i in range(len_steer):
        ctr = i
        for j in range(i,len_steer):
            if np.abs(run_data_dic['steer'][j]) > steer_thresh:
                break
            elif run_data_dic['rps'][j] > 0:
                ctr += 1
        m[i] = ctr-i
    return m



def plot_run(run_data_dic):
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
    plt.plot(2.5+run_data_dic['rand_control']/4.0,'r',label='rand_control')
    plt.plot(run_data_dic['speed'],'k',label='speed')
    plt.plot(run_data_dic['rps']/3.0,'g',label='rps/3')
    plt.plot(run_data_dic['timestamp_deltas'],'r',label='timestamp_deltas')
    plt.title(run_data_dic['run_path'].split('/')[-1])
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plot_run_timestamp_deltas(run_data_dic,max_thresh=3)

"""
def plot_run_timestamp_deltas(run_data_dic,max_thresh=1):
    deltas = [0]
    for i in range(1,len(run_data_dic['timestamp'])):
        d = run_data_dic['timestamp'][i]-run_data_dic['timestamp'][i-1]
        d = min(max_thresh,d)
        deltas.append(d)
    plot(deltas,'r')
    return deltas
"""

current_key = ''
all_runs_dic = {}
some_data = {}

def button_press_event(event):
    current_key = some_data['current_key']
    all_runs_dic = some_data['all_runs_dic']
    play_range = some_data['play_range']
    plt.figure(1)
    plt.plot([event.xdata+play_range[0],event.xdata+play_range[1]],[2,2],'k')
    for x in range(np.int(np.floor(event.xdata))+play_range[0],np.int(np.floor(event.xdata))+play_range[1]):
        run_data_dic = all_runs_dic[current_key]
        f = run_data_dic['img_lst'][x]
        r = run_data_dic['rand_control'][x]
        #print f
        img = imread(opj(run_data_dic['run_path'],f))
        if r > 0:
            img[:,:,1:] *= 0.5
        #plt.figure(1).add_subplot(2,3,5)
        #plt.cla()
        figure(2)
        plt.clf()
        mi(img,2)#1,[2,3,5])
        plt.pause(0.0001)



"""
run_data_dic = all_runs_dic[some_data['current_key']]
m = frames_to_next_turn(run_data_dic)
plt.figure(5)
plt.clf()
plt.plot(m)
plt.xlim([0,len(m)])



"""



all_runs_dic = get_all_runs_dic(opjD('RPi3_data/runs'))
k = sorted(all_runs_dic.keys())
  
play_range = (0,9)
some_data['current_key'] = k[-1]
some_data['all_runs_dic'] = all_runs_dic
some_data['play_range'] = play_range

"""
plt.clf()
fig = plt.figure(1,figsize=(7,2))
plt.ion()
plt.show()
fig.canvas.mpl_connect('button_press_event', button_press_event)
plot_run(all_runs_dic[some_data['current_key']])
"""



