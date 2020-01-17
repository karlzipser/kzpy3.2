# https://github.com/pgtgrly/Convolution-Deconvolution-Network-Pytorch/blob/master/Neural_Network_Class.py

from net import *
exec(identify_file_str)

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

aa = 8
a = 16
b = 32
c = 64
d = 128
e = 256
f = 512
rgb = 3




class ConDecon_FS(Net):

    def setup_layers(self,P):
        #super(ConDecon_FS, self).__init__()
        self.A = {}

        self.fire1=Fire(P['NUM_INPUT_CHANNELS'],aa,b,b)
        #self.sq1=Squeeze(P['NUM_INPUT_CHANNELS'],aa,b,b)
        #self.ex1=Expand(P['NUM_INPUT_CHANNELS'],aa,b,b)

        self.fire2=Fire(c,a,c,c)
        #self.sq2=Fire(c,a,c,c)
        #self.ex2=Fire(c,a,c,c)

        self.fire3=Fire(d,b,d,d)
        #self.sq3=Fire(d,b,d,d)
        #self.ex3=Fire(d,b,d,d)

        #self.fire4=Fire(e,c,e,e)

        self.maxpool= nn.MaxPool2d(kernel_size=3,stride=2,return_indices=True,padding=0)

        #self.smoke4=Smoke(f,c,d,d)
        self.smoke3=Smoke(e+e,b,c,c)
        self.smoke2=Smoke(d+d,a,b,b)
        self.smoke1=Smoke(c+c,aa,a,a)

        self.maxunpool=nn.MaxUnpool2d(kernel_size=3,stride=2,padding=0)

        self.final_deconv = nn.ConvTranspose2d(2*a, P['NUM_OUTPUTS'], kernel_size=1)
        self.swish6=nn.ReLU()

    def forward(self,Data):

        self.optimizer.zero_grad()
        Torch_data = self.data_to_torch(Data)
        self.A['input'] = Torch_data['input']
        x = self.A['input']

        #kprint(x.size(),"x",ra=0)

        x=self.fire1(x)
        f1 = x
        #x=self.sq1(x)
        #x=self.ex1(x)
        #kprint(x.size(),"fire1",ra=0)
        size_fire1 = x.size()

        x,indices_fire1=self.maxpool(x)
        #kprint(x.size(),"maxpool",ra=0)

        x=self.fire2(x)
        f2 = x
        #kprint(x.size(),"fire2",ra=0)
        #x=self.sq2(x)
        #x=self.ex2(x)
        size_fire2 = x.size()

        x,indices_fire2=self.maxpool(x)
        #kprint(x.size(),"maxpool",ra=0)

        x=self.fire3(x)
        f3 = x
        #kprint(x.size(),"fire3",ra=0)
        #x=self.sq3(x)
        #x=self.ex3(x)
        size_fire3 = x.size()

        """

        x,indices_fire3=self.maxpool(x)
        #kprint(x.size(),"maxpool",ra=0)

        x=self.fire4(x)
        #kprint(x.size(),"fire4",ra=0)
        size_fire4 = x.size()

        x=self.smoke4(x)
        #kprint(x.size(),"smoke4",ra=0)

        
        x=self.maxunpool(x,indices_fire3,size_fire3)
        #kprint(x.size(),"maxunpool",ra=0)

        """

        x=self.smoke3(torch.cat((x,f3),1))
        #kprint(x.size(),"smoke3",ra=0)

        
        x=self.maxunpool(x,indices_fire2,size_fire2)
        #kprint(x.size(),"maxunpool",ra=0)


        x=self.smoke2(torch.cat((x,f2),1))
        #kprint(x.size(),"smoke2",ra=0)


        x=self.maxunpool(x,indices_fire1,size_fire1)
        #kprint(x.size(),"maxunpool",ra=0)


        x=self.smoke1(torch.cat((x,f1),1))
        #kprint(x.size(),"smoke1",ra=0)


        x = self.final_deconv(x)
        x = self.swish6(x)
        #kprint(x.size(),"final_deconv",ra=0)

        self.A['output'] = x
        self.A['target'] = Torch_data['target']
        self.loss = self.criterion(self.A['output'],self.A['target'])
        self.losses_to_average.append(self.extract('loss'))
        if len(self.losses_to_average) >= self.num_losses_to_average:
            self.losses.append( na(self.losses_to_average).mean() )
            self.losses_to_average = []
        return(self.A['output'])

    


    def setup_weights(self):
        pass



class Squeeze(nn.Module):
    def __init__(self, inplanes, squeeze_planes,
                 expand1x1_planes, expand3x3_planes):
        super(Squeeze, self).__init__()
        self.inplanes = inplanes
        self.squeeze = nn.Conv2d(inplanes, squeeze_planes, kernel_size=1)
        self.squeeze_activation = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.squeeze_activation(self.squeeze(x))
        return x

class Expand(nn.Module):
    def __init__(self, inplanes, squeeze_planes,
                 expand1x1_planes, expand3x3_planes):
        super(Expand, self).__init__()
        self.expand1x1 = nn.Conv2d(squeeze_planes, expand1x1_planes,
                                   kernel_size=1)
        self.expand1x1_activation = nn.ReLU(inplace=True)
        self.expand3x3 = nn.Conv2d(squeeze_planes, expand3x3_planes,
                                   kernel_size=3, padding=1)
        self.expand3x3_activation = nn.ReLU(inplace=True)

    def forward(self, x):
        return torch.cat([
            self.expand1x1_activation(self.expand1x1(x)),
            self.expand3x3_activation(self.expand3x3(x))
        ], 1)
#EOF