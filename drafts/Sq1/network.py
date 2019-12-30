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





class SqueezeNet(nn.Module):
    def __init__(
        self,
        NUM_INPUT_CHANNELS,
        NUM_OUTPUTS,
        NUM_METADATA_CHANNELS,
        NUM_LOSSES_TO_AVERAGE,
        NETWORK_OUTPUT_FOLDER,
        NET_SAVE_TIMER_TIME,
        previous_losses = [],
        LR=0.01,
        MOMENTUM=0.001,
    ):
        super(SqueezeNet, self).__init__()
        self.A = {}
        self.lr = LR
        self.momentum = MOMENTUM
        self.NETWORK_OUTPUT_FOLDER = NETWORK_OUTPUT_FOLDER
        self.pre_metadata_features = nn.Sequential(
            nn.Conv2d(NUM_INPUT_CHANNELS, 64, kernel_size=3, stride=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(64, 16, 64, 64),            
            )
        self.post_metadata_features = nn.Sequential(
            Fire(64+64+NUM_METADATA_CHANNELS, 16, 64, 64),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(128, 32, 128, 128),
            Fire(256, 32, 128, 128),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(256, 48, 192, 192),
            Fire(384, 48, 192, 192),
            Fire(384, 64, 256, 256),
            Fire(512, 64, 256, 256),
        )
        final_conv = nn.Conv2d(512, NUM_OUTPUTS, kernel_size=1)
        self.final_output = nn.Sequential(
            nn.Dropout(p=0.5),
            final_conv,
            nn.AvgPool2d(kernel_size=5, stride=6)
        )

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                if m is final_conv:
                    init.normal(m.weight.data, mean=0.0, std=0.01)
                else:
                    init.kaiming_uniform(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()
    
        self.criterion = torch.nn.MSELoss()#.cuda()
        self.optimizer = torch.optim.Adadelta(filter(lambda p: p.requires_grad,self.parameters()))
        self.loss = None
        self.losses = previous_losses
        self.num_losses_to_average = NUM_LOSSES_TO_AVERAGE
        self.losses_to_average = []
        self.save_net_timer = Timer(NET_SAVE_TIMER_TIME)

    def forward(self,input_data,meta_data,target_data):

        self.optimizer.zero_grad()

        input_torch = torch.autograd.Variable(torch.from_numpy(input_data).float())

        if type(meta_data) != type(None):
            meta_data_torch = torch.autograd.Variable(torch.from_numpy(meta_data).float())
        else:
            meta_data_torch = None

        target_torch = torch.autograd.Variable(torch.from_numpy(target_data).float())

        self.A['camera_input'] = input_torch
        self.A['pre_metadata_features'] = self.pre_metadata_features(self.A['camera_input'])
        if type(meta_data) == type(None):
            self.A['pre_metadata_features_metadata'] = self.A['pre_metadata_features']
        else:
            self.A['pre_metadata_features_metadata'] = torch.cat((self.A['pre_metadata_features'], meta_data_torch), 1)
        self.A['post_metadata_features'] = self.post_metadata_features(self.A['pre_metadata_features_metadata'])
        self.A['final_output'] = self.final_output(self.A['post_metadata_features'])
        self.A['final_output'] = self.A['final_output'].view(self.A['final_output'].size(0), -1)

        self.loss = self.criterion(self.A['final_output'],target_torch)
        self.losses_to_average.append(self.extract('loss'))
        if len(self.losses_to_average) >= self.num_losses_to_average:
            #cy(self.num_losses_to_average,len(self.losses_to_average))
            self.losses.append( na(self.losses_to_average).mean() )
            self.losses_to_average = []
        return self.A['final_output']


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
                weights['net'][key] = weights['net'][key]#.cuda(device=0)
            if temp:
                torch.save(weights, opj(self.NETWORK_OUTPUT_FOLDER,'weights','temp.infer'))
                cb('. . . done saving temp.infer')
                return
            torch.save(weights, opj(self.NETWORK_OUTPUT_FOLDER,'weights','net'+'_'+time_str()+'.infer'))
            so(self.losses,opj(self.NETWORK_OUTPUT_FOLDER,'loss','net'+'_'+time_str()+'.loss_avg'))
            torch.save(self.optimizer.state_dict(), opj(self.NETWORK_OUTPUT_FOLDER,'optimizer','net'+'_'+time_str()+'.optimizer_state'))
            torch.save(self.state_dict(), opj(self.NETWORK_OUTPUT_FOLDER,'state_dict','net'+'_'+time_str()+'.state_dict'))
            print('. . . done saving.')
            self.save_net_timer.reset()


    def load(self):
        f = most_recent_file_in_folder(opj(self.NETWORK_OUTPUT_FOLDER,'weights'),['.infer'],[])
        #f = most_recent_file_in_folder(opj(self.NETWORK_OUTPUT_FOLDER,'state_dict'),['.state_dict'],[])
        #cm(f,ra=0)
        clp('Resuming with','`','',f,'','`--rb'); time.sleep(1)
        save_data = torch.load(f)
        self.load_state_dict(save_data['net'])

        f = most_recent_file_in_folder(opj(self.NETWORK_OUTPUT_FOLDER,'loss'),['.loss_avg.pkl'],[])
        self.losses = lo(f)


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


def make_batch(input_target_function,batch_size):
    input_batch = []
    meta_batch = []
    target_batch = []
    for i in range(batch_size):
        input_data,meta_data,target_data = input_target_function()
        input_batch.append(input_data)
        target_batch.append(target_data)
    return na(input_batch),None,na(target_batch)


"""
def load_net(path):
    save_data = torch.load(path)
    net = save_data['net']
    return net
"""

"""
_ = {}
_['NETWORK_OUTPUT_FOLDER'] = opjD('Temp')
_['save_net_timer'] = Timer(10)
_['SAVE_FILE_NAME'] = 'temp'
def save_net(N,temp=False):
    for f in ['weights','optimizer','state_dict','loss']:
        os.system(d2s('mkdir -p',opj(_['NETWORK_OUTPUT_FOLDER'],f)))
    if _['save_net_timer'].check() or temp:
        print('saving net state . . .')
        weights = {'net':N.state_dict().copy()}
        for key in weights['net']:
            weights['net'][key] = weights['net'][key]#.cuda(device=0)
        if temp:
            torch.save(weights, opj(_['NETWORK_OUTPUT_FOLDER'],'weights','temp.infer'))
            cb('. . . done saving temp.infer')
            return
        torch.save(weights, opj(_['NETWORK_OUTPUT_FOLDER'],'weights',_['SAVE_FILE_NAME']+'_'+time_str()+'.infer'))
        #so(_['LOSS_LIST_AVG'],opj(_['NETWORK_OUTPUT_FOLDER'],'loss',_['SAVE_FILE_NAME']+'_'+time_str()+'.loss_avg'))
        torch.save(N.optimizer.state_dict(), opj(_['NETWORK_OUTPUT_FOLDER'],'optimizer',_['SAVE_FILE_NAME']+'_'+time_str()+'.optimizer_state'))
        torch.save(N.state_dict(), opj(_['NETWORK_OUTPUT_FOLDER'],'state_dict',_['SAVE_FILE_NAME']+'_'+time_str()+'.state_dict'))
        print('. . . done saving.')
        _['save_net_timer'].reset()
"""

#EOF
