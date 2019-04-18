from kzpy3.utils3 import *
import torch
exec(identify_file_str)


def Torch_Network(weight_file_path):
    
    if True:#try:
        D = {}
        """
        D['heading'] = {}
        D['encoder'] = {}
        D['motor'] = {}
        """
        D['save_data'] = torch.load(weight_file_path)
        cg("*** Torch_Network():: Loading "+weight_file_path+" ***")
        from kzpy3.Train_app.nets.SqueezeNet40 import SqueezeNet
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
        #D['output'] = D['solver'](input_,torch.autograd.Variable(metadata))
        #ccm("type(input_) =",type(input_),"\ntype(metadata) =",type(metadata),ra=1)
        D['output'] = D['solver'](torch.autograd.Variable(input_),torch.autograd.Variable(metadata))       
        #print D['output'][0][:],type(D['output'][0][:].data[0])
        return D['output'][0][:].data.cpu().numpy()

    D['run_model'] = _run_model
    
    return D
#EOF

