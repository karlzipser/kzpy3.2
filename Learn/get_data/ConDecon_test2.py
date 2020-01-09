from kzpy3.vis3 import *
exec(identify_file_str)

# python kzpy3/drafts/Sq7/main.py --RESUME 1 --NET_TYPE ConDecon_test2 --NET_TYPE_SUFFIX 84x47

X = {'data_tracker':{}}

WIDTH,HEIGHT = 41,23
#WIDTH,HEIGHT = 168,94
WIDTH,HEIGHT = 168/2,94/2


if False:
    a = sggo(opjD('Data/Network_Predictions_projected/*.h5py'))
    train_runs,val_runs = [],[]
    for r in a:
        train_runs.append(fname(r).replace('.net_projections.h5py',''))
    random.shuffle(train_runs)
    for i in range(int(0.1*len(train_runs))):
        val_runs.append(train_runs.pop())



val_runs = [
    'tegra-ubuntu_16Nov18_15h59m28s',
    'tegra-ubuntu_01Nov18_13h46m55s',
    'Mr_Black_24Sep18_18h52m26s',
    'tegra-ubuntu_07Oct18_18h24m28s',
    'tegra-ubuntu_17Oct18_12h11m22s',
    'tegra-ubuntu_12Oct18_11h11m30s',
    'tegra-ubuntu_25Oct18_10h21m55s',
    'tegra-ubuntu_12Nov18_20h56m16s',
    'tegra-ubuntu_25Oct18_15h43m36s',
]


