from kzpy3.vis import *
import kzpy3.teg9.data.animate as animate

import cv2

import threading
try:
    import rospy
    import rosbag
    from cv_bridge import CvBridge,CvBridgeError
except:
    print("""Failed to import:

    import rospy
    import rosbag
    from cv_bridge import CvBridge,CvBridgeError

    """)

try:
    bridge = CvBridge()
except:
    print("Failed: bridge = CvBridge()")


image_topics = ['left_image','right_image']
single_value_topics = ['steer','state','motor','encoder','GPS2_lat']
vector3_topics = ['acc','gyro','gyro_heading']#,'gps']
camera_sides = ['left','right']




def multi_preprocess_bagfiles(A,meta_path,bag_folder_path,bagfile_range=[]):
    A['meta'] = load_obj(meta_path)
    bag_files = sorted(gg(opj(bag_folder_path,'*.bag')))
    if len(bagfile_range) > 0:
        bag_files = bag_files[bagfile_range[0]:bagfile_range[1]]
    A['images'] = []
    threading.Thread(target=multi_preprocess_bagfiles_thread,args=[A,bag_files]).start()

def multi_preprocess_bagfiles_thread(A,bag_files):
    A['steer_previous'] = 49
    A['motor_previous'] = 49
    for b in bag_files:
        if A['STOP_LOADER_THREAD']:
            print('Stopping multi_preprocess_thread.')
            break
        preprocess_bagfiles(A,b)

def preprocess_bagfiles(A,path):
    timer = Timer(0)
    for topic in image_topics + single_value_topics:
        if topic not in A:
            A[topic] = []
    for topic in vector3_topics:
        if topic+'_x' not in A:
            A[topic+'_x'] = []
            A[topic+'_y'] = []
            A[topic+'_z'] = []
    if True:#try:
        cprint('Loading bagfile '+path,'yellow')

        bag = rosbag.Bag(path)

        color_mode = "rgb8"
        if 'image_ts' not in A:
            A['image_ts'] = []
        for s in ['left']:
            for m in bag.read_messages(topics=['/bair_car/zed/'+s+'/image_rect_color']):
                t = round(m.timestamp.to_time(),3)
                if A['t_previous'] > 0:            
                    if s == 'left':
                        A['left_deltas'].append([t,t-A['t_previous']])
                A['t_previous'] = t
                A['image_ts'].append(t)
                A['images'].append(bridge.imgmsg_to_cv2(m[1],color_mode))
                if False:
                    if t not in A['meta']:
                        print(d2s(t,"not in A['meta']"))
                    try:
                        if A['SMOOTHING']:
                            A['steer'].append((A['meta'][t]['steer']+A['steer_previous'])/2.0)
                            A['motor'].append((A['meta'][t]['motor']+A['motor_previous'])/2.0)
                            A['state'].append(A['meta'][t]['state'])
                            A['steer_previous'] = A['steer'][-1]
                            A['motor_previous'] = A['motor'][-1]
                        else:
                            A['steer'].append(A['meta'][t]['steer'])
                            A['state'].append(A['meta'][t]['state'])
                            A['motor'].append(A['meta'][t]['motor'])
                    except:
                        A['steer'].append(0)
                        A['state'].append(0)
                        A['motor'].append(0)
      
            #figure("left_deltas")
            #hist(A['left_deltas'])
    #except Exception as e:
    #    print e.message, e.args
    figure('left_deltas')
    clf()
    left_deltas = array(A['left_deltas'])
    print(shape(left_deltas))
    hist(left_deltas[:,1])
    plt.pause(0.01)
    print(d2s('Done in',timer.time(),'seconds'))





def multi_preprocess_pkl_files(A,meta_path,rgb_1to4_path):
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
    for b in bag_pkls:
        print b
        o = load_obj(b)
        ts = sorted(o['left'].keys())
        for t in ts:
            if A['t_previous'] > 0:            
                    A['left_deltas'].append([t,t-A['t_previous']])
            A['t_previous'] = t
            A['images'].append(o['left'][t])
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

    #A['acc_xz_dst'] = sqrt(array(A['acc_x'])**2 + array(A['acc_z'])**2)
    A['collisions'] = 0*array(A['steer'])
    figure('left_deltas')
    clf()
    A['left_deltas'] = array(A['left_deltas'])
    hist(A['left_deltas'][:,1])
    plt.pause(0.01)






