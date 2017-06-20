"""



"""

from kzpy3.vis import *
if '/Users/' in home_path:
    from kzpy3.misc.OSX_free_memory import OSX_free_memory

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
                if os.path.getsize(self.path) < 20000000: # A bag file should be greater than 20 MB.
                    return None
                #print 'Bag_File: loading ' + self.path
                self.img_dic = load_obj(self.path)
                self.timestamps = sorted(self.img_dic['left'].keys())
                self.binned_timestamp_nums = [[],[]]
                """
                Binning timestamps. Most of the time the car drives straight.
                If we sample the timestamps uniformly, we will not get many examples
                of turning, proportionally. Therefore, I bin timestamps. I use only two
                bins, mostly-straight and turning. Having done this, we can request a
                random choice within either category.
                """
                for i in range(len(self.timestamps)-num_data_steps):
                    t = self.timestamps[i+num_data_steps]
                    if t in left_image_bound_to_data:
                        if left_image_bound_to_data[t]['state_one_steps'] > num_data_steps:
                            steer = left_image_bound_to_data[t]['steer']
                            if steer < 43 or steer > 55:
                                self.binned_timestamp_nums[0].append(i)
                            else:
                                self.binned_timestamp_nums[1].append(i)
            #print((len(self.binned_timestamp_nums[0]),len(self.binned_timestamp_nums[1])))
            """
            Sometimes a bin is empty, so we need to check for this while making a
            random selection.
            """
            if len(self.binned_timestamp_nums[0]) > 0 and len(self.binned_timestamp_nums[1]) > 0:
                timestamp_num = random.choice(self.binned_timestamp_nums[np.random.randint(len(self.binned_timestamp_nums))])
            elif len(self.binned_timestamp_nums[0]) > 0:
                timestamp_num = random.choice(self.binned_timestamp_nums[0])
            elif len(self.binned_timestamp_nums[1]) > 0:
                timestamp_num = random.choice(self.binned_timestamp_nums[1])
            else:
                return None

            t = self.timestamps[timestamp_num]
            """ Here is our timestamp."""

            data_dic = {}

            if t in left_image_bound_to_data:
                if left_image_bound_to_data[t]['state_one_steps'] > num_data_steps:
                    if timestamp_num + num_data_steps <= len(self.timestamps):
                        for topic in target_topics:
                            target_data = []
                            left_list = []
                            right_list = []
                            fctr = 0
                            for tn in range(timestamp_num,timestamp_num+num_data_steps):
                                data = "NO DATA"
                                if topic in left_image_bound_to_data[self.timestamps[tn]]:
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
                return None
            if len(data_dic) == 0:
                return None

            # assert that data_dic holds what it is supposed to hold.
            #print self.path
            #print data_dic.keys()
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
    def __init__(self, path, max_requests, max_subrequests, validation_set_flag):
        files = sorted(glob.glob(opj(path,'.preprocessed','*.bag.pkl')))
        self.files = []
        for i in range(len(files)):
            if mod(i,17) == 0:
                if validation_set_flag:
                    self.files.append(files[i])
                    print "validation data"
                else:
                    pass
            else:
                if validation_set_flag:
                    pass
                else:
                    self.files.append(files[i])
                    #print "test data"
        file_path = opj(path,'.preprocessed','left_image_bound_to_data')
        print "Bag_Folder: loading "+file_path+'.pkl'
        self.left_image_bound_to_data = load_obj(file_path)
        self.bag_file = None
        self.request_ctr = 0
        self.max_requests = max_requests
        self.max_subrequests = max_subrequests
        self.bag_files_dic = {}
        self.depth = 0
        # The state_one_steps were forund in preprocess_bag_data.py, but I redo it here to get state 3.
        """
        -- state_one_steps --
        Data at a given timestamp may be valid or invalid with respect to our data needs.
        For example, state 2 is by definition invalid, while state 1 is by definition valid.
        We also want to know, at any given timestamp, how many valid timestamps there are in a continuous
        sequence in the future. That is what we are figuring out here.
        A problem is that state number is not necessarily enough. For example, the car could
        be in state 1 but not be moving, or it could be in state 1 an be being carried by hand
        because there was a mistake in changing states -- but the lack of a motor signal could catch this.
        """
        timestamps = sorted(self.left_image_bound_to_data.keys())
        state_one_steps = 0
        for i in range(len(timestamps)-1,-1,-1):
            state = self.left_image_bound_to_data[timestamps[i]]['state']
            motor = self.left_image_bound_to_data[timestamps[i]]['motor']
            if state in [1,3,5,6,7]: #== 1.0 or state == 3.0:
                if motor > 51: # i.e., there must be at least a slight forward motor command 
                    state_one_steps += 1
                else:
                    state_one_steps = 0
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
                self.bag_files_dic[b] = Bag_File(b, self.max_subrequests)
            self.bag_file = self.bag_files_dic[b]
            self.bag_file.reset()
            #self.bag_file = Bag_File(b, self.max_subrequests)
        if True:#try:
            data = self.bag_file.get_data(self.left_image_bound_to_data, target_topics, num_data_steps, num_frames)
            if not data == None:
                data['bag_filename'] = self.bag_file.path
            #print b
        else: #except Exception, e:
            #print e 
            #print "Bag_Folder ***************************************"
            data = None

        if data == None:
            self.bag_file = None
            if self.depth > 5:
                print "self.depth > 5"
                self.depth = 0;
                return None
            self.depth += 1
            return self.get_data(target_topics, num_data_steps, num_frames)
        self.request_ctr += 1
        #print d2s("Bag_Folder::request_ctr =",self.request_ctr)
        self.depth = 0
        return data









