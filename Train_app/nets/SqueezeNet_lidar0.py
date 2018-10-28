from kzpy3.utils3 import *
exec(identify_file_str)
spd2s('Using SqueezeNet !!!!!!!!!!!!!!!!!!')
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
            nn.Conv2d(3, 64, kernel_size=3, stride=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(64, 16, 64, 64),            
            )

        final_conv = nn.Conv2d(256, self.N_STEPS * 2, kernel_size=3,stride=2)
        self.post_metadata_features = nn.Sequential(
            nn.Dropout(p=0.5),
            final_conv,
            nn.ReLU(inplace=True)
        )

        self.final_output = nn.Sequential(
            nn.AdaptiveAvgPool2d(1)
        )

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                if m is self.post_metadata_features:
                    init.normal(m.weight.data, mean=0.0, std=0.01)
                else:
                    init.kaiming_uniform(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()


    def forward(self, x, metadata):

        self.A['camera_input'] = x
        print self.A['camera_input']
        raw_enter('camera_input: ' )

        self.A['pre_metadata_features'] = self.pre_metadata_features(self.A['camera_input'])
        print self.A['pre_metadata_features']
        raw_enter('pre_metadata_features: ')

        self.A['pre_metadata_features_metadata'] = torch.cat((self.A['pre_metadata_features'], metadata), 1)
        print self.A['pre_metadata_features_metadata'] 
        raw_enter('pre_metadata_features_metadata: ')

        self.A['post_metadata_features'] = self.post_metadata_features(self.A['pre_metadata_features_metadata'])
        print self.A['post_metadata_features'] 
        raw_enter('post_metadata_features: ')

        self.A['final_output'] = self.final_output(self.A['post_metadata_features'])
        print self.A['final_output'] 
        raw_enter('final_output: ')

        return self.A['final_output']

def unit_test():
    spd2s('not running unit test because it affects stuff')
    return
    test_net = SqueezeNet()
    a = test_net(Variable(torch.randn(5, 12, 94, 168)), Variable(torch.randn(5, 128, 23, 41)))    
    print('Tested SqueezeNet')

unit_test()
