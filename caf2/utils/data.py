"""
Specific functions for getting frame data.
"""
from kzpy3.RPi3.view_drive_data_essentials import *

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