train_runs = [
    'Mr_Black_18Sep18_18h06m34s',
    'tegra-ubuntu_16Oct18_11h24m21s',
    'tegra-ubuntu_26Oct18_09h14m36s',
    'Mr_Black_26Jul18_20h03m31s',
    'tegra-ubuntu_08Oct18_19h15m18s',
    'tegra-ubuntu_15Nov18_20h51m52s',
    'tegra-ubuntu_24Oct18_16h38m19s',
    'tegra-ubuntu_31Oct18_16h06m32s',
    'tegra-ubuntu_22Oct18_15h11m34s',
    'tegra-ubuntu_29Oct18_13h28m05s',
    'tegra-ubuntu_01Nov18_16h25m40s',
    'tegra-ubuntu_21Oct18_17h22m36s',
    'tegra-ubuntu_21Oct18_16h49m30s',
    'Mr_Black_08Sep18_16h11m59s',
    'tegra-ubuntu_02Nov18_17h09m48s',
    'tegra-ubuntu_29Oct18_14h05m23s',
    'tegra-ubuntu_02Nov18_10h06m03s',
    'tegra-ubuntu_16Oct18_17h02m43s',
    'tegra-ubuntu_18Oct18_08h14m24s_b',
    'tegra-ubuntu_26Oct18_08h37m07s',
    'tegra-ubuntu_17Oct18_12h46m32s',
    'Mr_Black_25Sep18_16h32m32s',
    'Mr_Black_28Sep18_13h55m17s',
    'Mr_Black_26Sep18_19h14m00s',
    'tegra-ubuntu_16Nov18_15h29m20s',
    'tegra-ubuntu_07Oct18_11h38m15s',
    'Mr_Black_30Sep18_18h34m01s',
    'tegra-ubuntu_19Oct18_11h33m22s',
    'Mr_Black_27Sep18_14h51m07s',
    'tegra-ubuntu_07Oct18_18h59m59s',
    'Mr_Black_04Oct18_18h16m14s',
    'Mr_Black_24Sep18_13h19m51s',
    'tegra-ubuntu_16Nov18_13h02m06s',
    'tegra-ubuntu_02Nov18_15h29m59s',
    'Mr_Black_21Sep18_18h42m46s',
    'tegra-ubuntu_15Nov18_20h55m02s',
    'Mr_Black_24Jul18_20h04m17s_local_lrc',
    'tegra-ubuntu_19Oct18_08h55m02s',
    'Mr_Black_03Oct18_11h27m02s',
    'Mr_Black_29Sep18_19h05m09s',
    'tegra-ubuntu_11Oct18_17h11m39s',
    'tegra-ubuntu_16Oct18_10h02m45s',
    'tegra-ubuntu_30Oct18_15h58m09s',
    'Mr_Black_08Sep18_16h57m06s',
    'Mr_Black_25Jul18_14h44m55s_local_lrc',
    'tegra-ubuntu_01Nov18_17h00m24s',
    'tegra-ubuntu_08Oct18_10h46m44s',
    'tegra-ubuntu_16Oct18_17h42m25s',
    'Mr_Black_25Jul18_14h29m56s_local_lrc',
    'tegra-ubuntu_01Nov18_13h09m32s',
    'tegra-ubuntu_22Oct18_15h48m48s',
    'tegra-ubuntu_18Oct18_16h15m46s',
    'tegra-ubuntu_31Oct18_16h47m50s',
    'tegra-ubuntu_18Oct18_17h10m29s',
    'tegra-ubuntu_19Oct18_12h22m42s',
    'tegra-ubuntu_15Nov18_20h53m56s',
    'tegra-ubuntu_28Oct18_17h27m55s',
    'Mr_Black_25Sep18_11h41m45s',
    'tegra-ubuntu_08Oct18_18h09m29s',
    'tegra-ubuntu_02Nov18_12h24m59s',
    'tegra-ubuntu_23Oct18_17h19m34s',
    'tegra-ubuntu_18Oct18_08h43m23s',
    'tegra-ubuntu_24Oct18_17h15m14s',
    'Mr_Black_25Jul18_19h55m13s',
    'Mr_Black_27Jul18_18h46m35s',
    'Mr_Black_03Oct18_19h11m35s',
    'tegra-ubuntu_25Oct18_16h17m55s',
    'tegra-ubuntu_29Oct18_17h22m22s',
    'Mr_Black_04Oct18_18h53m06s',
    'tegra-ubuntu_15Nov18_20h52m26s',
    'Mr_Black_27Jul18_17h55m00s',
    'Mr_Black_02Oct18_18h16m32s',
    'tegra-ubuntu_08Oct18_19h16m15s',
    'Mr_Black_05Oct18_17h18m02s_lost_IMU_early',
    'Mr_Black_01Oct18_18h58m41s',
    'tegra-ubuntu_16Oct18_09h27m05s',
    'tegra-ubuntu_19Oct18_11h46m46s',
    'tegra-ubuntu_15Oct18_18h47m18s',
    'tegra-ubuntu_02Nov18_16h04m58s',
    'Mr_Black_03Oct18_11h11m38s',
    'tegra-ubuntu_08Oct18_18h36m24s',
    'tegra-ubuntu_29Oct18_16h45m16s',
    'tegra-ubuntu_21Oct18_15h22m18s',
    'tegra-ubuntu_15Nov18_20h52m45s',
    'tegra-ubuntu_08Oct18_19h15m15s',
    'tegra-ubuntu_08Oct18_19h15m21s',
    'Mr_Black_29Jul18_18h56m59s',
]



Runs = {}

runs = train_runs
#runs = val_runs

Run_coder = {}

run_ctr = 0

good_list = []

for r in runs:

    Run_coder[run_ctr] = r

    H = find_files_recursively(opjD('Data'),r,DIRS_ONLY=True)

    Runs[r] = {
        'original_timestamp_data':{},
        'flip_images':{},
        'left_timestamp_metadata_right_ts':{},
        'net_projections':{},
    }


    Runs[r]['original_timestamp_data'] = \
        {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'original_timestamp_data.h5py'),'data':None}

    Runs[r]['flip_images'] = \
        {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'flip_images.h5py'),'data':None}

    Runs[r]['left_timestamp_metadata_right_ts'] = \
        {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'left_timestamp_metadata_right_ts.h5py'),'data':None}

    Runs[r]['net_projections'] = \
        {'path':opj(opjD('Data'),'Network_Predictions_projected',r+'.net_projections.h5py'),'data':None}

    Runs[r]['button_number'] = None
    Runs[r]['encoder'] = None



    for k in Runs[r].keys():
        if k not in ['button_number','encoder']:
            if Runs[r][k]['data'] == None:
                Runs[r][k]['data'] = h5r(Runs[r][k]['path'])
    for kk in ['button_number','encoder']:
        if Runs[r][kk] == None:
            Runs[r][kk] = Runs[r]['left_timestamp_metadata_right_ts']['data'][kk][:]

    length = len(Runs[r]['original_timestamp_data']['data']['left_image']['vals'])
    for i in range(length):
        if Runs[r]['button_number'][i] != 4 and Runs[r]['encoder'][i] > 0.1:
            good_list.append((run_ctr,i))

    run_ctr += 1   