def get_new_A():
    A = {}
    A['STOP_LOADER_THREAD'] = False
    A['STOP_ANIMATOR_THREAD'] = False
    A['STOP_GRAPH_THREAD'] = False
    A['d_indx'] = 1.0
    A['current_img_index'] = -A['d_indx']
    A['t_previous'] = 0
    A['left_deltas'] = []
    A['scale'] = 1.0
    A['delay'] = 33
    A['steer'] = []
    A['state'] = []
    A['SMOOTHING'] = True
    A['motor'] = []
    A['images'] = []
    A['left'] = []
    A['meta'] = None
    A['color_mode'] = cv2.COLOR_RGB2BGR
    A['save_start_index'] = 0
    A['save_stop_index'] = 100000
    A['collisions'] = []
    return A


#A = get_new_A()
def main():
    """
    e.g.
    python kzpy3/teg9/data/animate_bag_or_pkl_data.py pkl '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017' '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017/meta/direct_rewrite_test_15May17_03h17m17s_Mr_Yellow'

    """
    #bag_or_pkl = 'pkl'#sys.argv[1]
    #data_path = '/home/karlzipser/Desktop/bair_car_data_Main_Dataset'#sys.argv[2]
    #run_name = 'follow_26Aug2016_Mr_Orange_Tilden_1'#fname(sys.argv[3])
    bag_or_pkl = sys.argv[1]
    data_path = sys.argv[2]
    run_name = fname(sys.argv[3])
    if bag_or_pkl == 'bag':
        print('Working with bag files')
    elif bag_or_pkl == 'pkl':
        print('Working with pkl file')
    else:
        print("sys.argv[1] must be 'bag' or 'pkl'.")
        return
    if len(gg(data_path)) != 1:
        print("if len(gg(meta_path)) != 1:")
        return
    if len(sys.argv) > 4:
        alt_bagfolder_path = sys.argv[4]
    if len(sys.argv) > 5:
        bagfile_range = sys.argv[5]
    if len(sys.argv) > 6:
        print("Too many arguments")
        return
    A = get_new_A()
    if bag_or_pkl == 'pkl':
        A['scale'] = 3.0
    A['run_name'] = run_name
    A['loaded_collisions'] = None
    if False:
        collision_files = gg(opjD('collisions','*'))
        for c in collision_files:
            if run_name in c:
                A['loaded_collisions'] = lo(c)
                print 'loaded '+c
                break
    if bag_or_pkl == 'pkl':
        meta_path = opj(data_path,'meta',run_name)
        rgb_1to4_path = opj(data_path,'rgb_1to4',run_name)
        multi_preprocess_pkl_files(A,meta_path,rgb_1to4_path)
    elif bag_or_pkl == 'bag':
        meta_path = opj(data_path,run_name,'.preprocessed2/left_image_bound_to_data.pkl')
        bags_path = opj(data_path,run_name)
        multi_preprocess_bagfiles(A,meta_path,bags_path,bagfile_range=[])
    else:
        assert(False)
    threading.Thread(target=animate.animate_with_key_control,args=[A]).start()
    if bag_or_pkl == 'pkl':
        animate.graph(A)



        


if __name__ == '__main__':
    main()






if False:
    meta = sgg('/home/karlzipser/Desktop/bair_car_data_new/meta/*' )
    for i in range(len(meta)):

        meta[i] = fname(meta[i])
    meta = set(meta)

    ctr = 0
    collisions = sgg('/home/karlzipser/Desktop/collisions/*' )
    for i in range(len(collisions)):
        c = lo(collisions[i])
        ctr += c.sum()
        collisions[i] = fname(collisions[i]).split('.')[0]
    collisions = set(collisions)


