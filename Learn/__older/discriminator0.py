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


#_dataset = 'mnist'
#_dataroot = ''
_workers=2
_batchSize=1
_imageSize = 64
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
_outf='.'
_manualSeed=None
_classes='bedroom'
nc=3

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






###########################################################################
#
class Generator(nn.Module):
    def __init__(self, ngpu):
        super(Generator, self).__init__()
        self.ngpu = ngpu
        self.main = nn.Sequential(
            # input is Z, going into a convolution
            nn.ConvTranspose2d(     nz, ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),
            # state size. (ngf*8) x 4 x 4

            #nn.Upsample(size=(8,8), mode='nearest'),

            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
            # state size. (ngf*4) x 8 x 8
            nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
            # state size. (ngf*2) x 16 x 16
            nn.ConvTranspose2d(ngf * 2,     ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),


            ####
            #nn.ConvTranspose2d(ngf * 1,     ngf, 4, 2, 1, bias=False),
            #nn.BatchNorm2d(ngf),
            #nn.ReLU(True),
            ####


            # state size. (ngf) x 32 x 32
            nn.ConvTranspose2d(    ngf,      nc, 4, 2, 1, bias=False),
            nn.Tanh(),
            # state size. (nc) x 64 x 64            
        )

    def forward(self, input):
        if input.is_cuda and self.ngpu > 1:
            output = nn.parallel.data_parallel(self.main, input, range(self.ngpu))
        else:
            output = self.main(input)
        #output = torch.nn.functional.interpolate(output,size=(64,64))#,mode='linear')
        return output
#
###########################################################################



GENERATOR = Generator(ngpu).cuda()#to(device)
GENERATOR.apply(weights_init)
if _GENERATOR != '':
    GENERATOR.load_state_dict(torch.load(_GENERATOR))




###########################################################################
#
class Discriminator(nn.Module):
    def __init__(self, ngpu):
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




DISCRIMINATOR = Discriminator(ngpu).cuda()#.to(device)
DISCRIMINATOR.apply(weights_init)
if _DISCRIMINATOR != '':
    DISCRIMINATOR.load_state_dict(torch.load(_DISCRIMINATOR))
criterion = nn.BCELoss()
fixed_noise = torch.randn(_batchSize, nz, 1, 1,).cuda()# device=device)
real_label = 1
fake_label = 0


optimizerD = optim.Adam(DISCRIMINATOR.parameters(), lr=_lr, betas=(_beta1, 0.999))

optimizerG = optim.Adam(GENERATOR.parameters(), lr=_lr, betas=(_beta1, 0.999))


if False:

    losses = []
    loss_avg = []
    A = h5r('/home/karlzipser/Desktop/Data/1_TB_Samsung_n1/left_direct_stop__31Oct_to_1Nov2018/locations/local/left_direct_stop/h5py/tegra-ubuntu_01Nov18_13h09m32s/flip_images.h5py' )
    print_timer = Timer(1)
    loss_timer = Timer(10)
    CA()





    epoch = 0

    for i in range(_niter):
        if True:#try:
            ############################
            # (1) Update D network: maximize log(D(x)) + log(1 - D(G(z)))
            ###########################
            # train with real

            #A
            DISCRIMINATOR.zero_grad() #!
            q = rndint(len(A['left_image_flip']['vals']))
            real_cpu = torch.zeros(1,1,64,64).cuda() #2
            real_cpu[0,0,:,:] = torch.from_numpy(cv2.resize(A['left_image_flip']['vals'][q,:,:,1],(64,64))).cuda()#.to(device)
            batch_size = real_cpu.size(0)
            label = torch.full((batch_size,), real_label,).cuda()# device=device) #3
            output = DISCRIMINATOR(real_cpu) #4
            errD_real = criterion(output, label) #5
            errD_real.backward() #6
            D_x = output.mean().item() #7

            # train with fake
            noise = torch.randn(batch_size, nz, 1, 1,).cuda()# device=device)
            fake = GENERATOR(noise) #8
            label.fill_(fake_label) #9
            output = DISCRIMINATOR(fake.detach()) #10
            errD_fake = criterion(output, label) #11
            errD_fake.backward() #12
            D_G_z1 = output.mean().item() #13
            errD = errD_real + errD_fake #14
            optimizerD.step() #15

            ############################
            # (2) Update G network: maximize log(D(G(z)))
            ###########################
            GENERATOR.zero_grad() #16
            label.fill_(real_label)  #17 # fake labels are real for generator cost
            output = DISCRIMINATOR(fake) #18
            errG = criterion(output, label) #19
            errG.backward() #20
            D_G_z2 = output.mean().item()
            optimizerG.step() #21

            loss_avg.append(errD.item())

            if print_timer.check():
                print_timer.reset()   
                
                losses.append(na(loss_avg).mean())
                
                if loss_timer.check():
                    loss_timer.reset()
                    figure('loss')
                    clf()
                    plot(losses,'.')
                    spause()
                    loss_avg = []

                if True:
                    fake = GENERATOR(fixed_noise)
                    f = z55(fake.data.cpu().numpy()[rndint(1),0,:,:])
                    r = z55(real_cpu.data.cpu().numpy()[0,0,:,:])

                    timer = Timer()
                    mci(r,title='real',scale=5)
                    mci(f,title='fake',scale=5)
                    
                    




    for i in range(10000,99999):
        mci(A['left_image_flip']['vals'][i,:,:,1])
        print(i)
