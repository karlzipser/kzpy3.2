from kzpy3.utils3 import *
import torch
#from kzpy3.Train_app.nets.SqueezeNet40_global_A import SqueezeNet
from kzpy3.Train_app.nets.SqueezeNet120 import SqueezeNet as SqueezeNet_zed
from kzpy3.Train_app.nets.SqueezeNet120_16chLIDAR import SqueezeNet as SqueezeNet120_16chLIDAR
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
    

def load_net(path):
    save_data = torch.load(path)
    net = save_data['net']
    return net
"""
changing net structure and carrying over old weights
import torch
#import kzpy3.Train_app.nets.SqueezeNet40
import kzpy3.Train_app.nets.SqueezeNet120
A = load_net(most_recent_file_in_folder(opjD('Networks/Sq40_proj_from_scratch_premeta_from_24Dec/weights'),['.infer'],[]))
B = kzpy3.Train_app.nets.SqueezeNet120.SqueezeNet().cuda()
C = B.state_dict()
for k in A.keys():
    if 'final_output' not in k:
        C[k] = A[k]
weights = {'net':C}
torch.save(weights,opjD('Sq120_from_Sq40.infer'))
"""


def Pytorch_Network(P,network_class='zed'):
    """
    print(P['NETWORK_OUTPUT_FOLDER'])
    print(P['INITIAL_WEIGHTS_FOLDER'])
    print(P['WEIGHTS_FILE_PATH'])
    """
    D = {}
    torch.set_default_tensor_type('torch.FloatTensor') 
    torch.cuda.set_device(P['GPU'])
    torch.cuda.device(P['GPU'])
    cg("GPUs =",torch.cuda.device_count(),"current GPU =",torch.cuda.current_device())

    if network_class == 'zed':
        D['net'] = SqueezeNet_zed().cuda()
    elif network_class == 'depth':
        D['net'] = SqueezeNet120_16chLIDAR().cuda()





    D['criterion'] = torch.nn.MSELoss().cuda()
    if False: #original
        D['optimizer'] = torch.optim.Adadelta(D['net'].parameters())
    D['optimizer'] = torch.optim.Adadelta(filter(lambda p: p.requires_grad,D['net'].parameters()))
    try:
        for folder in ['weights','loss','dm_ctrs','state_dict','optimizer']:
            unix(d2s('mkdir -p',opj(P['NETWORK_OUTPUT_FOLDER'],folder)))
    except:
        cr('*** Failed to create default network output folders ***')

    def _function_save_net(temp=False):
        cprint(network_class,'yellow','on_blue')
        if network_class == 'zed':
            return
        if P['save_net_timer'].check() or temp:
            pd2s('2 lr=',D['net'].lr)
            print('saving net state . . .')
            weights = {'net':D['net'].state_dict().copy()}
            for key in weights['net']:
                weights['net'][key] = weights['net'][key].cuda(device=0)
            if temp:
                torch.save(weights, opj(P['NETWORK_OUTPUT_FOLDER'],'weights','temp.infer'))
                cb('. . . done saving temp.infer')
                return
            torch.save(weights, opj(P['NETWORK_OUTPUT_FOLDER'],'weights',P['SAVE_FILE_NAME']+'P'+time_str()+'.infer'))
            so(P['LOSS_LIST_AVG'],opj(P['NETWORK_OUTPUT_FOLDER'],'loss',P['SAVE_FILE_NAME']+'P'+time_str()+'.loss_avg'))
            if 'dm_ctrs' in P:
                so(P['dm_ctrs'],opj(P['NETWORK_OUTPUT_FOLDER'],'dm_ctrs',P['SAVE_FILE_NAME']+'P'+time_str()+'.dm_ctrs'))
            torch.save(D['optimizer'].state_dict(), opj(P['NETWORK_OUTPUT_FOLDER'],'optimizer',P['SAVE_FILE_NAME']+'P'+time_str()+'.optimizer_state'))
            torch.save(D['net'].state_dict(), opj(P['NETWORK_OUTPUT_FOLDER'],'state_dict',P['SAVE_FILE_NAME']+'P'+time_str()+'.state_dict'))
            print('. . . done saving.')
            P['save_net_timer'].reset()

    D['SAVE_NET'] = _function_save_net

    if P['RESUME']:


        if P['freeze premetadata weights']:



            A = load_net(most_recent_file_in_folder(opjD('Networks/net_24Dec2018_12imgs_projections/weights'),['.infer'],[]))
            B = load_net(P['WEIGHTS_FILE_PATH'])

            for l in ['pre_metadata_features.0.weight',
                     'pre_metadata_features.0.bias',
                     'pre_metadata_features.3.squeeze.weight',
                     'pre_metadata_features.3.squeeze.bias',
                     'pre_metadata_features.3.expand1x1.weight',
                     'pre_metadata_features.3.expand1x1.bias',
                     'pre_metadata_features.3.expand3x3.weight',
                     'pre_metadata_features.3.expand3x3.bias',]:
                cy("Copying",l,'from',P['update premetadata weights from other model'])
                B[l] = A[l]
            weights = {'net':B}
            torch.save(weights,opj(P['NETWORK_OUTPUT_FOLDER'],'weights','merged.infer'))
        cy(network_class)
        try:
            if len(sggo(P['WEIGHTS_FILE_PATH'])) > 0:
                

                if P['freeze premetadata weights']:
                    cprint(d2s('Resuming with',opj(P['NETWORK_OUTPUT_FOLDER'],'weights','merged.infer')),'red')
                    save_data = torch.load(opj(P['NETWORK_OUTPUT_FOLDER'],'weights','merged.infer'))
                else:
                    cprint(d2s('Resuming with',P['WEIGHTS_FILE_PATH']),'blue','on_white')
                    save_data = torch.load(P['WEIGHTS_FILE_PATH'])

                D['net'].load_state_dict(save_data['net'])

                if False:
                    P['save_net_timer'].trigger()
                    D['SAVE_NET']()
                    raw_enter('This is STRANGE too!!!')

                if P['freeze premetadata weights']:
                    ctr = 0
                    for param in D['net'].parameters():
                        rg = True
                        if ctr < 8:
                            rg = False
                        param.requires_grad = rg
                        if rg:
                            f = cg
                        else:
                            f = cr
                        f(ctr,param.size())
                        ctr += 1

            else:
                CS_("Could not load "+P['WEIGHTS_FILE_PATH'])
            m = most_recent_file_in_folder( opj(P['NETWORK_OUTPUT_FOLDER'],'loss') )
            if m:
                CS_("loading "+m)
                P['LOSS_LIST_AVG'] = lo(m)
            else:
                CS_("Could not load loss")
            m = most_recent_file_in_folder(opj(P['NETWORK_OUTPUT_FOLDER'],'optimizer'))
            if m:
                CS_("loading "+m)
                D['optimizer'].load_state_dict(torch.load(m))
                pd2s('1 lr=',D['net'].lr)
            else:
                CS_("Could not load optimizer")
            m = most_recent_file_in_folder(opj(P['NETWORK_OUTPUT_FOLDER'],'state_dict'))
            """
            # This always fails
            if m:
                CS_("loading "+m)
                torch.load(D['net'].state_dict(),m)
            else:
                CS_("Could not load state_dict")
            """
            
        except Exception as e:
            CS_("********** Network_Module.py Exception ***********************")
            print(e.message, e.args)
            cr("*** D['optimizer'] = torch.optim.Adadelta(filter(lambda p: p.requires_grad,D['net'].parameters())) ***") 
            if False: #original
                D['optimizer'] = torch.optim.Adadelta(D['net'].parameters())
            D['optimizer'] = torch.optim.Adadelta(filter(lambda p: p.requires_grad,D['net'].parameters())) 
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            time.sleep(4)
    else:
        cprint('Training network from random weights','red')


   
    return D




#EOF