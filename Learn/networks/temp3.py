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
        self.conv1b=        nn.Conv2d(in_channels=1,out_channels=1, kernel_size=1,stride=1, padding=0)

        self.maxpool1= nn.MaxPool2d(kernel_size=3,stride=2,return_indices=True,padding=0)

        self.deconv1=nn.ConvTranspose2d(in_channels=1,out_channels=1,kernel_size=3,stride=1,padding=0)
        self.deconv1b=nn.ConvTranspose2d(in_channels=1,out_channels=1,kernel_size=1,stride=1,padding=0)

        self.maxunpool1=nn.MaxUnpool2d(kernel_size=3,stride=2,padding=0)


    def forward(self,x):
        kprint(x.size(),"x",ra=0)
        size1 = x.size()

        out=self.conv1(x)
        outb = self.conv1b(x)
        kprint(out.size(),"conv1",ra=0)
        kprint(outb.size(),"conv1b",ra=0)

        out,indices1=self.maxpool1(out)
        kprint(out.size(),"maxpool1",ra=0)



        out=self.maxunpool1(out,indices1,size1)
        kprint(out.size(),"maxunpool1",ra=0)


        out=self.deconv1(out)
        outb=self.deconv1b(out)
        kprint(out.size(),"deconv1",ra=0)
        kprint(outb.size(),"deconv1b",ra=0)


        return True#out

    
N = ConDecon()
N(Variable(torch.randn(1, 1, 94, 168)))

#EOF