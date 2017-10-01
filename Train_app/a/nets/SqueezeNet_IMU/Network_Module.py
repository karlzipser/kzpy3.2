from Parameters_Module import *
exec(identify_file_str)

import math
import torch
import torch.nn as nn
import torch.nn.init as init
from torch.autograd import Variable
exec(identify_file_str)

torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(P[GPU])
torch.cuda.device(P[GPU])


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


class SqueezeNet(nn.Module):

	def __init__(self):
		super(SqueezeNet, self).__init__()
		self.A = {}
		self.lr = 0.01
		self.momentum = 0.01
		self.pre_metadata_features = nn.Sequential(
			nn.Conv2d(6*P[N_FRAMES], 64, kernel_size=3, stride=2),
			nn.ReLU(inplace=True),
			nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
			Fire(64, 16, 64, 64),            
			)
		self.post_metadata_features = nn.Sequential(
			Fire(256, 16, 64, 64),
			nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
			Fire(128, 32, 128, 128),
			Fire(256, 32, 128, 128),
			nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
			Fire(256, 48, 192, 192),
			Fire(384, 48, 192, 192),
			Fire(384, 64, 256, 256),
			Fire(512, 64, 256, 256),
		)
		final_conv = nn.Conv2d(512, P[N_OUTPUTS], kernel_size=1)
		self.final_output = nn.Sequential(
			nn.Dropout(p=0.5),
			final_conv,
			# nn.ReLU(inplace=True), # this allows initial training to recover from zeros in output
			nn.AvgPool2d(kernel_size=5, stride=6)
			#nn.AdaptiveAvgPool2d(1)#kernel_size=5, stride=6)


		)

		for m in self.modules():
			if isinstance(m, nn.Conv2d):
				if m is final_conv:
					init.normal(m.weight.data, mean=0.0, std=0.01)
				else:
					init.kaiming_uniform(m.weight.data)
				if m.bias is not None:
					m.bias.data.zero_()


	def forward(self, x, metadata):
		self.A['camera_input'] = x
		self.A['pre_metadata_features'] = self.pre_metadata_features(self.A['camera_input'])
		self.A['pre_metadata_features_metadata'] = torch.cat((self.A['pre_metadata_features'], metadata), 1)
		self.A['post_metadata_features'] = self.post_metadata_features(self.A['pre_metadata_features_metadata'])
		self.A['final_output'] = self.final_output(self.A['post_metadata_features'])
		self.A['final_output'] = self.A['final_output'].view(self.A['final_output'].size(0), -1)
		return self.A['final_output']



def unit_test():
	print 'Not doing unit_test.'
	return
	test_net = SqueezeNet()
	#a = test_net(Variable(torch.randn(5, 12, 94, 168)), Variable(torch.randn(5, 128, 23, 41)))    
	print('Tested SqueezeNet')

unit_test()








def Pytorch_Network():
    _ = {}
    True
    _[NET] = SqueezeNet().cuda()
    _[criterion] = torch.nn.MSELoss().cuda()
    _[optimizer] = torch.optim.Adadelta(_[NET].parameters())
    _[data_moment_loss_record] = {}
    _[rate_counter] = Rate_Counter(batch_size,P[BATCH_SIZE])
    _[epoch_counter] = {}
    for modev in [train,val]:
        _[epoch_counter][modev] = 0
    if P[RESUME]:
        cprint(d2s('Resuming with',P[WEIGHTS_FILE_PATH]),'yellow')
        save_data = torch.load(P[WEIGHTS_FILE_PATH])
        _[NET].load_state_dict(save_data['net'])
        time.sleep(4)
    else:
        pass

    def _function_save_net():
        if P[SAVE_NET_TIMER].check():
            print('saving NET state . . .')

            weights = {NET:_[NET].state_dict().copy()}
            for key in weights[NET]:
                weights[NET][key] = weights[NET][key].cuda(device=0)
            torch.save(weights, opj(P[NETWORK_OUTPUT_FOLDER],'weights',P[SAVE_FILE_NAME]+'_'+time_str()+'.infer'))

            print('. . . done saving.')
            P[SAVE_NET_TIMER].reset()
    _[SAVE_NET] = _function_save_net
   
    return _

