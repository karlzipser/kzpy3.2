
from kzpy3.vis import *
import cv2

good_start_timestamp_indicies_test_results = load_obj(opjD('good_start_timestamp_indicies_test_results'))

#
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
            cprint("""Bag_Folder::__init__, WARNING!!!!, len(self.data['good_start_timestamps']) == 0, ***NO DATA***,"""+self.path,'red','on_yellow')
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

        self.steer_angle_dic = {}
        for i in range(len(self.data['good_start_timestamps'])):
            good_timestamp = self.data['good_start_timestamps'][i]
            raw_timestamp = self.good_timestamps_to_raw_timestamps_indicies__dic[good_timestamp]
            steer = self.data['steer'][raw_timestamp]
            steer = int(steer)
            if steer < 0:
                steer = 0
            if steer > 99:
                steer = 99
            if not steer in self.steer_angle_dic:
                self.steer_angle_dic[steer] = []
            self.steer_angle_dic[steer].append(i)


        self.motor_level_dic = {}
        self.make_motor_level_dic()
        #self.loss_indicies_dic = {}
        self.make_loss_indicies_dic()

        cprint(d2s("Bag_Folder::__init__, good_start_timestamps =",len(self.data['good_start_timestamps']),"out of",len(self.data['raw_timestamps']),"raw_timestamps, i.e.",int(100*len(self.data['good_start_timestamps'])/(1.0*len(self.data['raw_timestamps']))),"%"))


    def make_motor_level_dic(self):
        for i in range(len(self.data['good_start_timestamps'])):
            good_timestamp = self.data['good_start_timestamps'][i]
            raw_timestamp = self.good_timestamps_to_raw_timestamps_indicies__dic[good_timestamp]
            motor = self.data['motor'][raw_timestamp]
            motor = int(motor)
            if motor < 0:
                motor = 0
            if motor > 99:
                motor = 99
            if not motor in self.motor_level_dic:
                self.motor_level_dic[motor] = []
            self.motor_level_dic[motor].append(i)
        print("Bag_Folder::make_motor_level_dic, done.")
        time.sleep(2)



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



    def get_random_steer_equal_weighting(self):
        indx = -99
        while True:
            if 'caffe' in self.path:
                steer = np.random.randint(1,99) # to compensate for a problem with human-caffe interaction
            else:
                steer = np.random.randint(0,100)

            if steer in self.steer_angle_dic:
                indx = random.choice(self.steer_angle_dic[steer])
                break
        assert(indx >= 0)
        return indx,steer

    def get_random_motor_equal_weighting(self):
        #print("Bag_Folder::get_random_motor_equal_weighting")
        if len(self.motor_level_dic) == 0:
            self.make_motor_level_dic() 
        indx = -99
        while True:
            motor = np.random.randint(51,100)
            if motor in self.motor_level_dic:
                indx = random.choice(self.motor_level_dic[motor])
                break
        assert(indx >= 0)
        return indx,motor




    def get_data(self,topics=['state','steer','motor'],num_topic_steps=10,num_image_steps=2,good_start_index=0):

        timestamp = self.data['good_start_timestamps'][good_start_index]
                
        raw_start_index = self.good_timestamps_to_raw_timestamps_indicies__dic[timestamp]

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
        return data_dic





def make_loss_indicies_dic(self):
    global good_start_timestamp_indicies_test_results
    self.data['loss_indicies_dic'] = {}
    a = good_start_timestamp_indicies_test_results[self.path]
    l = a['loss']
    l = np.array(l)
    l[l<0] = 0
    for i in range(len(l)):
        m = l[i]
        m *= 100
        m = to_range(m,0,60)
        m = int(m)
        if not m in self.data['loss_indicies_dic']:
            self.data['loss_indicies_dic'][m] = []
        self.data['loss_indicies_dic'][m].append(i)




def get_random_turn_with_high_loss_equal_weighting(self):
    if 'loss_indicies_dic' not in self.data:
        self.data['loss_indicies_dic'] = {}
    if len(self.data['loss_indicies_dic']) == 0:
        make_loss_indicies_dic(self) 
    j = -99
    ctr = 0
    while True:
        i = np.random.randint(23,61)
        if i in self.data['loss_indicies_dic']:
            j = random.choice(self.data['loss_indicies_dic'][i])
            good_timestamp = self.data['good_start_timestamps'][j]
            raw_index = self.good_timestamps_to_raw_timestamps_indicies__dic[good_timestamp]
            s = self.data['steer'][raw_index]
            if in_range(s,49-9,49+9):
                continue
            if 'caffe' in self.path:
                if not in_range(s,1,98):
                    continue
            break
        ctr += 1
        if ctr > 1000:
            print self.path
            assert(ctr<1000)
    assert(j >= 0)
    return j,s


