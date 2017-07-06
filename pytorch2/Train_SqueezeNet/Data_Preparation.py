from kzpy3.utils2 import *
cprint('****************** '+__file__+' ******************','yellow')
pythonpaths(['kzpy3','kzpy3/teg9','kzpy3/pytorch2/Train_SqueezeNet'])
from kzpy3.vis import *
import Parameters as P
import data.utils.Segment_Data as Segment_Data


translation_dic = {'a':'apples','b':'build','c':'cats','d':'dogs'}
if __name__ == "__main__" and '__file__' in vars():
    argument_dictionary = args_to_dic({  'pargs':sys.argv[1:]  })
else:
    print('Running this within interactive python.')
    argument_dictionary = args_to_dic({  'pargs':"-a -1 -b 4 -c [1,2,9] -d {1:5,2:4}"  })
argument_dictionary = translate_args(
    {'argument_dictionary':argument_dictionary,
    'translation_dic':translation_dic})
print(argument_dictionary)

hdf5_runs_path = opj(P.BAIR_CAR_DATA_PATH,'hdf5/runs')
hdf5_segment_metadata_path = opj(P.BAIR_CAR_DATA_PATH,'hdf5/segment_metadata')
Segment_Data.load_Segment_Data(hdf5_segment_metadata_path,hdf5_runs_path)
        
