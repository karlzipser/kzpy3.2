from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/pytorch1','kzpy3/pytorch1/nets',])
from vis2 import *
import torch
import Data
from Data import get_data_considering_high_low_steer as get_data_function
import Batch
from Utils import Rate_Counter


GPU = 1
BATCH_SIZE = 100
DISPLAY = False
MODEL = 'SqueezeNet'
RESUME = True
print(MODEL)
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
from nets.MODEL import SqueezeNet
net = SqueezeNet().cuda()
"""
init_str = init_str.replace("MODEL",MODEL)
exec(init_str)
criterion = torch.nn.MSELoss().cuda()
optimizer = torch.optim.Adadelta(net.parameters())

if True:#RESUME:
    cprint(d2s('Resuming with',weights_file_path),'yellow')
    save_data = torch.load(weights_file_path)
    net.load_state_dict(save_data)
    time.sleep(4)


#saved_net_weights = torch.load('/home/karlzipser/pytorch_models/epoch6goodnet')
#net.load_state_dict(saved_net_weights['net'])

def save_net():
    if save_net_timer.check():
        torch.save(net.state_dict(), opjD('save_file.weights'))
        save_net_timer.reset()
    

loss_list = []


rate_counter = Rate_Counter()


while True:

    batch = Batch.Batch({'batch_size':BATCH_SIZE})
    batch['fill']({'get_data_function':get_data_function,'get_data_args':{'N_STEPS':net.N_STEPS,'N_FRAMES':net.N_FRAMES,'ignore':ignore}})
    batch['train']({'net':net,'optimizer':optimizer})

    loss_list.append(batch['loss'].data[0])
    loss_list_N = 1000/BATCH_SIZE
    if len(loss_list) > 1.5*loss_list_N:
        loss_list = loss_list[-loss_list_N:]

    save_net()
    
    batch['display']({})

    rate_counter['step']({'batch_size':batch['batch_size']})

    batch['clear']()




