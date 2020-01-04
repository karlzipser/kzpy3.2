from net import *
exec(identify_file_str)


class SqueezeNet(Net):

    def setup_layers(self,P):
        self.pre_metadata_features = nn.Sequential(
            nn.Conv2d(P['NUM_INPUT_CHANNELS'], 64, kernel_size=3, stride=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(64, 16, 64, 64),            
            )
        self.post_metadata_features = nn.Sequential(
            Fire(64+64+P['NUM_METADATA_CHANNELS'], 16, 64, 64),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(128, 32, 128, 128),
            Fire(256, 32, 128, 128),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            Fire(256, 48, 192, 192),
            Fire(384, 48, 192, 192),
            Fire(384, 64, 256, 256),
            Fire(512, 64, 256, 256),
        )
        self.final_conv = nn.Conv2d(512, P['NUM_OUTPUTS'], kernel_size=1)
        self.output = nn.Sequential(
            nn.Dropout(p=0.5),
            self.final_conv,
            nn.AvgPool2d(kernel_size=5, stride=6)
        )

    def setup_weights(self):
        for m in self.modules():
            #print m
            if isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d):
                try:
                    if m is self.final_conv:
                        init.normal(m.weight.data, mean=0.0, std=0.01)
                    else:
                        init.kaiming_uniform(m.weight.data)
                except:
                    print('exception')
                if m.bias is not None:
                    m.bias.data.zero_()
            else:
                pass#assert(False)
                    
    def forward(self,Data):
        self.optimizer.zero_grad()

        Torch_data = self.data_to_torch(Data)

        self.A['input'] = Torch_data['input']

        self.A['pre_metadata_features'] = self.pre_metadata_features(self.A['input'])
        if 'meta' not in Torch_data or type(Torch_data['meta_data']) == type(None):
            self.A['pre_metadata_features_metadata'] = self.A['pre_metadata_features']
        else:
            self.A['pre_metadata_features_metadata'] = torch.cat((self.A['pre_metadata_features'], Torch_data['meta']), 1)
        self.A['post_metadata_features'] = self.post_metadata_features(self.A['pre_metadata_features_metadata'])
        self.A['output'] = self.output(self.A['post_metadata_features'])
        self.A['output'] = self.A['output'].view(self.A['output'].size(0), -1)
        self.A['target'] = Torch_data['target']
        self.loss = self.criterion(self.A['output'],Torch_data['target'])
        self.losses_to_average.append(self.extract('loss'))
        if len(self.losses_to_average) >= self.num_losses_to_average:
            self.losses.append( na(self.losses_to_average).mean() )
            self.losses_to_average = []
        return self.A['output']








#EOF