"""
loss_level = []
steer = []
for i in range(15,61):
    if i in BF.data['loss_indicies_dic']:
        for j in BF.data['loss_indicies_dic'][i]:
            
            good_timestamp = BF.data['good_start_timestamps'][j]
            raw_index = BF.good_timestamps_to_raw_timestamps_indicies__dic[good_timestamp]
            s = BF.data['steer'][raw_index]
            if 'caffe' in BF.path:
                if not in_range(s,1,98):
                    continue
                if not in_range(s,49-9,49+9):
                    loss_level.append(i)
                    if s < 49:
                        s = 49 + 49-s
                    steer.append(s)
plt.plot(steer,loss_level,'o')
"""







class Bair_Car_Data_temp:
    """ """
    def __init__(self, path, to_ignore=[], NUM_STATE_ONE_STEPS=10):
        self.bag_folders_with_loaded_images = {}
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
        for b in bag_folder_paths_dic.keys():
            if bag_folder_paths_dic[b]:
                temp.append(b)
        bag_folder_paths = temp
        self.bag_folders_weighted = []
        train_preprocessed_bag_folder_path = opjD('train_preprocessed_bag_folder_path')
        if True:#try:
            unix('mkdir -p '+train_preprocessed_bag_folder_path)
            for f in bag_folder_paths:
                n = len(gg(opj(f,'.preprocessed','*.bag.pkl')))
                m = len(gg(opj(f,'.preprocessed','left*')))
                if len(gg(opj(train_preprocessed_bag_folder_path,f.split('/')[-1]+'.pkl'))) == 1:
                    #self.bag_folders_dic[f] = load_obj(opj(train_preprocessed_bag_folder_path,f.split('/')[-1]+'.pkl'))
                    print "could have loaded "+opj(train_preprocessed_bag_folder_path,f.split('/')[-1]+'.pkl')
                else:
                    if n > 0 and m > 0:
                        self.bag_folders_dic[f] = Bag_Folder(f,NUM_STATE_ONE_STEPS)
                        bpath = opj(train_preprocessed_bag_folder_path,self.bag_folders_dic[f].path.split('/')[-1]+'.pkl')
                        if len(gg(bpath)) == 0:
                            print("saveing "+bpath)
                            save_obj(self.bag_folders_dic[f],bpath)
                            self.bag_folders_dic[f] = []
                self.bag_folders_with_loaded_images[f] = True
                for i in range(max(n/10,1)):
                    self.bag_folders_weighted.append(f)
        if False: #except Exception as e:
            cprint("Bair_Car_Data::__init__ ********** Exception ******* with "+f,'red')
            print e.message, e.args


def total_num_loaded_bag_files(BCD):
    ctr = 0
    for k in BCD.bag_folders_dic:
        bf = BCD.bag_folders_dic[k]
        ctr += len(bf.files)
    return ctr




