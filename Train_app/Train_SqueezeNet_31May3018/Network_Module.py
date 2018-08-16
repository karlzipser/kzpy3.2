from Parameters_Module import *
import torch
from kzpy3.Train_app.nets.SqueezeNet import SqueezeNet
exec(identify_file_str)

torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(P['GPU'])
torch.cuda.device(P['GPU'])


def Pytorch_Network():
    D = {}
    True

    D['net'] = SqueezeNet().cuda()
    D['criterion'] = torch.nn.MSELoss().cuda()
    D['optimizer'] = torch.optim.Adadelta(D['net'].parameters())

    if P['RESUME']:
        cprint(d2s('Resuming with',P['WEIGHTS_FILE_PATH']),'red')
        save_data = torch.load(P['WEIGHTS_FILE_PATH'])
        D['net'].load_state_dict(save_data['net'])
        P['LOSS_LIST_AVG'] = lo( most_recent_file_in_folder( opj(P['NETWORK_OUTPUT_FOLDER'],'loss') ) )
        try:
            D['optimizer'].load_state_dict(torch.load(most_recent_file_in_folder(opj(P['NETWORK_OUTPUT_FOLDER'],'optimizer'))))
        except:
            print 'unable load_state of optimizer'
            D['optimizer'] = torch.optim.Adadelta(D['net'].parameters())
        time.sleep(4)
    else:
        cprint('Training network from random weights','red')

    def _function_save_net():
        if P['save_net_timer'].check():
            print('saving net state . . .')
            for folder in ['weights','loss','dm_ctrs','state_dict','optimizer']:
                unix(d2s('mkdir -p',opj(P['NETWORK_OUTPUT_FOLDER'],folder)))
            weights = {'net':D['net'].state_dict().copy()}
            for key in weights['net']:
                weights['net'][key] = weights['net'][key].cuda(device=0)
            torch.save(weights, opj(P['NETWORK_OUTPUT_FOLDER'],'weights',P['SAVE_FILE_NAME']+'_'+time_str()+'.infer'))
            so(P['LOSS_LIST_AVG'],opj(P['NETWORK_OUTPUT_FOLDER'],'loss',P['SAVE_FILE_NAME']+'_'+time_str()+'.loss_avg'))
            so(P['dm_ctrs'],opj(P['NETWORK_OUTPUT_FOLDER'],'dm_ctrs',P['SAVE_FILE_NAME']+'_'+time_str()+'.dm_ctrs'))
            torch.save(D['optimizer'].state_dict(), opj(P['NETWORK_OUTPUT_FOLDER'],'optimizer',P['SAVE_FILE_NAME']+'_'+time_str()+'.optimizer_state'))
            torch.save(D['net'].state_dict(), opj(P['NETWORK_OUTPUT_FOLDER'],'state_dict',P['SAVE_FILE_NAME']+'_'+time_str()+'.state_dict'))
            print('. . . done saving.')
            P['save_net_timer'].reset()

    D['SAVE_NET'] = _function_save_net
   
    return D




#EOF