def Data():
    D = {}
    #D[''] = d['']
    True
    D['type'] = 'Training_Data'
    D['Purpose'] = d2s(inspect.stack()[0][3],':','Object to hold various data and information for training')
    D['train_los_dic'] = {}
    def _check(d):
        a = d['all_steer']
        True
        b = []
        ctr = 0
        for e in a:
            run_code = e[3]
            seg_num = e[0]
            offset = e[1]
            r = Segment_Data.get_data(run_code,seg_num,offset,3*P.N_STEPS,offset+0,P.N_FRAMES,ignore=P.IGNORE,require_one=P.REQUIRE_ONE,use_states=P.USE_STATES,no_images=True)
            if r != None:
                b.append(e)
            if np.mod(ctr,1000) == 0:
                print ctr
            ctr += 1
            #if ctr > 1000:
            #    break
        return b
    def _get_all_steer():

        print('\nloading low_steer... (takes awhile)')
        low_steer = load_obj(opj(hdf5_segment_metadata_path,'low_steer'))
        random.shuffle(low_steer)
        print('\nloading high_steer... (takes awhile)')
        high_steer = load_obj(opj(hdf5_segment_metadata_path,'high_steer'))
        random.shuffle(high_steer)
        print('done')
        len_high_steer = len(high_steer)
        len_low_steer = len(low_steer)
        ctr_low = -1
        ctr_high = -1
        if P.DISPLAY:
            figure(P.HIGH_LOW_HISTOGRAM_FIGURE_NAME,figsize=(2,1))
            histogram_plot_there = True
            clf()
            plt.hist(array(low_steer)[:,2],bins=range(0,100))
            plt.hist(array(high_steer)[:,2],bins=range(0,100))
            pause(0.001)
            #figure(1)
        all_steer = low_steer + high_steer
        all_steer = _check({'all_steer':all_steer})
        random.shuffle(all_steer)
        #train_len = int(len(all_steer)*0.9)
        #D['train_steer'] = all_steer[:train_len]
        #D['validate_steer'] = all_steer[train_len:]
        D['all_steer'] = all_steer
    D['get_all_steer'] = _get_all_steer

    def _get_data(d):
        run_code = d['run_code']
        seg_num = d['seg_num']
        offset = d['offset']       
        data = Segment_Data.get_data(run_code,seg_num,offset,3*P.N_STEPS,offset+0,P.N_FRAMES,ignore=P.IGNORE,require_one=P.REQUIRE_ONE,use_states=P.USE_STATES)
        return data
    D['get_data'] = _get_data



    def _get_data_considering_high_low_steer(d):
        global ctr_low
        global ctr_high
        global low_steer
        global high_steer
        
        if ctr_low >= len_low_steer:
            ctr_low = -1
        if ctr_high >= len_high_steer:
            ctr_high = -1
        if ctr_low == -1:
            random.shuffle(low_steer)
            ctr_low = 0
        if ctr_high == -1:
            random.shuffle(high_steer)
            ctr_high = 0
        if random.random() < 0.5:
            choice = low_steer[ctr_low]
            ctr_low += 1
        else:
            choice = high_steer[ctr_high]
            ctr_high += 1

        run_code = choice[3]
        seg_num = choice[0]
        offset = choice[1]

        data = Segment_Data.get_data(run_code,seg_num,offset,3*N_STEPS,offset+0,N_FRAMES,ignore=ignore,require_one=require_one,use_states=use_states)

        return data
    D['get_data_considering_high_low_steer'] = _get_data_considering_high_low_steer



    def _get_data_considering_high_low_steer_and_valid_trajectory_timestamp(d):
        True
        global ctr_low
        global ctr_high
        global low_steer
        global high_steer
        global counts
        global high_loss_key_ctr
        global high_loss_keys

        if ctr_low >= len_low_steer:
            ctr_low = -1
        if ctr_high >= len_high_steer:
            ctr_high = -1
        if ctr_low == -1:
            random.shuffle(low_steer)
            ctr_low = 0
        if ctr_high == -1:
            random.shuffle(high_steer)
            ctr_high = 0
            
        if random.random() < 0.5:
            choice = low_steer[ctr_low]
            ctr_low += 1
        else:
            choice = high_steer[ctr_high]
            ctr_high += 1
        run_code = choice[3]
        seg_num = choice[0]
        offset = choice[1]

        run_name = Segment_Data.Segment_Data['run_codes'][run_code]

        if run_name not in Aruco_Steering_Trajectories.keys():
            #print('Run name '+run_name+' not in Aruco_Steering_Trajectories')
            return None
        if len(Aruco_Steering_Trajectories[run_name].keys()) < 2:
            #print('len(Aruco_Steering_Trajectories[run_name].keys()) <= 2')
            return None

        seg_num_str = str(seg_num)
        aruco_matches = []

        for i in [0]:#range(N_FRAMES):
            timestamp = Segment_Data.Segment_Data['runs'][run_name]['segments'][seg_num_str]['left_timestamp'][offset+i]
            behavioral_mode = np.random.choice(
                ['Direct_Arena_Potential_Field',
                #'Furtive_Arena_Potential_Field',
                'Follow_Arena_Potential_Field'])
                #'Play_Arena_Potential_Field'])
            desired_direction = np.random.choice([0,1])

            if timestamp in Aruco_Steering_Trajectories[run_name][behavioral_mode][desired_direction].keys():
                aruco_matches.append(timestamp)
            if len(aruco_matches) < 1:
                return None
        data = Segment_Data.get_data(run_code,seg_num,offset,N_STEPS,offset+0,N_FRAMES,ignore=ignore,require_one=require_one)
        if data != None:
            data['behavioral_mode'] = behavioral_mode
            data['desired_direction'] = desired_direction
            for topic in Aruco_Steering_Trajectories[run_name][behavioral_mode][desired_direction][timestamp]:
                data[topic] = Aruco_Steering_Trajectories[run_name][behavioral_mode][desired_direction][timestamp][topic]
            data['id'] = (run_name,behavioral_mode,desired_direction,timestamp,run_code,seg_num,offset)
        if P.other_cars_only and np.random.random() < 0.85: 
            if data == None:
                return None
            if data['other_car_inverse_distances'] == None:
                return None
            if len(data['other_car_inverse_distances']) == 0:
                return None
        return data
    D['get_data_considering_high_low_steer_and_valid_trajectory_timestamp'] = _get_data_considering_high_low_steer_and_valid_trajectory_timestamp


    def _prepare_Aruco_trajectory_data():
        CS_('load aruco trajectory data')
        Aruco_Steering_Trajectories = {}
        aruco_data_location = opjD('output_data')
        paths = sggo(aruco_data_location,'*.pkl')
        for i in range(len(paths)):
            o = paths[i]
            ast = lo(o)
            for run_name in ast.keys(): 
                print(d2n(run_name,' (',i+1,' of ',len(paths),')'))
                if run_name not in Aruco_Steering_Trajectories:
                    Aruco_Steering_Trajectories[run_name] = {}
                if len(ast[run_name].keys()) > 4:
                    print_stars()
                    continue
                for mode in ast[run_name].keys():
                    print('\t'+mode)
                    if mode not in Aruco_Steering_Trajectories[run_name]:
                        Aruco_Steering_Trajectories[run_name][mode] = {}
                    timestamps = ast[run_name][mode]['near_t']
                    dd = ast[run_name][mode]['desired_direction'][0]
                    print('\t\t'+str(dd))
                    Aruco_Steering_Trajectories[run_name][mode][dd] = {}
                    for i in range(len(timestamps)):
                        t = timestamps[i]
                        Aruco_Steering_Trajectories[run_name][mode][dd][t] = {}
                        for topic in ast[run_name][mode].keys():
                            if topic not in ['near_t','desired_direction']:
                                q = ast[run_name][mode][topic][i]
                                if not(is_number(q)):
                                    q = array(q)
                                    q = q.astype(np.float16)
                                else:
                                    q = np.float16(q)
                                Aruco_Steering_Trajectories[run_name][mode][dd][t][topic] = q
        ctr = 0
        for run_name in Aruco_Steering_Trajectories.keys():
            if 'flip_' in run_name:
                del Aruco_Steering_Trajectories[run_name]
                continue
            flip = 'flip_'+run_name
            print(d2n(flip,' (',ctr+1,' of ',len(paths),')'))
            ctr += 1
            Aruco_Steering_Trajectories[flip]= {}
            for mode in Aruco_Steering_Trajectories[run_name]:
                Aruco_Steering_Trajectories[flip][mode] = {}
                for dd in [0,1]:
                    Aruco_Steering_Trajectories[flip][mode][dd] = {}
                    for t in Aruco_Steering_Trajectories[run_name][mode][dd].keys():
                        Aruco_Steering_Trajectories[flip][mode][dd][t] = {}
                        Aruco_Steering_Trajectories[flip][mode][dd][t]['steer'] = np.float16(99-Aruco_Steering_Trajectories[run_name][mode][dd][t]['steer'])
                        Aruco_Steering_Trajectories[flip][mode][dd][t]['velocity'] = np.float16(Aruco_Steering_Trajectories[run_name][mode][dd][t]['velocity'])
                        l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['other_car_inverse_distances'])
                        l.reverse(); l = array(l); l = l.astype(np.float16)
                        Aruco_Steering_Trajectories[flip][mode][dd][t]['other_car_inverse_distances'] = l
                        l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['marker_inverse_distances'])
                        l.reverse(); l = array(l); l = l.astype(np.float16)
                        Aruco_Steering_Trajectories[flip][mode][dd][t]['marker_inverse_distances'] = l
                        l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['potential_values'])
                        l.reverse(); l = array(l); l = l.astype(np.float16)
                        Aruco_Steering_Trajectories[flip][mode][dd][t]['potential_values'] = l

                        l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['clock_potential_values'])
                        l.reverse(); l = array(l); l = l.astype(np.float16)
                        Aruco_Steering_Trajectories[flip][mode][dd][t]['clock_potential_values'] = l

                        if dd == 0:
                            Aruco_Steering_Trajectories[flip][mode][dd][t]['desired_direction'] = 1
                        else:
                            Aruco_Steering_Trajectories[flip][mode][dd][t]['desired_direction'] = 0
                        Aruco_Steering_Trajectories[flip][mode][dd][t]['relative_heading'] =  np.float16(360 - Aruco_Steering_Trajectories[run_name][mode][dd][t]['relative_heading'])

        unix('mkdir -p '+opjD('Aruco_Steering_Trajectories'))
        ctr = 0
        for run_name in sorted(Aruco_Steering_Trajectories.keys()):
            print(d2n(run_name,' (',ctr+1,' of ',len(paths),')'))
            so(Aruco_Steering_Trajectories[run_name],opjD('Aruco_Steering_Trajectories',run_name))
            ctr += 1
        raw_input('enter')
    D['prepare_Aruco_trajectory_data'] = _prepare_Aruco_trajectory_data



    def _load_Aruco_Steering_Trajectories():
        print("Loading Aruco_Steering_Trajectories . . .")
        paths = sggo(opjD('Aruco_Steering_Trajectories','*.pkl'))
        Aruco_Steering_Trajectories = {}
        ctr = 0
        for p in paths:
            o = lo(p)
            run_name = fname(p).replace('.pkl','')
            print(d2n(run_name,' (',ctr+1,' of ',len(paths),')'))
            Aruco_Steering_Trajectories[run_name] = o
            ctr += 1
        D['Aruco_Steering_Trajectories'] = Aruco_Steering_Trajectories
    D['load_Aruco_Steering_Trajectories'] = _load_Aruco_Steering_Trajectories

    return D


