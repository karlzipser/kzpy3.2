from kzpy3.utils3 import *
import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.utils as nnutils
exec(identify_file_str)






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

        self.optimizer = torch.optim.Adadelta(filter(lambda p: p.requires_grad,self.parameters()))
        self.loss = None
        self.losses = previous_losses
        self.num_losses_to_average = NUM_LOSSES_TO_AVERAGE
        self.losses_to_average = []
        self.save_net_timer = Timer(NET_SAVE_TIMER_TIME)


    def forward(self,input_torch,meta_data_torch,target_torch):
        cm(0)
        self.optimizer.zero_grad()
        cm(1)
        self.A['camera_input'] = input_torch
        cm(2)
        self.A['pre_metadata_features'] = self.pre_metadata_features(
                input_torch
            )
        #self.A['camera_input'])
        cm(3)
        self.A['pre_metadata_features_metadata'] = self.A['pre_metadata_features']

        self.A['post_metadata_features'] = self.post_metadata_features(self.A['pre_metadata_features_metadata'])
        self.A['final_output'] = self.final_output(self.A['post_metadata_features'])
        self.A['final_output'] = self.A['final_output'].view(self.A['final_output'].size(0), -1)

        self.loss = self.criterion(self.A['final_output'],target_torch)
        self.losses_to_average.append(self.extract('loss'))
        if len(self.losses_to_average) >= self.num_losses_to_average:
            self.losses.append( na(self.losses_to_average).mean() )
            self.losses_to_average = []
        return self.A['final_output']


    def backward(self):
        cm(15)
        self.loss.backward()
        nnutils.clip_grad_norm(self.parameters(), 1.0)
        self.optimizer.step()


    def extract(self,layer_name,batch_number=0):
        cm(10)
        if layer_name == 'loss':
            return self.loss.data.cpu().numpy()
        else:
            return self.A[layer_name][batch_number,:].data.cpu().numpy()





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










#EOF
