
from kzpy3.vis import *


class Bag_Folder:
    def __init__(self, path, NUM_STATE_ONE_STEPS=10):
        self.path = path
        cprint('Bag_Folder::__init__, path = '+path,'yellow','on_red')
        self.files = sorted(glob.glob(opj(path,'.preprocessed','*.bag.pkl')))
        left_path = opj(path,'.preprocessed','left_image_bound_to_data2.pkl')
        if len(gg(left_path)) == 0:
            left_path = opj(path,'.preprocessed','left_image_bound_to_data.pkl')
        self.left_image_bound_to_data = load_obj(left_path)
        if 'acc' not in an_element(self.left_image_bound_to_data):
            for ts in self.left_image_bound_to_data:
                self.left_image_bound_to_data[ts]['acc'] = [0.,9.8,0.]
        self.data = {}
        self.data['raw_timestamps'] = sorted(self.left_image_bound_to_data.keys())
        self.good_timestamps_to_raw_timestamps_indicies__dic = {}
        self.img_dic = {}
        self.img_dic['left'] = {}
        self.img_dic['right'] = {}
        self.incremental_index = 0
        self.timestamp_num = 0
        for f in self.files:
            bag_file_img_dic = load_obj(f)
            for s in ['left','right']:
                for ts in bag_file_img_dic[s].keys():
                    self.img_dic[s][ts] = bag_file_img_dic[s][ts]
        good_timestamps_set = set(self.left_image_bound_to_data.keys()) & set(self.img_dic['left'].keys())
        bad_timestamps_list = []
        cprint('basic checking . . .','yellow')
        for ts in self.data['raw_timestamps']:
            if not ts in self.img_dic['left']:
                bad_timestamps_list.append(ts)
                continue                
            if not self.left_image_bound_to_data[ts]['right_image'] in self.img_dic['right']:
                bad_timestamps_list.append(ts)
                continue
            L = self.img_dic['left'][ts]
            r_t = self.left_image_bound_to_data[ts]['right_image']
            R = self.img_dic['right'][r_t]
            #assert(type(L) == np.ndarray)
            if not type(L) == np.ndarray:
                bad_timestamps_list.append(ts)
                continue
            #assert(type(R) == np.ndarray)
            if not type(R) == np.ndarray:
                bad_timestamps_list.append(ts)
                continue
            #assert(shape(L) == (94, 168))
            if not  shape(L) == (94, 168):
                bad_timestamps_list.append(ts)
                continue
            #assert( shape(R) == (94, 168))    
            if not  shape(R) == (94, 168):
                bad_timestamps_list.append(ts)
                continue
            SL = self.left_image_bound_to_data
            #assert('encoder' in SL[ts])
            if not 'encoder' in SL[ts]:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not 'gyro' in SL[ts]:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not 'motor' in SL[ts]:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not 'steer' in SL[ts]:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not 'state' in SL[ts]:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not type(SL[ts]['encoder']) == float:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not len(SL[ts]['gyro']) == 3:
                bad_timestamps_list.append(ts)
                continue
            if not len(SL[ts]['acc']) == 3:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not type(SL[ts]['motor']) == float:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not type(SL[ts]['steer']) == float:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not type(SL[ts]['state']) == float:
                bad_timestamps_list.append(ts)
                continue


        if len(bad_timestamps_list) > 0:
            good_timestamps_set -= set(bad_timestamps_list)
            cprint(d2s('Removed bad_timestamps:',len(bad_timestamps_list),'of',len(good_timestamps_set),'total.'),'red')
            #print bad_timestamps_list
        cprint('basic checking done','yellow')

        # Corrections. We need to adjust some State values that were interpolated.
        for ts in good_timestamps_set: # There i=was interpolation of values. For State we don't want this! Here we undo the problem.
            s = self.left_image_bound_to_data[ts]['state'] 
            self.left_image_bound_to_data[ts]['state'] = np.round(s)

        good_timestamps_list = sorted(list(good_timestamps_set))
        del good_timestamps_set

        for i in range(len(good_timestamps_list)-2): # Here we assume that isolated state 4 timepoints are rounding/sampling errors.
            t0 = good_timestamps_list[i]
            t1 = good_timestamps_list[i+1]
            t2 = good_timestamps_list[i+2]
            if self.left_image_bound_to_data[t1]['state'] == 4:
                if self.left_image_bound_to_data[t0]['state'] != 4:
                    if self.left_image_bound_to_data[t2]['state'] != 4:
                            self.left_image_bound_to_data[t1]['state'] = self.left_image_bound_to_data[t0]['state']

        state_one_steps = 0
        for i in range(len(good_timestamps_list)-2,-1,-1):
            self.left_image_bound_to_data[good_timestamps_list[i]]['state_one_steps'] = 0 # overwrite loaded values
            if self.is_timestamp_valid_data(good_timestamps_list[i]) and good_timestamps_list[i+1] - good_timestamps_list[i] < 0.3:
                state_one_steps += 1
            else:
                state_one_steps = 0
            self.left_image_bound_to_data[good_timestamps_list[i]]['state_one_steps'] = state_one_steps

        bad_timestamps = []
        for ts in good_timestamps_list:
            if self.left_image_bound_to_data[ts]['state_one_steps'] < NUM_STATE_ONE_STEPS:
                bad_timestamps.append(ts)

        
        self.data['good_start_timestamps'] = sorted(list(set(good_timestamps_list) - set(bad_timestamps)))
        
        for gts in self.data['good_start_timestamps']:
            raw_index = self.data['raw_timestamps'].index(gts)
            self.good_timestamps_to_raw_timestamps_indicies__dic[gts] = raw_index

        if len(self.data['good_start_timestamps']) == 0:
            cprint("""WARNING!!!!, len(self.data['good_start_timestamps']) == 0, ***NO DATA***,"""+self.path,'red','on_yellow')
            self.img_dic = {}
            return None

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
        print acc
        self.data['acc_x'] = acc[:,0]
        self.data['acc_z'] = acc[:,1]
        self.data['acc_y'] = acc[:,2]

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

        self.binned_timestamp_nums = [[],[]]
        for i in range(len(self.data['good_start_timestamps'])):
            t = self.data['good_start_timestamps'][i]
            steer = self.left_image_bound_to_data[t]['steer']
            if steer < 43 or steer > 55:
                self.binned_timestamp_nums[0].append(i)
            else:
                self.binned_timestamp_nums[1].append(i)
            #print((len(self.binned_timestamp_nums[0]),len(self.binned_timestamp_nums[1])))


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
        
    def elements_older(self,topic):
        data = []
        for t in self.data['good_start_timestamps']:
            if topic in self.left_image_bound_to_data[t]:
                data.append(self.left_image_bound_to_data[t][topic])
            else:
                print 'def elements(self,topic)::returning nothing'
                return []
        return np.array(data)

    def elements(self,topic):
        data = []
        for t in self.data['raw_timestamps']:
            if topic in self.left_image_bound_to_data[t]:
                data.append(self.left_image_bound_to_data[t][topic])
            else:
                data.append(-999.999)
                print "Bag_Folder::elements Warning, data.append(-999.999), topic ="+topic
        return np.array(data)



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

    def get_data_older(self,topics=['state','steer','motor'],num_topic_steps=10,num_image_steps=2):
        if self.incremental_index >= len(self.data['good_start_timestamps']):
            return 'end_of_bag_folder_reached'
        start_index = self.incremental_index
        start_timestep = self.data['good_start_timestamps'][start_index]
        data_dic = {}
        data_dic['path'] = self.path
        data_dic['timestamp'] = self.data['good_start_timestamps'][start_index:(start_index+num_topic_steps)]
        for tp in topics:
            data_dic[tp] = self.data[tp][start_index:(start_index+num_topic_steps)]

        data_dic['left'] = []
        data_dic['right'] = []
        for n in range(num_image_steps):
            t = self.data['good_start_timestamps'][start_index+n]
            data_dic['left'].append(self.img_dic['left'][t])
            t_ = self.left_image_bound_to_data[t]['right_image']
            data_dic['right'].append(self.img_dic['right'][t_])

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
        self.incremental_index
        return data_dic


    def get_data(self,topics=['state','steer','motor'],num_topic_steps=10,num_image_steps=2,step = 0):
        #if self.incremental_index >= len(self.data['good_start_timestamps']):
        #    return 'end_of_bag_folder_reached'
        #start_index = self.incremental_index
        if not hasattr(self, 'timestamp_num'):
            self.timestamp_num = lambda: None
            setattr(self,'timestamp_num', 0)
        #if step == 0:
        #    self.timestamp_num = random.choice(self.binned_timestamp_nums[np.random.randint(len(self.binned_timestamp_nums))])
        timestamp = self.data['good_start_timestamps'][self.timestamp_num]
        
        if step == 0:
            if len(self.binned_timestamp_nums[0]) > 0 and len(self.binned_timestamp_nums[1]) > 0:
                self.timestamp_num = random.choice(self.binned_timestamp_nums[np.random.randint(len(self.binned_timestamp_nums))])
            elif len(self.binned_timestamp_nums[0]) > 0:
                self.timestamp_num = random.choice(self.binned_timestamp_nums[0])
            elif len(self.binned_timestamp_nums[1]) > 0:
                self.timestamp_num = random.choice(self.binned_timestamp_nums[1])
            else:
                assert(False) #return None
        timestamp = self.data['good_start_timestamps'][self.timestamp_num]

        
        raw_start_index = self.good_timestamps_to_raw_timestamps_indicies__dic[timestamp] + step

        data_dic = {}
        data_dic['path'] = self.path
        data_dic['timestamp'] = self.data['raw_timestamps'][raw_start_index:(raw_start_index+num_topic_steps)]
        for tp in topics:
            data_dic[tp] = self.data[tp][raw_start_index:(raw_start_index+num_topic_steps)]

        data_dic['left'] = []
        data_dic['right'] = []
        for n in range(num_image_steps):
            t = self.data['raw_timestamps'][raw_start_index+n]
            data_dic['left'].append(self.img_dic['left'][t])
            t_ = self.left_image_bound_to_data[t]['right_image']
            data_dic['right'].append(self.img_dic['right'][t_])

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
        self.incremental_index
        return data_dic

    def make_contact_print(self,X=20,Y=20):
        step = int(len(self.data['good_start_timestamps'])/(X*Y))
        num = 0
        shp = shape(an_element(self.img_dic['left']))
        width = shp[0]
        height = shp[1]
        offset = width/20
        contact_print = np.zeros(((width+offset)*X,(height+offset)*Y),'uint8') + 128
        for x in range(X):
            for y in range(Y):
                ts = self.data['good_start_timestamps'][num]
                #ts = self.data['raw_timestamps'][indx]
                x_ = x*(width+offset)
                y_ = y*(height+offset)
                contact_print[x_:(x_+width),y_:(y_+height)] = self.img_dic['left'][ts]
                #mi(self.img_dic['left'][ts],img_title=d2s(x,y,num,len(self.data['state_one_steps_0_5s_indicies'])))
                plt.pause(0.00002)
                num += step
        return contact_print