class Bag_Folder2:
    def __init__(self, path):
        self.path = path
        self.files = sorted(glob.glob(opj(path,'.preprocessed','*.bag.pkl')))
        file_path = opj(path,'.preprocessed','left_image_bound_to_data')
        print "Bag_Folder: loading "+file_path+'.pkl'
        self.left_image_bound_to_data = load_obj(file_path)
        self.img_dic = {}
        # The state_one_steps were forund in preprocess_bag_data.py, but I redo it here to get state 3.
        """
        -- state_one_steps --
        Data at a given timestamp may be valid or invalid with respect to our data needs.
        For example, state 2 is by definition invalid, while state 1 is by definition valid.
        We also want to know, at any given timestamp, how many valid timestamps there are in a continuous
        sequence in the future. That is what we are figuring out here.
        A problem is that state number is not necessarily enough. For example, the car could
        be in state 1 but not be moving, or it could be in state 1 an be being carried by hand
        because there was a mistake in changing states -- but the lack of a motor signal could catch this.
        """
        timestamps = sorted(self.left_image_bound_to_data.keys())
        state_one_steps = 0
        for i in range(len(timestamps)-1,-1,-1):
            state = self.left_image_bound_to_data[timestamps[i]]['state']
            motor = self.left_image_bound_to_data[timestamps[i]]['motor']
            if state in [1,3,5,6,7]: #== 1.0 or state == 3.0:
                if motor > 51: # i.e., there must be at least a slight forward motor command 
                    state_one_steps += 1
                else:
                    state_one_steps = 0
            else:
                state_one_steps = 0
            self.left_image_bound_to_data[timestamps[i]]['state_one_steps'] = state_one_steps

    def load_all_bag_files(self):
        for f in self.files:
            bag_file_img_dic = load_obj(f)
            for t in bag_file_img_dic['left'].keys():
                self.img_dic[t] = bag_file_img_dic['left'][t]

def play(self,start_t,stop_t):
    print((start_t,stop_t))
    ts = sorted( self.img_dic.keys())
    print len(ts)
    t_tracker = ts[0]
    for i in range(0,len(ts),1):
        if ts[i] >= start_t and ts[i] < stop_t:
            img = self.img_dic[ts[i]]
            if ts[i] - t_tracker > 0.25:
                plt.figure(1)
                plt.plot(ts[i],10,'o')
                t_tracker = ts[i]
            mi(self.img_dic[ts[i]],2,img_title=str(ts[i]),toolBar=True)
            plt.pause(0.001)#max(0.03 - time.time()-t0,0))


