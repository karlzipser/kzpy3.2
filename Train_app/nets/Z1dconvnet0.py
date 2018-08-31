import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as initialization
from torch.autograd import Variable
from kzpy3.vis3 import *
clear_screen()

"""
        self.ip2 = nn.Linear(in_features=512, out_features=20)

        # Initialize weights
        nn.init.normal(self.conv1.weight, std=0.00001)
        nn.init.normal(self.conv2.weight, std=0.1)

        nn.init.xavier_normal(self.ip1.weight)
        nn.init.xavier_normal(self.ip2.weight)

    def forward(self, x, metadata):
        # conv1
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv1_pool(x)
        x = self.conv1_pool_norm(x)

        # metadata_concat
        x = torch.cat((metadata, x), 1)

        # conv2
        x = self.conv2_pool_norm(self.conv2_pool(F.relu(self.conv2(x))))
        
        x = x.view(-1, 2560)

        # ip1
        x = self.ip1_norm(F.relu(self.ip1(x)))

        # ip2
        x = self.ip2(x)
        
        return x
"""
if False:
    class Z1dconvnet0(nn.Module):
        def __init__(self):
            super(Z1dconvnet0, self).__init__
            self.lr = 0.1
            self.momentum = 0.1
            self.ip1 = nn.Linear(in_features=60, out_features=20)
            self.ip2 = nn.Linear(in_features=20, out_features=20)
            nn.init.xavier_normal(self.ip1.weight)
            nn.init.xavier_normal(self.ip2.weight)
            self.C={}
        def forward(self, x):
            self.C['input'] = x
            self.C['ip1'] = self.ip1(self.C['input'])
            self.C['ip1/relu'] = F.relu(self.C['ip1'])
            self.C['ip2'] = self.ip1(self.C['ip1/relu'])
            self.C['output'] = self.C['ip2']
            
            return self.C['output']


    def unit_test():
        Z = Z1dconvnet0()
        t = torch.randn(num_batches,8,60)
        Z.forward(Variable(t))
        pprint(Z.C)


    unit_test()
    #raw_enter()

if True:
    class Z1dconvnet0(nn.Module):
        def __init__(self):
            super(Z1dconvnet0, self).__init__()
            self.lr = 0.1
            self.momentum = 0.00000001
            i0=8
            i1=20
            i2=20
            i3=20
            self.conv1 = nn.Conv1d(in_channels=i0, out_channels=i1, kernel_size=6, stride=2, groups=1)
            self.conv2 = nn.Conv1d(in_channels=i1, out_channels=i2, kernel_size=6, stride=2, groups=1)
            self.conv3 = nn.Conv1d(in_channels=i2, out_channels=i3, kernel_size=6, stride=2, groups=1)
            self.ip1 = nn.Linear(in_features=80, out_features=20)
            self.ip2 = nn.Linear(in_features=20, out_features=20)
            nn.init.normal(self.conv1.weight, std=1.0)
            nn.init.normal(self.conv2.weight, std=1.0)
            nn.init.normal(self.conv3.weight, std=1.0)
            nn.init.normal(self.ip1.weight, std=1.0)
            #nn.init.normal(self.ip2.weight, std=1.0)
            #nn.init.xavier_normal(self.ip1.weight)
            #nn.init.xavier_normal(self.ip2.weight)
            self.C={}
        
        def forward(self, x):
            self.C['input'] = x
            self.C['conv1'] = self.conv1(self.C['input'])
            self.C['conv1/relu'] = F.relu(self.C['conv1'])
            self.C['conv2'] = self.conv2(self.C['conv1/relu'])
            self.C['conv2/relu'] = F.relu(self.C['conv2'])
            self.C['conv3'] = self.conv2(self.C['conv2/relu'])
            self.C['conv3/relu'] = F.relu(self.C['conv3'])
            #print self.C['conv3/relu'].size()
            #self.C['conv3/flat'] = self.C['conv3/relu'].view(self.C['conv3/relu'].size()[0],-1)
            self.C['conv3/flat'] = self.C['conv3/relu'].view(-1,80)
            self.C['ip1'] = self.ip1(self.C['conv3/flat'])
            #self.C['ip1/relu'] = F.relu(self.C['ip1'])
            #self.C['ip2'] = self.ip1(self.C['ip1/relu'])
            self.C['output'] = self.C['ip1']
            return self.C['output']


    def unit_test():
        Z = Z1dconvnet0()
        t = torch.randn(2,8,60)
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
            i0=8
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
            self.C['output'] = self.C['avg pool']
            return self.C['output']


    def unit_test():
        Z = Z1dconvnet0()
        t = torch.randn(2,8,60)
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