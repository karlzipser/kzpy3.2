"""



"""



from kzpy3.vis import *
#import cv2
#import cv_bridge
#bridge = cv_bridge.CvBridge()




class Bag_File:
    def __init__(self, path, max_requests):
        self.path = path
        self.img_dic = None
        self.timestamps = None
        self.max_requests = max_requests
        self.request_ctr = 0
    def get_data(self, left_image_bound_to_data, target_topics, num_data_steps, num_frames):
            if self.request_ctr > self.max_requests:
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
            timestamp_num = random.choice(self.binned_timestamp_nums[np.random.randint(len(self.binned_timestamp_nums))])
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
        file_path = opj(path,'.preprocessed','left_image_bound_to_data')
        print "Bag_Folder: loading "+file_path+'.pkl'
        self.left_image_bound_to_data = load_obj(file_path)
        self.bag_file = None
        self.request_ctr = 0
        self.max_requests = max_requests
        self.max_subrequests = max_subrequests

    def get_data(self, target_topics, num_data_steps, num_frames):
        #print 'Bag_Folder::get_data'
        if self.request_ctr >= self.max_requests:
            return None
        if self.bag_file == None:
            self.bag_file = Bag_File(random.choice(self.files), self.max_subrequests)
        try:
            data = self.bag_file.get_data(self.left_image_bound_to_data, target_topics, num_data_steps, num_frames)
        except Exception, e:
            print e 
            print "***************************************"
            data = None

        if data == None:
            self.bag_file = None
            return self.get_data(target_topics, num_data_steps, num_frames)
        self.request_ctr += 1
        #print d2s("Bag_Folder::request_ctr =",self.request_ctr)
        return data



class Bair_Car_Data:
    """ """
    def __init__(self, path, max_requests, max_subrequests):
        bag_folder_paths = sorted(glob.glob(opj(path,'*')))
        self.bag_folders_weighted = []
        for f in bag_folder_paths:
            print f
            n = len(gg(opj(f,'.preprocessed','*.bag.pkl')))
            if n > 0:
                for i in range(max(n/10,1)):
                    self.bag_folders_weighted.append(f)
        #print self.bag_folders_weighted
        #time.sleep(60)
        self.bag_folder_choice = None
        self.bag_folder_dic = {}
        self.max_requests = max_requests
        self.max_subrequests = max_subrequests

    def get_data(self, target_topics, num_data_steps, num_frames):
        #print 'Bair_Car_Data::get_data'
        try:
            if self.bag_folder_choice == None:
                self.bag_folder_choice = random.choice(self.bag_folders_weighted)
                if not self.bag_folder_choice in self.bag_folder_dic:
                    self.bag_folder_dic[self.bag_folder_choice] = Bag_Folder(self.bag_folder_choice, self.max_requests, self.max_subrequests)
                    

            data = self.bag_folder_dic[self.bag_folder_choice].get_data(target_topics, num_data_steps, num_frames)
        except Exception, e:
            print e 
            print "***************************************"
            data = None

        if data == None:
            self.bag_folder = None
            return self.get_data(target_topics, num_data_steps, num_frames)
        return data





