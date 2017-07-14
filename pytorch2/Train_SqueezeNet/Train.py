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

rate_counter = Utils.Rate_Counter()

DD=Data.Data()

timer = {}
timer['train'] = Timer(60*30)
timer['val'] = Timer(60*3)
trial_loss_record = {}

batch = Batch.Batch({'net':net,'batch_size':P.BATCH_SIZE})


while True:
    for mode in ['train','val']:

        timer[mode].reset()

        while not timer[mode].check():

            batch['fill']({'Data':DD,'mode':mode})
            
            batch['forward']({'optimizer':optimizer,'criterion':criterion,'trial_loss_record':trial_loss_record})

            if mode == 'train':
                batch['backward']({'optimizer':optimizer})

            loss_record[mode]['add']({'loss':batch['loss'].data.cpu().numpy()[0]})

            Utils.save_net({'net':net,'loss_record':loss_record})

            batch['display']({})


            rate_counter['step']({'batch_size':batch['batch_size']})

            batch['clear']()


            if P.epoch_timer.check():
                pd2s('\tmode =',mode,'ctr =',DD[mode]['ctr'],dp(100.0*DD[mode]['ctr']/(1.0*len(DD[mode]['all_steer']))),'%')
                P.epoch_timer.reset()
                figure('loss');clf();ylim(0.003,0.006);xlim(146,200)
                loss_record['train']['plot']({'c':'b'})
                loss_record['val']['plot']({'c':'r'})





import operator
sorted_trial_loss_record = sorted(trial_loss_record.items(),key=operator.itemgetter(1))

for i in range(len(sorted_trial_loss_record)/2,len(sorted_trial_loss_record)/2+100):#range(-1,-100,-1):
    l =  sorted_trial_loss_record[i]
    run_code,seg_num,offset = sorted_trial_loss_record[i][0][0]
    t = sorted_trial_loss_record[i][0][1]
    o = sorted_trial_loss_record[i][0][2]
    data = DD['get_data']({'run_code':run_code,'seg_num':seg_num,'offset':offset})
    figure(22);clf();ylim(0,1)
    plot(t,'r.')
    plot(o,'g.')
    plot([0,20],[0.5,0.5],'k')
    mi(data['right'][0,:,:],23,img_title=d2s(l[1]))
    pause(1)


Sorted_trial_loss_record_dic = {}
Sorted_trial_loss_record_dic['ids'] = []
Sorted_trial_loss_record_dic['losses'] = []
for i in range(len(sorted_trial_loss_record)):
    l =  sorted_trial_loss_record[i]
    run_code,seg_num,offset = sorted_trial_loss_record[i][0][0]
    t = sorted_trial_loss_record[i][0][1]
    o = sorted_trial_loss_record[i][0][2]
    Sorted_trial_loss_record_dic['ids'].append((run_code,seg_num,offset))
    Sorted_trial_loss_record_dic['losses'].append(l[1])

#so(Sorted_trial_loss_record_dic,opjD('Sorted_trial_loss_record_dic_'+time_str()))

#EOF