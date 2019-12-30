from kzpy3.vis3 import *
import network  
import graphics  
import Menu.main
from get_data import make_XOR_input_target as make_input_meta_target
exec(identify_file_str)
import menu_str
exec(menu_str.exec_str)

kprint(M['Q'])



import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.utils as nnutils

GPU = 0
torch.set_default_tensor_type('torch.FloatTensor')
torch.cuda.set_device(GPU)
#torch.cuda.device(GPU)
#clp("GPUs =",torch.cuda.device_count(),"current GPU =",torch.cuda.current_device())


try:
    torch._utils._rebuild_tensor_v2
except AttributeError:
    def _rebuild_tensor_v2(storage, storage_offset, size, stride, requires_grad, backward_hooks):
        tensor = torch._utils._rebuild_tensor(storage, storage_offset, size, stride)
        tensor.requires_grad = requires_grad
        tensor._backward_hooks = backward_hooks
        return tensor
    torch._utils._rebuild_tensor_v2 = _rebuild_tensor_v2




N = network.SqueezeNet(
    P['NUM_INPUT_CHANNELS'],
    P['NUM_OUTPUTS'],
    P['NUM_METADATA_CHANNELS'],
    P['NUM_LOSSES_TO_AVERAGE'],
    P['NETWORK_OUTPUT_FOLDER'],
    P['NET_SAVE_TIMER_TIME'],
    ).cuda()



N.criterion = torch.nn.MSELoss().cuda()





if P['RESUME']:
    import torch
    N.load()
else:
    clp('Starting with random weights','`wbb')
 

#torch.autograd.Variable(D['camera_data'])



def main():

    while not M['Q']['other_parameters']['abort']:

        M['load']()

        N.forward(
            torch.autograd.Variable(torch.from_numpy(zeros((64,2,168,94))).float().cuda()),
            None,
            torch.autograd.Variable(torch.from_numpy(zeros((64,1))).cuda()),
        )

        N.backward()

        N.save()

        graphics.graphics(N)

    raw_enter()






if __name__ == '__main__':
    main()



#EOF
