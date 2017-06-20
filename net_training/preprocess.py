from kzpy3.vis import *
from kzpy3.utils import *
import rospy
import rosbag
from collections import defaultdict
from kzpy3.data_analysis.data_parsing.Bagfile_Handler import Bagfile_Handler
import kzpy3.net_training.type_handlers.Bag_Folder as Bag_Folder
import kzpy3.net_training.type_handlers.Bag_File as Bag_File


############## topics, not necessarily original rosbag names ###################
#
image_topics = ['left_image', 'right_image']
single_value_topics = ['steer', 'state', 'motor', 'encoder']  # ,'GPS2_lat']
vector3_topics = ['acc', 'gyro', 'gps', 'gyro_heading']
all_topics = image_topics + single_value_topics + vector3_topics
#
######################################################################

############## bagfile data processing to useful forms ##############################
#
A = {}  # this will be renamed preprocessed_data for return



def preprocess_bag_data(bag_folder_path, bagfile_range=[]):
    
    A = {}  # this will be renamed preprocessed_data for return
    
    topic_name_map = {}
    topic_string_list = []
    
    for topic in all_topics:
        A[topic] = {}

    for topic in single_value_topics:
        topic_name_map['/bair_car/' + topic] = topic
        topic_string_list.append('/bair_car/' + topic)
        
    for topic in vector3_topics:    
        topic_name_map[topic] = topic
            
    topic_name_map['/bair_car/zed/left/image_rect_color'] = 'left_image'
    topic_name_map['/bair_car/zed/right/image_rect_color'] = 'right_image'
    topic_string_list.append('/bair_car/zed/left/image_rect_color')
    topic_string_list.append('/bair_car/zed/right/image_rect_color')
            
    bag_files = sorted(glob.glob(opj(bag_folder_path, '*.bag')))
    
    if len(bagfile_range) > 0:
        bag_files = bag_files[bagfile_range[0]:(bagfile_range[1] + 1)]
        
    cprint(d2s('Processing', len(bag_files), 'bag files:'), 'red')
    for b in bag_files:
        cprint('\t' + b, 'blue')

    for b in bag_files:
        try:
            cprint(b + str(' - augmented'), 'yellow')
            bagfile_handler = Bagfile_Handler(b, topic_string_list)
            
            topic, message, timestamp = bagfile_handler.get_bag_content()
            while(message != None):
                timestamp = round(timestamp.to_sec(), 3)
                
                if topic_name_map[topic] in vector3_topics and topic_name_map[topic] != 'gps':                    
                    
                        if not isinstance(message.x, (int, long, float)):
                            print("if not isinstance(message.x,(int,long,float)):")
                            print(d2s("message.x = ", message.x))
                            assert(False)
                        if not isinstance(message.y, (int, long, float)):
                            print("if not isinstance(message.y,(int,long,float)):")
                            print(d2s("message.y = ", message.y))
                            assert(False)
                        if not isinstance(message.z, (int, long, float)):
                            print("if not isinstance(message.x,(int,long,float)):")
                            print(d2s("message.z = ", message.z)) 
                            assert(False)
                        A[topic_name_map[topic]][timestamp] = (message.x, message.y, message.z)
                        
                elif topic_name_map[topic] in single_value_topics:
                
                    if not isinstance(message.data, (int, long, float)):
                        print("if not isinstance(m[1].data,(int,long,float)):")
                        print(d2s("m[1].data = ", message.data))
                        assert(False)
                    A[topic_name_map[topic]][timestamp] = message.data
                
                elif topic_name_map[topic] == 'gps':
                    try:                    
                        A[topic][timestamp] = (message.latitude, message.longitude, message.altitude)
                    except:
                        print 'gps problem'
                        
                elif topic_name_map[topic] in image_topics:
                    A[topic_name_map[topic]][timestamp] = 'z'
                    
                topic, message, timestamp = bagfile_handler.get_bag_content()
                
        except Exception as e:
            print e.message, e.args


    for img in ['left_image', 'right_image']:
        ctr = 0
        sorted_timestamps = sorted(A[img].keys())
        for t in sorted_timestamps:
            A[img][t] = ctr
            ctr += 1
    
    preprocessed_data = A

    left_image_bound_to_data, error_log = _bind_left_image_timestamps_to_data(A)
    print """left_image_bound_to_data,error_log = _bind_left_image_timestamps_to_data(A) """

    if False:
        timestamps = sorted(left_image_bound_to_data.keys())
        state_one_steps = 0
        for i in range(len(timestamps) - 1, -1, -1):
            if left_image_bound_to_data[timestamps[i]]['state'] == 1.0:
                state_one_steps += 1
            else:
                state_one_steps = 0
            left_image_bound_to_data[timestamps[i]]['state_one_steps'] = state_one_steps

    

    dst_path = opj(bag_folder_path, '.preprocessed2')
    print """unix('mkdir -p ' """ + dst_path + ')'
    unix('mkdir -p ' + dst_path)

    print """save_obj(left_image_bound_to_data,opj(dst_path,'left_image_bound_to_data')) """
    save_obj(left_image_bound_to_data, opj(dst_path, 'left_image_bound_to_data'))

    print """save_obj(preprocessed_data,opj(dst_path,'preprocessed_data'))"""
    save_obj(preprocessed_data, opj(dst_path, 'preprocessed_data'))


    return preprocessed_data, left_image_bound_to_data