"""
def show_data_sequence(BF,N):
    caffe_steer_color_color = [255,0,0]
    human_steer_color_color = [0,0,255]
    t0 = 0
    dt = 0
    for i in range(N):
        d = BF.get_data(['state','steer','motor','encoder','gyro_x','gyro_y','gyro_z','acc_x','acc_y','acc_z'])
        if i > 0:
            img_prev = img.copy()
        img = np.zeros((shape(d['right'][0])[0],shape(d['right'][0])[1],3),'uint8')
        dt = d['timestamp'][0] - t0
        #mi(d['left'][1],3,[1,2,2])
        #mi(d['right'][1],3,[1,2,1],do_clf=False)
        plt.pause(0.0001)
        img[:,:,0] = d['right'][0].copy()
        img[:,:,1] = d['right'][0].copy()
        img[:,:,2] = d['right'][0].copy()
        BF.incremental_index += 1
        if np.int(d['state'][0]) in [3,6]: #caffe is steering
            steer_rect_color = caffe_steer_color_color
        else:
            steer_rect_color = human_steer_color_color
        apply_rect_to_img(img,d['steer'][0],0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=True)
        apply_rect_to_img(img,d['acc_x'][0],-6,8,steer_rect_color,steer_rect_color,0.78,0.05,center=True,reverse=False,horizontal=True)
        apply_rect_to_img(img,d['gyro_x'][0],-60,60,steer_rect_color,steer_rect_color,0.75,0.05,center=True,reverse=False,horizontal=True)        
        
        apply_rect_to_img(img,80-d['motor'][0],0,80,steer_rect_color,steer_rect_color,0.8,0.05,center=False,reverse=True,horizontal=False)
        apply_rect_to_img(img,8-d['encoder'][0],0,8,steer_rect_color,steer_rect_color,0.78,0.05,center=False,reverse=True,horizontal=False)

        apply_rect_to_img(img,d['gyro_y'][0],-240,240,steer_rect_color,steer_rect_color,0.2,0.05,center=True,reverse=False,horizontal=False)
        apply_rect_to_img(img,d['acc_y'][0],-48,48,steer_rect_color,steer_rect_color,0.18,0.05,center=True,reverse=False,horizontal=False)
        apply_rect_to_img(img,d['gyro_z'][0],-480,480,steer_rect_color,steer_rect_color,0.16,0.05,center=True,reverse=False,horizontal=False)
        apply_rect_to_img(img,d['acc_z'][0],-135,160,steer_rect_color,steer_rect_color,0.14,0.05,center=True,reverse=False,horizontal=False)
        #apply_rect_to_img(img,d['gyro_z'][0],-280*2,280*2,steer_rect_color,steer_rect_color,0.12,0.05,center=True,reverse=True,horizontal=False)
        if dt > 0.06 and i > 0:
            #img_prev[:,:,1] = img_prev[:,:,1] / 2
            #img_prev[:,:,2] = img_prev[:,:,2] / 2
            pz = min(dt,1.0)
            mi(img_prev,img_title=(d2s('dt = ', int(1000*dt),'ms')))
            plt.pause(pz)

        pz = 0.0001
        mi(img,img_title=(d2s('dt = ', int(1000*dt),'ms')))
        t0 = d['timestamp'][0]
        plt.pause(pz)
"""