class Bair_Car_Data:
    """ """
    def __init__(self, path, to_ignore=[], NUM_STATE_ONE_STEPS=10):
        #self.bag_folders_with_loaded_images = {}
        self.bag_folders_dic = {}
        self.NUM_STATE_ONE_STEPS = NUM_STATE_ONE_STEPS
        bag_folder_paths = sorted(glob.glob(opj(path,'*')))
        bag_folder_paths_dic = {}
        for b in bag_folder_paths:
            bag_folder_paths_dic[b] = True
            for ig in to_ignore:
                if ig in b:
                    bag_folder_paths_dic[b] = False
                    print "Not using " + b.split('/')[-1]
        temp = []
        for b in bag_folder_paths_dic.keys():
            if bag_folder_paths_dic[b]:
                temp.append(b)
        self.bag_folder_paths = temp

    def load_bag_folders(self,train_preprocessed_only=True,num_to_load=4):
        cprint("Bair_Car_Data::load_bag_folders",'red','on_yellow')
        self.bag_folders_weighted = []
        #m=memory()
        #free_propotion = m['free']/(1.0*m['total'])
        #if free_propotion < 0.20:
        if total_num_loaded_bag_files(self) < 3400:
            fs = self.bag_folders_dic.keys()
            if not fs == None:
                random.shuffle(fs)
                for i in range(len(fs)/6):
                    cprint("Bair_Car_Data::load_bag_folders, unloading "+fn(fs[i]),'red','on_blue')
                    del self.bag_folders_dic[fs[i]]
        train_preprocessed_bag_folder_path = opjD('train_preprocessed_bag_folder_path')
        ctr = 0
        if True:#try:
            unix('mkdir -p '+train_preprocessed_bag_folder_path)
            random.shuffle(self.bag_folder_paths)
            for f in self.bag_folder_paths:               
                if f not in self.bag_folders_dic.keys():
                    if total_num_loaded_bag_files(self) > 3400:
                        break

                    if train_preprocessed_only and len(gg(opj(train_preprocessed_bag_folder_path,f.split('/')[-1]+'.pkl'))) == 1:
                        self.bag_folders_dic[f] = load_obj(opj(train_preprocessed_bag_folder_path,f.split('/')[-1]+'.pkl'))
                        print "loaded "+opj(train_preprocessed_bag_folder_path,f.split('/')[-1]+'.pkl')
                    elif not train_preprocessed_only:
                        if n > 0 and m > 0:
                            self.bag_folders_dic[f] = Bag_Folder(f,self.NUM_STATE_ONE_STEPS)
                            bpath = opj(train_preprocessed_bag_folder_path,self.bag_folders_dic[f].path.split('/')[-1]+'.pkl')
                            if len(gg(bpath)) == 0:
                                print("saveing "+bpath)
                                save_obj(self.bag_folders_dic[f],bpath)
                    else:
                        continue
                    ctr += 1
                    if ctr >= num_to_load:
                        break
                #self.bag_folders_with_loaded_images[f] = True
            for f in self.bag_folders_dic.keys():
                n = len(gg(opj(f,'.preprocessed','*.bag.pkl')))
                m = len(gg(opj(f,'.preprocessed','left*'))) 
                for i in range(max(n/10,1)):
                    self.bag_folders_weighted.append(f)

        if False: #except Exception as e:
            cprint("Bair_Car_Data::__init__ ********** Exception ******* with "+f,'red')
            print e.message, e.args
        cprint("Here are the loaded bag files:",'red','on_white')
        pprint(self.bag_folders_dic.keys())



def load_bag_folders(self,train_preprocessed_only=True,num_to_load=4):
    cprint("load_bag_folders",'red','on_yellow')
    self.bag_folders_weighted = []

    while True:
        total_num_bag_files = 0
        fs = self.bag_folders_dic.keys()
        for bf in fs:
            BF = self.bag_folders_dic[bf]
            total_num_bag_files += len(BF.files)
        if total_num_bag_files > 3200:
            f = fs[np.random.randint(len(fs))]
            print("load_bag_folders, unloading "+f)
            del self.bag_folders_dic[f]
        else:
            break

    train_preprocessed_bag_folder_path = opjD('train_preprocessed_bag_folder_path')
    ctr = 0
    if True:#try:
        unix('mkdir -p '+train_preprocessed_bag_folder_path)
        random.shuffle(self.bag_folder_paths)
        for f in self.bag_folder_paths:               
            if f not in self.bag_folders_dic.keys():
                total_num_bag_files = 0
                fs = self.bag_folders_dic.keys()
                for bf in fs:
                    BF = self.bag_folders_dic[bf]
                    total_num_bag_files += len(BF.files)
                if total_num_bag_files > 3600:
                    break

                if train_preprocessed_only and len(gg(opj(train_preprocessed_bag_folder_path,f.split('/')[-1]+'.pkl'))) == 1:
                    self.bag_folders_dic[f] = load_obj(opj(train_preprocessed_bag_folder_path,f.split('/')[-1]+'.pkl'))
                    print "loaded "+opj(train_preprocessed_bag_folder_path,f.split('/')[-1]+'.pkl')
                elif not train_preprocessed_only:
                    if n > 0 and m > 0:
                        self.bag_folders_dic[f] = Bag_Folder(f,self.NUM_STATE_ONE_STEPS)
                        bpath = opj(train_preprocessed_bag_folder_path,self.bag_folders_dic[f].path.split('/')[-1]+'.pkl')
                        if len(gg(bpath)) == 0:
                            print("saveing "+bpath)
                            save_obj(self.bag_folders_dic[f],bpath)
                else:
                    continue
                ctr += 1
                if ctr >= num_to_load:
                    break
            #self.bag_folders_with_loaded_images[f] = True
        for f in self.bag_folders_dic.keys():
            n = len(gg(opj(f,'.preprocessed','*.bag.pkl')))
            m = len(gg(opj(f,'.preprocessed','left*'))) 
            for i in range(max(n/10,1)):
                self.bag_folders_weighted.append(f)

    if False: #except Exception as e:
        cprint("Bair_Car_Data::__init__ ********** Exception ******* with "+f,'red')
        print e.message, e.args