#
######################################################################
# 
#
########################## binding data to left_image timestamps ######
#

def _bind_left_image_timestamps_to_data(A):

    ms_timestamps = {}

    ms_timestamps['right_image'] = _assign_right_image_timestamps(A)

    for topic in single_value_topics:
        try:
            ms_timestamps[topic] = _interpolate_single_values(A, topic)
        except:
            print 'Error with topic ' + topic
    for topic in vector3_topics:
        try:
            ms_timestamps[topic] = _interpolate_vector_values(A, topic)
        except:
            print 'Error with topic ' + topic

    left_image_bound_to_data = {}

    error_log = []

    sorted_keys = sorted(A['left_image'].keys())
    for i in range(30, len(sorted_keys) - 30):
    # we throw away the first and last 5 frames to avoid boundry problems with other sensors
        k = sorted_keys[i]
        left_image_bound_to_data[k] = {}
        for l in ms_timestamps.keys():
            try:
                left_image_bound_to_data[k][l] = ms_timestamps[l][k]
            except:
                error_log.append((k, l))
                left_image_bound_to_data[k][l] = 'no data'
                print (k, l)
                cprint("""
            except:
                error_log.append((k,l))
                left_image_bound_to_data[k][l] = 'no data'
                print (k,l)                    
                    """, 'red', 'on_blue')
    print error_log
    return left_image_bound_to_data, error_log


def _interpolate_single_values(A, topic):
    """
    Warning, this will interpolate the topic 'state', which we do not want.
    """
    interp_dic = {}
    k, d = get_sorted_keys_and_data(A[topic])
    for i in range(0, len(k) - 1):
        for j in range(int(k[i] * 1000), int(k[i + 1] * 1000)):
            v = round((d[i + 1] - d[i]) / (k[i + 1] - k[i]) * (j / 1000. - k[i]) + d[i], 3)
            interp_dic[j / 1000.] = v
    return interp_dic

def _interpolate_vector_values(A, topic):
    interp_dic = {}
    k, d = get_sorted_keys_and_data(A[topic])
    d = np.array(d)
    dim = len(d[0])
    for i in range(0, len(k) - 1):
        for j in range(int(k[i] * 1000), int(k[i + 1] * 1000)):
            v = []
            for u in range(dim):
                if topic != 'gps':  # with GPS we need as many decimal places as possible
                    v.append(round((d[i + 1, u] - d[i, u]) / (k[i + 1] - k[i]) * (j / 1000. - k[i]) + d[i, u], 3))
                else:
                    v.append((d[i + 1, u] - d[i, u]) / (k[i + 1] - k[i]) * (j / 1000. - k[i]) + d[i, u])
            interp_dic[j / 1000.] = v
    return interp_dic

def _assign_right_image_timestamps(A):
    interp_dic = {}
    k, d = get_sorted_keys_and_data(A['right_image'])
    for i in range(0, len(k) - 1):
        a = int(k[i] * 1000)
        b = int(k[i + 1] * 1000)
        c = (a + b) / 2
        for j in range(a, b):
            if j < c:
                v = k[i]
            else:
                v = k[i + 1]
            interp_dic[j / 1000.] = v
    return interp_dic
#
######################################################################


