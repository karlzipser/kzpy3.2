"""



"""



from kzpy3.vis import *

#import rospy
#import rosbag
import cv2
#import cv_bridge
#bridge = cv_bridge.CvBridge()




class Bag_File:
    def __init__(self, path, max_requests):
        self.path = path
        self.img_dic = None
        self.timestamps = None
        self.max_requests = max_requests
        self.request_ctr = 0

    def reset(self):
        self.request_ctr = 0


    def get_data(self, left_image_bound_to_data, target_topics, num_data_steps, num_frames):
            if self.request_ctr >= self.max_requests:
                return None
            if self.img_dic == None:
                #print 'Bag_File: loading ' + self.path
                self.img_dic = load_obj(self.path.replace('.pkl',''))
                self.timestamps = sorted(self.img_dic['left'].keys())
                self.binned_timestamp_nums = [[],[]]
                for i in range(len(self.timestamps)-num_data_steps):
                    t = self.timestamps[i+num_data_steps]
                    if left_image_bound_to_data[t]['state_one_steps'] > num_data_steps:
                        steer = left_image_bound_to_data[t]['steer']
                        if steer < 43 or steer > 55:
                            self.binned_timestamp_nums[0].append(i)
                        else:
                            self.binned_timestamp_nums[1].append(i)
            #print((len(self.binned_timestamp_nums[0]),len(self.binned_timestamp_nums[1])))
            if len(self.binned_timestamp_nums[0]) > 0 and len(self.binned_timestamp_nums[1]) > 0:
                timestamp_num = random.choice(self.binned_timestamp_nums[np.random.randint(len(self.binned_timestamp_nums))])
            elif len(self.binned_timestamp_nums[0]) > 0:
                timestamp_num = random.choice(self.binned_timestamp_nums[0])
            elif len(self.binned_timestamp_nums[1]) > 0:
                timestamp_num = random.choice(self.binned_timestamp_nums[1])
            else:
                return None
            t = self.timestamps[timestamp_num]
            data_dic = {}

            if t in left_image_bound_to_data:
                if left_image_bound_to_data[t]['state_one_steps'] > num_data_steps:
                    if timestamp_num+num_data_steps <= len(self.timestamps):
                        for topic in target_topics:
                            target_data = []
                            left_list = []
                            right_list = []
                            fctr = 0
                            for tn in range(timestamp_num,timestamp_num+num_data_steps):
                                data = left_image_bound_to_data[self.timestamps[tn]][topic]
                                target_data.append(data)
                                if fctr < num_frames:
                                    left_list.append(self.img_dic['left'][self.timestamps[tn]])
                                    right_list.append(self.img_dic['right'][left_image_bound_to_data[self.timestamps[tn]]['right_image']])
                                    fctr += 1
                            data_dic[topic] = target_data
                        data_dic['left'] = left_list
                        data_dic['right'] = right_list
            else:
                pass

            # assert that data_dic holds what it is supposed to hold.
            for topic in target_topics:
                assert type(data_dic[topic]) == list
                assert len(data_dic[topic]) == num_data_steps
            for side in ['left','right']:
                assert type(data_dic[side]) == list
                assert len(data_dic[side]) == num_frames
                for i in range(num_frames):
                    assert type(data_dic[side][i]) == np.ndarray
                    assert shape(data_dic[side][i]) == (94, 168)

            self.request_ctr += 1
            #print d2s("Bag_File::request_ctr =",self.request_ctr)
            return data_dic



class Bag_Folder:
    def __init__(self, path, max_requests, max_subrequests):
        self.files = sorted(glob.glob(opj(path,'.preprocessed','*.bag.pkl')))
        """ 
        file_path = opj(path,'.preprocessed','left_image_bound_to_data')
        #print "Bag_Folder: loading "+file_path+'.pkl'
        self.left_image_bound_to_data = load_obj(file_path)
        """
        file_path = opj(path,'.preprocessed','left_image_bound_to_data.pkl')
        if len(gg(file_path)) == 0:
            file_path = opj(path,'.preprocessed','left_image_bound_to_data2.pkl')
        print "Bag_Folder: loading "+file_path
        self.left_image_bound_to_data = load_obj(file_path)

        self.bag_file = None
        self.request_ctr = 0
        self.max_requests = max_requests
        self.max_subrequests = max_subrequests
        self.bag_files_dic = {}
        # The state_one_steps were forund in preprocess_bag_data.py, but I redo it here to get state 3.
        timestamps = sorted(self.left_image_bound_to_data.keys())
        state_one_steps = 0
        for i in range(len(timestamps)-1,-1,-1):
            state = self.left_image_bound_to_data[timestamps[i]]['state']
            if state in [1,3,5,6,7]: #== 1.0 or state == 3.0:
                state_one_steps += 1
            else:
                state_one_steps = 0
            self.left_image_bound_to_data[timestamps[i]]['state_one_steps'] = state_one_steps


    def reset(self):
        self.request_ctr = 0

    def get_data(self, target_topics, num_data_steps, num_frames):
        if len(self.files) == 0:
            return None
        assert len(self.files) > 0
        #print 'Bag_Folder::get_data'
        if self.request_ctr >= self.max_requests:
            return None
        if self.bag_file == None:
            b = random.choice(self.files)
            if b not in self.bag_files_dic:
                m=memory()
                if m['free']/(1.0*m['total']) < 0.15:
                    if len(self.bag_files_dic.keys()) > 0:
                        rc = random.choice(self.bag_files_dic.keys())
                        #print "Bag_Folder: deleting " + rc + " *****************************************"
                        del self.bag_files_dic[rc]
                self.bag_files_dic[b] = Bag_File(b, self.max_subrequests)
            self.bag_file = self.bag_files_dic[b]
            self.bag_file.reset()
            #self.bag_file = Bag_File(b, self.max_subrequests)
        try:
            data = self.bag_file.get_data(self.left_image_bound_to_data, target_topics, num_data_steps, num_frames)
            if not data == None:
                data['bag_filename'] = self.bag_file.path
            #print b
        except Exception, e:
            #print e 
            #print "Bag_Folder ***************************************"
            data = None

        if data == None:
            self.bag_file = None
            return self.get_data(target_topics, num_data_steps, num_frames)
        self.request_ctr += 1
        #print d2s("Bag_Folder::request_ctr =",self.request_ctr)
        return data