def show_data_dic(d):
    caffe_steer_color_color = [255,0,0]
    human_steer_color_color = [0,0,255]
    t0 = 0
    dt = 0
    for i in range(len(d['steer'])):
        #print i
        if i > 0:
            img_prev = img.copy()
        img = np.zeros((shape(d['right'][0])[0],shape(d['right'][0])[1],3),'uint8')
        dt = d['timestamp'][i] - t0
        #mi(d['left'][1],3,[1,2,2])
        #mi(d['right'][1],3,[1,2,1],do_clf=False)
        plt.pause(0.0001)
        img[:,:,0] = d['right'][i].copy()
        img[:,:,1] = d['right'][i].copy()
        img[:,:,2] = d['right'][i].copy()

        if np.int(d['state'][i]) in [3,6]: #caffe is steering
            steer_rect_color = caffe_steer_color_color
        else:
            steer_rect_color = human_steer_color_color
        apply_rect_to_img(img,d['steer'][i],0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=True)
        apply_rect_to_img(img,d['acc_x'][i],-8,8,steer_rect_color,steer_rect_color,0.78,0.05,center=True,reverse=False,horizontal=True)
        apply_rect_to_img(img,d['gyro_x'][i],-60,60,steer_rect_color,steer_rect_color,0.75,0.05,center=True,reverse=False,horizontal=True)        
        
        apply_rect_to_img(img,d['motor'][i],49,99,steer_rect_color,steer_rect_color,0.8,0.05,center=False,reverse=True,horizontal=False)
        apply_rect_to_img(img,d['encoder'][i],0,15,steer_rect_color,steer_rect_color,0.78,0.05,center=False,reverse=True,horizontal=False)

        apply_rect_to_img(img,d['gyro_y'][i],-240,240,steer_rect_color,steer_rect_color,0.2,0.05,center=True,reverse=False,horizontal=False)
        apply_rect_to_img(img,d['acc_y'][i],-48,48,steer_rect_color,steer_rect_color,0.18,0.05,center=True,reverse=False,horizontal=False)
        apply_rect_to_img(img,d['gyro_z'][i],-480,480,steer_rect_color,steer_rect_color,0.16,0.05,center=True,reverse=False,horizontal=False)
        apply_rect_to_img(img,d['acc_z'][i],-135,160,steer_rect_color,steer_rect_color,0.14,0.05,center=True,reverse=False,horizontal=False)
        apply_rect_to_img(img,d['gyro_z'][i],-280*2,280*2,steer_rect_color,steer_rect_color,0.12,0.05,center=True,reverse=True,horizontal=False)
        if dt > 0.06 and i > 0:
            #img_prev[:,:,1] = img_prev[:,:,1] / 2
            #img_prev[:,:,2] = img_prev[:,:,2] / 2
            pz = min(dt,1.0)
            mi(img_prev,img_title=(d2s('dt = ', int(1000*dt),'ms')))
            plt.pause(pz)

        pz = 0.0001
        mi(img,img_title=(d2s('dt = ', int(1000*dt),'ms')))
        t0 = d['timestamp'][i]
        plt.pause(pz)


