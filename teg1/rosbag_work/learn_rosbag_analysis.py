"""
Take rosbag files and have the option of doing any of the following:
1) look at timestamp intervals for a given topic
2) look at difference in timestamps of left and right camera
3) plot data versus timestamps
4) save images to separate files at optionally reduced resolution
5) bind data to left_image timestamps, so that one stream of timestamps is
   bound to all data types.
   e.g.,



from kzpy3.teg1.rosbag_work.learn_rosbag_analysis import *
preprocessed_data,left_image_bound_to_data = Preprocess_Bag_Data('/home/karlzipser/Desktop/rosbag_2Aug',[71,71],True,1.0,False,'png')

cd Desktop/rosbag_2Aug/png/left_image/
link_files_into_one_dir('.','*.png','links')

make_stereo_frames(bag_files_path,left_image_bound_to_data,image_extension='png')






To play frames:
    
    mplayer -fps 24 mf://*.png

"""

from kzpy3.vis import *
import rospy
import rosbag
import sensor_msgs.msg
import cv_bridge
from cv_bridge import CvBridge, CvBridgeError
bridge = cv_bridge.CvBridge()

############## topics, not necessarily original rosbag names ###################
#
image_topics = ['left_image','right_image']
single_value_topics = ['steer','state','motor','encoder','sonar']
vector3_topics = ['gyro'] # leave out gps for now.
all_topics = image_topics + single_value_topics + vector3_topics
#
######################################################################

############## bagfile data processing to useful forms ##############################
#

def Preprocess_Bag_Data(bag_files_path,bagfile_range=[],save_images=False,scale_factor=1.0,apply_rectangles=False,image_extension='png'):
    
    A = {} # this will be renamed preprocessed_data for return

    for topic in all_topics:
        A[topic] = {}

    bag_files = sorted(glob.glob(opj(bag_files_path,'bags','*.bag')))
    
    if len(bagfile_range) > 0:
        bag_files = bag_files[bagfile_range[0]:(bagfile_range[1]+1)]
    
    print bag_files

    for b in bag_files:
        try:
            print b

            bag = rosbag.Bag(b)

            for topic in single_value_topics:
                for m in bag.read_messages(topics=['/bair_car/'+topic]):
                    t = round(m.timestamp.to_time(),3) # millisecond resolution
                    A[topic][t] = m[1].data

            for topic in vector3_topics:
                for m in bag.read_messages(topics=['/bair_car/'+topic]):
                    t = round(m.timestamp.to_time(),3)
                    A[topic][t] = (m[1].x,m[1].y,m[1].z)

            for m in bag.read_messages(topics=['/bair_car/zed/left/image_rect_color']):
                t = round(m.timestamp.to_time(),3)
                A['left_image'][t] = 'z' # placeholder for ctr

            for m in bag.read_messages(topics=['/bair_car/zed/right/image_rect_color']):
                t = round(m.timestamp.to_time(),3)
                A['right_image'][t] = 'z' # placeholder for ctr
        except Exception as e:
            print e.message, e.args


    for img in ['left_image','right_image']:
        ctr = 0
        sorted_timestamps = sorted(A[img].keys())
        for t in sorted_timestamps:
            A[img][t] = ctr
            ctr += 1

    
    left_image_bound_to_data,error_log = _bind_left_image_timestamps_to_data(A)

    if save_images:

        for side in ['left','right']:
            ctr1 = 0
            ctr2 = 0
            A[side+'_image_folder_number'] = {}
            for b in bag_files:
                print b
                bag = rosbag.Bag(b)
                for m in bag.read_messages(topics=['/bair_car/zed/'+side+'/image_rect_color']):
                    t = round(m.timestamp.to_time(),3)
                    t_str = "%.3f"%t
                    A[side+'_image_folder_number'][t] = ctr1
                    if scale_factor == 1.0:
                        img = bridge.imgmsg_to_cv2(m[1],"rgb8")
                    else:
                        img = imresize(bridge.imgmsg_to_cv2(m[1],"rgb8"),scale_factor)
                    if apply_rectangles:
                        if True: #side == 'left':
                            try:
                                apply_rect_to_img(img,left_image_bound_to_data[t]['steer'],0,99,[255,0,0],[0,255,0],0.1,0.03,center=True,reverse=True)
                            except:
                                print t
                            try:
                                apply_rect_to_img(img,left_image_bound_to_data[t]['motor'],0,99,[0,0,255],[255,255,0],0.9,0.03,center=True,reverse=False)
                            except:
                                print t
                            try:
                                apply_rect_to_img(img,left_image_bound_to_data[t]['encoder'],0,15,[150,150,0],[0,0,0],0.8,0.03)
                            except:
                                print t
                            #try:# sonar seems to be mostly noise
                            #    apply_rect_to_img(img,left_image_bound_to_data[t]['sonar'],0,200,[0,150,150],[0,0,0],0.6,0.03)
                            #except:
                            #    print t
                            try:
                                gy = left_image_bound_to_data[t]['gyro']
                                gymag = np.sqrt(gy[0]**2 + gy[1]**2 + gy[2]**2)
                                apply_rect_to_img(img,gymag,0,120,[0,150,255],[0,0,0],0.7,0.03)
                            except:
                                print t
                    unix('mkdir -p ' + opj(bag_files_path,'images/'+side+'_image',str(ctr1)),False,False)
                    imsave(opj(bag_files_path,'images/'+side+'_image',str(ctr1),t_str+'.'+image_extension), img)
                    ctr2 += 1
                    if ctr2 >= 300:
                        ctr2 = 0
                        ctr1 += 1
            link_files_into_one_dir(opj(bag_files_path,'images/'+side+'_image'),'*.'+image_extension,opj(bag_files_path,'images/'+side+'_image','links'))

    preprocessed_data = A
    return preprocessed_data,left_image_bound_to_data
    

