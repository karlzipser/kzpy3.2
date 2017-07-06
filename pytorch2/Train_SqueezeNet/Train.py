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

DD=Data.Data()

batch = Batch.Batch({'net':net,'batch_size':P.BATCH_SIZE})

loss_record = {}
loss_record['train'] = Utils.Loss_Record()
loss_record['val'] = Utils.Loss_Record()

train_timer = Timer(60*5)
val_timer = Timer(60*1)
while True:

    batch['fill']({'Data':DD,'mode':'train'})
    
    batch['forward']({'optimizer':optimizer,'criterion':criterion})
    batch['backward']({'optimizer':optimizer})

    loss_record['add']({'loss':batch['loss'].data.cpu().numpy()[0]})

    Utils.save_net({'net':net})
    batch['display']({})
    """
    print batch['loss'];print['loss'];pause(4)
    print batch['outputs'];print['outputs'];pause(4)
    print batch['target_data'];print['target_data'];pause(4)
    print batch['data_ids'];print['data_ids'];pause(4)
    """
    rate_counter['step']({'batch_size':batch['batch_size']})

    batch['clear']()


    if P.epoch_timer.check():
        pd2s('\tctr =',DD['train']['ctr'],dp(100.0*DD['train']['ctr']/(1.0*len(DD['train']['all_steer']))),'%')
        P.epoch_timer.reset()
        figure(mode+' loss');clf()
        loss_record['plot']()

#EOF