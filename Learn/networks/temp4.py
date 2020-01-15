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

        self.conv1=nn.Conv2d(in_channels=1,out_channels=1, kernel_size=4,stride=1, padding=0)
        nn.init.xavier_uniform(self.conv1.weight) #Xaviers Initialisation
        self.swish1= nn.ReLU()

        self.maxpool1= nn.MaxPool2d(kernel_size=2,return_indices=True)

        self.conv2 = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=5)
        nn.init.xavier_uniform(self.conv2.weight)
        self.swish2 = nn.ReLU()

        self.maxpool2 = nn.MaxPool2d(kernel_size=2,return_indices=True)

        self.conv3 = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3)
        nn.init.xavier_uniform(self.conv3.weight)
        self.swish3 = nn.ReLU()

        self.deconv1=nn.ConvTranspose2d(in_channels=1,out_channels=1,kernel_size=3)
        nn.init.xavier_uniform(self.deconv1.weight)
        self.swish4=nn.ReLU()

        self.maxunpool1=nn.MaxUnpool2d(kernel_size=2)

        self.deconv2=nn.ConvTranspose2d(in_channels=1,out_channels=1,kernel_size=5)
        nn.init.xavier_uniform(self.deconv2.weight)
        self.swish5=nn.ReLU()

        self.maxunpool2=nn.MaxUnpool2d(kernel_size=2)

        self.deconv3=nn.ConvTranspose2d(in_channels=1,out_channels=1,kernel_size=4)
        nn.init.xavier_uniform(self.deconv3.weight)
        self.swish6=nn.ReLU()

    def forward(self,x):
        kprint(x.size(),"x",ra=0)

        out=self.conv1(x)
        kprint(out.size(),"conv1",ra=0)

        out=self.swish1(out)
        
        size1 = out.size()
        out,indices1=self.maxpool1(out)
        kprint(out.size(),"maxpool1",ra=0)


        out=self.conv2(out)
        kprint(out.size(),"conv2",ra=0)

        out=self.swish2(out)
        size2 = out.size()
        out,indices2=self.maxpool2(out)
        kprint(out.size(),"maxpool2",ra=0)

        out=self.conv3(out)
        kprint(out.size(),"conv3",ra=0)

        out=self.swish3(out)

        out=self.deconv1(out)
        kprint(out.size(),"deconv1",ra=0)

        out=self.swish4(out)

        out=self.maxunpool1(out,indices2,size2)
        kprint(out.size(),"maxunpool1",ra=0)

        out=self.deconv2(out)
        kprint(out.size(),"deconv2",ra=0)

        out=self.swish5(out)
        out=self.maxunpool2(out,indices1,size1)
        kprint(out.size(),"maxunpool2",ra=0)

        out=self.deconv3(out)
        kprint(out.size(),"deconv3",ra=0)

        out=self.swish6(out)

        return True
    
N = ConDecon()
N(Variable(torch.randn(1, 1, 23, 41)))

#EOF