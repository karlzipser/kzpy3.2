print('pytorch2/Data_train_load')
from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg9','kzpy3/pytorch1/train9'])
import data.utils.Segment_Data as Segment_Data
import Parameters as P

hdf5_runs_path = opj(P.BAIR_CAR_DATA_PATH,'hdf5/runs')
hdf5_segment_metadata_path = opj(P.BAIR_CAR_DATA_PATH,'hdf5/segment_metadata')
Segment_Data.load_Segment_Data(hdf5_segment_metadata_path,hdf5_runs_path)



def get_data_considering_high_low_steer(d):
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




def get_data_considering_high_low_steer_and_valid_trajectory_timestamp(d):
    True
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
    if P.other_cars_only and np.random.random() < 0.85: 
        if data == None:
            return None
        if data['other_car_inverse_distances'] == None:
            return None
        if len(data['other_car_inverse_distances']) == 0:
            return None
    return data






