"""



"""

from kzpy3.vis import *
if '/Users/' in home_path:
    from kzpy3.misc.OSX_free_memory import OSX_free_memory





click_ts = []
def button_press_event(event):
    global click_ts
    #print len(click_ts)
    ts = event.xdata
    click_ts.append(ts)
    print click_ts[-2:]

def z2o_plot(x,y,y_offset,plt_str='.',label='no label'):
    return plt.plot(x,z2o(y)+y_offset,plt_str,label=label)

"""
Make 'contact prints' of bag folders
"""

class Bag_Folder:
    def __init__(self, path, NUM_STATE_ONE_STEPS=15):
        if True:
            self.path = path
            cprint('Bag_Folder::__init__, path = '+path,'yellow','on_red')
            self.files = sorted(glob.glob(opj(path,'.preprocessed','*.bag.pkl')))
            file_path = opj(path,'.preprocessed','left_image_bound_to_data2.pkl')
            if len(gg(file_path)) == 0:
                file_path = opj(path,'.preprocessed','left_image_bound_to_data.pkl')
            self.incremental_index = -1
            self.left_image_bound_to_data = load_obj(file_path)
            self.img_dic = {}
            self.img_dic['left'] = {}
            self.img_dic['right'] = {}
            self.load_all_bag_files()

            timestamps = sorted(list(set(self.left_image_bound_to_data.keys()).intersection(self.img_dic['left'])))

            cprint('checking assertions . . .','yellow')
            if False:
                ctr = 0
                for t in timestamps:
                    if np.mod(ctr,1000) == 0:
                        print ctr
                    assert(t in self.left_image_bound_to_data.keys())
                    assert(t in self.img_dic['left'])
                    assert(self.left_image_bound_to_data[t]['right_image'] in self.img_dic['right'])
                    ctr += 1
            bad_timestamps = []
            for t in timestamps:
                L = self.img_dic['left'][t]
                r_t = self.left_image_bound_to_data[t]['right_image']
                if r_t in self.img_dic['right']:
                    R = self.img_dic['right'][r_t]
                    assert type(L) == np.ndarray
                    assert type(R) == np.ndarray
                    assert shape(L) == (94, 168)
                    assert shape(R) == (94, 168)
                else:
                    bad_timestamps.append(t)
            if len(bad_timestamps) > 0:
                for bt in bad_timestamps:
                    timestamps.remove(bt)
                cprint('Removed bad_timestamps:','red')
                print bad_timestamps
            cprint('assertions okay','yellow')


            self.returning_data_dic = 0
            self.returning_empty_data_dic = 0

            # Corrections. We need to adjust some State values that were interpolated.
            for t in timestamps: # There i=was interpolation of values. For State we don't want this! Here we undo the problem.
                s = self.left_image_bound_to_data[t]['state'] 
                self.left_image_bound_to_data[t]['state'] = np.round(s) 
            for i in range(len(timestamps)-2): # Here we assume that isolated state 4 timepoints are rounding/sampling errors.
                t0 = timestamps[i]
                t1 = timestamps[i+1]
                t2 = timestamps[i+2]
                if self.left_image_bound_to_data[t1]['state'] == 4:
                    if self.left_image_bound_to_data[t0]['state'] != 4:
                        if self.left_image_bound_to_data[t2]['state'] != 4:
                                self.left_image_bound_to_data[t1]['state'] = self.left_image_bound_to_data[t0]['state']

            state_one_steps = 0
            for i in range(len(timestamps)-2,-1,-1):
                self.left_image_bound_to_data[timestamps[i]]['state_one_steps'] = 0 # overwrite loaded values
                if self.is_timestamp_valid_data(timestamps[i]) and timestamps[i+1] - timestamps[i] < 0.3:
                    state_one_steps += 1
                else:
                    state_one_steps = 0
                self.left_image_bound_to_data[timestamps[i]]['state_one_steps'] = state_one_steps
            self.data = {}
            self.data['timestamps'] = timestamps #np.array(timestamps) # list or array?
            self.data['state'] = self.elements('state')
            self.data['steer'] = self.elements('steer')
            self.data['motor'] = self.elements('motor')
            
            gyro = self.elements('gyro')
            self.data['gyro_x'] = gyro[:,0]
            self.data['gyro_z'] = gyro[:,1]
            self.data['gyro_y'] = gyro[:,2]
            self.data['encoder'] = self.elements('encoder')
            self.data['state_one_steps'] = self.elements('state_one_steps')

            acc = self.elements('acc')
            if len(acc) > 0: # acc added later than other sensors, not in all bagfiles
                self.data['acc_x'] = acc[:,0]
                self.data['acc_z'] = acc[:,1]
                self.data['acc_y'] = acc[:,2]
            else:
                self.data['acc_x'] = 0*self.data['gyro_x'].copy()
                self.data['acc_z'] = 0*self.data['gyro_x'].copy()
                self.data['acc_y'] = 0*self.data['gyro_x'].copy()
            assert(len(self.data['acc_x']) == len(self.data['state']))
            assert(len(self.data['acc_y']) == len(self.data['state']))
            assert(len(self.data['acc_z']) == len(self.data['state']))


            extremes = [['gyro_x', -140,140],
                ['gyro_z', -140,140],
                ['gyro_y',-140,140],
                ['encoder', 0, 10],
                ['acc_x',-12,12],
                ['acc_y', -12,12],
                ['acc_z',-8,20],
                ['motor',0,99],
                ['steer',0,99]]
            for e in extremes:
                cprint(d2s("Bag_Folder::__init__", e[0],len(self.data[e[0]])),'blue')
                self.fix_extremes(e[0],e[1],e[2])


            self.data['state_one_steps_0_5s_indicies'] = np.where(np.array(self.data['state_one_steps'])>=NUM_STATE_ONE_STEPS)[0]

            self.binned_timestamp_nums = [[],[]]
            for i in range(len(self.data['state_one_steps_0_5s_indicies'])):
                steer = self.data['steer'][i]
                if steer < 43 or steer > 55:
                    self.binned_timestamp_nums[0].append(self.data['state_one_steps_0_5s_indicies'][i])
                else:
                    self.binned_timestamp_nums[1].append(self.data['state_one_steps_0_5s_indicies'][i])

            self.good_timestamps = np.array(self.data['timestamps'])[self.data['state_one_steps_0_5s_indicies']]

            print "Bag_Folder::init() preloaded " + self.path.split('/')[-1] + " (" + str(len(self.files)) + " bags)"



    def fix_extremes(self,topic,min_val,max_val):
        d = self.data[topic]
        mn = d[d<min_val]
        if len(mn)>0:
            cprint(d2s('Bag_Folder::fix_extremes, Warning: limiting',len(mn),topic,'values (i.e.,',(100*len(mn))/(1.0*len(d)),'%) to',min_val),'red')
            d[d<min_val] = min_val
        mx = d[d>max_val]
        if len(mx)>0:
            cprint(d2s('Bag_Folder::fix_extremes, Warning: limiting',len(mx),topic,'values (i.e.,',(100*len(mx))/(1.0*len(d)),'%) to',max_val),'red')
            d[d>max_val] = max_val
        #print(d2s(topic,":len=",len(d),",",len(mn),len(mx)))

    def all_hists(self):
        plt.ion()
        for topic in self.data.keys():
            plt.figure('histograms')
            plt.clf()
            plt.title(topic)
            plt.hist(self.data[topic],bins=100)
            plt.pause(0.1)
            print(topic)
            raw_input('(press enter to continue)')


    def load_all_bag_files(self):
        for f in self.files:
            bag_file_img_dic = load_obj(f)
            for s in ['left','right']:
                for t in bag_file_img_dic[s].keys():
                    self.img_dic[s][t] = bag_file_img_dic[s][t]



    def make_contact_print(self,X=20,Y=20):
        step = int(len(self.data['state_one_steps_0_5s_indicies'])/(X*Y))
        num = 0
        shp = shape(an_element(self.img_dic['left']))
        width = shp[0]
        height = shp[1]
        offset = width/20
        contact_print = np.zeros(((width+offset)*X,(height+offset)*Y),'uint8') + 128
        for x in range(X):
            for y in range(Y):
                indx = self.data['state_one_steps_0_5s_indicies'][num]
                ts = self.data['timestamps'][indx]
                x_ = x*(width+offset)
                y_ = y*(height+offset)
                contact_print[x_:(x_+width),y_:(y_+height)] = self.img_dic['left'][ts]
                #mi(self.img_dic['left'][ts],img_title=d2s(x,y,num,len(self.data['state_one_steps_0_5s_indicies'])))
                plt.pause(0.00002)
                num += step
        return contact_print



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
        


    def elements(self,topic):
        data = []
        for t in self.data['timestamps']:
            if topic in self.left_image_bound_to_data[t]:
                data.append(self.left_image_bound_to_data[t][topic])
            else:
                return []
        return np.array(data)

    
    def verify_get_data(self,d,do_print=False):
        ts = d['timestamp']
        assert(ts in self.good_timestamps)
        assert(self.is_timestamp_valid_data(ts))
        if do_print:
            print(d2s(ts,'ok'))



    def get_data(self,topics=['steer','motor'],num_topic_steps=10,num_image_steps=2,randomized=False):
        tries = 0
        while tries < 5:
            try:
                if randomized:
                    if len(self.binned_timestamp_nums[0]) > 0 and len(self.binned_timestamp_nums[1]) > 0:
                        start_index = random.choice(self.binned_timestamp_nums[np.random.randint(len(self.binned_timestamp_nums))])
                    elif len(self.binned_timestamp_nums[0]) > 0:
                        start_index = random.choice(self.binned_timestamp_nums[0])
                    elif len(self.binned_timestamp_nums[1]) > 0:
                        start_index = random.choice(self.binned_timestamp_nums[1])
                    else:
                        break
                else:
                    start_index = self.incremental_index
                    while True:
                        self.incremental_index += 1
                        if self.incremental_index in self.data['state_one_steps_0_5s_indicies']: #This shouldn't be necessary.
                            break
                        if self.incremental_index >= len(self.data['state_one_steps_0_5s_indicies']):
                            self.incremental_index = -1
                            return 'finished_bag_folder'

                data_dic = {}
                data_dic['path'] = self.path
                data_dic['timestamp'] = self.data['timestamps'][start_index]
                data_dic['state'] = self.data['state'][start_index]
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
                self.verify_get_data(data_dic)
                self.returning_data_dic += 1
                return data_dic
            except:
               tries += 1
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
        self.incremental_index = 0
        self.ctr = 0
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
                self.bag_folders_with_loaded_images[f] = True
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

    

    def get_data(self,topics=['steer','motor'],num_topic_steps=10,num_image_steps=2,randomized=False):
        if randomized:
            while True:
                rc = random.choice(self.bag_folders_weighted)
                if rc in self.bag_folders_with_loaded_images:
                    break
            return self.bag_folders_dic[random.choice(self.bag_folders_weighted)].get_data(topics,num_topic_steps,num_image_steps,True)

        else:
            self.bag_folders_with_loaded_images_list = sorted(self.bag_folders_with_loaded_images.keys())
            while True:
                data = self.bag_folders_dic[self.bag_folders_with_loaded_images_list[self.incremental_index]].get_data(topics,num_topic_steps,num_image_steps,False)
                if data != 'finished_bag_folder':
                    if self.ctr == 0:
                        print('self.ctr == 0')
                    if np.mod(self.ctr,1000) == 0:
                        cprint(self.bag_folders_with_loaded_images_list[self.incremental_index],'magenta')
                        self.ctr += 1
                    return data        
                else:
                    self.incremental_index += 1
                    if self.incremental_index >= len(sorted(self.bag_folders_with_loaded_images_list)):
                        self.incremental_index = 0

