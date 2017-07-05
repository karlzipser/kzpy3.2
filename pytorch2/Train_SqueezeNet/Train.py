if '__file__' not in locals():
    __file__ = 'Train.py'
from kzpy3.utils2 import *
cprint('****************** '+__file__+' ******************','yellow')
pythonpaths(['kzpy3','kzpy3/pytorch2/nets','kzpy3/pytorch2/Train_SqueezeNet'])
from vis2 import *
import torch
import Data
DD=Data.Data()
get_data_function = DD['get_data']
import Batch
import Utils
import Parameters as P



torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(P.GPU)
torch.cuda.device(P.GPU)

from nets.SqueezeNet import SqueezeNet
net = SqueezeNet().cuda()
criterion = torch.nn.MSELoss().cuda()
optimizer = torch.optim.Adadelta(net.parameters())


if P.RESUME:
    cprint(d2s('Resuming with',P.weights_file_path),'yellow')
    save_data = torch.load(P.weights_file_path)
    net.load_state_dict(save_data)
    time.sleep(4)


rate_counter = Utils.Rate_Counter()

data = lo(opjD('valid_steer_data'))


#timer = Timer(0)

batch = Batch.Batch({'net':net,'batch_size':P.BATCH_SIZE})

P.data_ctr = 0
while P.data_ctr < len(data['train_steer']):
    e = data['train_steer'][i]
    run_code = e[3]
    seg_num = e[0]
    offset = e[1]



    #print dp(1/timer.time())
    #timer.reset()

    #batch = Batch.Batch({'net':net,'batch_size':P.BATCH_SIZE})
    
    batch['fill']({'get_data_function':get_data_function,'data':data}) #get_data_args':{'run_code':run_code,'seg_num':seg_num,'offset':offset}})
    
    batch['forward']({'optimizer':optimizer,'criterion':criterion})
    batch['backward']({'optimizer':optimizer})

    #data['train_los_dic'][(run_code,seg_num,offset)] = loss

    Utils.save_net({'net':net})
    
    batch['display']({})


    rate_counter['step']({'batch_size':batch['batch_size']})

    batch['clear']()

    if P.epoch_timer.check():
        pd2s(' i =',i)
        P.epoch_timer.reset()


"""
        loss_record
        ['loss_sum'] += D['loss'].data[0]
        loss_record['loss_ctr'] += 1
        if D['loss_ctr'] == P.LOSS_CTR_LIMIT:
            D['avg_los']

    D['loss_ctr'] = 0
    D['loss_sum'] = 0
"""


