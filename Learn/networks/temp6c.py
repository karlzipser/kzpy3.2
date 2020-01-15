# https://github.com/pgtgrly/Convolution-Deconvolution-Network-Pytorch/blob/master/Neural_Network_Class.py

from kzpy3.utils3 import *
import math
import torch
import torch.nn as nn
import torch.nn.init as init
from torch.autograd import Variable






class Fire(nn.Module):
    def __init__(
        self,
        inplanes,
        squeeze_planes,
        expand1x1_planes,
        expand3x3_planes
    ):
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

class Smoke(nn.Module):
    def __init__(
        self,
        inplanes,
        squeeze_planes,
        expand1x1_planes,
        expand3x3_planes
    ):
        super(Smoke, self).__init__()
        self.inplanes = inplanes
        self.squeeze = nn.ConvTranspose2d(inplanes, squeeze_planes, kernel_size=1)
        self.squeeze_activation = nn.ReLU(inplace=True)
        self.expand1x1 = nn.ConvTranspose2d(squeeze_planes, expand1x1_planes,
                                   kernel_size=1)
        self.expand1x1_activation = nn.ReLU(inplace=True)
        self.expand3x3 = nn.ConvTranspose2d(squeeze_planes, expand3x3_planes,
                                   kernel_size=3, padding=1)
        self.expand3x3_activation = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.squeeze_activation(self.squeeze(x))
        return torch.cat([
            self.expand1x1_activation(self.expand1x1(x)),
            self.expand3x3_activation(self.expand3x3(x))
        ], 1)




class ConDecon(nn.Module):

    def __init__(self):
        super(ConDecon, self).__init__()

        self.A = {}

        self.fire1=Fire(2,1,1,1)
        self.fire2=Fire(2,1,1,1)
        self.fire3=Fire(2,1,1,1)

        self.maxpool1= nn.MaxPool2d(kernel_size=3,stride=2,return_indices=True,padding=0)
        self.maxpool2= nn.MaxPool2d(kernel_size=3,stride=2,return_indices=True,padding=0)

        self.smoke1=Smoke(2,1,1,1)
        self.smoke2=Smoke(2,1,1,1)
        self.smoke3=Smoke(2,1,1,1)

        self.maxunpool_size_fire1=nn.MaxUnpool2d(kernel_size=3,stride=2,padding=0)
        self.maxunpool_size_fire2=nn.MaxUnpool2d(kernel_size=3,stride=2,padding=0)


    def forward(self,x):

        kprint(x.size(),"x",ra=0)

        x=self.fire1(x)
        kprint(x.size(),"fire1",ra=0)
        size_fire1 = x.size()

        x,indices_fire1=self.maxpool1(x)
        kprint(x.size(),"maxpool1",ra=0)

        x=self.fire2(x)
        kprint(x.size(),"fire2",ra=0)
        size_fire2 = x.size()



        

        x,indices_fire2=self.maxpool2(x)
        kprint(x.size(),"maxpool2",ra=0)

        x=self.fire3(x)
        kprint(x.size(),"fire3",ra=0)
        size_fire3 = x.size()


        


        x=self.smoke3(x)
        kprint(x.size(),"smoke3",ra=0)

        
        x=self.maxunpool_size_fire2(x,indices_fire2,size_fire2)
        kprint(x.size(),"maxunpool2",ra=0)


        




        x=self.smoke2(x)
        kprint(x.size(),"smoke2",ra=0)


        x=self.maxunpool_size_fire1(x,indices_fire1,size_fire1)
        kprint(x.size(),"maxunpool1",ra=0)


        x=self.smoke1(x)
        kprint(x.size(),"smoke1",ra=0)


        return True#x

    
N = ConDecon()
#N(Variable(torch.randn(1, 2, 94, 168)))
#N(Variable(torch.randn(1, 2, 47, 84)))
N(Variable(torch.randn(1, 2, 23, 41)))

#EOF