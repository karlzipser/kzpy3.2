# https://github.com/pgtgrly/Convolution-Deconvolution-Network-Pytorch/blob/master/Neural_Network_Class.py

try:
    from net import *
except:
    print "from net import * failed."
    assert False

exec(identify_file_str)


del Fire

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
        D = {
            'inplanes':inplanes,
            'squeeze_planes':squeeze_planes,
            'expand1x1_planes':expand1x1_planes,
            'expand3x3_planes':expand3x3_planes,
            'outplanes': expand1x1_planes + expand3x3_planes,
            'name':name,
        }
        self.D = D
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
        #self.describe()

    def describe(self):
        kprint(self.D,title=self.D['name'],ignore_keys=['name'],r=1)

    def forward(self, x):
        inxsize = x.size()

        x = self.squeeze_activation(self.squeeze(x))
        if type(self.A) != type(False):
            self.A[d2p(self.name,'squeeze_activation')] = x
        x = torch.cat([
            self.expand1x1_activation(self.expand1x1(x)),
            self.expand3x3_activation(self.expand3x3(x))
        ], 1)

        outxsize = x.size()

        if 'in_size' not in self.D:
            self.D['in_size'] = (inxsize[2],inxsize[3])
            self.D['out_size'] = (outxsize[2],outxsize[3])
            self.describe()

        return x


class MyMaxPool(nn.Module):
    def __init__(
        self,
        kernel_size,
        stride,
        return_indices,
        padding,
        name='',
        A=False
    ):
        self.name = name
        super(MyMaxPool, self).__init__()
        self.A = A
        D = {
            'name':name,
            'kernel_size':kernel_size,
            'stride':stride,
            'return_indices':return_indices,
            'padding':padding,
        }
        self.D = D
        self.name = name
        self.maxpool = nn.MaxPool2d(
            kernel_size=D['kernel_size'],
            stride=D['stride'],
            return_indices=D['return_indices'],
            padding=D['padding']
        )

    def describe(self):
        kprint(self.D,title=self.D['name'],ignore_keys=['name'],r=1)

    def forward(self, x):
        print type(x)
        print x
        inxsize = x.size()
        x,indicies = self.maxpool(x)
        print type(x)
        print x
        outxsize = x.size()

        if 'in_size' not in self.D:
            self.D['in_size'] = (inxsize[2],inxsize[3])
            self.D['out_size'] = (outxsize[2],outxsize[3])
            self.describe()

        if self.D['return_indices']:
            return x,indicies
        else:
            return x


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
        self.maxpool1 = MyMaxPool(kernel_size=3,stride=2,return_indices=True,padding=0,name='maxpool1')
        #self.maxpool1 = nn.MaxPool2d(kernel_size=3,stride=2,return_indices=True,padding=0)
        self.maxpool2 = nn.MaxPool2d(kernel_size=3,stride=2,return_indices=True,padding=0)
        self.maxpool3= nn.MaxPool2d(kernel_size=3,stride=2,return_indices=True,padding=0)

        self.final_deconv = nn.ConvTranspose2d(2*a, P['NUM_OUTPUTS'], kernel_size=1)
        self.relu=nn.ReLU()

        self.drop_layer = nn.Dropout(p=0.1)

        self.final_conv_2 = nn.Conv2d(256, P['NUM_OUTPUTS'], kernel_size=1)
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

        x = self.drop_layer(x)
        x,indices_fire1 = self.maxpool1(x)
        x = self.fire2(x)

        x = self.drop_layer(x)
        x,indices_fire2=self.maxpool2(x)
        x = self.fire3(x)

        size_fire3 = x.size()
        x = self.drop_layer(x)

        self.A['output_2'] = self.output_2(x)
        self.A['output_2'] = self.A['output_2'].view(self.A['output_2'].size(0), -1)

        self.A['target'] = Torch_data['target']

        return(self.A['output_2'])

    

    def setup_weights(self):
        pass



#EOF