from kzpy3.utils3 import *
exec(identify_file_str)

import math
import torch
import torch.nn as nn
import torch.nn.init as init
from torch.autograd import Variable

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


class SqueezeNet(nn.Module):

    def __init__(self):
        super(SqueezeNet, self).__init__()
        self.A = {}
        self.lr = 0.01
        self.momentum = 0.001 #0.0001
        self.N_FRAMES = 2
        self.N_STEPS = 10
        self.pre_metadata_features = nn.Sequential(
            nn.Conv2d(3, 6, kernel_size=3, stride=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(6, 3, 3, 3),            
            )
        self.post_metadata_features = nn.Sequential(
            Fire(6, 3, 3, 3),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(6, 4, 8, 8),
        )
        final_conv = nn.Conv2d(16, 1024, kernel_size=1)

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


    def forward(self, x):
        #cm(1)
        self.A['camera_input'] = x
        #cm(2)
        self.A['pre_metadata_features'] = self.pre_metadata_features(self.A['camera_input'])
        #cm(3)
        self.A['post_metadata_features'] = self.post_metadata_features(self.A['pre_metadata_features'])
        #cm(4)
        self.A['final_output'] = self.final_output(self.A['post_metadata_features'])
        #cm(5)
        self.A['final_output'] = self.A['final_output'].view(self.A['final_output'].size(0), -1)
        #cm(6)
        #print "self.A['final_output']",self.A['final_output'].size()
        return self.A['final_output']


#EOF
