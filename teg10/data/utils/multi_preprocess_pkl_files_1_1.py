from kzpy3.vis import *

image_topics = ['left_image','right_image']
single_value_topics = ['steer','state','motor','encoder','GPS2_lat']
vector3_topics = ['acc','gyro','gyro_heading']#,'gps']
camera_sides = ['left','right']




def multi_preprocess_pkl_files_WITH_IMAGES(A,meta_path,rgb_1to4_path,print_b=False,load_images=True,load_right_images=False):
    assert(load_images==True)
    for topic in image_topics + single_value_topics:
        if topic not in A:
            A[topic] = []
    for topic in vector3_topics:
        if topic+'_x' not in A:
            A[topic+'_x'] = []
            A[topic+'_y'] = []
            A[topic+'_z'] = []
    A['meta'] = load_obj(opj(meta_path,'left_image_bound_to_data.pkl'))
    steer_previous = 49
    motor_previous = 49
    bag_pkls = sgg(opj(rgb_1to4_path,'*.bag.pkl'))
    assert(len(bag_pkls) > 0)
    indx = 0
    print "multi_preprocess_pkl_files_1_1.py . . . WITH IMAGES"
    for b in bag_pkls:
        if print_b:
            print b
        if load_images:
            o = load_obj(b)
            ts = sorted(o['left'].keys())
        else:
            ts = A['meta'].keys()
        for t in ts:
            if load_images:
                if t in A['meta']:
                    if load_right_images:
                        tr = A['meta'][t]['right_image']
                        if tr in o['right']:
                            A['right'].append(o['right'][tr])
                        else:
                            continue
                    A['left'].append(o['left'][t])
                    A['t_to_indx'][t] = indx
                    indx += 1
            try:
                if A['SMOOTHING']:
                    A['steer'].append((A['meta'][t]['steer']+steer_previous)/2.0)
                    A['motor'].append((A['meta'][t]['motor']+motor_previous)/2.0)
                    A['state'].append(A['meta'][t]['state'])
                    steer_previous = A['steer'][-1]
                    motor_previous = A['motor'][-1]
                else:
                    A['steer'].append(A['meta'][t]['steer'])
                    A['state'].append(A['meta'][t]['state'])
                    A['motor'].append(A['meta'][t]['motor'])
            except:
                A['steer'].append(0)
                A['state'].append(0)
                A['motor'].append(0)
            try:
                A['acc_x'].append(A['meta'][t]['acc'][0])
                A['acc_y'].append(A['meta'][t]['acc'][1])
                A['acc_z'].append(A['meta'][t]['acc'][2])

            except:
                A['acc_x'].append(0)
                A['acc_y'].append(1)
                A['acc_z'].append(2)
            try:
                A['gyro_heading_x'].append(A['meta'][t]['gyro_heading'][0])
                A['gyro_heading_y'].append(A['meta'][t]['gyro_heading'][1])
                A['gyro_heading_z'].append(A['meta'][t]['gyro_heading'][2])

            except:
                A['gyro_heading_x'].append(0)
                A['gyro_heading_y'].append(1)
                A['gyro_heading_z'].append(2)

            try:
                A['gyro_x'].append(A['meta'][t]['gyro'][0])
                A['gyro_y'].append(A['meta'][t]['gyro'][1])
                A['gyro_z'].append(A['meta'][t]['gyro'][2])

            except:
                A['gyro_x'].append(0)
                A['gyro_y'].append(1)
                A['gyro_z'].append(2)
            try:
                A['encoder'].append(A['meta'][t]['encoder'])

            except:
                A['encoder'].append(0)

    A['acc_xz_dst'] = np.sqrt(array(A['acc_x'])**2 + array(A['acc_z'])**2)
    A['collisions'] = 0*array(A['steer'])






def multi_preprocess_pkl_files_NO_IMAGES(A,meta_path,rgb_1to4_path,print_b=False,load_images=False,load_right_images=False):
    assert(load_images==False)
    for topic in image_topics + single_value_topics:
        if topic not in A:
            A[topic] = []
    for topic in vector3_topics:
        if topic+'_x' not in A:
            A[topic+'_x'] = []
            A[topic+'_y'] = []
            A[topic+'_z'] = []
    A['meta'] = load_obj(opj(meta_path,'left_image_bound_to_data.pkl'))
    steer_previous = 49
    motor_previous = 49
    #bag_pkls = sgg(opj(rgb_1to4_path,'*.bag.pkl'))
    #assert(len(bag_pkls) > 0)
    indx = 0
    print "multi_preprocess_pkl_files_1_1.py . . . NO IMAGES"
    ts = A['meta'].keys()
    for t in ts:
        A['t_to_indx'][t] = indx
        indx += 1
        try:
            if A['SMOOTHING']:
                A['steer'].append((A['meta'][t]['steer']+steer_previous)/2.0)
                A['motor'].append((A['meta'][t]['motor']+motor_previous)/2.0)
                A['state'].append(A['meta'][t]['state'])
                steer_previous = A['steer'][-1]
                motor_previous = A['motor'][-1]
            else:
                A['steer'].append(A['meta'][t]['steer'])
                A['state'].append(A['meta'][t]['state'])
                A['motor'].append(A['meta'][t]['motor'])
        except:
            A['steer'].append(0)
            A['state'].append(0)
            A['motor'].append(0)
        try:
            A['acc_x'].append(A['meta'][t]['acc'][0])
            A['acc_y'].append(A['meta'][t]['acc'][1])
            A['acc_z'].append(A['meta'][t]['acc'][2])

        except:
            A['acc_x'].append(0)
            A['acc_y'].append(1)
            A['acc_z'].append(2)
        try:
            A['gyro_heading_x'].append(A['meta'][t]['gyro_heading'][0])
            A['gyro_heading_y'].append(A['meta'][t]['gyro_heading'][1])
            A['gyro_heading_z'].append(A['meta'][t]['gyro_heading'][2])

        except:
            A['gyro_heading_x'].append(0)
            A['gyro_heading_y'].append(1)
            A['gyro_heading_z'].append(2)

        try:
            A['gyro_x'].append(A['meta'][t]['gyro'][0])
            A['gyro_y'].append(A['meta'][t]['gyro'][1])
            A['gyro_z'].append(A['meta'][t]['gyro'][2])

        except:
            A['gyro_x'].append(0)
            A['gyro_y'].append(1)
            A['gyro_z'].append(2)
        try:
            A['encoder'].append(A['meta'][t]['encoder'])

        except:
            A['encoder'].append(0)

    A['acc_xz_dst'] = np.sqrt(array(A['acc_x'])**2 + array(A['acc_z'])**2)
    A['collisions'] = 0*array(A['steer'])






def multi_preprocess_pkl_files(A,meta_path,rgb_1to4_path,print_b=False,load_images=True,load_right_images=False):

    if load_images:
        multi_preprocess_pkl_files_WITH_IMAGES(A,meta_path,rgb_1to4_path,print_b=False,load_images=True,load_right_images=False)
    else:
        multi_preprocess_pkl_files_NO_IMAGES(A,meta_path,rgb_1to4_path,print_b=False,load_images=False,load_right_images=False)

