# https://github.com/pgtgrly/Convolution-Deconvolution-Network-Pytorch/blob/master/Neural_Network_Class.py

try:
    from net import *
except:
    print "from net import * failed."
    assert False

exec(identify_file_str)


del Fire

class MyFire(nn.Module):
    def __init__(
        self,
        inplanes,
        squeeze_planes,
        expand1x1_planes,
        expand3x3_planes,
        name='',
        A=False
    ):
        super(MyFire, self).__init__()
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
        kprint(self.D,title=self.D['name'],ignore_keys=['name'],r=0)

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


class MyInitialConv(nn.Module):
    def __init__(
        self,
        name='',
        A=False
    ):
        self.name = name
        super(MyInitialConv, self).__init__()
        self.A = A
        D = {
            'name':name,
        }
        self.D = D
        self.name = name
        self.conv2d = nn.Conv2d(3, 64, kernel_size=3, stride=2)
        self.relu = nn.ReLU(inplace=True)


    def describe(self):
        kprint(self.D,title=self.D['name'],ignore_keys=['name'],r=0)

    def forward(self, x):

        inxsize = x.size()
        x = self.conv2d(x)
        x = self.relu(x)
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
        kprint(self.D,title=self.D['name'],ignore_keys=['name'],r=0)

    def forward(self, x):

        inxsize = x.size()
        if self.D['return_indices']:
            x,indicies = self.maxpool(x)
        else:
            x = self.maxpool(x)

        outxsize = x.size()

        if 'in_size' not in self.D:
            self.D['in_size'] = (inxsize[2],inxsize[3])
            self.D['out_size'] = (outxsize[2],outxsize[3])
            self.describe()

        if self.D['return_indices']:
            return x,indicies
        else:
            return x

"""
aa = 8
a = 16
b = 32
c = 64
d = 128
e = 256
f = 512
rgb = 3
"""


lateral = True

class MyConv(Net):

    def setup_layers(self,P):
        self.A = {}
        self.conv_init = MyInitialConv('conv_init',self.A)

        self.fire1 = MyFire(64, 16, 64, 64,'Fire1',self.A)
        self.fire2 = MyFire(128, 16, 64, 64,'Fire2',self.A)

        self.fire3 = MyFire(128, 32, 128, 128,'Fire3',self.A)
        self.fire4 = MyFire(256, 32, 128, 128,'Fire4',self.A)

        self.fire5 = MyFire(256, 48, 192, 192,'Fire5',self.A)
        self.fire6 = MyFire(384, 48, 192, 192,'Fire6',self.A)
        self.fire7 = MyFire(384, 64, 256, 256,'Fire7',self.A)
        self.fire8 = MyFire(512, 64, 256, 256,'Fire8',self.A)
        self.maxpool1 = MyMaxPool(kernel_size=3,stride=2,return_indices=True,padding=0,name='maxpool1')
        self.maxpool2 = MyMaxPool(kernel_size=3,stride=2,return_indices=True,padding=0,name='maxpool2')
        self.maxpool3 = MyMaxPool(kernel_size=3,stride=2,return_indices=True,padding=0,name='maxpool3')
        self.relu=nn.ReLU()

        self.drop_layer = nn.Dropout(p=0.1)


        self.final_conv = nn.Conv2d(512, P['NUM_TARGETS'], kernel_size=1)
        self.drop = nn.Dropout(p=0.5)
        self.avg = nn.AvgPool2d(kernel_size=5, stride=6)
        






    
    def forward_no_loss(self,Data):
        Torch_data = self.data_to_torch(Data)
        self.A['input'] = Torch_data['input']

        x = self.A['input']

        x = self.conv_init(x)

        x,___ = self.maxpool1(x)

        x = self.fire1(x) 
        x = self.fire2(x)

        x,___ = self.maxpool2(x)

        x = self.fire3(x)
        x = self.fire4(x)

        x,___ = self.maxpool3(x)

        x = self.fire5(x)
        x = self.fire6(x)
        x = self.fire7(x)
        x = self.fire8(x)

        x = self.drop(x)
        x = self.final_conv(x)
        x = self.avg(x)

        self.A['output_2'] = x

        self.A['output_2'] = self.A['output_2'].view(self.A['output_2'].size(0), -1)

        self.A['target'] = Torch_data['target']

        # x = self.drop_layer(x)

        return(self.A['output_2'])

    

    def setup_weights(self):
        pass



#EOF