def apply_rect_to_img(img,value,min_val,max_val,pos_color,neg_color,rel_bar_height,rel_bar_thickness,center=False,reverse=False):
    h,w,d = shape(img)
    p = (value - min_val) / (max_val - 1.0*min_val)
    if reverse:
        p = 1.0 - p
    if p > 1:
        p = 1
    if p < 0:
        p = 0
    wp = int(p*w)
    bh = int((1-rel_bar_height) * h)
    bt = int(rel_bar_thickness * h)
    
    if center:
        if wp < w/2:
            img[(bh-bt/2):(bh+bt/2),(wp):(w/2),:] = neg_color
        else:
            img[(bh-bt/2):(bh+bt/2),(w/2):(wp),:] = pos_color
    else:
        img[(bh-bt/2):(bh+bt/2),0:wp,:] = pos_color



import fnmatch

def find_files_recursively(start_dir,pattern):
    matches = []
    for root, dirnames, filenames in os.walk(start_dir):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches

def link_files_into_one_dir(start_dir,pattern,end_dir):
    """
    start_dir must be one level above end_dir
    """
    matches = find_files_recursively(start_dir,pattern)
    unix('mkdir -p ' + end_dir,False)
    cwd = os.getcwd()
    os.chdir(end_dir)
    for fp in matches:
        f = fp.split('/')[-1]
        print f
        unix('ln -s ' + fp.replace(start_dir,'..') + ' ' + f,False)
    os.chdir(cwd)
#
######################################################################
#

def make_stereo_frames(bag_files_path,left_image_bound_to_data,image_extension='png'):
    left_ts = []
    right_ts = []
    for k in left_image_bound_to_data.keys():
        left_ts.append(k)
        right_ts.append(left_image_bound_to_data[k]['right_image'])
    t_str = "%.3f"%left_ts[0]
    img = imread(opj(bag_files_path,'images/left_image/links',t_str+'.'+image_extension))
    h,w,d = shape(img)
    print h,w
    stereo_img = np.zeros((h,int(2.03*w),d),np.uint8)
                    
    
    ctr1 = 0
    ctr2 = 0

    for i in range(len(left_ts)):
        left_t_str = "%.3f"%left_ts[i]
        right_t_str = "%.3f"%right_ts[i]
        left_img = imread(opj(bag_files_path,'images/left_image/links',left_t_str+'.'+image_extension))
        right_img = imread(opj(bag_files_path,'images/right_image/links',right_t_str+'.'+image_extension))

        stereo_img[:,:w,:] = right_img
        stereo_img[:,-w:,:] = left_img # for cross fusing
        unix('mkdir -p ' + opj(bag_files_path,'images/stereo_image',str(ctr1)),False,False)
        imsave(opj(bag_files_path,'images/stereo_image',str(ctr1),left_t_str+'.'+image_extension),stereo_img)
        ctr2 += 1
        if ctr2 >= 300:
            ctr2 = 0
            ctr1 += 1
    link_files_into_one_dir(opj(bag_files_path,'images/stereo_image'),'*.'+image_extension,opj(bag_files_path,'images/stereo_image','links'))