def play2(self,start_t,stop_t,step=1,save_instead_of_display=False):
    caffe_steer_color_color = [255,0,0]
    human_steer_color_color_state_2 = [0,0,255]
    human_steer_color_color_state_1 = [0,255,0]
    img = np.zeros((94, 168,3),np.uint8)
    img_dic = {}
    print((start_t,stop_t))
    ts = sorted( self.img_dic.keys())
    print len(ts)
    t_tracker = ts[0]
    for i in range(0,len(ts),step):
        try:
            if ts[i] >= start_t and ts[i] < stop_t:
                im = self.img_dic[ts[i]]
                img[:,:,0] = im
                img[:,:,1] = im
                img[:,:,2] = im
                if np.int(self.left_image_bound_to_data[ts[i]]['state']) in [3,6]: #caffe is steering
                    steer_rect_color = caffe_steer_color_color
                elif np.int(self.left_image_bound_to_data[ts[i]]['state']) == 2:
                    steer_rect_color = human_steer_color_color_state_2
                elif np.int(self.left_image_bound_to_data[ts[i]]['state']) == 1:
                    steer_rect_color = human_steer_color_color_state_1
                else:
                    steer_rect_color = [255,0,255]
                apply_rect_to_img(img,self.left_image_bound_to_data[ts[i]]['steer'],0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True)
                if ts[i] - t_tracker > 0.25 and not save_instead_of_display:
                    plt.figure(1)
                    plt.plot(ts[i],10,'o')
                    t_tracker = ts[i]

                if save_instead_of_display:
                    img_dic[ts[i]] = img.copy()
                if (not save_instead_of_display) or (np.mod(i,10) == 0): 
                    mi(img,2,img_title=str(ts[i]),toolBar=True)
                    plt.pause(0.001)#max(0.03 - time.time()-t0,0))
        except Exception as e:
           print "train ***************************************"
           print e.message, e.args
           print "***************************************"

    if save_instead_of_display:
        return img_dic    




def play_cv2(self,start_t,stop_t):
    import cv2
    cv2.namedWindow('left',1)
    ts = sorted( self.img_dic.keys())
    print len(ts)
    for i in range(0,len(ts),1):
        if ts[i] >= start_t and ts[i] < stop_t:
            #print i
            img = self.img_dic[ts[i]]
            cv2.imshow('left',img.astype('uint8'))
            if cv2.waitKey(1) & 0xFF == ord('q'):   
                return      
            #t0 = time.time()   
            #mi(self.img_dic[ts[i]],2,img_title=str(ts[i]))
            plt.pause(0.03)#max(0.03 - time.time()-t0,0))
    cv2.destroyWindow('left')

click_ts = []
def button_press_event(event):
    global click_ts
    #print len(click_ts)
    ts = event.xdata
    click_ts.append(ts)
    print click_ts[-2:]


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


"""
(1474581103.2895727, 1474581268.1056883)
    (1474580959.4764488, 1474581045.9608831)
    1474576522.58,1474576603.85
    1474577588.98,1474577653.58 !
    1474577817.37,1474577824.85 hill rollover
    1474331412.37,1474331420.67 sidewalk obsticals
    1474331288.89,1474331350.38 good sidewalk sequence
    ,1474331037.87,1474331059.92 pedestrian avoidance
img_dic = play2(bf2,click_ts[-2],click_ts[-1],1,True)
img_dic = play2(bf2,0,9999999999,1,True)
    data_dir = 'caffe_z2_direct_18Sept2016_Mr_Orange_local_sidewalks'
    data_dir = 'caffe_z2_direct_Tilden_22Sep16_13h18m02s_Mr_Orange'
    data_dir = 'caffe_z2_direct_local_Tilden_22Sep16_14h31m11s_Mr_Orange'
"""
#from kzpy3.teg1.rosbag_work.get_data_from_bag_files5 import *
#bf2 = Bag_Folder2('/home/karlzipser/Desktop/bair_car_data_min/caffe_z2_from_Evans_19Sept2016_Mr_Orange');#

