import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as initialization
from torch.autograd import Variable
from kzpy3.vis2 import *
clear_screen()



class Z1dconvnet0(nn.Module):
    def __init__(self):
        super(Z1dconvnet0, self).__init__()
        self.lr = 0.1
        self.momentum = 0.1
        self.conv1 = nn.Conv1d(in_channels=12, out_channels=64, kernel_size=6, stride=2, groups=1)
        self.conv2 = nn.Conv1d(in_channels=64, out_channels=20, kernel_size=6, stride=2, groups=1)
        self.avg = nn.AvgPool1d(kernel_size=18, stride=19)
        nn.init.normal_(self.conv1.weight, std=1.0)
        nn.init.normal_(self.conv2.weight, std=1.0)
        self.P={}
    def forward(self, x):
        P = self.P
        P['input'] = x.data.numpy()
        x = self.conv1(x)
        P['conv1'] = x.data.numpy()
        x = F.relu(x)
        P['conv1_relu'] = x.data.numpy()
        x = self.conv2(x)
        P['conv2'] = x.data.numpy()
        x = F.relu(x)
        P['conv2_relu'] = x.data.numpy()
        x = self.avg(x)
        P['avg'] = x.data.numpy()
        x = F.relu(x)
        P['avg_relu'] = x.data.numpy()
        if False:
            mi(P['conv1'][0],'conv1-0')
            mi(P['conv1'][1],'conv1-1')
            mi(P['conv2'][0],'conv2-0')
            mi(P['conv2'][1],'conv2-1')
            mi(P['avg'][0],'avg-0')
            mi(P['avg'][1],'avg-1')
        return x


def unit_test():
    Z = Z1dconvnet0()
    t = torch.randn(2,12,150)
    Z.forward(Variable(t))
    pprint(Z.P)


#unit_test()
#raw_enter()