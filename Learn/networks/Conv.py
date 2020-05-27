# https://github.com/pgtgrly/Convolution-Deconvolution-Network-Pytorch/blob/master/Neural_Network_Class.py

try:
    from net import *
except:
    print "from net import * failed."
    assert False

exec(identify_file_str)



class Fire(nn.Module):
    def __init__(
        self,
        inplanes,
        squeeze_planes,
        expand1x1_planes,
        expand3x3_planes,
        name='',
        A=False
    ):
        super(Fire, self).__init__()
        self.A = A
        self.name = name
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
        if type(self.A) != type(False):
            self.A[d2p(self.name,'squeeze_activation')] = x
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
        expand3x3_planes,
        name='',
        A=False
    ):
        super(Smoke, self).__init__()
        self.A = A
        self.name = name
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
        if type(self.A) != type(False):
            self.A[d2p(self.name,'squeeze_activation')] = x
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


lateral = True

class Conv(Net):

    def setup_layers(self,P):
        self.A = {}
        self.fire1 = Fire(P['NUM_INPUT_CHANNELS'],aa,b,b,'Fire1',self.A)
        self.fire2 = Fire(c,a,c,c,'Fire2',self.A)
        self.fire3 = Fire(d,b,d,d,'Fire3',self.A)
        self.fire4=Fire(e,c,e,e,'Fire4',self.A)
        self.smoke4=Smoke(f,c,d,d,'Smoke4',self.A)
        self.maxpool1 = nn.MaxPool2d(kernel_size=3,stride=2,return_indices=True,padding=0)
        self.maxpool2 = nn.MaxPool2d(kernel_size=3,stride=2,return_indices=True,padding=0)
        self.maxpool3= nn.MaxPool2d(kernel_size=3,stride=2,return_indices=True,padding=0)

        if lateral:
            self.smoke3 = Smoke(e+e,b,c,c,'Smoke3',self.A)
            self.smoke2 = Smoke(d+d,a,b,b,'Smoke2',self.A)
            self.smoke1 = Smoke(c+c,aa,a,a,'Smoke1',self.A)
        else:
            self.smoke3 = Smoke(e,b,c,c,'Smoke3',self.A)
            self.smoke2 = Smoke(d,a,b,b,'Smoke2',self.A)
            self.smoke1 = Smoke(c,aa,a,a,'Smoke1',self.A)

        self.maxunpool1 = nn.MaxUnpool2d(kernel_size=3,stride=2,padding=0)
        self.maxunpool2 = nn.MaxUnpool2d(kernel_size=3,stride=2,padding=0)
        self.maxunpool3 = nn.MaxUnpool2d(kernel_size=3,stride=2,padding=0)

        self.final_deconv = nn.ConvTranspose2d(2*a, P['NUM_OUTPUTS'], kernel_size=1)
        self.relu=nn.ReLU()

        self.drop_layer = nn.Dropout(p=0.1)


        self.final_conv_2 = nn.Conv2d(256, 100, kernel_size=1)
        self.output_2 = nn.Sequential(
            nn.Dropout(p=0.5),
            self.final_conv_2,
            nn.AvgPool2d(kernel_size=5*4, stride=6*4)
        )

    

    def forward_no_loss(self,Data):
        Torch_data = self.data_to_torch(Data)
        self.A['input'] = Torch_data['input']
        x = self.A['input']
        x = self.fire1(x)
        f1 = x
        size_fire1 = x.size()
        x = self.drop_layer(x)
        x,indices_fire1 = self.maxpool1(x)
        x = self.fire2(x)
        f2 = x
        size_fire2 = x.size()
        x = self.drop_layer(x)
        x,indices_fire2=self.maxpool2(x)
        x = self.fire3(x)
        f3 = x
        size_fire3 = x.size()
        x = self.drop_layer(x)


        
        self.A['output_2'] = self.output_2(x)
        self.A['output_2'] = self.A['output_2'].view(self.A['output_2'].size(0), -1)
        clp('x',x.size(),'output_2',self.A['output_2'].size())
        




        if lateral:
            x = self.smoke3(torch.cat((x,f3),1))
        else:
            x = self.smoke3(x)

        x = self.drop_layer(x)
        x = self.maxunpool2(x,indices_fire2,size_fire2)

        if lateral:
            x = self.smoke2(torch.cat((x,f2),1))
        else:
            x = self.smoke2(x)

        x = self.drop_layer(x)
        x = self.maxunpool1(x,indices_fire1,size_fire1)

        if lateral:
            x = self.smoke1(torch.cat((x,f1),1))
        else:
            x = self.smoke1(x)

        x = self.final_deconv(x)
        x = self.relu(x)

        self.A['output'] = x
        self.A['target'] = Torch_data['target']

        return(self.A['output'])

    

    def setup_weights(self):
        pass


if False:
    P_ = {
        'LR': 0.01,
        'momentum':0.001,
        'GPU':0,
        'clip':1,
        'NETWORK_OUTPUT_FOLDER':'',
        'losses_to_average':4,
        'save_timer_time':300,
        'NUM_INPUT_CHANNELS':3,
        'NUM_OUTPUTS':3,
        'resume':False,
    }

    S = ConDecon_FS(P_) 

    h,w = 94,168
    """
    Fire1.squeeze_activation (5, 8, 94, 168)
    Fire2.squeeze_activation (5, 16, 46, 83)
    Fire3.squeeze_activation (5, 32, 22, 41)
    Smoke1.squeeze_activation (5, 8, 94, 168)
    Smoke2.squeeze_activation (5, 16, 46, 83)
    Smoke3.squeeze_activation (5, 32, 22, 41)
    input (5, 3, 94, 168)
    output (5, 3, 94, 168)
    target (5, 3, 94, 168)
    """
    h,w = 10,20
    """
    Fire1.squeeze_activation (5, 8, 10, 20)
    Fire2.squeeze_activation (5, 16, 4, 9)
    Fire3.squeeze_activation (5, 32, 1, 4)
    Smoke1.squeeze_activation (5, 8, 10, 20)
    Smoke2.squeeze_activation (5, 16, 4, 9)
    Smoke3.squeeze_activation (5, 32, 1, 4)
    input (5, 3, 10, 20)
    output (5, 3, 10, 20)
    target (5, 3, 10, 20)
    """


    o = S.forward_no_loss(
        {
            'input':randn(5, 3, h, w),
            'target':randn(5, 3, h, w),
        }
    )
    for k in sorted(S.A.keys()):
        print k,S.A[k].size()



"""

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

"""

#EOF