if True:
    all_steer = lo(opjD('all_steer'))


if True:
    segments = {}
    for e in all_steer:
        run_code = e[3]
        seg_num = e[0]
        offset = e[1]
        seg = (run_code,seg_num)
        if seg not in segments:
            segments[seg] = []
        segments[seg].append(e)

if True:
    segsk = segments.keys()
    random.shuffle(segsk)
    validation_proportion = 0.1
    val_len = int(validation_proportion * len(segsk))
    val_segsk = segsk[:val_len]
    train_segsk = segsk[val_len:]

if True:
    train_all_steer = []
    val_all_steer = []
    for segsk in train_segsk:
        train_all_steer += segments[segsk]
    for segsk in val_segsk:
        val_all_steer += segments[segsk]

if True:
    so(train_all_steer,opjD('train_all_steer'))
    so(val_all_steer,opjD('val_all_steer'))

"""
if True:
    runs_segs = {}
    for e in all_steer:
        run_code = e[3]
        seg_num = e[0]
        offset = e[1]
        if run_code not in runs_segs:
            runs_segs[run_code] = {}
        if seg_num not in runs_segs[run_code]:
            runs_segs[run_code][seg_num] = {}
            runs_segs[run_code][seg_num]['len'] = 0
        if offset > runs_segs[run_code][seg_num]['len']:
            runs_segs[run_code][seg_num]['len'] = offset
    ctr = 0
    ctr_plus_10 = 0
    for run_code in sorted(runs_segs.keys()):
        for seg_num in sorted(runs_segs[run_code].keys()):
            ctr += runs_segs[run_code][seg_num]['len']
            ctr_plus_10 += runs_segs[run_code][seg_num]['len'] + 10
            runs_segs[run_code][seg_num]['cumulative'] = ctr
            runs_segs[run_code][seg_num]['cumulative_plus_ten'] = ctr_plus_10



if True:
    data = {}
    validation_proportion = 0.1
    for d in ['train','val']:
        data[d] = {}
    for run_code in sorted(runs_segs.keys()):
        for d in ['train','val']:    
            data[d][run_code] = {}
        segs = runs_segs[run_code].keys()
        random.shuffle(segs)
        val_len = int(validation_proportion * len(segs))
        val_segs = segs[:val_len]
        train_segs = segs[val_len:]
        for i in range(len(val_segs)):
            data['val'][run_code][val_segs[i]] = runs_segs[run_code][val_segs[i]]
        for i in range(len(train_segs)):
            data['train'][run_code][train_segs[i]] = runs_segs[run_code][train_segs[i]]


    out = {}
    for mode in ['train','val']:
        points = []
        for run_code in data[mode].keys():
            for seg_num in data[mode][run_code].keys():
                for p in data[run_code][seg_num]:
                    points.append(data[mode][run_code][seg_num])
        out[mode] = points
            
if True:
    WIDTH = 3666
    all_steer_img = np.zeros((WIDTH,WIDTH,3),np.uint8)

    def timepoint_to_all_steer_img(d):
        run_code = d['run_code']
        seg_num = d['seg_num']
        offset = d['offset']
        runs_segs = d['runs_segs']
        True
        cumulative_plus_ten = runs_segs[run_code][seg_num]['cumulative_plus_ten']
        position = cumulative_plus_ten - 10 - runs_segs[run_code][seg_num]['len'] + offset
        y = int(position/WIDTH)
        x = np.mod(position,WIDTH)
        return x,y

    mi_timer = Timer(0.1)
    c = 0
    for runs_segs in [ data['val'],data['train']]:
        for run_code in sorted(runs_segs.keys()):
            for seg_num in sorted(runs_segs[run_code].keys()):
                for offset in range(runs_segs[run_code][seg_num]['len']):
                    x,y = timepoint_to_all_steer_img(
                        {'run_code':run_code,
                        'seg_num':seg_num,
                        'offset':offset,
                        'runs_segs':runs_segs})
                    all_steer_img[y,x,c] = int(127+128*offset/(1.0*runs_segs[run_code][seg_num]['len']))
                    if mi_timer.check():
                        mi(all_steer_img)
                        pause(0.001)
                        mi_timer.reset()
        c += 1
"""



#EOF