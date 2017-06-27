from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg9','kzpy3/pytorch1/train9'])
from vis2 import *
import data.utils.get_data_with_hdf5 as Segment_Data
import Parameters as P


hdf5_runs_path = opj(P.bair_car_data_path,'hdf5/runs')
hdf5_segment_metadata_path = opj(P.bair_car_data_path,'hdf5/segment_metadata')
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
    pause(0.001)
    #figure(1)


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




def prepare_Aruco_trajectory_data():

    CS_('load aruco trajectory data')
    Aruco_Steering_Trajectories = {}
    aruco_data_location = opjD('output_data')
    paths = sggo(aruco_data_location,'*.pkl')
    for i in range(len(paths)):
        o = paths[i]
        ast = lo(o)
        for run_name in ast.keys(): 
            print(d2n(run_name,' (',i+1,' of ',len(paths),')'))
            if run_name not in Aruco_Steering_Trajectories:
                Aruco_Steering_Trajectories[run_name] = {}
            if len(ast[run_name].keys()) > 4:
                print_stars()
                continue
            for mode in ast[run_name].keys():
                print('\t'+mode)
                if mode not in Aruco_Steering_Trajectories[run_name]:
                    Aruco_Steering_Trajectories[run_name][mode] = {}
                timestamps = ast[run_name][mode]['near_t']
                dd = ast[run_name][mode]['desired_direction'][0]
                print('\t\t'+str(dd))
                Aruco_Steering_Trajectories[run_name][mode][dd] = {}
                for i in range(len(timestamps)):
                    t = timestamps[i]
                    Aruco_Steering_Trajectories[run_name][mode][dd][t] = {}
                    for topic in ast[run_name][mode].keys():
                        if topic not in ['near_t','desired_direction']:
                            q = ast[run_name][mode][topic][i]
                            if not(is_number(q)):
                                q = array(q)
                                q = q.astype(np.float16)
                            else:
                                q = np.float16(q)
                            Aruco_Steering_Trajectories[run_name][mode][dd][t][topic] = q
    ctr = 0
    for run_name in Aruco_Steering_Trajectories.keys():
        if 'flip_' in run_name:
            del Aruco_Steering_Trajectories[run_name]
            continue
        flip = 'flip_'+run_name
        print(d2n(flip,' (',ctr+1,' of ',len(paths),')'))
        ctr += 1
        Aruco_Steering_Trajectories[flip]= {}
        for mode in Aruco_Steering_Trajectories[run_name]:
            Aruco_Steering_Trajectories[flip][mode] = {}
            for dd in [0,1]:
                Aruco_Steering_Trajectories[flip][mode][dd] = {}
                for t in Aruco_Steering_Trajectories[run_name][mode][dd].keys():
                    Aruco_Steering_Trajectories[flip][mode][dd][t] = {}
                    Aruco_Steering_Trajectories[flip][mode][dd][t]['steer'] = np.float16(99-Aruco_Steering_Trajectories[run_name][mode][dd][t]['steer'])
                    Aruco_Steering_Trajectories[flip][mode][dd][t]['velocity'] = np.float16(Aruco_Steering_Trajectories[run_name][mode][dd][t]['velocity'])
                    l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['other_car_inverse_distances'])
                    l.reverse(); l = array(l); l = l.astype(np.float16)
                    Aruco_Steering_Trajectories[flip][mode][dd][t]['other_car_inverse_distances'] = l
                    l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['marker_inverse_distances'])
                    l.reverse(); l = array(l); l = l.astype(np.float16)
                    Aruco_Steering_Trajectories[flip][mode][dd][t]['marker_inverse_distances'] = l
                    l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['potential_values'])
                    l.reverse(); l = array(l); l = l.astype(np.float16)
                    Aruco_Steering_Trajectories[flip][mode][dd][t]['potential_values'] = l

                    l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['clock_potential_values'])
                    l.reverse(); l = array(l); l = l.astype(np.float16)
                    Aruco_Steering_Trajectories[flip][mode][dd][t]['clock_potential_values'] = l

                    if dd == 0:
                        Aruco_Steering_Trajectories[flip][mode][dd][t]['desired_direction'] = 1
                    else:
                        Aruco_Steering_Trajectories[flip][mode][dd][t]['desired_direction'] = 0
                    Aruco_Steering_Trajectories[flip][mode][dd][t]['relative_heading'] =  np.float16(360 - Aruco_Steering_Trajectories[run_name][mode][dd][t]['relative_heading'])

    unix('mkdir -p '+opjD('Aruco_Steering_Trajectories'))
    ctr = 0
    for run_name in sorted(Aruco_Steering_Trajectories.keys()):
        print(d2n(run_name,' (',ctr+1,' of ',len(paths),')'))
        so(Aruco_Steering_Trajectories[run_name],opjD('Aruco_Steering_Trajectories',run_name))
        ctr += 1
    raw_input('enter')




