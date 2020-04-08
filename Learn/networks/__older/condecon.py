# https://github.com/pgtgrly/Convolution-Deconvolution-Network-Pytorch/blob/master/Neural_Network_Class.py

from net import *
exec(identify_file_str)

class ConDecon(Net):

    def setup_layers(self,P):

        self.conv1=nn.Conv2d(in_channels=P['NUM_INPUT_CHANNELS'],out_channels=16, kernel_size=4,stride=1, padding=0)
        nn.init.xavier_uniform(self.conv1.weight) #Xaviers Initialisation
        self.swish1= nn.ReLU()

        self.maxpool1= nn.MaxPool2d(kernel_size=2,return_indices=True)

        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=5)
        nn.init.xavier_uniform(self.conv2.weight)
        self.swish2 = nn.ReLU()

        self.maxpool2 = nn.MaxPool2d(kernel_size=2,return_indices=True)

        self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3)
        nn.init.xavier_uniform(self.conv3.weight)
        self.swish3 = nn.ReLU()

        self.deconv1=nn.ConvTranspose2d(in_channels=64,out_channels=32,kernel_size=3)
        nn.init.xavier_uniform(self.deconv1.weight)
        self.swish4=nn.ReLU()

        self.maxunpool1=nn.MaxUnpool2d(kernel_size=2)

        self.deconv2=nn.ConvTranspose2d(in_channels=32,out_channels=16,kernel_size=5)
        nn.init.xavier_uniform(self.deconv2.weight)
        self.swish5=nn.ReLU()

        self.maxunpool2=nn.MaxUnpool2d(kernel_size=2)

        self.deconv3=nn.ConvTranspose2d(in_channels=16,out_channels=P['NUM_OUTPUTS'],kernel_size=4)
        nn.init.xavier_uniform(self.deconv3.weight)
        self.swish6=nn.ReLU()

    def forward(self,Data):

        self.optimizer.zero_grad()
        Torch_data = self.data_to_torch(Data)
        self.A['input'] = Torch_data['input']
        out=self.conv1(self.A['input'])
        out=self.swish1(out)
        size1 = out.size()
        out,indices1=self.maxpool1(out)
        out=self.conv2(out)
        out=self.swish2(out)
        size2 = out.size()
        out,indices2=self.maxpool2(out)
        out=self.conv3(out)
        out=self.swish3(out)

        out=self.deconv1(out)
        out=self.swish4(out)
        out=self.maxunpool1(out,indices2,size2)
        out=self.deconv2(out)
        out=self.swish5(out)
        out=self.maxunpool2(out,indices1,size1)
        out=self.deconv3(out)
        out=self.swish6(out)
        self.A['output'] = out
        self.A['target'] = Torch_data['target']
        self.loss = self.criterion(self.A['output'],self.A['target'])
        self.losses_to_average.append(self.extract('loss'))
        if len(self.losses_to_average) >= self.num_losses_to_average:
            self.losses.append( na(self.losses_to_average).mean() )
            self.losses_to_average = []
        return(self.A['output'])

    
    def setup_weights(self):
        pass

#EOF