from kzpy3.utils3 import *
import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.utils as nnutils
from torch.autograd import Variable
exec(identify_file_str)

try:
    torch._utils._rebuild_tensor_v2
except AttributeError:
    def _rebuild_tensor_v2(storage, storage_offset, size, stride, requires_grad, backward_hooks):
        tensor = torch._utils._rebuild_tensor(storage, storage_offset, size, stride)
        tensor.requires_grad = requires_grad
        tensor._backward_hooks = backward_hooks
        return tensor
    torch._utils._rebuild_tensor_v2 = _rebuild_tensor_v2



class Net(nn.Module):
    def __init__(self,P):

        super(Net, self).__init__()
        self.A = {}
        self.lr = P['LR']
        self.momentum = P['momentum']
        self.GPU = P['GPU']
        self.clip_param = P['clip']
        self.NETWORK_OUTPUT_FOLDER = P['NETWORK_OUTPUT_FOLDER']
        self.loss = None
        self.losses = []
        self.num_losses_to_average = P['losses_to_average']
        self.losses_to_average = []
        self.save_net_timer = Timer(P['save_timer_time'])
        self.setup_layers(P)
        self.setup_weights()
        self.setup_GPU()
        self.optimizer = torch.optim.Adadelta(filter(lambda p: p.requires_grad,self.parameters()))
        #elf.weight_list = []
        self.W = {}
        if P['resume']:
            self.load()
        else:
            clp('Starting with random weights','`wbb')





    def setup_GPU(self):
        self.GPU = 0
        print 'GPU set to 0'
        if self.GPU > -1:
            if self.GPU == 999:
                GPUs = gpu_stats(200)
                if GPUs[0]['util'] < 5 and GPUs[1]['util'] < 5:
                    self.GPU = random.choice([0,1])
                else:
                    self.GPU = GPUs['most_free']            
            torch.cuda.set_device(self.GPU)
            torch.cuda.device(self.GPU)
            clp("GPUs =",torch.cuda.device_count(),"current GPU =",torch.cuda.current_device(),'`ybb')#;time.sleep(1)
            #torch.cuda.set_device(0);torch.cuda.device(0)
            self.criterion = torch.nn.MSELoss().cuda()
        else:
            self.criterion = torch.nn.MSELoss()
        if self.GPU > -1:
            self = self.cuda()
        else:
            self = self.cpu()
            clp('Running in CPU mode')

    def data_to_torch(self,Data):

        Torch_data = {}

        for k in Data:

            if type(Data[k]) != type(None):
                if self.GPU > -1:
                    Torch_data[k] = torch.autograd.Variable(torch.from_numpy(Data[k]).cuda(device=self.GPU).float())
                else:
                    Torch_data[k] = torch.autograd.Variable(torch.from_numpy(Data[k]).float())
            else:
                Torch_data[k] = None

        return Torch_data


    def backward(self):
        self.loss.backward()
        nnutils.clip_grad_norm(self.parameters(), self.clip_param)#0.01) #1.0)
        self.optimizer.step()


    def extract(self,layer_name,batch_number=0):
        if layer_name == 'loss':
            return self.loss.data.cpu().numpy()
        else:
            return self.A[layer_name][batch_number,:].data.cpu().numpy()


    def save(self,temp=False):
        if self.save_net_timer.check() or temp:
            for f in ['weights','optimizer','state_dict','loss']:
                os.system(d2s('mkdir -p',opj(self.NETWORK_OUTPUT_FOLDER,f)))
            print('saving net state . . .')
            weights = {'net':self.state_dict().copy()}
            for key in weights['net']:
                if self.GPU > -1:
                    weights['net'][key] = weights['net'][key].cuda(device=self.GPU)
                else:
                    weights['net'][key] = weights['net'][key]
            if temp:
                torch.save(weights, opj(self.NETWORK_OUTPUT_FOLDER,'weights','temp.infer'))
                cb('. . . done saving temp.infer')
                return
            net_str = 'net'+'_'+time_str()+'.'+str(self.losses[-1])
            if self.GPU > -1:
                net_str = net_str+'.cuda'
            torch.save(weights, opj(self.NETWORK_OUTPUT_FOLDER,'weights',net_str+'.infer'))
            so(self.losses,opj(self.NETWORK_OUTPUT_FOLDER,'loss',net_str+'.loss_avg'))
            torch.save(self.optimizer.state_dict(), opj(self.NETWORK_OUTPUT_FOLDER,'optimizer',net_str+'.optimizer_state'))
            torch.save(self.state_dict(), opj(self.NETWORK_OUTPUT_FOLDER,'state_dict',net_str+'.state_dict'))
            print('. . . done saving.')
            self.save_net_timer.reset()
            return True
        else:
            return False



    def load(self):
        clp(opj(self.NETWORK_OUTPUT_FOLDER,'weights'))
        f = most_recent_file_in_folder(opj(self.NETWORK_OUTPUT_FOLDER,'weights'),['.infer'],[])
        clp('Resuming with','`','',f,'','`--rb'); time.sleep(1)
        save_data = torch.load(f)
        self.load_state_dict(save_data['net'])

        f = most_recent_file_in_folder(opj(self.NETWORK_OUTPUT_FOLDER,'loss'),['.loss_avg.pkl'],[])
        self.losses = lo(f)


    def store_weights(self):
        import copy
        self.W[self.losses[-1]] = copy.deepcopy(self.state_dict())
        #self.weight_list.append(copy.deepcopy(self.state_dict()))
        ks = sorted(self.W.keys())
        if len(ks) > 100:
            for k in [100,len(ks)]:
                del self.W[k]
        #if len(self.weight_list) > 30:
            self.weight_list.pop(0)
        clp("len(self.W) =",len(self.W.keys()))

    def use_stored_weight(self):
        print("use_stored_weight(self)")
        #a = self.state_dict()['final_deconv.weight'].data.cpu().numpy()[:,0,0,0]
        ks = sorted(self.W.keys())
        print(ks)
        #b = self.weight_list[0]['final_deconv.weight'].data.cpu().numpy()[:,0,0,0]
        #b = self.weight_list[0]['final_deconv.weight'].data.cpu().numpy()[:,0,0,0]
        #print("((a-b)**2).sum()",((a-b)**2).sum())
        #l = max(1,int(len(ks)/10.0))
        l = min(10,len(ks))
        self.load_state_dict(self.W[rndchoice(ks[:l])])

        clp("self.load_state_dict(rndchoice(self.weight_list))",'`rwb')

class Fire(nn.Module):
    def __init__(self, inplanes, squeeze_planes,
                 expand1x1_planes, expand3x3_planes):
        super(Fire, self).__init__()
        self.inplanes = inplanes
        self.squeeze = nn.Conv2d(inplanes, squeeze_planes, kernel_size=1)
        self.squeeze_activation = nn.ReLU(inplace=True)
        self.expand1x1 = nn.Conv2d(squeeze_planes, expand1x1_planes,
                                   kernel_size=1)
        self.expand1x1_activation = nn.ReLU(inplace=True)
        self.expand3x3 = nn.Conv2d(squeeze_planes, expand3x3_planes,
                                   kernel_size=3, padding=1)
        self.expand3x3_activation = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.squeeze_activation(self.squeeze(x))
        return torch.cat([
            self.expand1x1_activation(self.expand1x1(x)),
            self.expand3x3_activation(self.expand3x3(x))
        ], 1)






def make_batch(get_data_function,P,batch_size):
    Data = {}
    for i in range(batch_size):
        D = get_data_function(P)
        for k in D.keys():
            if k not in Data:
                Data[k] = []
            Data[k].append(D[k])
    for k in Data.keys():
        Data[k] = na(Data[k])
    return Data


#EOF