def generate_frames(data_dir):
    bf2 = Bag_Folder2('/home/karlzipser/Desktop/bair_car_data_min/'+data_dir)
    bf2.load_all_bag_files()
    L = bf2.left_image_bound_to_data
    if False:
        fig = plt.figure(1,figsize=(14,4))
        plt.rcParams['toolbar'] = 'toolbar2'
        plt.clf()
        plt.ion()
        plt.show()
        fig.canvas.mpl_connect('button_press_event', button_press_event)
        plot_L_file(L,1,False)
    img_dic = play2(bf2,0,9999999999,1,True)
    ts = sorted(img_dic.keys())
    dir = opjD('frames',data_dir+'_jpg')
    unix(d2s('mkdir -p',dir))
    for i in range(len(ts)):
        if np.mod(i,10) == 0:
            print i
        imsave(opjD(dir,d2n(i,'.jpg')),imresize(img_dic[ts[i]],4.0))

if False:

    data_dirs = []
    _, dirs = dir_as_dic_and_list( '/home/karlzipser/Desktop/bair_car_data_min' )
    for d in dirs:
        if 'furtive' in d:
            if 'caffe' not in d:
                if 'follow_and_furtive_27Aug' not in d:
                    if 'furtive_8Aug' not in d:
                        data_dirs.append(d)
                        generate_frames(d)


class Bair_Car_Data:
    """ """
    def __init__(self, path, max_requests, max_subrequests, validation_set_flag=False,use_caffe_data=False):
        self.bag_folder = None
        self.max_requests = max_requests
        self.max_subrequests = max_subrequests
        self.bag_folders_dic = {}        
        bag_folder_paths = sorted(glob.glob(opj(path,'*')))
        if use_caffe_data == False:
            temp = []
            for b in bag_folder_paths:
                if 'caffe' not in b:
                    temp.append(b)
                else:
                    print "Not using " + b + " as data."
            bag_folder_paths = temp
        self.bag_folders_weighted = []
        for f in bag_folder_paths:
            
            n = len(gg(opj(f,'.preprocessed','*.bag.pkl')))
            m = len(gg(opj(f,'.preprocessed','left*')))
            print (n,m,f)
            if n > 0 and m > 0:
                self.bag_folders_dic[f] = Bag_Folder(f, self.max_requests, self.max_subrequests, validation_set_flag)
                for i in range(max(n/10,1)):
                    self.bag_folders_weighted.append(f)
        #print self.bag_folders_weighted
        #time.sleep(60)


    def check_memory(self):
        free_propotion = 1.0
        free_gigabytes = 999999.0
        if '/Users/' not in home_path: # OSX doesn't have the memory() function that linux has.
            m=memory()
            #print m['free']/(1.0*m['total'])
            #while m['free']/(1.0*m['total']) < 0.15:
            free_propotion = m['free']/(1.0*m['total'])
            #print free_propotion
        else:
            free_gigabytes = OSX_free_memory()
        if free_propotion < 0.15 or free_gigabytes < 3.0:
            b = random.choice(self.bag_folders_dic.keys())
            self.bag_folders_dic[b].bag_files_dic = {}
            #print "Deleting "+b+" bag files."
            #del self.bag_folders_dic[b]

    def get_data(self, target_topics, num_data_steps, num_frames):
        #print 'Bair_Car_Data::get_data'
        self.check_memory()
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


def time_stamps_and_elements(L,topic):
    ts = sorted(L.keys())
    data = []
    for t in ts:
        data.append(L[t][topic])
    return ts,data

def plot_L_file(L,fig_num=1,by_index=False):
    ts,steer=time_stamps_and_elements(L,'steer')
    ts,motor=time_stamps_and_elements(L,'motor')
    ts,encoder=time_stamps_and_elements(L,'encoder')
    ts,gyro=time_stamps_and_elements(L,'gyro')   
    #ts,acc=time_stamps_and_elements(L,'acc') 
    ts,state=time_stamps_and_elements(L,'state')
    if by_index:
        ts = range(len(ts))
    plt.plot(ts,steer)
    plt.plot(ts,motor)
    plt.plot(ts,np.array(gyro)/10.)
    #plt.plot(ts,np.array(acc)-10.)
    plt.plot(ts,encoder)
    plt.plot(ts,state)



