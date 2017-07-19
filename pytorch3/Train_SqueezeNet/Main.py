##############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/pytorch3/Train_SqueezeNet','kzpy3/teg9'])
#
##############################
from Parameters_Module import *
exec(identify_file_str)
import Data_Module
import Batch_Module
import torch

_ = dictionary_access

for a in Args.keys():
    _(P,a,equals,_(Args,a)) #P[a] = Args[a]





torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(_(P,GPU))
torch.cuda.device(_(P,GPU))



from SqueezeNet import SqueezeNet
netv = SqueezeNet().cuda()
criterion = torch.nn.MSELoss().cuda()
optimizer = torch.optim.Adadelta(netv.parameters())



Training_data = Data_Module.Training_Data()


Batch = Batch_Module.Batch(net,netv, batch_size,_(P,BATCH_SIZE))

_(Batch,fill)('Data',Training_data, mode,train)
#batch['fill']({'Data':DD,'mode':mode})
#Data_moment = _(Training_data,get_data)(run_code,1, seg_num,2, offset,3)

#zdprint(dic,Data_moment)





#EOF