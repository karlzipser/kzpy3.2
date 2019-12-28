
from kzpy3.vis3 import *

if False:
    import Menu.main


    M = Menu.main.start_Dic(
        dic_project_path=pname(opjh(__file__)), 
        Arguments={
            'menu':False,
            'read_only':True,
        }
    )


    def sample_use_of_menu_data():

        while True:

            loaded = M['load']()

            if loaded:
                clp(' '+time_str('Pretty')+' ','`ybb')
                kprint(M['Q'])


    if __name__ == '__main__':
        sample_use_of_menu_data()



from kzpy3.utils3 import *
import torch
import kzpy3.drafts.Sq.network as network
import torch._utils
exec(identify_file_str)
try:
    torch._utils._rebuild_tensor_v2
except AttributeError:
    def _rebuild_tensor_v2(storage, storage_offset, size, stride, requires_grad, backward_hooks):
        tensor = torch._utils._rebuild_tensor(storage, storage_offset, size, stride)
        tensor.requires_grad = requires_grad
        tensor._backward_hooks = backward_hooks
        return tensor
    torch._utils._rebuild_tensor_v2 = _rebuild_tensor_v2
    

NUM_INPUT_CHANNELS=6
NUM_OUTPUTS=1
NUM_METADATA_CHANNELS=0
INPUT_WIDTH = 168
INPUT_HEIGHT = 94
METADATA_WIDTH = 41
METADATA_HEIGHT = 23

NUM_IN_BATCH = 64

input_data =    np.zeros((NUM_IN_BATCH,NUM_INPUT_CHANNELS,INPUT_WIDTH,INPUT_HEIGHT))
meta_data =     None#np.zeros((NUM_IN_BATCH,NUM_METADATA_CHANNELS,METADATA_WIDTH,METADATA_HEIGHT))
target_data =   np.zeros((NUM_IN_BATCH,NUM_OUTPUTS))

N = network.SqueezeNet(
    NUM_INPUT_CHANNELS,
    NUM_OUTPUTS,
    NUM_METADATA_CHANNELS,
    )


"""    
def Pytorch_Network(_):
    D = {}
    D['net'] = network.SqueezeNet(
        NUM_INPUT_CHANNELS,
        NUM_OUTPUTS,
        NUM_METADATA_CHANNELS,
        )
"""

    """
    D['criterion'] = torch.nn.MSELoss()#.cuda()
    D['optimizer'] = torch.optim.Adadelta(filter(lambda p: p.requires_grad,D['net'].parameters()))
    try:
        for folder in ['weights','loss','validation_loss','dm_ctrs','state_dict','optimizer']:
            os.system(d2s('mkdir -p',opj(_['NETWORK_OUTPUT_FOLDER'],folder)))
    except:
        clp(' *** Failed to create default network output folders *** ','`rwb') ; time.sleep(1)

    if _['RESUME']:
        pass
    else:
        clp(' *** Training network from random weights *** ','`rwb') ; time.sleep(1)

    def _function_forward(input_data,meta_data,target_data):
        D['optimizer'].zero_grad()
        input_torch = torch.autograd.Variable(torch.from_numpy(input_data).float())
        if meta_data != None:
            meta_data_torch = torch.autograd.Variable(torch.from_numpy(meta_data).float())
        else:
            meta_data_torch = None
        target_torch = torch.autograd.Variable(torch.from_numpy(target_data).float())
        D['outputs'] = D['net'](input_torch,meta_data_torch)


        D['loss'] = D['criterion'](D['outputs'],target_torch)

        #D['loss'] = D['criterion'](D['outputs'])

    D['forward'] = _function_forward

    return D
    """

"""
N = Pytorch_Network(
    {
        'RESUME':False,
    })

N['forward'](input_data,meta_data,target_data)
"""




#EOF
