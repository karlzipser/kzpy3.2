from kzpy3.utils3 import *
exec(identify_file_str)

import math
import torch
import torch.nn as nn
import torch.nn.init as init
from torch.autograd import Variable

class Fire(nn.Module):

    def __init__(self, inplanes, squeeze_planes,
                 expand1x1_planes, expand3x3_planes,name='',A=False):
        self.A = A
        self.name = name
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
        if type(self.A) != type(False):
            self.A[d2p(self.name,'squeeze_activation')] = x
        return torch.cat([
            self.expand1x1_activation(self.expand1x1(x)),
            self.expand3x3_activation(self.expand3x3(x))
        ], 1)


class SqueezeNet(nn.Module):

    def __init__(self):
        super(SqueezeNet, self).__init__()
        self.A = {}
        self.lr = 0.01
        self.momentum = 0.001 #0.0001
        self.N_FRAMES = 2
        self.N_STEPS = 10
        self.pre_metadata_features = nn.Sequential(
            nn.Conv2d(12, 64, kernel_size=3, stride=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(64, 16, 64, 64,'Fire0',self.A),            
            )
        self.post_metadata_features = nn.Sequential(
            Fire(256, 16, 64, 64,'Fire1',self.A),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(128, 32, 128, 128,'Fire2',self.A),
            Fire(256, 32, 128, 128,'Fire3',self.A),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(256, 48, 192, 192,'Fire4',self.A),
            Fire(384, 48, 192, 192,'Fire5',self.A),
            Fire(384, 64, 256, 256,'Fire6',self.A),
            Fire(512, 64, 256, 256,'Fire7',self.A),
        )
        final_conv = nn.Conv2d(512, 120, kernel_size=1)
        self.final_output = nn.Sequential(
            nn.Dropout(p=0.5),
            final_conv,
            # nn.ReLU(inplace=True), # this allows initial training to recover from zeros in output
            nn.AvgPool2d(kernel_size=5, stride=6)
            #nn.AdaptiveAvgPool2d(1)#kernel_size=5, stride=6)
        )

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                if m is final_conv:
                    init.normal(m.weight.data, mean=0.0, std=0.01)
                else:
                    init.kaiming_uniform(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()


    def forward(self, x, metadata):
        self.A['camera_input'] = x
        self.A['pre_metadata_features'] = self.pre_metadata_features(self.A['camera_input'])
        self.A['pre_metadata_features_metadata'] = torch.cat((self.A['pre_metadata_features'], metadata), 1)
        self.A['post_metadata_features'] = self.post_metadata_features(self.A['pre_metadata_features_metadata'])
        self.A['final_output'] = self.final_output(self.A['post_metadata_features'])
        self.A['final_output'] = self.A['final_output'].view(self.A['final_output'].size(0), -1)
        return self.A['final_output']


#def unit_test():
S = SqueezeNet()
a = S(Variable(torch.randn(64, 12, 94, 168)), Variable(torch.randn(64, 128, 23, 41)))    
print('Tested SqueezeNet')
for a in sorted(S.A.keys()):
    kprint(S.A[a].size(),title=a)
    #raw_enter()
#print S.A['Fire1.squeeze_activation'].size()

#unit_test()
