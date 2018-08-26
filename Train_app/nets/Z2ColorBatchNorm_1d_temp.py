import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as initialization
from torch.autograd import Variable


class Z2ColorBatchNorm(nn.Module):
    def __init__(self):
        super(Z2ColorBatchNorm, self).__init__()

        self.lr = 0.1
        self.momentum = 0.1
        self.N_FRAMES = 2
        self.N_STEPS = 10

        self.conv1 = nn.Conv1d(in_channels=10, out_channels=1, kernel_size=1, stride=1, groups=1)
        #self.conv1_pool = nn.MaxPool1d(kernel_size=1, stride=1) 
        #self.conv1_pool_norm = nn.BatchNorm2d(1)

        self.ip1 = nn.Linear(in_features=1, out_features=1)
        self.ip1_norm = nn.BatchNorm1d(1)
        self.ip2 = nn.Linear(in_features=1, out_features=1)

        # Initialize weights
        nn.init.normal(self.conv1.weight, std=0.00001)

        nn.init.xavier_normal(self.ip1.weight)

    def forward(self, x):
        # conv1
        x = self.conv1(x)
        x = F.relu(x)
        #x = self.conv1_pool(x)
        #x = self.conv1_pool_norm(x)

        # metadata_concat
        #x = torch.cat((metadata, x), 1)

        # conv2
        #x = self.conv2_pool_norm(self.conv2_pool(F.relu(self.conv2(x))))
        
        #x = x.view(-1, 2560)

        # ip1
        x = self.ip1_norm(F.relu(self.ip1(x)))

        # ip2
        x = self.ip2(x)
        
        return x


def unit_test():
    test_net = Z2ColorBatchNorm()
    print test_net.forward(Variable(torch.randn(2,10,1)))
    #a = test_net(Variable(torch.randn(10,1,1)), Variable(torch.randn(1,1,1)))
    #print (a)


unit_test()
