from kzpy3.utils3 import *
import torch
import kzpy3.Menu_app.menu2 as menu2
exec(identify_file_str)


def read_menu_and_load_network(N):
    
    if not N['timer']['parameter_file_load'].check():
        return

    Topics = menu2.load_Topics(
        opjk("Cars/n26Dec18/nodes"),
        first_load=False,
        customer='Network')

    if type(Topics) == dict:
        for t in Topics.keys():
            if t == 'ABORT':
                if Topics[t] == True:
                    N['ABORT'] = True
                    time.sleep(1)
                    return
        for t in Topics['To Expose']['Network']+\
                 Topics['To Expose']['Weights']+\
                 Topics['To Expose']['Flex']:
            if '!' in t:
                pass
            else:
                N[t] = Topics[t]
    
    if N['LOAD NETWORK'] == False:
        N['net']['loaded_net'] = False
    N['weight_file_path'] = False
    if N['net']['loaded_net'] == False:
        if N['LOAD NETWORK'] == True:
            N['net']['loaded_net'] = True
            ns = N['weight_files'].keys()
            for n in ns:
                if N[n] != False:
                    if type(N[n]) == int:
                        if N[n] != 0:
                            N['weight_file_path'] = \
                                N['weight_files'][n][N[n]]
                            sbpd2s("N['weight_file_path'] = N['weight_files'][n][a[1]]")
                            break
            if N['weight_file_path'] != False:
                cs( "if N['weight_file_path'] != False:" )
                N['net']['Torch_network'] = Torch_Network(N['weight_file_path'])
                cs( "Torch_network = net_utils.Torch_Network(N)" )

    N['timer']['parameter_file_load'].reset()

# weight_file_path=N['weight_files']['weights (1370)'][-1]

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