def show_data_dic(d):
    caffe_steer_color_color = [255,0,0]
    human_steer_color_color = [0,0,255]
    
    time0 = time.time()
    t0 = 0
    dt = 0
    for i in range(len(d['left'])):
        #print i
        if i > 0:
            img_prev = img.copy()
        img = np.zeros((shape(d['right'][0])[0],shape(d['right'][0])[1],3),'uint8')
        dt = d['timestamp'][i] - t0
        #mi(d['left'][1],3,[1,2,2])
        #mi(d['right'][1],3,[1,2,1],do_clf=False)
        #plt.pause(0.0001)
        img[:,:,0] = d['right'][i].copy()
        img[:,:,1] = d['right'][i].copy()
        img[:,:,2] = d['right'][i].copy()

        if np.int(d['state'][i]) in [3,6]: #caffe is steering
            steer_rect_color = caffe_steer_color_color
        else:
            steer_rect_color = human_steer_color_color
        apply_rect_to_img(img,d['steer'][i],0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=True)
        if False:
            apply_rect_to_img(img,d['acc_x'][i],-8,8,steer_rect_color,steer_rect_color,0.78,0.05,center=True,reverse=False,horizontal=True)
            apply_rect_to_img(img,d['gyro_x'][i],-60,60,steer_rect_color,steer_rect_color,0.75,0.05,center=True,reverse=False,horizontal=True)        
            
            apply_rect_to_img(img,d['motor'][i],49,99,steer_rect_color,steer_rect_color,0.8,0.05,center=False,reverse=True,horizontal=False)
            apply_rect_to_img(img,d['encoder'][i],0,15,steer_rect_color,steer_rect_color,0.78,0.05,center=False,reverse=True,horizontal=False)

            apply_rect_to_img(img,d['gyro_y'][i],-240,240,steer_rect_color,steer_rect_color,0.2,0.05,center=True,reverse=False,horizontal=False)
            apply_rect_to_img(img,d['acc_y'][i],-48,48,steer_rect_color,steer_rect_color,0.18,0.05,center=True,reverse=False,horizontal=False)
            apply_rect_to_img(img,d['gyro_z'][i],-480,480,steer_rect_color,steer_rect_color,0.16,0.05,center=True,reverse=False,horizontal=False)
            apply_rect_to_img(img,d['acc_z'][i],-135,160,steer_rect_color,steer_rect_color,0.14,0.05,center=True,reverse=False,horizontal=False)
            apply_rect_to_img(img,d['gyro_z'][i],-280*2,280*2,steer_rect_color,steer_rect_color,0.12,0.05,center=True,reverse=True,horizontal=False)
        if False: #dt > 0.06 and i > 0:
            #img_prev[:,:,1] = img_prev[:,:,1] / 2
            #img_prev[:,:,2] = img_prev[:,:,2] / 2
            pz = min(dt,1.0)
            mi(img_prev,do_clf=True) #img_title=(d2s('dt = ', int(1000*dt),'ms')),
            plt.pause(pz)
        pz = 0.0001
        while ( time.time()-time0 + d['timestamp'][0]) - d['timestamp'][i] < 0.03:
            #print ( time.time()-time0 + d['timestamp'][0]) - d['timestamp'][i]
            time.sleep(0.001)
        if ( time.time()-time0 + d['timestamp'][0]) - d['timestamp'][i] > 0:
            cv2.imshow('left',imresize(cv2.cvtColor(img,cv2.COLOR_RGB2BGR),4.).astype('uint8'))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return
        else:
            print "skipped frame"

        t0 = d['timestamp'][i]
        #plt.pause(pz)



def show_data_dic_sequence(BF,N,start_indx):
    for i in range(0,len(BF.data['good_start_timestamps']),N):
        d = BF.get_data(topics=['state','steer','motor'],num_topic_steps=N,num_image_steps=N,good_start_index=start_indx+i)
        show_data_dic(d)
  


def make_contact_prints():
    unix('mkdir -p '+opjD('bair_car_data_contact_sheets'))
    files = gg(opjD('train_preprocessed_bag_folder_path','*.pkl'))
    for f in files:
        print f
        BF = load_obj(f)
        cs = BF.make_contact_print()
        imsave(opjD('bair_car_data_contact_sheets',f.split('/')[-1]+'.png'),cs)

