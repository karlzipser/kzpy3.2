from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg9','kzpy3/pytorch1','kzpy3/pytorch1/nets'])
from vis2 import *
import data.utils.get_data_with_hdf5 as get_data_with_hdf5
import torch

#################################################
# PyTorch Network Initialization
#################################################

if True: # Easily Modifiable Parameters
    GPU = 1
    BATCH_SIZE = 100
    DISPLAY = False
    MODEL = 'SqueezeNet'
    RESUME = False
    print(MODEL)
    bair_car_data_path = opjD('bair_car_data_Main_Dataset')
    if RESUME:
        weights_file_path = 'xxx'
    ignore = ['reject_run','left','out1_in2']#,'Smyth','racing','local','Tilden','campus']
    require_one = []
    use_states = [1,3,5,6,7]
    rate_timer_interval = 5.
    print_timer = Timer(5)



torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(GPU)
torch.cuda.device(GPU)

init_str = """
from nets.MODEL import MODEL
net = MODEL().cuda()
"""
init_str = init_str.replace("MODEL",MODEL)
exec(init_str)
criterion = torch.nn.MSELoss().cuda()  # define loss function
optimizer = torch.optim.Adadelta(net.parameters()) # define optimizer (adjusts learning rate dynamically)

N_FRAMES = net.N_FRAMES
N_STEPS = net.N_STEPS

##################################################
# ENDPyTorch Network Initialization
##################################################


##################################################
# Data Loading
##################################################



hdf5_runs_path = opj(bair_car_data_path,'hdf5/runs')
hdf5_segment_metadata_path = opj(bair_car_data_path,'hdf5/segment_metadata')

rate_timer = Timer(rate_timer_interval)
rate_ctr = 0

get_data_with_hdf5.load_Segment_Data(hdf5_segment_metadata_path,hdf5_runs_path)

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

def get_data_considering_high_low_steer():
    global ctr_low
    global ctr_high
    global low_steer
    global high_steer

    if ctr_low >= len_low_steer:
        ctr_low = -1
    if ctr_high >= len_high_steer:
        ctr_high = -1
    if ctr_low == -1:
        random.shuffle(low_steer) # shuffle data before using (again)
        ctr_low = 0
    if ctr_high == -1:
        random.shuffle(high_steer)
        ctr_high = 0
    if random.random() < 0.5: # len_high_steer/(len_low_steer+len_high_steer+0.0): # with some probability choose a low_steer element
        choice = low_steer[ctr_low]
        ctr_low += 1
    else:
        choice = high_steer[ctr_high]
        ctr_high += 1

    run_code = choice[3]
    seg_num = choice[0]
    offset = choice[1]

    data = get_data_with_hdf5.get_data(run_code,seg_num,offset,N_STEPS,offset+0,N_FRAMES,ignore=ignore,require_one=require_one,use_states=use_states)

    return data

if DISPLAY:
        figure('high low steer histograms',figsize=(2,1))
        histogram_plot_there = True
        clf()
        plt.hist(array(low_steer)[:,2],bins=range(0,100))
        plt.hist(array(high_steer)[:,2],bins=range(0,100))
        figure(1)


##################################################
# ENDData Loading
##################################################

loss_list = []

while True:

    batch_camera_data = torch.FloatTensor().cuda()
    batch_metadata = torch.FloatTensor().cuda()
    batch_labels = torch.FloatTensor().cuda()

    for b in range(BATCH_SIZE): #######################
        _data = None
        while _data == None:
            _data = get_data_considering_high_low_steer()
        data = _data

        if True: # Get camera data
            list_camera_input = []
            for t in range(N_FRAMES):
                for camera in ('left', 'right'):
                    list_camera_input.append(torch.from_numpy(data[camera][t]))

            camera_data = torch.cat(list_camera_input, 2)
            camera_data = camera_data.cuda().float()
            camera_data = torch.transpose(camera_data, 0, 2)
            camera_data = torch.transpose(camera_data, 1, 2)

            batch_camera_data = torch.cat((torch.unsqueeze(camera_data, 0), batch_camera_data), 0)

        if True: # Get metadata
            metadata = torch.FloatTensor().cuda()
            zero_matrix = torch.FloatTensor(1, 1, 23, 41).zero_().cuda()
            one_matrix = torch.FloatTensor(1, 1, 23, 41).fill_(1).cuda()
         
            for cur_label in ['racing', 'caffe', 'follow', 'direct', 'play', 'furtive']:
                if cur_label == 'caffe':
                    if data['states'][0]:
                        metadata = torch.cat((one_matrix, metadata), 1)
                    else:
                        metadata = torch.cat((zero_matrix, metadata), 1)
                else:
                    if data['labels'][cur_label]:
                        metadata = torch.cat((one_matrix, metadata), 1)
                    else:
                        metadata = torch.cat((zero_matrix, metadata), 1)

            for i in range(122): # Concatenate zero matrices to fit the dataset
                metadata = torch.cat((zero_matrix, metadata), 1)

            batch_metadata = torch.cat((metadata, batch_metadata), 0)


        if True: # Get labels
            steer = torch.from_numpy(data['steer'][-net.N_STEPS:]).cuda().float() / 99.
            motor = torch.from_numpy(data['motor'][-net.N_STEPS:]).cuda().float() / 99.
            labels = torch.unsqueeze(torch.cat((steer, motor), 0), 0)
            batch_labels = torch.cat((labels, batch_labels), 0)

        rate_ctr += 1
        if rate_timer.check():
            print(d2s('rate =',dp(rate_ctr/rate_timer_interval,2),'Hz'))
            rate_timer.reset()
            rate_ctr = 0

    optimizer.zero_grad()
    outputs = net(torch.autograd.Variable(batch_camera_data), torch.autograd.Variable(batch_metadata)).cuda()
    loss = criterion(outputs, torch.autograd.Variable(batch_labels))
    loss_list.append(loss.data[0])
    loss_list_N = 1000/BATCH_SIZE
    if len(loss_list) > 1.5*loss_list_N:
        loss_list = loss_list[-loss_list_N:]
    loss.backward()
    optimizer.step()

    if print_timer.check():
        print('1. Output:')
        print(outputs) # Output of Network
        print('2. Labels:')
        print(labels)
        print('3. Loss:')
        print(array(loss_list[-loss_list_N:]).mean())
        print(loss_list[-1])
        print_timer.reset()
        mi(batch_camera_data[0][0].cpu().numpy());pause(0.000000001)
