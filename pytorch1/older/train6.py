from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg9','kzpy3/pytorch1','kzpy3/pytorch1/nets'])
from vis2 import *
import data.utils.get_data_with_hdf5 as get_data_with_hdf5
import torch



GPU = 1
BATCH_SIZE = 100
DISPLAY = False
MODEL = 'SqueezeNet'
RESUME = True
print(MODEL)
bair_car_data_path = opjD('bair_car_data_Main_Dataset')
if RESUME:
    weights_file_path = opjD('save_file.weights')
ignore = ['reject_run','left','out1_in2']#,'Smyth','racing','local','Tilden','campus']
require_one = []
use_states = [1,3,5,6,7]

print_timer = Timer(5)
save_net_timer = Timer(60*10)





torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(GPU)
torch.cuda.device(GPU)
init_str = """
from nets.MODEL import MODEL
net = MODEL().cuda()
"""
init_str = init_str.replace("MODEL",MODEL)
exec(init_str)
criterion = torch.nn.MSELoss().cuda()
optimizer = torch.optim.Adadelta(net.parameters())


if False:#RESUME:
    cprint(d2s('Resuming with',weights_file_path),'yellow')
    save_data = torch.load(weights_file_path)
    net.load_state_dict(save_data)


#saved_net_weights = torch.load('/home/karlzipser/pytorch_models/epoch6goodnet')
#net.load_state_dict(saved_net_weights['net'])







hdf5_runs_path = opj(bair_car_data_path,'hdf5/runs')
hdf5_segment_metadata_path = opj(bair_car_data_path,'hdf5/segment_metadata')
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
if DISPLAY:
        figure('high low steer histograms',figsize=(2,1))
        histogram_plot_there = True
        clf()
        plt.hist(array(low_steer)[:,2],bins=range(0,100))
        plt.hist(array(high_steer)[:,2],bins=range(0,100))
        figure(1)





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

    data = get_data_with_hdf5.get_data(run_code,seg_num,offset,net.N_STEPS,offset+0,net.N_FRAMES,ignore=ignore,require_one=require_one,use_states=use_states)

    return data







def display_output(d):
    if 'print_now' not in d:
        d['print_now'] = False
    print_now = d['print_now']

    if print_timer.check() or print_now:

        batch = d['batch']
        #outputs = d['outputs']

        o = batch['outputs'][0].data.cpu().numpy()
        #o = outputs[0].data.cpu().numpy()
        t= batch['target_data'][0].cpu().numpy()
        print('1. Output:')
        print(t) # Output of Network
        print('2. Labels:')
        print(o)
        print('3. Loss:')
        #print(array(loss_list[-loss_list_N:]).mean())
        #print(loss_list[-1])
        a=batch['camera_data'][0][:].cpu().numpy()
        b=a.transpose(1,2,0)
        h = shape(a)[1]
        w = shape(a)[2]
        c = zeros((10+h*2,10+2*w,3))
        c[:h,:w,:] = z2o(b[:,:,3:6])
        c[:h,-w:,:] = z2o(b[:,:,:3])
        c[-h:,:w,:] = z2o(b[:,:,9:12])
        c[-h:,-w:,:] = z2o(b[:,:,6:9])
        mi(c,'cameras')
        figure('steer')
        clf()
        ylim(-0.05,1.05);xlim(0,len(t))
        plot([-1,60],[0.49,0.49],'k');plot(o,'og'); plot(t,'or'); plt.title(batch['names'][0])
        pause(0.000000001)
        print_timer.reset()
        #batch['clear']()







def save_net():
    if save_net_timer.check():
        torch.save(net.state_dict(), opjD('save_file.weights'))
        save_net_timer.reset()
    


loss_list = []






