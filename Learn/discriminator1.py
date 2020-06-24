#from __future__ import print_function
from kzpy3.vis3 import *
import argparse
import os
import random
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim as optim
import torch.utils.data
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torchvision.utils as vutils

_nz=100
_ngf=64
_ndf=64*2
_niter=9999999
_lr=0.01
_beta1=0.5
_cuda=True
_ngpu=1
_GENERATOR=''
_DISCRIMINATOR=''

ngpu = int(_ngpu)
nz = int(_nz)
ngf = int(_ngf)
ndf = int(_ndf)


# custom weights initialization called on GENERATOR and DISCRIMINATOR

def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)



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


class Discriminator(nn.Module):

    def __init__(self,nc=3):
        super(Discriminator, self).__init__()
        self.A = {}
        self.lr = 0.01
        self.momentum = 0.001 #0.0001
        self.N_FRAMES = 2
        self.N_STEPS = 10
        self.pre_metadata_features = nn.Sequential(
            nn.Conv2d(nc, 64, kernel_size=3, stride=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(64, 16, 64, 64),            
            )
        self.post_metadata_features = nn.Sequential(
            Fire(128, 16, 64, 64),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(128, 32, 128, 128),
            Fire(256, 32, 128, 128),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(256, 48, 192, 192),
            Fire(384, 48, 192, 192),
            Fire(384, 64, 256, 256),
            Fire(512, 64, 256, 256),
        )
        final_conv = nn.Conv2d(512, 1, kernel_size=1)
        self.final_output = nn.Sequential(
            nn.Dropout(p=0.5),
            final_conv,
            # nn.ReLU(inplace=True), # this allows initial training to recover from zeros in output
            nn.AvgPool2d(kernel_size=5, stride=6),
            #nn.AdaptiveAvgPool2d(1)#kernel_size=5, stride=6)
            nn.Sigmoid()
        )

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                if m is final_conv:
                    init.normal(m.weight.data, mean=0.0, std=0.01)
                else:
                    init.kaiming_uniform(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()

    #self.timer = Timer(2)
    def forward(self, x):
        self.A['camera_input'] = x
        self.A['pre_metadata_features'] = self.pre_metadata_features(self.A['camera_input'])
        #self.A['pre_metadata_features_metadata'] = torch.cat((self.A['pre_metadata_features'], metadata), 1)
        self.A['post_metadata_features'] = self.post_metadata_features(self.A['pre_metadata_features'])
        self.A['final_output'] = self.final_output(self.A['post_metadata_features'])
        self.A['final_output'] = self.A['final_output'].view(self.A['final_output'].size(0), -1)
        #self.A['final_output'] = self.A['final_output'].view(-1, 1).squeeze(1)
        #print self.A['final_output'].size()
        return self.A['final_output'].view(-1, 1).squeeze(1)



    def save(self,NETWORK_OUTPUT_FOLDER):
        if True:
            for f in ['weights','optimizer','state_dict','loss']:
                os.system(d2s('mkdir -p',opj(NETWORK_OUTPUT_FOLDER,f)))
            print('saving net state . . .')
            weights = {'net':self.state_dict().copy()}
            for key in weights['net']:
                if True:#self.GPU > -1:
                    weights['net'][key] = weights['net'][key].cuda()#(device=self.GPU)
                else:
                    weights['net'][key] = weights['net'][key]
            net_str = 'net'+'_'+time_str()#+'.'+str(self.losses[-1])
            if True:#self.GPU > -1:
                net_str = net_str+'.cuda'
            torch.save(weights, opj(NETWORK_OUTPUT_FOLDER,'weights',net_str+'.infer'))
            #so(self.losses,opj(NETWORK_OUTPUT_FOLDER,'loss',net_str+'.loss_avg'))
            #torch.save(self.optimizer.state_dict(), opj(NETWORK_OUTPUT_FOLDER,'optimizer',net_str+'.optimizer_state'))
            torch.save(self.state_dict(), opj(NETWORK_OUTPUT_FOLDER,'state_dict',net_str+'.state_dict'))
            print('. . . done saving.')
            #self.save_net_timer.reset()



    def load(self,NETWORK_OUTPUT_FOLDER):
        print NETWORK_OUTPUT_FOLDER
        clp(opj(NETWORK_OUTPUT_FOLDER,'weights'))
        f = most_recent_file_in_folder(opj(NETWORK_OUTPUT_FOLDER,'weights'),['.infer'],[])
        clp('Resuming with','`','',f,'','`--rb'); time.sleep(1)
        save_data = torch.load(f)
        self.load_state_dict(save_data['net'])

        #f = most_recent_file_in_folder(opj(NETWORK_OUTPUT_FOLDER,'loss'),['.loss_avg.pkl'],[])
        #self.losses = lo(f)



###########################################################################
#
class DDDDiscriminator(nn.Module):
    def __init__(self, ngpu=1):
        super(Discriminator, self).__init__()
        self.ctr = 0
        self.ngpu = ngpu
        self.main0 = nn.Sequential(
            # input is (nc) x 64 x 64
            nn.Conv2d(nc, ndf, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf) x 32 x 32
            nn.Conv2d(ndf, ndf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*2) x 16 x 16
            nn.Conv2d(ndf * 2, ndf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*4) x 8 x 8
        )

        self.main1 = nn.Sequential(

            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),

            nn.Conv2d(ndf * 4, ndf * 8, 4, 2, 1, bias=False),


            nn.BatchNorm2d(ndf * 8),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*8) x 4 x 4

            nn.Conv2d(ndf*8, 1, 2, 1, 0, bias=False),

            nn.Sigmoid()
        )

    def forward(self, x):
        x = torch.nn.functional.interpolate(x,size=(64,64))
        #print 'x',x.size()
        #mi(z55(x.data.cpu().numpy()[0,:,:,:].transpose(2,1,0)),self.ctr);spause()
        if self.ctr:
            self.ctr = 0
        else:
            self.ctr = 1
        x = self.main0(x)
        x = self.main1(x)

        return x.view(-1, 1).squeeze(1)
#
###########################################################################


