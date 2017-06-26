from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis2 import *
import data.utils.get_data_with_hdf5 as Segment_Data


bair_car_data_path = opjD('bair_car_data_Main_Dataset')

hdf5_runs_path = opj(bair_car_data_path,'hdf5/runs')
hdf5_segment_metadata_path = opj(bair_car_data_path,'hdf5/segment_metadata')
Segment_Data.load_Segment_Data(hdf5_segment_metadata_path,hdf5_runs_path)


print('\nloading low_steer... (takes awhile)')
low_steer = load_obj(opj(hdf5_segment_metadata_path,'low_steer'))
random.shuffle(low_steer)
print('\nloading high_steer... (takes awhile)')
high_steer = load_obj(opj(hdf5_segment_metadata_path,'high_steer'))
random.shuffle(high_steer)
print('done')
len_high_steer = len(high_steer)
len_low_steer = len(low_steer)
ctr_low = -1
ctr_high = -1
if True:
    figure('high low steer histograms',figsize=(2,1))
    histogram_plot_there = True
    clf()
    plt.hist(array(low_steer)[:,2],bins=range(0,100))
    plt.hist(array(high_steer)[:,2],bins=range(0,100))
    figure(1)


def get_data_considering_high_low_steer(d):
    N_STEPS = d['N_STEPS']
    N_FRAMES = d['N_FRAMES']
    ignore = d['ignore']
    require_one = d['require_one']
    use_states = d['use_states']

    global ctr_low
    global ctr_high
    global low_steer
    global high_steer

    if ctr_low >= len_low_steer:
        ctr_low = -1
    if ctr_high >= len_high_steer:
        ctr_high = -1
    if ctr_low == -1:
        random.shuffle(low_steer)
        ctr_low = 0
    if ctr_high == -1:
        random.shuffle(high_steer)
        ctr_high = 0
    if random.random() < 0.5:
        choice = low_steer[ctr_low]
        ctr_low += 1
    else:
        choice = high_steer[ctr_high]
        ctr_high += 1

    run_code = choice[3]
    seg_num = choice[0]
    offset = choice[1]

    data = Segment_Data.get_data(run_code,seg_num,offset,3*N_STEPS,offset+0,N_FRAMES,ignore=ignore,require_one=require_one,use_states=use_states)

    return data

