"""



"""

from kzpy3.vis import *
if '/Users/' in home_path:
    from kzpy3.misc.OSX_free_memory import OSX_free_memory


#import gc
from termcolor import cprint

click_ts = []
def button_press_event(event):
    global click_ts
    #print len(click_ts)
    ts = event.xdata
    click_ts.append(ts)
    print click_ts[-2:]

def z2o_plot(x,y,y_offset,plt_str='.',label='no label'):
    return plt.plot(x,z2o(y)+y_offset,plt_str,label=label)



class Bag_Folder:
    def __init__(self, path):
        if True:
            self.path = path
            self.files = sorted(glob.glob(opj(path,'.preprocessed','*.bag.pkl')))
            file_path = opj(path,'.preprocessed','left_image_bound_to_data.pkl')
            #print file_path
            if len(gg(file_path)) == 0:
                file_path = opj(path,'.preprocessed','left_image_bound_to_data2.pkl')
            #print "Bag_Folder: __init__: loading "+file_path
            self.left_image_bound_to_data = load_obj(file_path)
            self.img_dic = {}
            self.img_dic['left'] = {}
            self.img_dic['right'] = {}
            self.timestamps = sorted(self.left_image_bound_to_data.keys())
            self.returning_data_dic = 0
            self.returning_empty_data_dic = 0
            for t in self.timestamps:
                s = self.left_image_bound_to_data[t]['state'] # There is interpolation of values. For state we don't want this!
                self.left_image_bound_to_data[t]['state'] = np.round(s) # Here we undo the problem.

            for i in range(len(self.timestamps)-2): # Here we assume that isolated state 4 timepoints are rounding/sampling errors.
                t0 = self.timestamps[i]
                t1 = self.timestamps[i+1]
                t2 = self.timestamps[i+2]
                if self.left_image_bound_to_data[t1]['state'] == 4:
                    if self.left_image_bound_to_data[t0]['state'] != 4:
                        if self.left_image_bound_to_data[t2]['state'] != 4:
                                self.left_image_bound_to_data[t1]['state'] = self.left_image_bound_to_data[t0]['state']

            state_one_steps = 0
            for i in range(len(self.timestamps)-2,-1,-1):
                self.left_image_bound_to_data[self.timestamps[i]]['state_one_steps'] = 0 # overwrite loaded values
                if self.is_timestamp_valid_data(self.timestamps[i]) and self.timestamps[i+1] - self.timestamps[i] < 0.3:
                    state_one_steps += 1
                else:
                    state_one_steps = 0
                self.left_image_bound_to_data[self.timestamps[i]]['state_one_steps'] = state_one_steps
            self.data = {}
            self.data['timestamps'] = self.timestamps
            self.data['state'] = self.elements('state')
            self.data['steer'] = self.elements('steer')
            self.data['motor'] = self.elements('motor')
            
            acc = self.elements('acc')
            if len(acc) > 0: # acc added later than other sensors, not in all bagfiles
                self.data['acc_x'] = acc[:,0]
                self.data['acc_z'] = acc[:,1]
                self.data['acc_y'] = acc[:,2]
            else:
                self.data['acc_x'] = 0*self.data['timestamps']
                self.data['acc_z'] = 0*self.data['timestamps']
                self.data['acc_y'] = 0*self.data['timestamps']
            
            gyro = self.elements('gyro')
            self.data['gyro_x'] = gyro[:,0]
            self.data['gyro_z'] = gyro[:,1]
            self.data['gyro_y'] = gyro[:,2]
            self.data['encoder'] = self.elements('encoder')
            self.data['state_one_steps'] = self.elements('state_one_steps')
            #self.data['state_one_steps_1s_indicies'] = np.where(np.array(self.data['state_one_steps'])>=30)[0]
            self.data['state_one_steps_0_5s_indicies'] = np.where(np.array(self.data['state_one_steps'])>=15)[0]
            """
            topics = ['steer','motor','acc_x','acc_y','acc_z','gyro_x','gyro_y','gyro_z','encoder']
            for tp in topics:
                    d = self.data[tp][self.data['state_one_steps_1s_indicies']]
                    mn = d.mean()
                    sd = d.std()
                    if sd == 0 or sd == 0.0: # acc can be all zero, as can encoder, so we don't want to devide by this.
                        sd = 1.0
                    self.data[tp+'_z_scored'] = (self.data[tp]-mn)/sd
            """
            self.binned_timestamp_nums = [[],[]]
            for i in range(len(self.data['state_one_steps_0_5s_indicies'])):
                steer = self.data['steer'][i]
                if steer < 43 or steer > 55:
                    self.binned_timestamp_nums[0].append(i)
                else:
                    self.binned_timestamp_nums[1].append(i)

            print "Bag_Folder::init() preloaded " + self.path.split('/')[-1] + " (" + str(len(self.files)) + " bags)"
        #except Exception as e:
        #    cprint("********** " + self.path + " *****************************",'red')
        #    print e.message, e.args


    def load_all_bag_files(self):
        for f in self.files:
            bag_file_img_dic = load_obj(f)
            for s in ['left','right']:
                for t in bag_file_img_dic[s].keys():
                    self.img_dic[s][t] = bag_file_img_dic[s][t]

    def is_timestamp_valid_data(self,t):
        valid = True
        state = self.left_image_bound_to_data[t]['state']
        motor = self.left_image_bound_to_data[t]['motor']
        steer = self.left_image_bound_to_data[t]['steer']
        if state not in [1,3,5,6,7]:
            valid = False
        
        if motor < 51: # i.e., there must be at least a slight forward motor command 
            valid = False    
        if state in [3,5,6,7]: # Some strange things can happen when human takes control, steering gets stuck at max
            if steer > 99:
                valid = False
            elif steer < 1: # Can get stuck in steer = 0
                valid = False
        
        
        return valid
        
    ######################### GRAPHICS #############################################
    #
    def plot_L_file(self,fig_num=1,by_index=False):
        plt.rcParams['toolbar'] = 'toolbar2'
        steer=self.elements('steer')
        motor=self.elements('motor')
        encoder=self.elements('encoder')
        gyro=self.elements('gyro')   
        #ts,acc=elements(L,'acc') 
        state=self.elements('state')
        ts = self.timestamps
        
        ts_filtered,state_filtered = self.filtered_elements('state')
        _,motor_filtered = self.filtered_elements('motor')
        _,steer_filtered = self.filtered_elements('steer')
        _,gyro_filtered = self.filtered_elements('gyro')
        _,encoder_filtered = self.filtered_elements('encoder')
 
        if by_index:
            ts = range(len(ts))
            ts_filtered = range(len(ts_filtered))
        
        plt.plot(ts,motor,'0.7')
        plt.plot(ts,np.array(gyro)/10.,'0.7')
        #plt.plot(ts,np.array(acc)-10.,'0.7')
        plt.plot(ts,encoder,'0.7')
        plt.plot(ts,state,'0.7')
        plt.plot(ts,steer,'0.7')
        plt.plot(ts_filtered,state_filtered,'.')
        plt.plot(ts_filtered,steer_filtered,'.')

    def plot_click_L_file(self,fig_num=1,by_index=False):
        fig = plt.figure(fig_num,figsize=(14,4))
        plt.rcParams['toolbar'] = 'toolbar2'
        plt.clf()
        plt.ion()
        plt.show()
        fig.canvas.mpl_connect('button_press_event', button_press_event)
        self.plot_L_file(1,by_index)

    def elements(self,topic):
        data = []
        for t in self.timestamps:
            if topic in self.left_image_bound_to_data[t]:
                data.append(self.left_image_bound_to_data[t][topic])
            else:
                return []
        return np.array(data)

    def filtered_elements(self,topic):
        other = self.elements(topic)
        filtered = []
        ts_filtered = []
        for i in range(len(other)):
            if self.is_timestamp_valid_data(self.timestamps[i]):
               filtered.append(other[i])
               ts_filtered.append(self.timestamps[i]) 
        return ts_filtered,np.array(filtered)


    def play(self,start_t,stop_t,use_cv2=False,step=1):
        import cv2
        cv2.namedWindow('left',1)
        ts = sorted( self.img_dic.keys())
        print len(ts)
        img = np.zeros((94, 168,3),np.uint8)
        for i in range(0,len(ts),step):
            if ts[i] >= start_t and ts[i] < stop_t:
                if ts[i] in self.left_image_bound_to_data:
                    print ts[i],self.left_image_bound_to_data[ts[i]]['state']

                    im = self.img_dic[ts[i]].copy()
                    img[:,:,0] = im
                    img[:,:,1] = im
                    img[:,:,2] = im
                    #img = self.img_dic[ts[i]].copy()
                    steer_rect_color = [255,0,0]
                    #apply_rect_to_img(img,self.left_image_bound_to_data[ts[i]]['steer'],0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True)
                    apply_rect_to_img(img,self.left_image_bound_to_data[ts[i]]['acc'][0],-50,50,steer_rect_color,steer_rect_color,0.1,0.1,center=True,reverse=False)
                    apply_rect_to_img(img,self.left_image_bound_to_data[ts[i]]['acc'][1],-50,50,steer_rect_color,steer_rect_color,0.2,0.1,center=True,reverse=False)
                    apply_rect_to_img(img,self.left_image_bound_to_data[ts[i]]['acc'][2],-50,50,steer_rect_color,steer_rect_color,0.3,0.1,center=True,reverse=False)
                    #apply_rect_to_img(img,self.left_image_bound_to_data[ts[i]]['gyro'][0],-50,50,steer_rect_color,steer_rect_color,0.2,0.1,center=True,reverse=False)
                    m = max(0,self.left_image_bound_to_data[ts[i]]['motor']-49)
                    #apply_rect_to_img(img,m,0,49,steer_rect_color,steer_rect_color,0.1,0.1,center=False,reverse=False)
                    if use_cv2: # cv2 is fast, but slows if matplotlib figure is open.
                        cv2.imshow('left',img.astype('uint8'))
                        if cv2.waitKey(1) & 0xFF == ord('q'):   
                            return      
                    #t0 = time.time()   
                    else:
                        mi(self.img_dic[ts[i]],2,img_title=str(ts[i]))
                    plt.pause(0.033)#max(0.03 - time.time()-t0,0))
                else:
                    print "no data"        
        if use_cv2:
            cv2.destroyWindow('left')
        #
        ######################################################################
    


        """
            while True:
                bf=an_element(BCD.bag_folders_dic)
                if bf.data['acc_z'].mean() > 5 and len(bf.data['state_one_steps_1s_indicies']) > 1000: # the mean should be around 9.5 if acc is in datafile
                    break
        """


    def get_data(self,topics=['steer','motor'],num_topic_steps=10,num_image_steps=2,state_one_steps_indicies_str='state_one_steps_0_5s_indicies'):
        """
        state_one_steps_indicies_str can be, e.g.:
            'state_one_steps_1s_indicies' or 'state_one_steps_0_5s_indicies'

        topics means non-image topics
        """
        tries = 0
        while tries < 5:
            try:
                if len(self.binned_timestamp_nums[0]) > 0 and len(self.binned_timestamp_nums[1]) > 0:
                    start_index = random.choice(self.binned_timestamp_nums[np.random.randint(len(self.binned_timestamp_nums))])
                elif len(self.binned_timestamp_nums[0]) > 0:
                    start_index = random.choice(self.binned_timestamp_nums[0])
                elif len(self.binned_timestamp_nums[1]) > 0:
                    start_index = random.choice(self.binned_timestamp_nums[1])
                else:
                    break
                #start_index = random.choice(  self.data[state_one_steps_indicies_str])
                data_dic = {}
                data_dic['path'] = self.path
                for tp in topics:
                    data_dic[tp] = self.data[tp][start_index:(start_index+num_topic_steps)]
                for s in ['left']:
                    data_dic[s] = []   
                    for n in range(num_image_steps):
                        t = self.data['timestamps'][start_index+n]
                        data_dic[s].append(self.img_dic[s][t])
                for s in ['right']:
                    data_dic[s] = []   
                    for n in range(num_image_steps):
                        t_ = self.left_image_bound_to_data[t]['right_image']
                        data_dic[s].append(self.img_dic[s][t_])
                # assert that data_dic holds what it is supposed to hold.
                for tp in topics:
                    assert type(data_dic[tp]) == np.ndarray
                    assert len(data_dic[tp]) == num_topic_steps
                for s in ['left','right']:
                    assert type(data_dic[s]) == list
                    assert len(data_dic[s]) == num_image_steps
                    for i in range(num_image_steps):
                        assert type(data_dic[s][i]) == np.ndarray
                        assert shape(data_dic[s][i]) == (94, 168)
                self.returning_data_dic += 1
                return data_dic
            except:
                tries += 1
                #print "Try again."
        #print("Returning empty data_dic")
        self.returning_empty_data_dic += 1
        if np.mod(self.returning_empty_data_dic,1000) == 0:
            print(d2s("returning_empty_data_dic =",self.returning_empty_data_dic,"returning_data_dic =",self.returning_data_dic))
        return {}















