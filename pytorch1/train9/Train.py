from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/pytorch1','kzpy3/pytorch1/nets','kzpy3/pytorch1/train9'])
from vis2 import *
import torch
import Data
from Data import get_data_considering_high_low_steer_and_valid_trajectory_timestamp as get_data_function
import Batch
from Utils import Rate_Counter
import Parameters as P



torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(P.GPU)
torch.cuda.device(P.GPU)
init_str = """
from nets.MODEL import SqueezeNet
net = SqueezeNet().cuda()
"""
init_str = init_str.replace("MODEL",P.MODEL)
exec(init_str)
criterion = torch.nn.MSELoss().cuda()
optimizer = torch.optim.Adadelta(net.parameters())


if RESUME:
    cprint(d2s('Resuming with',P.weights_file_path),'yellow')
    save_data = torch.load(P.weights_file_path)
    net.load_state_dict(save_data)
    time.sleep(4)


#saved_net_weights = torch.load('/home/karlzipser/pytorch_models/epoch6goodnet')
#net.load_state_dict(saved_net_weights['net'])

def save_net():
    if P.save_net_timer.check():
        torch.save(net.state_dict(), opjD('save_file_Aruco.weights'))
        P.save_net_timer.reset()
    

loss_list = []


rate_counter = Rate_Counter()


while True:

    batch = Batch.Batch({'net':net,'batch_size':P.BATCH_SIZE})
    
    batch['fill']({
        'get_data_function':get_data_function,
        'get_data_args':{'N_STEPS':net.N_STEPS,'N_FRAMES':net.N_FRAMES,'ignore':P.ignore,'require_one':P.require_one,'use_states':P.use_states}})
    
    batch['train']({'optimizer':optimizer,'criterion':criterion})

    loss_list.append(batch['loss'].data[0])
    loss_list_N = 1000/P.BATCH_SIZE
    if len(loss_list) > 1.5*loss_list_N:
        loss_list = loss_list[-loss_list_N:]

    save_net()
    
    batch['display']({})

    rate_counter['step']({'batch_size':batch['batch_size']})

    batch['clear']()