"""

class Bair_Car_Data:
    """ """
    def __init__(self, path, to_ignore=[], NUM_STATE_ONE_STEPS=10):
        self.bag_folders_with_loaded_images = {}
        self.bag_folders_priority_list = []
        self.bag_folders_dic = {}
        self.incremental_index = 0
        self.ctr = 0
        self.current_bag_folder = None
        self.step = 0
        bag_folder_paths = sorted(glob.glob(opj(path,'*')))
        bag_folder_paths_dic = {}
        for b in bag_folder_paths:
            bag_folder_paths_dic[b] = True
            for ig in to_ignore:
                if ig in b:
                    bag_folder_paths_dic[b] = False
                    print "Not using " + b.split('/')[-1]
        temp = []
        #print "bag_folder_paths 1: "
        #print bag_folder_paths
        for b in bag_folder_paths_dic.keys():
            if bag_folder_paths_dic[b]:
                temp.append(b)
        bag_folder_paths = temp
"""


class Bair_Car_Data:
    """ """
    def __init__(self, path, max_requests, max_subrequests): #, to_ignore=[]):
        bag_folder_paths = sorted(glob.glob(opj(path,'*')))
        self.bag_folders_weighted = []
        for f in bag_folder_paths:
            
            n = len(gg(opj(f,'.preprocessed','*.bag.pkl')))
            m = len(gg(opj(f,'.preprocessed','left*')))
            print (n,m,f)
            if n > 0 and m > 0:
                for i in range(max(n/10,1)):
                    self.bag_folders_weighted.append(f)
        #print self.bag_folders_weighted
        #time.sleep(60)
        self.bag_folder = None
        self.max_requests = max_requests
        self.max_subrequests = max_subrequests
        self.bag_folders_dic = {}

    def get_data(self, target_topics, num_data_steps, num_frames):
        #print 'Bair_Car_Data::get_data'
        if True:#try:
            if self.bag_folder == None:
                b = random.choice(self.bag_folders_weighted)
                if b not in self.bag_folders_dic:
                    self.bag_folders_dic[b] = Bag_Folder(b, self.max_requests, self.max_subrequests)
                    print d2s("len(self.bag_folders_dic) =",len(self.bag_folders_dic))
                self.bag_folder = self.bag_folders_dic[b]
                self.bag_folder.reset()

            data = self.bag_folder.get_data(target_topics, num_data_steps, num_frames)
        else: #except Exception, e:
            #print e 
            #print "Bair_Car_Data ***************************************"
            data = None

        if data == None:
            self.bag_folder = None
            return self.get_data(target_topics, num_data_steps, num_frames)
        return data








def load_images_from_bag(bag_file_path,color_mode="rgb8"):
    print "loading " + bag_file_path
    bag_img_dic = {}
    bag_img_dic['left'] = {}
    bag_img_dic['right'] = {}
    sides=['left','right']
    bag = rosbag.Bag(bag_file_path)
    for side in sides:
        for m in bag.read_messages(topics=['/bair_car/zed/'+side+'/image_rect_color']):
            t = round(m.timestamp.to_time(),3)
            bag_img_dic[side][t] = bridge.imgmsg_to_cv2(m[1],color_mode)
    return bag_img_dic


def save_grayscale_quarter_images(bag_folder,bag_filename):
    b = load_images_from_bag(opj(bag_folder,bag_filename),color_mode="rgb8")
    for s in ['left','right']:
        for t in b[s]:
            b[s][t] = b[s][t][:,:,1]
            b[s][t] = imresize(b[s][t],0.25)
    unix('mkdir -p '+opj(bag_folder,'.preprocessed'))
    save_obj(b,opj(bag_folder,'.preprocessed',bag_filename))

def save_grayscale_quarter_bagfolder(bag_folder_path):
    bag_files = sorted(glob.glob(opj(bag_folder_path,'*.bag')))
    for b in bag_files:
        b = b.split('/')[-1]
        save_grayscale_quarter_images(bag_folder_path,b)

"""
bag_folder_path = '/home/karlzipser/Desktop/bair_car_data/direct_7Sept2016_Mr_Orange_Tilden'

d = Bair_Car_Recorded_Data(bag_folder_path,10,['steer','motor','encoder','acc','gyro','sonar'])

for i in range(500):
    data = d.get_data()
"""