#
######################### binding data to left_image timestamps ######
#

def _bind_left_image_timestamps_to_data(A):

    ms_timestamps = {}

    ms_timestamps['right_image'] = _assign_right_image_timestamps(A)

    for topic in single_value_topics:
        ms_timestamps[topic] = _interpolate_single_values(A,topic)

    for topic in vector3_topics:
        ms_timestamps[topic] = _interpolate_vector_values(A,topic)

    left_image_bound_to_data = {}

    error_log = []

    sorted_keys = sorted(A['left_image'].keys())
    for i in range(30,len(sorted_keys)-30):
    # we throw away the first and last 30 frames to avoid boundry problems with other sensors
        k = sorted_keys[i]
        left_image_bound_to_data[k] = {}
        for l in ms_timestamps.keys():
            try:
                left_image_bound_to_data[k][l] = ms_timestamps[l][k]
            except:
                error_log.append((k,l))
                left_image_bound_to_data[k][l] = 'no data'
                print (k,l)
    print error_log
    return left_image_bound_to_data,error_log


def _interpolate_single_values(A,topic):
    interp_dic = {}
    k,d = get_sorted_keys_and_data(A[topic])
    for i in range(0,len(k)-1):
        for j in range(int(k[i]*1000),int(k[i+1]*1000)):
            v =  (d[i+1]-d[i])/(k[i+1]-k[i]) * (j/1000.-k[i])  + d[i]
            interp_dic[j/1000.] = v
    return interp_dic

def _interpolate_vector_values(A,topic):
    interp_dic = {}
    k,d = get_sorted_keys_and_data(A[topic])
    d = np.array(d)
    dim = len(d[0])
    for i in range(0,len(k)-1):
        for j in range(int(k[i]*1000),int(k[i+1]*1000)):
            v = []
            for u in range(dim):
                v.append(  (d[i+1,u]-d[i,u])/(k[i+1]-k[i]) * (j/1000.-k[i])  + d[i,u] )
            interp_dic[j/1000.] = v
    return interp_dic

def _assign_right_image_timestamps(A):
    interp_dic = {}
    k,d = get_sorted_keys_and_data(A['right_image'])
    for i in range(0,len(k)-1):
        a = int(k[i]*1000)
        b = int(k[i+1]*1000)
        c = (a+b)/2
        for j in range(a,b):
            if j < c:
                v = k[i]
            else:
                v = k[i+1]
            interp_dic[j/1000.] = v
    return interp_dic
#
######################################################################


######################### diagnostic graphics ####################
#
def make_timestamp_diagnostic_histograms(A):
    hist_topics_timestamp_intervals(A,all_topics,0.1)
    hist_diff_left_right_image_timestamps(A,ignore_threshold=0.1)

def hist_topics_timestamp_intervals(A,topics,ignore_threshold=0.1):
    for s in topics:
        k,d = get_sorted_keys_and_data(A[s])
        i = _get_timestamp_intervals(k,ignore_threshold)
        plt.figure(s)
        hist(i,bins=100)
        plt.title(d2s(s,"intervals"))
        plt.xlabel("seconds")

def hist_diff_left_right_image_timestamps(A,ignore_threshold=0.1):
    l,_ = get_sorted_keys_and_data(A['left_image'])
    r,_ = get_sorted_keys_and_data(A['right_image'])
    d = np.array(l) - np.array(r)
    dd = []
    for i in range(len(d)):
        if np.abs(d[i]) < ignore_threshold:
            dd.append(d[i])
        else:
            print d2s("!!!WARNING, inverval =",d[i],"s. Ignoring this interval!!!")
    plt.figure('hist_diff_left_right_image_timestamps')
    hist(dd,bins=100)
    plt.title("hist_diff_left_right_image_timestamps")
    plt.xlabel("seconds")

def _get_timestamp_intervals(timestamps,ignore_threshold):
    d = []
    for i in range(0,len(timestamps)-1):
        interval = timestamps[i+1] - timestamps[i]
        if interval < ignore_threshold:
            d.append(interval)
        else:
            print d2s("!!!WARNING, inverval =",interval,"s. Ignoring this interval!!! ( timestamp =",timestamps[i],")")
    return d

def plot_topics(A):

    """
    pylab.plot(x, y1, '-b', label='sine')
    pylab.plot(x, y2, '-r', label='cosine')
    pylab.legend(loc='upper left')
    pylab.ylim(-1.5, 2.0)
    pylab.show()
    """
    pass
#
######################################################################