def Batch(d):
    batch_size = d['batch_size']

    D = {}
    D['type'] = 'batch'
    D['Purpose'] = d2s(inspect.stack()[0][3],':','object to collect data for pytorch batch')
    D['batch_size'] = batch_size
    D['camera_data'] = torch.FloatTensor().cuda()
    D['metadata'] = torch.FloatTensor().cuda()
    D['target_data'] = torch.FloatTensor().cuda()
    D['names'] = []
    def _fill(d):
        get_data_function = d['get_data_function']

        for b in range(D['batch_size']):
            _data = None
            while _data == None:
                _data = get_data_function()
            data = _data
            _data_into_batch(data)
    D['fill'] = _fill
    def _data_into_batch(data):

        if True:
            D['names'].insert(0,data['name']) # This to match torch.cat use below

        if True:
            list_camera_input = []
            for t in range(net.N_FRAMES):
                for camera in ('left', 'right'):
                    list_camera_input.append(torch.from_numpy(data[camera][t]))

            camera_data = torch.cat(list_camera_input, 2)
            camera_data = camera_data.cuda().float()
            camera_data = torch.transpose(camera_data, 0, 2)
            camera_data = torch.transpose(camera_data, 1, 2)

            D['camera_data'] = torch.cat((torch.unsqueeze(camera_data, 0), D['camera_data']), 0)

        if True:
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
            D['metadata'] = torch.cat((metadata, D['metadata']), 0)

        if True:
            steer = torch.from_numpy(data['steer'][-net.N_STEPS:]).cuda().float() / 99.
            motor = torch.from_numpy(data['motor'][-net.N_STEPS:]).cuda().float() / 99.
            steer_motor = torch.unsqueeze(torch.cat((steer, motor), 0), 0)
            D['target_data'] = torch.cat((steer_motor, D['target_data']), 0)
    def _clear():
        D['batch_size'] = None
        D['camera_data'] = None
        D['metadata'] = None
        D['target_data'] = None
        D['names'] = None
        D['outputs'] = None
        D['loss'] = None
    D['clear'] = _clear
    def _train(d):
        net = d['net']
        optimizer = d['optimizer']
        
        optimizer.zero_grad()
        D['outputs'] = net(torch.autograd.Variable(D['camera_data']), torch.autograd.Variable(D['metadata'])).cuda()
        D['loss'] = criterion(D['outputs'], torch.autograd.Variable(D['target_data']))
        D['loss'].backward()
        optimizer.step()
    D['train'] = _train
    return D



def Rate_Counter():
    D = {}
    D['type'] = 'Rate_Counter'
    D['Purpose'] = d2s(inspect.stack()[0][3],':','Network rate object')
    D['rate_ctr'] = 0
    D['rate_timer_interval'] = 10.0
    D['rate_timer'] = Timer(D['rate_timer_interval'])
    def _step(d):
        batch_size = d['batch_size']

        D['rate_ctr'] += 1
        if D['rate_timer'].check():
            print(d2s('rate =',dp(batch_size*D['rate_ctr']/D['rate_timer_interval'],2),'Hz'))
            D['rate_timer'].reset()
            D['rate_ctr'] = 0
    D['step'] = _step
    return D   

rate_counter = Rate_Counter()


while True:

    batch = Batch({'batch_size':BATCH_SIZE})
    batch['fill']({'get_data_function':get_data_considering_high_low_steer})
    batch['train']({'net':net,'optimizer':optimizer})

    """
    optimizer.zero_grad()
    outputs = net(torch.autograd.Variable(batch['camera_data']), torch.autograd.Variable(batch['metadata'])).cuda()
    loss = criterion(outputs, torch.autograd.Variable(batch['target_data']))
    """
    
    loss_list.append(batch['loss'].data[0])
    loss_list_N = 1000/BATCH_SIZE
    if len(loss_list) > 1.5*loss_list_N:
        loss_list = loss_list[-loss_list_N:]
    """
    loss.backward()
    optimizer.step()
    """
    save_net()
    
    display_output({'batch':batch})

    rate_counter['step']({'batch_size':batch['batch_size']})

    batch['clear']()