def preprocess_Bag_Folders(bag_folders_path_meta_path,bag_folders_path_rgb1to4_path,NUM_STATE_ONE_STEPS=30,graphics=False,accepted_states=[1],pkl_name='Bag_Folder.pkl'):
    
    
    bag_folders_paths_list = sorted(gg(opj(bag_folders_path_meta_path,'*')),key=natural_keys)

    
    for bfp in bag_folders_paths_list:

        try:

            print bfp
            run_name = bfp.split('/')[-1]

            left_image_bound_to_data_name = get_preprocess_dir_name_info(bfp)
            if left_image_bound_to_data_name == None:
                cprint("if left_image_bound_to_data_name == None:",'red')
                continue

            if len(gg(opj(bfp,pkl_name))) == 1:
                print('\t exists')
                if False: #graphics:
                    cprint(opj(run_name,'Bag_Folder.pkl')+' exists, loading it.','yellow','on_red')
                    BF = load_obj(opj(bfp,'Bag_Folder.pkl'))
            else:
                BF = Bag_Folder.init(bfp,
                    opj(bag_folders_path_rgb1to4_path,fname(bfp)),
                    left_image_bound_to_data_name=left_image_bound_to_data_name,
                    NUM_STATE_ONE_STEPS=NUM_STATE_ONE_STEPS,
                    accepted_states=accepted_states)
                if BF != None:
                    save_obj(BF,opj(bfp,'Bag_Folder.pkl'))

            if graphics:
                figure(run_name+' timecourses')
                plot(BF['data']['raw_timestamps'],100*BF['data']['encoder'],'y')
                plot(BF['data']['raw_timestamps'],BF['data']['state_one_steps'],'bo-')
                plot(BF['data']['good_start_timestamps'],zeros(len(BF['data']['good_start_timestamps']))+100,'go')
                plot(BF['data']['raw_timestamps'],2000*BF['data']['raw_timestamp_deltas'],'r')
                ylim(0,1000)

                figure(run_name+' raw_timestamp_deltas')
                rtd = BF['data']['raw_timestamp_deltas'].copy()
                rtd[rtd>0.08] = 0.08
                hist(rtd)
                #plot(BF['data']['raw_timestamps'],100*BF['data']['state'],'r')
                #plot(BF['data']['raw_timestamps'],100*BF['data']['acc_z'],'r')

                figure(run_name+' scatter')
                plot(BF['data']['steer'][BF['data']['good_start_indicies']],BF['data']['gyro_x'][BF['data']['good_start_indicies']],'o')

                plt.pause(0.001)

        except Exception as e:
            cprint("********** Exception ***********************",'red')
            print(e.message, e.args)            



def get_preprocess_dir_name_info(bag_file_path):
    fl = sgg(opj(bag_file_path,'left*'))
    if len(fl) > 0:
        return sgg(opj(bag_file_path,'left*'))[-1]
    else:
        return None




bag_folders_src_location = sys.argv[1]
bag_folders_dst = sys.argv[2]
NUM_STATE_ONE_STEPS = int(sys.argv[3])

assert(is_number(NUM_STATE_ONE_STEPS))

bag_folders_src = opj(bag_folders_src_location,'new' )
bag_folders_dst_rgb1to4_path = opj(bag_folders_dst,'rgb_1to4')
bag_folders_dst_meta_path = opj(bag_folders_dst,'meta')



# 
# runs = sgg(opj(bag_folders_src,'*'))
# assert(len(runs) > 0)
#  
# tb = '\t'
#  
# cprint('Preliminary check of '+bag_folders_src)
# cprint("	checking bag file sizes and run durations")
#  
# for r in runs:
#     bags = sgg(opj(r,'*.bag'))
#     cprint(d2s(tb,fname(r),len(bags)))
#     mtimes = []
#     for b in bags:
#         bag_size = os.path.getsize(b)
#         mtimes.append(os.path.getmtime(b))
#         if bag_size < 0.99 * 1074813904:
#             cprint(d2s('Bagfile',b,'has size',bag_size,'which is below full size.'),'red')
#             unix('mv '+b+' '+b+'.too_small')
#     mtimes = sorted(mtimes)
#     run_duration = mtimes[-1]-mtimes[0]
#     print run_duration
#     assert(run_duration/60./60. < 3.) # If clock set incorrectly, this can change during run leading to year-long intervals
#     cprint(d2s(r,'is okay'))
#  
# for r in runs:
#     preprocess_bag_data(r)


 # The following code creates the rgb 1 to 4 folders. 
# It takes a folder with runs in a "new" folder. 
Bag_File.bag_folders_transfer_meta(bag_folders_src,bag_folders_dst_meta_path)
Bag_File.bag_folders_save_images(bag_folders_src,bag_folders_dst_rgb1to4_path)


graphics=False
accepted_states=[1,3,5,6,7]
pkl_name='Bag_Folder.pkl' # if different from 'Bag_Folder.pkl', (e.g., 'Bag_Folder_90_state_one_steps.pkl') files will be reprocessed.

preprocess_Bag_Folders(bag_folders_dst_meta_path,
	bag_folders_dst_rgb1to4_path
	,NUM_STATE_ONE_STEPS=NUM_STATE_ONE_STEPS,
	graphics=graphics,accepted_states=accepted_states,
	pkl_name=pkl_name)

#os.rename(bag_folders_src,opj(bag_folders_src_location,'processed'))

