#hdf5_segment_metadata_path = '/home/karlzipser/Desktop/bair_car_data_new_28April2017/hdf5/segment_metadata'
#Segment_Data.load_Segment_Data(hdf5_segment_metadata_path,hdf5_runs_path)
GPU = 1
BATCH_SIZE = 100
DISPLAY = True
VERBOSE = True
LOAD_ARUCO = False
#BAIR_CAR_DATA_PATH = opjD('bair_car_data_Main_Dataset') #opjD('bair_car_data_new_28April2017')
BAIR_CAR_DATA_PATH = opjD('bair_car_data_new_28April2017')
RESUME = True
if RESUME:
    weights_file_path = most_recent_file_in_folder(opjD(),['save_file_LCR'],['infer'])
IGNORE = ['reject_run','left','out1_in2']#,'Smyth','racing','local','Tilden','campus']
REQUIRE_ONE = []
USE_STATES = [1,3,5,6,7]
print_stars0();pd2s('USE_STATES =',USE_STATES);print_stars1()
N_FRAMES = 2
N_STEPS = 10
STRIDE = 3 # multiply by N Steps in order to have fixed number of steps reach further in time.
# STRIDE is not fully controlled here, there must be changes in _data_into_batch().
save_net_timer = Timer(60*30)
print_timer = Timer(15)
epoch_timer = Timer(15)
#save_file_name = 'save_file_LCR_'
save_file_name = 'save_file_'
import kzpy3.teg9.data.utils.Segment_Data as Segment_Data



hdf5_runs_path = opj(BAIR_CAR_DATA_PATH,'hdf5/runs')
hdf5_segment_metadata_path = opj(BAIR_CAR_DATA_PATH,'hdf5/segment_metadata')
Segment_Data.load_Segment_Data(hdf5_segment_metadata_path,hdf5_runs_path)



def _check(d):
    a = d['all_steer']
    True
    b = []
    ctr = 0
    for e in a:
        run_code = e[3]
        seg_num = e[0]
        offset = e[1]
        r = Segment_Data.get_data(run_code,seg_num,offset,3*N_STEPS,offset+0,N_FRAMES,ignore=IGNORE,require_one=REQUIRE_ONE,use_states=USE_STATES,no_images=True)
        if r != None:
            b.append(e)
        if np.mod(ctr,1000) == 0:
            print ctr
        ctr += 1
        #if ctr > 1000:
        #    break
    return b

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
if True:
    figure(1,figsize=(2,1))
    histogram_plot_there = True
    clf()
    plt.hist(array(low_steer)[:,2],bins=range(0,100))
    plt.hist(array(high_steer)[:,2],bins=range(0,100))
    pause(0.001)
    #figure(1)
all_steer = low_steer + high_steer
all_steer = _check({'all_steer':all_steer})
random.shuffle(all_steer)
train_all_steer = all_steer[:int(0.95*len(all_steer))]
val_all_steer = all_steer[int(0.95*len(all_steer)):]
so(val_all_steer,'/home/karlzipser/Desktop/bair_car_data_new_28April2017/val_all_steer')
so(train_all_steer,'/home/karlzipser/Desktop/bair_car_data_new_28April2017/train_all_steer')

o=lo('/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo/Aruco_Steering_Trajectories/Mr_Black_2017-09-03-15-46-34.pkl' )
a=o['Follow_Arena_Potential_Field'][1].keys()
segs = {}
ctr = 0
segs[str(ctr)] = {}
segs[str(ctr)]['left_timestamp'] = []
for i in range(0,len(a)-1):
	if a[i+1]-a[i]<0.1:
		segs[str(ctr)]['left_timestamp'].append(a[i])
	else:
		ctr += 1
		segs[str(ctr)] = {}
		segs[str(ctr)]['left_timestamp'] = []




