from kzpy3.utils2 import *
import cv2

def get_new_Data_dic(_=None):
    D = {}
    D['STOP_LOADER_THREAD'] = False
    D['STOP_ANIMATOR_THREAD'] = False
    D['STOP_GRAPH_THREAD'] = False
    D['d_indx'] = 1.0
    D['current_img_index'] = -D['d_indx']
    D['t_previous'] = 0
    D['left_deltas'] = []
    D['scale'] = 1#4.0
    D['delay'] = None
    D['steer'] = []
    D['state'] = []
    D['SMOOTHING'] = True
    D['motor'] = []
    D['images'] = []
    D['left'] = []
    D['right'] = []
    D['meta'] = None
    D['color_mode'] = cv2.COLOR_RGB2BGR
    D['save_start_index'] = 0
    D['save_stop_index'] = 100000
    D['collisions'] = []
    D['t_to_indx'] = {}
    return D

def car_name_from_run_name(rn):
    a = rn.split('Mr_')
    car_name = 'Mr_'+a[-1]
    car_name = car_name.replace('Mr_Yellow_A','Mr_Yellow')
    car_name = car_name.replace('Mr_Yellow_B','Mr_Yellow')
    return car_name

car_colors = {'Mr_Yellow':(255,255,0), 'Mr_Silver':(255,255,255), 'Mr_Blue':(0,0,255), 'Mr_Orange':(255,0,0), 'Mr_Black':(100,100,100)}


def get_metadata(run_name,bair_car_data_location):
    print('get_metadata')
    L = lo(opj(bair_car_data_location,'meta',run_name,'left_image_bound_to_data.pkl'))
    ts,data_list = get_sorted_keys_and_data(L)
    ts = array(ts)
    data_types = data_list[0].keys()
    data = {}
    for d in data_types:
        data[d] = []
    for e in data_list:
        for d in data_types:
            data[d].append(e[d])
    for d in data_types:
        for i in rlen(data[d]):
            if not is_number(data[d][i]):
                data[d][i] = 0
        data[d] = array(data[d])
    return ts,data


def get_bag_pkl_images(run_name,bair_car_data_location):
    print "get_bag_pkl_images"
    bag_pkls = sgg(opj(bair_car_data_location,'rgb_1to4',run_name,'*.bag.pkl'))
    images = {}
    images['left'] = {}
    images['right'] = {}
    assert(len(bag_pkls) > 0)
    indx = 0
    for b in bag_pkls:
        print b
        o = load_obj(b)
        for side in ['left','right']:
            ts = sorted(o[side].keys())
            for t in ts:
                images[side][t] = o[side][t]
    return images