"""
dts = []
raw_timestamps = sorted(BF.img_dic['right'].keys()) #sorted(BF.left_image_bound_to_data.keys())
for i in range(len(raw_timestamps)-2):
    dt = raw_timestamps[i+1]-raw_timestamps[i]
    if dt < .11:
        dts.append(dt)
plt.figure(2)
plt.clf()
plt.hist(dts,bins=50);
True
"""




"""
bins steering
weight folder
"""

def make_contact_prints():
    unix('mkdir -p '+opjD('bair_car_data_contact_sheets'))
    files = gg(opjD('train_preprocessed_bag_folder_path','*.pkl'))
    for f in files:
        print f
        BF = load_obj(f)
        cs = BF.make_contact_print()
        imsave(opjD('bair_car_data_contact_sheets',f.split('/')[-1]+'.png'),cs)









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
        #print "bag_folder_paths: "
        #print bag_folder_paths
        self.bag_folders_weighted = []
        train_preprocessed_bag_folder_path = opjD('train_preprocessed_bag_folder_path')
        if True:#try:
            unix('mkdir -p '+train_preprocessed_bag_folder_path)
            for f in bag_folder_paths:
                n = len(gg(opj(f,'.preprocessed','*.bag.pkl')))
                m = len(gg(opj(f,'.preprocessed','left*')))
                #print opj(train_preprocessed_bag_folder_path,f.split('/')[-1]+'.pkl')
                if len(gg(opj(train_preprocessed_bag_folder_path,f.split('/')[-1]+'.pkl'))) == 1:
                    self.bag_folders_dic[f] = load_obj(opj(train_preprocessed_bag_folder_path,f.split('/')[-1]+'.pkl'))
                    print "loaded "+opj(train_preprocessed_bag_folder_path,f.split('/')[-1]+'.pkl')
                else:
                    n = len(gg(opj(f,'.preprocessed','*.bag.pkl')))
                    m = len(gg(opj(f,'.preprocessed','left*')))
                    #print(f.split('/')[-1],n,m)
                    if n > 0 and m > 0:
                        self.bag_folders_dic[f] = Bag_Folder(f,NUM_STATE_ONE_STEPS)
                        bpath = opj(train_preprocessed_bag_folder_path,self.bag_folders_dic[f].path.split('/')[-1]+'.pkl')
                        if len(gg(bpath)) == 0:
                            print("saveing "+bpath)
                            save_obj(self.bag_folders_dic[f],bpath)
                self.bag_folders_with_loaded_images[f] = True
                for i in range(max(n/10,1)):
                    self.bag_folders_weighted.append(f)
        self.current_bag_folder = random.choice(self.bag_folders_weighted)
        if False: #except Exception as e:
            cprint("Bair_Car_Data::__init__ ********** Exception ******* with "+f,'red')
            print e.message, e.args


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

    

    def get_data(self,topics=['steer','motor'],num_topic_steps=10,num_image_steps=2):
        self.bag_folders_with_loaded_images_list = sorted(self.bag_folders_with_loaded_images.keys())
        t0 = time.time()
        
        while True:
            if np.random.random() > 0.00:
                self.current_bag_folder = random.choice(self.bag_folders_weighted)
                #print "Bair_Car_Data::get_data, self.current_bag_folder = "+self.current_bag_folder
            #rc = random.choice(self.bag_folders_with_loaded_images_list)
            BF = self.bag_folders_dic[self.current_bag_folder]
            BF.incremental_index = np.random.randint(0,len(BF.data['good_start_timestamps']))
            data = BF.get_data(topics,num_topic_steps,num_image_steps,self.step)
            self.step += 1
            if self.step >= 1:
                self.step = 0

            if data != 'end_of_bag_folder_reached':
                if self.ctr == 0:
                    print('self.ctr == 0')
                if np.mod(self.ctr,1000) == 0:
                    cprint(self.bag_folders_with_loaded_images_list[self.incremental_index],'magenta')
                    self.ctr += 1
                return data        
            if time.time()-t0 > 60:
                print "Bair_Car_Data::get_data, timeout"
                assert(0)
