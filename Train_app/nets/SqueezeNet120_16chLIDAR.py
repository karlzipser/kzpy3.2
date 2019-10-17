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
            nn.Conv2d(6, 64, kernel_size=3, stride=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(64, 16, 64, 64),            
            )
        self.post_metadata_features = nn.Sequential(
            Fire(256, 16, 64, 64),
            nn.MaxPool2d(kernel_size=3, stride=1, ceil_mode=True),
            #nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            # Disabling the above MaxPool2d,
            # and optionally replacing it with a MaxPool2d of stride 1,
            # allows the lidar net to use almost the
            # same structure as the long-used zed net. Otherwise the vertical dimensions
            # go to zero.
            Fire(128, 32, 128, 128),
            Fire(256, 32, 128, 128),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(256, 48, 192, 192),
            Fire(384, 48, 192, 192),
            Fire(384, 64, 256, 256),
            Fire(512, 64, 256, 256),
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

def unit_test2():
    print("Running unit_test2...")
    S = SqueezeNet()
    i = Variable(torch.randn(5, 6, 64, 690))
    print i.size()
    cm(0)
    p = S.pre_metadata_features(i)
    cm(1)
    meta = Variable(torch.randn(5, 128, 15, 172))
    cm(2)
    m = torch.cat((p,meta),1)
    cm(3)
    po = S.post_metadata_features(m)
    f = S.final_output(po)
    cm(4)
    print("...done.")


#unit_test()
unit_test2()



