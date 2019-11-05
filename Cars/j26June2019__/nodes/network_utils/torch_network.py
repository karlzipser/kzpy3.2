from kzpy3.utils3 import *
import torch
exec(identify_file_str)

import torch._utils
try:
    torch._utils._rebuild_tensor_v2
except AttributeError:
    def _rebuild_tensor_v2(storage, storage_offset, size, stride, requires_grad, backward_hooks):
        tensor = torch._utils._rebuild_tensor(storage, storage_offset, size, stride)
        tensor.requires_grad = requires_grad
        tensor._backward_hooks = backward_hooks
        return tensor
    torch._utils._rebuild_tensor_v2 = _rebuild_tensor_v2
    
def Torch_Network(weight_file_path):
    
    if True:#try:
        D = {}

        D['save_data'] = torch.load(weight_file_path)
        cg("*** Torch_Network():: Loading "+weight_file_path+" ***")
        from kzpy3.Train_app.nets.SqueezeNet120 import SqueezeNet
        D['solver'] = SqueezeNet().cuda()
        D['solver'].load_state_dict(D['save_data']['net'])
        D['solver'].eval()
        cg("*** Torch_Network():: Loading complete. ***")

    else:#except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        cr('Exception!')
        cr(d2s(exc_type,file_name,exc_tb.tb_lineno))

    def _run_model(input_,metadata):

        D['output'] = D['solver'](torch.autograd.Variable(input_),torch.autograd.Variable(metadata))       

        return D['output'][0][:].data.cpu().numpy()

    D['run_model'] = _run_model
    
    return D
#EOF

