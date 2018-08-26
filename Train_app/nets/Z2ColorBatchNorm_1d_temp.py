import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as initialization
from torch.autograd import Variable
from kzpy3.utils2 import *
clear_screen()

P={}

class Z2ColorBatchNorm(nn.Module):
    def __init__(self):
        super(Z2ColorBatchNorm, self).__init__()

        self.lr = 0.1
        self.momentum = 0.1

        self.conv1 = nn.Conv1d(in_channels=1, out_channels=3, kernel_size=3, stride=1, groups=1)
        self.ip1 = nn.Linear(in_features=3, out_features=3)
        
        self.ip2 = nn.Linear(in_features=3, out_features=1)

        nn.init.normal_(self.conv1.weight, std=0.1)
        nn.init.xavier_normal_(self.ip1.weight)
        nn.init.xavier_normal_(self.ip2.weight)

    def forward(self, x):
        P['input'] = x.data.numpy()
        x = self.conv1(x)
        P['conv1'] = x.data.numpy()
        """
        x = F.relu(x)
        P['conv1/relu'] = x.data.numpy()
        x = x.view(-1, 3)
        P['x.view'] = x.data.numpy()
        x = F.relu(self.ip1(x))
        P['F.relu(self.ip1(x))'] = x.data.numpy()
        x = self.ip2(x)
        P['ip2'] = x.data.numpy()
        """
        return x


def unit_test():
    Z = Z2ColorBatchNorm()
    t = torch.randn(2,1,5)
    #print t
    print "----"
    Z.forward(t)#Variable(t))
    pprint(P)


unit_test()