def load_Aruco_Steering_Trajectories():
    print("Loading Aruco_Steering_Trajectories . . .")
    paths = sggo(opjD('Aruco_Steering_Trajectories','*.pkl'))
    Aruco_Steering_Trajectories = {}
    ctr = 0
    for p in paths:
        o = lo(p)
        run_name = fname(p).replace('.pkl','')
        print(d2n(run_name,' (',ctr+1,' of ',len(paths),')'))
        Aruco_Steering_Trajectories[run_name] = o
        ctr += 1
    return Aruco_Steering_Trajectories






if True:
    Aruco_Steering_Trajectories = load_Aruco_Steering_Trajectories()








def get_data_considering_high_low_steer_and_valid_trajectory_timestamp(d):
    N_STEPS = d['N_STEPS']
    N_FRAMES = d['N_FRAMES']
    ignore = d['ignore']
    require_one = d['require_one']
    use_states = d['use_states']
    
    global ctr_low
    global ctr_high
    global low_steer
    global high_steer
    global counts
    global high_loss_key_ctr
    global high_loss_keys

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

    run_name = Segment_Data.Segment_Data['run_codes'][run_code]

    if run_name not in Aruco_Steering_Trajectories.keys():
        #print('Run name '+run_name+' not in Aruco_Steering_Trajectories')
        return None
    if len(Aruco_Steering_Trajectories[run_name].keys()) < 2:
        #print('len(Aruco_Steering_Trajectories[run_name].keys()) <= 2')
        return None

    seg_num_str = str(seg_num)
    aruco_matches = []

    for i in [0]:#range(N_FRAMES):
        timestamp = Segment_Data.Segment_Data['runs'][run_name]['segments'][seg_num_str]['left_timestamp'][offset+i]
        behavioral_mode = np.random.choice(
            ['Direct_Arena_Potential_Field',
            #'Furtive_Arena_Potential_Field',
            'Follow_Arena_Potential_Field'])
            #'Play_Arena_Potential_Field'])
        desired_direction = np.random.choice([0,1])

        if timestamp in Aruco_Steering_Trajectories[run_name][behavioral_mode][desired_direction].keys():
            aruco_matches.append(timestamp)
        if len(aruco_matches) < 1:
            return None
    data = Segment_Data.get_data(run_code,seg_num,offset,N_STEPS,offset+0,N_FRAMES,ignore=ignore,require_one=require_one)
    if data != None:
        data['behavioral_mode'] = behavioral_mode
        data['desired_direction'] = desired_direction
        for topic in Aruco_Steering_Trajectories[run_name][behavioral_mode][desired_direction][timestamp]:
            data[topic] = Aruco_Steering_Trajectories[run_name][behavioral_mode][desired_direction][timestamp][topic]
        data['id'] = (run_name,behavioral_mode,desired_direction,timestamp,run_code,seg_num,offset)
    if P.other_cars_only and np.random.random() < 0.90: 
        if data == None:
            return None
        if data['other_car_inverse_distances'] == None:
            return None
        if len(data['other_car_inverse_distances']) == 0:
            return None
    return data






