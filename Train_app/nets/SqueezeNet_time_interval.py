from kzpy3.utils3 import *
import math
import torch
import torch.nn as nn
import torch.nn.init as init
from torch.autograd import Variable
exec(identify_file_str)

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
        self.momentum = 0.001
        self.N_FRAMES = 1
        self.N_STEPS = 1
        self.features = nn.Sequential(
            Fire(6, 8, 16, 16),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(32, 16, 32, 32),
            Fire(64, 16, 32, 32),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(64, 24, 48, 48),
            Fire(96, 24, 48, 48),
            Fire(96, 32, 64, 64),
            Fire(128, 32, 64, 64),
        )
        final_conv = nn.Conv2d(128, 1, kernel_size=1)
        self.final_output = nn.Sequential(
            nn.Dropout(p=0.5),
            final_conv,
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


    def forward(self, x):
        self.A['ldr_input'] = x
        self.A['features'] = self.features(self.A['ldr_input'])
        self.A['final_output'] = self.final_output(self.A['features'])
        self.A['final_output'] = self.A['final_output'].view(self.A['final_output'].size(0), -1)
        return self.A['final_output']

#EOF
