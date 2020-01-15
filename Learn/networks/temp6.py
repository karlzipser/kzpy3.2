# https://github.com/pgtgrly/Convolution-Deconvolution-Network-Pytorch/blob/master/Neural_Network_Class.py

from kzpy3.utils3 import *
import math
import torch
import torch.nn as nn
import torch.nn.init as init
from torch.autograd import Variable

class ConDecon(nn.Module):

    def __init__(self):
        super(ConDecon, self).__init__()

        self.A = {}

        self.conv1=         nn.Conv2d(in_channels=1,out_channels=1, kernel_size=3,stride=1, padding=1)

        self.conv2=         nn.Conv2d(in_channels=1,out_channels=1, kernel_size=3,stride=1, padding=1)

        self.maxpool1= nn.MaxPool2d(kernel_size=3,stride=2,return_indices=True,padding=0)

        self.deconv1=nn.ConvTranspose2d(in_channels=1,out_channels=1,kernel_size=3,stride=1,padding=1)

        self.deconv2=nn.ConvTranspose2d(in_channels=1,out_channels=1,kernel_size=3,stride=1,padding=1)

        self.maxunpool1=nn.MaxUnpool2d(kernel_size=3,stride=2,padding=0)


    def forward(self,x):

        kprint(x.size(),"x",ra=0)
        size1 = x.size()

        x=self.conv1(x)
        kprint(x.size(),"conv1",ra=0)

        x,indices1=self.maxpool1(x)
        kprint(x.size(),"maxpool1",ra=0)

        x=self.conv2(x)
        kprint(x.size(),"conv2",ra=0)

        x=self.deconv2(x)
        kprint(x.size(),"deconv2",ra=0)


        x=self.maxunpool1(x,indices1,size1)
        kprint(x.size(),"maxunpool1",ra=0)


        x=self.deconv1(x)
        kprint(x.size(),"deconv1",ra=0)


        return True#x

    
N = ConDecon()
N(Variable(torch.randn(1, 1, 94, 168)))

#EOF