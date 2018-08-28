import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as initialization
from torch.autograd import Variable
from kzpy3.vis3 import *
clear_screen()



class Z1dconvnet0(nn.Module):
    def __init__(self):
        super(Z1dconvnet0, self).__init__()
        self.lr = 0.1
        self.momentum = 0.1
        i0=12
        i1=20
        i2=20
        i3=20
        self.conv1 = nn.Conv1d(in_channels=i0, out_channels=i1, kernel_size=6, stride=2, groups=1)
        self.conv2 = nn.Conv1d(in_channels=i1, out_channels=i2, kernel_size=6, stride=2, groups=1)
        self.conv3 = nn.Conv1d(in_channels=i2, out_channels=i3, kernel_size=6, stride=2, groups=1)
        #self.conv4 = nn.Conv1d(in_channels=i2, out_channels=i3, kernel_size=6, stride=2, groups=1)
        self.avg = nn.AvgPool1d(kernel_size=4, stride=1)
        nn.init.normal(self.conv1.weight, std=1.0)
        nn.init.normal(self.conv2.weight, std=10.0)
        nn.init.normal(self.conv3.weight, std=10.0)
        #nn.init.normal(self.conv4.weight, std=1.0)

        self.C={}
    def forward(self, x):
        self.C['input'] = x
        self.C['conv1'] = self.conv1(self.C['input'])
        self.C['conv1/relu'] = F.relu(self.C['conv1'])
        self.C['conv2'] = self.conv2(self.C['conv1/relu'])
        self.C['conv2/relu'] = F.relu(self.C['conv2'])
        self.C['conv3'] = self.conv2(self.C['conv2/relu'])
        self.C['conv3/relu'] = F.relu(self.C['conv3'])
        #self.C['conv4'] = self.conv2(self.C['conv3/relu'])
        self.C['avg pool'] = self.avg(self.C['conv3']) 
        return self.C['avg pool']


def unit_test():
    Z = Z1dconvnet0()
    t = torch.randn(2,12,60)
    Z.forward(Variable(t))
    pprint(Z.C)


unit_test()
#raw_enter()


if False:

    class Z1dconvnet0(nn.Module):
        def __init__(self):
            super(Z1dconvnet0, self).__init__()
            self.lr = 0.1
            self.momentum = 0.1
            i0=12
            i1=20
            i2=20
            i3=20
            self.conv1 = nn.Conv1d(in_channels=i0, out_channels=i1, kernel_size=6, stride=2, groups=1)
            self.conv2 = nn.Conv1d(in_channels=i1, out_channels=i2, kernel_size=6, stride=2, groups=1)
            self.conv3 = nn.Conv1d(in_channels=i2, out_channels=i3, kernel_size=63, stride=24, groups=1)
            self.avg = nn.AvgPool1d(kernel_size=15, stride=15)
            nn.init.normal(self.conv1.weight, std=1.0)
            nn.init.normal(self.conv2.weight, std=10.0)
            nn.init.normal(self.conv3.weight, std=10.0)
            self.C={}
        def forward(self, x):
            self.C['input'] = x
            self.C['conv1'] = self.conv1(self.C['input'])
            self.C['conv1/relu'] = F.relu(self.C['conv1'])
            self.C['conv2'] = self.conv2(self.C['conv1/relu'])
            self.C['conv2/relu'] = F.relu(self.C['conv2'])
            self.C['conv3'] = self.conv2(self.C['conv2/relu'])
            self.C['avg pool'] = self.avg(self.C['conv3']) 
            return self.C['avg pool']


    def unit_test():
        Z = Z1dconvnet0()
        t = torch.randn(2,12,150)
        Z.forward(Variable(t))
        pprint(Z.C)


    unit_test()
    #raw_enter()