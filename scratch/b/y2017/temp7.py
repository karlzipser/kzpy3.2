if '__file__' not in locals():
    __file__ = 'Train.py'
from kzpy3.utils2 import *
cprint('****************** '+__file__+' ******************','yellow')
pythonpaths(['kzpy3','kzpy3/pytorch2/nets','kzpy3/pytorch2/Train_SqueezeNet'])
from vis2 import *
import torch
import Data
import Batch
import Utils
import Parameters as P



torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(P.GPU)
torch.cuda.device(P.GPU)

from nets2.SqueezeNet import SqueezeNet
net = SqueezeNet().cuda()
criterion = torch.nn.MSELoss().cuda()
optimizer = torch.optim.Adadelta(net.parameters())

if P.RESUME:
    cprint(d2s('Resuming with',P.weights_file_path),'yellow')
    save_data = torch.load(P.weights_file_path)
    net.load_state_dict(save_data)
    time.sleep(4)
    loss_record_loaded = zload_obj({'path':opjD('loss_record')})
    loss_record = {}
    for mode in ['train','val']:
        loss_record[mode] = Utils.Loss_Record()
        for k in loss_record_loaded[mode].keys():
            if not callable(loss_record[mode][k]):
                loss_record[mode][k] = loss_record_loaded[mode][k]
else:
    loss_record = {}
    loss_record['train'] = Utils.Loss_Record()
    loss_record['val'] = Utils.Loss_Record()