class Bair_Car_Data:
    """ """
    def __init__(self, path, to_ignore=[]):
        self.bag_folders_with_loaded_images = {}
        self.bag_folders_priority_list = []
        self.bag_folders_dic = {}        
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
        #print "bag_folder_paths: "
        #print bag_folder_paths
        self.bag_folders_weighted = []
        for f in bag_folder_paths:
            n = len(gg(opj(f,'.preprocessed','*.bag.pkl')))
            m = len(gg(opj(f,'.preprocessed','left*')))
            #print(f.split('/')[-1],n,m)
            if n > 0 and m > 0:
                self.bag_folders_dic[f] = Bag_Folder(f)
                for i in range(max(n/10,1)):
                    self.bag_folders_weighted.append(f)

    def load_bag_folder_images(self,num_bags_to_load):
        self.bag_folders_priority_list = self.bag_folders_dic.keys()
        random.shuffle(self.bag_folders_priority_list)
        bag_count = 0
        i = 0
        for i in range(len(self.bag_folders_priority_list)):
            b = self.bag_folders_priority_list[i]
            bag_count += len(self.bag_folders_dic[b].files)
            if bag_count > num_bags_to_load:
                break
        cprint(d2s("\nUsing",i,"bag folders"),'red','on_green')
        for j in range(len(self.bag_folders_priority_list)-1,0,-1):
            #print j
            b = self.bag_folders_priority_list[j]
            if j <= i:
                if b in self.bag_folders_with_loaded_images:
                    cprint("Bair_Car_Data::load_bag_folder_images() already have "+b.split('/')[-1],'blue')
                    pass
                else:
                    #m=memory()
                    #free_propotion = m['free']/(1.0*m['total'])
                    #if free_propotion > min_free_proportion: 
                    self.bag_folders_dic[b].load_all_bag_files()
                    self.bag_folders_with_loaded_images[b] = 'Loaded'
                    cprint("Bair_Car_Data::load_bag_folder_images() loaded "+b.split('/')[-1],'green')
                    #else:
                    #    cprint("Bair_Car_Data::load_bag_folder_images() didn't load "+b+" because of memory limit.",'blink')
            else:
                if b in self.bag_folders_with_loaded_images:
                    cprint("Bair_Car_Data::load_bag_folder_images() removed "+b.split('/')[-1],'red')
                    del self.bag_folders_dic[b].img_dic
                    self.bag_folders_dic[b].img_dic = {}
                    del self.bag_folders_with_loaded_images[b]
                    #gc.collect()
        cprint(d2s("Bair_Car_Data::load_bag_folder_images() self.bag_folders_with_loaded_images (",len(self.bag_folders_with_loaded_images),')'),'yellow','on_blue')
        for f in self.bag_folders_with_loaded_images:
            print '\t'+f.split('/')[-1]

        """
        for b in self.bag_folders_priority_list:
            if b in self.bag_folders_with_loaded_images:
                pass
            else:
                #while True:
                freed_bag_folder = self.free_memory(free_memory_proportion)
                if freed_bag_folder == b:
                    print "Bair_Car_Data::load_bag_folder_images() freed_bag_folder == " + b
                    return
                #    if freed_bag_folder == None:
                #        break
                self.bag_folders_dic[b].load_all_bag_files()
                self.bag_folders_with_loaded_images[b] = 'Loaded'
                print "Bair_Car_Data::load_bag_folder_images() loaded "+b
                print d2s("Bair_Car_Data::load_bag_folder_images() self.bag_folders_with_loaded_images (",len(self.bag_folders_with_loaded_images),')')
                for f in self.bag_folders_with_loaded_images:
                    print '\t'+f.split('/')[-1]
        """

    """
    def free_memory(self, min_free_proportion=0.15, min_free_gigabytes=3.0):
        free_propotion = 1.0
        free_gigabytes = 999999.0
        if '/Users/' not in home_path: # OSX doesn't have the memory() function that linux has.
            m=memory()
            #print m['free']/(1.0*m['total'])
            #while m['free']/(1.0*m['total']) < 0.15:
            free_propotion = m['free']/(1.0*m['total'])
            print d2s('Bair_Car_Data::free_memory() free_propotion =', free_propotion)
        else:
            free_gigabytes = OSX_free_memory()
        if free_propotion < min_free_proportion or free_gigabytes < min_free_gigabytes:
            for i in range(len(self.bag_folders_priority_list)-1,-1,-1):
                b = self.bag_folders_priority_list[i]
                if b in self.bag_folders_with_loaded_images:
                    #del self.bag_folders_dic[b].img_dic
                    self.bag_folders_dic[b].img = {}
                    del self.bag_folders_with_loaded_images[b]
                    print "Bair_Car_Data::free_memory() removed "+b
                    return b
        return None


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
    """


    def get_data(self,topics=['steer','motor'],num_topic_steps=10,num_image_steps=2,state_one_steps_indicies_str='state_one_steps_0_5s_indicies'):
        while True:
            rc = random.choice(self.bag_folders_weighted)
            if rc in self.bag_folders_with_loaded_images:
                break
        return self.bag_folders_dic[random.choice(self.bag_folders_weighted)].get_data(topics,num_topic_steps,num_image_steps,state_one_steps_indicies_str)


#bag_folders_weighted
#bag_folders_with_loaded_images