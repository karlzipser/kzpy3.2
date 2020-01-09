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

        kprint(P,title='from SN')
        super(Net, self).__init__()
        self.A = {}
        self.lr = P['LR']
        self.momentum = P['MOMENTUM']
        self.GPU = P['GPU']
        self.NETWORK_OUTPUT_FOLDER = P['NETWORK_OUTPUT_FOLDER']
        self.loss = None
        self.losses = []
        self.num_losses_to_average = P['NUM_LOSSES_TO_AVERAGE']
        self.losses_to_average = []
        self.save_net_timer = Timer(P['NET_SAVE_TIMER_TIME'])
        self.setup_layers(P)
        self.setup_weights()
        self.setup_GPU()
        self.optimizer = torch.optim.Adadelta(filter(lambda p: p.requires_grad,self.parameters()))

        if P['RESUME']:
            self.load()
        else:
            clp('Starting with random weights','`wbb')


    def setup_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                if m is self.final_conv:
                    init.normal(m.weight.data, mean=0.0, std=0.01)
                else:
                    init.kaiming_uniform(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()


    def setup_GPU(self):
        if self.GPU > -1:
            if self.GPU == 999:
                GPUs = gpu_stats(400)
                if GPUs[0]['util'] < 5 and GPUs[1]['util'] < 5:
                    self.GPU = random.choice([0,1])
                else:
                    self.GPU = GPUs['most_free']            
            torch.cuda.set_device(self.GPU)
            torch.cuda.device(self.GPU)
            clp("GPUs =",torch.cuda.device_count(),"current GPU =",torch.cuda.current_device(),'`ybb');time.sleep(1)
            torch.cuda.set_device(0);torch.cuda.device(0)
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
                    Torch_data[k] = torch.autograd.Variable(torch.from_numpy(Data[k]).cuda(device=0).float())
                else:
                    Torch_data[k] = torch.autograd.Variable(torch.from_numpy(Data[k]).float())
            else:
                Torch_data[k] = None

        return Torch_data


    def backward(self):
        self.loss.backward()
        nnutils.clip_grad_norm(self.parameters(), 1.0)
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
                    weights['net'][key] = weights['net'][key].cuda(device=0)
                else:
                    weights['net'][key] = weights['net'][key]
            if temp:
                torch.save(weights, opj(self.NETWORK_OUTPUT_FOLDER,'weights','temp.infer'))
                cb('. . . done saving temp.infer')
                return
            net_str = 'net'+'_'+time_str()
            if self.GPU > -1:
                net_str = net_str+'.cuda'
            torch.save(weights, opj(self.NETWORK_OUTPUT_FOLDER,'weights',net_str+'.infer'))
            so(self.losses,opj(self.NETWORK_OUTPUT_FOLDER,'loss',net_str+'.loss_avg'))
            torch.save(self.optimizer.state_dict(), opj(self.NETWORK_OUTPUT_FOLDER,'optimizer',net_str+'.optimizer_state'))
            torch.save(self.state_dict(), opj(self.NETWORK_OUTPUT_FOLDER,'state_dict',net_str+'.state_dict'))
            print('. . . done saving.')
            self.save_net_timer.reset()


    def load(self):
        f = most_recent_file_in_folder(opj(self.NETWORK_OUTPUT_FOLDER,'weights'),['.infer'],[])
        clp('Resuming with','`','',f,'','`--rb'); time.sleep(1)
        save_data = torch.load(f)
        self.load_state_dict(save_data['net'])

        f = most_recent_file_in_folder(opj(self.NETWORK_OUTPUT_FOLDER,'loss'),['.loss_avg.pkl'],[])
        self.losses = lo(f)





class SqueezeNet(Net):
    def forward(self,Data):
        self.optimizer.zero_grad()

        Torch_data = self.data_to_torch(Data)

        self.A['camera_input'] = Torch_data['input']

        self.A['pre_metadata_features'] = self.pre_metadata_features(self.A['camera_input'])
        if 'meta' not in Torch_data or type(Torch_data['meta_data']) == type(None):
            self.A['pre_metadata_features_metadata'] = self.A['pre_metadata_features']
        else:
            self.A['pre_metadata_features_metadata'] = torch.cat((self.A['pre_metadata_features'], Torch_data['meta']), 1)
        self.A['post_metadata_features'] = self.post_metadata_features(self.A['pre_metadata_features_metadata'])
        self.A['final_output'] = self.final_output(self.A['post_metadata_features'])
        self.A['final_output'] = self.A['final_output'].view(self.A['final_output'].size(0), -1)
        self.A['target'] = Torch_data['target']
        self.loss = self.criterion(self.A['final_output'],Torch_data['target'])
        self.losses_to_average.append(self.extract('loss'))
        if len(self.losses_to_average) >= self.num_losses_to_average:
            self.losses.append( na(self.losses_to_average).mean() )
            self.losses_to_average = []
        return self.A['final_output']


    def setup_layers(self,P):
        self.pre_metadata_features = nn.Sequential(
            nn.Conv2d(P['NUM_INPUT_CHANNELS'], 64, kernel_size=3, stride=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(64, 16, 64, 64),            
            )
        self.post_metadata_features = nn.Sequential(
            Fire(64+64+P['NUM_METADATA_CHANNELS'], 16, 64, 64),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(128, 32, 128, 128),
            Fire(256, 32, 128, 128),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(256, 48, 192, 192),
            Fire(384, 48, 192, 192),
            Fire(384, 64, 256, 256),
            Fire(512, 64, 256, 256),
        )
        self.final_conv = nn.Conv2d(512, P['NUM_OUTPUTS'], kernel_size=1)
        self.final_output = nn.Sequential(
            nn.Dropout(p=0.5),
            self.final_conv,
            nn.AvgPool2d(kernel_size=5, stride=6)
        )







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