#kprint(Runs)

###############
n = 5
input_data_plus = zeros((3,2*n+WIDTH,2*n+HEIGHT))#+0.5
target_data_plus = zeros((3,2*n+WIDTH,2*n+HEIGHT))+0.5



"""
r = 'Mr_Black_27Jul18_18h46m35s' #.net_projections.h5py'
p = opjD('temp_data')
O = h5r(opj(p,r,'original_timestamp_data.h5py'))
J = h5r(opj(p,d2p(r,'net_projections.h5py')))
ctr = 0
length = len(O['left_image']['vals'])
assert len(J['normal']) == length
"""


def get_data_function(P):

    #print Runs[r]['original_timestamp_data'].keys()
    #length = len(Runs[r]['original_timestamp_data']['data']['left_image']['vals'])
    #while True:
    #    ctr = rndint(length)
    #    if Runs[r]['button_number'][ctr] != 4:
    #        break
    good = good_list[rndint(len(good_list))]

    r, ctr = Run_coder[good[0]], good[1]

    flip = rndint(2)
    #flip = 1 


    if not flip:
        A = Runs[r]['net_projections']['data']['normal']
        B = Runs[r]['original_timestamp_data']['data']['left_image']['vals']
        #print 'not flip'
    else:
        A = Runs[r]['net_projections']['data']['flip']
        B = Runs[r]['flip_images']['data']['left_image_flip']['vals']
        #print 'FLIP'
    #input_data =  Runs[r]['net_projections']['data']['normal'][ctr].transpose(2,1,0)
    #target_data =  Runs[r]['original_timestamp_data']['data']['left_image']['vals'][ctr]
    #input_data =  A[ctr].transpose(2,1,0)

    ###############
    input_data =  A[ctr]
    temp = A[ctr]
    if flip:
        input_data[:,:,0] = temp[:,:,1]
        input_data[:,:,1] = temp[:,:,0]
    target_data = B[ctr]

    if False:
        if WIDTH == 41:
            target_data = cv2.resize(target_data ,(WIDTH,HEIGHT)).transpose(2,1,0)
            input_data =  input_data.transpose(2,1,0)
        else:
            input_data = cv2.resize(input_data ,(WIDTH,HEIGHT)).transpose(2,1,0)
            target_data =  target_data.transpose(2,1,0)

    input_data = cv2.resize(input_data ,(WIDTH,HEIGHT)).transpose(2,1,0)
    target_data = cv2.resize(target_data ,(WIDTH,HEIGHT)).transpose(2,1,0)


    input_data = 1/255.0*input_data
    input_data = input_data - 0.5
    target_data = 1/255.0*target_data
    #target_data = target_data - 0.5
    #print target_data.min().min(),target_data.max().max()
    #ctr += 1
    #if ctr >= length:
    #    ctr = 0
    #cy(P.keys(),ra=1)
    if r not in X['data_tracker']:
        X['data_tracker'][r] = {}
    if ctr not in X['data_tracker'][r]:
        X['data_tracker'][r][ctr] = 0
    X['data_tracker'][r][ctr] += 1

    ###############
    target_data_plus[:,n:n+WIDTH,n:n+HEIGHT] = target_data
    input_data_plus[:,n:n+WIDTH,n:n+HEIGHT] = input_data

    #cy( shape(input_data_plus),shape(target_data_plus))
    return {
        'input':input_data_plus,
        'target':target_data_plus,
        'ctr':ctr,
    }




#EOF
